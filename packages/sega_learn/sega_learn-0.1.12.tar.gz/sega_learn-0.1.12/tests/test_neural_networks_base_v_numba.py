import os
import sys
import unittest
import warnings

# Adjust sys.path to import from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from numba.core.errors import NumbaPendingDeprecationWarning
from sega_learn.neural_networks import *
from sega_learn.neural_networks.numba_utils import (
    apply_dropout_jit,
    compute_l2_reg,
    sum_axis0,
)
from sega_learn.neural_networks.numba_utils import (
    leaky_relu as leaky_relu_nb,
)
from sega_learn.neural_networks.numba_utils import (
    leaky_relu_derivative as leaky_relu_derivative_nb,
)
from sega_learn.neural_networks.numba_utils import (
    relu as relu_nb,
)
from sega_learn.neural_networks.numba_utils import (
    relu_derivative as relu_derivative_nb,
)
from sega_learn.neural_networks.numba_utils import (
    sigmoid as sigmoid_nb,
)
from sega_learn.neural_networks.numba_utils import (
    sigmoid_derivative as sigmoid_derivative_nb,
)
from sega_learn.neural_networks.numba_utils import (
    softmax as softmax_nb,
)
from sega_learn.neural_networks.numba_utils import (
    tanh as tanh_nb,
)
from sega_learn.neural_networks.numba_utils import (
    tanh_derivative as tanh_derivative_nb,
)
from tests.utils import BaseTest

# from tests.utils import suppress_print

os.environ["NUMBA_WARNINGS"] = "0"
warnings.filterwarnings("ignore", category=NumbaPendingDeprecationWarning)


def compare_activation_functions(func1, func2, tolerance, *args):
    """Compare two activation functions for equality within a tolerance."""
    output1 = func1(*args)
    output2 = func2(*args)

    return bool(np.allclose(output1, output2, atol=tolerance))


