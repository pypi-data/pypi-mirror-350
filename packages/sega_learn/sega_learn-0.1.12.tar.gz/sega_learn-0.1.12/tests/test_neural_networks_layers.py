import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.neural_networks import *
from tests.utils import BaseTest


class TestDenseLayer(BaseTest):
    """Comprehensive test suite for DenseLayer class.

    Tests initialization, forward pass, and backward pass functionalities.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting DenseLayer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        self.input_size = 10
        self.output_size = 5
        self.layer = DenseLayer(self.input_size, self.output_size, activation="relu")
        np.random.seed(42)

    ### Initialization Tests ###
    def test_initialization(self):
        """Test layer initialization with correct shapes and He initialization."""
        self.assertEqual(self.layer.weights.shape, (self.input_size, self.output_size))
        self.assertEqual(self.layer.biases.shape, (1, self.output_size))
        # Check He initialization for ReLU
        expected_scale = np.sqrt(2.0 / self.input_size)
        weights = self.layer.weights
        self.assertTrue(np.all(weights < 3 * expected_scale))
        self.assertTrue(np.all(weights > -3 * expected_scale))
        # Verify biases are initialized to zeros
        np.testing.assert_array_equal(
            self.layer.biases, np.zeros((1, self.output_size))
        )

    ### Forward Pass Tests ###
    def test_forward(self):
        """Test the forward pass with ReLU activation."""
        X = np.random.randn(3, self.input_size)
        output = self.layer.forward(X)
        self.assertEqual(output.shape, (3, self.output_size))
        # Manually compute expected output
        Z = np.dot(X, self.layer.weights) + self.layer.biases
        expected_output = np.maximum(0, Z)  # ReLU activation
        np.testing.assert_array_almost_equal(output, expected_output)

    ### Backward Pass Tests ###
    def test_backward(self):
        """Test the backward pass with gradient computations."""
        X = np.random.randn(3, self.input_size)
        self.layer.forward(X)  # Cache input and output
        dA = np.random.randn(3, self.output_size)
        dA_prev = self.layer.backward(dA, reg_lambda=0)
        self.assertEqual(dA_prev.shape, (3, self.input_size))
        # Manually compute expected gradients
        Z = np.dot(X, self.layer.weights) + self.layer.biases
        _output = np.maximum(0, Z)
        dZ = dA * (Z > 0)  # ReLU derivative
        dW = np.dot(X.T, dZ) / 3  # m=3 (batch size)
        db = np.sum(dZ, axis=0, keepdims=True) / 3
        dA_prev_expected = np.dot(dZ, self.layer.weights.T)
        np.testing.assert_array_almost_equal(self.layer.weight_gradients, dW)
        np.testing.assert_array_almost_equal(self.layer.bias_gradients, db)
        np.testing.assert_array_almost_equal(dA_prev, dA_prev_expected)

    ### Edge Case Tests ###
    def test_forward_with_zeros(self):
        """Test forward pass with zero input."""
        X = np.zeros((3, self.input_size))
        output = self.layer.forward(X)
        self.assertEqual(output.shape, (3, self.output_size))
        np.testing.assert_array_equal(output, np.zeros((3, self.output_size)))

    def test_backward_with_zeros(self):
        """Test backward pass with zero gradients."""
        X = np.random.randn(3, self.input_size)
        self.layer.forward(X)
        dA = np.zeros((3, self.output_size))
        dA_prev = self.layer.backward(dA, reg_lambda=0)
        self.assertEqual(dA_prev.shape, (3, self.input_size))
        np.testing.assert_array_equal(dA_prev, np.zeros((3, self.input_size)))

    ### Activation Function Tests ###
    def test_activation_function_relu(self):
        """Test ReLU activation function."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="relu")
        X = np.array([[1, -1], [2, -2]])
        output = self.layer.activate(X)
        expected_output = np.array([[1, 0], [2, 0]])
        np.testing.assert_array_equal(output, expected_output)

    def test_activation_function_leaky_relu(self):
        """Test Leaky ReLU activation function."""
        self.layer = DenseLayer(
            self.input_size, self.output_size, activation="leaky_relu"
        )
        X = np.array([[1, -1], [2, -2]])
        output = self.layer.activate(X)
        expected_output = np.array([[1, -0.01], [2, -0.02]])
        np.testing.assert_array_almost_equal(output, expected_output, decimal=5)

    def test_activation_function_sigmoid(self):
        """Test Sigmoid activation function."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="sigmoid")
        X = np.array([[0, 0], [1, 1]])
        output = self.layer.activate(X)
        expected_output = 1 / (1 + np.exp(-X))
        np.testing.assert_array_almost_equal(output, expected_output, decimal=5)

    def test_activation_function_tanh(self):
        """Test Tanh activation function."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="tanh")
        X = np.array([[0, 0], [1, 1]])
        output = self.layer.activate(X)
        expected_output = np.tanh(X)
        np.testing.assert_array_almost_equal(output, expected_output, decimal=5)

    def test_activation_function_softmax(self):
        """Test Softmax activation function."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="softmax")
        X = np.array([[1, 2], [3, 4]])
        output = self.layer.activate(X)
        expected_output = np.exp(X) / np.sum(np.exp(X), axis=1, keepdims=True)
        np.testing.assert_array_almost_equal(output, expected_output, decimal=5)

    def test_activation_function_none(self):
        """Test None activation function."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="none")
        X = np.array([[1, 2], [3, 4]])
        output = self.layer.activate(X)
        expected_output = X
        np.testing.assert_array_equal(output, expected_output)

    def test_activation_function_lineaar(self):
        """Test linear activation function."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="linear")
        X = np.array([[1, 2], [3, 4]])
        output = self.layer.activate(X)
        expected_output = X
        np.testing.assert_array_equal(output, expected_output)

    def test_activation_function_invalid(self):
        """Test invalid activation function."""
        with self.assertRaises(ValueError):
            self.layer = DenseLayer(
                self.input_size, self.output_size, activation="invalid"
            )
            X = np.array([[1, 2], [3, 4]])
            self.layer.activate(X)

    ### Activation Derivative Tests ###
    def test_relu_derivative(self):
        """Test ReLU activation derivative."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="relu")
        Z = np.array([[1, -1], [0, 2]])
        expected_derivative = np.array([[1, 0], [0, 1]])
        np.testing.assert_array_equal(
            self.layer.activation_derivative(Z), expected_derivative
        )

    def test_leaky_relu_derivative(self):
        """Test Leaky ReLU activation derivative."""
        self.layer = DenseLayer(
            self.input_size, self.output_size, activation="leaky_relu"
        )
        Z = np.array([[1, -1], [0, 2]])
        expected_derivative = np.array([[1, 0.01], [0.01, 1]])
        np.testing.assert_array_almost_equal(
            self.layer.activation_derivative(Z), expected_derivative, decimal=5
        )

    def test_sigmoid_derivative(self):
        """Test Sigmoid activation derivative."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="sigmoid")
        Z = np.array([[0, 1], [-1, 2]])
        sigmoid = 1 / (1 + np.exp(-Z))
        expected_derivative = sigmoid * (1 - sigmoid)
        np.testing.assert_array_almost_equal(
            self.layer.activation_derivative(Z), expected_derivative, decimal=5
        )

    def test_tanh_derivative(self):
        """Test Tanh activation derivative."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="tanh")
        Z = np.array([[0, 1], [-1, 2]])
        tanh = np.tanh(Z)
        expected_derivative = 1 - tanh**2
        np.testing.assert_array_almost_equal(
            self.layer.activation_derivative(Z), expected_derivative, decimal=5
        )

    def test_softmax_derivative(self):
        """Test Softmax activation derivative."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="softmax")
        Z = np.array([[1, 2], [3, 4]])
        softmax = np.exp(Z) / np.sum(np.exp(Z), axis=1, keepdims=True)
        expected_derivative = np.ones_like(
            softmax
        )  # Softmax derivative is handled in loss
        np.testing.assert_array_equal(
            self.layer.activation_derivative(Z), expected_derivative
        )

    def test_linear_derivative(self):
        """Test Linear activation derivative."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="linear")
        Z = np.array([[1, 2], [3, 4]])
        expected_derivative = np.ones_like(Z)
        np.testing.assert_array_equal(
            self.layer.activation_derivative(Z), expected_derivative
        )

    def test_none_derivative(self):
        """Test None activation derivative."""
        self.layer = DenseLayer(self.input_size, self.output_size, activation="none")
        Z = np.array([[1, 2], [3, 4]])
        expected_derivative = np.ones_like(Z)
        np.testing.assert_array_equal(
            self.layer.activation_derivative(Z), expected_derivative
        )

    def test_invalid_activation_derivative(self):
        """Test invalid activation derivative."""
        with self.assertRaises(ValueError):
            self.layer = DenseLayer(
                self.input_size, self.output_size, activation="invalid"
            )
            Z = np.array([[1, 2], [3, 4]])
            self.layer.activation_derivative(Z)


