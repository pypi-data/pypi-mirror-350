import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.neural_networks import *
from tests.utils import BaseTest


class MockLayer:
    """Mock layer class for testing optimizers."""

    def __init__(self, input_size, output_size):
        """Initialize the MockLayer class."""
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.biases = np.zeros((1, output_size))


class TestAdamOptimizer(BaseTest):
    """Unit tests for the AdamOptimizer class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Print message before running tests."""
        print("\nTesting AdamOptimizer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize the AdamOptimizer class and layers."""
        self.optimizer = AdamOptimizer()
        self.layers = [MockLayer(3, 2), MockLayer(2, 1)]
        self.optimizer.initialize(self.layers)

    def test_initialize(self):
        """Test the initialize method."""
        self.assertEqual(len(self.optimizer.m), len(self.layers))
        self.assertEqual(len(self.optimizer.v), len(self.layers))
        for m, v, layer in zip(self.optimizer.m, self.optimizer.v, self.layers):
            np.testing.assert_array_equal(m, np.zeros_like(layer.weights))
            np.testing.assert_array_equal(v, np.zeros_like(layer.weights))

    def test_update(self):
        """Test the update method."""
        layer = self.layers[0]
        dW = np.random.randn(*layer.weights.shape)
        db = np.random.randn(*layer.biases.shape)
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        self.assertFalse(np.array_equal(layer.weights, initial_weights))
        self.assertFalse(np.array_equal(layer.biases, initial_biases))

    def test_update_with_zero_gradients(self):
        """Test update method with zero gradients."""
        layer = self.layers[0]
        dW = np.zeros_like(layer.weights)
        db = np.zeros_like(layer.biases)
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        np.testing.assert_array_equal(layer.weights, initial_weights)
        np.testing.assert_array_equal(layer.biases, initial_biases)

    def test_update_with_large_gradients(self):
        """Test update method with large gradients."""
        layer = self.layers[0]
        dW = np.ones_like(layer.weights) * 1e5
        db = np.ones_like(layer.biases) * 1e5
        self.optimizer.update(layer, dW, db, 0)
        self.assertTrue(np.all(layer.weights < 1e5))
        self.assertTrue(np.all(layer.biases < 1e5))

    def test_update_with_small_gradients(self):
        """Test update method with small gradients."""
        layer = self.layers[0]
        dW = np.ones_like(layer.weights) * 1e-5
        db = np.ones_like(layer.biases) * 1e-5
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        self.assertFalse(np.array_equal(layer.weights, initial_weights))
        self.assertFalse(np.array_equal(layer.biases, initial_biases))


class TestSGDOptimizer(BaseTest):
    """Unit tests for the SGDOptimizer class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Print message before running tests."""
        print("\nTesting SGDOptimizer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize the SGDOptimizer class and layers."""
        self.optimizer = SGDOptimizer()
        self.layers = [MockLayer(3, 2), MockLayer(2, 1)]
        self.optimizer.initialize(self.layers)

    def test_initialize(self):
        """Test the initialize method."""
        self.assertEqual(len(self.optimizer.velocity), len(self.layers))
        for v, layer in zip(self.optimizer.velocity, self.layers):
            np.testing.assert_array_equal(v, np.zeros_like(layer.weights))

    def test_update(self):
        """Test the update method."""
        layer = self.layers[0]
        dW = np.random.randn(*layer.weights.shape)
        db = np.random.randn(*layer.biases.shape)
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        self.assertFalse(np.array_equal(layer.weights, initial_weights))
        self.assertFalse(np.array_equal(layer.biases, initial_biases))

    def test_update_with_zero_gradients(self):
        """Test update method with zero gradients."""
        layer = self.layers[0]
        dW = np.zeros_like(layer.weights)
        db = np.zeros_like(layer.biases)
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        np.testing.assert_array_equal(layer.weights, initial_weights)
        np.testing.assert_array_equal(layer.biases, initial_biases)

    def test_update_with_large_gradients(self):
        """Test update method with large gradients."""
        layer = self.layers[0]
        dW = np.ones_like(layer.weights) * 1e5
        db = np.ones_like(layer.biases) * 1e5
        self.optimizer.update(layer, dW, db, 0)
        self.assertTrue(np.all(layer.weights < 1e5))
        self.assertTrue(np.all(layer.biases < 1e5))

    def test_update_with_small_gradients(self):
        """Test update method with small gradients."""
        layer = self.layers[0]
        dW = np.ones_like(layer.weights) * 1e-5
        db = np.ones_like(layer.biases) * 1e-5
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        self.assertFalse(np.array_equal(layer.weights, initial_weights))
        self.assertFalse(np.array_equal(layer.biases, initial_biases))


class TestAdadeltaOptimizer(BaseTest):
    """Unit tests for the AdadeltaOptimizer class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Print message before running tests."""
        print("\nTesting AdadeltaOptimizer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize the AdadeltaOptimizer class and layers."""
        self.optimizer = AdadeltaOptimizer()
        self.layers = [MockLayer(3, 2), MockLayer(2, 1)]
        self.optimizer.initialize(self.layers)

    def test_initialize(self):
        """Test the initialize method."""
        self.assertEqual(len(self.optimizer.E_g2), len(self.layers))
        self.assertEqual(len(self.optimizer.E_delta_x2), len(self.layers))
        for E_g2, E_delta_x2, layer in zip(
            self.optimizer.E_g2, self.optimizer.E_delta_x2, self.layers
        ):
            np.testing.assert_array_equal(E_g2, np.zeros_like(layer.weights))
            np.testing.assert_array_equal(E_delta_x2, np.zeros_like(layer.weights))

    def test_update(self):
        """Test the update method."""
        layer = self.layers[0]
        dW = np.random.randn(*layer.weights.shape)
        db = np.random.randn(*layer.biases.shape)
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        self.assertFalse(np.array_equal(layer.weights, initial_weights))
        self.assertFalse(np.array_equal(layer.biases, initial_biases))

    def test_update_with_zero_gradients(self):
        """Test update method with zero gradients."""
        layer = self.layers[0]
        dW = np.zeros_like(layer.weights)
        db = np.zeros_like(layer.biases)
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        np.testing.assert_array_equal(layer.weights, initial_weights)
        np.testing.assert_array_equal(layer.biases, initial_biases)

    def test_update_with_large_gradients(self):
        """Test update method with large gradients."""
        layer = self.layers[0]
        dW = np.ones_like(layer.weights) * 1e5
        db = np.ones_like(layer.biases) * 1e5
        self.optimizer.update(layer, dW, db, 0)
        self.assertTrue(np.all(layer.weights < 1e5))
        self.assertTrue(np.all(layer.biases < 1e5))

    def test_update_with_small_gradients(self):
        """Test update method with small gradients."""
        layer = self.layers[0]
        dW = np.ones_like(layer.weights) * 1e-5
        db = np.ones_like(layer.biases) * 1e-5
        initial_weights = layer.weights.copy()
        initial_biases = layer.biases.copy()
        self.optimizer.update(layer, dW, db, 0)
        self.assertFalse(np.array_equal(layer.weights, initial_weights))
        self.assertFalse(np.array_equal(layer.biases, initial_biases))


if __name__ == "__main__":
    unittest.main()
