import numpy as np
from numba import float64, int32, types
from numba.experimental import jitclass

from .numba_utils import *

# Define the unified layer specification, including a field for flatten layers.
layer_spec = [
    ("layer_type", types.unicode_type),  # "dense", "conv", or "flatten"
    (
        "input_size",
        int32,
    ),  # For dense: # of inputs; for conv: # channels; for flatten: dummy
    (
        "output_size",
        int32,
    ),  # For dense: # of neurons; for conv: # filters; for flatten: flattened size
    (
        "activation",
        types.unicode_type,
    ),  # Activation function (used for dense and conv; ignored for flatten)
    # Dense-specific fields:
    ("dense_weights", float64[:, ::1]),
    ("dense_biases", float64[:, ::1]),
    ("dense_weight_grad", float64[:, ::1]),  # Gradient of weights
    ("dense_bias_grad", float64[:, ::1]),  # Gradient of biases
    ("dense_input_cache", float64[:, ::1]),  # Cache for input during forward pass
    ("dense_output_cache", float64[:, ::1]),  # Cache for output during forward pass
    # Convolution-specific fields:
    ("kernel_size", int32),
    ("stride", int32),
    ("padding", int32),
    ("conv_weights", float64[:, :, :, :]),  # 4D array for weights
    ("conv_biases", float64[:, :]),  # 2D array for biases
    ("conv_weight_grad", float64[:, :, :, :]),  # 4D array for weight gradients
    ("conv_bias_grad", float64[:, :]),  # 2D array for bias gradients
    ("conv_input_cache", float64[:, :, :, :]),  # 4D array for input cache
    ("X_cols", float64[:, :, :]),  # 3D array for column-transformed input
    ("X_padded", float64[:, :, :, :]),  # 4D array for padded input
    ("h_out", int32),  # Output height
    ("w_out", int32),  # Output width
    # Flatten-specific field:
    ("flatten_input_shape", types.UniTuple(int32, 3)),
    ("flatten_input_cache", float64[:, :, :, :]),
]


