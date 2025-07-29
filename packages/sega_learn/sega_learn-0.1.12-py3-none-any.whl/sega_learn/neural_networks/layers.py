import numpy as np

from .activations import Activation


class DenseLayer:
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
            weights: (np.ndarray) - The weight matrix initialized using He initialization for ReLU or Leaky ReLU, or standard initialization otherwise.
            biases: (np.ndarray) - The bias vector initialized to zeros.
            input_size: (int) - The number of input features to the layer.
            output_size: (int) - The number of output features from the layer.
            activation: (str) - The activation function to use.
            weight_gradients: (np.ndarray or None) - Gradients of the weights, initialized to None.
            bias_gradients: (np.ndarray or None) - Gradients of the biases, initialized to None.
        """
        # He initialization for weights
        if activation in ["relu", "leaky_relu"]:
            scale = np.sqrt(2.0 / input_size)
        else:
            scale = np.sqrt(1.0 / input_size)

        self.weights = np.random.randn(input_size, output_size) * scale
        self.biases = np.zeros((1, output_size))
        self.input_size = input_size
        self.output_size = output_size
        self.activation = activation
        self.weight_gradients = None
        self.bias_gradients = None

    def zero_grad(self):
        """Reset the gradients of the weights and biases to zero."""
        self.weight_gradients = None
        self.bias_gradients = None

    def forward(self, X):
        """Forward pass of the layer."""
        Z = np.dot(X, self.weights) + self.biases
        self.input_cache = X
        self.output_cache = self.activate(Z)
        return self.output_cache

    def backward(self, dA, reg_lambda):
        """Backward pass of the layer."""
        m = self.input_cache.shape[0]
        dZ = dA * self.activation_derivative(self.output_cache)
        dW = np.dot(self.input_cache.T, dZ) / m + reg_lambda * self.weights
        db = np.sum(dZ, axis=0, keepdims=True) / m
        dA_prev = np.dot(dZ, self.weights.T)

        self.weight_gradients = dW
        self.bias_gradients = db

        return dA_prev

    def activate(self, Z):
        """Apply activation function."""
        activation_functions = {
            "relu": Activation.relu,
            "leaky_relu": Activation.leaky_relu,
            "tanh": Activation.tanh,
            "sigmoid": Activation.sigmoid,
            "softmax": Activation.softmax,
            "linear": lambda Z: Z,
            "none": lambda Z: Z,
        }

        if self.activation in activation_functions:
            return activation_functions[self.activation](Z)
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")

    def activation_derivative(self, Z):
        """Apply activation derivative."""
        if self.activation == "relu":
            return Activation.relu_derivative(Z)
        elif self.activation == "leaky_relu":
            return Activation.leaky_relu_derivative(Z)
        elif self.activation == "tanh":
            return Activation.tanh_derivative(Z)
        elif self.activation == "sigmoid":
            return Activation.sigmoid_derivative(Z)
        elif self.activation == "softmax":
            # Softmax derivative handled in loss function
            return np.ones_like(Z)  # Identity for compatibility
        elif self.activation in ["none", "linear"]:
            return np.ones_like(Z)  # Identity for compatibility
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")


class FlattenLayer:
    """A layer that flattens multi-dimensional input into a 2D array (batch_size, flattened_size).

    Useful for transitioning from convolutional layers to dense layers.

    Attributes:
        input_shape: (tuple) - Shape of the input data (excluding batch size).
        output_size: (int) - Size of the flattened output vector.
        input_cache: (np.ndarray) - Cached input for backpropagation.
        input_size: (int) - Size of the input (same as input_shape).
        output_size: (int) - Size of the output (same as output_size).
    """

    def __init__(self):
        """Initializes the layer with default attributes.

        Attributes:
            input_shape: (tuple or None) - Shape of the input data, to be set dynamically during the forward pass.
            output_size: (int or None) - Size of the output data, to be set dynamically during the forward pass.
            input_cache: (any or None) - Cache to store input data for use during backpropagation.
            input_size: (int or None) - Flattened size of the input, calculated as channels * height * width.
            output_size: (int or None) - Flattened size of the output, same as input_size.
        """
        self.input_shape = None
        self.output_size = None
        self.input_cache = None
        # These are set dynamically during the forward pass
        self.input_size = None  # Will be set based on input channels * height * width
        self.output_size = None  # Same as input_size (flattened)

    def forward(self, X):
        """Flattens the input tensor.

        Args:
            X: (np.ndarray) - Input data of shape (batch_size, channels, height, width)
                           or any multi-dimensional shape after batch dimension.

        Returns:
            np.ndarray: Flattened output of shape (batch_size, flattened_size)
        """
        self.input_cache = X.copy()
        batch_size = X.shape[0]
        self.input_shape = X.shape[1:]  # Store input shape excluding batch size

        # Calculate the size of the flattened vector
        self.input_size = np.prod(self.input_shape)
        self.output_size = self.input_size

        # Reshape to (batch_size, flattened_size)
        return X.reshape(batch_size, self.input_size)

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
        # Reshape gradient back to the original input shape
        return dA.reshape(batch_size, *self.input_shape)


class ConvLayer:
    """A convolutional layer implementation for neural networks.

    This layer performs 2D convolution operations, commonly used in convolutional neural networks (CNNs).
    The implementation uses the im2col technique for efficient computation, transforming the convolution operation into matrix multiplication.
    An optional activation function is applied element-wise to the output.

    Args:
        in_channels (int): Number of input channels (depth of input volume).
        out_channels (int): Number of output channels (number of filters).
        kernel_size (int): Size of the convolutional kernel (square kernel assumed).
        stride (int, optional): Stride of the convolution. Default: 1.
        padding (int, optional): Zero-padding added to both sides of the input. Default: 0.
        activation (str, optional): Activation function to use. Options are "relu", "sigmoid", "tanh", or None. Default: "relu".

    Attributes:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
        kernel_size (int): Size of the square convolutional kernel.
        stride (int): Stride of the convolution.
        padding (int): Zero-padding added to both sides of the input.
        weights (numpy.ndarray): Learnable weights of shape (out_channels, in_channels, kernel_size, kernel_size).
        biases (numpy.ndarray): Learnable biases of shape (out_channels, 1).
        activation (str): Type of activation function.
        weight_gradients (numpy.ndarray): Gradients with respect to weights.
        bias_gradients (numpy.ndarray): Gradients with respect to biases.
        input_cache (numpy.ndarray): Cached input for use in backward pass.
        X_cols (numpy.ndarray): Cached column-transformed input.
        X_padded (numpy.ndarray): Cached padded input.
        h_out (int): Height of output feature maps.
        w_out (int): Width of output feature maps.
        input_size (int): Size of input (same as in_channels).
        output_size (int): Size of output (same as out_channels).

    Methods:
        zero_grad(): Reset gradients to zero.
        _im2col(x, h_out, w_out): Convert image regions to columns for efficient convolution.
        forward(X): Perform forward pass of the convolutional layer.
        _col2im(dcol, x_shape): Convert column back to image format for the backward pass.
        backward(d_out, reg_lambda=0): Perform backward pass of the convolutional layer.
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        stride=1,
        padding=0,
        activation="relu",
    ):
        """Initializes a convolutional layer object for neural networks.

        This layer performs 2D convolution operations, commonly used in convolutional neural networks (CNNs).

        Args:
            in_channels: (int) - Number of input channels (depth of input volume).
            out_channels: (int) - Number of output channels (number of filters).
            kernel_size: (int) - Size of the convolutional kernel (square kernel assumed).
            stride: (int), optional - Stride of the convolution (default is 1).
            padding: (int), optional - Zero-padding added to both sides of the input (default is 0).
            activation: (str), optional - Activation function to use (default is "relu").

        Attributes:
            in_channels: (int) - Number of input channels.
            out_channels: (int) - Number of output channels.
            kernel_size: (int) - Size of the square convolutional kernel.
            stride: (int) - Stride of the convolution.
            padding: (int) - Zero-padding added to both sides of the input.
            weights: (np.ndarray) - Learnable weights of shape (out_channels, in_channels, kernel_size, kernel_size).
            biases: (np.ndarray) - Learnable biases of shape (out_channels, 1).
            activation: (str) - Type of activation function.
            weight_gradients: (np.ndarray or None) - Gradients with respect to weights, initialized to None.
            bias_gradients: (np.ndarray or None) - Gradients with respect to biases, initialized to None.
            input_cache: (np.ndarray or None) - Cached input for use in backward pass.
            input_size: (int) - Size of input (same as in_channels).
            output_size: (int) - Size of output (same as out_channels).
        """
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size  # Assume square kernels
        self.stride = stride
        self.padding = padding

        # He initialization for convolutional weights
        self.weights = np.random.randn(
            out_channels, in_channels, kernel_size, kernel_size
        ) * np.sqrt(2.0 / (in_channels * kernel_size * kernel_size))
        self.biases = np.zeros((out_channels, 1))
        self.activation = activation

        # Placeholders for gradients and cache for backpropagation
        self.weight_gradients = None
        self.bias_gradients = None
        self.input_cache = None

        # Layer size information
        self.input_size = in_channels
        self.output_size = out_channels

    def zero_grad(self):
        """Reset the gradients of the weights and biases to zero."""
        self.weight_gradients = np.zeros_like(self.weights)
        self.bias_gradients = np.zeros_like(self.biases)

    def _im2col(self, x, h_out, w_out):
        """Convert image regions to columns for efficient convolution.

        This transforms the 4D input tensor into a 2D matrix where each column
        contains a kernel-sized region of the input.
        """
        batch_size, channels, h, w = x.shape
        col = np.zeros(
            (batch_size, channels * self.kernel_size * self.kernel_size, h_out * w_out)
        )

        for b in range(batch_size):
            col_idx = 0
            for i in range(0, h - self.kernel_size + 1, self.stride):
                for j in range(0, w - self.kernel_size + 1, self.stride):
                    patch = x[b, :, i : i + self.kernel_size, j : j + self.kernel_size]
                    col[b, :, col_idx] = patch.reshape(-1)
                    col_idx += 1

        return col

    def _col2im(self, dcol, x_shape):
        """Convert column back to image format for the backward pass."""
        batch_size, channels, h, w = x_shape
        h_padded, w_padded = h + 2 * self.padding, w + 2 * self.padding
        dx_padded = np.zeros((batch_size, channels, h_padded, w_padded))

        for b in range(batch_size):
            col_idx = 0
            for i in range(0, h_padded - self.kernel_size + 1, self.stride):
                for j in range(0, w_padded - self.kernel_size + 1, self.stride):
                    col_patch = dcol[b, :, col_idx].reshape(
                        channels, self.kernel_size, self.kernel_size
                    )
                    dx_padded[
                        b, :, i : i + self.kernel_size, j : j + self.kernel_size
                    ] += col_patch
                    col_idx += 1

        if self.padding > 0:
            return dx_padded[
                :, :, self.padding : -self.padding, self.padding : -self.padding
            ]
        return dx_padded

    def forward(self, X):
        """Perform forward pass of the convolutional layer.

        Args:
            X: numpy array with shape (batch_size, in_channels, height, width)

        Returns:
            Output feature maps after convolution and activation.
        """
        self.input_cache = X
        batch_size, in_channels, h_in, w_in = X.shape

        # Calculate output dimensions
        h_out = int((h_in + 2 * self.padding - self.kernel_size) / self.stride) + 1
        w_out = int((w_in + 2 * self.padding - self.kernel_size) / self.stride) + 1

        # Apply padding if needed
        if self.padding > 0:
            X_padded = np.pad(
                X,
                (
                    (0, 0),
                    (0, 0),
                    (self.padding, self.padding),
                    (self.padding, self.padding),
                ),
                mode="constant",
            )
        else:
            X_padded = X

        # Use im2col to transform input for efficient matrix multiplication
        X_cols = self._im2col(X_padded, h_out, w_out)

        # Reshape weights for batch matrix multiplication
        W_reshaped = self.weights.reshape(
            self.out_channels, -1
        )  # (out_channels, in_channels*k*k)

        # Perform convolution using matrix multiplication
        output = np.zeros((batch_size, self.out_channels, h_out * w_out))
        for b in range(batch_size):
            output[b] = W_reshaped @ X_cols[b] + self.biases

        # Reshape output to feature map format
        output = output.reshape(batch_size, self.out_channels, h_out, w_out)

        # Cache for backward pass
        self.X_cols = X_cols
        self.X_padded = X_padded
        self.h_out, self.w_out = h_out, w_out

        return self.activate(output)

    def backward(self, d_out, reg_lambda=0):
        """Optimized backward pass using im2col technique.

        Args:
            d_out: (np.ndarray) - Gradient of the loss with respect to the layer output,
                              shape (batch_size, out_channels, h_out, w_out)
            reg_lambda: (float, optional) - Regularization parameter.

        Returns:
            dX: Gradient with respect to the input X.
        """
        X = self.input_cache
        batch_size = X.shape[0]

        # Reshape gradients to match the im2col format
        d_out_reshaped = d_out.reshape(
            batch_size, self.out_channels, -1
        )  # (batch, out_channels, h_out*w_out)

        # Initialize gradients
        d_weights = np.zeros_like(self.weights)
        d_biases = np.zeros((self.out_channels, 1))
        d_X_cols = np.zeros_like(self.X_cols)

        # Reshape weights
        W_reshaped = self.weights.reshape(
            self.out_channels, -1
        )  # (out_channels, in_channels*k*k)

        # Compute gradients
        for b in range(batch_size):
            # Gradient of bias is the sum across spatial dimensions
            d_biases += np.sum(d_out_reshaped[b], axis=1, keepdims=True)

            # Gradient of weights
            d_weights_reshaped = (
                d_out_reshaped[b] @ self.X_cols[b].T
            )  # (out_channels, in_channels*k*k)
            d_weights += d_weights_reshaped.reshape(self.weights.shape).astype(
                self.weights.dtype
            )

            # Gradient of input
            d_X_cols[b] = W_reshaped.T @ d_out_reshaped[b]

        # Convert gradients back to image format
        d_X = self._col2im(d_X_cols, X.shape)

        # Store gradients
        self.weight_gradients = d_weights
        self.bias_gradients = d_biases

        return d_X

    def activate(self, Z):
        """Apply activation function."""
        activation_functions = {
            "relu": Activation.relu,
            "leaky_relu": Activation.leaky_relu,
            "tanh": Activation.tanh,
            "sigmoid": Activation.sigmoid,
            "softmax": Activation.softmax,
            "linear": lambda Z: Z,
            "none": lambda Z: Z,
        }

        if self.activation in activation_functions:
            return activation_functions[self.activation](Z)
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")


