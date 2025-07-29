import sys
import warnings

import numpy as np

from .loss import HuberLoss, MeanAbsoluteErrorLoss
from .neuralNetworkBase import NeuralNetworkBase
from .schedulers import lr_scheduler_plateau

try:
    from .layers_jit import *
    from .loss_jit import *
    from .numba_utils import *
    from .optimizers_jit import *

    NUMBA_AVAILABLE = True
except ImportError:
    raise ImportError(
        "Numba is not installed. Please install it to use the Numba backend."
    ) from None

try:
    from tqdm.auto import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

# Notes: Using different JITLayers is currently broken, IDEAS:
# ---------------------------------------------------------------------------------------
# 1. Split the Layers into Homogeneous Lists
# Separate your layers by type and then initialize/update them separately.
# trainable_conv_layers = [layer for layer in self.layers if isinstance(layer, JITConvLayer)]
# trainable_dense_layers = [layer for layer in self.layers if isinstance(layer, JITDenseLayer)]
# 2. Refactor to a Single Layer Type
# Refactoring code so that both convolutional and dense layers share a unified interface and are implemented as a single jitclass type.
# Store all layers in one homogeneous list.


class NumbaBackendNeuralNetwork(NeuralNetworkBase):
    """A neural network implementation using Numba for Just-In-Time (JIT) compilation to optimize performance.

    This class supports forward and backward propagation, training, evaluation, and hyperparameter tuning
    with various optimizers and activation functions.

    Attributes:
        compiled (bool): Indicates whether Numba functions are compiled.
        trainable_layers (list): Layers with trainable parameters (weights and biases).
        progress_bar (bool): Whether to display a progress bar during training.

    Methods:
        __init__(layers, dropout_rate, reg_lambda, activations, compile_numba, progress_bar):
            Initializes the neural network with the specified parameters.
        store_init_layers():
            Stores the initial layers and their parameters for restoration after initialization.
        restore_layers():
            Restores the layers and their parameters after initialization.
        initialize_new_layers():
            Initializes the layers of the neural network with specified sizes and activation functions.
        forward(X, training):
            Performs forward propagation through the neural network.
        backward(y):
            Performs backward propagation to calculate gradients.
        is_not_instance_of_classes(obj, classes):
            Checks if an object is not an instance of any class in a list of classes.
        train(X_train, y_train, X_val, y_val, optimizer, epochs, batch_size, early_stopping_threshold,
              lr_scheduler, p, use_tqdm, n_jobs, track_metrics, track_adv_metrics, save_animation,
              save_path, fps, dpi, frame_every):
            Trains the neural network model with the specified parameters.
        evaluate(X, y):
            Evaluates the neural network on the given data and returns accuracy and predictions.
        predict(X):
            Predicts the output for the given input data.
        calculate_loss(X, y):
            Calculates the loss with L2 regularization.
        _create_optimizer(optimizer_type, learning_rate, JIT):
            Helper method to create optimizer instances.
        tune_hyperparameters(X_train, y_train, X_val, y_val, param_grid, layer_configs, optimizer_types,
                             lr_range, epochs, batch_size):
            Performs hyperparameter tuning using grid search.
        compile_numba_functions(progress_bar):
            Compiles all Numba JIT functions to improve performance.
    """

    def __init__(
        self,
        layers,
        dropout_rate=0.2,
        reg_lambda=0.01,
        activations=None,
        loss_function=None,
        regressor=False,
        compile_numba=True,
        progress_bar=True,
    ):
        """Initializes the Numba backend neural network.

        Args:
            layers: (list) - List of layer sizes or Layer objects.
            dropout_rate: (float) - Dropout rate for regularization.
            reg_lambda: (float) - L2 regularization parameter.
            activations: (list) - List of activation functions for each layer.
            loss_function: (callable) optional - Custom loss function (default: selects based on task).
            regressor: (bool) - Whether the model is a regressor (default is False).
            compile_numba: (bool) - Whether to compile Numba functions.
            progress_bar: (bool) - Whether to display a progress bar.
        """
        super().__init__(
            layers, dropout_rate, reg_lambda, activations, loss_function, regressor
        )
        self.compiled = False

        # if layers are empty list, initialize them
        if len(self.layers) == 0:
            self.initialize_new_layers()

        # Identify trainable layers
        self.trainable_layers = [
            layer
            for layer in self.layers
            if hasattr(layer, "weights") and hasattr(layer, "biases")
        ]

        # Check if the provided loss_function is already a JIT version
        is_jit_loss = isinstance(
            self.loss_function,
            (
                JITMeanSquaredErrorLoss,
                JITMeanAbsoluteErrorLoss,
                JITHuberLoss,
                JITBCEWithLogitsLoss,
                JITCrossEntropyLoss,
            ),
        )

        if not is_jit_loss:
            # If not a JIT version or None, determine the default JIT loss
            if self.is_regressor:
                if isinstance(self.loss_function, MeanAbsoluteErrorLoss):
                    self.loss_function = JITMeanAbsoluteErrorLoss()
                elif isinstance(self.loss_function, HuberLoss):
                    # Keep the delta from the original if possible
                    delta = getattr(self.loss_function, "delta", 1.0)
                    self.loss_function = JITHuberLoss(delta=delta)
                else:  # Default to MSE for regression (or if original was MSELoss/None)
                    self.loss_function = JITMeanSquaredErrorLoss()
            elif self.is_binary:
                # Default to JIT BCE for binary (handles None or BCEWithLogitsLoss)
                self.loss_function = JITBCEWithLogitsLoss()
            else:
                # Default to JIT CrossEntropy for multi-class
                self.loss_function = JITCrossEntropyLoss()
            if loss_function is not None:  # Warn if we converted a non-JIT function
                warnings.warn(
                    f"Converted non-JIT loss function {type(loss_function).__name__} to {type(self.loss_function).__name__} for Numba backend.",
                    stacklevel=2,
                )

        # Flag to only warn once for HuberLoss
        self.warn_huber_delta = False

        # Progress bar setup
        if progress_bar and not TQDM_AVAILABLE:
            warnings.warn(
                "tqdm is not installed. Progress bar will not be displayed.",
                stacklevel=2,
            )
            self.progress_bar = False
        else:
            self.progress_bar = progress_bar

        # Compile Numba functions if requested
        if compile_numba and not self.compiled:
            self.store_init_layers()
            try:
                self.compile_numba_functions(self.progress_bar)
                self.compiled = True
            except Exception as e:
                warnings.warn(
                    f"Numba compilation failed: {e}. Running without JIT acceleration.",
                    stacklevel=2,
                )
                self.compiled = False  # Ensure flag is false if compilation fails
            finally:
                # Always restore layers, even if compilation failed
                self.restore_layers()

    def store_init_layers(self):
        """Stores the layers to restore after initialization."""
        self._layers = self.layers.copy()
        self._weights = [
            layer.weights.copy() for layer in self.layers if hasattr(layer, "weights")
        ]
        self._biases = [
            layer.biases.copy() for layer in self.layers if hasattr(layer, "biases")
        ]

        self.weights = [
            layer.weights.copy() for layer in self.layers if hasattr(layer, "weights")
        ]
        self.biases = [
            layer.biases.copy() for layer in self.layers if hasattr(layer, "biases")
        ]
        self.dWs_cache = [np.zeros_like(w) for w in self.weights]
        self.dbs_cache = [np.zeros_like(b) for b in self.biases]

    def restore_layers(self):
        """Restores the layers after initialization."""
        self.layers = self._layers.copy()
        self.weights = [
            layer.weights.copy() for layer in self.layers if hasattr(layer, "weights")
        ]
        self.biases = [
            layer.biases.copy() for layer in self.layers if hasattr(layer, "biases")
        ]

    def initialize_new_layers(self):
        """Initializes the layers of the neural network.

        Each layer is created with the specified number of neurons and activation function.
        """
        for i in range(len(self.layer_sizes) - 1):
            self.layers.append(
                JITDenseLayer(
                    self.layer_sizes[i], self.layer_sizes[i + 1], self.activations[i]
                )
            )
            weight = (
                np.random.randn(self.layer_sizes[i], self.layer_sizes[i + 1]) * 0.01
            )
            bias = np.zeros((1, self.layer_sizes[i + 1]))
            self.weights.append(weight)
            self.biases.append(bias)
        self.dWs_cache = [np.zeros_like(w) for w in self.weights]
        self.dbs_cache = [np.zeros_like(b) for b in self.biases]

    def forward(self, X, training=True):
        """Performs forward propagation through the neural network.

        Args:
            X (ndarray): Input data of shape (batch_size, input_size).
            training (bool): Whether the network is in training mode (applies dropout).

        Returns:
            ndarray: Output predictions of shape (batch_size, output_size).
        """
        # Convert input to float64 for Numba compatibility
        self.layer_outputs = [X]
        A = X.astype(np.float64)

        output = None
        for i, layer in enumerate(self.layers):
            A = layer.forward(A)

            # If last layer, store output for return
            if i == len(self.layers) - 1:
                output = A

            if training and self.dropout_rate > 0 and isinstance(layer, JITDenseLayer):
                A = apply_dropout_jit(A, self.dropout_rate)
            self.layer_outputs.append(A)

        return output

    def backward(self, y):
        """Performs backward propagation to calculate the gradients.

        Args:
            y (ndarray): Target labels of shape (m, output_size).
        """
        # Convert target labels to int32 for Numba compatibility
        y = y.astype(np.int32)
        m = y.shape[0]
        outputs = self.layer_outputs[-1]

        if self.is_binary:
            y = y.reshape(-1, 1).astype(np.float64)
            dA = -(y / (outputs + 1e-15) - (1 - y) / (1 - outputs + 1e-15))
        else:
            dA = outputs.copy()
            for i in range(m):
                dA[i, y[i]] -= 1

        for i in reversed(range(len(self.layers))):
            dA = self.layers[i].backward(dA, self.reg_lambda)

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
            optimizer = JITAdamOptimizer(learning_rate=0.0001)

        # If optimizer is not a JIT optimizer, convert it to a JIT optimizer
        jit_optimizer_classes = [
            JITAdamOptimizer,
            JITSGDOptimizer,
            JITAdadeltaOptimizer,
        ]
        if NumbaBackendNeuralNetwork.is_not_instance_of_classes(
            optimizer, jit_optimizer_classes
        ):
            warnings.warn(
                "Attempting to use a non-JIT optimizer. Converting to a JIT optimizer.",
                UserWarning,
                stacklevel=2,
            )
            try:
                if optimizer.__class__.__name__ == "AdamOptimizer":
                    optimizer = JITAdamOptimizer(
                        learning_rate=optimizer.learning_rate,
                        beta1=optimizer.beta1,
                        beta2=optimizer.beta2,
                        epsilon=optimizer.epsilon,
                        reg_lambda=optimizer.reg_lambda,
                    )
                elif optimizer.__class__.__name__ == "SGDOptimizer":
                    optimizer = JITSGDOptimizer(
                        learning_rate=optimizer.learning_rate,
                        momentum=optimizer.momentum,
                        reg_lambda=optimizer.reg_lambda,
                    )
                elif optimizer.__class__.__name__ == "AdadeltaOptimizer":
                    optimizer = JITAdadeltaOptimizer(
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

        # Number of threads for parallel processing
        # If n_jobs > 1, use that many threads, otherwise let Numba decide
        if n_jobs > 1:
            import os

            os.environ["NUMBA_NUM_THREADS"] = str(n_jobs)

        # Set metrics to track
        if track_metrics:
            self.train_loss = []
            self.train_metric = []  # Stores MSE for regression, Accuracy for classification
            self.learning_rates = []
            if X_val is not None:
                self.val_loss = []
                self.val_metric = []

        # Remove tracking for precision/recall/f1 if it's a regressor
        if self.is_regressor:
            track_adv_metrics = False

        # Set advanced metrics to track
        if track_adv_metrics:
            self.train_precision = []
            self.train_recall = []
            self.train_f1 = []
            if X_val is not None:
                self.val_precision = []
                self.val_recall = []
                self.val_f1 = []

        lr = optimizer.learning_rate  # Initialize lr for animation tracking

        # Training loop with progress bar
        progress_bar = tqdm(range(epochs)) if use_tqdm else range(epochs)
        for epoch in progress_bar:
            # Reset gradients
            for layer in self.trainable_layers:
                layer.zero_grad()

            # Shuffle training data
            indices = np.arange(X_train.shape[0])
            np.random.shuffle(indices)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            # Prepare layer parameters for JIT function
            weights = [layer.weights for layer in self.trainable_layers]
            biases = [layer.biases for layer in self.trainable_layers]

            # Initialize accumulated gradients with zeros
            dWs_zeros = [np.zeros_like(w) for w in weights]
            dbs_zeros = [np.zeros_like(b) for b in biases]

            # Get indices of dropout layers
            dropout_layer_indices = [
                i
                for i, layer in enumerate(self.layers)
                if isinstance(layer, JITDenseLayer)
            ]
            if len(dropout_layer_indices) == 0:
                dropout_layer_indices = [-1]

            # Process batches based on classification type
            if self.is_regressor:
                # Ensure y_shuffled has the correct shape and type for regression
                y_shuffled_reg = y_shuffled.astype(np.float64)
                if y_shuffled_reg.ndim == 1:
                    y_shuffled_reg = y_shuffled_reg.reshape(-1, 1)

                jit_loss_calculator = self._get_jit_loss_calculator()
                if not jit_loss_calculator:
                    # Should not happen if initialized correctly, but handle defensively
                    raise TypeError(
                        "Could not find appropriate JIT loss calculator for regression."
                    )

                dWs_acc, dbs_acc, train_loss, train_metric_value = (
                    process_batches_regression_jit(
                        X_shuffled,
                        y_shuffled_reg,
                        batch_size,
                        self.layers,
                        self.dropout_rate,
                        dropout_layer_indices,
                        self.reg_lambda,
                        dWs_zeros,
                        dbs_zeros,
                        jit_loss_calculator,
                    )
                )
            elif self.is_binary:
                dWs_acc, dbs_acc, train_loss, train_metric_value = (
                    process_batches_binary(
                        X_shuffled,
                        y_shuffled,
                        batch_size,
                        self.layers,
                        self.dropout_rate,
                        dropout_layer_indices,
                        self.reg_lambda,
                        dWs_zeros,
                        dbs_zeros,
                    )
                )
            else:
                dWs_acc, dbs_acc, train_loss, train_metric_value = (
                    process_batches_multi(
                        X_shuffled,
                        y_shuffled,
                        batch_size,
                        self.layers,
                        self.dropout_rate,
                        dropout_layer_indices,
                        self.reg_lambda,
                        dWs_zeros,
                        dbs_zeros,
                    )
                )

            # Update weights and biases using the optimizer
            optimizer.update_layers(self.trainable_layers, dWs_acc, dbs_acc)

            # Validation metrics
            val_metrics_str = ""
            if X_val is not None:
                val_loss = self.calculate_loss(X_val, y_val)
                val_metric_value, _ = self.evaluate(X_val, y_val)
                val_metric_label = "MSE" if self.is_regressor else "Acc"
                val_metrics_str = f", Val Loss: {val_loss:.4f}, Val {val_metric_label}: {val_metric_value:.4f}"

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
                self.train_metric.append(train_metric_value)
                if lr_scheduler:  # Store LR only if scheduler exists
                    self.learning_rates.append(optimizer.learning_rate)
                if X_val is not None:
                    self.val_loss.append(val_loss)
                    self.val_metric.append(val_metric_value)

            # Store advanced metrics
            if track_adv_metrics and not self.is_regressor:
                train_precision, train_recall, train_f1 = (
                    self.calculate_precision_recall_f1(X_train, y_train)
                )
                self.train_precision.append(train_precision)
                self.train_recall.append(train_recall)
                self.train_f1.append(train_f1)
                if X_val is not None:
                    val_precision, val_recall, val_f1 = (
                        self.calculate_precision_recall_f1(X_val, y_val)
                    )
                    self.val_precision.append(val_precision)
                    self.val_recall.append(val_recall)
                    self.val_f1.append(val_f1)

            # Update progress bar or print metrics
            metric_label = "MSE" if self.is_regressor else "Acc"
            train_metrics_display = f"Loss: {train_loss:.4f}, Train {metric_label}: {train_metric_value:.4f}"
            if p:
                log_message = f"Epoch {epoch + 1}/{epochs} - {train_metrics_display}{val_metrics_str}"
                if use_tqdm and isinstance(progress_bar, tqdm):
                    progress_bar.set_description(log_message)
                else:
                    print(log_message)

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
                # Prepare metrics dictionary for animator
                epoch_train_metrics = {
                    "loss": train_loss,
                    (
                        "metric",
                        "MSE" if self.is_regressor else "Accuracy",
                    ): train_metric_value,  # Use tuple for label
                }
                if not self.is_regressor and track_adv_metrics:
                    epoch_train_metrics.update(
                        {
                            "precision": train_precision,
                            "recall": train_recall,
                            "f1": train_f1,
                        }
                    )
                if lr_scheduler:
                    epoch_train_metrics["learning_rate"] = lr

                animator.update_metrics(epoch_train_metrics, validation=False)

                if X_val is not None:
                    epoch_val_metrics = {
                        "loss": val_loss,
                        (
                            "metric",
                            "MSE" if self.is_regressor else "Accuracy",
                        ): val_metric_value,
                    }
                    if not self.is_regressor and track_adv_metrics:
                        epoch_val_metrics.update(
                            {
                                "precision": val_precision,
                                "recall": val_recall,
                                "f1": val_f1,
                            }
                        )
                    animator.update_metrics(epoch_val_metrics, validation=True)

                # Add frame to the animation if needed
                if epoch % frame_every == 0 or epoch == epochs - 1:
                    try:
                        animator.add_training_frame()
                    except Exception as e:
                        print(f"Failed to add animation frame: {str(e)}")
                        save_animation = (
                            False  # Disable animation if adding frame fails
                        )

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
        """Evaluates the neural network on the given data.

        Args:
            X (ndarray): Input data.
            y (ndarray): Target labels.

        Returns:
            tuple: Accuracy and predicted labels.
        """
        y_hat = self.forward(X, training=False)
        y = np.asarray(y)  # Ensure y is numpy array

        if self.is_regressor:
            # Ensure y has the correct shape for regression loss calculation
            y = y.astype(np.float64)
            if y.ndim == 1:
                y = y.reshape(-1, 1)
            if y_hat.shape != y.shape:
                raise ValueError(
                    f"evaluate (regression) shape mismatch: y_true {y.shape} vs y_pred {y_hat.shape}"
                )

            # The loss_function object's calculate_loss method calls the @njit helper
            metric = self.loss_function.calculate_loss(y_hat, y)
            predicted = y_hat

        elif self.is_binary:
            # Use the existing evaluate_jit for classification accuracy
            metric, predicted = evaluate_jit(y_hat, y.astype(np.int32), True)
            predicted = predicted.reshape(y.shape)  # Ensure correct output shape
        else:
            # Use the existing evaluate_jit for classification accuracy
            metric, predicted = evaluate_jit(y_hat, y.astype(np.int32), False)
            # No need to reshape predicted here as evaluate_jit returns 1D argmax indices

        return metric, predicted

    def predict(self, X):
        """Predicts the output for the given input data.

        Args:
            X (ndarray): Input data.

        Returns:
            ndarray: Predicted outputs.
        """
        # Get predictions (forward pass w/o dropout)
        outputs = self.forward(X, training=False)
        if self.is_regressor:
            return outputs.flatten()  # Ensure 1D output for regression
        elif self.is_binary:
            return (outputs > 0.5).astype(int)
        else:
            return np.argmax(outputs, axis=1)

    def calculate_loss(self, X, y):
        """Calculates the loss with L2 regularization.

        Args:
            X (ndarray): Input data.
            y (ndarray): Target labels.

        Returns:
            float: The calculated loss value.
        """
        outputs = self.forward(X, training=False)
        y = np.asarray(y)  # Ensure numpy array

        if self.is_regressor:
            # Ensure y has the correct shape for regression loss calculation
            y = y.astype(np.float64)
            if y.ndim == 1:
                y = y.reshape(-1, 1)
            if outputs.shape != y.shape:
                raise ValueError(
                    f"calculate_loss (regression) shape mismatch: y_true {y.shape} vs y_pred {outputs.shape}"
                )
            loss = self.loss_function.calculate_loss(outputs, y)
        elif self.is_binary:
            loss = self.loss_function.calculate_loss(
                outputs, y.reshape(-1, 1).astype(np.float64)
            )
        else:
            y_ohe = np.eye(self.layer_sizes[-1])[y.astype(np.int32)]
            loss = self.loss_function.calculate_loss(outputs, y_ohe)

        # Add L2 regularization term
        weights = [
            layer.weights
            for layer in self.trainable_layers
            if hasattr(layer, "weights")
        ]
        l2_reg = self.reg_lambda * compute_l2_reg(weights)
        loss += l2_reg
        return float(loss)

    def _create_optimizer(self, optimizer_type, learning_rate, JIT=False):
        """Helper method to create optimizer instances."""
        if optimizer_type == "Adam":
            return JITAdamOptimizer(learning_rate)
        elif optimizer_type == "SGD":
            return JITSGDOptimizer(learning_rate)
        elif optimizer_type == "Adadelta":
            return JITAdadeltaOptimizer(learning_rate)
        else:
            raise ValueError(f"Unknown optimizer type: {optimizer_type}")

    def tune_hyperparameters(
        self,
        X_train,
        y_train,
        X_val,
        y_val,
        param_grid,
        layer_configs=None,
        optimizer_types=None,
        lr_range=(0.0001, 0.01, 5),
        epochs=30,
        batch_size=32,
    ):
        """Performs hyperparameter tuning using grid search.

        Args:
            X_train: (np.ndarray) - Training feature data.
            y_train: (np.ndarray) - Training target data.
            X_val: (np.ndarray) - Validation feature data.
            y_val: (np.ndarray) - Validation target data.
            param_grid: (dict) - Dictionary of parameters to try.
            layer_configs: (list), optional - List of layer configurations (default is None).
            optimizer_types: (list), optional - List of optimizer types (default is None).
            lr_range: (tuple), optional - (min_lr, max_lr, num_steps) for learning rates (default is (0.0001, 0.01, 5)).
            epochs: (int), optional - Max epochs for each trial (default is 30).
            batch_size: (int), optional - Batch size for training (default is 32).

        Returns:
            best_params: (dict) - Best hyperparameters found.
            best_accuracy: (float) - Best validation accuracy.
        """
        if not TQDM_AVAILABLE:
            # TODO: Make tqdm optional for hyperparameter tuning
            raise ImportError(
                "TQDM is currently required for hyperparameter tuning. Please install it using 'pip install tqdm'."
            )

        import warnings
        from itertools import product

        warnings.filterwarnings("ignore")

        # Default values if not provided
        if layer_configs is None:
            layer_configs = [[64], [128], [64, 32]]

        if optimizer_types is None:
            optimizer_types = ["Adam", "SGD"]

        # Output size based on target data
        output_size = (
            1 if len(y_train.shape) == 1 or y_train.shape[1] == 1 else y_train.max() + 1
        )

        # Generate learning rates
        min_lr, max_lr, num_steps = lr_range
        lr_options = np.logspace(np.log10(min_lr), np.log10(max_lr), num_steps).tolist()

        # Extract parameter combinations
        if sys.version_info >= (3, 10):
            keys, values = zip(*param_grid.items(), strict=False)
        else:
            keys, values = zip(
                *param_grid.items()
            )  # Python < 3.10 doesn't support 'strict'

        # Calculate total iterations for progress tracking
        total_iterations = (
            len(layer_configs)
            * len(lr_options)
            * len(optimizer_types)
            * np.prod([len(value) for value in values])
        )

        # Track best results
        best_accuracy = 0
        best_params = {}
        best_optimizer_type = None

        # Grid search with progress bar
        with tqdm(total=total_iterations, desc="Tuning Hyperparameters") as pbar:
            # Iterate through all combinations
            for optimizer_type in optimizer_types:
                for layer_structure in layer_configs:
                    full_layer_structure = (
                        [X_train.shape[1]] + layer_structure + [int(output_size)]
                    )

                    for combination in product(*values):
                        if sys.version_info >= (3, 10):
                            params = dict(zip(keys, combination, strict=False))
                        else:
                            params = dict(
                                zip(keys, combination)
                            )  # Python < 3.10 doesn't support 'strict'

                        for lr in lr_options:
                            # Create model with current hyperparameters
                            nn = NumbaBackendNeuralNetwork(
                                full_layer_structure,
                                dropout_rate=params["dropout_rate"],
                                reg_lambda=params["reg_lambda"],
                                compile_numba=False,
                            )

                            # Create optimizer
                            optimizer = self._create_optimizer(
                                optimizer_type, lr, JIT=True
                            )

                            # Train model (with early stopping for efficiency)
                            nn.train(
                                X_train,
                                y_train,
                                X_val,
                                y_val,
                                optimizer=optimizer,
                                epochs=epochs,
                                batch_size=batch_size,
                                early_stopping_threshold=5,
                                use_tqdm=False,
                                p=False,
                            )

                            # Evaluate on validation set
                            accuracy, _ = nn.evaluate(X_val, y_val)

                            # Update best if improved
                            if accuracy > best_accuracy:
                                best_accuracy = accuracy
                                best_params = {
                                    **params,
                                    "layers": full_layer_structure,
                                    "learning_rate": lr,
                                }
                                best_optimizer_type = optimizer_type

                                tqdm.write(
                                    f"New best: {best_accuracy:.4f} with {optimizer_type}, "
                                    f"lr={lr}, layers={full_layer_structure}, params={params}"
                                )

                            # Update progress
                            pbar.update(1)

        print(
            f"\nBest configuration: {best_optimizer_type} optimizer with lr={best_params['learning_rate']}"
        )
        print(f"Layers: {best_params['layers']}")
        print(
            f"Parameters: dropout={best_params['dropout_rate']}, reg_lambda={best_params['reg_lambda']}"
        )
        print(f"Validation accuracy: {best_accuracy:.4f}")

        # Add best optimizer type to best_params
        best_params["optimizer"] = best_optimizer_type

        return best_params, best_accuracy

    def _get_jit_loss_calculator(self):
        """Helper to get the corresponding @njit loss calculation function."""
        if isinstance(self.loss_function, JITMeanSquaredErrorLoss):
            return calculate_mse_loss
        elif isinstance(self.loss_function, JITMeanAbsoluteErrorLoss):
            return calculate_mae_loss
        elif isinstance(self.loss_function, JITHuberLoss):
            # The delta parameter is stored in self.loss_function.delta
            # However, we cannot easily pass this instance variable into the
            # @njit process_batches_regression_jit function which expects only
            # the @njit function reference (calculate_huber_loss).
            # The calculate_huber_loss function has a default delta=1.0.
            # We will return the function and issue a warning that the default delta is used.
            if not self.warn_huber_delta and self.loss_function.delta != 1.0:
                self.warn_huber_delta = True
                warnings.warn(
                    f"JITHuberLoss selected for Numba backend. "
                    f"The JIT batch processing loop will use the default delta={getattr(calculate_huber_loss, 'delta', 1.0)} "
                    f"for calculate_huber_loss. The specified delta ({self.loss_function.delta}) "
                    f"will be used for non-JIT evaluations (like final loss/metric calculation).",
                    UserWarning,
                    stacklevel=2,
                )
            return calculate_huber_loss
        elif (
            self.is_regressor
        ):  # Default case if loss is None or unexpected for regressor
            warnings.warn(
                "Defaulting to MSE loss calculator for JIT regression.", stacklevel=2
            )
            return calculate_mse_loss
        else:
            # Should not be called for classification, but handle defensively
            return None

    def compile_numba_functions(self, progress_bar=True):
        """Compiles all Numba JIT functions to improve performance.

        Args:
            progress_bar (bool): Whether to display a progress bar.
        """
        if progress_bar and not TQDM_AVAILABLE:
            warnings.warn("tqdm not installed. Progress bar disabled.", stacklevel=2)
            progress_bar = False

        # Total steps: 2 + 1 + 2 + 6 + 9 + 2 + 9 + 10 = 41
        # NN Functions: 2 calls
        # Batch Processing: 1 call
        # Evaluation Functions: 2 calls
        # Numba Utils - Loss Helpers: 6 calls
        # Numba Utils - Activations: 9 calls
        # Numba Utils - Other: 2 calls
        # Optimizers: 9 calls
        # Loss Modules: 10 calls
        total_steps = 41
        pbar = tqdm(
            total=total_steps,
            desc="Compiling Numba functions",
            disable=not progress_bar,
        )

        def update_pbar(p):
            if p:
                p.update(1)

        # Neural network functions
        # --------------------------------------------------------------------
        if pbar:
            pbar.set_description("Compiling NN Functions")
        apply_dropout_jit(np.random.randn(10, 10).astype(np.float64), self.dropout_rate)
        update_pbar(pbar)
        _weights_list = [
            w.astype(np.float64) for w in self.weights
        ]  # Ensure float64 list
        compute_l2_reg(_weights_list)
        update_pbar(pbar)

        # Prepare dummy data (Ensure both binary and multi-class dummy targets are defined)
        dummy_X = np.random.randn(10, self.layer_sizes[0]).astype(np.float64)
        # Creates dummy binary targets, shape (10, 1)
        dummy_y_binary = np.random.randint(0, 2, (10, 1)).astype(np.float64)
        # Create dummy multi-class index targets, shape (10,)
        dummy_y_multi_idx = np.random.randint(0, self.layer_sizes[-1], 10).astype(
            np.int32
        )
        # Create dummy regression targets if needed
        dummy_y_reg = np.random.randn(10, 1).astype(np.float64)

        dummy_dWs = [np.zeros_like(w, dtype=np.float64) for w in self.weights]
        dummy_dbs = [np.zeros_like(b, dtype=np.float64) for b in self.biases]
        dropout_idxs = [
            i for i, layer in enumerate(self.layers) if isinstance(layer, JITDenseLayer)
        ] or [-1]

        # Compile batch processing functions
        # --------------------------------------------------------------------
        if pbar:
            pbar.set_description("Compiling Batch Processing")
        if self.is_regressor:
            jit_loss_calculator = self._get_jit_loss_calculator()
            if jit_loss_calculator:  # Only compile if we have a valid calculator
                process_batches_regression_jit(
                    dummy_X,
                    dummy_y_reg,  # Use regression dummy data
                    4,  # batch_size
                    self.layers,
                    self.dropout_rate,
                    dropout_idxs,
                    self.reg_lambda,
                    dummy_dWs,
                    dummy_dbs,
                    jit_loss_calculator,  # Pass the loss function instance
                )
            else:
                warnings.warn(
                    "Skipping compilation of process_batches_regression_jit due to incompatible loss function.",
                    stacklevel=2,
                )
        elif self.is_binary:
            process_batches_binary(
                dummy_X,
                dummy_y_binary.astype(np.int32),  # Use binary dummy data
                4,  # batch_size
                self.layers,
                self.dropout_rate,
                dropout_idxs,
                self.reg_lambda,
                dummy_dWs,
                dummy_dbs,
            )
        else:  # Multi-class
            process_batches_multi(
                dummy_X,
                dummy_y_multi_idx,  # Use multi-class index dummy data
                4,  # batch_size
                self.layers,
                self.dropout_rate,
                dropout_idxs,
                self.reg_lambda,
                dummy_dWs,
                dummy_dbs,
            )
        update_pbar(pbar)

        # Compile evaluation functions
        # --------------------------------------------------------------------
        if pbar:
            pbar.set_description("Compiling Evaluation")
        dummy_y_hat_binary = np.random.rand(10, 1).astype(np.float64)
        dummy_y_hat_multi = np.random.rand(10, self.layer_sizes[-1]).astype(np.float64)
        # REMOVED: dummy_y_hat_reg = np.random.rand(10, 1).astype(np.float64) # No longer needed here

        evaluate_jit(dummy_y_hat_binary, dummy_y_binary.astype(np.int32), True)
        update_pbar(pbar)
        evaluate_jit(dummy_y_hat_multi, dummy_y_multi_idx, False)
        update_pbar(pbar)
        # REMOVED: evaluate_regression_jit compilation call

        # Numba Utils functions
        # --------------------------------------------------------------------
        if pbar:
            pbar.set_description("Compiling Numba Utils")
        # Loss calculation helpers
        calculate_loss_from_outputs_binary(
            dummy_y_hat_binary, dummy_y_binary, self.reg_lambda, _weights_list
        )
        update_pbar(pbar)
        dummy_y_ohe = np.eye(self.layer_sizes[-1])[dummy_y_multi_idx].astype(np.float64)
        calculate_loss_from_outputs_multi(
            dummy_y_hat_multi, dummy_y_ohe, self.reg_lambda, _weights_list
        )
        update_pbar(pbar)
        # Compile regression loss helpers
        dummy_y_hat_reg = np.random.rand(10, 1).astype(
            np.float64
        )  # Define it here for loss helpers
        calculate_mse_loss(dummy_y_hat_reg, dummy_y_reg)
        update_pbar(pbar)
        calculate_mae_loss(dummy_y_hat_reg, dummy_y_reg)
        update_pbar(pbar)
        calculate_huber_loss(dummy_y_hat_reg, dummy_y_reg)
        update_pbar(pbar)
        evaluate_batch(
            dummy_y_hat_multi, dummy_y_multi_idx, False
        )  # Covers both binary/multi logic inside
        update_pbar(pbar)
        # Activation functions (remain the same)
        relu(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        relu_derivative(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        leaky_relu(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        leaky_relu_derivative(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        tanh(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        tanh_derivative(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        sigmoid(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        sigmoid_derivative(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        softmax(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        # Other utility functions (remain the same)
        sum_reduce(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)
        sum_axis0(np.random.randn(10, 10).astype(np.float64))
        update_pbar(pbar)

        # Optimizers
        # --------------------------------------------------------------------
        if pbar:
            pbar.set_description("Compiling Optimizers")
        # Ensure dummy gradients match weight/bias dimensions for trainable layers
        dummy_dWs = []
        dummy_dbs = []
        for layer in self.trainable_layers:
            dummy_dWs.append(np.zeros_like(layer.weights, dtype=np.float64))
            dummy_dbs.append(np.zeros_like(layer.biases, dtype=np.float64))

        # Adam
        _adam = JITAdamOptimizer()
        update_pbar(pbar)
        _adam.initialize(self.trainable_layers)
        update_pbar(pbar)  # Pass trainable_layers
        _adam.update_layers(self.trainable_layers, dummy_dWs, dummy_dbs)
        update_pbar(pbar)  # Pass trainable_layers
        # SGD
        _sgd = JITSGDOptimizer()
        update_pbar(pbar)
        _sgd.initialize(self.trainable_layers)
        update_pbar(pbar)  # Pass trainable_layers
        _sgd.update_layers(self.trainable_layers, dummy_dWs, dummy_dbs)
        update_pbar(pbar)  # Pass trainable_layers
        # Adadelta
        _adadelta = JITAdadeltaOptimizer()
        update_pbar(pbar)
        _adadelta.initialize(self.trainable_layers)
        update_pbar(pbar)  # Pass trainable_layers
        _adadelta.update_layers(self.trainable_layers, dummy_dWs, dummy_dbs)
        update_pbar(pbar)  # Pass trainable_layers

        # Loss Modules
        # --------------------------------------------------------------------
        if pbar:
            pbar.set_description("Compiling Loss Modules")
        _cross_entropy = JITCrossEntropyLoss()
        update_pbar(pbar)
        _cross_entropy.calculate_loss(dummy_y_hat_multi, dummy_y_ohe)
        update_pbar(pbar)
        _bce = JITBCEWithLogitsLoss()
        update_pbar(pbar)
        _bce.calculate_loss(dummy_y_hat_binary, dummy_y_binary)
        update_pbar(pbar)
        # Compile JIT Regression Loss Classes
        _mse = JITMeanSquaredErrorLoss()
        update_pbar(pbar)
        _mse.calculate_loss(dummy_y_hat_reg, dummy_y_reg)
        update_pbar(pbar)
        _mae = JITMeanAbsoluteErrorLoss()
        update_pbar(pbar)
        _mae.calculate_loss(dummy_y_hat_reg, dummy_y_reg)
        update_pbar(pbar)
        _huber = JITHuberLoss()
        update_pbar(pbar)
        _huber.calculate_loss(dummy_y_hat_reg, dummy_y_reg)
        update_pbar(pbar)

        if pbar:
            pbar.close()
        self.compiled = True
