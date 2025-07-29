import cupy as cp
import numpy as np
from tqdm.auto import tqdm

from .cupy_utils import *
from .optimizers import AdadeltaOptimizer, AdamOptimizer, SGDOptimizer
from .schedulers import lr_scheduler_exp, lr_scheduler_plateau, lr_scheduler_step


class NeuralNetwork:
    """
    Neural network class for training and evaluating a custom neural network model.
    Args:
        - layer_sizes (list): A list of integers representing the sizes of each layer in the neural network.
        - dropout_rate (float): The dropout rate to be applied during training. Default is 0.2.
        - reg_lambda (float): The regularization lambda value. Default is 0.01.
        - activations (list): A list of activation functions for each layer. Default is ['relu', 'relu', ... 'softmax'].
    """

    def __init__(
        self, layer_sizes, dropout_rate=0.2, reg_lambda=0.01, activations=None
    ):
        # Initialize neural network parameters
        self.compiled = False

        self.layer_sizes = layer_sizes  # List of layer sizes
        self.dropout_rate = dropout_rate  # Dropout rate
        self.reg_lambda = reg_lambda  # Regularization lambda

        # Set default activation functions if not provided
        if activations is None:
            self.activations = ["relu"] * (len(layer_sizes) - 2) + [
                "softmax"
            ]  # Default to ReLU for hidden layers and Softmax for the output layer
        else:
            self.activations = activations

        # Initialize layers
        self.layers = []
        for i in range(len(layer_sizes) - 1):
            self.layers.append(
                Layer(layer_sizes[i], layer_sizes[i + 1], self.activations[i])
            )

        # Initialize weights
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            weight = (
                cp.random.randn(layer_sizes[i], layer_sizes[i + 1]) * 0.01
            )  # Small random weights
            bias = cp.zeros((1, layer_sizes[i + 1]))  # Initialize biases to zeros
            self.weights.append(weight)
            self.biases.append(bias)

        # Cache for forward/backward pass
        self.layer_outputs = None
        self.is_binary = layer_sizes[-1] == 1

        # Cache for optimizer update
        self.dWs_cache = [cp.zeros_like(w) for w in self.weights]
        self.dbs_cache = [cp.zeros_like(b) for b in self.biases]

        # Create a fixed pool of CUDA streams for asynchronous processing.
        self.stream_pool_size = 8
        self.stream_pool = [
            cp.cuda.Stream(non_blocking=True) for _ in range(self.stream_pool_size)
        ]

    def apply_dropout(self, X):
        # Pre-generate random values and apply fused dropout
        random_vals = cp.random.rand(*X.shape)
        return fused_dropout(X, self.dropout_rate, random_vals)

    def forward(self, X, training=True):
        self.layer_outputs = forward_cupy(
            X,
            self.weights,
            self.biases,
            self.activations,
            self.dropout_rate,
            training,
            self.is_binary,
        )
        return self.layer_outputs[-1]

    def backward(self, y):
        for i in range(len(self.dWs_cache)):
            self.dWs_cache[i].fill(0)
            self.dbs_cache[i].fill(0)
        dWs, dbs = backward_cupy(
            self.layer_outputs,
            cp.array(y),
            self.weights,
            self.activations,
            self.reg_lambda,
            self.is_binary,
            self.dWs_cache,
            self.dbs_cache,
        )
        for i, layer in enumerate(self.layers):
            layer.weight_gradients = dWs[i]
            layer.bias_gradients = dbs[i]

    def _process_batches_async(
        self,
        X_shuffled,
        y_shuffled,
        batch_size,
        weights,
        biases,
        activations,
        dropout_rate,
        is_binary,
        reg_lambda,
        dWs_acc,
        dbs_acc,
    ):
        num_samples = X_shuffled.shape[0]
        num_batches = (num_samples + batch_size - 1) // batch_size
        results = [None] * num_batches

        # Launch asynchronous operations using a fixed stream pool.
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, num_samples)
            X_batch = X_shuffled[start_idx:end_idx]
            y_batch = y_shuffled[start_idx:end_idx]

            # Reuse a stream from the fixed pool in a cyclic fashion.
            stream = self.stream_pool[i % len(self.stream_pool)]
            with stream:
                # Asynchronously perform the forward pass.
                layer_outputs = forward_cupy(
                    X_batch, weights, biases, activations, dropout_rate, True, is_binary
                )
                # Compute gradients asynchronously.
                dWs, dbs = backward_cupy(
                    layer_outputs,
                    y_batch,
                    weights,
                    activations,
                    reg_lambda,
                    is_binary,
                    dWs_acc,
                    dbs_acc,
                )

                # Compute loss and accuracy.
                if is_binary:
                    batch_loss = calculate_loss_from_outputs_binary(
                        layer_outputs[-1], y_batch, reg_lambda, weights
                    )
                else:
                    y_batch_ohe = cp.eye(weights[-1].shape[1])[y_batch]
                    batch_loss = calculate_loss_from_outputs_multi(
                        layer_outputs[-1], y_batch_ohe, reg_lambda, weights
                    )
                batch_accuracy = evaluate_batch(layer_outputs[-1], y_batch, is_binary)

                results[i] = (dWs, dbs, batch_loss, batch_accuracy)

        # Synchronize all streams in the pool.
        for stream in self.stream_pool:
            stream.synchronize()

        # Efficient gradient accumulation on GPU using vectorized operations.
        for j in range(len(dWs_acc)):
            # Stack gradients from all batches along a new axis and sum along that axis.
            dWs_stack = cp.stack([result[0][j] for result in results], axis=0)
            dbs_stack = cp.stack([result[1][j] for result in results], axis=0)
            # Write the mean gradients back into the preallocated accumulators.
            dWs_acc[j][...] = cp.sum(dWs_stack, axis=0) / num_batches
            dbs_acc[j][...] = cp.sum(dbs_stack, axis=0) / num_batches

        # Accumulate loss and accuracy using GPU operations.
        batch_loss_arr = cp.array([result[2] for result in results])
        batch_accuracy_arr = cp.array([result[3] for result in results])
        running_loss = cp.mean(batch_loss_arr)
        running_accuracy = cp.mean(batch_accuracy_arr)

        return dWs_acc, dbs_acc, running_loss, running_accuracy

    def train(
        self,
        X_train,
        y_train,
        X_val=None,
        y_val=None,
        optimizer=None,
        epochs=100,
        batch_size=32,
        early_stopping_threshold=10,
        lr_scheduler=None,
        p=True,
        use_tqdm=True,
        n_jobs=1,
    ):
        """
        Trains the neural network model.
        Args:
            - X_train (ndarray): Training data features.
            - y_train (ndarray): Training data labels.
            - X_val (ndarray): Validation data features, optional.
            - y_val (ndarray): Validation data labels, optional.
            - optimizer (Optimizer): Optimizer for updating parameters (default: Adam, lr=0.0001).
            - epochs (int): Number of training epochs (default: 100).
            - batch_size (int): Batch size for mini-batch gradient descent (default: 32).
            - early_stopping_patience (int): Patience for early stopping (default: 10).
            - lr_scheduler (Scheduler): Learning rate scheduler (default: None).
            - verbose (bool): Whether to print training progress (default: True).
            - use_tqdm (bool): Whether to use tqdm for progress bar (default: True).
            - n_jobs (int): Number of jobs for parallel processing (default: 1).
        """
        # Default optimizer if not provided
        if optimizer is None:
            optimizer = AdamOptimizer(learning_rate=0.0001)

        # Initialize optimizer
        optimizer.initialize(self.layers)

        # Track best model for early stopping
        best_loss = float("inf")
        patience_counter = 0
        best_weights = [layer.weights.copy() for layer in self.layers]
        best_biases = [layer.biases.copy() for layer in self.layers]

        # Move data to GPU
        X_train_gpu = cp.array(X_train)
        y_train_gpu = cp.array(y_train)
        if X_val is not None:
            X_val_gpu = cp.array(X_val)
            y_val_gpu = cp.array(y_val)

        # Training loop with progress bar
        progress_bar = tqdm(range(epochs)) if use_tqdm else range(epochs)
        for epoch in progress_bar:
            # Reset gradients
            for layer in self.layers:
                layer.zero_grad()

            # Shuffle training data
            indices = cp.random.permutation(X_train_gpu.shape[0])
            X_shuffled = X_train_gpu[indices]
            y_shuffled = y_train_gpu[indices]

            # Prepare layer parameters for JIT function
            weights = [layer.weights for layer in self.layers]
            biases = [layer.biases for layer in self.layers]
            activations = [layer.activation for layer in self.layers]

            # Initialize accumulated gradients with zeros
            dWs_zeros = [cp.zeros_like(w) for w in weights]
            dbs_zeros = [cp.zeros_like(b) for b in biases]

            # Process all batches in parallel and get averaged gradients, loss
            dWs_acc, dbs_acc, train_loss, train_accuracy = self._process_batches_async(
                X_shuffled,
                y_shuffled,
                batch_size,
                weights,
                biases,
                activations,
                self.dropout_rate,
                self.is_binary,
                self.reg_lambda,
                dWs_zeros,
                dbs_zeros,
            )

            # Update weights and biases using the optimizer
            optimizer.update_layers(self.layers, dWs_acc, dbs_acc)

            # Validation metrics
            val_metrics = ""
            if X_val is not None:
                val_loss = self.calculate_loss(X_val_gpu, y_val_gpu)
                val_accuracy, _ = self.evaluate(X_val_gpu, y_val_gpu)
                val_metrics = f", Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}"

                # Early stopping check
                if val_loss < best_loss:
                    best_loss = val_loss
                    patience_counter = 0
                    # Save best weights
                    best_weights = [layer.weights.copy() for layer in self.layers]
                    best_biases = [layer.biases.copy() for layer in self.layers]
                else:
                    patience_counter += 1
            else:
                # Use training loss for early stopping if no validation set
                if train_loss < best_loss:
                    best_loss = train_loss
                    patience_counter = 0
                    best_weights = [layer.weights.copy() for layer in self.layers]
                    best_biases = [layer.biases.copy() for layer in self.layers]
                else:
                    patience_counter += 1

            # Update progress bar or print metrics
            if p:
                if use_tqdm and isinstance(progress_bar, tqdm):
                    progress_bar.set_description(
                        f"Epoch {epoch + 1}/{epochs} - Loss: {train_loss:.4f}, Acc: {train_accuracy:.4f}{val_metrics}"
                    )
                else:
                    print(
                        f"Epoch {epoch + 1}/{epochs} - Loss: {train_loss:.4f}, Acc: {train_accuracy:.4f}{val_metrics}"
                    )

            # Learning rate scheduler step
            if lr_scheduler:
                if isinstance(lr_scheduler, lr_scheduler_plateau):
                    msg = lr_scheduler.step(
                        epoch, train_loss if X_val is None else val_loss
                    )
                    if p and msg:
                        tqdm.write(msg)
                else:
                    msg = lr_scheduler.step(epoch)
                    if p and msg:
                        tqdm.write(msg)

            # Early stopping
            if patience_counter >= early_stopping_threshold:
                if p and use_tqdm:
                    tqdm.write(f"Early stopping at epoch {epoch + 1}")
                break

        # Restore best weights
        for i, layer in enumerate(self.layers):
            layer.weights = best_weights[i]
            layer.biases = best_biases[i]

    def calculate_loss(self, X, y, class_weights=None):
        # Avoid unnecessary conversion if inputs are already CuPy arrays.
        if not isinstance(X, cp.ndarray):
            X = cp.array(X)
        if not isinstance(y, cp.ndarray):
            y = cp.array(y)
        outputs = self.forward(X, training=False)
        if self.is_binary:
            loss = calculate_bce_with_logits_loss(outputs, y.reshape(-1, 1))
        else:
            if y.ndim == 1:
                y = cp.eye(self.layer_sizes[-1])[y]
            loss = calculate_cross_entropy_loss(outputs, y)
        l2_reg = self.reg_lambda * sum(cp.sum(w**2) for w in self.weights)
        return float(loss + l2_reg)

    def evaluate(self, X, y):
        """
        Evaluates the model performance.
        Args:
            - X (ndarray): Input data (NumPy or CuPy array)
            - y (ndarray): Target labels (NumPy or CuPy array)
        Returns:
            - accuracy (float): Model accuracy
            - predicted (ndarray): Predicted labels (NumPy array)
        """
        # Convert inputs to GPU arrays only if necessary.
        if not isinstance(X, cp.ndarray):
            X = cp.array(X)
        if not isinstance(y, cp.ndarray):
            y = cp.array(y)
        y_hat = self.forward(X, training=False)
        accuracy, predicted = self._evaluate_cupy(y_hat, y, self.is_binary)
        return float(accuracy), cp.asnumpy(predicted)

    @staticmethod
    def _evaluate_cupy(y_hat, y_true, is_binary):
        """
        CuPy-based function to evaluate model performance.
        Args:
            y_hat (cp.ndarray): Model predictions (CuPy array).
            y_true (cp.ndarray): True labels (CuPy array).
            is_binary (bool): Whether the model is binary or multi-class.
        Returns:
            tuple: Accuracy (CuPy scalar) and predicted labels (CuPy array).
        """
        if is_binary:
            predicted = (y_hat > 0.5).astype(cp.int32).ravel()
            accuracy = cp.mean(predicted == y_true.ravel())
        else:
            predicted = cp.argmax(y_hat, axis=1).astype(cp.int32)
            accuracy = cp.mean(predicted == y_true)
        return accuracy, predicted

    def predict(self, X):
        """
        Generate predictions for input data.
        Args:
            - X (ndarray): Input data
        Returns:
            - predictions: Model predictions (class probabilities or labels)
        """
        # Get raw predictions
        outputs = self.forward(X, training=False)

        # For binary classification, return class probabilities
        if self.is_binary:
            return outputs
        # For multiclass, return class labels
        else:
            return np.argmax(outputs, axis=1)

    def _create_optimizer(self, optimizer_type, learning_rate):
        """Helper method to create optimizer instances."""
        if optimizer_type == "Adam":
            return AdamOptimizer(learning_rate)
        elif optimizer_type == "SGD":
            return SGDOptimizer(learning_rate)
        elif optimizer_type == "Adadelta":
            return AdadeltaOptimizer(learning_rate)
        else:
            raise ValueError(f"Unknown optimizer type: {optimizer_type}")

    def create_scheduler(self, scheduler_type, optimizer, **kwargs):
        """Creates a learning rate scheduler."""
        if scheduler_type == "step":
            return lr_scheduler_step(optimizer, **kwargs)
        elif scheduler_type == "plateau":
            return lr_scheduler_plateau(optimizer, **kwargs)
        elif scheduler_type == "exp":
            return lr_scheduler_exp(optimizer, **kwargs)
        else:
            raise ValueError(f"Unknown scheduler type: {scheduler_type}")


