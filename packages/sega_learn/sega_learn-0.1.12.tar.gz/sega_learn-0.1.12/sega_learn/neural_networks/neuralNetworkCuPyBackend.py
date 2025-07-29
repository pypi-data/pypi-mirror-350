import warnings

import numpy as np

from .neuralNetworkBase import NeuralNetworkBase
from .schedulers import lr_scheduler_plateau

try:
    import cupy as cp

    from .cupy_utils import *
    from .layers_cupy import *
    from .loss_cupy import *
    from .optimizers_cupy import *

    CUPY_AVAILABLE = True
except ImportError:
    raise ImportError(
        "Numba is not installed. Please install it to use the Numba backend."
    ) from None

try:
    from tqdm.auto import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class CuPyBackendNeuralNetwork(NeuralNetworkBase):
    """CuPyBackendNeuralNetwork is a neural network implementation that uses CuPy for GPU-accelerated computations.

    It inherits from NeuralNetworkBase and provides functionality for forward and backward propagation,
    training, evaluation, and optimization using CuPy arrays and operations.

    Attributes:
        layers (list): List of layers in the neural network.
        compiled (bool): Indicates whether the network is compiled.
        trainable_layers (list): List of layers with trainable parameters.
        layer_outputs (list): Cache for forward pass outputs.
        is_binary (bool): Indicates if the network is for binary classification.
        weights (list): List of weights for trainable layers.
        biases (list): List of biases for trainable layers.
        dWs_cache (list): Cache for weight gradients.
        dbs_cache (list): Cache for bias gradients.
        stream_pool_size (int): Number of CUDA streams for asynchronous processing.
        stream_pool (list): Pool of CUDA streams for asynchronous operations.

    Methods:
        __init__(layers, dropout_rate=0.2, reg_lambda=0.01, activations=None):
            Initializes the CuPyBackendNeuralNetwork with specified layers, dropout rate, regularization, and activations.
        initialize_new_layers():
            Initializes the layers of the neural network with specified sizes and activation functions.
        apply_dropout(X):
            Applies dropout regularization to the input data.
        forward(X, training=True):
            Performs forward propagation through the neural network.
        backward(y):
            Performs backward propagation to calculate gradients for weights and biases.
        _process_batches_async(X_shuffled, y_shuffled, batch_size, weights, biases, activations, dropout_rate, is_binary, reg_lambda, dWs_acc, dbs_acc):
            Processes batches asynchronously using CUDA streams for forward and backward propagation.
        is_not_instance_of_classes(obj, classes):
            Checks if an object is not an instance of any class in a given list of classes.
        train(X_train, y_train, X_val=None, y_val=None, optimizer=None, epochs=100, batch_size=32, early_stopping_threshold=10, lr_scheduler=None, p=True, use_tqdm=True, n_jobs=1, track_metrics=False, track_adv_metrics=False, save_animation=False, save_path="training_animation.mp4", fps=1, dpi=100, frame_every=1):
            Trains the neural network model with specified parameters and options.
        evaluate(X, y):
            Evaluates the model performance on the given input data and labels.
        _evaluate_cupy(y_hat, y_true, is_binary):
            Evaluates model performance using CuPy arrays for predictions and true labels.
        predict(X):
            Predicts the output for the given input data.
        calculate_loss(X, y):
            Calculates the loss with L2 regularization for the given input data and labels.
        _create_optimizer(optimizer_type, learning_rate, JIT=False):
            Helper method to create optimizer instances based on the specified type and learning rate.
    """

    def __init__(self, layers, dropout_rate=0.2, reg_lambda=0.01, activations=None):
        """Initializes the CuPy backend neural network.

        Args:
            layers: (list) - List of layer sizes or Layer objects.
            dropout_rate: (float) - Dropout rate for regularization (default is 0.2).
            reg_lambda: (float) - L2 regularization parameter (default is 0.01).
            activations: (list), optional - List of activation functions for each layer (default is None).

        Returns:
            None
        """
        super().__init__(layers, dropout_rate, reg_lambda, activations)
        self.compiled = False
        # if layers are empty list, initialize them
        if len(self.layers) == 0:
            self.initialize_new_layers()

        # Identify trainable layers
        self.trainable_layers = [
            layer
            for layer in self.layers
            if layer.weights is not None and layer.biases is not None
        ]

        # Cache for forward/backward pass
        self.layer_outputs = None
        self.is_binary = self.layer_sizes[-1] == 1

        # Cache for optimizer update
        self.weights = [layer.weights for layer in self.trainable_layers]
        self.biases = [layer.biases for layer in self.trainable_layers]
        self.activations = [layer.activation for layer in self.layers]

        self.dWs_cache = [cp.zeros_like(w) for w in self.weights]
        self.dbs_cache = [cp.zeros_like(b) for b in self.biases]

        # Create a fixed pool of CUDA streams for asynchronous processing.
        self.stream_pool_size = 8
        self.stream_pool = [
            cp.cuda.Stream(non_blocking=True) for _ in range(self.stream_pool_size)
        ]

    def initialize_new_layers(self):
        """Initializes the layers of the neural network.

        Each layer is created with the specified number of neurons and activation function.
        """
        for i in range(len(self.layer_sizes) - 1):
            self.layers.append(
                CuPyDenseLayer(
                    self.layer_sizes[i], self.layer_sizes[i + 1], self.activations[i]
                )
            )

    def apply_dropout(self, X):
        """Applies dropout regularization to the input data."""
        # Pre-generate random values and apply fused dropout
        random_vals = cp.random.rand(*X.shape)
        return fused_dropout(X, self.dropout_rate, random_vals)

    def forward(self, X, training=True):
        """Performs forward propagation through the neural network.

        Args:
            X (ndarray): Input data of shape (batch_size, input_size).
            training (bool): Whether the network is in training mode (applies dropout).

        Returns:
            ndarray: Output predictions of shape (batch_size, output_size).
        """
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
        """Performs backward propagation to calculate the gradients.

        Args:
            y (ndarray): Target labels of shape (m, output_size).
        """
        # Convert target labels to int32 for Numba compatibility
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

    @staticmethod
    def is_not_instance_of_classes(obj, classes):
        """Checks if an object is not an instance of any class in a list of classes.

        Args:
            obj: The object to check.
            classes: A list of classes.

        Returns:
            bool: True if the object is not an instance of any class in the list of classes, False otherwise.
        """
        return not isinstance(obj, tuple(classes))

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
        track_metrics=False,
        track_adv_metrics=False,
        save_animation=False,
        save_path="training_animation.mp4",
        fps=1,
        dpi=100,
        frame_every=1,
    ):
        """Trains the neural network model.

        Args:
            X_train: (ndarray) - Training data features.
            y_train: (ndarray) - Training data labels.
            X_val: (ndarray) - Validation data features, optional.
            y_val: (ndarray) - Validation data labels, optional.
            optimizer: (Optimizer) - Optimizer for updating parameters (default: JITAdam, lr=0.0001).
            epochs: (int) - Number of training epochs (default: 100).
            batch_size: (int) - Batch size for mini-batch gradient descent (default: 32).
            early_stopping_threshold: (int) - Patience for early stopping (default: 10).
            lr_scheduler: (Scheduler) - Learning rate scheduler (default: None).
            p: (bool) - Whether to print training progress (default: True).
            use_tqdm: (bool) - Whether to use tqdm for progress bar (default: True).
            n_jobs: (int) - Number of jobs for parallel processing (default: 1).
            track_metrics: (bool) - Whether to track training metrics (default: False).
            track_adv_metrics: (bool) - Whether to track advanced metrics (default: False).
            save_animation: (bool) - Whether to save the animation of metrics (default: False).
            save_path: (str) - Path to save the animation file. File extension must be .mp4 or .gif (default: 'training_animation.mp4').
            fps: (int) - Frames per second for the saved animation (default: 1).
            dpi: (int) - DPI for the saved animation (default: 100).
            frame_every: (int) - Capture frame every N epochs (to reduce file size) (default: 1).
        """
        if use_tqdm and not TQDM_AVAILABLE:
            warnings.warn(
                "TQDM is not available. Disabling progress bar.",
                UserWarning,
                stacklevel=2,
            )
            use_tqdm = False

        # If track_adv_metrics is True, X_val and y_val must be provided
        if track_adv_metrics and (X_val is None or y_val is None):
            track_adv_metrics = False
            warnings.warn(
                "track_adv_metrics is True but X_val and y_val are not provided. Disabling track_adv_metrics.",
                UserWarning,
                stacklevel=2,
            )

        # If track_adv_metrics is True, set track_metrics to True
        if track_adv_metrics:
            track_metrics = True

        # If save_animation is True but track_metrics is False, set track_metrics to True, try to set track_adv_metrics to True
        if save_animation and not track_metrics:
            track_metrics = True
            if (X_val is not None) and (y_val is not None):
                track_adv_metrics = True

        if save_animation:
            import os

            from .animation import TrainingAnimator

            # Animation metrics to track
            metrics = ["loss", "accuracy", "precision", "recall", "f1"]
            if lr_scheduler:
                metrics.append("learning_rate")

            # Initialize the animator
            animator = TrainingAnimator(figure_size=(18, 10), dpi=dpi)

            # Initialize animator with metrics
            animator.initialize(metrics, has_validation=(X_val is not None))

            # Setup the training video capture with error handling
            try:
                # Ensure directory exists
                directory = os.path.dirname(save_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)

                animator.setup_training_video(save_path, fps=fps, dpi=dpi)
            except Exception as e:
                print(f"Failed to setup animation: {str(e)}")
                print("Training will continue without animation capture.")
                save_animation = False

        # Default optimizer if not provided
        if optimizer is None:
            optimizer = CuPyAdamOptimizer(learning_rate=0.0001)

        # If optimizer is not a JIT optimizer, convert it to a JIT optimizer
        jit_optimizer_classes = [
            CuPyAdamOptimizer,
            CuPySGDOptimizer,
            CuPyAdadeltaOptimizer,
        ]
        if CuPyBackendNeuralNetwork.is_not_instance_of_classes(
            optimizer, jit_optimizer_classes
        ):
            warnings.warn(
                "Attempting to use a non-JIT optimizer. Converting to a JIT optimizer.",
                UserWarning,
                stacklevel=2,
            )
            try:
                if optimizer.__class__.__name__ == "AdamOptimizer":
                    optimizer = CuPyAdamOptimizer(
                        learning_rate=optimizer.learning_rate,
                        beta1=optimizer.beta1,
                        beta2=optimizer.beta2,
                        epsilon=optimizer.epsilon,
                        reg_lambda=optimizer.reg_lambda,
                    )
                elif optimizer.__class__.__name__ == "SGDOptimizer":
                    optimizer = CuPySGDOptimizer(
                        learning_rate=optimizer.learning_rate,
                        momentum=optimizer.momentum,
                        reg_lambda=optimizer.reg_lambda,
                    )
                elif optimizer.__class__.__name__ == "AdadeltaOptimizer":
                    optimizer = CuPyAdadeltaOptimizer(
                        learning_rate=optimizer.learning_rate,
                        rho=optimizer.rho,
                        epsilon=optimizer.epsilon,
                        reg_lambda=optimizer.reg_lambda,
                    )
                else:
                    raise ValueError(
                        f"Unsupported optimizer: {optimizer.__class__.__name__}"
                    )
            except Exception as e:
                raise ValueError(
                    f"Unable to convert optimizer to a JIT optimizer: {str(e)}. Please use a JIT optimizer."
                ) from None

        # Initialize optimizer
        optimizer.initialize(self.trainable_layers)

        # Track best model for early stopping
        best_loss = float("inf")
        patience_counter = 0
        best_weights = [
            layer.weights.copy() for layer in self.layers if hasattr(layer, "weights")
        ]
        best_biases = [
            layer.biases.copy() for layer in self.layers if hasattr(layer, "biases")
        ]

        # Set metrics to track
        if track_metrics:
            self.train_loss = []
            self.train_accuracy = []
            self.learning_rates = []
            if X_val is not None:
                self.val_loss = []
                self.val_accuracy = []

        # Set advanced metrics to track
        if track_adv_metrics:
            self.train_precision = []
            self.train_recall = []
            self.train_f1 = []
            if X_val is not None:
                self.val_precision = []
                self.val_recall = []
                self.val_f1 = []

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
            for layer in self.trainable_layers:
                layer.zero_grad()

            # Shuffle training data
            indices = cp.random.permutation(X_train_gpu.shape[0])
            X_shuffled = X_train_gpu[indices]
            y_shuffled = y_train_gpu[indices]

            # Prepare layer parameters for function
            weights = [layer.weights for layer in self.trainable_layers]
            biases = [layer.biases for layer in self.trainable_layers]
            activations = [layer.activation for layer in self.layers]

            # Initialize accumulated gradients with zeros
            dWs_zeros = [cp.zeros_like(w) for w in weights]
            dbs_zeros = [cp.zeros_like(b) for b in biases]

            # Get indices of dropout layers
            dropout_layer_indices = [
                i
                for i, layer in enumerate(self.layers)
                if isinstance(layer, CuPyDenseLayer)
            ]
            if len(dropout_layer_indices) == 0:
                dropout_layer_indices = [-1]

            # Process batches based on classification type
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
            optimizer.update_layers(self.trainable_layers, dWs_acc, dbs_acc)

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
                    best_weights = [
                        layer.weights.copy()
                        for layer in self.layers
                        if hasattr(layer, "weights")
                    ]
                    best_biases = [
                        layer.biases.copy()
                        for layer in self.layers
                        if hasattr(layer, "biases")
                    ]
                else:
                    patience_counter += 1
            else:
                # Use training loss for early stopping if no validation set
                if train_loss < best_loss:
                    best_loss = train_loss
                    patience_counter = 0
                    best_weights = [
                        layer.weights.copy()
                        for layer in self.layers
                        if hasattr(layer, "weights")
                    ]
                    best_biases = [
                        layer.biases.copy()
                        for layer in self.layers
                        if hasattr(layer, "biases")
                    ]
                else:
                    patience_counter += 1

            # Store metrics
            if track_metrics:
                self.train_loss.append(train_loss)
                self.train_accuracy.append(train_accuracy)
                self.learning_rates.append(optimizer.learning_rate)
                if X_val_gpu is not None:
                    self.val_loss.append(val_loss)
                    self.val_accuracy.append(val_accuracy)

            # Store advanced metrics
            if track_adv_metrics:
                train_precision, train_recall, train_f1 = (
                    self.calculate_precision_recall_f1(X_train, y_train)
                )
                self.train_precision.append(train_precision)
                self.train_recall.append(train_recall)
                self.train_f1.append(train_f1)
                if X_val_gpu is not None:
                    val_precision, val_recall, val_f1 = (
                        self.calculate_precision_recall_f1(X_val, y_val)
                    )
                    self.val_precision.append(val_precision)
                    self.val_recall.append(val_recall)
                    self.val_f1.append(val_f1)

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
                    lr = optimizer.learning_rate
                    if p and msg:
                        tqdm.write(msg)
                else:
                    msg = lr_scheduler.step(epoch)
                    lr = optimizer.learning_rate
                    if p and msg:
                        tqdm.write(msg)

            # Update animator with metrics
            if save_animation:
                train_metrics = {
                    "loss": train_loss,
                    "accuracy": train_accuracy,
                    "precision": train_precision,
                    "recall": train_recall,
                    "f1": train_f1,
                }
                if lr:
                    train_metrics["learning_rate"] = lr
                animator.update_metrics(train_metrics, validation=False)
                val_metrics = {
                    "loss": val_loss,
                    "accuracy": val_accuracy,
                    "precision": val_precision,
                    "recall": val_recall,
                    "f1": val_f1,
                }
                animator.update_metrics(val_metrics, validation=True)

                # Add frame to the animation if needed
                if epoch % frame_every == 0 or epoch == epochs - 1:
                    try:
                        animator.add_training_frame()
                    except Exception as e:
                        print(f"Failed to add animation frame: {str(e)}")
                        save_animation = False
            # Early stopping
            if patience_counter >= early_stopping_threshold:
                if p and use_tqdm:
                    tqdm.write(f"Early stopping at epoch {epoch + 1}")
                break

        # Restore best weights
        trainable_layers = [layer for layer in self.layers if hasattr(layer, "weights")]
        for i, layer in enumerate(trainable_layers):
            layer.weights = best_weights[i]
            layer.biases = best_biases[i]

        # Finish and save the animation if enabled
        if save_animation:
            try:
                animator.finish_training_video()
                print(f"Animation saved to {save_path}")
            except Exception as e:
                print(f"Failed to finish animation: {str(e)}")

                # Alternative: generate static plot
                try:
                    static_plot_path = save_path.rsplit(".", 1)[0] + ".png"
                    self.plot_metrics(save_dir=static_plot_path)
                    print(f"Static metrics plot saved to {static_plot_path} instead")
                except Exception:
                    pass

        # Return the animator for further use if needed
        return animator if save_animation else None

    def evaluate(self, X, y):
        """Evaluates the model performance on the given data.

        Args:
            X: (np.ndarray or cp.ndarray) - Input feature data.
            y: (np.ndarray or cp.ndarray) - Target labels.

        Returns:
            accuracy: (float) - The accuracy of the model.
            predicted: (np.ndarray) - Predicted labels as a NumPy array.
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
        """CuPy-based function to evaluate model performance.

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
        """Predicts the output for the given input data.

        Args:
            X (ndarray): Input data.

        Returns:
            ndarray: Predicted outputs.
        """
        # Get predictions (forward pass w/o dropout)
        outputs = self.forward(X, training=False)
        return outputs if self.is_binary else np.argmax(outputs, axis=1)

    def calculate_loss(self, X, y):
        """Calculates the loss with L2 regularization.

        Args:
            X (ndarray): Input data.
            y (ndarray): Target labels.

        Returns:
            float: The calculated loss value.
        """
        if not isinstance(X, cp.ndarray):
            X = cp.array(X)
        if not isinstance(y, cp.ndarray):
            y = cp.array(y)

        # Get predictions (forward pass w/o dropout)
        outputs = self.forward(X, training=False)

        # If binary classification use BCE loss
        if self.is_binary:
            loss_fn = CuPyBCEWithLogitsLoss()
            loss = loss_fn(outputs, y.reshape(-1, 1))

        # If multi-class classification use Cross-Entropy loss
        else:
            loss_fn = CuPyCrossEntropyLoss()
            # y_ohe = np.eye(self.layer_sizes[-1])[y]
            loss = loss_fn(outputs, y)

        # Add L2 regularization term
        _weights = [layer.weights for layer in self.layers if hasattr(layer, "weights")]
        l2_reg = self.reg_lambda * sum(cp.sum(w**2) for w in self.weights)
        loss += l2_reg
        return float(loss)

    def _create_optimizer(self, optimizer_type, learning_rate, JIT=False):
        """Helper method to create optimizer instances."""
        if optimizer_type == "Adam":
            return CuPyAdamOptimizer(learning_rate)
        elif optimizer_type == "SGD":
            return CuPySGDOptimizer(learning_rate)
        elif optimizer_type == "Adadelta":
            return CuPyAdadeltaOptimizer(learning_rate)
        else:
            raise ValueError(f"Unknown optimizer type: {optimizer_type}")
