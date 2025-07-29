import numpy as np
from numba import njit, prange
from numba.typed import List

CACHE = False


# -------------------------------------------------------------------------------------------------
# Loss functions and accuracy
# -------------------------------------------------------------------------------------------------
@njit(fastmath=True, nogil=True, cache=CACHE)
def calculate_loss_from_outputs_binary(outputs, y, weights, reg_lambda):
    """Calculate binary classification loss with L2 regularization."""
    # Apply loss function
    loss = calculate_bce_with_logits_loss(outputs, y)

    # If weights is a list, compute L2 regularization for each weight matrix
    # If not a list, only one value, so no regularization needed
    if isinstance(weights, list):
        # Add L2 regularization
        l2_reg = reg_lambda * _compute_l2_reg(weights)
        # Add L2 regularization to loss
        loss += l2_reg

    return float(loss)


@njit(fastmath=True, nogil=True, cache=CACHE)
def calculate_loss_from_outputs_multi(outputs, y, weights, reg_lambda):
    """Calculate multi-class classification loss with L2 regularization."""
    # Apply loss function
    loss = calculate_cross_entropy_loss(outputs, y)

    # If weights is a list, compute L2 regularization for each weight matrix
    if isinstance(weights, list):
        # Add L2 regularization
        l2_reg = reg_lambda * _compute_l2_reg(weights)
        # Add L2 regularization to loss
        loss += l2_reg

    return float(loss)


@njit(fastmath=True, nogil=True, cache=CACHE)
def calculate_cross_entropy_loss(logits, targets):
    """Calculate cross-entropy loss for multi-class classification."""
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


@njit(fastmath=True, nogil=True, cache=CACHE)
def calculate_bce_with_logits_loss(logits, targets):
    """Calculate binary cross-entropy loss with logits."""
    probs = 1 / (1 + np.exp(-logits))  # Apply sigmoid to logits to get probabilities
    loss = -np.mean(
        targets * np.log(probs + 1e-15) + (1 - targets) * np.log(1 - probs + 1e-15)
    )  # Binary cross-entropy loss
    return loss


@njit(fastmath=True, nogil=True, parallel=True, cache=CACHE)
def _compute_l2_reg(weights):
    """Compute L2 regularization for a list of weight matrices."""
    total = 0.0
    for i in prange(len(weights)):
        total += np.sum(weights[i] ** 2)
    return total


@njit(fastmath=True, nogil=True, cache=CACHE)
def evaluate_batch(y_hat, y_true, is_binary):
    """Evaluate accuracy for a batch of predictions."""
    if is_binary:
        predicted = (y_hat > 0.5).astype(np.int32).flatten()
        accuracy = np.mean(predicted == y_true.flatten())
    else:
        predicted = np.argmax(y_hat, axis=1).astype(np.int32)
        accuracy = np.mean(predicted == y_true)
    return accuracy


# JIT Regression Loss Calculation Helpers
@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def calculate_mse_loss(y_pred, y_true):
    """Helper function to calculate the mean squared error loss. Handles 1D and 2D inputs."""
    n_samples = y_true.shape[0]
    loss = 0.0

    # Check dimensions and handle accordingly
    if y_true.ndim == 1:  # Single output case
        for i in prange(n_samples):
            loss += (y_true[i] - y_pred[i]) ** 2
    elif y_true.ndim == 2:  # Multi-output case
        n_outputs = y_true.shape[1]
        if n_outputs == 0:
            return 0.0  # Handle empty second dimension case
        for i in prange(n_samples):
            diff_sq_sum = 0.0
            for j in range(n_outputs):  # Iterate over outputs
                diff_sq_sum += (y_true[i, j] - y_pred[i, j]) ** 2
            loss += diff_sq_sum / n_outputs  # Average over outputs for the sample
    else:
        # Numba doesn't support raising exceptions easily here in nopython mode.
        # Rely on input validation before calling.
        return np.nan  # Or some other indicator of error

    return loss / n_samples


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def calculate_mae_loss(y_pred, y_true):
    """Helper function to calculate the mean absolute error loss. Handles 1D and 2D inputs."""
    n_samples = y_true.shape[0]
    loss = 0.0

    if y_true.ndim == 1:
        for i in prange(n_samples):
            loss += np.abs(y_true[i] - y_pred[i])
    elif y_true.ndim == 2:
        n_outputs = y_true.shape[1]
        if n_outputs == 0:
            return 0.0
        for i in prange(n_samples):
            abs_diff_sum = 0.0
            for j in range(n_outputs):
                abs_diff_sum += np.abs(y_true[i, j] - y_pred[i, j])
            loss += abs_diff_sum / n_outputs
    else:
        return np.nan

    return loss / n_samples


