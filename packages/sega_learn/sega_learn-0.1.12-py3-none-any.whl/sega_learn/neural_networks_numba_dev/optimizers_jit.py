import warnings

import numba.core.errors
import numpy as np
from numba import float64, int32, njit, prange, types
from numba.experimental import jitclass
from numba.typed import List

warnings.filterwarnings("ignore", category=numba.core.errors.NumbaTypeSafetyWarning)

CACHE = False

spec_adam = [
    ("layer_type", types.unicode_type),  # 'dense' or 'conv'
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
        self.learning_rate = learning_rate  # Learning rate, alpha
        self.beta1 = beta1  # Exponential decay rate for the first moment estimates
        self.beta2 = beta2  # Exponential decay rate for the second moment estimates
        self.epsilon = epsilon  # Small value to prevent division by zero
        self.reg_lambda = reg_lambda  # Regularization parameter, large lambda means more regularization

        self.m = np.zeros((1, 1, 1))  # First moment estimates
        self.v = np.zeros((1, 1, 1))  # Second moment estimates
        self.t = 0  # Time step

    def initialize(self, layers):
        """
        Initializes the first and second moment estimates for each layer's weights.
        Args:
            layers (list): List of layers in the neural network.
            layer_type (str): Type of layers ('dense' or 'conv').
        Returns: None
        """
        num_layers = len(layers)
        max_rows = 0
        max_cols = 0
        for layer in layers:
            if layer.layer_type == "dense":
                max_rows = max(max_rows, layer.dense_weights.shape[0])
                max_cols = max(max_cols, layer.dense_weights.shape[1])
            elif layer.layer_type == "conv":
                max_rows = max(max_rows, layer.conv_weights.shape[0])
                max_cols = max(max_cols, layer.conv_weights.shape[1])

        self.m = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize first moment estimates
        self.v = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize second moment estimates

        for i, layer in enumerate(layers):
            if layer.layer_type == "dense":
                for row in range(int(layer.dense_weights.shape[0])):
                    for col in range(int(layer.dense_weights.shape[1])):
                        self.m[i, row, col] = 0.0
                        self.v[i, row, col] = 0.0
            elif layer.layer_type == "conv":
                for row in range(int(layer.conv_weights.shape[0])):
                    for col in range(int(layer.conv_weights.shape[1])):
                        self.m[i, row, col] = 0.0
                        self.v[i, row, col] = 0.0

    def update(self, layer, dW, db, index, layer_type):
        self.t += 1
        rows = int(dW.shape[0])
        cols = int(dW.shape[1])
        self.m[index][:rows, :cols] = (
            self.beta1 * self.m[index][:rows, :cols] + (1 - self.beta1) * dW
        )
        self.v[index][:rows, :cols] = self.beta2 * self.v[index][:rows, :cols] + (
            1 - self.beta2
        ) * np.square(dW)
        m_hat = self.m[index][:rows, :cols] / (1 - self.beta1**self.t)
        v_hat = self.v[index][:rows, :cols] / (1 - self.beta2**self.t)
        if layer_type == "dense":
            layer.dense_weights[:rows, :cols] -= self.learning_rate * (
                m_hat / (np.sqrt(v_hat) + self.epsilon)
                + self.reg_lambda * layer.dense_weights[:rows, :cols]
            )
            layer.dense_biases -= self.learning_rate * db
        elif layer_type == "conv":
            layer.conv_weights[:rows, :cols] -= self.learning_rate * (
                m_hat / (np.sqrt(v_hat) + self.epsilon)
                + self.reg_lambda * layer.conv_weights[:rows, :cols]
            )
            layer.conv_biases -= self.learning_rate * db

    def update_layers(self, layers, dWs, dbs):
        # Build typed lists for dense layers
        dense_indices = List.empty_list(types.int64)
        dense_weights = List()
        dense_biases = List()
        dense_dWs = List()
        dense_dbs = List()
        # Build typed lists for conv layers
        conv_indices = List.empty_list(types.int64)
        conv_weights = List()
        conv_biases = List()
        conv_dWs = List()
        conv_dbs = List()

        # for i in range(len(layers)):
        #     if layers[i].layer_type == 'dense':
        #         dense_indices.append(i)
        #         dense_weights.append(layers[i].dense_weights)
        #         dense_biases.append(layers[i].dense_biases)
        #         dense_dWs.append(dWs[i])
        #         dense_dbs.append(dbs[i])
        #     else:
        #         conv_indices.append(i)
        #         conv_weights.append(layers[i].conv_weights)
        #         conv_biases.append(layers[i].conv_biases)
        #         conv_dWs.append(dWs[i])
        #         conv_dbs.append(dbs[i])
        for i, layer in enumerate(layers):
            if layer.layer_type == "dense":
                dense_indices.append(i)
                dense_weights.append(layer.dense_weights)
                dense_biases.append(layer.dense_biases)
                dense_dWs.append(dWs[i])
                dense_dbs.append(dbs[i])
            else:
                conv_indices.append(i)
                conv_weights.append(layer.conv_weights)
                conv_biases.append(layer.conv_biases)
                conv_dWs.append(dWs[i])
                conv_dbs.append(dbs[i])

        # Increment timestep by total layers
        self.t += len(layers)

        # Call separate helper functions for dense and conv layers
        dense_adam_update_layers(
            self.m,
            self.v,
            self.t,
            dense_indices,
            dense_weights,
            dense_biases,
            dense_dWs,
            dense_dbs,
            self.learning_rate,
            self.beta1,
            self.beta2,
            self.epsilon,
            self.reg_lambda,
        )
        conv_adam_update_layers(
            self.m,
            self.v,
            self.t,
            conv_indices,
            conv_weights,
            conv_biases,
            conv_dWs,
            conv_dbs,
            self.learning_rate,
            self.beta1,
            self.beta2,
            self.epsilon,
            self.reg_lambda,
        )


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def dense_adam_update_layers(
    m,
    v,
    t,
    indices,
    weights,
    biases,
    dWs,
    dbs,
    learning_rate,
    beta1,
    beta2,
    epsilon,
    reg_lambda,
):
    n = len(indices)
    for j in prange(n):
        i = indices[j]  # original index into m and v
        dW = dWs[j]
        db = dbs[j]
        rows = int(dW.shape[0])
        cols = int(dW.shape[1])
        # Update moment estimates for layer i
        for r in range(rows):
            for c in range(cols):
                m[i, r, c] = beta1 * m[i, r, c] + (1 - beta1) * dW[r, c]
                v[i, r, c] = beta2 * v[i, r, c] + (1 - beta2) * (dW[r, c] * dW[r, c])
        # Compute bias-corrected estimates and update weights
        for r in range(rows):
            for c in range(cols):
                m_hat = m[i, r, c] / (1 - beta1**t)
                v_hat = v[i, r, c] / (1 - beta2**t)
                weights[j][r, c] = weights[j][r, c] - learning_rate * (
                    m_hat / (np.sqrt(v_hat) + epsilon) + reg_lambda * weights[j][r, c]
                )
        # Update biases elementwise
        for k in range(db.shape[0]):
            biases[j][k] = biases[j][k] - learning_rate * db[k]


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def conv_adam_update_layers(
    m,
    v,
    t,
    indices,
    weights,
    biases,
    dWs,
    dbs,
    learning_rate,
    beta1,
    beta2,
    epsilon,
    reg_lambda,
):
    n = len(indices)
    for j in prange(n):
        i = indices[j]  # original index into m and v
        dW = dWs[j]
        db = dbs[j]
        rows = int(dW.shape[0])
        cols = int(dW.shape[1])
        # Update moment estimates for layer i
        for r in range(rows):
            for c in range(cols):
                m[i, r, c] = beta1 * m[i, r, c] + (1 - beta1) * dW[r, c]
                v[i, r, c] = beta2 * v[i, r, c] + (1 - beta2) * (dW[r, c] * dW[r, c])
        # Compute bias-corrected estimates and update weights
        for r in range(rows):
            for c in range(cols):
                m_hat = m[i, r, c] / (1 - beta1**t)
                v_hat = v[i, r, c] / (1 - beta2**t)
                weights[j][r, c] = weights[j][r, c] - learning_rate * (
                    m_hat / (np.sqrt(v_hat) + epsilon) + reg_lambda * weights[j][r, c]
                )
        # Update biases elementwise
        for k in range(db.shape[0]):
            biases[j][k] = biases[j][k] - learning_rate * db[k]


spec_sgd = [
    ("learning_rate", float64),
    ("momentum", float64),
    ("reg_lambda", float64),
    ("velocity", float64[:, :, ::1]),
]


@jitclass(spec_sgd)
class JITSGDOptimizer:
    """
    Stochastic Gradient Descent (SGD) optimizer class for training neural networks.
    Formula: w = w - learning_rate * dW, b = b - learning_rate * db
    Args:
        learning_rate (float, optional): The learning rate for the optimizer. Defaults to 0.001.
        momentum (float, optional): The momentum factor. Defaults to 0.0.
        reg_lambda (float, optional): The regularization parameter. Defaults to 0.0.
    """

    def __init__(self, learning_rate=0.001, momentum=0.0, reg_lambda=0.0):
        self.learning_rate = learning_rate  # Learning rate
        self.momentum = momentum  # Momentum factor
        self.reg_lambda = reg_lambda  # Regularization parameter
        self.velocity = np.zeros((1, 1, 1))  # Velocity for momentum

    def initialize(self, layers):
        """
        Initializes the velocity for each layer's weights.
        Args: layers (list): List of layers in the neural network.
        Returns: None
        """
        num_layers = len(layers)
        max_rows = 0
        max_cols = 0
        for layer in layers:
            if layer.layer_type == "dense":
                max_rows = max(max_rows, layer.dense_weights.shape[0])
                max_cols = max(max_cols, layer.dense_weights.shape[1])
            elif layer.layer_type == "conv":
                max_rows = max(max_rows, layer.conv_weights.shape[0])
                max_cols = max(max_cols, layer.conv_weights.shape[1])

        self.velocity = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize velocity as a NumPy array

        for i in range(num_layers):
            layer = layers[i]
            if layer.layer_type == "dense":
                for row in range(layer.dense_weights.shape[0]):
                    for col in range(layer.dense_weights.shape[1]):
                        self.velocity[i, row, col] = 0.0
            elif layer.layer_type == "conv":
                for row in range(layer.conv_weights.shape[0]):
                    for col in range(layer.conv_weights.shape[1]):
                        self.velocity[i, row, col] = 0.0

    def update(self, layer, dW, db, index, layer_type):
        """
        Updates the weights and biases of a layer using the SGD optimization algorithm.
        Args:
            layer (Layer): The layer to update.
            dW (ndarray): The gradient of the weights.
            db (ndarray): The gradient of the biases.
            index (int): The index of the layer.
            layer_type (str): Type of layers ('dense' or 'conv').
        Returns: None
        """
        self.velocity[index][: dW.shape[0], : dW.shape[1]] = (
            self.momentum * self.velocity[index][: dW.shape[0], : dW.shape[1]]
            - self.learning_rate * dW
        )  # Update velocity

        if layer_type == "dense":
            layer.dense_weights[: dW.shape[0], : dW.shape[1]] += (
                self.velocity[index][: dW.shape[0], : dW.shape[1]]
                - self.learning_rate
                * self.reg_lambda
                * layer.dense_weights[: dW.shape[0], : dW.shape[1]]
            )  # Update weights
            layer.dense_biases[: db.shape[0]] -= (
                self.learning_rate * db
            )  # Update biases
        elif layer_type == "conv":
            layer.conv_weights[: dW.shape[0], : dW.shape[1]] += (
                self.velocity[index][: dW.shape[0], : dW.shape[1]]
                - self.learning_rate
                * self.reg_lambda
                * layer.conv_weights[: dW.shape[0], : dW.shape[1]]
            )  # Update weights
            layer.conv_biases[: db.shape[0]] -= self.learning_rate * db  # Update biases

    def update_layers(self, layers, dWs, dbs):
        # Build typed lists for dense layers
        dense_indices = List.empty_list(types.int64)
        dense_weights = List()
        dense_biases = List()
        dense_dWs = List()
        dense_dbs = List()
        # Build typed lists for conv layers
        conv_indices = List.empty_list(types.int64)
        conv_weights = List()
        conv_biases = List()
        conv_dWs = List()
        conv_dbs = List()

        for i in range(len(layers)):
            if layers[i].layer_type == "dense":
                dense_indices.append(i)
                dense_weights.append(layers[i].dense_weights)
                dense_biases.append(layers[i].dense_biases)
                dense_dWs.append(dWs[i])
                dense_dbs.append(dbs[i])
            else:
                conv_indices.append(i)
                conv_weights.append(layers[i].conv_weights)
                conv_biases.append(layers[i].conv_biases)
                conv_dWs.append(dWs[i])
                conv_dbs.append(dbs[i])

        # Call separate helper functions for dense and conv layers
        dense_sgd_update_layers(
            self.velocity,
            dense_indices,
            dense_weights,
            dense_biases,
            dense_dWs,
            dense_dbs,
            self.learning_rate,
            self.momentum,
            self.reg_lambda,
        )
        conv_sgd_update_layers(
            self.velocity,
            conv_indices,
            conv_weights,
            conv_biases,
            conv_dWs,
            conv_dbs,
            self.learning_rate,
            self.momentum,
            self.reg_lambda,
        )


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def dense_sgd_update_layers(
    velocity, indices, weights, biases, dWs, dbs, learning_rate, momentum, reg_lambda
):
    n = len(indices)
    for j in prange(n):
        i = indices[j]  # original index into velocity
        dW = dWs[j]
        db = dbs[j]
        rows = int(dW.shape[0])
        cols = int(dW.shape[1])

        # Update velocity with momentum
        for r in range(rows):
            for c in range(cols):
                velocity[i, r, c] = (
                    momentum * velocity[i, r, c] - learning_rate * dW[r, c]
                )

        # Update weights with velocity and regularization
        for r in range(rows):
            for c in range(cols):
                weights[j][r, c] += (
                    velocity[i, r, c] - learning_rate * reg_lambda * weights[j][r, c]
                )

        # Update biases elementwise
        for k in range(db.shape[0]):
            biases[j][k] -= learning_rate * db[k]


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def conv_sgd_update_layers(
    velocity, indices, weights, biases, dWs, dbs, learning_rate, momentum, reg_lambda
):
    n = len(indices)
    for j in prange(n):
        i = indices[j]  # original index into velocity
        dW = dWs[j]
        db = dbs[j]
        rows = int(dW.shape[0])
        cols = int(dW.shape[1])

        # Update velocity with momentum
        for r in range(rows):
            for c in range(cols):
                velocity[i, r, c] = (
                    momentum * velocity[i, r, c] - learning_rate * dW[r, c]
                )

        # Update weights with velocity and regularization
        for r in range(rows):
            for c in range(cols):
                weights[j][r, c] += (
                    velocity[i, r, c] - learning_rate * reg_lambda * weights[j][r, c]
                )

        # Update biases elementwise
        for k in range(db.shape[0]):
            biases[j][k] -= learning_rate * db[k]


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
        self.learning_rate = learning_rate  # Learning rate
        self.rho = rho  # Decay rate
        self.epsilon = epsilon  # Small value to prevent division by zero
        self.reg_lambda = reg_lambda  # Regularization parameter

        self.E_g2 = np.zeros((1, 1, 1))  # Running average of squared gradients
        self.E_delta_x2 = np.zeros(
            (1, 1, 1)
        )  # Running average of squared parameter updates

    def initialize(self, layers):
        """
        Initializes the running averages for each layer's weights.
        Args: layers (list): List of layers in the neural network.
        Returns: None
        """
        num_layers = len(layers)
        max_rows = 0
        max_cols = 0
        for layer in layers:
            if layer.layer_type == "dense":
                max_rows = max(max_rows, layer.dense_weights.shape[0])
                max_cols = max(max_cols, layer.dense_weights.shape[1])
            elif layer.layer_type == "conv":
                max_rows = max(max_rows, layer.conv_weights.shape[0])
                max_cols = max(max_cols, layer.conv_weights.shape[1])

        self.E_g2 = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize running average of squared gradients
        self.E_delta_x2 = np.zeros(
            (num_layers, max_rows, max_cols)
        )  # Initialize running average of squared parameter updates

        for i in range(num_layers):
            layer = layers[i]
            if layer.layer_type == "dense":
                for row in range(layer.dense_weights.shape[0]):
                    for col in range(layer.dense_weights.shape[1]):
                        self.E_g2[i, row, col] = 0.0
                        self.E_delta_x2[i, row, col] = 0.0
            elif layer.layer_type == "conv":
                for row in range(layer.conv_weights.shape[0]):
                    for col in range(layer.conv_weights.shape[1]):
                        self.E_g2[i, row, col] = 0.0
                        self.E_delta_x2[i, row, col] = 0.0

    def update(self, layer, dW, db, index, layer_type):
        """
        Updates the weights and biases of a layer using the Adadelta optimization algorithm.
        Args:
            layer (Layer): The layer to update.
            dW (ndarray): The gradient of the weights.
            db (ndarray): The gradient of the biases.
            index (int): The index of the layer.
        Returns: None
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

        if layer_type == "dense":
            layer.dense_weights[: dW.shape[0], : dW.shape[1]] += (
                delta_x
                - self.learning_rate
                * self.reg_lambda
                * layer.dense_weights[: dW.shape[0], : dW.shape[1]]
            )  # Update weights
            layer.dense_biases[: db.shape[0]] -= (
                self.learning_rate * db
            )  # Update biases
        elif layer_type == "conv":
            layer.conv_weights[: dW.shape[0], : dW.shape[1]] += (
                delta_x
                - self.learning_rate
                * self.reg_lambda
                * layer.conv_weights[: dW.shape[0], : dW.shape[1]]
            )  # Update weights
            layer.conv_biases[: db.shape[0]] -= self.learning_rate * db  # Update biases

    def update_layers(self, layers, dWs, dbs):
        # Build typed lists for dense layers
        dense_indices = List.empty_list(types.int64)
        dense_weights = List()
        dense_biases = List()
        dense_dWs = List()
        dense_dbs = List()
        # Build typed lists for conv layers
        conv_indices = List.empty_list(types.int64)
        conv_weights = List()
        conv_biases = List()
        conv_dWs = List()
        conv_dbs = List()

        for i in range(len(layers)):
            if layers[i].layer_type == "dense":
                dense_indices.append(i)
                dense_weights.append(layers[i].dense_weights)
                dense_biases.append(layers[i].dense_biases)
                dense_dWs.append(dWs[i])
                dense_dbs.append(dbs[i])
            else:
                conv_indices.append(i)
                conv_weights.append(layers[i].conv_weights)
                conv_biases.append(layers[i].conv_biases)
                conv_dWs.append(dWs[i])
                conv_dbs.append(dbs[i])

        # Call separate helper functions for dense and conv layers
        dense_adadelta_update_layers(
            self.E_g2,
            self.E_delta_x2,
            dense_indices,
            dense_weights,
            dense_biases,
            dense_dWs,
            dense_dbs,
            self.learning_rate,
            self.rho,
            self.epsilon,
            self.reg_lambda,
        )
        conv_adadelta_update_layers(
            self.E_g2,
            self.E_delta_x2,
            conv_indices,
            conv_weights,
            conv_biases,
            conv_dWs,
            conv_dbs,
            self.learning_rate,
            self.rho,
            self.epsilon,
            self.reg_lambda,
        )


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def dense_adadelta_update_layers(
    E_g2,
    E_delta_x2,
    indices,
    weights,
    biases,
    dWs,
    dbs,
    learning_rate,
    rho,
    epsilon,
    reg_lambda,
):
    n = len(indices)
    for j in prange(n):
        i = indices[j]  # original index into E_g2 and E_delta_x2
        dW = dWs[j]
        db = dbs[j]
        rows = int(dW.shape[0])
        cols = int(dW.shape[1])

        # Update running average of squared gradients
        for r in range(rows):
            for c in range(cols):
                E_g2[i, r, c] = rho * E_g2[i, r, c] + (1 - rho) * (dW[r, c] ** 2)

        # Compute parameter updates and update running average of squared updates
        delta_x = np.zeros((rows, cols))
        for r in range(rows):
            for c in range(cols):
                # Compute parameter update
                delta_x[r, c] = (
                    -(
                        np.sqrt(E_delta_x2[i, r, c] + epsilon)
                        / np.sqrt(E_g2[i, r, c] + epsilon)
                    )
                    * dW[r, c]
                )

                # Update running average of squared parameter updates
                E_delta_x2[i, r, c] = rho * E_delta_x2[i, r, c] + (1 - rho) * (
                    delta_x[r, c] ** 2
                )

                # Apply update to weights
                weights[j][r, c] += (
                    delta_x[r, c] - learning_rate * reg_lambda * weights[j][r, c]
                )

        # Update biases elementwise
        for k in range(db.shape[0]):
            biases[j][k] -= learning_rate * db[k]


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def conv_adadelta_update_layers(
    E_g2,
    E_delta_x2,
    indices,
    weights,
    biases,
    dWs,
    dbs,
    learning_rate,
    rho,
    epsilon,
    reg_lambda,
):
    n = len(indices)
    for j in prange(n):
        i = indices[j]  # original index into E_g2 and E_delta_x2
        dW = dWs[j]
        db = dbs[j]
        rows = int(dW.shape[0])
        cols = int(dW.shape[1])

        # Update running average of squared gradients
        for r in range(rows):
            for c in range(cols):
                E_g2[i, r, c] = rho * E_g2[i, r, c] + (1 - rho) * (dW[r, c] ** 2)

        # Compute parameter updates and update running average of squared updates
        delta_x = np.zeros((rows, cols))
        for r in range(rows):
            for c in range(cols):
                # Compute parameter update
                delta_x[r, c] = (
                    -(
                        np.sqrt(E_delta_x2[i, r, c] + epsilon)
                        / np.sqrt(E_g2[i, r, c] + epsilon)
                    )
                    * dW[r, c]
                )

                # Update running average of squared parameter updates
                E_delta_x2[i, r, c] = rho * E_delta_x2[i, r, c] + (1 - rho) * (
                    delta_x[r, c] ** 2
                )

                # Apply update to weights
                weights[j][r, c] += (
                    delta_x[r, c] - learning_rate * reg_lambda * weights[j][r, c]
                )

        # Update biases elementwise
        for k in range(db.shape[0]):
            biases[j][k] -= learning_rate * db[k]
