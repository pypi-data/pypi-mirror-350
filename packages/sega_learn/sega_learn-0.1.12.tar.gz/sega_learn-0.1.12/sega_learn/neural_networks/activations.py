import numpy as np


class Activation:
    """This class contains various activation functions and their corresponding derivatives for use in neural networks.

    Methods:
        relu: Rectified Linear Unit activation function. Returns the input directly if it's positive, otherwise returns 0.
        leaky_relu: Leaky ReLU activation function. A variant of ReLU that allows a small gradient when the input is negative.
        tanh: Hyperbolic tangent activation function. Maps input to range [-1, 1]. Commonly used for normalized input.
        sigmoid: Sigmoid activation function. Maps input to range [0, 1]. Commonly used for binary classification.
        softmax: Softmax activation function. Maps input into a probability distribution over multiple classes.
    """

    @staticmethod
    def relu(z):
        """ReLU (Rectified Linear Unit) activation function: f(z) = max(0, z).

        Returns the input directly if it's positive, otherwise returns 0.
        """
        return np.maximum(0, z)

    @staticmethod
    def relu_derivative(z):
        """Derivative of the ReLU function: f'(z) = 1 if z > 0, else 0.

        Returns 1 for positive input, and 0 for negative input.
        """
        return (z > 0).astype(np.float32)

    @staticmethod
    def leaky_relu(z, alpha=0.01):
        """Leaky ReLU activation function: f(z) = z if z > 0, else alpha * z.

        Allows a small, non-zero gradient when the input is negative to address the dying ReLU problem.
        """
        return np.where(z > 0, z, alpha * z)

    @staticmethod
    def leaky_relu_derivative(z, alpha=0.01):
        """Derivative of the Leaky ReLU function: f'(z) = 1 if z > 0, else alpha.

        Returns 1 for positive input, and alpha for negative input.
        """
        return np.where(z > 0, 1, alpha)

    @staticmethod
    def tanh(z):
        """Hyperbolic tangent (tanh) activation function: f(z) = (exp(z) - exp(-z)) / (exp(z) + exp(-z)).

        Maps input to the range [-1, 1], typically used for normalized input.
        """
        return np.tanh(z)

    @staticmethod
    def tanh_derivative(z):
        """Derivative of the tanh function: f'(z) = 1 - tanh(z)^2.

        Used for backpropagation through the tanh activation.
        """
        return 1 - np.tanh(z) ** 2

    @staticmethod
    def sigmoid(z):
        """Sigmoid activation function: f(z) = 1 / (1 + exp(-z)).

        Maps input to the range [0, 1], commonly used for binary classification.
        """
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def sigmoid_derivative(z):
        """Derivative of the sigmoid function: f'(z) = sigmoid(z) * (1 - sigmoid(z)).

        Used for backpropagation through the sigmoid activation.
        """
        sig = Activation.sigmoid(z)
        return sig * (1 - sig)

    @staticmethod
    def softmax(z):
        """Softmax activation function: f(z)_i = exp(z_i) / sum(exp(z_j)) for all j.

        Maps input into a probability distribution over multiple classes. Used for multiclass classification.
        """
        # Subtract the max value from each row to prevent overflow (numerical stability)
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