@njit(parallel=True, fastmath=True, nogil=True, cache=CACHE)
def calculate_huber_loss(y_pred, y_true, delta=1.0):
    """Helper function to calculate the Huber loss. Handles 1D and 2D inputs."""
    n_samples = y_true.shape[0]
    loss = 0.0

    if y_true.ndim == 1:
        for i in prange(n_samples):
            error = y_true[i] - y_pred[i]
            abs_error = np.abs(error)
            if abs_error <= delta:
                loss += 0.5 * error**2
            else:
                loss += delta * (abs_error - 0.5 * delta)
    elif y_true.ndim == 2:
        n_outputs = y_true.shape[1]
        if n_outputs == 0:
            return 0.0
        for i in prange(n_samples):
            sample_loss = 0.0
            for j in range(n_outputs):
                error = y_true[i, j] - y_pred[i, j]
                abs_error = np.abs(error)
                if abs_error <= delta:
                    sample_loss += 0.5 * error**2
                else:
                    sample_loss += delta * (abs_error - 0.5 * delta)
            loss += sample_loss / n_outputs  # Average over outputs
    else:
        return np.nan

    return loss / n_samples


# -------------------------------------------------------------------------------------------------
# Activation functions
# -------------------------------------------------------------------------------------------------
@njit(fastmath=True, cache=CACHE)
def relu(z):
    """Apply ReLU activation function."""
    return np.maximum(0, z)


@njit(fastmath=True, cache=CACHE)
def relu_derivative(z):
    """Compute the derivative of the ReLU activation function."""
    return (z > 0).astype(np.float64)  # Ensure return type is float64


@njit(fastmath=True, cache=CACHE)
def leaky_relu(z, alpha=0.01):
    """Apply Leaky ReLU activation function."""
    return np.where(z > 0, z, alpha * z)


@njit(fastmath=True, cache=CACHE)
def leaky_relu_derivative(z, alpha=0.01):
    """Compute the derivative of the Leaky ReLU activation function."""
    return np.where(z > 0, 1, alpha).astype(np.float64)  # Ensure return type is float64


@njit(fastmath=True, cache=CACHE)
def tanh(z):
    """Apply tanh activation function."""
    return np.tanh(z)


@njit(fastmath=True, cache=CACHE)
def tanh_derivative(z):
    """Compute the derivative of the tanh activation function."""
    return 1 - np.tanh(z) ** 2


@njit(fastmath=True, cache=CACHE)
def sigmoid(z):
    """Apply sigmoid activation function."""
    return 1 / (1 + np.exp(-z))


@njit(fastmath=True, cache=CACHE)
def sigmoid_derivative(z):
    """Compute the derivative of the sigmoid activation function."""
    sig = sigmoid(z)
    return sig * (1 - sig)


@njit(parallel=True, fastmath=True, cache=CACHE)
def softmax(z):
    """Apply softmax activation function."""
    out = np.empty_like(z)
    for i in prange(z.shape[0]):
        row = z[i]
        max_val = np.max(row)
        shifted = row - max_val
        exp_vals = np.exp(shifted)
        sum_exp = np.sum(exp_vals)
        out[i] = exp_vals / sum_exp
    return out


# -------------------------------------------------------------------------------------------------
# Other utility functions
# -------------------------------------------------------------------------------------------------
@njit(fastmath=True, cache=CACHE)
def sum_reduce(arr):
    """Sum elements along the last axis and reduce the array."""
    sum_vals = np.empty((arr.shape[0], 1), dtype=arr.dtype)
    for i in range(arr.shape[0]):
        sum_vals[i, 0] = np.sum(arr[i])
    return sum_vals


@njit(fastmath=True, nogil=True, cache=CACHE)
def sum_axis0(arr):
    """Sum elements along axis 0."""
    sum_vals = np.zeros((1, arr.shape[1]), dtype=arr.dtype)
    for j in range(arr.shape[1]):
        for i in range(arr.shape[0]):
            sum_vals[0, j] += arr[i, j]
    return sum_vals


# -------------------------------------------------------------------------------------------------
# Neural Network functions
# -------------------------------------------------------------------------------------------------
@njit(fastmath=True, nogil=True, cache=CACHE)
def apply_dropout_jit(X, dropout_rate):
    """Apply dropout to activation values."""
    # Generate the entire mask at once - more vectorized approach
    mask = (np.random.random(X.shape) < (1 - dropout_rate)).astype(np.float64)
    return (X * mask) / (1 - dropout_rate)