class Layer:
    """
    Initializes a Layer object.
    Args:
        input_size (int): The size of the input to the layer.
        output_size (int): The size of the output from the layer.
        activation (str): The activation function to be used in the layer.
    """

    def __init__(self, input_size, output_size, activation="relu"):
        # He initialization for weights
        if activation in ["relu", "leaky_relu"]:
            scale = cp.sqrt(2.0 / input_size)
        else:
            scale = cp.sqrt(1.0 / input_size)

        self.weights = cp.random.randn(input_size, output_size) * scale
        self.biases = cp.zeros((1, output_size))
        self.activation = activation
        self.weight_gradients = cp.zeros(
            (input_size, output_size)
        )  # Initialize weight gradients to zeros
        self.bias_gradients = cp.zeros(
            (1, output_size)
        )  # Initialize bias gradients to zeros

    def zero_grad(self):
        """Reset the gradients of the weights and biases to zero."""
        self.weight_gradients = cp.zeros_like(self.weight_gradients)
        self.bias_gradients = cp.zeros_like(self.bias_gradients)

    def activate(self, Z):
        """Apply activation function."""
        activation_functions = {
            "relu": Activation.relu,
            "leaky_relu": Activation.leaky_relu,
            "tanh": Activation.tanh,
            "sigmoid": Activation.sigmoid,
            "softmax": Activation.softmax,
        }

        if self.activation in activation_functions:
            return activation_functions[self.activation](Z)
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")

    def activation_derivative(self, Z):
        """Apply activation derivative."""
        if self.activation == "relu":
            return Activation.relu_derivative(Z)
        elif self.activation == "leaky_relu":
            return Activation.leaky_relu_derivative(Z)
        elif self.activation == "tanh":
            return Activation.tanh_derivative(Z)
        elif self.activation == "sigmoid":
            return Activation.sigmoid_derivative(Z)
        elif self.activation == "softmax":
            # Softmax derivative handled in loss function
            return cp.ones_like(Z)  # Identity for compatibility
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")


