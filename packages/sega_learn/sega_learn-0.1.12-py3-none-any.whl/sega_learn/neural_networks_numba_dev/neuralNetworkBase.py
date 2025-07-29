import numpy as np

from .schedulers import *

try:
    from .layers_jit_unified import *
except:
    JITLayer = None


class NeuralNetworkBase:
    def __init__(self, layers, dropout_rate=0.0, reg_lambda=0.0, activations=None):
        _layers = []
        _layers_jit = [JITLayer]
        available_layers = tuple(_layers + _layers_jit)

        # iF all layers are integers, initialize the layers as DenseLayers
        if all(isinstance(layer, int) for layer in layers):
            self.layer_sizes = layers
            self.dropout_rate = dropout_rate
            self.reg_lambda = reg_lambda
            self.activations = (
                activations
                if activations
                else ["relu"] * (len(layers) - 2) + ["softmax"]
            )
            self.layers = []
            self.weights = []
            self.biases = []
            self.layer_outputs = None
            self.is_binary = layers[-1] == 1

        # Else if all layers are Layer objects, use them directly
        elif all(isinstance(layer, available_layers) for layer in layers):
            self.layers = layers
            self.layer_sizes = [layer.input_size for layer in layers] + [
                layers[-1].output_size
            ]
            self.dropout_rate = dropout_rate
            self.reg_lambda = reg_lambda
            self.is_binary = layers[-1].output_size == 1
        else:
            raise ValueError(
                "layers must be a list of integers or a list of Layer objects."
            )

    def initialize_layers(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def forward(self, X, training=True):
        raise NotImplementedError("This method should be implemented by subclasses")

    def backward(self, y):
        raise NotImplementedError("This method should be implemented by subclasses")

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
    ):
        raise NotImplementedError("This method should be implemented by subclasses")

    def evaluate(self, X, y):
        raise NotImplementedError("This method should be implemented by subclasses")

    def predict(self, X):
        raise NotImplementedError("This method should be implemented by subclasses")

    def calculate_loss(self, X, y):
        raise NotImplementedError("This method should be implemented by subclasses")

    def apply_dropout(self, X):
        """
        Applies dropout to the activation X.
        Args:
            X (ndarray): Activation values.
        Returns:
            ndarray: Activation values after applying dropout.
        """
        mask = np.random.rand(*X.shape) < (1 - self.dropout_rate)
        return np.multiply(X, mask) / (1 - self.dropout_rate)

    def compute_l2_reg(self, weights):
        """
        Computes the L2 regularization term.
        Args:
            weights (list): List of weight matrices.
        Returns:
            float: L2 regularization term.
        """
        total = 0.0
        for i in range(len(weights)):
            total += np.sum(weights[i] ** 2)
        return total

    def calculate_precision_recall_f1(self, X, y):
        """
        Calculates precision, recall, and F1 score.
        Args:
            - X (ndarray): Input data
            - y (ndarray): Target labels
        Returns:
            - precision (float): Precision score
            - recall (float): Recall score
            - f1 (float): F1 score
        """
        _, predicted = self.evaluate(X, y)
        true_positive = np.sum((predicted == 1) & (y == 1))
        false_positive = np.sum((predicted == 1) & (y == 0))
        false_negative = np.sum((predicted == 0) & (y == 1))

        precision = true_positive / (true_positive + false_positive + 1e-15)
        recall = true_positive / (true_positive + false_negative + 1e-15)
        f1 = 2 * (precision * recall) / (precision + recall + 1e-15)

        return precision, recall, f1

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

    def plot_metrics(self, save_dir=None):
        """
        Plots the training and validation metrics.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError(
                "Matplotlib is required for plotting. Please install matplotlib first."
            )

        if not hasattr(self, "train_loss"):
            raise ValueError(
                "No training history available. Please set track_metrics=True during training."
            )

        # Different number of plots for metrics vs metrics/adv_metrics

        # If ONLY metrics are tracked OR ONLY adv_metrics are tracked
        if (hasattr(self, "train_loss") + hasattr(self, "train_precision")) == 1:
            cnt = 1
            plt.figure(
                figsize=(18, 5)
            )  # Adjust the figure size to accommodate three plots

        elif (hasattr(self, "train_loss") + hasattr(self, "train_precision")) == 2:
            cnt = 2
            plt.figure(figsize=(18, 10))

        # Plot Loss
        if cnt == 1:
            plt.subplot(1, 3, 1)
        if cnt == 2:
            plt.subplot(2, 3, 1)
        plt.plot(self.train_loss, label="Train Loss")
        if hasattr(self, "val_loss"):
            plt.plot(self.val_loss, label="Val Loss")
        plt.title("Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()

        # Plot Accuracy
        if cnt == 1:
            plt.subplot(1, 3, 2)
        if cnt == 2:
            plt.subplot(2, 3, 2)
        plt.plot(self.train_accuracy, label="Train Accuracy")
        if hasattr(self, "val_accuracy"):
            plt.plot(self.val_accuracy, label="Val Accuracy")
        plt.title("Accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.legend()

        # Plot Learning Rate
        if cnt == 1:
            plt.subplot(1, 3, 3)
        if cnt == 2:
            plt.subplot(2, 3, 3)
        plt.plot(self.learning_rates, label="Learning Rate")
        plt.title("Learning Rate")
        plt.xlabel("Epoch")
        plt.ylabel("Learning Rate")
        plt.legend()

        if cnt == 2:
            # Plot Precision
            plt.subplot(2, 3, 4)
            plt.plot(self.train_precision, label="Train Precision")
            if hasattr(self, "val_precision"):
                plt.plot(self.val_precision, label="Val Precision")
            plt.title("Precision")
            plt.xlabel("Epoch")
            plt.ylabel("Precision")
            plt.legend()

            # Plot Recall
            plt.subplot(2, 3, 5)
            plt.plot(self.train_recall, label="Train Recall")
            if hasattr(self, "val_recall"):
                plt.plot(self.val_recall, label="Val Recall")
            plt.title("Recall")
            plt.xlabel("Epoch")
            plt.ylabel("Recall")
            plt.legend()

            # Plot F1 Score
            plt.subplot(2, 3, 6)
            plt.plot(self.train_f1, label="Train F1 Score")
            if hasattr(self, "val_f1"):
                plt.plot(self.val_f1, label="Val F1 Score")
            plt.title("F1 Score")
            plt.xlabel("Epoch")
            plt.ylabel("F1 Score")
            plt.legend()

        plt.tight_layout()

        if save_dir:
            plt.savefig(save_dir, dpi=600)
        else:
            plt.show()