class TestFlattenLayer(BaseTest):
    """Comprehensive test suite for FlattenLayer class.

    Tests forward and backward pass functionalities for flattening multi-dimensional inputs.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting FlattenLayer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        self.layer = FlattenLayer()
        np.random.seed(42)

    ### Forward Pass Tests ###
    def test_forward(self):
        """Test the forward pass flattens input correctly."""
        X = np.random.randn(2, 3, 4, 4)  # batch_size=2, channels=3, height=4, width=4
        output = self.layer.forward(X)
        self.assertEqual(output.shape, (2, 3 * 4 * 4))  # (2, 48)
        expected_output = X.reshape(2, -1)
        np.testing.assert_array_equal(output, expected_output)
        # Verify input shape is cached
        self.assertEqual(self.layer.input_shape, (3, 4, 4))

    ### Backward Pass Tests ###
    def test_backward(self):
        """Test the backward pass reshapes gradients correctly."""
        X = np.random.randn(2, 3, 4, 4)
        self.layer.forward(X)  # Cache input shape
        dA = np.random.randn(2, 3 * 4 * 4)
        dA_prev = self.layer.backward(dA)
        self.assertEqual(dA_prev.shape, (2, 3, 4, 4))
        expected_dA_prev = dA.reshape(2, 3, 4, 4)
        np.testing.assert_array_equal(dA_prev, expected_dA_prev)

    ### Edge Case Tests ###
    def test_forward_with_empty_input(self):
        """Test forward pass with empty input."""
        X = np.empty((0, 3, 4, 4))  # Empty batch
        output = self.layer.forward(X)
        self.assertEqual(output.shape, (0, 3 * 4 * 4))

    def test_backward_with_empty_input(self):
        """Test backward pass with empty gradients."""
        X = np.empty((0, 3, 4, 4))  # Empty batch
        self.layer.forward(X)
        dA = np.empty((0, 3 * 4 * 4))
        dA_prev = self.layer.backward(dA)
        self.assertEqual(dA_prev.shape, (0, 3, 4, 4))


class TestConvLayer(BaseTest):
    """Comprehensive test suite for ConvLayer class.

    Tests initialization, forward pass, and backward pass with convolution operations.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting ConvLayer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        self.in_channels = 1
        self.out_channels = 1
        self.kernel_size = 3
        self.stride = 1
        self.padding = 0
        self.layer = ConvLayer(
            self.in_channels,
            self.out_channels,
            self.kernel_size,
            self.stride,
            self.padding,
            activation="none",
        )
        # Set predictable weights and biases
        self.layer.weights = np.ones((1, 1, 3, 3))  # All weights are 1
        self.layer.biases = np.zeros((1, 1))
        np.random.seed(42)

    ### Initialization Tests ###
    def test_initialization(self):
        """Test layer initialization with correct shapes."""
        self.assertEqual(
            self.layer.weights.shape,
            (self.out_channels, self.in_channels, self.kernel_size, self.kernel_size),
        )
        self.assertEqual(self.layer.biases.shape, (self.out_channels, 1))

    ### Forward Pass Tests ###
    def test_forward(self):
        """Test the forward pass with a simple convolution."""
        X = np.array([[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]])  # 1 batch, 1 channel, 3x3
        output = self.layer.forward(X)
        self.assertEqual(output.shape, (1, 1, 1, 1))  # Output size: (1, 1, 1, 1)
        expected_output = np.array([[[[45]]]])  # Sum of all elements with 3x3 kernel
        np.testing.assert_array_equal(output, expected_output)

    ### Backward Pass Tests ###
    def test_backward(self):
        """Test the backward pass with gradient computations."""
        X = np.array([[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]])
        self.layer.forward(X)  # Cache input and intermediates
        d_out = np.array([[[[1]]]])  # Gradient from next layer
        dX = self.layer.backward(d_out)
        self.assertEqual(dX.shape, (1, 1, 3, 3))
        # With all-one weights and d_out=1, dX should be all ones
        expected_dX = np.ones((1, 1, 3, 3))
        np.testing.assert_array_equal(dX, expected_dX)
        # Weight gradients should equal the input X
        expected_dW = X
        np.testing.assert_array_equal(self.layer.weight_gradients, expected_dW)
        # Bias gradient should be the sum of d_out
        expected_db = np.array([[1]])
        np.testing.assert_array_equal(self.layer.bias_gradients, expected_db)

    ### Edge Case Tests ###
    def test_forward_with_single_pixel(self):
        """Test forward pass with a single pixel input."""
        X = np.array([[[[1]]]])  # 1 batch, 1 channel, 1x1
        self.layer = ConvLayer(1, 1, 1, stride=1, padding=0, activation="none")
        self.layer.weights = np.array([[[[2]]]])  # Single weight
        self.layer.biases = np.array([[1]])  # Single bias
        output = self.layer.forward(X)
        self.assertEqual(output.shape, (1, 1, 1, 1))
        np.testing.assert_array_equal(output, np.array([[[[3]]]]))  # 1*2 + 1 = 3

    def test_backward_with_single_pixel(self):
        """Test backward pass with a single pixel input."""
        X = np.array([[[[1]]]])  # 1 batch, 1 channel, 1x1
        self.layer = ConvLayer(1, 1, 1, stride=1, padding=0, activation="none")
        self.layer.weights = np.array([[[[2]]]])  # Single weight
        self.layer.biases = np.array([[1]])  # Single bias
        self.layer.forward(X)
        d_out = np.array([[[[1]]]])  # Gradient from next layer
        dX = self.layer.backward(d_out)
        self.assertEqual(dX.shape, (1, 1, 1, 1))
        np.testing.assert_array_equal(dX, np.array([[[[2]]]]))  # Gradient wrt input
        np.testing.assert_array_equal(self.layer.weight_gradients, np.array([[[[1]]]]))
        np.testing.assert_array_equal(self.layer.bias_gradients, np.array([[1]]))

    def test_forward_with_large_padding(self):
        """Test forward pass with large padding."""
        X = np.array([[[[1, 2], [3, 4]]]])  # 1 batch, 1 channel, 2x2
        self.layer = ConvLayer(1, 1, 2, stride=1, padding=2, activation="none")
        self.layer.weights = np.ones((1, 1, 2, 2))  # All weights are 1
        self.layer.biases = np.zeros((1, 1))
        output = self.layer.forward(X)
        self.assertEqual(output.shape, (1, 1, 5, 5))  # Larger output due to padding

    def test_backward_with_large_padding(self):
        """Test backward pass with large padding."""
        X = np.array([[[[1, 2], [3, 4]]]])  # 1 batch, 1 channel, 2x2
        self.layer = ConvLayer(1, 1, 2, stride=1, padding=2, activation="none")
        self.layer.weights = np.ones((1, 1, 2, 2))  # All weights are 1
        self.layer.biases = np.zeros((1, 1))
        self.layer.forward(X)
        d_out = np.ones((1, 1, 5, 5))  # Gradient from next layer
        dX = self.layer.backward(d_out)
        self.assertEqual(dX.shape, (1, 1, 2, 2))  # Input shape restored

    ### Helper Function Tests ###
    def test_im2col(self):
        """Test im2col function, which converts input to column format."""
        X = np.array([[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]])  # 1 batch, 1 channel, 3x3
        h_out = 1
        w_out = 1
        col = self.layer._im2col(X, h_out, w_out)
        expected_col = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9]]).reshape(
            1, 9, 1
        )  # Reshape to match im2col output
        np.testing.assert_array_equal(col, expected_col)

    def test_col2im(self):
        """Test col2im function, which reconstructs input from column format."""
        X = np.array([[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]])  # 1 batch, 1 channel, 3x3
        h_out = 2
        w_out = 2
        col = self.layer._im2col(X, h_out, w_out)
        reconstructed_X = self.layer._col2im(col, X.shape)
        np.testing.assert_array_equal(reconstructed_X, X)

    ### Activation Function Tests ###
    def test_activation_function_relu(self):
        """Test ReLU activation function."""
        self.layer = ConvLayer(2, 2, 3, 1, 0, activation="relu")
        X = np.array([[1, -1], [2, -2]])
        output = self.layer.activate(X)
        expected_output = np.array([[1, 0], [2, 0]])
        np.testing.assert_array_equal(output, expected_output)

    def test_activation_function_leaky_relu(self):
        """Test Leaky ReLU activation function."""
        self.layer = ConvLayer(2, 2, 3, 1, 0, activation="leaky_relu")
        X = np.array([[1, -1], [2, -2]])
        output = self.layer.activate(X)
        expected_output = np.array([[1, -0.01], [2, -0.02]])
        np.testing.assert_array_almost_equal(output, expected_output, decimal=5)

    def test_activation_function_sigmoid(self):
        """Test Sigmoid activation function."""
        self.layer = ConvLayer(2, 2, 3, 1, 0, activation="sigmoid")
        X = np.array([[0, 0], [1, 1]])
        output = self.layer.activate(X)
        expected_output = 1 / (1 + np.exp(-X))
        np.testing.assert_array_almost_equal(output, expected_output, decimal=5)

    def test_activation_function_tanh(self):
        """Test Tanh activation function."""
        self.layer = ConvLayer(2, 2, 3, 1, 0, activation="tanh")
        X = np.array([[0, 0], [1, 1]])
        output = self.layer.activate(X)
        expected_output = np.tanh(X)
        np.testing.assert_array_almost_equal(output, expected_output, decimal=5)

    def test_activation_function_softmax(self):
        """Test Softmax activation function."""
        self.layer = ConvLayer(2, 2, 3, 1, 0, activation="softmax")
        X = np.array([[1, 2], [3, 4]])
        output = self.layer.activate(X)
        expected_output = np.exp(X) / np.sum(np.exp(X), axis=1, keepdims=True)
        np.testing.assert_array_almost_equal(output, expected_output, decimal=5)

    def test_activation_function_none(self):
        """Test None activation function."""
        self.layer = ConvLayer(2, 2, 3, 1, 0, activation="none")
        X = np.array([[1, 2], [3, 4]])
        output = self.layer.activate(X)
        expected_output = X
        np.testing.assert_array_equal(output, expected_output)

    def test_activation_function_lineaar(self):
        """Test linear activation function."""
        self.layer = ConvLayer(2, 2, 3, 1, 0, activation="linear")
        X = np.array([[1, 2], [3, 4]])
        output = self.layer.activate(X)
        expected_output = X
        np.testing.assert_array_equal(output, expected_output)

    def test_activation_function_invalid(self):
        """Test invalid activation function."""
        with self.assertRaises(ValueError):
            self.layer = ConvLayer(2, 2, 3, 1, 0, activation="invalid")
            X = np.array([[1, 2], [3, 4]])
            self.layer.activate(X)


if __name__ == "__main__":
    unittest.main()
