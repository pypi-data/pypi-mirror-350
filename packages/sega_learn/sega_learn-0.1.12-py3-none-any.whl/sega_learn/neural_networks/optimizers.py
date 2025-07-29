import numpy as np

from .layers import FlattenLayer


class AdamOptimizer:
    """Adam optimizer class for training neural networks.

    Formula: w = w - alpha * m_hat / (sqrt(v_hat) + epsilon) - lambda * w
    Derived from: https://arxiv.org/abs/1412.6980

    Args:
        learning_rate (float, optional): The learning rate for the optimizer. Defaults to 0.001.
        beta1 (float, optional): The exponential decay rate for the first moment estimates. Defaults to 0.9.
        beta2 (float, optional): The exponential decay rate for the second moment estimates. Defaults to 0.999.
        epsilon (float, optional): A small value to prevent division by zero. Defaults to 1e-8.
        reg_lambda (float, optional): The regularization parameter. Defaults to 0.01.
    """

    def __init__(
        self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, reg_lambda=0.01
    ):
        """Initializes the optimizer with the given hyperparameters.

        Args:
            learning_rate (float, optional): The learning rate (alpha) for the optimizer. Defaults to 0.001.
            beta1 (float, optional): Exponential decay rate for the first moment estimates. Defaults to 0.9.
            beta2 (float, optional): Exponential decay rate for the second moment estimates. Defaults to 0.999.
            epsilon (float, optional): A small value to prevent division by zero. Defaults to 1e-8.
            reg_lambda (float, optional): Regularization parameter; higher values indicate stronger regularization. Defaults to 0.01.

        Attributes:
            learning_rate (float): The learning rate for the optimizer.
            beta1 (float): Exponential decay rate for the first moment estimates.
            beta2 (float): Exponential decay rate for the second moment estimates.
            epsilon (float): A small value to prevent division by zero.
            reg_lambda (float): Regularization parameter for controlling overfitting.
            m (list): List to store first moment estimates for each parameter.
            v (list): List to store second moment estimates for each parameter.
            t (int): Time step counter for the optimizer.
        """
        self.learning_rate = learning_rate  # Learning rate, alpha
        self.beta1 = beta1  # Exponential decay rate for the first moment estimates
        self.beta2 = beta2  # Exponential decay rate for the second moment estimates
        self.epsilon = epsilon  # Small value to prevent division by zero
        self.reg_lambda = reg_lambda  # Regularization parameter, large lambda means more regularization

        self.m = []  # First moment estimates
        self.v = []  # Second moment estimates
        self.t = 0  # Time step

    def initialize(self, layers):
        """Initializes the first and second moment estimates for each layer's weights.

        Args:
            layers (list): List of layers in the neural network.

        Returns:
            None
        """
        for layer in layers:  # For each layer in the neural network.
            if isinstance(
                layer, FlattenLayer
            ):  # FlattenLayer has no trainable parameters.
                continue
            self.m.append(
                np.zeros_like(layer.weights)
            )  # Initialize first moment estimates
            self.v.append(
                np.zeros_like(layer.weights)
            )  # Initialize second moment estimates

    def update(self, layer, dW, db, index):
        """Updates the weights and biases of a layer using the Adam optimization algorithm.

        Args:
            layer (Layer): The layer to update.
            dW (ndarray): The gradient of the weights.
            db (ndarray): The gradient of the biases.
            index (int): The index of the layer.
        Returns: None
        """
        self.t += 1  # Increment time step
        self.m[index] = (
            self.beta1 * self.m[index] + (1 - self.beta1) * dW
        )  # Update first moment estimate, beta1 * m + (1 - beta1) * dW
        self.v[index] = self.beta2 * self.v[index] + (1 - self.beta2) * np.square(
            dW
        )  # Update second moment estimate, beta2 * v + (1 - beta2) * dW^2

        m_hat = self.m[index] / (
            1 - self.beta1**self.t
        )  # Bias-corrected first moment estimate, m / (1 - beta1^t)
        v_hat = self.v[index] / (
            1 - self.beta2**self.t
        )  # Bias-corrected second moment estimate, v / (1 - beta2^t)

        weight_update = m_hat / (np.sqrt(v_hat) + self.epsilon)
        if not np.allclose(
            dW, 0
        ):  # Apply regularization only if gradients are non-zero
            weight_update += self.reg_lambda * layer.weights

        layer.weights -= self.learning_rate * weight_update  # Update weights
        layer.biases -= self.learning_rate * db  # Update biases


