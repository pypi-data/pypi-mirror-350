import os
import sys
import unittest
import warnings

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.neural_networks import *
from tests.utils import BaseTest


class TestCrossEntropyLoss(BaseTest):
    """Unit tests for the CrossEntropyLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting CrossEntropyLoss", end="", flush=True)

    def test_cross_entropy_loss_single_class(self):
        """Test the cross entropy loss for a single class."""
        loss_fn = CrossEntropyLoss()
        logits = np.array([[2.0, 1.0, 0.1]])
        targets = np.array([[1, 0, 0]])
        loss = loss_fn(logits, targets)

        # Correct the expected loss calculation
        exp_logits = np.exp(logits)
        softmax_probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        expected_loss = (
            -np.sum(targets * np.log(softmax_probs + 1e-15)) / logits.shape[0]
        )

        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_cross_entropy_loss_multi_class(self):
        """Test the cross entropy loss for multiple classes."""
        loss_fn = CrossEntropyLoss()
        logits = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 1.0]])
        targets = np.array([[1, 0, 0], [0, 1, 0]])
        loss = loss_fn(logits, targets)

        # Correct the expected loss calculation
        exp_logits = np.exp(logits)
        softmax_probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        expected_loss = (
            -np.sum(targets * np.log(softmax_probs + 1e-15)) / logits.shape[0]
        )

        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_cross_entropy_loss_empty_inputs(self):
        """Test the cross entropy loss for empty inputs."""
        loss_fn = CrossEntropyLoss()
        logits = np.array([])
        targets = np.array([])
        with self.assertRaises((ValueError, IndexError)):
            loss_fn(logits, targets)

    def test_cross_entropy_loss_mismatched_shapes(self):
        """Test the cross entropy loss for mismatched shapes."""
        loss_fn = CrossEntropyLoss()
        logits = np.array([[2.0, 1.0]])
        targets = np.array([1, 0, 0])
        with self.assertRaises(ValueError):
            loss_fn(logits, targets)

    def test_cross_entropy_loss_extreme_values(self):
        """Test the cross entropy loss for extreme values."""
        loss_fn = CrossEntropyLoss()
        logits = np.array([[1000.0, -1000.0]])
        targets = np.array([[1, 0]])
        loss = loss_fn(logits, targets)
        self.assertTrue(np.isfinite(loss))


class TestBCEWithLogitsLoss(BaseTest):
    """Unit tests for the BCEWithLogitsLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting BCEWithLogitsLoss", end="", flush=True)

    def test_bce_with_logits_loss(self):
        """Test the binary cross entropy loss with logits."""
        loss_fn = BCEWithLogitsLoss()
        logits = np.array([0.0, 2.0, -2.0])
        targets = np.array([0, 1, 0])
        loss = loss_fn(logits, targets)
        expected_loss = -np.mean(
            targets * np.log(1 / (1 + np.exp(-logits)) + 1e-15)
            + (1 - targets) * np.log(1 - 1 / (1 + np.exp(-logits)) + 1e-15)
        )
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_bce_with_logits_loss_edge_cases(self):
        """Test the binary cross entropy loss with logits for edge cases (large logits)."""
        warnings.filterwarnings(
            "ignore"
        )  # Suppress warnings, large logits will trigger overflow warnings
        loss_fn = BCEWithLogitsLoss()
        logits = np.array([1000.0, -1000.0])
        targets = np.array([1, 0])
        loss = loss_fn(logits, targets)
        expected_loss = -np.mean(
            targets * np.log(1 / (1 + np.exp(-logits)) + 1e-15)
            + (1 - targets) * np.log(1 - 1 / (1 + np.exp(-logits)) + 1e-15)
        )
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_bce_with_logits_loss_empty_inputs(self):
        """Test the binary cross entropy loss with empty inputs."""
        loss_fn = BCEWithLogitsLoss()
        logits = np.array([])
        targets = np.array([])
        loss_fn(logits, targets)


class TestMeanSquaredErrorLoss(BaseTest):
    """Unit tests for the MeanSquaredErrorLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting MeanSquaredErrorLoss", end="", flush=True)

    def test_mean_squared_error_loss(self):
        """Test the mean squared error loss."""
        loss_fn = MeanSquaredErrorLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])
        loss = loss_fn(y_true, y_pred)
        expected_loss = np.mean((y_true - y_pred) ** 2)
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_mean_squared_error_loss_empty_inputs(self):
        """Test the mean squared error loss for empty inputs."""
        loss_fn = MeanSquaredErrorLoss()
        y_true = np.array([])
        y_pred = np.array([])
        loss_fn(y_true, y_pred)

    def test_mean_squared_error_loss_mismatched_shapes(self):
        """Test the mean squared error loss for mismatched shapes."""
        loss_fn = MeanSquaredErrorLoss()
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            loss_fn(y_true, y_pred)


class TestMeanAbsoluteErrorLoss(BaseTest):
    """Unit tests for the MeanAbsoluteErrorLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting MeanAbsoluteErrorLoss", end="", flush=True)

    def test_mean_absolute_error_loss(self):
        """Test the mean absolute error loss."""
        loss_fn = MeanAbsoluteErrorLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])
        loss = loss_fn(y_true, y_pred)
        expected_loss = np.mean(np.abs(y_true - y_pred))
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_mean_absolute_error_loss_empty_inputs(self):
        """Test the mean absolute error loss for empty inputs."""
        loss_fn = MeanAbsoluteErrorLoss()
        y_true = np.array([])
        y_pred = np.array([])
        loss_fn(y_true, y_pred)

    def test_mean_absolute_error_loss_mismatched_shapes(self):
        """Test the mean absolute error loss for mismatched shapes."""
        loss_fn = MeanAbsoluteErrorLoss()
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            loss_fn(y_true, y_pred)


class TestHuberLoss(BaseTest):
    """Unit tests for the HuberLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting HuberLoss", end="", flush=True)

    def test_huber_loss_small_error(self):
        """Test the Huber loss for small errors."""
        loss_fn = HuberLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 2.1, 3.1])
        delta = 1.0
        loss = loss_fn(y_true, y_pred, delta)
        error = y_true - y_pred
        expected_loss = np.mean(0.5 * error**2)
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_huber_loss_large_error(self):
        """Test the Huber loss for large errors."""
        loss_fn = HuberLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([4.0, 5.0, 6.0])
        delta = 1.0
        loss = loss_fn(y_true, y_pred, delta)
        error = y_true - y_pred
        expected_loss = np.mean(delta * (np.abs(error) - 0.5 * delta))
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_huber_loss_empty_inputs(self):
        """Test the Huber loss for empty inputs."""
        loss_fn = HuberLoss()
        y_true = np.array([])
        y_pred = np.array([])
        loss_fn(y_true, y_pred)

    def test_huber_loss_mismatched_shapes(self):
        """Test the Huber loss for mismatched shapes."""
        loss_fn = HuberLoss()
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            loss_fn(y_true, y_pred)

    def test_huber_loss_extreme_values(self):
        """Test the Huber loss for extreme values."""
        loss_fn = HuberLoss()
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1e10, -1e10])
        delta = 1.0
        loss = loss_fn(y_true, y_pred, delta)
        self.assertTrue(np.isfinite(loss))


if __name__ == "__main__":
    unittest.main()
