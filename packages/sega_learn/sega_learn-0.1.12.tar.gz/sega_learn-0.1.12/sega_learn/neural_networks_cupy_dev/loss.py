import cupy as cp


class CrossEntropyLoss:
    """
    Optimized cross entropy loss implementation using cupy for multi-class classification.
    Formula: -sum(y * log(p)) / m
    Methods:
        __call__(self, logits, targets): Calculate the cross entropy loss.
    """

    def __call__(self, logits, targets):
        """
        Calculate the cross entropy loss.
        Args:
            logits (cp.ndarray): The logits (predicted values) of shape (num_samples, num_classes).
            targets (cp.ndarray): The target labels of shape (num_samples, num_classes) or (num_samples,).
        Returns:
            float: The cross entropy loss.
        """
        # Convert numpy arrays to cupy if needed - using asarray which avoids copying if already on GPU
        logits = cp.asarray(logits)
        targets = cp.asarray(targets)

        # One-hot encode targets if they are not already (using more efficient method)
        if targets.ndim == 1:
            num_classes = logits.shape[1]
            targets = cp.eye(num_classes, dtype=logits.dtype)[targets]

        # Apply log-softmax more efficiently (numerically stable)
        # Subtract max for numerical stability
        logits_max = cp.max(logits, axis=1, keepdims=True)
        logits_stable = logits - logits_max

        # Compute log softmax
        log_probs = logits_stable - cp.log(
            cp.sum(cp.exp(logits_stable), axis=1, keepdims=True)
        )

        # Compute loss directly without intermediate probability calculation
        batch_loss = -cp.sum(targets * log_probs) / logits.shape[0]

        # No need to check for .get() - just use .item() which works for both CuPy and NumPy
        return float(batch_loss.item())


class BCEWithLogitsLoss:
    """
    Optimized binary cross entropy loss with logits implementation using cupy.
    Formula: -mean(y * log(sigmoid(x)) + (1 - y) * log(1 - sigmoid(x)))
    Methods:
        __call__(self, logits, targets): Calculate the binary cross entropy loss.
    """

    def __call__(self, logits, targets):
        """
        Calculate the binary cross entropy loss.
        Args:
            logits (cp.ndarray): The logits (predicted values) of shape (num_samples,).
            targets (cp.ndarray): The target labels of shape (num_samples,).
        Returns:
            float: The binary cross entropy loss.
        """
        # Convert arrays if needed
        logits = cp.asarray(logits)
        targets = cp.asarray(targets)

        # Use a more numerically stable implementation
        # max(x,0) - x * z + log(1 + exp(-abs(x)))
        loss = (
            cp.maximum(logits, 0) - logits * targets + cp.log1p(cp.exp(-cp.abs(logits)))
        )

        # Calculate mean loss
        mean_loss = cp.mean(loss)

        # Return as scalar
        return float(mean_loss.item())