class SGDOptimizer:
    """Stochastic Gradient Descent (SGD) optimizer class for training neural networks.

    Formula: w = w - learning_rate * dW, b = b - learning_rate * db

    Args:
        learning_rate (float, optional): The learning rate for the optimizer. Defaults to 0.001.
        momentum (float, optional): The momentum factor. Defaults to 0.0.
        reg_lambda (float, optional): The regularization parameter. Defaults to 0.0.
    """

    def __init__(self, learning_rate=0.001, momentum=0.0, reg_lambda=0.0):
        """Initializes the optimizer with specified parameters.

        Args:
            learning_rate (float, optional): The step size for updating weights. Defaults to 0.001.
            momentum (float, optional): The momentum factor to accelerate gradient descent. Defaults to 0.0.
            reg_lambda (float, optional): The regularization parameter to prevent overfitting. Defaults to 0.0.
        """
        self.learning_rate = learning_rate  # Learning rate
        self.momentum = momentum  # Momentum factor
        self.reg_lambda = reg_lambda  # Regularization parameter
        self.velocity = []  # Velocity for momentum

    def initialize(self, layers):
        """Initializes the velocity for each layer's weights.

        Args:
            layers (list): List of layers in the neural network.

        Returns:
            None
        """
        for layer in layers:  # For each layer in the neural network..
            self.velocity.append(np.zeros_like(layer.weights))  # Initialize velocity

    def update(self, layer, dW, db, index):
        """Updates the weights and biases of a layer using the SGD optimization algorithm.

        Args:
            layer (Layer): The layer to update.
            dW (ndarray): The gradient of the weights.
            db (ndarray): The gradient of the biases.
            index (int): The index of the layer.

        Returns:
            None
        """
        self.velocity[index] = (
            self.momentum * self.velocity[index] - self.learning_rate * dW
        )  # Update velocity
        layer.weights += (
            self.velocity[index] - self.learning_rate * self.reg_lambda * layer.weights
        )  # Update weights
        layer.biases -= self.learning_rate * db  # Update biases


class AdadeltaOptimizer:
    """Adadelta optimizer class for training neural networks.

    Formula:
        E[g^2]_t = rho * E[g^2]_{t-1} + (1 - rho) * g^2
        Delta_x = - (sqrt(E[delta_x^2]_{t-1} + epsilon) / sqrt(E[g^2]_t + epsilon)) * g
        E[delta_x^2]_t = rho * E[delta_x^2]_{t-1} + (1 - rho) * Delta_x^2
    Derived from: https://arxiv.org/abs/1212.5701

    Args:
        learning_rate (float, optional): The learning rate for the optimizer. Defaults to 1.0.
        rho (float, optional): The decay rate. Defaults to 0.95.
        epsilon (float, optional): A small value to prevent division by zero. Defaults to 1e-6.
        reg_lambda (float, optional): The regularization parameter. Defaults to 0.0.
    """

    def __init__(self, learning_rate=1.0, rho=0.95, epsilon=1e-6, reg_lambda=0.0):
        """Initializes the optimizer with the specified hyperparameters.

        Args:
            learning_rate (float, optional): The learning rate for the optimizer. Defaults to 1.0.
            rho (float, optional): The decay rate for the running averages. Defaults to 0.95.
            epsilon (float, optional): A small value to prevent division by zero. Defaults to 1e-6.
            reg_lambda (float, optional): The regularization parameter for weight decay. Defaults to 0.0.
        """
        self.learning_rate = learning_rate  # Learning rate
        self.rho = rho  # Decay rate
        self.epsilon = epsilon  # Small value to prevent division by zero
        self.reg_lambda = reg_lambda  # Regularization parameter

        self.E_g2 = []  # Running average of squared gradients
        self.E_delta_x2 = []  # Running average of squared parameter updates

    def initialize(self, layers):
        """Initializes the running averages for each layer's weights.

        Args:
            layers (list): List of layers in the neural network.

        Returns:
            None
        """
        for layer in layers:  # For each layer in the neural network..
            self.E_g2.append(
                np.zeros_like(layer.weights)
            )  # Initialize running average of squared gradients
            self.E_delta_x2.append(
                np.zeros_like(layer.weights)
            )  # Initialize running average of squared parameter updates

    def update(self, layer, dW, db, index):
        """Updates the weights and biases of a layer using the Adadelta optimization algorithm.

        Args:
            layer (Layer): The layer to update.
            dW (ndarray): The gradient of the weights.
            db (ndarray): The gradient of the biases.
            index (int): The index of the layer.

        Returns:
            None
        """
        self.E_g2[index] = self.rho * self.E_g2[index] + (1 - self.rho) * np.square(
            dW
        )  # Update running average of squared gradients
        delta_x = (
            -(
                np.sqrt(self.E_delta_x2[index] + self.epsilon)
                / np.sqrt(self.E_g2[index] + self.epsilon)
            )
            * dW
        )  # Compute parameter update
        self.E_delta_x2[index] = self.rho * self.E_delta_x2[index] + (
            1 - self.rho
        ) * np.square(delta_x)  # Update running average of squared parameter updates

        layer.weights += (
            delta_x - self.learning_rate * self.reg_lambda * layer.weights
        )  # Update weights
        layer.biases -= self.learning_rate * db  # Update biases
