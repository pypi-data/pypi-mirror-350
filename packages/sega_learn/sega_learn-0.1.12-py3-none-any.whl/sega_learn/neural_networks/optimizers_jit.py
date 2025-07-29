import numpy as np
from numba import float64, int32, njit, prange
from numba.experimental import jitclass

CACHE = False

spec_adam = [
    ("learning_rate", float64),
    ("beta1", float64),
    ("beta2", float64),
    ("epsilon", float64),
    ("reg_lambda", float64),
    ("m", float64[:, :, ::1]),  # 3D array of shape (num_layers, max_rows, max_cols)
    ("v", float64[:, :, ::1]),
    ("t", int32),
    ("dW", float64[:, :]),
    ("db", float64[:, :]),
    ("index", int32),
]


@jitclass(spec_adam)
class JITAdamOptimizer:
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
            learning_rate: (float), optional - The learning rate for the optimizer (default is 0.001).
            beta1: (float), optional - Exponential decay rate for the first moment estimates (default is 0.9).
            beta2: (float), optional - Exponential decay rate for the second moment estimates (default is 0.999).
            epsilon: (float), optional - A small value to prevent division by zero (default is 1e-8).
            reg_lambda: (float), optional - Regularization parameter; larger values imply stronger regularization (default is 0.01).
        """
        self.learning_rate = learning_rate  # Learning rate, alpha
        self.beta1 = beta1  # Exponential decay rate for the first moment estimates
        self.beta2 = beta2  # Exponential decay rate for the second moment estimates
        self.epsilon = epsilon  # Small value to prevent division by zero
        self.reg_lambda = reg_lambda  # Regularization parameter, large lambda means more regularization

        self.m = np.zeros((1, 1, 1))  # First moment estimates
        self.v = np.zeros((1, 1, 1))  # Second moment estimates
        self.t = 0  # Time step

    def initialize(self, layers):
        """Initializes the first and second moment estimates for each layer's weights.

        Args:
            layers: (list) - List of layers in the neural network.

        Returns:
            None
        """
        num_layers = len(layers)
        max_rows = 0
        max_cols = 0
        for layer in layers:
            max_rows = max(max_rows, layer.weights.shape[0])
            max_cols = max(max_cols, layer.weights.shape[1])

        self.m = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize first moment estimates
        self.v = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize second moment estimates

        for i in range(num_layers):
            layer = layers[i]
            for row in range(layer.weights.shape[0]):
                for col in range(layer.weights.shape[1]):
                    self.m[i, row, col] = 0.0
                    self.v[i, row, col] = 0.0

    def update(self, layer, dW, db, index):
        """Updates the weights and biases of a layer using the Adam optimization algorithm.

        Args:
            layer: (Layer) - The layer to update.
            dW: (np.ndarray) - The gradient of the weights.
            db: (np.ndarray) - The gradient of the biases.
            index: (int) - The index of the layer.

        Returns:
            None
        """
        if np.all(dW == 0) and np.all(db == 0):
            return  # Skip update if gradients are zero

        self.t += 1  # Increment time step
        self.m[index][: dW.shape[0], : dW.shape[1]] = (
            self.beta1 * self.m[index][: dW.shape[0], : dW.shape[1]]
            + (1 - self.beta1) * dW
        )  # Update first moment estimate
        self.v[index][: dW.shape[0], : dW.shape[1]] = self.beta2 * self.v[index][
            : dW.shape[0], : dW.shape[1]
        ] + (1 - self.beta2) * np.square(dW)  # Update second moment estimate

        m_hat = self.m[index][: dW.shape[0], : dW.shape[1]] / (
            1 - self.beta1**self.t
        )  # Bias-corrected first moment estimate
        v_hat = self.v[index][: dW.shape[0], : dW.shape[1]] / (
            1 - self.beta2**self.t
        )  # Bias-corrected second moment estimate

        layer.weights -= self.learning_rate * (
            m_hat / (np.sqrt(v_hat) + self.epsilon)
            + self.reg_lambda * layer.weights[: dW.shape[0], : dW.shape[1]]
        )  # Update weights
        layer.biases -= self.learning_rate * db  # Update biases

    def update_layers(self, layers, dWs, dbs):
        """Updates all layers' weights and biases using the Adam optimization algorithm.

        Args:
            layers: (list) - List of layers in the neural network.
            dWs: (list of np.ndarray) - Gradients of the weights for each layer.
            dbs: (list of np.ndarray) - Gradients of the biases for each layer.

        Returns:
            None
        """
        # Increment timestep by number of layers
        self.t += len(layers)
        adam_update_layers(
            self.m,
            self.v,
            self.t,
            layers,
            dWs,
            dbs,
            self.learning_rate,
            self.beta1,
            self.beta2,
            self.epsilon,
            self.reg_lambda,
        )


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def adam_update_layers(
    m, v, t, layers, dWs, dbs, learning_rate, beta1, beta2, epsilon, reg_lambda
):
    """Performs parallelized Adam updates for all layers.

    Args:
        m: (np.ndarray) - First moment estimates.
        v: (np.ndarray) - Second moment estimates.
        t: (int) - Current time step.
        layers: (list) - List of layers in the neural network.
        dWs: (list of np.ndarray) - Gradients of the weights for each layer.
        dbs: (list of np.ndarray) - Gradients of the biases for each layer.
        learning_rate: (float) - Learning rate for the optimizer.
        beta1: (float) - Exponential decay rate for the first moment estimates.
        beta2: (float) - Exponential decay rate for the second moment estimates.
        epsilon: (float) - Small value to prevent division by zero.
        reg_lambda: (float) - Regularization parameter.

    Returns:
        None
    """
    for i in prange(len(layers)):
        layer = layers[i]
        dW = dWs[i]
        db = dbs[i]
        rows, cols = dW.shape

        # Update first and second moment estimates
        m[i, :rows, :cols] = beta1 * m[i, :rows, :cols] + (1 - beta1) * dW
        v[i, :rows, :cols] = beta2 * v[i, :rows, :cols] + (1 - beta2) * (dW**2)

        # Bias-corrected estimates
        m_hat = m[i, :rows, :cols] / (1 - beta1**t)
        v_hat = v[i, :rows, :cols] / (1 - beta2**t)

        # Update weights and biases
        layer.weights[:rows, :cols] -= learning_rate * (
            m_hat / (np.sqrt(v_hat) + epsilon)
            + reg_lambda * layer.weights[:rows, :cols]
        )
        layer.biases -= learning_rate * db


spec_sgd = [
    ("learning_rate", float64),
    ("momentum", float64),
    ("reg_lambda", float64),
    ("velocity", float64[:, :, ::1]),
]


@jitclass(spec_sgd)
class JITSGDOptimizer:
    """Stochastic Gradient Descent (SGD) optimizer class for training neural networks.

    Formula: w = w - learning_rate * dW, b = b - learning_rate * db
    Args:
        learning_rate (float, optional): The learning rate for the optimizer. Defaults to 0.001.
        momentum (float, optional): The momentum factor. Defaults to 0.0.
        reg_lambda (float, optional): The regularization parameter. Defaults to 0.0.
    """

    def __init__(self, learning_rate=0.001, momentum=0.0, reg_lambda=0.0):
        """Initializes the optimizer with specified hyperparameters.

        Args:
            learning_rate: (float), optional - The learning rate for the optimizer (default is 0.001).
            momentum: (float), optional - The momentum factor for the optimizer (default is 0.0).
            reg_lambda: (float), optional - The regularization parameter (default is 0.0).

        Attributes:
            learning_rate: (float) - The learning rate for the optimizer.
            momentum: (float) - The momentum factor for the optimizer.
            reg_lambda: (float) - The regularization parameter.
            velocity: (np.ndarray) - The velocity used for momentum updates, initialized to zeros.
        """
        self.learning_rate = learning_rate  # Learning rate
        self.momentum = momentum  # Momentum factor
        self.reg_lambda = reg_lambda  # Regularization parameter
        self.velocity = np.zeros((1, 1, 1))  # Velocity for momentum

    def initialize(self, layers):
        """Initializes the velocity for each layer's weights.

        Args:
            layers: (list) - List of layers in the neural network.

        Returns:
            None
        """
        num_layers = len(layers)
        max_rows = 0
        max_cols = 0
        for layer in layers:
            max_rows = max(max_rows, layer.weights.shape[0])
            max_cols = max(max_cols, layer.weights.shape[1])

        self.velocity = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize velocity as a NumPy array

        for i in range(num_layers):
            layer = layers[i]
            for row in range(layer.weights.shape[0]):
                for col in range(layer.weights.shape[1]):
                    self.velocity[i, row, col] = 0.0

    def update(self, layer, dW, db, index):
        """Updates the weights and biases of a layer using the SGD optimization algorithm.

        Args:
            layer: (Layer) - The layer to update.
            dW: (np.ndarray) - The gradient of the weights.
            db: (np.ndarray) - The gradient of the biases.
            index: (int) - The index of the layer.

        Returns:
           None
        """
        self.velocity[index][: dW.shape[0], : dW.shape[1]] = (
            self.momentum * self.velocity[index][: dW.shape[0], : dW.shape[1]]
            - self.learning_rate * dW
        )  # Update velocity
        layer.weights[: dW.shape[0], : dW.shape[1]] += (
            self.velocity[index][: dW.shape[0], : dW.shape[1]]
            - self.learning_rate
            * self.reg_lambda
            * layer.weights[: dW.shape[0], : dW.shape[1]]
        )  # Update weights
        layer.biases[: db.shape[0], : db.shape[1]] -= (
            self.learning_rate * db
        )  # Update biases

    def update_layers(self, layers, dWs, dbs):
        """Updates all layers' weights and biases using the SGD optimization algorithm.

        Args:
            layers: (list) - List of layers in the neural network.
            dWs: (list of np.ndarray) - Gradients of the weights for each layer.
            dbs: (list of np.ndarray) - Gradients of the biases for each layer.

        Returns:
            None
        """
        sgd_update_layers(
            self.velocity,
            layers,
            dWs,
            dbs,
            self.learning_rate,
            self.momentum,
            self.reg_lambda,
        )


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def sgd_update_layers(velocity, layers, dWs, dbs, learning_rate, momentum, reg_lambda):
    """Performs parallelized SGD updates for all layers.

    Args:
        velocity: (np.ndarray) - Velocity for momentum.
        layers: (list) - List of layers in the neural network.
        dWs: (list of np.ndarray) - Gradients of the weights for each layer.
        dbs: (list of np.ndarray) - Gradients of the biases for each layer.
        learning_rate: (float) - Learning rate for the optimizer.
        momentum: (float) - Momentum factor.
        reg_lambda: (float) - Regularization parameter.

    Returns:
        None
    """
    for i in prange(len(layers)):
        layer = layers[i]
        dW = dWs[i]
        db = dbs[i]
        rows, cols = dW.shape

        # Update velocity with momentum
        velocity[i, :rows, :cols] = (
            momentum * velocity[i, :rows, :cols] - learning_rate * dW
        )

        # Update weights and biases
        layer.weights[:rows, :cols] += (
            velocity[i, :rows, :cols]
            - learning_rate * reg_lambda * layer.weights[:rows, :cols]
        )
        layer.biases -= learning_rate * db


spec_adadelta = [
    ("learning_rate", float64),
    ("rho", float64),
    ("epsilon", float64),
    ("reg_lambda", float64),
    ("E_g2", float64[:, :, ::1]),
    ("E_delta_x2", float64[:, :, ::1]),
]


@jitclass(spec_adadelta)
class JITAdadeltaOptimizer:
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
        """Initializes the optimizer with specified hyperparameters.

        Args:
            learning_rate: (float), optional - The learning rate for the optimizer (default is 1.0).
            rho: (float), optional - The decay rate for the running averages (default is 0.95).
            epsilon: (float), optional - A small value to prevent division by zero (default is 1e-6).
            reg_lambda: (float), optional - The regularization parameter (default is 0.0).

        Attributes:
            E_g2: (np.ndarray) - Running average of squared gradients.
            E_delta_x2: (np.ndarray) - Running average of squared parameter updates.
        """
        self.learning_rate = learning_rate  # Learning rate
        self.rho = rho  # Decay rate
        self.epsilon = epsilon  # Small value to prevent division by zero
        self.reg_lambda = reg_lambda  # Regularization parameter

        self.E_g2 = np.zeros((1, 1, 1))  # Running average of squared gradients
        self.E_delta_x2 = np.zeros(
            (1, 1, 1)
        )  # Running average of squared parameter updates

    def initialize(self, layers):
        """Initializes the running averages for each layer's weights.

        Args:
            layers: (list) - List of layers in the neural network.

        Returns:
            None
        """
        num_layers = len(layers)
        max_rows = 0
        max_cols = 0
        for layer in layers:
            max_rows = max(max_rows, layer.weights.shape[0])
            max_cols = max(max_cols, layer.weights.shape[1])

        self.E_g2 = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize running average of squared gradients
        self.E_delta_x2 = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize running average of squared parameter updates

        for i in range(num_layers):
            layer = layers[i]
            for row in range(layer.weights.shape[0]):
                for col in range(layer.weights.shape[1]):
                    self.E_g2[i, row, col] = 0.0
                    self.E_delta_x2[i, row, col] = 0.0

    def update(self, layer, dW, db, index):
        """Updates the weights and biases of a layer using the Adadelta optimization algorithm.

        Args:
            layer: (Layer) - The layer to update.
            dW: (np.ndarray) - The gradient of the weights.
            db: (np.ndarray) - The gradient of the biases.
            index: (int) - The index of the layer.

        Returns:
            None
        """
        self.E_g2[index][: dW.shape[0], : dW.shape[1]] = self.rho * self.E_g2[index][
            : dW.shape[0], : dW.shape[1]
        ] + (1 - self.rho) * np.square(
            dW
        )  # Update running average of squared gradients
        delta_x = (
            -(
                np.sqrt(
                    self.E_delta_x2[index][: dW.shape[0], : dW.shape[1]] + self.epsilon
                )
                / np.sqrt(self.E_g2[index][: dW.shape[0], : dW.shape[1]] + self.epsilon)
            )
            * dW
        )  # Compute parameter update
        self.E_delta_x2[index][: dW.shape[0], : dW.shape[1]] = (
            self.rho * self.E_delta_x2[index][: dW.shape[0], : dW.shape[1]]
            + (1 - self.rho) * np.square(delta_x)
        )  # Update running average of squared parameter updates

        layer.weights[: dW.shape[0], : dW.shape[1]] += (
            delta_x
            - self.learning_rate
            * self.reg_lambda
            * layer.weights[: dW.shape[0], : dW.shape[1]]
        )  # Update weights
        layer.biases[: db.shape[0], : db.shape[1]] -= (
            self.learning_rate * db
        )  # Update biases

    def update_layers(self, layers, dWs, dbs):
        """Updates all layers' weights and biases using the Adadelta optimization algorithm.

        Args:
            layers: (list) - List of layers in the neural network.
            dWs: (list of np.ndarray) - Gradients of the weights for each layer.
            dbs: (list of np.ndarray) - Gradients of the biases for each layer.

        Returns:
            None
        """
        adadelta_update_layers(
            self.E_g2,
            self.E_delta_x2,
            layers,
            dWs,
            dbs,
            self.learning_rate,
            self.rho,
            self.epsilon,
            self.reg_lambda,
        )


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def adadelta_update_layers(
    E_g2, E_delta_x2, layers, dWs, dbs, learning_rate, rho, epsilon, reg_lambda
):
    """Performs parallelized Adadelta updates for all layers.

    Args:
        E_g2: (np.ndarray) - Running average of squared gradients.
        E_delta_x2: (np.ndarray) - Running average of squared parameter updates.
        layers: (list) - List of layers in the neural network.
        dWs: (list of np.ndarray) - Gradients of the weights for each layer.
        dbs: (list of np.ndarray) - Gradients of the biases for each layer.
        learning_rate: (float) - Learning rate for the optimizer.
        rho: (float) - Decay rate.
        epsilon: (float) - Small value to prevent division by zero.
        reg_lambda: (float) - Regularization parameter.

    Returns:
        None
    """
    for i in prange(len(layers)):
        layer = layers[i]
        dW = dWs[i]
        db = dbs[i]
        rows, cols = dW.shape

        # Update running average of squared gradients
        E_g2[i, :rows, :cols] = rho * E_g2[i, :rows, :cols] + (1 - rho) * (dW**2)

        # Compute parameter update
        delta_x = (
            -(
                np.sqrt(E_delta_x2[i, :rows, :cols] + epsilon)
                / np.sqrt(E_g2[i, :rows, :cols] + epsilon)
            )
            * dW
        )

        # Update running average of squared parameter updates
        E_delta_x2[i, :rows, :cols] = rho * E_delta_x2[i, :rows, :cols] + (1 - rho) * (
            delta_x**2
        )

        # Update weights and biases
        layer.weights[:rows, :cols] += (
            delta_x - learning_rate * reg_lambda * layer.weights[:rows, :cols]
        )
        layer.biases -= learning_rate * db
