import cupy as cp
from cupy import fuse


# Fused dropout kernel: combines masking and scaling into one operation.
@fuse()
def fused_dropout(x, dropout_rate, random_vals):
    """Apply fused dropout operation."""
    return cp.where(random_vals < (1 - dropout_rate), x / (1 - dropout_rate), 0)


def apply_dropout(X, dropout_rate):
    """Generate dropout mask and apply fused dropout."""
    random_vals = cp.random.rand(*X.shape)
    return fused_dropout(X, dropout_rate, random_vals)


# Fused activation functions to fuse operations and reduce kernel launches.
@fuse()
def fused_relu(x):
    """Apply fused ReLU activation."""
    return cp.where(x > 0, x, 0)


@fuse()
def fused_sigmoid(x):
    """Apply fused sigmoid activation."""
    return 1 / (1 + cp.exp(-x))


@fuse()
def fused_leaky_relu(x, alpha=0.01):
    """Apply fused leaky ReLU activation."""
    return cp.where(x > 0, x, alpha * x)


# Optimized forward pass with in-place operations and fused kernels.
def forward_cupy(X, weights, biases, activations, dropout_rate, training, is_binary):
    """Perform forward pass using CuPy with fused and in-place operations."""
    num_layers = len(weights)
    layer_outputs = [X]
    for i in range(num_layers - 1):
        # Compute linear transformation.
        Z = cp.dot(layer_outputs[i], weights[i]) + biases[i]

        # Apply activation using in-place or fused operations.
        if activations[i] == "relu":
            cp.maximum(Z, 0, out=Z)  # In-place ReLU.
            A = Z
        elif activations[i] == "leaky_relu":
            A = fused_leaky_relu(Z)
        elif activations[i] == "tanh":
            cp.tanh(Z, out=Z)  # In-place tanh.
            A = Z
        elif activations[i] == "sigmoid":
            A = fused_sigmoid(Z)
        elif activations[i] == "softmax":
            # Use log-sum-exp trick for numerical stability.
            max_Z = cp.max(Z, axis=1, keepdims=True)
            Z -= max_Z  # In-place subtraction.
            cp.exp(Z, out=Z)
            sum_Z = cp.sum(Z, axis=1, keepdims=True)
            A = Z / sum_Z
        else:
            raise ValueError(f"Unsupported activation: {activations[i]}")

        # Apply dropout if in training mode.
        if training and dropout_rate > 0:
            A = apply_dropout(A, dropout_rate)
        layer_outputs.append(A)

    # Output layer computation.
    Z = cp.dot(layer_outputs[-1], weights[-1]) + biases[-1]
    if is_binary:
        A = fused_sigmoid(Z)
    else:
        max_Z = cp.max(Z, axis=1, keepdims=True)
        Z -= max_Z
        cp.exp(Z, out=Z)
        sum_Z = cp.sum(Z, axis=1, keepdims=True)
        A = Z / sum_Z
    layer_outputs.append(A)
    return layer_outputs


# Backward pass remains similar; note that you can also consider fusing derivative computations.
def backward_cupy(
    layer_outputs, y, weights, activations, reg_lambda, is_binary, dWs, dbs
):
    """Perform backward pass using CuPy with fused derivative computations."""
    m = y.shape[0]
    num_layers = len(weights)
    outputs = layer_outputs[-1]
    if is_binary:
        y = y.reshape(-1, 1).astype(cp.float64)
        dA = -(y / (outputs + 1e-15) - (1 - y) / (1 - outputs + 1e-15))
    else:
        dA = outputs.copy()
        dA[cp.arange(m), y] -= 1  # Advanced indexing supported in CuPy.

    for i in range(num_layers - 1, -1, -1):
        prev_activation = layer_outputs[i]
        if i < num_layers - 1:
            output = layer_outputs[i + 1]
            if activations[i] == "relu":
                dZ = dA * (output > 0)
            elif activations[i] == "leaky_relu":
                dZ = dA * cp.where(output > 0, 1, 0.01)
            elif activations[i] == "tanh":
                dZ = dA * (1 - output**2)
            elif activations[i] == "sigmoid":
                dZ = dA * output * (1 - output)
            elif activations[i] == "softmax":
                dZ = dA
            else:
                raise ValueError(f"Unsupported activation: {activations[i]}")
        else:
            dZ = dA

        dW = cp.dot(prev_activation.T, dZ) / m + reg_lambda * weights[i]
        db = cp.sum(dZ, axis=0, keepdims=True) / m
        dWs[i] = dW
        dbs[i] = db
        if i > 0:
            dA = cp.dot(dZ, weights[i].T)
    return dWs, dbs


# Optimized loss functions.
def logsumexp(a, axis=None, keepdims=False):
    """Compute log-sum-exp for numerical stability."""
    a_max = cp.max(a, axis=axis, keepdims=True)
    out = cp.log(cp.sum(cp.exp(a - a_max), axis=axis, keepdims=True)) + a_max
    if not keepdims:
        out = cp.squeeze(out, axis=axis)
    return out


def calculate_cross_entropy_loss(logits, targets):
    """Calculate cross-entropy loss for multi-class classification."""
    n = logits.shape[0]
    c_i = cp.argmax(targets, axis=1)
    loss = cp.mean(logsumexp(logits, axis=1) - logits[cp.arange(n), c_i])
    return loss


def calculate_bce_with_logits_loss(logits, targets):
    """Calculate binary cross-entropy loss with logits."""
    # Numerically stable BCE with logits formulation.
    loss = cp.mean(
        cp.maximum(logits, 0) - logits * targets + cp.log1p(cp.exp(-cp.abs(logits)))
    )
    return loss


def calculate_loss_from_outputs_binary(outputs, y, weights, reg_lambda):
    """Calculate binary classification loss with L2 regularization."""
    loss = calculate_bce_with_logits_loss(outputs, y)
    if isinstance(weights, list):
        l2_reg = reg_lambda * cp.sum([cp.sum(w**2) for w in weights])
        loss += l2_reg
    return float(loss)


def calculate_loss_from_outputs_multi(outputs, y, weights, reg_lambda):
    """Calculate multi-class classification loss with L2 regularization."""
    loss = calculate_cross_entropy_loss(outputs, y)
    if isinstance(weights, list):
        l2_reg = reg_lambda * cp.sum([cp.sum(w**2) for w in weights])
        loss += l2_reg
    return float(loss)


def evaluate_batch(y_hat, y_true, is_binary):
    """Evaluate batch accuracy for binary or multi-class classification."""
    if is_binary:
        predicted = (y_hat > 0.5).astype(cp.int32).ravel()
        accuracy = cp.mean(predicted == y_true.ravel())
    else:
        predicted = cp.argmax(y_hat, axis=1).astype(cp.int32)
        accuracy = cp.mean(predicted == y_true)
    return accuracy
