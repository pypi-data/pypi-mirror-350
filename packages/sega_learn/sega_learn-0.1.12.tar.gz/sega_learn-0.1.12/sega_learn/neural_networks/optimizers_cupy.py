import cupy as cp


class CuPyAdamOptimizer:
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
        """Initializes the optimizer with the specified hyperparameters.

        Args:
            learning_rate: (float), optional - The step size for updating weights (default is 0.001).
            beta1: (float), optional - Exponential decay rate for the first moment estimates (default is 0.9).
            beta2: (float), optional - Exponential decay rate for the second moment estimates (default is 0.999).
            epsilon: (float), optional - A small constant to prevent division by zero (default is 1e-8).
            reg_lambda: (float), optional - Regularization parameter for weight decay (default is 0.01).
        """
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.reg_lambda = reg_lambda
        self.m = None
        self.v = None
        self.t = 0

    def initialize(self, layers):
        """Initializes the optimizer's internal state for the given layers.

        Args:
            layers: (list) - A list of layers, each containing weights and biases.
        """
        self.m = [cp.zeros_like(layer.weights) for layer in layers]
        self.v = [cp.zeros_like(layer.weights) for layer in layers]

    def update_layers(self, layers, dWs, dbs):
        """Updates the weights and biases of the layers using Adam optimization.

        Args:
            layers: (list) - A list of layers to update.
            dWs: (list) - Gradients of the weights for each layer.
            dbs: (list) - Gradients of the biases for each layer.
        """
        self.t += 1
        for i, layer in enumerate(layers):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * dWs[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (dWs[i] ** 2)
            m_hat = self.m[i] / (1 - self.beta1**self.t)
            v_hat = self.v[i] / (1 - self.beta2**self.t)
            layer.weights -= self.learning_rate * (
                m_hat / (cp.sqrt(v_hat) + self.epsilon)
                + self.reg_lambda * layer.weights
            )
            layer.biases -= self.learning_rate * dbs[i]


class CuPySGDOptimizer:
    """Stochastic Gradient Descent (SGD) optimizer class for training neural networks.

    Formula: v = momentum * v - learning_rate * dW, w = w + v - learning_rate * reg_lambda * w

    Args:
        learning_rate (float, optional): The learning rate for the optimizer. Defaults to 0.001.
        momentum (float, optional): The momentum factor. Defaults to 0.0.
        reg_lambda (float, optional): The regularization parameter. Defaults to 0.0.
    """

    def __init__(self, learning_rate=0.001, momentum=0.0, reg_lambda=0.0):
        """Initializes the optimizer with specified hyperparameters.

        Args:
            learning_rate: (float), optional - The step size for updating weights (default is 0.001).
            momentum: (float), optional - The momentum factor for accelerating gradient descent (default is 0.0).
            reg_lambda: (float), optional - The regularization strength to prevent overfitting (default is 0.0).

        Attributes:
            velocity: (None or np.ndarray) - The velocity term used for momentum-based updates (initialized as None).
        """
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.reg_lambda = reg_lambda
        self.velocity = None

    def initialize(self, layers):
        """Initializes the optimizer's velocity for the given layers.

        Args:
            layers: (list) - A list of layers, each containing weights and biases.
        """
        self.velocity = [cp.zeros_like(layer.weights) for layer in layers]

    def update_layers(self, layers, dWs, dbs):
        """Updates the weights and biases of the layers using SGD optimization.

        Args:
            layers: (list) - A list of layers to update.
            dWs: (list) - Gradients of the weights for each layer.
            dbs: (list) - Gradients of the biases for each layer.
        """
        for i, layer in enumerate(layers):
            self.velocity[i] = (
                self.momentum * self.velocity[i] - self.learning_rate * dWs[i]
            )
            layer.weights += (
                self.velocity[i] - self.learning_rate * self.reg_lambda * layer.weights
            )
            layer.biases -= self.learning_rate * dbs[i]


class CuPyAdadeltaOptimizer:
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
            learning_rate: (float), optional - The learning rate for the optimizer (default is 1.0).
            rho: (float), optional - The decay rate for the moving average of squared gradients (default is 0.95).
            epsilon: (float), optional - A small constant to prevent division by zero (default is 1e-6).
            reg_lambda: (float), optional - The regularization parameter for weight decay (default is 0.0).

        Attributes:
            E_g2: (None or np.ndarray) - The moving average of squared gradients, initialized as None.
            E_delta_x2: (None or np.ndarray) - The moving average of squared parameter updates, initialized as None.
        """
        self.learning_rate = learning_rate
        self.rho = rho
        self.epsilon = epsilon
        self.reg_lambda = reg_lambda
        self.E_g2 = None
        self.E_delta_x2 = None

    def initialize(self, layers):
        """Initializes the optimizer's internal state for the given layers.

        Args:
            layers: (list) - A list of layers, each containing weights and biases.
        """
        self.E_g2 = [cp.zeros_like(layer.weights) for layer in layers]
        self.E_delta_x2 = [cp.zeros_like(layer.weights) for layer in layers]

    def update_layers(self, layers, dWs, dbs):
        """Updates the weights and biases of the layers using Adadelta optimization.

        Args:
            layers: (list) - A list of layers to update.
            dWs: (list) - Gradients of the weights for each layer.
            dbs: (list) - Gradients of the biases for each layer.
        """
        for i, layer in enumerate(layers):
            self.E_g2[i] = self.rho * self.E_g2[i] + (1 - self.rho) * (dWs[i] ** 2)
            delta_x = (
                -(
                    cp.sqrt(self.E_delta_x2[i] + self.epsilon)
                    / cp.sqrt(self.E_g2[i] + self.epsilon)
                )
                * dWs[i]
            )
            self.E_delta_x2[i] = self.rho * self.E_delta_x2[i] + (1 - self.rho) * (
                delta_x**2
            )
            layer.weights += (
                delta_x - self.learning_rate * self.reg_lambda * layer.weights
            )
            layer.biases -= self.learning_rate * dbs[i]