class RNNLayer:
    """Will be implemented later."""

    def __init__(self, input_size, hidden_size, activation="tanh"):
        """Will be implemented later."""
        pass

    #     self.input_size = input_size
    #     self.hidden_size = hidden_size
    #     # Initialize weights (small random values)
    #     self.Wxh = np.random.randn(input_size, hidden_size) * 0.01  # Input-to-hidden weights
    #     self.Whh = np.random.randn(hidden_size, hidden_size) * 0.01  # Hidden-to-hidden weights
    #     self.bh = np.zeros((1, hidden_size))                       # Biases
    #     self.activation = activation
    #     self.weight_gradients = {"Wxh": None, "Whh": None, "bh": None}
    #     # Caches for backpropagation through time
    #     self.last_inputs = None
    #     self.last_hs = None

    # def forward(self, X):
    #     """
    #     X: numpy array with shape (batch_size, time_steps, input_size)
    #     Returns:
    #         hidden_states: numpy array with shape (batch_size, time_steps, hidden_size)
    #     """
    #     batch_size, time_steps, _ = X.shape
    #     # Initialize hidden state to zeros
    #     h = np.zeros((batch_size, self.hidden_size))
    #     self.last_hs = {-1: h}
    #     self.last_inputs = X
    #     outputs = []
    #     # Process each time step
    #     for t in range(time_steps):
    #         x_t = X[:, t, :]
    #         h = np.tanh(np.dot(x_t, self.Wxh) + np.dot(h, self.Whh) + self.bh)
    #         self.last_hs[t] = h
    #         outputs.append(h)
    #     # Stack outputs along time dimension
    #     return np.stack(outputs, axis=1)

    # def backward(self, d_out, learning_rate=1e-2):
    #     """
    #     d_out: Gradient of the loss with respect to the hidden states,
    #            shape (batch_size, time_steps, hidden_size)
    #     learning_rate: Learning rate for parameter updates
    #     Returns:
    #         d_h_next: Gradient to propagate to previous network layers (from t=0)
    #     """
    #     X = self.last_inputs
    #     batch_size, time_steps, _ = X.shape
    #     dWxh = np.zeros_like(self.Wxh)
    #     dWhh = np.zeros_like(self.Whh)
    #     dbh = np.zeros_like(self.bh)
    #     d_h_next = np.zeros((batch_size, self.hidden_size))

    #     # Backpropagation through time
    #     for t in reversed(range(time_steps)):
    #         h = self.last_hs[t]
    #         h_prev = self.last_hs[t-1]
    #         # Total gradient at current time step
    #         dh = d_out[:, t, :] + d_h_next
    #         # Derivative of tanh activation
    #         dtanh = (1 - h * h) * dh
    #         dWxh += np.dot(X[:, t, :].T, dtanh)
    #         dWhh += np.dot(h_prev.T, dtanh)
    #         dbh += np.sum(dtanh, axis=0, keepdims=True)
    #         d_h_next = np.dot(dtanh, self.Whh.T)

    #     # Store gradients
    #     self.weight_gradients = {"Wxh": dWxh, "Whh": dWhh, "bh": dbh}
    #     # (Optionally, update weights here or do it externally with an optimizer)
    #     # For example:
    #     # self.Wxh -= learning_rate * dWxh
    #     # self.Whh -= learning_rate * dWhh
    #     # self.bh -= learning_rate * dbh
    #     return d_h_next  # This could be used to propagate gradients to earlier layers
