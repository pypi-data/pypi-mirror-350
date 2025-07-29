import numpy as np
from numba import float64, int32, types
from numba.experimental import jitclass

from .numba_utils import *

spec = [
    ("weights", float64[:, ::1]),  # 2D array for weights
    ("biases", float64[:, ::1]),  # 2D array for biases
    ("activation", types.unicode_type),  # String for activation function
    ("weight_gradients", float64[:, ::1]),  # 2D array for weight gradients
    ("bias_gradients", float64[:, ::1]),  # 2D array for bias gradients
    ("input_cache", float64[:, ::1]),  # 2D array for input cache
    ("output_cache", float64[:, ::1]),  # 2D array for output cache
    ("input_size", int32),
    ("output_size", int32),
]


@jitclass(spec)
class JITDenseLayer:
    """Initializes a fully connected layer object, where each neuron is connected to all neurons in the previous layer.

    Each layer consists of weights, biases, and an activation function.

    Args:
        input_size (int): The size of the input to the layer.
        output_size (int): The size of the output from the layer.
        activation (str): The activation function to be used in the layer.

    Attributes:
        weights (np.ndarray): Weights of the layer.
        biases (np.ndarray): Biases of the layer.
        activation (str): Activation function name.
        weight_gradients (np.ndarray): Gradients of the weights.
        bias_gradients (np.ndarray): Gradients of the biases.
        input_cache (np.ndarray): Cached input for backpropagation.
        output_cache (np.ndarray): Cached output for backpropagation.

    Methods:
        zero_grad(): Resets the gradients of the weights and biases to zero.
        forward(X): Performs the forward pass of the layer.
        backward(dA, reg_lambda): Performs the backward pass of the layer.
        activate(Z): Applies the activation function.
        activation_derivative(Z): Applies the derivative of the activation function.
    """

    def __init__(self, input_size, output_size, activation="relu"):
        """Initializes the layer with weights, biases, and activation function.

        Args:
            input_size: (int) - The number of input features to the layer.
            output_size: (int) - The number of output features from the layer.
            activation: (str), optional - The activation function to use (default is "relu").

        Attributes:
            weights: (np.ndarray) - The weight matrix initialized using He initialization for ReLU or Leaky ReLU,
                        or Xavier initialization for other activations.
            biases: (np.ndarray) - The bias vector initialized to zeros.
            activation: (str) - The activation function for the layer.
            weight_gradients: (np.ndarray) - Gradients of the weights, initialized to zeros.
            bias_gradients: (np.ndarray) - Gradients of the biases, initialized to zeros.
            input_cache: (np.ndarray) - Cached input values for backpropagation, initialized to zeros.
            output_cache: (np.ndarray) - Cached output values for backpropagation, initialized to zeros.
            input_size: (int) - The number of input features to the layer.
            output_size: (int) - The number of output features from the layer.
        """
        # He initialization for weights
        if activation in ["relu", "leaky_relu"]:
            scale = np.sqrt(2.0 / input_size)
        else:
            scale = np.sqrt(1.0 / input_size)

        self.weights = np.random.randn(input_size, output_size) * scale
        self.biases = np.zeros((1, output_size))
        self.activation = activation
        self.weight_gradients = np.zeros(
            (input_size, output_size)
        )  # Initialize weight gradients to zeros
        self.bias_gradients = np.zeros(
            (1, output_size)
        )  # Initialize bias gradients to zeros
        self.input_cache = np.zeros((1, input_size))
        self.output_cache = np.zeros((1, output_size))
        self.input_size = input_size
        self.output_size = output_size

    def zero_grad(self):
        """Reset the gradients of the weights and biases to zero."""
        self.weight_gradients = np.zeros_like(self.weight_gradients)
        self.bias_gradients = np.zeros_like(self.bias_gradients)

    def forward(self, X):
        """Perform the forward pass of the layer."""
        Z = np.dot(X, self.weights) + self.biases
        self.input_cache = X
        self.output_cache = self.activate(Z)
        return self.output_cache

    def backward(self, dA, reg_lambda):
        """Perform the backward pass of the layer."""
        m = self.input_cache.shape[0]
        dZ = dA * self.activation_derivative(self.output_cache)
        dW = np.dot(self.input_cache.T, dZ) / m + reg_lambda * self.weights
        db = sum_axis0(dZ) / m
        dA_prev = np.dot(dZ, self.weights.T)

        self.weight_gradients = dW
        self.bias_gradients = db

        return dA_prev

    def activate(self, Z):
        """Apply activation function."""
        if self.activation == "relu":
            return relu(Z)
        elif self.activation == "leaky_relu":
            return leaky_relu(Z)
        elif self.activation == "tanh":
            return tanh(Z)
        elif self.activation == "sigmoid":
            return sigmoid(Z)
        elif self.activation == "softmax":
            return softmax(Z)
        elif self.activation == "linear" or self.activation == "none":
            return Z
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")

    def activation_derivative(self, Z):
        """Apply activation derivative."""
        if self.activation == "relu":
            return relu_derivative(Z)
        elif self.activation == "leaky_relu":
            return leaky_relu_derivative(Z)
        elif self.activation == "tanh":
            return tanh_derivative(Z)
        elif self.activation == "sigmoid":
            return sigmoid_derivative(Z)
        elif self.activation == "softmax":
            return np.ones_like(Z)  # Identity for compatibility
        elif self.activation == "linear" or self.activation == "none":
            return np.ones_like(Z)
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")


