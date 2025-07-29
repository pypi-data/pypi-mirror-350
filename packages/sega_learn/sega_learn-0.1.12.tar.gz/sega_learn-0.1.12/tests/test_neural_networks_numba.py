import os
import sys
import unittest
import warnings

# Adjust sys.path to import from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from numba.core.errors import NumbaPendingDeprecationWarning
from sega_learn.neural_networks import *
from tests.utils import BaseTest, suppress_print

os.environ["NUMBA_WARNINGS"] = "0"
warnings.filterwarnings("ignore", category=NumbaPendingDeprecationWarning)


class TestNeuralNetworkNumba(BaseTest):
    """Comprehensive test suite for NumbaBackendNeuralNetwork class.

    Tests all major functions and edge cases under Numba acceleration.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting NeuralNetwork class with Numba backend", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize test fixtures."""
        with suppress_print():
            # Binary classification network
            self.nn_binary = NumbaBackendNeuralNetwork(
                [2, 10, 5, 1],
                dropout_rate=0.1,
                reg_lambda=0.01,
                compile_numba=False,
                progress_bar=False,
            )
            # Multi-class classification network
            self.nn_multi = NumbaBackendNeuralNetwork(
                [2, 10, 5, 3],
                dropout_rate=0.1,
                reg_lambda=0.01,
                compile_numba=False,
                progress_bar=False,
            )
            # Regression network
            self.nn_regressor = NumbaBackendNeuralNetwork(
                [2, 10, 5, 1],
                dropout_rate=0.1,
                reg_lambda=0.01,
                compile_numba=False,
                regressor=True,
                loss_function=JITMeanSquaredErrorLoss(),
                progress_bar=False,
            )
        self.optimizer = JITAdamOptimizer(learning_rate=0.01)
        np.random.seed(42)
        self.X = np.random.randn(50, 2).astype(np.float64)
        self.y_binary = np.random.randint(0, 2, (50, 1)).astype(np.float64)
        self.y_multi = np.random.randint(0, 3, (50,)).astype(np.int32)
        self.y_reg = (np.random.randn(50, 1) * 5 + 2).astype(np.float64)

    ### Initialization Tests ###
    def test_initial_numba_compilation(self):
        """Test Numba compilation of initial network."""
        nn = NumbaBackendNeuralNetwork(
            [2, 10, 1], compile_numba=True, progress_bar=False
        )
        self.assertTrue(nn.compiled)

    def test_initialization(self):
        """Test layer initialization with custom sizes and activations."""
        nn = NumbaBackendNeuralNetwork(
            [3, 4, 2],
            activations=["tanh", "sigmoid"],
            compile_numba=False,
            progress_bar=False,
        )
        self.assertEqual(len(nn.layers), 2)
        self.assertEqual(nn.layers[0].activation, "tanh")
        self.assertEqual(nn.layers[1].activation, "sigmoid")
        self.assertEqual(nn.layers[0].weights.shape, (3, 4))
        self.assertEqual(nn.layers[1].weights.shape, (4, 2))
        self.assertEqual(nn.layers[0].biases.shape, (1, 4))
        self.assertEqual(nn.layers[1].biases.shape, (1, 2))

    def test_default_activations(self):
        """Test default activation settings."""
        nn = NumbaBackendNeuralNetwork(
            [3, 4, 5, 2], compile_numba=False, progress_bar=False
        )
        self.assertEqual(nn.activations, ["relu", "relu", "softmax"])

    def test_initialize_layers(self):
        """Test layer initialization."""
        layers = [JITDenseLayer(2, 4, "relu"), JITDenseLayer(4, 2, "sigmoid")]
        nn = BaseBackendNeuralNetwork(layers)
        self.assertEqual(len(nn.layers), 2)
        self.assertEqual(nn.layers[0].activation, "relu")
        self.assertEqual(nn.layers[1].activation, "sigmoid")
        self.assertEqual(nn.layers[0].weights.shape, (2, 4))
        self.assertEqual(nn.layers[1].weights.shape, (4, 2))
        self.assertEqual(nn.layers[0].biases.shape, (1, 4))
        self.assertEqual(nn.layers[1].biases.shape, (1, 2))

    def test_nonJIT_optimizer(self):
        """Test non-JIT optimizer conversion."""
        optimizer = AdamOptimizer(learning_rate=0.01)
        nn = NumbaBackendNeuralNetwork(
            [2, 100, 1], compile_numba=False, progress_bar=False
        )
        with self.assertWarns(UserWarning), suppress_print():
            nn.train(
                self.X,
                self.y_binary,
                optimizer=optimizer,
                epochs=1,
                batch_size=32,
                use_tqdm=False,
            )

    ### Dropout Tests ###
    def test_apply_dropout(self):
        """Test dropout application with Numba."""
        A = np.ones((100, 100))  # Increased size for better statistics
        A_dropped = self.nn_binary.apply_dropout(A)  # nn_binary has dropout_rate=0.1
        self.assertEqual(A.shape, A_dropped.shape)
        self.assertTrue(np.any(A_dropped == 0))
        non_zero_elements = A_dropped[A_dropped != 0]
        # Check scaling factor
        self.assertAlmostEqual(
            np.mean(non_zero_elements), 1 / (1 - self.nn_binary.dropout_rate), delta=0.1
        )
        num_zeros = np.sum(A_dropped == 0)
        total_elements = A_dropped.size
        self.assertAlmostEqual(
            num_zeros / total_elements,
            self.nn_binary.dropout_rate,
            delta=0.15,  # Increased delta
        )

    def test_apply_dropout_zero(self):
        """Test dropout with rate=0 (no dropout)."""
        nn = NumbaBackendNeuralNetwork(
            [2, 100, 1], dropout_rate=0, compile_numba=False, progress_bar=False
        )
        A = np.random.randn(10, 10)
        A_dropped = nn.apply_dropout(A)
        np.testing.assert_array_equal(A, A_dropped)

    ### Forward Pass Tests ###
    def test_forward_binary(self):
        """Test forward pass for binary classification with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            outputs = self.nn_binary.forward(self.X)
            self.assertEqual(outputs.shape, (50, 1))
            self.assertTrue(np.all(outputs >= 0) and np.all(outputs <= 1))

    def test_forward_multiclass(self):
        """Test forward pass for multi-class classification with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            outputs = self.nn_multi.forward(self.X)
            self.assertEqual(outputs.shape, (50, 3))
            self.assertTrue(np.allclose(np.sum(outputs, axis=1), 1.0, atol=1e-5))

    def test_forward_regression(self):
        """Test forward pass for regression with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            outputs = self.nn_regressor.forward(self.X)
            self.assertEqual(outputs.shape, (50, 1))
            # No activation constraint for regression output

    ### Backward Pass Test ###
    def test_backward(self):
        """Test backward pass gradient computation with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.nn_binary.forward(self.X)
            self.nn_binary.backward(self.y_binary)
            for layer in self.nn_binary.layers:
                dW, db = layer.weight_gradients, layer.bias_gradients
                self.assertEqual(dW.shape, layer.weights.shape)
                self.assertEqual(db.shape, layer.biases.shape)
                self.assertFalse(np.all(dW == 0))  # Ensure gradients are non-zero

    ### Training Tests ###
    def test_train(self):
        """Test basic training functionality with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with suppress_print():
                self.nn_binary.train(
                    self.X,
                    self.y_binary,
                    self.X,
                    self.y_binary,
                    self.optimizer,
                    epochs=1,
                    batch_size=32,
                    use_tqdm=False,
                )
            accuracy, predicted = self.nn_binary.evaluate(self.X, self.y_binary)
            loss = self.nn_binary.calculate_loss(self.X, self.y_binary)
            self.assertTrue(0 <= accuracy <= 1)
            self.assertGreater(loss, 0)

    def test_train_loss_decrease(self):
        """Test if loss decreases after a training step with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nn = NumbaBackendNeuralNetwork(
                [2, 10, 1],
                dropout_rate=0,
                reg_lambda=0,
                compile_numba=False,
                progress_bar=False,
            )
            optimizer = JITSGDOptimizer(learning_rate=0.1)
            X_small = np.array([[0.5, 0.5], [0.5, -0.5], [-0.5, 0.5], [-0.5, -0.5]])
            y_small = np.array([[1], [0], [0], [0]])
            initial_loss = nn.calculate_loss(X_small, y_small)
            with suppress_print():
                nn.train(
                    X_small,
                    y_small,
                    optimizer=optimizer,
                    epochs=1,
                    batch_size=4,
                    use_tqdm=False,
                    p=False,
                )
            final_loss = nn.calculate_loss(X_small, y_small)
            self.assertLessEqual(final_loss, initial_loss)

    def test_train_regression(self):
        """Test basic training functionality for regression with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with suppress_print():
                self.nn_regressor.train(
                    self.X,
                    self.y_reg,
                    self.X,
                    self.y_reg,
                    self.optimizer,
                    epochs=2,
                    batch_size=16,
                    use_tqdm=False,
                )
            metric, _predicted = self.nn_regressor.evaluate(
                self.X, self.y_reg
            )  # Metric is MSE by default
            loss = self.nn_regressor.calculate_loss(self.X, self.y_reg)
            self.assertIsInstance(metric, float)
            self.assertGreaterEqual(metric, 0)  # MSE >= 0
            self.assertGreater(loss, 0)

    ### Evaluation Test ###
    def test_evaluate(self):
        """Test evaluation for binary and multi-class cases with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            accuracy, predicted = self.nn_binary.evaluate(self.X, self.y_binary)
            self.assertTrue(0 <= accuracy <= 1)
            self.assertEqual(predicted.shape, self.y_binary.shape)
            self.assertTrue(np.all(predicted >= 0) and np.all(predicted <= 1))

            accuracy, predicted = self.nn_multi.evaluate(self.X, self.y_multi)
            self.assertTrue(0 <= accuracy <= 1)
            self.assertEqual(predicted.shape, self.y_multi.shape)
            self.assertTrue(np.all(predicted >= 0) and np.all(predicted < 10))

    def test_evaluate_regression(self):
        """Test evaluation for regression cases with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            metric, predicted = self.nn_regressor.evaluate(self.X, self.y_reg)
            self.assertIsInstance(metric, float)
            self.assertGreaterEqual(metric, 0)  # MSE >= 0
            self.assertEqual(predicted.shape, (50, 1))  # Evaluate returns 1D array

    ### Loss Calculation Test ###
    def test_calculate_loss(self):
        """Test loss calculation with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            loss = self.nn_binary.calculate_loss(self.X, self.y_binary)
            self.assertGreater(loss, 0)

    def test_calculate_loss_regression(self):
        """Test loss calculation for regression with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            loss = self.nn_regressor.calculate_loss(self.X, self.y_reg)
            self.assertIsInstance(loss, float)
            self.assertGreater(loss, 0)

    ### Prediction Tests ###
    def test_predict_binary(self):
        """Test prediction for binary classification with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            predictions = self.nn_binary.predict(self.X)
            self.assertEqual(predictions.shape, (50, 1))
            self.assertTrue(np.all(predictions >= 0) and np.all(predictions <= 1))

    def test_predict_multiclass(self):
        """Test prediction for multi-class classification with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            predictions = self.nn_multi.predict(self.X)
            self.assertEqual(predictions.shape, (50,))
            self.assertTrue(np.all(predictions >= 0) and np.all(predictions < 10))

    def test_predict_regression(self):
        """Test prediction for regression with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            predictions = self.nn_regressor.predict(self.X)
            self.assertEqual(
                predictions.shape, (50,)
            )  # Predict returns flattened array
            self.assertTrue(np.issubdtype(predictions.dtype, np.floating))

    ### Regularization Test ###
    def test_regularization(self):
        """Test regularization effect on loss with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nn = NumbaBackendNeuralNetwork(
                [2, 100, 1], reg_lambda=0, compile_numba=False, progress_bar=False
            )
            loss_no_reg = nn.calculate_loss(self.X, self.y_binary)
            nn.reg_lambda = 0.01
            loss_with_reg = nn.calculate_loss(self.X, self.y_binary)
            self.assertGreater(loss_with_reg, loss_no_reg)

    ### Edge Case Tests ###
    def test_single_sample(self):
        """Test handling of single-sample input with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            X_single = np.random.randn(1, 2)
            y_single = np.array([[1]])  # Shape (1, 1) for binary classification
            nn = NumbaBackendNeuralNetwork(
                [2, 10, 1], compile_numba=False, progress_bar=False
            )
            nn.forward(X_single)
            nn.backward(y_single)
            _accuracy, predicted = nn.evaluate(X_single, y_single)
            self.assertEqual(predicted.shape, (1, 1))

    def test_lr_scheduler(self):
        """Test learning rate scheduler integration with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nn = NumbaBackendNeuralNetwork(
                [2, 100, 1], compile_numba=False, progress_bar=False
            )
            optimizer = JITAdamOptimizer(learning_rate=0.01)
            scheduler = nn.create_scheduler(
                "step", optimizer, lr_decay=0.5, lr_decay_epoch=2
            )
            initial_lr = optimizer.learning_rate
            with suppress_print():
                nn.train(
                    self.X,
                    self.y_binary,
                    optimizer=optimizer,
                    epochs=3,
                    batch_size=32,
                    lr_scheduler=scheduler,
                    use_tqdm=False,
                    p=False,
                )
            final_lr = optimizer.learning_rate
        self.assertEqual(final_lr, initial_lr * 0.5)

    def test_integer_inputs(self):
        """Test handling of integer inputs with Numba."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            X_int = np.array([[1, 2], [3, 4]])
            _y_int = np.array([[0], [1]])
            nn = NumbaBackendNeuralNetwork(
                [2, 10, 1], compile_numba=False, progress_bar=False
            )
            outputs = nn.forward(X_int)
            self.assertEqual(outputs.shape, (2, 1))


if __name__ == "__main__":
    unittest.main()