class Activation:
    @staticmethod
    def relu(z):
        """
        ReLU (Rectified Linear Unit) activation function: f(z) = max(0, z)
        Returns the input directly if it's positive, otherwise returns 0.
        """
        return cp.maximum(0, z)

    @staticmethod
    def relu_derivative(z):
        """
        Derivative of the ReLU function: f'(z) = 1 if z > 0, else 0
        Returns 1 for positive input, and 0 for negative input.
        """
        return (z > 0).astype(cp.float32)

    @staticmethod
    def leaky_relu(z, alpha=0.01):
        """
        Leaky ReLU activation function: f(z) = z if z > 0, else alpha * z
        Allows a small, non-zero gradient when the input is negative to address the dying ReLU problem.
        """
        return cp.where(z > 0, z, alpha * z)

    @staticmethod
    def leaky_relu_derivative(z, alpha=0.01):
        """
        Derivative of the Leaky ReLU function: f'(z) = 1 if z > 0, else alpha
        Returns 1 for positive input, and alpha for negative input.
        """
        return cp.where(z > 0, 1, alpha)

    @staticmethod
    def tanh(z):
        """
        Hyperbolic tangent (tanh) activation function: f(z) = (exp(z) - exp(-z)) / (exp(z) + exp(-z))
        Maps input to the range [-1, 1], typically used for normalized input.
        """
        return cp.tanh(z)

    @staticmethod
    def tanh_derivative(z):
        """
        Derivative of the tanh function: f'(z) = 1 - tanh(z)^2
        Used for backpropagation through the tanh activation.
        """
        return 1 - cp.tanh(z) ** 2

    @staticmethod
    def sigmoid(z):
        """
        Sigmoid activation function: f(z) = 1 / (1 + exp(-z))
        Maps input to the range [0, 1], commonly used for binary classification.
        """
        return 1 / (1 + cp.exp(-z))

    @staticmethod
    def sigmoid_derivative(z):
        """
        Derivative of the sigmoid function: f'(z) = sigmoid(z) * (1 - sigmoid(z))
        Used for backpropagation through the sigmoid activation.
        """
        sig = Activation.sigmoid(z)
        return sig * (1 - sig)

    @staticmethod
    def softmax(z):
        """
        Softmax activation function: f(z)_i = exp(z_i) / sum(exp(z_j)) for all j
        Maps input into a probability distribution over multiple classes. Used for multiclass classification.
        """
        # Subtract the max value from each row to prevent overflow (numerical stability)
        exp_z = cp.exp(z - cp.max(z, axis=1, keepdims=True))
        return exp_z / cp.sum(exp_z, axis=1, keepdims=True)