# Unchanged JITFlattenLayer implementation
flatten_spec = [
    ("input_shape", types.UniTuple(int32, 3)),
    ("output_size", int32),
    ("input_cache", float64[:, :, :, :]),
    ("input_size", int32),
]


@jitclass(flatten_spec)
class JITFlattenLayer:
    """A layer that flattens multi-dimensional input into a 2D array (batch_size, flattened_size).

    Useful for transitioning from convolutional layers to dense layers.
    """

    def __init__(self):
        """Initializes the layer with placeholder values for input and output dimensions.

        Attributes:
            input_shape: (tuple) - Shape of the input data, initialized to (0, 0, 0).
                       This will be set during the forward pass.
            output_size: (int) - Size of the output, initialized to 0.
                     This will be set during the forward pass.
            input_size: (int) - Size of the input, initialized to 0.
                    This will be set during the forward pass.
            input_cache: (any) - Cache for input data, to be set during the forward pass.
        """
        # Initialize with placeholder values
        self.input_shape = (0, 0, 0)  # Will be set during forward pass
        self.output_size = 0  # Will be set during forward pass
        self.input_size = 0  # Will be set during forward pass
        # input_cache will be set during forward pass

    def forward(self, X):
        """Flattens the input tensor.

        Args:
            X (np.ndarray): Input data of shape (batch_size, channels, height, width)

        Returns:
            np.ndarray: Flattened output of shape (batch_size, flattened_size)
        """
        # Cache the input for backward pass
        self.input_cache = X.copy()
        batch_size = X.shape[0]

        # Store input shape excluding batch size
        self.input_shape = (X.shape[1], X.shape[2], X.shape[3])

        # Calculate the size of the flattened vector
        self.input_size = (
            self.input_shape[0] * self.input_shape[1] * self.input_shape[2]
        )
        self.output_size = self.input_size

        # Reshape to (batch_size, flattened_size)
        result = np.zeros((batch_size, self.input_size), dtype=np.float64)
        for b in range(batch_size):
            # Manual flattening to avoid reshape contiguity issues
            idx = 0
            for c in range(self.input_shape[0]):
                for h in range(self.input_shape[1]):
                    for w in range(self.input_shape[2]):
                        result[b, idx] = X[b, c, h, w]
                        idx += 1
        return result

    def backward(self, dA, reg_lambda=0):
        """Reshapes the gradient back to the original input shape.

        Args:
            dA (np.ndarray): Gradient of the loss with respect to the layer's output,
                           shape (batch_size, flattened_size)
            reg_lambda (float): Regularization parameter (unused in FlattenLayer).

        Returns:
            np.ndarray: Gradient with respect to the input, reshaped to original input shape.
        """
        batch_size = dA.shape[0]
        # Create output array with proper shape
        result = np.zeros(
            (batch_size, self.input_shape[0], self.input_shape[1], self.input_shape[2]),
            dtype=np.float64,
        )

        # Manual reshaping to avoid contiguity issues
        for b in range(batch_size):
            idx = 0
            for c in range(self.input_shape[0]):
                for h in range(self.input_shape[1]):
                    for w in range(self.input_shape[2]):
                        result[b, c, h, w] = dA[b, idx]
                        idx += 1
        return result


