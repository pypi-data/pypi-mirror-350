import os
import sys
import unittest

import numpy as np
from numba import float64
from numba.experimental import jitclass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.neural_networks import *
from tests.utils import BaseTest

spec = [
    ("weights", float64[:, :]),
    ("biases", float64[:, :]),
]


@jitclass(spec)
class MockLayer:
    """Mock layer class for testing optimizers."""

    def __init__(self, input_size, output_size):
        """Initialize the MockLayer class."""
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.biases = np.zeros((1, output_size))


class TestJITAdamOptimizer(BaseTest):
    """Unit tests for the JITAdamOptimizer class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Print message before running tests."""
        print("\nTesting JITAdamOptimizer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize the JITAdamOptimizer class and layers."""
        self.optimizer = JITAdamOptimizer()
        self.layers = [MockLayer(3, 2), MockLayer(2, 1)]
        self.optimizer.initialize(self.layers)

    def test_initialize(self):
        """Test the initialize method."""
        self.assertEqual(len(self.optimizer.m), len(self.layers))
        self.assertEqual(len(self.optimizer.v), len(self.layers))
        # For JIT classes all layers are the same size
        for m, v in zip(self.optimizer.m, self.optimizer.v):
            np.testing.assert_array_equal(m, np.zeros_like(self.layers[0].weights))
            np.testing.assert_array_equal(v, np.zeros_like(self.layers[0].weights))

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


class TestJITSGDOptimizer(BaseTest):
    """Unit tests for the JITSGDOptimizer class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Print message before running tests."""
        print("\nTesting JITSGDOptimizer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize the JITSGDOptimizer class and layers."""
        self.optimizer = JITSGDOptimizer()
        self.layers = [MockLayer(3, 2), MockLayer(2, 1)]
        self.optimizer.initialize(self.layers)

    def test_initialize(self):
        """Test the initialize method."""
        self.assertEqual(len(self.optimizer.velocity), len(self.layers))
        # For JIT classes all layers are the same size
        for v, layer in zip(self.optimizer.velocity, self.layers):
            np.testing.assert_array_equal(
                v[: layer.weights.shape[0], : layer.weights.shape[1]],
                np.zeros_like(layer.weights),
            )

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


class TestJITAdadeltaOptimizer(BaseTest):
    """Unit tests for the JITAdadeltaOptimizer class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Print message before running tests."""
        print("\nTesting JITAdadeltaOptimizer", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Initialize the JITAdadeltaOptimizer class and layers."""
        self.optimizer = JITAdadeltaOptimizer()
        self.layers = [MockLayer(3, 2), MockLayer(2, 1)]
        self.optimizer.initialize(self.layers)

    def test_initialize(self):
        """Test the initialize method."""
        self.assertEqual(len(self.optimizer.E_g2), len(self.layers))
        self.assertEqual(len(self.optimizer.E_delta_x2), len(self.layers))
        # For JIT classes all layers are the same size
        for E_g2, E_delta_x2 in zip(self.optimizer.E_g2, self.optimizer.E_delta_x2):
            np.testing.assert_array_equal(E_g2, np.zeros_like(self.layers[0].weights))
            np.testing.assert_array_equal(
                E_delta_x2, np.zeros_like(self.layers[0].weights)
            )

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
