import numpy as np
from numba import njit, prange

CACHE = False


# -------------------------------------------------------------------------------------------------
# Loss functions and accuracy
# -------------------------------------------------------------------------------------------------
@njit(fastmath=True, nogil=True, cache=CACHE)
def calculate_loss_from_outputs_binary(outputs, y, weights, reg_lambda):
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
    probs = 1 / (1 + np.exp(-logits))  # Apply sigmoid to logits to get probabilities
    loss = -np.mean(
        targets * np.log(probs + 1e-15) + (1 - targets) * np.log(1 - probs + 1e-15)
    )  # Binary cross-entropy loss
    return loss


@njit(fastmath=True, nogil=True, parallel=True, cache=CACHE)
def _compute_l2_reg(weights):
    total = 0.0
    for i in prange(len(weights)):
        total += np.sum(weights[i] ** 2)
    return total


@njit(fastmath=True, nogil=True, cache=CACHE)
def evaluate_batch(y_hat, y_true, is_binary):
    if is_binary:
        predicted = (y_hat > 0.5).astype(np.int32).flatten()
        accuracy = np.mean(predicted == y_true.flatten())
    else:
        predicted = np.argmax(y_hat, axis=1).astype(np.int32)
        accuracy = np.mean(predicted == y_true)
    return accuracy


# -------------------------------------------------------------------------------------------------
# Activation functions
# -------------------------------------------------------------------------------------------------
@njit(fastmath=True, cache=CACHE)
def relu(z):
    return np.maximum(0, z)


@njit(fastmath=True, cache=CACHE)
def relu_derivative(z):
    return (z > 0).astype(np.float64)  # Ensure return type is float64


@njit(fastmath=True, cache=CACHE)
def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)


@njit(fastmath=True, cache=CACHE)
def leaky_relu_derivative(z, alpha=0.01):
    return np.where(z > 0, 1, alpha).astype(np.float64)  # Ensure return type is float64


@njit(fastmath=True, cache=CACHE)
def tanh(z):
    return np.tanh(z)


@njit(fastmath=True, cache=CACHE)
def tanh_derivative(z):
    return 1 - np.tanh(z) ** 2


@njit(fastmath=True, cache=CACHE)
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


@njit(fastmath=True, cache=CACHE)
def sigmoid_derivative(z):
    sig = sigmoid(z)
    return sig * (1 - sig)


@njit(parallel=True, fastmath=True, cache=CACHE)
def softmax(z):
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
    sum_vals = np.empty((arr.shape[0], 1), dtype=arr.dtype)
    for i in range(arr.shape[0]):
        sum_vals[i, 0] = np.sum(arr[i])
    return sum_vals


@njit(fastmath=True, nogil=True, cache=CACHE)
def sum_axis0(arr):
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
    """
    Numba JIT-compiled function to apply dropout.
    Args:
        X (ndarray): Activation values.
        dropout_rate (float): Dropout rate.
    Returns:
        ndarray: Activation values after applying dropout.
    """
    # Generate the entire mask at once - more vectorized approach
    mask = (np.random.random(X.shape) < (1 - dropout_rate)).astype(np.float64)
    return (X * mask) / (1 - dropout_rate)


@njit(fastmath=True, nogil=True, cache=CACHE)
def compute_l2_reg(weights):
    total = 0.0
    for i in prange(len(weights)):
        total += np.sum(weights[i] ** 2)
    return total


@njit(fastmath=True, nogil=True, cache=CACHE)
def one_hot_encode(y, num_classes):
    m = y.shape[0]
    y_ohe = np.zeros((m, num_classes), dtype=np.float64)
    for i in range(m):
        y_ohe[i, y[i]] = 1.0
    return y_ohe


# TODO: @njit not working for this function
# @njit(fastmath=True, nogil=True, cache=CACHE)
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
        y_batch = y_batch.reshape(-1, 1).astype(np.float64)
        dA = -(y_batch / (outputs + 1e-15) - (1 - y_batch) / (1 - outputs + 1e-15))

        for j in range(len(layers) - 1, -1, -1):
            dA = layers[j].backward(dA, reg_lambda)

        # Calculate loss and accuracy for binary classification
        all_weights = [
            layer.dense_weights if layer.layer_type == "dense" else layer.conv_weights
            for layer in layers
        ]
        running_loss += calculate_loss_from_outputs_binary(
            layer_outputs[-1], y_batch, all_weights, reg_lambda
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


# TODO: @njit not working for this function
# @njit(fastmath=True, nogil=True, cache=CACHE)
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
        if layers[-1].layer_type == "dense":
            y_batch_ohe = one_hot_encode(y_batch, layers[-1].dense_weights.shape[1])
            # running_loss += calculate_loss_from_outputs_multi(layer_outputs[-1], y_batch_ohe, reg_lambda, [layer.dense_weights for layer in layers])
        elif layers[-1].layer_type == "conv":
            y_batch_ohe = one_hot_encode(y_batch, layers[-1].conv_weights.shape[0])
            # running_loss += calculate_loss_from_outputs_multi(layer_outputs[-1], y_batch_ohe, reg_lambda, [layer.conv_weights for layer in layers])

        all_weights = [
            layer.dense_weights if layer.layer_type == "dense" else layer.conv_weights
            for layer in layers
        ]
        running_loss += calculate_loss_from_outputs_multi(
            layer_outputs[-1], y_batch_ohe, reg_lambda, all_weights
        )

        running_accuracy += evaluate_batch(layer_outputs[-1], y_batch, False)

        # Accumulate gradients
        for i, layer in enumerate(layers):
            if layer.layer_type == "dense":
                dWs_acc.append(layer.dense_weight_grad)
                dbs_acc.append(layer.dense_bias_grad)
            elif layer.layer_type == "conv":
                dWs_acc.append(layer.conv_weight_grad)
                dbs_acc.append(layer.conv_bias_grad)

    # Average the accumulated gradients, loss, and accuracy
    for j in range(len(dWs_acc)):
        dWs_acc[j] /= num_batches
        dbs_acc[j] /= num_batches
    running_loss /= num_batches
    running_accuracy /= num_batches

    return dWs_acc, dbs_acc, running_loss, running_accuracy


@njit(fastmath=True, nogil=True, cache=CACHE)
def evaluate_jit(y_hat, y_true, is_binary):
    """
    Numba JIT-compiled function to evaluate model performance.
    Args:
        y_hat (ndarray): Model predictions.
        is_binary (bool): Whether the model is binary or multi-class.
    Returns:
        tuple: Accuracy and predicted labels.
    """
    if is_binary:
        predicted = (y_hat > 0.5).astype(np.int32).flatten()
        accuracy = np.mean(predicted == y_true.flatten())
    else:
        predicted = np.argmax(y_hat, axis=1).astype(np.int32)
        accuracy = np.mean(predicted == y_true)
    return accuracy, predicted