# JITConvLayer specification
conv_spec = [
    ("in_channels", int32),
    ("out_channels", int32),
    ("kernel_size", int32),
    ("stride", int32),
    ("padding", int32),
    ("weights", float64[:, :, :, :]),  # 4D array for weights
    ("biases", float64[:, :]),  # 2D array for biases
    ("activation", types.unicode_type),  # String for activation function
    ("weight_gradients", float64[:, :, :, :]),  # 4D array for weight gradients
    ("bias_gradients", float64[:, :]),  # 2D array for bias gradients
    ("input_cache", float64[:, :, :, :]),  # 4D array for input cache
    ("X_cols", float64[:, :, :]),  # 3D array for column-transformed input
    ("X_padded", float64[:, :, :, :]),  # 4D array for padded input
    ("h_out", int32),  # Output height
    ("w_out", int32),  # Output width
    ("input_size", int32),
    ("output_size", int32),
]


@jitclass(conv_spec)
class JITConvLayer:
    """A convolutional layer implementation for neural networks using Numba JIT compilation."""

    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride=1,
        padding=0,
        activation="relu",
    ):
        """Initializes the convolutional layer with weights, biases, and activation function.

        Args:
            in_channels: (int) - Number of input channels.
            out_channels: (int) - Number of output channels.
            kernel_size: (int) - Size of the convolutional kernel (assumes square kernels).
            stride: (int), optional - Stride of the convolution (default is 1).
            padding: (int), optional - Padding added to the input (default is 0).
            activation: (str), optional - Activation function to use (default is "relu").

        Attributes:
            weights: (np.ndarray) - Convolutional weight matrix initialized using He initialization.
            biases: (np.ndarray) - Bias vector initialized to zeros.
            activation: (str) - Activation function for the layer.
            weight_gradients: (np.ndarray) - Gradients of the weights, initialized to zeros.
            bias_gradients: (np.ndarray) - Gradients of the biases, initialized to zeros.
            input_cache: (np.ndarray) - Cached input values for backpropagation, initialized to zeros.
            X_cols: (np.ndarray) - Cached column-transformed input for backpropagation, initialized to zeros.
            X_padded: (np.ndarray) - Cached padded input for backpropagation, initialized to zeros.
            h_out: (int) - Height of the output feature map, initialized to 0.
            w_out: (int) - Width of the output feature map, initialized to 0.
            input_size: (int) - Number of input channels.
            output_size: (int) - Number of output channels.
        """
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding

        # He initialization for convolutional weights
        scale = np.sqrt(2.0 / (in_channels * kernel_size * kernel_size))
        self.weights = (
            np.random.randn(out_channels, in_channels, kernel_size, kernel_size) * scale
        )
        self.biases = np.zeros((out_channels, 1))
        self.activation = activation

        # Initialize gradients and cache
        self.weight_gradients = np.zeros(
            (out_channels, in_channels, kernel_size, kernel_size)
        )
        self.bias_gradients = np.zeros((out_channels, 1))

        # These will be set during forward pass
        self.input_cache = np.zeros((1, in_channels, 1, 1))  # Placeholder
        self.X_cols = np.zeros((1, 1, 1))  # Placeholder
        self.X_padded = np.zeros((1, 1, 1, 1))  # Placeholder
        self.h_out = 0
        self.w_out = 0

        # Layer size info
        self.input_size = in_channels
        self.output_size = out_channels

    def zero_grad(self):
        """Reset the gradients of the weights and biases to zero."""
        self.weight_gradients = np.zeros_like(self.weights)
        self.bias_gradients = np.zeros_like(self.biases)

    def _im2col(self, x, h_out, w_out):
        """Convert image regions to columns for efficient convolution."""
        batch_size = x.shape[0]
        channels = x.shape[1]
        h = x.shape[2]
        w = x.shape[3]

        # Explicitly create contiguous output array
        col = np.zeros(
            (batch_size, channels * self.kernel_size * self.kernel_size, h_out * w_out),
            dtype=np.float64,
        )

        for b in range(batch_size):
            col_idx = 0
            for i in range(0, h - self.kernel_size + 1, self.stride):
                for j in range(0, w - self.kernel_size + 1, self.stride):
                    # Manually flatten the patch instead of using reshape
                    flat_idx = 0
                    for c in range(channels):
                        for ki in range(self.kernel_size):
                            for kj in range(self.kernel_size):
                                col[b, flat_idx, col_idx] = x[b, c, i + ki, j + kj]
                                flat_idx += 1
                    col_idx += 1

        return col

    def _col2im(self, dcol, x_shape):
        """Convert column back to image format for the backward pass."""
        batch_size = x_shape[0]
        channels = x_shape[1]
        h = x_shape[2]
        w = x_shape[3]

        h_padded = h + 2 * self.padding
        w_padded = w + 2 * self.padding

        dx_padded = np.zeros(
            (batch_size, channels, h_padded, w_padded), dtype=np.float64
        )

        for b in range(batch_size):
            col_idx = 0
            for i in range(0, h_padded - self.kernel_size + 1, self.stride):
                for j in range(0, w_padded - self.kernel_size + 1, self.stride):
                    # Manually reshape col_patch without using reshape
                    for c in range(channels):
                        for ki in range(self.kernel_size):
                            for kj in range(self.kernel_size):
                                flat_idx = (
                                    c * self.kernel_size * self.kernel_size
                                    + ki * self.kernel_size
                                    + kj
                                )
                                dx_padded[b, c, i + ki, j + kj] += dcol[
                                    b, flat_idx, col_idx
                                ]
                    col_idx += 1

        if self.padding > 0:
            # Return sliced array without padding
            result = np.zeros((batch_size, channels, h, w), dtype=np.float64)
            for b in range(batch_size):
                for c in range(channels):
                    for i in range(h):
                        for j in range(w):
                            result[b, c, i, j] = dx_padded[
                                b, c, i + self.padding, j + self.padding
                            ]
            return result
        return dx_padded

    def forward(self, X):
        """Forward pass for convolutional layer.

        Args:
            X: numpy array with shape (batch_size, in_channels, height, width)

        Returns:
            Output feature maps after convolution and activation.
        """
        self.input_cache = X.copy()
        batch_size = X.shape[0]
        h_in = X.shape[2]
        w_in = X.shape[3]

        # Calculate output dimensions
        h_out = (h_in + 2 * self.padding - self.kernel_size) // self.stride + 1
        w_out = (w_in + 2 * self.padding - self.kernel_size) // self.stride + 1
        self.h_out = h_out
        self.w_out = w_out

        # Apply padding if needed
        if self.padding > 0:
            X_padded = np.zeros(
                (
                    batch_size,
                    self.in_channels,
                    h_in + 2 * self.padding,
                    w_in + 2 * self.padding,
                ),
                dtype=np.float64,
            )
            # Manual padding
            for b in range(batch_size):
                for c in range(self.in_channels):
                    for i in range(h_in):
                        for j in range(w_in):
                            X_padded[b, c, i + self.padding, j + self.padding] = X[
                                b, c, i, j
                            ]
        else:
            X_padded = X.copy()  # Ensure it's a copy to maintain contiguity

        self.X_padded = X_padded

        # Use im2col to transform input for efficient matrix multiplication
        X_cols = self._im2col(X_padded, h_out, w_out)
        self.X_cols = X_cols

        # Create output array
        output = np.zeros(
            (batch_size, self.out_channels, h_out * w_out), dtype=np.float64
        )

        # Perform convolution using explicit loops instead of matrix multiplication for better Numba compatibility
        for b in range(batch_size):
            for o in range(self.out_channels):
                for i in range(h_out * w_out):
                    # Compute the dot product manually
                    val = self.biases[o, 0]
                    for c in range(self.in_channels):
                        for kh in range(self.kernel_size):
                            for kw in range(self.kernel_size):
                                # Calculate index in the flattened filter
                                filter_idx = (
                                    c * self.kernel_size * self.kernel_size
                                    + kh * self.kernel_size
                                    + kw
                                )
                                val += (
                                    self.weights[o, c, kh, kw]
                                    * X_cols[b, filter_idx, i]
                                )
                    output[b, o, i] = val

        # Reshape output to feature map format
        output_reshaped = np.zeros(
            (batch_size, self.out_channels, h_out, w_out), dtype=np.float64
        )
        for b in range(batch_size):
            for c in range(self.out_channels):
                for i in range(h_out):
                    for j in range(w_out):
                        idx = i * w_out + j
                        output_reshaped[b, c, i, j] = output[b, c, idx]

        # Apply activation function
        return self.activate(output_reshaped)

    def backward(self, d_out, reg_lambda=0):
        """Backward pass for convolutional layer.

        Args:
            d_out (np.ndarray): Gradient of the loss with respect to the layer output
            reg_lambda (float, optional): Regularization parameter

        Returns:
            dX: Gradient with respect to the input X
        """
        X = self.input_cache
        batch_size = X.shape[0]

        # Apply activation derivative
        d_activated = d_out * self.activation_derivative(d_out)

        # Reshape gradients to match the im2col format
        d_out_reshaped = np.zeros(
            (batch_size, self.out_channels, self.h_out * self.w_out), dtype=np.float64
        )
        for b in range(batch_size):
            for c in range(self.out_channels):
                for i in range(self.h_out):
                    for j in range(self.w_out):
                        idx = i * self.w_out + j
                        d_out_reshaped[b, c, idx] = d_activated[b, c, i, j]

        # Initialize gradients
        d_weights = np.zeros_like(self.weights)
        d_biases = np.zeros((self.out_channels, 1))
        d_X_cols = np.zeros_like(self.X_cols)

        # Compute gradients explicitly
        for b in range(batch_size):
            # Bias gradients
            for o in range(self.out_channels):
                for i in range(self.h_out * self.w_out):
                    d_biases[o, 0] += d_out_reshaped[b, o, i]

            # Weight gradients
            for o in range(self.out_channels):
                for c in range(self.in_channels):
                    for kh in range(self.kernel_size):
                        for kw in range(self.kernel_size):
                            filter_idx = (
                                c * self.kernel_size * self.kernel_size
                                + kh * self.kernel_size
                                + kw
                            )
                            for i in range(self.h_out * self.w_out):
                                d_weights[o, c, kh, kw] += (
                                    d_out_reshaped[b, o, i]
                                    * self.X_cols[b, filter_idx, i]
                                )

            # Input gradients
            for i in range(self.h_out * self.w_out):
                for filter_idx in range(
                    self.in_channels * self.kernel_size * self.kernel_size
                ):
                    val = 0.0
                    for o in range(self.out_channels):
                        val += (
                            d_out_reshaped[b, o, i]
                            * self.weights[
                                o,
                                filter_idx // (self.kernel_size * self.kernel_size),
                                (filter_idx % (self.kernel_size * self.kernel_size))
                                // self.kernel_size,
                                (filter_idx % (self.kernel_size * self.kernel_size))
                                % self.kernel_size,
                            ]
                        )
                    d_X_cols[b, filter_idx, i] = val

        # Convert gradients back to image format
        d_X = self._col2im(d_X_cols, X.shape)

        # Apply regularization to weight gradients
        if reg_lambda > 0:
            for o in range(self.out_channels):
                for c in range(self.in_channels):
                    for kh in range(self.kernel_size):
                        for kw in range(self.kernel_size):
                            d_weights[o, c, kh, kw] += (
                                reg_lambda * self.weights[o, c, kh, kw]
                            )

        # Store gradients
        self.weight_gradients = d_weights / batch_size  # Normalize by batch size
        self.bias_gradients = d_biases / batch_size  # Normalize by batch size

        return d_X

    def activate(self, Z):
        """Apply activation function."""
        if self.activation == "relu":
            return relu(Z)
        elif self.activation == "leaky_relu":
            return leaky_relu(Z)
        elif self.activation == "tanh":
            return tanh(Z)
        elif self.activation == "sigmoid":
            return sigmoid(Z)
        elif self.activation == "softmax":
            return softmax(Z)
        else:
            # For 'none' or unsupported activations, return input unchanged
            return Z

    def activation_derivative(self, Z):
        """Apply activation derivative."""
        if self.activation == "relu":
            return relu_derivative(Z)
        elif self.activation == "leaky_relu":
            return leaky_relu_derivative(Z)
        elif self.activation == "tanh":
            return tanh_derivative(Z)
        elif self.activation == "sigmoid":
            return sigmoid_derivative(Z)
        elif self.activation == "softmax":
            return np.ones_like(Z)  # Identity for compatibility
        else:
            # For 'none' or unsupported activations, return ones
            return np.ones_like(Z)


class JITRNNLayer:
    """A recurrent layer implementation for neural networks using Numba JIT compilation."""

    def __init__(self, input_size, hidden_size, activation="tanh"):
        """Will be implemented later."""
        pass
