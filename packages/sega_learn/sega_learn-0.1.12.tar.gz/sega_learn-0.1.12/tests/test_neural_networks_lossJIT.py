import os
import sys
import unittest
import warnings

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.neural_networks import *
from tests.utils import BaseTest


class TestJITCrossEntropyLoss(BaseTest):
    """Unit tests for the JITCrossEntropyLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting JITCrossEntropyLoss", end="", flush=True)

    def test_cross_entropy_loss_single_class(self):
        """Test the cross entropy loss for a single class."""
        loss_fn = JITCrossEntropyLoss()
        logits = np.array([[2.0, 1.0, 0.1]])
        targets = np.array([[1, 0, 0]])
        loss = loss_fn.calculate_loss(logits, targets)

        # Correct the expected loss calculation
        exp_logits = np.exp(logits)
        softmax_probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        expected_loss = (
            -np.sum(targets * np.log(softmax_probs + 1e-15)) / logits.shape[0]
        )

        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_cross_entropy_loss_multi_class(self):
        """Test the cross entropy loss for multiple classes."""
        loss_fn = JITCrossEntropyLoss()
        logits = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 1.0]])
        targets = np.array([[1, 0, 0], [0, 1, 0]])
        loss = loss_fn.calculate_loss(logits, targets)

        # Correct the expected loss calculation
        exp_logits = np.exp(logits)
        softmax_probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        expected_loss = (
            -np.sum(targets * np.log(softmax_probs + 1e-15)) / logits.shape[0]
        )

        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_cross_entropy_loss_empty_inputs(self):
        """Test the cross entropy loss for empty inputs."""
        loss_fn = JITCrossEntropyLoss()
        logits = np.array([])
        targets = np.array([])
        with self.assertRaises((ValueError, AttributeError)):
            loss_fn.calculate_loss(logits, targets)

    def test_cross_entropy_loss_mismatched_shapes(self):
        """Test the cross entropy loss for mismatched shapes."""
        loss_fn = JITCrossEntropyLoss()
        logits = np.array([[2.0, 1.0]])
        targets = np.array([1, 0, 0])
        with self.assertRaises((ValueError, AttributeError)):
            loss_fn.calculate_loss(logits, targets)

    def test_cross_entropy_loss_extreme_values(self):
        """Test the cross entropy loss for extreme values."""
        loss_fn = JITCrossEntropyLoss()
        logits = np.array([[1000.0, -1000.0]])
        targets = np.array([[1, 0]])
        loss = loss_fn.calculate_loss(logits, targets)
        self.assertTrue(np.isfinite(loss))


class TestJITBCEWithLogitsLoss(BaseTest):
    """Unit tests for the JITBCEWithLogitsLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting JITBCEWithLogitsLoss", end="", flush=True)

    def test_bce_with_logits_loss(self):
        """Test the binary cross entropy loss with logits."""
        loss_fn = JITBCEWithLogitsLoss()
        logits = np.array([0.0, 2.0, -2.0])
        targets = np.array([0, 1, 0])
        loss = loss_fn.calculate_loss(logits, targets)
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
        loss_fn = JITBCEWithLogitsLoss()
        logits = np.array([1000.0, -1000.0])
        targets = np.array([1, 0])
        loss = loss_fn.calculate_loss(logits, targets)
        expected_loss = -np.mean(
            targets * np.log(1 / (1 + np.exp(-logits)) + 1e-15)
            + (1 - targets) * np.log(1 - 1 / (1 + np.exp(-logits)) + 1e-15)
        )
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_bce_with_logits_loss_empty_inputs(self):
        """Test the binary cross entropy loss with empty inputs."""
        loss_fn = JITBCEWithLogitsLoss()
        logits = np.array([])
        targets = np.array([])
        with self.assertRaises((ValueError, ZeroDivisionError)):
            loss_fn.calculate_loss(logits, targets)


class TestMeanSquaredErrorLoss(BaseTest):
    """Unit tests for the JITMeanSquaredErrorLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting JITMeanSquaredErrorLoss", end="", flush=True)

    def test_mean_squared_error_loss(self):
        """Test the mean squared error loss."""
        loss_fn = JITMeanSquaredErrorLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])
        loss = loss_fn.calculate_loss(y_true, y_pred)
        expected_loss = np.mean((y_true - y_pred) ** 2)
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_mean_squared_error_loss_empty_inputs(self):
        """Test the mean squared error loss for empty inputs."""
        loss_fn = JITMeanSquaredErrorLoss()
        y_true = np.array([])
        y_pred = np.array([])
        with self.assertRaises((ValueError, ZeroDivisionError)):
            loss_fn.calculate_loss(y_true, y_pred)

    def test_mean_squared_error_loss_mismatched_shapes(self):
        """Test the mean squared error loss for mismatched shapes."""
        loss_fn = JITMeanSquaredErrorLoss()
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            loss_fn.calculate_loss(y_true, y_pred)


class TestMeanAbsoluteErrorLoss(BaseTest):
    """Unit tests for the JITMeanAbsoluteErrorLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting JITMeanAbsoluteErrorLoss", end="", flush=True)

    def test_mean_absolute_error_loss(self):
        """Test the mean absolute error loss."""
        loss_fn = JITMeanAbsoluteErrorLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])
        loss = loss_fn.calculate_loss(y_true, y_pred)
        expected_loss = np.mean(np.abs(y_true - y_pred))
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_mean_absolute_error_loss_empty_inputs(self):
        """Test the mean absolute error loss for empty inputs."""
        loss_fn = JITMeanAbsoluteErrorLoss()
        y_true = np.array([])
        y_pred = np.array([])
        with self.assertRaises((ValueError, ZeroDivisionError)):
            loss_fn.calculate_loss(y_true, y_pred)

    def test_mean_absolute_error_loss_mismatched_shapes(self):
        """Test the mean absolute error loss for mismatched shapes."""
        loss_fn = JITMeanAbsoluteErrorLoss()
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            loss_fn.calculate_loss(y_true, y_pred)