class TestNeuralNetworkBaseNumbaTrain(BaseTest):
    """Comprehensive test suite for comparing Numba and non-Numba Train Functions."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print(
            "\nTesting Comparing NeuralNetwork Base and Numba Train Functions...",
            end="",
            flush=True,
        )

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        self.tolerance = 1e-7

        # Generate random data
        sample_size = 100_000
        np.random.seed(0)
        self.X_train = np.random.randn(sample_size, 10)
        self.y_train = np.random.randint(0, 2, sample_size)
        self.X_val = np.random.randn(20, 10)
        self.y_val = np.random.randint(0, 2, 20)

        # Neural network configurations
        layer_sizes = [10, 5, 3, 2]
        dropout_rate = 0
        reg_lambda = 0
        activations = ["relu", "relu", "softmax"]

        # Initialize neural networks
        self.nn_numba = NumbaBackendNeuralNetwork(
            layer_sizes, dropout_rate, reg_lambda, activations, compile_numba=False
        )
        self.nn_no_numba = BaseBackendNeuralNetwork(
            layer_sizes, dropout_rate, reg_lambda, activations
        )

        # Models are initialized with the same parameters but receive different randomized weights and biases
        def set_weights_biases(nn_numba, nn_no_numba):
            # Set weights to the same values for comparison
            for i in range(len(nn_numba.weights)):
                nn_numba.weights[i] = np.random.randn(*nn_numba.weights[i].shape)
                nn_no_numba.weights[i] = nn_numba.weights[i].copy()

            # Set biases to the same values for comparison
            for i in range(len(nn_numba.biases)):
                nn_numba.biases[i] = np.random.randn(*nn_numba.biases[i].shape)
                nn_no_numba.biases[i] = nn_numba.biases[i].copy()

        set_weights_biases(self.nn_numba, self.nn_no_numba)

        def set_layer_weights_biases(nn_numba, nn_no_numba):
            for i in range(len(nn_numba.layers)):
                nn_numba.layers[i].weights = np.random.randn(
                    *nn_numba.layers[i].weights.shape
                )
                nn_no_numba.layers[i].weights = nn_numba.layers[i].weights.copy()

                nn_numba.layers[i].biases = np.random.randn(
                    *nn_numba.layers[i].biases.shape
                )
                nn_no_numba.layers[i].biases = nn_numba.layers[i].biases.copy()

        set_layer_weights_biases(self.nn_numba, self.nn_no_numba)

    ### Set Up Tests ###
    def test_weights_biases_initialization(self):
        """Test that weights and biases are initialized correctly."""
        # Assert equality of weights
        for w1, w2 in zip(self.nn_numba.weights, self.nn_no_numba.weights):
            self.assertTrue(np.array_equal(w1, w2), "Weights are not equal!")

        # Assert equality of biases
        for b1, b2 in zip(self.nn_numba.biases, self.nn_no_numba.biases):
            self.assertTrue(np.array_equal(b1, b2), "Biases are not equal!")

    def test_layer_weights_biases_initialization(self):
        """Test that layer weights and biases are initialized correctly."""
        # Assert equality of layer weights
        for l1, l2 in zip(self.nn_numba.layers, self.nn_no_numba.layers):
            self.assertTrue(
                np.array_equal(l1.weights, l2.weights), "Layer weights are not equal!"
            )
            self.assertTrue(
                np.array_equal(l1.biases, l2.biases), "Layer biases are not equal!"
            )

    # ### Forward and Backward Propagation Tests ###
    # def test_forward_propagation(self):
    #     """Test forward propagation of the neural network."""
    #     output_numba = self.nn_numba.forward(self.X_train)
    #     output_no_numba = self.nn_no_numba.forward(self.X_train)

    #     self.assertTrue(np.allclose(output_numba, output_no_numba, atol=self.tolerance))

    # def test_backward_propagation(self):
    #     """Test backward propagation of the neural network."""
    #     # Forward pass
    #     _output_numba = self.nn_numba.forward(self.X_train)
    #     _output_no_numba = self.nn_no_numba.forward(self.X_train)

    #     # Backward pass comparison
    #     self.nn_numba.backward(self.y_train)
    #     self.nn_no_numba.backward(self.y_train)

    #     # Layers gradients comparison
    #     for i in range(len(self.nn_numba.layers)):
    #         self.assertTrue(
    #             np.allclose(
    #                 self.nn_numba.layers[i].weight_gradients,
    #                 self.nn_no_numba.layers[i].weight_gradients,
    #                 atol=self.tolerance,
    #             )
    #         )
    #         self.assertTrue(
    #             np.allclose(
    #                 self.nn_numba.layers[i].bias_gradients,
    #                 self.nn_no_numba.layers[i].bias_gradients,
    #                 atol=self.tolerance,
    #             )
    #         )

    ### Evaluation and Prediction Tests ###
    def test_evaluate(self):
        """Test evaluation of the neural network."""
        # Evaluation comparison
        accuracy_numba, _ = self.nn_numba.evaluate(self.X_val, self.y_val)
        accuracy_no_numba, _ = self.nn_no_numba.evaluate(self.X_val, self.y_val)

        self.assertTrue(
            np.allclose(accuracy_numba, accuracy_no_numba, atol=self.tolerance)
        )

    def test_predict(self):
        """Test prediction of the neural network."""
        # Prediction comparison
        predictions_numba = self.nn_numba.predict(self.X_val)
        predictions_no_numba = self.nn_no_numba.predict(self.X_val)

        self.assertTrue(np.array_equal(predictions_numba, predictions_no_numba))


class TestNeuralNetworkBaseNumbaActivations(BaseTest):
    """Comprehensive test suite for comparing Numba and non-Numba Activations."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print(
            "\nTesting Comparing NeuralNetwork Base and Numba Activations...",
            end="",
            flush=True,
        )

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        np.random.seed(42)
        self.Z = np.random.randn(1000, 2)
        self.tolerance = 1e-7

    ### Activation Functions Tests ###
    def test_sigmoid(self):
        """Test sigmoid activation function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.sigmoid, sigmoid_nb, self.tolerance, self.Z
            )
        )

    def test_relu(self):
        """Test ReLU activation function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.relu, relu_nb, self.tolerance, self.Z
            )
        )

    def test_leaky_relu(self):
        """Test leaky ReLU activation function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.leaky_relu, leaky_relu_nb, self.tolerance, self.Z
            )
        )

    def test_tanh(self):
        """Test tanh activation function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.tanh, tanh_nb, self.tolerance, self.Z
            )
        )

    def test_softmax(self):
        """Test softmax activation function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.softmax, softmax_nb, self.tolerance, self.Z
            )
        )

    ### Derivative Functions Tests ###
    def test_sigmoid_derivative(self):
        """Test sigmoid derivative function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.sigmoid_derivative,
                sigmoid_derivative_nb,
                self.tolerance,
                self.Z,
            )
        )

    def test_relu_derivative(self):
        """Test ReLU derivative function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.relu_derivative, relu_derivative_nb, self.tolerance, self.Z
            )
        )

    def test_leaky_relu_derivative(self):
        """Test leaky ReLU derivative function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.leaky_relu_derivative,
                leaky_relu_derivative_nb,
                self.tolerance,
                self.Z,
            )
        )

    def test_tanh_derivative(self):
        """Test tanh derivative function."""
        self.assertTrue(
            compare_activation_functions(
                Activation.tanh_derivative, tanh_derivative_nb, self.tolerance, self.Z
            )
        )


