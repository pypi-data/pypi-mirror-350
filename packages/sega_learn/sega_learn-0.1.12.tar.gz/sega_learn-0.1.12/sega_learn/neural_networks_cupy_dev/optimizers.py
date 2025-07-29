import cupy as cp


class AdamOptimizer:
    """
    Adam optimizer class for training neural networks.
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
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.reg_lambda = reg_lambda
        self.m = None
        self.v = None
        self.t = 0

    def initialize(self, layers):
        self.m = [cp.zeros_like(layer.weights) for layer in layers]
        self.v = [cp.zeros_like(layer.weights) for layer in layers]

    def update_layers(self, layers, dWs, dbs):
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


class SGDOptimizer:
    """
    Stochastic Gradient Descent (SGD) optimizer class for training neural networks.
    Formula: v = momentum * v - learning_rate * dW, w = w + v - learning_rate * reg_lambda * w
    Args:
        learning_rate (float, optional): The learning rate for the optimizer. Defaults to 0.001.
        momentum (float, optional): The momentum factor. Defaults to 0.0.
        reg_lambda (float, optional): The regularization parameter. Defaults to 0.0.
    """

    def __init__(self, learning_rate=0.001, momentum=0.0, reg_lambda=0.0):
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.reg_lambda = reg_lambda
        self.velocity = None

    def initialize(self, layers):
        self.velocity = [cp.zeros_like(layer.weights) for layer in layers]

    def update_layers(self, layers, dWs, dbs):
        for i, layer in enumerate(layers):
            self.velocity[i] = (
                self.momentum * self.velocity[i] - self.learning_rate * dWs[i]
            )
            layer.weights += (
                self.velocity[i] - self.learning_rate * self.reg_lambda * layer.weights
            )
            layer.biases -= self.learning_rate * dbs[i]


class AdadeltaOptimizer:
    """
    Adadelta optimizer class for training neural networks.
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
        self.learning_rate = learning_rate
        self.rho = rho
        self.epsilon = epsilon
        self.reg_lambda = reg_lambda
        self.E_g2 = None
        self.E_delta_x2 = None

    def initialize(self, layers):
        self.E_g2 = [cp.zeros_like(layer.weights) for layer in layers]
        self.E_delta_x2 = [cp.zeros_like(layer.weights) for layer in layers]

    def update_layers(self, layers, dWs, dbs):
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