class TestHuberLoss(BaseTest):
    """Unit tests for the HuberLoss class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting JITHuberLoss", end="", flush=True)

    def test_huber_loss_small_error(self):
        """Test the Huber loss for small errors."""
        delta = 1.0
        loss_fn = JITHuberLoss(delta=delta)
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 2.1, 3.1])
        loss = loss_fn.calculate_loss(y_true, y_pred)
        error = y_true - y_pred
        expected_loss = np.mean(0.5 * error**2)
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_huber_loss_large_error(self):
        """Test the Huber loss for large errors."""
        delta = 1.0
        loss_fn = JITHuberLoss(delta=delta)
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([4.0, 5.0, 6.0])
        loss = loss_fn.calculate_loss(y_true, y_pred)
        error = y_true - y_pred
        expected_loss = np.mean(delta * (np.abs(error) - 0.5 * delta))
        self.assertAlmostEqual(loss, expected_loss, places=5)

    def test_huber_loss_empty_inputs(self):
        """Test the Huber loss for empty inputs."""
        loss_fn = JITHuberLoss()
        y_true = np.array([])
        y_pred = np.array([])
        with self.assertRaises((ValueError, ZeroDivisionError)):
            loss_fn.calculate_loss(y_true, y_pred)

    def test_huber_loss_mismatched_shapes(self):
        """Test the Huber loss for mismatched shapes."""
        loss_fn = JITHuberLoss()
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            loss_fn.calculate_loss(y_true, y_pred)

    def test_huber_loss_extreme_values(self):
        """Test the Huber loss for extreme values."""
        loss_fn = JITHuberLoss()
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1e10, -1e10])
        loss = loss_fn.calculate_loss(y_true, y_pred)
        self.assertTrue(np.isfinite(loss))


class TestJITvsNonJITLosses(BaseTest):
    """Unit tests to compare JIT and non-JIT loss implementations."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print(
            "\nTesting Comparing JIT and non-JIT loss implementations",
            end="",
            flush=True,
        )

    def test_cross_entropy_loss(self):
        """Compare JIT and non-JIT CrossEntropyLoss."""
        jit_loss_fn = JITCrossEntropyLoss()
        non_jit_loss_fn = CrossEntropyLoss()
        logits = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 1.0]])
        targets = np.array([[1, 0, 0], [0, 1, 0]])
        jit_loss = jit_loss_fn.calculate_loss(logits, targets)
        non_jit_loss = non_jit_loss_fn(logits, targets)
        self.assertAlmostEqual(jit_loss, non_jit_loss, places=5)

    def test_bce_with_logits_loss(self):
        """Compare JIT and non-JIT BCEWithLogitsLoss."""
        jit_loss_fn = JITBCEWithLogitsLoss()
        non_jit_loss_fn = BCEWithLogitsLoss()
        logits = np.array([0.0, 2.0, -2.0])
        targets = np.array([0, 1, 0])
        jit_loss = jit_loss_fn.calculate_loss(logits, targets)
        non_jit_loss = non_jit_loss_fn(logits, targets)
        self.assertAlmostEqual(jit_loss, non_jit_loss, places=5)

    def test_mean_squared_error_loss(self):
        """Compare JIT and non-JIT MeanSquaredErrorLoss."""
        jit_loss_fn = JITMeanSquaredErrorLoss()
        non_jit_loss_fn = MeanSquaredErrorLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])
        jit_loss = jit_loss_fn.calculate_loss(y_true, y_pred)
        non_jit_loss = non_jit_loss_fn(y_true, y_pred)
        self.assertAlmostEqual(jit_loss, non_jit_loss, places=5)

    def test_mean_absolute_error_loss(self):
        """Compare JIT and non-JIT MeanAbsoluteErrorLoss."""
        jit_loss_fn = JITMeanAbsoluteErrorLoss()
        non_jit_loss_fn = MeanAbsoluteErrorLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.5, 2.5, 3.5])
        jit_loss = jit_loss_fn.calculate_loss(y_true, y_pred)
        non_jit_loss = non_jit_loss_fn(y_true, y_pred)
        self.assertAlmostEqual(jit_loss, non_jit_loss, places=5)

    def test_huber_loss(self):
        """Compare JIT and non-JIT HuberLoss."""
        jit_loss_fn = JITHuberLoss(delta=1.0)
        non_jit_loss_fn = HuberLoss()
        y_true = np.array([1.0, 2.0, 3.0])
        y_pred = np.array([1.1, 2.1, 3.1])
        jit_loss = jit_loss_fn.calculate_loss(y_true, y_pred)
        non_jit_loss = non_jit_loss_fn(y_true, y_pred, delta=1.0)
        self.assertAlmostEqual(jit_loss, non_jit_loss, places=5)


if __name__ == "__main__":
    unittest.main()