class TestNeuralNetworkBaseNumbaLoss(BaseTest):
    """Comprehensive test suite for comparing Numba and non-Numba Loss Functions."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print(
            "\nTesting Comparing NeuralNetwork Base and Numba Loss Functions...",
            end="",
            flush=True,
        )

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        np.random.seed(42)
        self.Z = np.random.randn(1000, 2)
        self.tolerance = 1e-7

    ### Cross-Entropy Loss Tests ###
    def test_cross_entropy_loss(self):
        """Test Cross Entropy Loss."""
        n_samples, n_classes = 5, 3
        logits_ce = np.random.randn(n_samples, n_classes)
        targets_int = np.random.randint(0, n_classes, size=n_samples)
        targets_onehot = np.eye(n_classes)[targets_int]

        base_ce_loss = CrossEntropyLoss()
        jit_ce_loss = JITCrossEntropyLoss()

        loss_base_ce = base_ce_loss(logits_ce, targets_onehot)
        loss_jit_ce = jit_ce_loss.calculate_loss(logits_ce, targets_onehot)

        self.assertTrue(np.allclose(loss_base_ce, loss_jit_ce, atol=self.tolerance))

    def test_binary_cross_entropy_loss(self):
        """Test Binary Cross Entropy Loss."""
        n_samples_bce = 10
        logits_bce = np.random.randn(n_samples_bce)
        targets_bce = np.random.randint(0, 2, size=n_samples_bce)

        base_bce_loss = BCEWithLogitsLoss()
        jit_bce_loss = JITBCEWithLogitsLoss()

        loss_base_bce = base_bce_loss(logits_bce, targets_bce)
        loss_jit_bce = jit_bce_loss.calculate_loss(logits_bce, targets_bce)

        self.assertTrue(np.allclose(loss_base_bce, loss_jit_bce, atol=self.tolerance))

    def test_mean_squared_error_loss(self):
        """Test Mean Squared Error Loss."""
        n_samples, n_features = 10, 5
        logits_mse = np.random.randn(n_samples, n_features)
        targets_mse = np.random.randn(n_samples, n_features)

        base_mse_loss = MeanSquaredErrorLoss()
        jit_mse_loss = JITMeanSquaredErrorLoss()

        loss_base_mse = base_mse_loss(logits_mse, targets_mse)
        loss_jit_mse = jit_mse_loss.calculate_loss(logits_mse, targets_mse)

        self.assertTrue(np.allclose(loss_base_mse, loss_jit_mse, atol=self.tolerance))

    def test_mean_absolute_error_loss(self):
        """Test Mean Absolute Error Loss."""
        n_samples, n_features = 10, 5
        logits_mae = np.random.randn(n_samples, n_features)
        targets_mae = np.random.randn(n_samples, n_features)

        base_mae_loss = MeanAbsoluteErrorLoss()
        jit_mae_loss = JITMeanAbsoluteErrorLoss()

        loss_base_mae = base_mae_loss(logits_mae, targets_mae)
        loss_jit_mae = jit_mae_loss.calculate_loss(logits_mae, targets_mae)

        self.assertTrue(np.allclose(loss_base_mae, loss_jit_mae, atol=self.tolerance))

    def test_huber_loss(self):
        """Test Huber Loss."""
        n_samples, n_features = 10, 5
        logits_huber = np.random.randn(n_samples, n_features)
        targets_huber = np.random.randn(n_samples, n_features)

        base_huber_loss = HuberLoss()
        jit_huber_loss = JITHuberLoss()

        loss_base_huber = base_huber_loss(logits_huber, targets_huber)
        loss_jit_huber = jit_huber_loss.calculate_loss(logits_huber, targets_huber)

        self.assertTrue(
            np.allclose(loss_base_huber, loss_jit_huber, atol=self.tolerance)
        )


class TestNeuralNetworkBaseNumbaUtils(BaseTest):
    """Comprehensive test suite for comparing Numba and non-Numba Utilities."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print(
            "\nTesting Comparing NeuralNetwork Base and Numba Utilities...",
            end="",
            flush=True,
        )

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        np.random.seed(42)
        self.X = np.random.randn(1000, 1000)
        self.tolerance = 1e-7

    def test_sum_axis0(self):
        """Test sum_axis0 function."""
        self.assertTrue(
            np.allclose(
                sum_axis0(self.X),
                np.sum(self.X, axis=0, keepdims=True),
                atol=self.tolerance,
            )
        )

    def test_apply_dropout(self):
        """Test apply_dropout against apply_dropout_jit."""
        layer_sizes = [10, 5, 3, 2]
        dropout_rate = 0.5
        reg_lambda = 0
        activations = ["relu", "relu", "softmax", "sigmoid", "tanh", "none", "linear"]
        nn = BaseBackendNeuralNetwork(
            layer_sizes, dropout_rate, reg_lambda, activations
        )

        counts_base = []
        counts_jit = []
        n_trials = 10_000
        for _ in range(n_trials):
            X = np.random.randn(1000, 5)
            X_dropout = nn.apply_dropout(X)
            X_dropout_jit = apply_dropout_jit(X, dropout_rate)

            counts_base.append(np.count_nonzero(X_dropout))
            counts_jit.append(np.count_nonzero(X_dropout_jit))

        avg_count_base = np.mean(counts_base)
        avg_count_jit = np.mean(counts_jit)
        std_dev_base = np.std(counts_base)
        std_dev_jit = np.std(counts_jit)

        self.assertTrue(np.isclose(avg_count_base, avg_count_jit, atol=1.0))
        self.assertTrue(np.isclose(std_dev_base, std_dev_jit, atol=1.0))

    def test_compute_l2_reg(self):
        """Test compute_l2_reg against the base implementation."""
        weights = [np.random.randn(5, 5) for _ in range(10)]
        activations = ["relu" for _ in range(10)]
        layer_sizes = [5] * 10
        dropout_rate = 0.5
        reg_lambda = 0
        nn = BaseBackendNeuralNetwork(
            layer_sizes, dropout_rate, reg_lambda, activations
        )

        # Catch and suppress the warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            l2_base = nn.compute_l2_reg(weights)
            l2_jit = compute_l2_reg(weights)

        self.assertTrue(np.isclose(l2_base, l2_jit, atol=self.tolerance))