@njit(fastmath=True, nogil=True, cache=CACHE)
def compute_l2_reg(weights):
    """Compute L2 regularization for weights."""
    total = 0.0
    for i in prange(len(weights)):
        total += np.sum(weights[i] ** 2)
    return total


@njit(fastmath=True, nogil=True, cache=CACHE)
def one_hot_encode(y, num_classes):
    """One-hot encode a vector of class labels."""
    m = y.shape[0]
    y_ohe = np.zeros((m, num_classes), dtype=np.float64)
    for i in range(m):
        y_ohe[i, y[i]] = 1.0
    return y_ohe


@njit(fastmath=True, nogil=True, cache=CACHE)
def process_batches_binary(
    X_shuffled,
    y_shuffled,
    batch_size,
    layers,
    dropout_rate,
    dropout_layer_indices,
    reg_lambda,
    dWs_acc,
    dbs_acc,
):
    """Process batches for binary classification."""
    num_samples = X_shuffled.shape[0]
    num_batches = (num_samples + batch_size - 1) // batch_size  # Ceiling division
    running_loss = 0.0
    running_accuracy = 0.0

    for i in prange(num_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, num_samples)

        X_batch = X_shuffled[start_idx:end_idx]
        y_batch = y_shuffled[start_idx:end_idx]

        # Forward pass
        layer_outputs = [X_batch]
        A = X_batch.astype(np.float64)
        for i, layer in enumerate(layers):
            A = layer.forward(A)
            if dropout_rate > 0 and i in dropout_layer_indices:
                A = apply_dropout_jit(A, dropout_rate)
            layer_outputs.append(A)

        # Backward pass
        _m = y_batch.shape[0]
        outputs = layer_outputs[-1]
        y_batch = y_batch.reshape(-1, 1).astype(np.float64)
        dA = -(y_batch / (outputs + 1e-15) - (1 - y_batch) / (1 - outputs + 1e-15))

        for j in range(len(layers) - 1, -1, -1):
            dA = layers[j].backward(dA, reg_lambda)

        # Calculate loss and accuracy for binary classification
        running_loss += calculate_loss_from_outputs_binary(
            layer_outputs[-1], y_batch, reg_lambda, [layer.weights for layer in layers]
        )
        running_accuracy += evaluate_batch(layer_outputs[-1], y_batch, True)

        # Accumulate gradients
        for j in range(len(layers)):
            dWs_acc[j] += layers[j].weight_gradients
            dbs_acc[j] += layers[j].bias_gradients

    # Average the accumulated gradients, loss, and accuracy
    for j in range(len(dWs_acc)):
        dWs_acc[j] /= num_batches
        dbs_acc[j] /= num_batches
    running_loss /= num_batches
    running_accuracy /= num_batches

    return dWs_acc, dbs_acc, running_loss, running_accuracy


@njit(fastmath=True, nogil=True, cache=CACHE)
def process_batches_multi(
    X_shuffled,
    y_shuffled,
    batch_size,
    layers,
    dropout_rate,
    dropout_layer_indices,
    reg_lambda,
    dWs_acc,
    dbs_acc,
):
    """Process batches for multi-class classification."""
    num_samples = X_shuffled.shape[0]
    num_batches = (num_samples + batch_size - 1) // batch_size  # Ceiling division
    running_loss = 0.0
    running_accuracy = 0.0

    for i in prange(num_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, num_samples)

        X_batch = X_shuffled[start_idx:end_idx]
        y_batch = y_shuffled[start_idx:end_idx]

        # Forward pass
        layer_outputs = [X_batch]
        A = X_batch.astype(np.float64)
        for i, layer in enumerate(layers):
            A = layer.forward(A)
            if dropout_rate > 0 and i in dropout_layer_indices:
                A = apply_dropout_jit(A, dropout_rate)
            layer_outputs.append(A)

        # Backward pass
        m = y_batch.shape[0]
        outputs = layer_outputs[-1]
        dA = outputs.copy()
        for k in range(m):
            dA[k, y_batch[k]] -= 1

        for j in range(len(layers) - 1, -1, -1):
            dA = layers[j].backward(dA, reg_lambda)

        # One-hot encode for multi-class loss
        y_batch_ohe = one_hot_encode(y_batch, layers[-1].weights.shape[1])
        running_loss += calculate_loss_from_outputs_multi(
            layer_outputs[-1],
            y_batch_ohe,
            reg_lambda,
            [layer.weights for layer in layers],
        )
        running_accuracy += evaluate_batch(layer_outputs[-1], y_batch, False)

        # Accumulate gradients
        for j in range(len(layers)):
            dWs_acc[j] += layers[j].weight_gradients
            dbs_acc[j] += layers[j].bias_gradients

    # Average the accumulated gradients, loss, and accuracy
    for j in range(len(dWs_acc)):
        dWs_acc[j] /= num_batches
        dbs_acc[j] /= num_batches
    running_loss /= num_batches
    running_accuracy /= num_batches

    return dWs_acc, dbs_acc, running_loss, running_accuracy


