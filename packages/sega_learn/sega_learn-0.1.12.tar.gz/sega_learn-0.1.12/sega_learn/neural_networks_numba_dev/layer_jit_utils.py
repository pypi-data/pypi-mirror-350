import numpy as np
from numba import njit

from .numba_utils import *

CACHE = False


@njit(fastmath=True, nogil=True, cache=CACHE)
def forward_dense(X, weights, biases, activation_func):
    """Forward pass for dense layer."""
    Z = np.dot(X, weights) + biases
    input_cache = X
    output_cache = activate(Z, activation_func)
    return output_cache, input_cache


@njit(fastmath=True, nogil=True, cache=CACHE)
def backward_dense(dA, reg_lambda, weights, input_cache, output_cache, activation_func):
    """Backward pass for dense layer."""
    m = input_cache.shape[0]
    dZ = dA * activation_derivative(output_cache, activation_func)
    dW = np.dot(input_cache.T, dZ) / m + reg_lambda * weights
    db = sum_axis0(dZ) / m
    dA_prev = np.dot(dZ, weights.T)

    return dA_prev, dW, db


@njit(fastmath=True, nogil=True, cache=CACHE)
def activate(Z, activation=None):
    """Apply activation function."""
    if activation == "relu":
        return relu(Z)
    elif activation == "leaky_relu":
        return leaky_relu(Z)
    elif activation == "tanh":
        return tanh(Z)
    elif activation == "sigmoid":
        return sigmoid(Z)
    elif activation == "softmax":
        return softmax(Z)
    else:
        raise ValueError(f"Unsupported activation: {activation}")


@njit(fastmath=True, nogil=True, cache=CACHE)
def activation_derivative(Z, activation=None):
    """Apply activation derivative."""
    if activation == "relu":
        return relu_derivative(Z)
    elif activation == "leaky_relu":
        return leaky_relu_derivative(Z)
    elif activation == "tanh":
        return tanh_derivative(Z)
    elif activation == "sigmoid":
        return sigmoid_derivative(Z)
    elif activation == "softmax":
        return np.ones_like(Z)  # Identity for compatibility
    else:
        raise ValueError(f"Unsupported activation: {activation}")