class TestNeuralNetworkBaseNumbaOptimizers(BaseTest):
    """Comprehensive test suite for comparing Numba and non-Numba Optimizers."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print(
            "\nTesting Comparing NeuralNetwork Base and Numba Optimizers...",
            end="",
            flush=True,
        )

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        self.num_layers = 5
        self.tolerance = 1e-7
        np.random.seed(42)

        self.lr = 0.01
        self.rho = 0.95
        self.beta1 = 0.5
        self.beta2 = 0.9
        self.epsilon = 1e-5
        self.momentum = 0.9
        self.reg_lambda = 0.01
        self.activations = ["relu"] * self.num_layers

        # Catch and suppress warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            self.base_layers = [DenseLayer(3, 3, act) for act in self.activations]
            self.jit_layers = [JITDenseLayer(3, 3, act) for act in self.activations]

            # Initialize Adam optimizers
            self.adam_base = AdamOptimizer(
                self.lr, self.beta1, self.beta2, self.epsilon, self.reg_lambda
            )
            self.adam_jit = JITAdamOptimizer(
                self.lr, self.beta1, self.beta2, self.epsilon, self.reg_lambda
            )
            self.adam_base.initialize(self.base_layers)
            self.adam_jit.initialize(self.jit_layers)

            # Initialize SGD optimizers
            self.sgd_base = SGDOptimizer(self.lr, self.momentum, self.reg_lambda)
            self.sgd_jit = JITSGDOptimizer(self.lr, self.momentum, self.reg_lambda)
            self.sgd_base.initialize(self.base_layers)
            self.sgd_jit.initialize(self.jit_layers)

            # Initialize Adadelta optimizers
            self.adadelta_base = AdadeltaOptimizer(
                self.lr, self.rho, self.epsilon, self.reg_lambda
            )
            self.adadelta_jit = JITAdadeltaOptimizer(
                self.lr, self.rho, self.epsilon, self.reg_lambda
            )
            self.adadelta_base.initialize(self.base_layers)
            self.adadelta_jit.initialize(self.jit_layers)

    def test_adam_optimizer_initial_values(self):
        """Test that the initial values of m, v, and t are the same for both optimizers."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for _ in range(self.num_layers):
                self.assertTrue(np.allclose(self.adam_base.m, self.adam_jit.m))
                self.assertTrue(np.allclose(self.adam_base.v, self.adam_jit.v))
                self.assertEqual(self.adam_base.t, self.adam_jit.t)

    def test_adam_optimizer_weights_biases_update(self):
        """Test that weights and biases are updated correctly for both optimizers."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for i in range(self.num_layers):
                self.jit_layers[i].weights = self.base_layers[i].weights

            dW = [np.random.randn(3, 3) for _ in range(self.num_layers)]
            db = [np.random.randn(3) for _ in range(self.num_layers)]
            for i in range(self.num_layers):
                self.adam_base.update(self.base_layers[i], dW[i], db[i], i)
            self.adam_jit.update_layers(self.jit_layers, dW, db)

            for i in range(self.num_layers):
                self.assertTrue(
                    np.allclose(
                        self.base_layers[i].weights,
                        self.jit_layers[i].weights,
                        atol=self.tolerance,
                    )
                )
                self.assertTrue(
                    np.allclose(
                        self.base_layers[i].biases,
                        self.jit_layers[i].biases,
                        atol=self.tolerance,
                    )
                )

    def test_sgd_optimizer_initial_values(self):
        """Test that the initial values of m and v are the same for both optimizers."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for _ in range(self.num_layers):
                self.assertTrue(
                    np.allclose(self.sgd_base.velocity, self.sgd_jit.velocity)
                )

    def test_sgd_optimizer_weights_biases_update(self):
        """Test that weights and biases are updated correctly for both optimizers."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for i in range(self.num_layers):
                self.jit_layers[i].weights = self.base_layers[i].weights

            dW = [np.random.randn(3, 3) for _ in range(self.num_layers)]
            db = [np.random.randn(3) for _ in range(self.num_layers)]
            for i in range(self.num_layers):
                self.sgd_base.update(self.base_layers[i], dW[i], db[i], i)
            self.sgd_jit.update_layers(self.jit_layers, dW, db)

            for i in range(self.num_layers):
                self.assertTrue(
                    np.allclose(
                        self.base_layers[i].weights,
                        self.jit_layers[i].weights,
                        atol=self.tolerance,
                    )
                )
                self.assertTrue(
                    np.allclose(
                        self.base_layers[i].biases,
                        self.jit_layers[i].biases,
                        atol=self.tolerance,
                    )
                )

    def test_adadelta_optimizer_initial_values(self):
        """Test that the initial values of E_g2, E_delta_x2 are the same for both optimizers."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for _ in range(self.num_layers):
                self.assertTrue(
                    np.allclose(self.adadelta_base.E_g2, self.adadelta_jit.E_g2)
                )
                self.assertTrue(
                    np.allclose(
                        self.adadelta_base.E_delta_x2, self.adadelta_jit.E_delta_x2
                    )
                )

    def test_adadelta_optimizer_weights_biases_update(self):
        """Test that weights and biases are updated correctly for both optimizers."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for i in range(self.num_layers):
                self.jit_layers[i].weights = self.base_layers[i].weights

            dW = [np.random.randn(3, 3) for _ in range(self.num_layers)]
            db = [np.random.randn(3) for _ in range(self.num_layers)]
            for i in range(self.num_layers):
                self.adadelta_base.update(self.base_layers[i], dW[i], db[i], i)
            self.adadelta_jit.update_layers(self.jit_layers, dW, db)

            for i in range(self.num_layers):
                self.assertTrue(
                    np.allclose(
                        self.base_layers[i].weights,
                        self.jit_layers[i].weights,
                        atol=self.tolerance,
                    )
                )
                self.assertTrue(
                    np.allclose(
                        self.base_layers[i].biases,
                        self.jit_layers[i].biases,
                        atol=self.tolerance,
                    )
                )


if __name__ == "__main__":
    unittest.main()
