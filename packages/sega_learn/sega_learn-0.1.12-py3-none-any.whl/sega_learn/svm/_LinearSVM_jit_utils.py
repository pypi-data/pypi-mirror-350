import numpy as np
from numba import njit, prange


@njit(fastmath=True)
def _linearSVC_minibatches(X, y, w, b, C, beta, learning_rate, batch_size):
    """Process all mini-batches for LinearSVC using gradient descent with momentum.

    Args:
        X (ndarray): Training data of shape (n_samples, n_features).
        y (ndarray): Target labels of shape (n_samples,).
        w (ndarray): Weight vector of shape (n_features,).
        b (float): Bias term.
        C (float): Regularization parameter.
        beta (float): Momentum factor.
        learning_rate (float): Learning rate for gradient descent.
        batch_size (int): Size of each mini-batch.

    Returns:
        w (ndarray): Updated weight vector.
        b (float): Updated bias term.
        dw (ndarray): Gradient of the weight vector.
        db (float): Gradient of the bias term.
    """
    n_samples, n_features = X.shape
    momentum_w = np.zeros(n_features)
    momentum_b = 0.0

    # Calculate the number of batches
    num_batches = (n_samples + batch_size - 1) // batch_size  # Ceiling division

    for batch_idx in prange(num_batches):
        start = batch_idx * batch_size
        end = min(start + batch_size, n_samples)
        X_batch = X[start:end]
        y_batch = y[start:end]

        # Compute the margin
        margin = y_batch * (np.dot(X_batch, w) + b)

        # Compute the hinge loss gradient
        violated_indices = margin < 1
        dw = C * w  # L2 regularization gradient
        db = 0.0

        if np.any(violated_indices):
            X_violated = X_batch[violated_indices]
            y_violated = y_batch[violated_indices]
            dw -= np.sum(X_violated * y_violated[:, np.newaxis], axis=0) / batch_size
            db -= np.sum(y_violated) / batch_size

        # Apply momentum
        momentum_w = beta * momentum_w + (1 - beta) * dw
        momentum_b = beta * momentum_b + (1 - beta) * db

        # Update weights and bias
        w -= learning_rate * momentum_w
        b -= learning_rate * momentum_b

    return w, b, dw, db


@njit(fastmath=True)
def _linearSVR_minibatches(X, y, w, b, C, beta, learning_rate, batch_size, epsilon):
    """Process all mini-batches for LinearSVR using gradient descent with momentum.

    Args:
        X (ndarray): Training data of shape (n_samples, n_features).
        y (ndarray): Target values of shape (n_samples,).
        w (ndarray): Weight vector of shape (n_features,).
        b (float): Bias term.
        C (float): Regularization parameter.
        beta (float): Momentum factor.
        learning_rate (float): Learning rate for gradient descent.
        batch_size (int): Size of each mini-batch.
        epsilon (float): Epsilon-insensitive loss parameter.

    Returns:
        w (ndarray): Updated weight vector.
        b (float): Updated bias term.
        dw (ndarray): Gradient of the weight vector.
        db (float): Gradient of the bias term.
    """
    n_samples, n_features = X.shape
    momentum_w = np.zeros(n_features)
    momentum_b = 0.0

    # Calculate the number of batches
    num_batches = (n_samples + batch_size - 1) // batch_size  # Ceiling division

    for batch_idx in prange(num_batches):
        start = batch_idx * batch_size
        end = start + batch_size
        X_batch = X[start:end]
        y_batch = y[start:end]

        # Compute predictions
        predictions = np.dot(X_batch, w) + b

        # Compute errors
        errors = y_batch - predictions

        # Initialize gradients
        dw = C * w  # L2 regularization gradient
        db = 0.0

        # Positive epsilon-insensitive loss
        pos_idx = errors > epsilon
        if np.any(pos_idx):
            dw -= np.sum(X_batch[pos_idx], axis=0) / batch_size
            db -= np.sum(np.ones(np.sum(pos_idx))) / batch_size

        # Negative epsilon-insensitive loss
        neg_idx = errors < -epsilon
        if np.any(neg_idx):
            dw += np.sum(X_batch[neg_idx], axis=0) / batch_size
            db += np.sum(np.ones(np.sum(neg_idx))) / batch_size

        # Apply momentum
        momentum_w = beta * momentum_w + (1 - beta) * dw
        momentum_b = beta * momentum_b + (1 - beta) * db

        # Update weights and bias
        w -= learning_rate * momentum_w
        b -= learning_rate * momentum_b

    return w, b, dw, db
