import contextlib
import sys
import warnings

import numpy as np
from joblib import Parallel, delayed

from .activations import Activation
from .layers import *
from .loss import (
    BCEWithLogitsLoss,
    CrossEntropyLoss,
    HuberLoss,
    MeanAbsoluteErrorLoss,
    MeanSquaredErrorLoss,
)
from .neuralNetworkBase import NeuralNetworkBase
from .optimizers import AdadeltaOptimizer, AdamOptimizer, SGDOptimizer
from .schedulers import lr_scheduler_plateau

try:
    from tqdm.auto import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class BaseBackendNeuralNetwork(NeuralNetworkBase):
    """A class representing a backend implementation of a neural network with support for forward propagation, backward propagation, training, evaluation, and hyperparameter tuning.

    This class extends the `NeuralNetworkBase` class and provides additional functionality
    for managing layers, applying dropout, calculating loss, and optimizing weights and biases.

    Attributes:
        layers (list): List of layer objects in the neural network.
        layer_outputs (list): Outputs of each layer during forward propagation.
        weights (list): Weights of each layer.
        biases (list): Biases of each layer.
        train_loss (list): Training loss values over epochs.
        train_accuracy (list): Training accuracy values over epochs.
        val_loss (list): Validation loss values over epochs.
        val_accuracy (list): Validation accuracy values over epochs.
        train_precision (list): Training precision values over epochs.
        train_recall (list): Training recall values over epochs.
        train_f1 (list): Training F1-score values over epochs.
        val_precision (list): Validation precision values over epochs.
        val_recall (list): Validation recall values over epochs.
        val_f1 (list): Validation F1-score values over epochs.
        learning_rates (list): Learning rates over epochs.

    Methods:
        __init__(layers, dropout_rate=0.2, reg_lambda=0.01, activations=None, loss_function=None, regressor=False):
            Initializes the neural network with the specified layers, dropout rate,
            regularization parameter, activation functions, and optional loss function.
        initialize_new_layers():
            Initializes the layers of the neural network with random weights and biases.
        forward(X, training=True):
            Performs forward propagation through the neural network.
        backward(y):
            Performs backward propagation to calculate gradients for weight and bias updates.
        fit(X_train, y_train, X_val=None, y_val=None, optimizer=None, epochs=100, batch_size=32, ...):
            Fits the neural network to the training data.
        train(X_train, y_train, X_val=None, y_val=None, optimizer=None, epochs=100, batch_size=32, ...):
            Trains the neural network model with optional validation and early stopping.
        evaluate(X, y):
            Evaluates the model on the given data and returns accuracy and predictions.
        predict(X):
            Predicts the output for the given input data.
        calculate_loss(X, y):
            Calculates the loss with L2 regularization for the given input and target labels.
        _create_optimizer(optimizer_type, learning_rate, JIT=False):
            Helper method to create optimizer instances based on the specified type.
        tune_hyperparameters(X_train, y_train, X_val, y_val, param_grid, ...):
            Performs hyperparameter tuning using grid search.
        train_with_animation_capture(X_train, y_train, X_val=None, y_val=None, ...):
            Trains the neural network while capturing training metrics in real-time animation.
    """

    # TODO: Check that last layer activation is 'none' or 'linear' if regressor, else warn
    def __init__(
        self,
        layers,
        dropout_rate=0.2,
        reg_lambda=0.01,
        activations=None,
        loss_function=None,
        regressor=False,
    ):
        """Initializes the Numba backend neural network.

        Args:
            layers: (list) - List of layer sizes or Layer objects.
            dropout_rate: (float) - Dropout rate for regularization.
            reg_lambda: (float) - L2 regularization parameter.
            activations: (list) - List of activation functions for each layer.
            loss_function: (callable) optional - Custom loss function to use (default is None, which uses the default calculate_loss implementation).
            regressor: (bool) - Whether the model is a regressor (default is False).
        """
        super().__init__(
            layers, dropout_rate, reg_lambda, activations, loss_function, regressor
        )

        # if layers are empty list, initialize them
        if len(self.layers) == 0:
            self.initialize_new_layers()

    def initialize_new_layers(self):
        """Initializes the layers of the neural network.

        Each layer is created with the specified number of neurons and activation function.
        """
        for i in range(len(self.layer_sizes) - 1):
            self.layers.append(
                DenseLayer(
                    self.layer_sizes[i], self.layer_sizes[i + 1], self.activations[i]
                )
            )
            weight = (
                np.random.randn(self.layer_sizes[i], self.layer_sizes[i + 1]) * 0.01
            )
            bias = np.zeros((1, self.layer_sizes[i + 1]))
            self.weights.append(weight)
            self.biases.append(bias)

    def forward(self, X, training=True):
        """Performs forward propagation through the neural network.

        Args:
            X: (ndarray): - Input data of shape (batch_size, input_size).
            training: (bool) - Whether the network is in training mode (applies dropout).

        Returns:
            ndarray: Output predictions of shape (batch_size, output_size).
        """
        # Store the outputs of each layer for backpropagation
        self.layer_outputs = [X]
        A = X

        # Pass through each layer
        for _i, layer in enumerate(self.layers):
            A = layer.forward(A)
            # Apply dropout only to DenseLayer outputs during training
            if training and self.dropout_rate > 0 and isinstance(layer, DenseLayer):
                A = self.apply_dropout(A)
            self.layer_outputs.append(A)

        # For regression, the last layer's output (A) is the final output
        # For classification, apply final activation if needed (handled in Layer.forward)
        # The `self.is_binary` check might be redundant if last layer activation is set correctly
        # kept for potential clarity/safety.
        if not self.is_regressor:
            if self.is_binary:
                return Activation.sigmoid(A)
            else:
                return Activation.softmax(A) if A.ndim > 1 else A

        # Return the raw output A for regression
        return A

    def backward(self, y):
        """Performs backward propagation to calculate the gradients.

        Args:
            y: (ndarray) - Target labels of shape (m, output_size).
        """
        outputs = self.layer_outputs[-1]
        m = y.shape[0]  # Number of samples in the batch

        # --- MODIFIED Initial Gradient Calculation ---
        if self.is_regressor:
            # Ensure y is float and has the correct shape (n_samples, n_outputs)
            y = np.asarray(y, dtype=np.float64)
            if y.ndim == 1:
                y = y.reshape(-1, 1)
            if outputs.shape != y.shape:
                raise ValueError(
                    f"Shape mismatch in backward pass: outputs {outputs.shape}, y {y.shape}"
                )

            # Calculate gradient based on the specified regression loss function
            # Derivative of MSE Loss w.r.t output A (assuming linear output): dL/dA = 2/m * (A - y)
            # Often, the 2/m factor is dropped or handled by the optimizer's learning rate.

            # Note: This assumes the LAST layer activation is 'none' or 'linear'.
            # If a non-linear activation was used, dA would need to be dA = dL/dA * activation_derivative(Z)
            # but the calculation below starts from dZ = dA * activation_derivative(Z) which simplifies if derivative is 1.
            if isinstance(self.loss_function, MeanSquaredErrorLoss):
                dA = (
                    outputs - y
                ) / m  # Gradient of MSE loss w.r.t prediction 'outputs'
            elif isinstance(self.loss_function, MeanAbsoluteErrorLoss):
                dA = (
                    np.sign(outputs - y) / m
                )  # Gradient of MAE loss w.r.t prediction 'outputs'
            elif isinstance(self.loss_function, HuberLoss):
                # Huber loss derivative: dL/dA = (A - y) / m for |A - y| < delta, delta * sign(A - y) / m otherwise
                delta = 1.0
                dA = np.where(
                    np.abs(outputs - y) < delta,
                    (outputs - y) / m,
                    delta * np.sign(outputs - y) / m,
                )
            else:
                # Default or fallback: Assume MSE derivative for dA
                print(
                    "Warning: Unknown regression loss function, defaulting to MSE derivative for backward pass."
                )
                dA = (outputs - y) / m

            # The first step of backprop for the last layer needs dZ = dA * activation_derivative(Z_last)
            # If activation is linear ('none'), derivative is 1, so dZ = dA.
            # We pass dA, and the layer's backward method computes dZ internally.

        elif self.is_binary:
            # Binary classification (ensure y shape is correct)
            y = np.asarray(y).reshape(-1, 1)
            dA = (
                (outputs - y) / m
            )  # Gradient dL/dA for sigmoid output, or dL/dZ for logit output used with BCEWithLogitsLoss

        else:
            # Multi-class classification
            if y.ndim == 1:  # Convert to one-hot if needed
                y = np.eye(self.layer_sizes[-1])[y]
            # Gradient for CrossEntropyLoss with Softmax (dL/dZ): A - y
            dA = (
                (outputs - y) / m
            )  # Gradient dL/dA for softmax output, or dL/dZ for logit output used with CrossEntropyLoss

        # Backpropagation through the network in reverse order
        for i in reversed(range(len(self.layers))):
            dA = self.layers[i].backward(
                dA, self.reg_lambda
            )  # Pass dA, layer computes its dZ

    def fit(
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
        p=False,
        use_tqdm=False,
        n_jobs=1,
        track_metrics=False,
        track_adv_metrics=False,
        save_animation=False,
        save_path="training_animation.mp4",
        fps=1,
        dpi=100,
        frame_every=1,
    ):
        """Fits the neural network to the training data."""
        # Call the train method
        return self.train(
            X_train,
            y_train,
            X_val,
            y_val,
            optimizer,
            epochs,
            batch_size,
            early_stopping_threshold,
            lr_scheduler,
            p,
            use_tqdm,
            n_jobs,
            track_metrics,
            track_adv_metrics,
            save_animation,
            save_path,
            fps,
            dpi,
            frame_every,
        )

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
            optimizer: (Optimizer) - Optimizer for updating parameters (default: Adam, lr=0.0001).
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
            optimizer = AdamOptimizer(learning_rate=0.0001)

        # Initialize optimizer
        optimizer.initialize(self.layers)

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
            self.train_metric = []  # e.g., stores MSE for regression, Accuracy for classification
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

        def process_batch(start_idx):
            X_batch = X_shuffled[start_idx : start_idx + batch_size]
            y_batch = y_shuffled[start_idx : start_idx + batch_size]

            # Forward and backward passes
            self.forward(X_batch, training=True)
            self.backward(y_batch)

            # Update weights and biases
            trainable_idx = 0  # Separate index for trainable layers
            for layer in self.layers:
                if (
                    hasattr(layer, "weight_gradients")
                    and layer.weight_gradients is not None
                ):
                    dW = layer.weight_gradients
                    db = layer.bias_gradients
                    optimizer.update(layer, dW, db, trainable_idx)
                    trainable_idx += 1

        # Training loop with progress bar
        progress_bar = tqdm(range(epochs)) if use_tqdm else range(epochs)
        for epoch in progress_bar:
            # Reset gradients
            for layer in self.layers:
                if hasattr(layer, "zero_grad"):
                    layer.zero_grad()

            # Shuffle training data
            indices = np.arange(X_train.shape[0])
            np.random.shuffle(indices)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            # Mini-batch training with parallel processing
            Parallel(n_jobs=n_jobs)(
                delayed(process_batch)(i)
                for i in range(0, X_train.shape[0], batch_size)
            )

            # Calculate metrics
            train_loss = self.calculate_loss(X_train, y_train)
            # Calculate primary metric (MSE for regression, Accuracy for classification)
            train_metric_value, _train_preds = self.evaluate(X_train, y_train)

            # Validation metrics
            val_metrics_str = ""
            if X_val is not None:
                val_loss = self.calculate_loss(X_val, y_val)
                val_metric_value, _val_preds = self.evaluate(X_val, y_val)
                val_metric_display = (
                    f"Val Loss: {val_loss:.4f}, Val Metric: {val_metric_value:.4f}"
                )
                val_metrics_str = f", {val_metric_display}"

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
            if track_adv_metrics:
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

            metric_label = (
                "MSE" if self.is_regressor else "Acc"
            )  # Choose appropriate label
            train_metrics_display = f"Loss: {train_loss:.4f}, Train {metric_label}: {train_metric_value:.4f}"

            # Update progress bar or print metrics
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
                    if use_tqdm and p and msg:
                        tqdm.write(msg)
                    elif p and msg:
                        print(msg)
                else:
                    msg = lr_scheduler.step(epoch)
                    lr = optimizer.learning_rate
                    if use_tqdm and p and msg:
                        tqdm.write(msg)
                    elif p and msg:
                        print(msg)

            # Update animator with metrics
            if save_animation:
                train_metrics = {
                    "loss": train_loss,
                    "accuracy": train_metric_value,
                    "precision": train_precision,
                    "recall": train_recall,
                    "f1": train_f1,
                }
                if lr:
                    train_metrics["learning_rate"] = lr
                animator.update_metrics(train_metrics, validation=False)
                val_metrics = {
                    "loss": val_loss,
                    "accuracy": val_metric_value,
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
                # Capture final frame if not already captured and if animation is enabled
                if save_animation and epoch % frame_every != 0:
                    with contextlib.suppress(Exception):
                        animator.add_training_frame()

                # Stop training
                if p and use_tqdm:
                    tqdm.write(f"Early stopping at epoch {epoch + 1}")
                elif p:
                    print(f"Early stopping at epoch {epoch + 1}")
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
        """Evaluates the model's performance on the given data.

        Args:
            X: (np.ndarray) - Input feature data for evaluation.
            y: (np.ndarray) - True target labels corresponding to the input data.

        Returns:
            metric: (float) - The evaluation metric (accuracy for classification, MSE for regression).
            predicted: (np.ndarray) - The predicted labels or values for the input data.
        """
        y_hat = self.forward(X, training=False)
        y = np.asarray(y)  # Ensure y is numpy array

        if self.is_regressor:
            # Regression: Calculate primary metric (e.g., MSE) and return raw predictions
            metric_fn = (
                self.loss_function if self.loss_function else MeanSquaredErrorLoss()
            )
            # Ensure y has the same shape as y_hat for loss calculation
            if y.ndim == 1 and y_hat.ndim == 2 and y_hat.shape[1] == 1:
                y = y.reshape(-1, 1)
            elif y_hat.ndim == 1 and y.ndim == 2 and y.shape[1] == 1:
                y_hat = y_hat.reshape(-1, 1)
            elif y.shape != y_hat.shape:
                raise ValueError(
                    f"evaluate shape mismatch: y_true {y.shape} vs y_pred {y_hat.shape}"
                )

            metric = metric_fn(
                y, y_hat
            )  # Using the loss as the primary evaluation metric
            predicted = y_hat  # Return raw predictions for regression

        elif self.is_binary:
            # Binary classification: Calculate accuracy and predicted classes
            predicted_classes = (y_hat > 0.5).astype(int)
            y_true_flat = y.flatten()
            predicted_flat = predicted_classes.flatten()
            metric = float(np.mean(predicted_flat == y_true_flat))  # Accuracy
            predicted = predicted_classes  # Return predicted classes (0 or 1)
        else:
            # Multi-class classification: Calculate accuracy and predicted classes
            predicted_classes = np.argmax(y_hat, axis=1)
            y_true_indices = y  # Assuming y contains class indices
            metric = float(np.mean(predicted_classes == y_true_indices))  # Accuracy
            predicted = predicted_classes  # Return predicted class indices

        return metric, predicted

    def predict(self, X):
        """Generates predictions for the given input data.

        Args:
            X: (np.ndarray) - Input feature data for which predictions are to be made.

        Returns:
            outputs: (np.ndarray) - Predicted outputs. If the model is binary, returns the raw outputs.
                        Otherwise, returns the class indices with the highest probability.
        """
        outputs = self.forward(X, training=False)
        if self.is_regressor:
            return (
                outputs.flatten()
            )  # Ensure predictions are returned as a 1D array for regression

        elif self.is_binary:
            return (outputs > 0.5).astype(int)  # Return class labels 0 or 1
        else:
            return np.argmax(
                outputs, axis=1
            )  # Return class index with highest probability

    def calculate_loss(self, X, y):
        """Calculates the loss with L2 regularization.

        Args:
            X: (np.ndarray) - Input feature data.
            y: (np.ndarray) - Target labels.

        Returns:
            loss: (float) - The calculated loss value with L2 regularization.
        """
        # Get the output of the network (forward pass w/o dropout)
        outputs = self.forward(X, training=False)

        if self.is_regressor:
            # Use the assigned or default regression loss function
            if not hasattr(self, "loss_function") or self.loss_function is None:
                # Fallback if not set during init (should be set)
                loss_fn = MeanSquaredErrorLoss()
                warnings.warn(
                    "Loss function not explicitly set for regressor, defaulting to MSE.",
                    stacklevel=2,
                )
            else:
                loss_fn = self.loss_function
            loss = loss_fn(y, outputs)  # Calculate regression loss

        elif self.is_binary:
            # Binary classification loss
            if not hasattr(self, "loss_function") or self.loss_function is None:
                loss_fn = BCEWithLogitsLoss()  # Default
                warnings.warn(
                    "Loss function not explicitly set for binary classification, defaulting to BCEWithLogitsLoss.",
                    stacklevel=2,
                )
            else:
                loss_fn = self.loss_function
            loss = loss_fn(outputs, np.asarray(y).reshape(-1, 1))

        else:
            # Multi-class classification loss
            if not hasattr(self, "loss_function") or self.loss_function is None:
                loss_fn = CrossEntropyLoss()  # Default
                warnings.warn(
                    "Loss function not explicitly set for multi-class classification, defaulting to CrossEntropyLoss.",
                    stacklevel=2,
                )
            else:
                loss_fn = self.loss_function
            loss = loss_fn(
                outputs, y
            )  # Assumes y is indices or loss_fn handles one-hot

        # Add L2 regularization term to the loss
        l2_reg = self.reg_lambda * self.compute_l2_reg(
            [layer.weights for layer in self.layers if hasattr(layer, "weights")]
        )
        loss += l2_reg
        return float(loss)

    def _create_optimizer(self, optimizer_type, learning_rate, JIT=False):
        """Helper method to create optimizer instances."""
        if optimizer_type == "Adam":
            return AdamOptimizer(learning_rate)
        elif optimizer_type == "SGD":
            return SGDOptimizer(learning_rate)
        elif optimizer_type == "Adadelta":
            return AdadeltaOptimizer(learning_rate)
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
            lr_range: (tuple) - Tuple of (min_lr, max_lr, num_steps) for learning rates.
            epochs: (int) - Maximum epochs for each trial.
            batch_size: (int) - Batch size for training.

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
                            nn = BaseBackendNeuralNetwork(
                                full_layer_structure,
                                dropout_rate=params["dropout_rate"],
                                reg_lambda=params["reg_lambda"],
                            )

                            # Create optimizer
                            optimizer = self._create_optimizer(optimizer_type, lr)

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

    def train_with_animation_capture(
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
        save_path="training_animation.mp4",
        fps=1,
        dpi=100,
        frame_every=1,
    ):
        """Trains the neural network model while capturing training metrics in real-time animation.

        Args:
            X_train: (np.ndarray) - Training feature data.
            y_train: (np.ndarray) - Training target data.
            X_val: (np.ndarray), optional - Validation feature data (default is None).
            y_val: (np.ndarray), optional - Validation target data (default is None).
            optimizer: (Optimizer), optional - Optimizer for updating parameters (default is None).
            epochs: (int), optional - Number of training epochs (default is 100).
            batch_size: (int), optional - Batch size for mini-batch gradient descent (default is 32).
            early_stopping_threshold: (int), optional - Patience for early stopping (default is 10).
            lr_scheduler: (Scheduler), optional - Learning rate scheduler (default is None).
            save_path: (str), optional - Path to save the animation file (default is 'training_animation.mp4').
            fps: (int), optional - Frames per second for the saved animation (default is 1).
            dpi: (int), optional - DPI for the saved animation (default is 100).
            frame_every: (int), optional - Capture frame every N epochs (default is 1).

        Returns:
            None
        """
        import os

        from .animation import TrainingAnimator

        # Initialize the animator
        animator = TrainingAnimator(figure_size=(18, 10), dpi=dpi)

        # Define metrics to track
        metrics = ["loss", "accuracy", "precision", "recall", "f1"]
        if lr_scheduler:
            metrics.append("learning_rate")

        # Initialize animator with metrics
        animator.initialize(metrics, has_validation=(X_val is not None))

        # Setup the training video capture with error handling
        try:
            # Ensure directory exists
            directory = os.path.dirname(save_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            animator.setup_training_video(save_path, fps=fps, dpi=dpi)
            animation_enabled = True
        except Exception as e:
            print(f"Failed to setup animation: {str(e)}")
            print("Training will continue without animation capture.")
            animation_enabled = False

        # Initialize metrics storage
        self.train_loss = []
        self.train_accuracy = []
        self.learning_rates = []
        self.train_precision = []
        self.train_recall = []
        self.train_f1 = []

        if X_val is not None:
            self.val_loss = []
            self.val_accuracy = []
            self.val_precision = []
            self.val_recall = []
            self.val_f1 = []

        # Default optimizer if not provided
        if optimizer is None:
            optimizer = AdamOptimizer(learning_rate=0.0001)

        # Initialize optimizer
        optimizer.initialize(self.layers)

        # Track best model for early stopping
        best_loss = float("inf")
        patience_counter = 0
        best_weights = [
            layer.weights.copy() for layer in self.layers if hasattr(layer, "weights")
        ]
        best_biases = [
            layer.biases.copy() for layer in self.layers if hasattr(layer, "biases")
        ]

        def process_batch(start_idx, X_shuffled, y_shuffled):
            X_batch = X_shuffled[start_idx : start_idx + batch_size]
            y_batch = y_shuffled[start_idx : start_idx + batch_size]

            # Forward and backward passes
            self.forward(X_batch, training=True)
            self.backward(y_batch)

            # Update weights and biases
            trainable_idx = 0  # Separate index for trainable layers
            for layer in self.layers:
                if (
                    hasattr(layer, "weight_gradients")
                    and layer.weight_gradients is not None
                ):
                    dW = layer.weight_gradients
                    db = layer.bias_gradients
                    optimizer.update(layer, dW, db, trainable_idx)
                    trainable_idx += 1

        # Training loop
        for epoch in range(epochs):
            # Reset gradients
            for layer in self.layers:
                if hasattr(layer, "zero_grad"):
                    layer.zero_grad()

            # Shuffle training data
            indices = np.arange(X_train.shape[0])
            np.random.shuffle(indices)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            # Process all batches
            for i in range(0, X_train.shape[0], batch_size):
                process_batch(i, X_shuffled, y_shuffled)

            # Calculate metrics
            train_loss = self.calculate_loss(X_train, y_train)
            train_accuracy, _ = self.evaluate(X_train, y_train)
            train_precision, train_recall, train_f1 = (
                self.calculate_precision_recall_f1(X_train, y_train)
            )

            # Store metrics
            self.train_loss.append(train_loss)
            self.train_accuracy.append(train_accuracy)
            self.train_precision.append(train_precision)
            self.train_recall.append(train_recall)
            self.train_f1.append(train_f1)

            # Prepare metrics for animator
            train_metrics = {
                "loss": train_loss,
                "accuracy": train_accuracy,
                "precision": train_precision,
                "recall": train_recall,
                "f1": train_f1,
            }

            # Validation metrics
            val_metrics_str = ""
            if X_val is not None:
                val_loss = self.calculate_loss(X_val, y_val)
                val_accuracy, _ = self.evaluate(X_val, y_val)
                val_precision, val_recall, val_f1 = self.calculate_precision_recall_f1(
                    X_val, y_val
                )

                # Store validation metrics
                self.val_loss.append(val_loss)
                self.val_accuracy.append(val_accuracy)
                self.val_precision.append(val_precision)
                self.val_recall.append(val_recall)
                self.val_f1.append(val_f1)

                val_metrics_str = (
                    f", Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}"
                )

                # Update animator with validation metrics
                val_metrics = {
                    "loss": val_loss,
                    "accuracy": val_accuracy,
                    "precision": val_precision,
                    "recall": val_recall,
                    "f1": val_f1,
                }
                animator.update_metrics(val_metrics, validation=True)

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

            # Update learning rate if scheduler is provided
            if lr_scheduler:
                if isinstance(lr_scheduler, lr_scheduler_plateau):
                    msg = lr_scheduler.step(
                        epoch, train_loss if X_val is None else val_loss
                    )
                    if msg:
                        print(msg)
                else:
                    msg = lr_scheduler.step(epoch)
                    if msg:
                        print(msg)

                self.learning_rates.append(optimizer.learning_rate)
                train_metrics["learning_rate"] = optimizer.learning_rate

            # Update animator with training metrics
            animator.update_metrics(train_metrics, validation=False)

            # Print progress
            print(
                f"Epoch {epoch + 1}/{epochs} - Loss: {train_loss:.4f}, Acc: {train_accuracy:.4f}{val_metrics_str}"
            )

            # Add frame to the animation if needed and if animation is enabled
            if animation_enabled and (epoch % frame_every == 0 or epoch == epochs - 1):
                try:
                    animator.add_training_frame()
                except Exception as e:
                    print(f"Failed to add animation frame: {str(e)}")
                    animation_enabled = False

            # Early stopping
            if patience_counter >= early_stopping_threshold:
                print(f"Early stopping at epoch {epoch + 1}")
                # Capture final frame if not already captured and if animation is enabled
                if animation_enabled and epoch % frame_every != 0:
                    with contextlib.suppress(Exception):
                        animator.add_training_frame()
                break
        # Restore best weights
        trainable_layers = [layer for layer in self.layers if hasattr(layer, "weights")]
        for i, layer in enumerate(trainable_layers):
            layer.weights = best_weights[i]
            layer.biases = best_biases[i]

        # Finish and save the animation if enabled
        if animation_enabled:
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
        else:
            # Generate static plot as fallback
            try:
                static_plot_path = save_path.rsplit(".", 1)[0] + ".png"
                self.plot_metrics(save_dir=static_plot_path)
                print(f"Static metrics plot saved to {static_plot_path}")
            except Exception as e:
                print(f"Failed to save static plot: {str(e)}")