@jitclass(layer_spec)
class JITLayer:
    def __init__(
        self,
        layer_type,
        input_size,
        output_size,
        activation="relu",
        # Conv-specific parameters (defaults for dense/flatten)
        #  Use input_size/output_size for in_channels/out_channels in conv layers
        kernel_size=0,
        stride=1,
        padding=0,
        # Flatten-specific parameters (defaults for dense/conv)
        # None
    ):
        # For all layers, set the layer type and sizes
        # layer_type: "dense", "conv", or "flatten"
        self.layer_type = layer_type
        self.input_size = input_size
        self.output_size = output_size
        self.activation = activation

        if layer_type == "dense":
            # For dense layers, use He initialization (for relu-like activations)
            if activation in ["relu", "leaky_relu"]:
                scale = np.sqrt(2.0 / input_size)
            else:
                scale = np.sqrt(1.0 / input_size)
            self.dense_weights = np.random.randn(input_size, output_size) * scale
            self.dense_biases = np.zeros((1, output_size))
            self.dense_weight_grad = np.zeros_like(self.dense_weights)
            self.dense_bias_grad = np.zeros_like(self.dense_biases)
            # Cache for input and output during forward pass
            self.dense_input_cache = np.zeros((1, input_size))
            self.dense_output_cache = np.zeros((1, output_size))

            # Dummy initialization for conv/flatten fields
            self.kernel_size = 0
            self.stride = 1
            self.padding = 0
            self.conv_weights = np.zeros((0, 0, 0, 0))
            self.conv_biases = np.zeros((0, 0))
            self.conv_weight_grad = np.zeros((0, 0, 0, 0))
            self.conv_bias_grad = np.zeros((0, 0))
            self.conv_input_cache = np.zeros((0, 0, 0, 0))
            self.X_cols = np.zeros((0, 0, 0))  # Dummy for column-transformed input
            self.X_padded = np.zeros((0, 0, 0, 0))
            self.h_out = 0
            self.w_out = 0
            self.flatten_input_cache = np.zeros(
                (1, input_size, 0, 0)
            )  # Dummy initialization for flatten

        elif layer_type == "conv":
            # For convolutional layers, input_size is number of input channels.
            self.kernel_size = kernel_size  # Assume square kernel
            self.stride = stride
            self.padding = padding
            # He initialization for conv layers
            scale = np.sqrt(2.0 / (input_size * kernel_size * kernel_size))
            self.conv_weights = (
                np.random.randn(output_size, input_size, kernel_size, kernel_size)
                * scale
            )
            self.conv_biases = np.zeros((output_size, 1))

            # Initialize gradients
            self.conv_weight_grad = np.zeros(
                (output_size, input_size, kernel_size, kernel_size)
            )
            self.conv_bias_grad = np.zeros((output_size, 1))

            # Initialize caches
            self.conv_input_cache = np.zeros((0, 0, 0, 0))
            self.X_cols = np.zeros((0, 0, 0))  # Dummy for column-transformed input
            self.X_padded = np.zeros((0, 0, 0, 0))  # Dummy for padded input
            self.h_out = 0  # Output height
            self.w_out = 0  # Output width

            # Dummy initialization for dense/flatten fields
            self.dense_weights = np.zeros((0, 0))
            self.dense_biases = np.zeros((0, 0))
            self.dense_weight_grad = np.zeros((0, 0))
            self.dense_bias_grad = np.zeros((0, 0))
            self.dense_input_cache = np.zeros((1, input_size))
            self.dense_output_cache = np.zeros((1, output_size))
            self.flatten_input_cache = np.zeros(
                (1, input_size, 0, 0)
            )  # Dummy initialization for flatten

        elif layer_type == "flatten":
            # Flatten layers do not have weights. Store the input shape on forward pass.
            # Ensure int32 for compatibility with Numba
            self.flatten_input_cache = np.zeros(
                (1, input_size, 0, 0)
            )  # Dummy initialization

            # Dummy initialization for dense
            self.dense_weights = np.zeros((0, 0))
            self.dense_biases = np.zeros((0, 0))
            self.dense_weight_grad = np.zeros((0, 0))
            self.dense_bias_grad = np.zeros((0, 0))
            self.dense_input_cache = np.zeros((1, input_size))
            self.dense_output_cache = np.zeros((1, output_size))

            # Dummy initialization for conv
            self.kernel_size = 0
            self.stride = 1
            self.padding = 0
            self.conv_weights = np.zeros((0, 0, 0, 0))
            self.conv_biases = np.zeros((0, 0))
            self.conv_weight_grad = np.zeros((0, 0, 0, 0))
            self.conv_bias_grad = np.zeros((0, 0))
            self.conv_input_cache = np.zeros((0, 0, 0, 0))
            self.X_cols = np.zeros((0, 0, 0))  # Dummy for column-transformed input
            self.X_padded = np.zeros((0, 0, 0, 0))
            self.h_out = 0
            self.w_out = 0

        else:
            raise ValueError("Unsupported layer type")

    def zero_grad(self):
        """Zero out gradients for the layer."""
        if self.layer_type == "dense":
            self.dense_weight_grad = np.zeros_like(self.dense_weights)
            self.dense_bias_grad = np.zeros_like(self.dense_biases)
        elif self.layer_type == "conv":
            self.conv_weights = np.zeros_like(self.conv_weights)
            self.conv_biases = np.zeros_like(self.conv_biases)
        elif self.layer_type == "flatten":
            pass

    def forward(self, X):
        if self.layer_type == "dense":
            return self._forward_dense(X)
        elif self.layer_type == "conv" or self.layer_type == "flatten":
            pass
            # return self._forward_flatten(X)
        else:
            raise ValueError("Unsupported layer type")

    def backward(self, dA, reg_lambda):
        if self.layer_type == "dense":
            return self._backward_dense(dA, reg_lambda)
        elif self.layer_type == "conv" or self.layer_type == "flatten":
            pass
            # return self._backward_flatten(dA)
        else:
            raise ValueError("Unsupported layer type")

    def _forward_dense(self, X):
        """Forward pass for dense layer."""
        Z = np.dot(X, self.dense_weights) + self.dense_biases
        self.dense_input_cache = X
        self.dense_output_cache = self.activate(Z)
        return self.dense_output_cache

    def _backward_dense(self, dA, reg_lambda):
        """Backward pass for dense layer."""
        m = self.dense_input_cache.shape[0]
        dZ = dA * self.activation_derivative(self.dense_output_cache)
        dW = np.dot(self.dense_input_cache.T, dZ) / m + reg_lambda * self.dense_weights
        db = sum_axis0(dZ) / m
        dA_prev = np.dot(dZ, self.dense_weights.T)

        self.dense_weight_grad = dW
        self.dense_bias_grad = db

        return dA_prev

    def _forward_conv(self, X):
        """
        Forward pass for convolutional layer.

        Args:
            X: numpy array with shape (batch_size, in_channels, height, width)
                in_channels = input channels
                height = input height
                width = input width
        Returns:
            Output feature maps after convolution and activation.
        """
        self.conv_input_cache = X  # Cache input for backward pass
        # Check input dimensions
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
                    self.input_size,
                    h_in + 2 * self.padding,
                    w_in + 2 * self.padding,
                ),
                dtype=np.float64,
            )
            # Manual padding
            for b in range(batch_size):
                for c in range(self.input_size):
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
            (batch_size, self.output_size, h_out * w_out), dtype=np.float64
        )

        # Perform convolution using explicit loops instead of matrix multiplication for better Numba compatibility
        for b in range(batch_size):
            for o in range(self.output_size):
                for i in range(h_out * w_out):
                    # Compute the dot product manually
                    val = self.conv_biases[o, 0]
                    for c in range(self.input_size):
                        for kh in range(self.kernel_size):
                            for kw in range(self.kernel_size):
                                # Calculate index in the flattened filter
                                filter_idx = (
                                    c * self.kernel_size * self.kernel_size
                                    + kh * self.kernel_size
                                    + kw
                                )
                                val += (
                                    self.conv_weights[o, c, kh, kw]
                                    * X_cols[b, filter_idx, i]
                                )
                    output[b, o, i] = val

        # Reshape output to feature map format
        output_reshaped = np.zeros(
            (batch_size, self.output_size, h_out, w_out), dtype=np.float64
        )
        for b in range(batch_size):
            for c in range(self.output_size):
                for i in range(h_out):
                    for j in range(w_out):
                        idx = i * w_out + j
                        output_reshaped[b, c, i, j] = output[b, c, idx]

        # Apply activation function
        return self.activate(output_reshaped)

    def _backward_conv(self, d_out, reg_lambda=0.0):
        """
        Backward pass for convolutional layer.

        Args:
            d_out (np.ndarray): Gradient of the loss with respect to the layer output
            reg_lambda (float, optional): Regularization parameter

        Returns:
            dX: Gradient with respect to the input X
        """
        X = self.conv_input_cache  # Cached input from forward pass
        # Check input dimensions
        batch_size = X.shape[0]

        # Apply activation derivative
        d_activated = d_out * self.activation_derivative(d_out)

        # Reshape gradients to match the im2col format
        d_out_reshaped = np.zeros(
            (batch_size, self.output_size, self.h_out * self.w_out), dtype=np.float64
        )
        for b in range(batch_size):
            for c in range(self.output_size):
                for i in range(self.h_out):
                    for j in range(self.w_out):
                        idx = i * self.w_out + j
                        d_out_reshaped[b, c, idx] = d_activated[b, c, i, j]

        # Initialize gradients
        d_weights = np.zeros_like(self.conv_weights)  # Gradient of weights
        d_biases = np.zeros((self.output_size, 1))
        d_X_cols = np.zeros_like(self.X_cols)

        # Compute gradients explicitly
        for b in range(batch_size):
            # Bias gradients
            for o in range(self.output_size):
                for i in range(self.h_out * self.w_out):
                    d_biases[o, 0] += d_out_reshaped[b, o, i]

            # Weight gradients
            for o in range(self.output_size):
                for c in range(self.input_size):
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
                    self.input_size * self.kernel_size * self.kernel_size
                ):
                    val = 0.0
                    for o in range(self.output_size):
                        val += (
                            d_out_reshaped[b, o, i]
                            * self.conv_weights[
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
            for o in range(self.output_size):
                for c in range(self.input_size):
                    for kh in range(self.kernel_size):
                        for kw in range(self.kernel_size):
                            d_weights[o, c, kh, kw] += (
                                reg_lambda * self.conv_weights[o, c, kh, kw]
                            )

        # Store gradients
        self.weight_gradients = d_weights / batch_size  # Normalize by batch size
        self.bias_gradients = d_biases / batch_size  # Normalize by batch size

        return d_X

    def _forward_flatten(self, X):
        """
        Flattens the input tensor.

        Args:
            X (np.ndarray): Input data of shape (batch_size, channels, height, width)

        Returns:
            np.ndarray: Flattened output of shape (batch_size, flattened_size)
        """
        # Cache the input for backward pass
        self.flatten_input_cache = X.copy()
        batch_size = X.shape[0]

        # Store input shape excluding batch size
        self.flatten_input_shape = (
            int32(X.shape[1]),
            int32(X.shape[2]),
            int32(X.shape[3]),
        )

        # Calculate flattened vector size
        self.input_size = X.shape[1] * X.shape[2] * X.shape[3]
        self.output_size = (
            self.input_size
        )  # For flatten layer, input and output sizes are the same

        # Reshape input to flatten (batch_size, channels * height * width (flatten_size))
        output = np.zeros((batch_size, self.input_size), dtype=np.float64)
        for b in range(batch_size):
            # Manual flattening to avoid reshape contiguity issues
            idx = 0
            for c in range(self.flatten_input_shape[0]):
                for h in range(self.flatten_input_shape[1]):
                    for w in range(self.flatten_input_shape[2]):
                        output[b, idx] = X[b, c, h, w]
                        idx += 1
        return output

    def _backward_flatten(self, dA):
        """
        Reshapes the gradient back to the original input shape.

        Args:
            dA (np.ndarray): Gradient of the loss with respect to the layer's output,
                           shape (batch_size, flattened_size)
            reg_lambda (float): Regularization parameter (unused in FlattenLayer).

        Returns:
            np.ndarray: Gradient with respect to the input, reshaped to original input shape.
        """
        batch_size = dA.shape[0]

        # Create an output array with the original input shape
        output = np.zeros(
            (
                batch_size,
                self.flatten_input_shape[0],
                self.flatten_input_shape[1],
                self.flatten_input_shape[2],
            ),
            dtype=np.float64,
        )

        # Manual reshaping to avoid contiguity issues
        for b in range(batch_size):
            idx = 0
            for c in range(self.flatten_input_shape[0]):
                for h in range(self.flatten_input_shape[1]):
                    for w in range(self.flatten_input_shape[2]):
                        output[b, c, h, w] = dA[b, idx]
                        idx += 1
        return output

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
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")

    def _im2col(self, x, h_out, w_out):
        """
        Convert image regions to columns for efficient convolution.
        Fixed to avoid reshape contiguity issues.
        """
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
        """
        Convert column back to image format for the backward pass.
        Fixed to avoid reshape contiguity issues.
        """
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
