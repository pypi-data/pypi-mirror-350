import numpy as np

from .layers import *
from .schedulers import *

try:
    from .layers_jit import *
except ImportError:
    JITDenseLayer = None
try:
    from .layers_cupy import *
except ImportError:
    CuPyDenseLayer = None


class NeuralNetworkBase:
    """NeuralNetworkBase is an abstract base class for building neural networks.

    It provides a framework for initializing layers, performing forward and backward propagation,
    training, evaluating, and predicting with a neural network. Subclasses should implement
    the abstract methods to define specific behavior.

    Attributes:
        layer_sizes (list): Sizes of the layers in the network.
        dropout_rate (float): Dropout rate for regularization.
        reg_lambda (float): Regularization strength for L2 regularization.
        activations (list): Activation functions for each layer.
        layers (list): List of layer objects or configurations.
        weights (list): List of weight matrices for the layers.
        biases (list): List of bias vectors for the layers.
        layer_outputs (ndarray): Outputs of each layer during forward propagation.
        is_binary (bool): Whether the network is for binary classification.

    Methods:
        __init__(layers, dropout_rate=0.0, reg_lambda=0.0, activations=None, loss_function=None, regressor=False):
            Initializes the neural network with the given layers and parameters.
        initialize_layers():
            Abstract method to initialize the weights and biases of the layers.
        forward(X, training=True):
            Abstract method to perform forward propagation through the network.
        backward(y):
            Abstract method to perform backward propagation through the network.
        train(X_train, y_train, X_val=None, y_val=None, optimizer=None, epochs=100,
                batch_size=32, early_stopping_threshold=10, lr_scheduler=None, p=True,
                use_tqdm=True, n_jobs=1, track_metrics=False, track_adv_metrics=False):
            Abstract method to train the neural network using the provided training data.
        evaluate(X, y):
            Abstract method to evaluate the neural network on the provided data.
        predict(X):
            Abstract method to make predictions using the trained neural network.
        calculate_loss(X, y):
            Abstract method to calculate the loss of the neural network.
        apply_dropout(X):
            Applies dropout to the activation values for regularization.
        compute_l2_reg(weights):
            Computes the L2 regularization term for the given weights.
        calculate_precision_recall_f1(X, y):
            Calculates precision, recall, and F1 score for the predictions.
        create_scheduler(scheduler_type, optimizer, **kwargs):
            Creates a learning rate scheduler based on the specified type.
        plot_metrics(save_dir=None):
            Plots the training and validation metrics, including loss, accuracy,
            learning rate, and optionally precision, recall, and F1 score.
    """

    def __init__(
        self,
        layers,
        dropout_rate=0.0,
        reg_lambda=0.0,
        activations=None,
        loss_function=None,
        regressor=False,
    ):
        """Initializes the neural network with the specified layers, dropout rate, regularization, and activations.

        Args:
            layers: (list) - A list of integers representing the sizes of each layer or a list of Layer objects.
            dropout_rate: (float), optional - The dropout rate for regularization (default is 0.0).
            reg_lambda: (float), optional - The regularization strength (default is 0.0).
            activations: (list of str), optional - A list of activation functions for each layer (default is None, which sets "relu" for hidden layers and "softmax" for the output layer).
            loss_function: (callable), optional - Custom loss function to use (default is None, which uses the default calculate_loss implementation).
            regressor: (bool), optional - If True, the network is treated as a regressor (default is False).

        Raises:
            ValueError: If `layers` is not a list of integers or a list of Layer objects.
        """
        _layers = [DenseLayer, FlattenLayer, ConvLayer, RNNLayer]
        _layers_jit = [JITDenseLayer, JITFlattenLayer, JITConvLayer, JITRNNLayer]
        _cupy_layers = [CuPyDenseLayer]
        available_layers = tuple(_layers + _layers_jit + _cupy_layers)

        self.is_binary = (
            layers[-1] == 1
            if isinstance(layers[0], int)
            else layers[-1].output_size == 1
        ) and not regressor
        self.is_regressor = regressor  # ADDED is_regressor attribute

        if activations is None and isinstance(layers[0], int):
            # If regression, default output is 'none', else 'softmax'/'sigmoid'
            if regressor:
                default_output_activation = "none"
            else:
                default_output_activation = "sigmoid" if self.is_binary else "softmax"

            self.activations = ["relu"] * (len(layers) - 2) + [
                default_output_activation
            ]

        if loss_function is None:
            if self.is_regressor:
                # Default loss function for regression is MSE
                from .loss import MeanSquaredErrorLoss

                self.loss_function = MeanSquaredErrorLoss()
            elif self.is_binary:
                #  Default loss function for binary classification is BCE
                from .loss import BCEWithLogitsLoss

                self.loss_function = BCEWithLogitsLoss()
            else:
                #  Default loss function for multi-class classification is CrossEntropy
                from .loss import CrossEntropyLoss

                self.loss_function = CrossEntropyLoss()
        else:
            self.loss_function = loss_function

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

        # Else if all layers are Layer objects, use them directly
        elif all(isinstance(layer, available_layers) for layer in layers):
            self.layers = layers
            self.layer_sizes = [layer.input_size for layer in layers] + [
                layers[-1].output_size
            ]
            self.dropout_rate = dropout_rate
            self.reg_lambda = reg_lambda

        else:
            raise ValueError(
                "layers must be a list of integers or a list of Layer objects."
            )

    def initialize_layers(self):
        """Initializes the weights and biases of the layers."""
        raise NotImplementedError("This method should be implemented by subclasses")

    def forward(self, X, training=True):
        """Performs forward propagation through the network."""
        raise NotImplementedError("This method should be implemented by subclasses")

    def backward(self, y):
        """Performs backward propagation through the network."""
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
        """Trains the neural network using the provided training data."""
        raise NotImplementedError("This method should be implemented by subclasses")

    def evaluate(self, X, y):
        """Evaluates the neural network on the provided data."""
        raise NotImplementedError("This method should be implemented by subclasses")

    def predict(self, X):
        """Makes predictions using the trained neural network."""
        raise NotImplementedError("This method should be implemented by subclasses")

    def calculate_loss(self, X, y):
        """Calculates the loss of the neural network."""
        raise NotImplementedError("This method should be implemented by subclasses")

    def apply_dropout(self, X):
        """Applies dropout to the activation X.

        Args:
            X: (ndarray) - Activation values.

        Returns:
            ndarray: Activation values after applying dropout.
        """
        mask = np.random.rand(*X.shape) < (1 - self.dropout_rate)
        return np.multiply(X, mask) / (1 - self.dropout_rate)

    def compute_l2_reg(self, weights):
        """Computes the L2 regularization term.

        Args:
            weights: (list) - List of weight matrices.

        Returns:
            float: L2 regularization term.
        """
        total = 0.0
        for i in range(len(weights)):
            total += np.sum(weights[i] ** 2)
        return total

    def calculate_precision_recall_f1(self, X, y):
        """Calculates precision, recall, and F1 score.

        Args:
            X: (ndarray) - Input data
            y: (ndarray) - Target labels
        Returns:
            precision: (float) - Precision score
            recall: (float) - Recall score
            f1: (float) - F1 score
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
        """Plots the training and validation metrics."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError(
                "Matplotlib is required for plotting. Please install matplotlib first."
            ) from None

        if not hasattr(self, "train_loss"):
            raise ValueError(
                "No training history available. Please set track_metrics=True during training."
            ) from None

        # --- MODIFIED: Determine metrics to plot and layout ---
        metrics_to_plot = []
        if hasattr(self, "train_loss"):
            metrics_to_plot.append("loss")
        if hasattr(self, "train_metric"):  # Use the generic metric name
            metric_label = (
                "MSE" if self.is_regressor else "Accuracy"
            )  # Label appropriately
            metrics_to_plot.append(
                ("metric", metric_label)
            )  # Tuple: (attribute_suffix, plot_label)
        if hasattr(self, "learning_rates"):
            metrics_to_plot.append("learning_rate")

        # Add adv metrics only if not regressor and tracked
        if not self.is_regressor:
            if hasattr(self, "train_precision"):
                metrics_to_plot.append("precision")
            if hasattr(self, "train_recall"):
                metrics_to_plot.append("recall")
            if hasattr(self, "train_f1"):
                metrics_to_plot.append("f1")

        n_metrics = len(metrics_to_plot)
        if n_metrics == 0:
            print("No metrics tracked for plotting.")
            return

        cols = min(n_metrics, 3)
        rows = (n_metrics + cols - 1) // cols

        plt.figure(figsize=(6 * cols, 5 * rows))

        plot_idx = 1
        for metric_info in metrics_to_plot:
            if isinstance(metric_info, tuple):
                metric_attr, metric_label = metric_info
            else:
                metric_attr = metric_info
                metric_label = metric_attr.replace("_", " ").title()

            ax = plt.subplot(rows, cols, plot_idx)

            train_attr = f"train_{metric_attr}"
            val_attr = f"val_{metric_attr}"

            if metric_attr == "learning_rate":
                ax.plot(self.learning_rates, label="Learning Rate", color="red")
                ax.set_ylim(
                    [-min(self.learning_rates), max(self.learning_rates) * 1.1]
                )  # Adjust y-axis limits

            if hasattr(self, train_attr):
                ax.plot(getattr(self, train_attr), label=f"Train {metric_label}")
            if hasattr(self, val_attr):
                ax.plot(getattr(self, val_attr), label=f"Val {metric_label}")

            ax.set_title(metric_label)
            ax.set_xlabel("Epoch")
            ax.set_ylabel(metric_label)
            if hasattr(self, train_attr) or hasattr(self, val_attr):
                ax.legend()
            ax.grid(True)
            plot_idx += 1

        plt.tight_layout()

        if save_dir:
            plt.savefig(save_dir, dpi=600)
        else:
            plt.show()
        # --- END MODIFIED plotting logic ---
