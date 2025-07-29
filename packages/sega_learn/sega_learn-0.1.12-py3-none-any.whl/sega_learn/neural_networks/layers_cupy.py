import cupy as cp


class CuPyDenseLayer:
    """Initializes a Layer object.

    Args:
        input_size (int): The size of the input to the layer.
        output_size (int): The size of the output from the layer.
        activation (str): The activation function to be used in the layer.
    """

    def __init__(self, input_size, output_size, activation="relu"):
        """Initializes the layer with weights, biases, and activation function.

        Args:
            input_size: (int) - The number of input features to the layer.
            output_size: (int) - The number of output features from the layer.
            activation: (str), optional - The activation function to use (default is "relu").
            Supported values: "relu", "leaky_relu", or others.

        Attributes:
            weights: (cp.ndarray) - The weight matrix initialized using He initialization for "relu" or "leaky_relu".
            biases: (cp.ndarray) - The bias vector initialized to zeros.
            weight_gradients: (cp.ndarray) - Gradients of the weights, initialized to zeros.
            bias_gradients: (cp.ndarray) - Gradients of the biases, initialized to zeros.
            input_size: (int) - The number of input features to the layer.
            output_size: (int) - The number of output features from the layer.
            activation: (str) - The activation function used in the layer.
        """
        # He initialization for weights
        if activation in ["relu", "leaky_relu"]:
            scale = cp.sqrt(2.0 / input_size)
        else:
            scale = cp.sqrt(1.0 / input_size)

        self.weights = cp.random.randn(input_size, output_size) * scale
        self.biases = cp.zeros((1, output_size))
        self.weight_gradients = cp.zeros(
            (input_size, output_size)
        )  # Initialize weight gradients to zeros
        self.bias_gradients = cp.zeros(
            (1, output_size)
        )  # Initialize bias gradients to zeros

        self.input_size = input_size
        self.output_size = output_size
        self.activation = activation

    def zero_grad(self):
        """Reset the gradients of the weights and biases to zero."""
        self.weight_gradients = cp.zeros_like(self.weight_gradients)
        self.bias_gradients = cp.zeros_like(self.bias_gradients)

    def activate(self, Z):
        """Apply activation function."""
        activation_functions = {
            "relu": CuPyActivation.relu,
            "leaky_relu": CuPyActivation.leaky_relu,
            "tanh": CuPyActivation.tanh,
            "sigmoid": CuPyActivation.sigmoid,
            "softmax": CuPyActivation.softmax,
        }

        if self.activation in activation_functions:
            return activation_functions[self.activation](Z)
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")

    def activation_derivative(self, Z):
        """Apply activation derivative."""
        if self.activation == "relu":
            return CuPyActivation.relu_derivative(Z)
        elif self.activation == "leaky_relu":
            return CuPyActivation.leaky_relu_derivative(Z)
        elif self.activation == "tanh":
            return CuPyActivation.tanh_derivative(Z)
        elif self.activation == "sigmoid":
            return CuPyActivation.sigmoid_derivative(Z)
        elif self.activation == "softmax":
            # Softmax derivative handled in loss function
            return cp.ones_like(Z)  # Identity for compatibility
        else:
            raise ValueError(f"Unsupported activation: {self.activation}")


class CuPyActivation:
    """Activation functions for neural networks using CuPy."""

    @staticmethod
    def relu(z):
        """ReLU (Rectified Linear Unit) activation function: f(z) = max(0, z).

        Returns the input directly if it's positive, otherwise returns 0.
        """
        return cp.maximum(0, z)

    @staticmethod
    def relu_derivative(z):
        """Derivative of the ReLU function: f'(z) = 1 if z > 0, else 0.

        Returns 1 for positive input, and 0 for negative input.
        """
        return (z > 0).astype(cp.float32)

    @staticmethod
    def leaky_relu(z, alpha=0.01):
        """Leaky ReLU activation function: f(z) = z if z > 0, else alpha * z.

        Allows a small, non-zero gradient when the input is negative to address the dying ReLU problem.
        """
        return cp.where(z > 0, z, alpha * z)

    @staticmethod
    def leaky_relu_derivative(z, alpha=0.01):
        """Derivative of the Leaky ReLU function: f'(z) = 1 if z > 0, else alpha.

        Returns 1 for positive input, and alpha for negative input.
        """
        return cp.where(z > 0, 1, alpha)

    @staticmethod
    def tanh(z):
        """Hyperbolic tangent (tanh) activation function: f(z) = (exp(z) - exp(-z)) / (exp(z) + exp(-z)).

        Maps input to the range [-1, 1], typically used for normalized input.
        """
        return cp.tanh(z)

    @staticmethod
    def tanh_derivative(z):
        """Derivative of the tanh function: f'(z) = 1 - tanh(z)^2.

        Used for backpropagation through the tanh activation.
        """
        return 1 - cp.tanh(z) ** 2

    @staticmethod
    def sigmoid(z):
        """Sigmoid activation function: f(z) = 1 / (1 + exp(-z)).

        Maps input to the range [0, 1], commonly used for binary classification.
        """
        return 1 / (1 + cp.exp(-z))

    @staticmethod
    def sigmoid_derivative(z):
        """Derivative of the sigmoid function: f'(z) = sigmoid(z) * (1 - sigmoid(z)).

        Used for backpropagation through the sigmoid activation.
        """
        sig = CuPyActivation.sigmoid(z)
        return sig * (1 - sig)

    @staticmethod
    def softmax(z):
        """Softmax activation function: f(z)_i = exp(z_i) / sum(exp(z_j)) for all j.

        Maps input into a probability distribution over multiple classes. Used for multiclass classification.
        """
        # Subtract the max value from each row to prevent overflow (numerical stability)
        exp_z = cp.exp(z - cp.max(z, axis=1, keepdims=True))
        return exp_z / cp.sum(exp_z, axis=1, keepdims=True)