@njit(fastmath=True, nogil=True, cache=CACHE)
def process_batches_regression_jit(
    X_shuffled,
    y_shuffled,
    batch_size,
    layers,
    dropout_rate,
    dropout_layer_indices,
    reg_lambda,
    dWs_acc,
    dbs_acc,
    loss_calculator_func,  # Reference to the @njit loss function
    # Note: If HuberLoss is used, delta must be handled within calculate_huber_loss (default)
    # or this function needs modification to accept delta.
):
    """Process batches for regression tasks using Numba."""
    num_samples = X_shuffled.shape[0]
    num_batches = (num_samples + batch_size - 1) // batch_size
    running_loss = 0.0
    running_metric = 0.0  # Will store the primary metric (e.g., MSE)

    for i in prange(num_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, num_samples)

        X_batch = X_shuffled[start_idx:end_idx]
        y_batch = y_shuffled[start_idx:end_idx]

        # Forward pass
        layer_outputs = [X_batch.astype(np.float64)]
        A = layer_outputs[0]
        for k, layer in enumerate(layers):
            A = layer.forward(A)
            if dropout_rate > 0 and k in dropout_layer_indices:
                A = apply_dropout_jit(A, dropout_rate)
            layer_outputs.append(A)

        # Backward pass
        outputs = layer_outputs[-1]
        m = y_batch.shape[0]
        # Assuming MSE derivative for now for dA calculation
        # TODO: Make dA calculation dependent on the actual loss function if needed
        dA = (outputs - y_batch) / m
        for j in range(len(layers) - 1, -1, -1):
            dA = layers[j].backward(dA.astype(np.float64), reg_lambda)

        # Calculate loss and primary metric using the passed function
        # Directly call the passed njit function
        batch_loss = loss_calculator_func(outputs, y_batch)
        # Assuming the primary metric is the same as the loss for now
        batch_metric = batch_loss

        # Add L2 regularization to batch loss
        # Need to be careful how weights are accessed if layers list is complex
        # Assuming layers list contains objects with a .weights attribute
        weights_list = List()  # Use numba typed list
        for layer in layers:
            if hasattr(layer, "weights"):  # Check if layer has weights
                weights_list.append(layer.weights)
        if len(weights_list) > 0:
            l2_reg = reg_lambda * compute_l2_reg(weights_list)
            batch_loss += l2_reg

        running_loss += batch_loss
        running_metric += batch_metric

        # Accumulate gradients (remains the same)
        for j, layer in enumerate(layers):
            if hasattr(layer, "weight_gradients"):
                dWs_acc[j] += layer.weight_gradients
                dbs_acc[j] += layer.bias_gradients

    # Average the accumulated gradients, loss, and metric (remains the same)
    for j in range(len(dWs_acc)):
        dWs_acc[j] /= num_batches
        dbs_acc[j] /= num_batches
    running_loss /= num_batches
    running_metric /= num_batches

    return dWs_acc, dbs_acc, running_loss, running_metric


@njit(fastmath=True, nogil=True, cache=CACHE)
def evaluate_jit(y_hat, y_true, is_binary):
    """Evaluate model performance and return accuracy and predictions."""
    if is_binary:
        predicted = (y_hat > 0.5).astype(np.int32).flatten()
        accuracy = np.mean(predicted == y_true.flatten())
    else:
        predicted = np.argmax(y_hat, axis=1).astype(np.int32)
        accuracy = np.mean(predicted == y_true)
    return accuracy, predicted


@njit(fastmath=True, nogil=True, cache=CACHE)
def evaluate_regression_jit(y_pred, y_true, loss_function):
    """Evaluate model performance for regression tasks using Numba.

    Args:
        y_pred (ndarray): Model predictions.
        y_true (ndarray): True target values.
        loss_function (object): The JIT loss function instance (e.g., JITMeanSquaredErrorLoss).

    Returns:
        tuple: Metric value (e.g., MSE) and the predictions.
    """
    # Calculate the primary metric using the provided loss function
    metric = loss_function.calculate_loss(y_pred, y_true)
    # Return the metric and the raw predictions
    return metric, y_pred
