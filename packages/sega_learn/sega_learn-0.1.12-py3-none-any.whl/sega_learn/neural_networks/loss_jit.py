import numpy as np
from numba import njit, prange

from .numba_utils import calculate_huber_loss, calculate_mae_loss, calculate_mse_loss

CACHE = False


def _validate_shapes(logits, targets):
    """Validate that logits and targets have compatible shapes."""
    if logits.shape[0] != targets.shape[0]:
        raise ValueError(
            f"Shape mismatch: logits {logits.shape} vs targets {targets.shape}"
        )
    return logits, targets


# JIT Classification Loss Classes
class JITCrossEntropyLoss:
    """Custom cross entropy loss implementation using numba for multi-class classification.

    Formula: -sum(y * log(p) + (1 - y) * log(1 - p)) / m
    Methods:
        calculate_loss(self, logits, targets): Calculate the cross entropy loss.
    """

    def __init__(self):
        """Initializes the instance variables for the class.

        Args:
            logits: (np.ndarray) - A 2D array initialized to zeros with shape (1, 1),
                       representing the predicted values or outputs of the model.
            targets: (np.ndarray) - A 2D array initialized to zeros with shape (1, 1),
                        representing the ground truth or target values.
        """
        self.logits = np.zeros((1, 1))
        self.targets = np.zeros((1, 1))

    def calculate_loss(self, logits, targets):
        """Calculate the cross entropy loss.

        Args:
            logits (np.ndarray): The logits (predicted values) of shape (num_samples, num_classes).
            targets (np.ndarray): The target labels of shape (num_samples,).

        Returns:
            float: The cross entropy loss.
        """
        logits, targets = _validate_shapes(logits, targets)
        return calculate_cross_entropy_loss(logits, targets)


@njit(fastmath=True, nogil=True, cache=CACHE)
def calculate_cross_entropy_loss(logits, targets):
    """Helper function to calculate the cross entropy loss."""
    n = logits.shape[0]
    loss = 0.0
    for i in prange(n):
        max_val = np.max(logits[i])
        exp_sum = 0.0
        for j in range(logits.shape[1]):
            exp_sum += np.exp(logits[i, j] - max_val)
        log_sum_exp = max_val + np.log(exp_sum)
        c_i = np.argmax(targets[i])  # True class index, assuming one-hot targets
        loss += -logits[i, c_i] + log_sum_exp
    return loss / n


class JITBCEWithLogitsLoss:
    """Custom binary cross entropy loss with logits implementation using numba.

    Formula: -mean(y * log(p) + (1 - y) * log(1 - p))

    Methods:
        calculate_loss(self, logits, targets): Calculate the binary cross entropy loss.
    """

    def __init__(self):
        """Initializes the class with default values for logits and targets.

        Attributes:
            logits (numpy.ndarray): A 2D array initialized to zeros with shape (1, 1),
                                    representing the predicted values.
            targets (numpy.ndarray): A 2D array initialized to zeros with shape (1, 1),
                                     representing the true target values.
        """
        self.logits = np.zeros((1, 1))
        self.targets = np.zeros((1, 1))

    def calculate_loss(self, logits, targets):
        """Calculate the binary cross entropy loss.

        Args:
            logits (np.ndarray): The logits (predicted values) of shape (num_samples,).
            targets (np.ndarray): The target labels of shape (num_samples,).

        Returns:
            float: The binary cross entropy loss.
        """
        logits, targets = _validate_shapes(logits, targets)
        return calculate_bce_with_logits_loss(logits, targets)


@njit(fastmath=True, nogil=True, cache=CACHE)
def calculate_bce_with_logits_loss(logits, targets):
    """Helper function to calculate the binary cross entropy loss."""
    probs = 1 / (1 + np.exp(-logits))  # Apply sigmoid to logits to get probabilities
    loss = -np.mean(
        targets * np.log(probs + 1e-15) + (1 - targets) * np.log(1 - probs + 1e-15)
    )  # Binary cross-entropy loss
    return loss


# JIT Regression Loss Classes
class JITMeanSquaredErrorLoss:
    """Custom mean squared error loss implementation using numba."""

    def calculate_loss(self, y_pred, y_true):
        """Calculate the mean squared error loss."""
        y_pred, y_true = _validate_shapes(y_pred, y_true)
        return calculate_mse_loss(y_pred, y_true)


class JITMeanAbsoluteErrorLoss:
    """Custom mean absolute error loss implementation using numba."""

    def calculate_loss(self, y_pred, y_true):
        """Calculate the mean absolute error loss."""
        y_pred, y_true = _validate_shapes(y_pred, y_true)
        return calculate_mae_loss(y_pred, y_true)


class JITHuberLoss:
    """Custom Huber loss implementation using numba.

    Attributes:
        delta (float): The threshold parameter for Huber loss. Default is 1.0.
    """

    def __init__(self, delta=1.0):
        """Initializes the JITHuberLoss instance.

        Args:
            delta (float): The threshold at which the loss function transitions
                           from quadratic to linear. Default is 1.0.
        """
        self.delta = float(delta)  # Ensure delta is float

    def calculate_loss(self, y_pred, y_true):
        """Calculate the Huber loss using the stored delta.

        Args:
            y_pred (np.ndarray): Predicted values.
            y_true (np.ndarray): True target values.

        Returns:
            float: The calculated Huber loss.
        """
        y_pred, y_true = _validate_shapes(y_pred, y_true)
        return calculate_huber_loss(y_pred, y_true, self.delta)
