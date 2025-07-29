import os
import sys
import unittest
import warnings

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.time_series.moving_average import (
    ExponentialMovingAverage,
    SimpleMovingAverage,
    WeightedMovingAverage,
)
from tests.utils import BaseTest


class TestSimpleMovingAverage(BaseTest):
    """Unit test suite for the SimpleMovingAverage class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting SimpleMovingAverage", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.sma = SimpleMovingAverage(window=3)

    def test_initialization(self):
        """Test SimpleMovingAverage initialization."""
        self.assertEqual(self.sma.window, 3)
        self.assertIsNone(self.sma.smoothed_values)
        self.assertIsNone(self.sma.model)

    def test_initialization_invalid_window(self):
        """Test SimpleMovingAverage initialization with invalid window."""
        with self.assertRaises(ValueError):
            SimpleMovingAverage(window=0)

    def test_fit(self):
        """Test fitting the model."""
        smoothed = self.sma.fit(self.time_series)
        self.assertIsNotNone(smoothed)
        self.assertEqual(len(smoothed), len(self.time_series))
        self.assertTrue(np.isnan(smoothed[:2]).all())  # First 2 values should be NaN

    def test_fit_empty_series(self):
        """Test fitting the model with an empty series."""
        smoothed = self.sma.fit(np.array([]))
        with self.assertRaises((ValueError, TypeError)):
            self.assertEqual(len(smoothed), 0)

    def test_forecast(self):
        """Test forecasting."""
        self.sma.fit(self.time_series)
        forecast = self.sma.forecast(5)
        self.assertEqual(len(forecast), 5)
        self.assertTrue(
            np.all(forecast == forecast[0])
        )  # All values should be the same

    def test_forecast_invalid_steps(self):
        """Test forecasting with invalid steps."""
        self.sma.fit(self.time_series)
        forecast = self.sma.forecast(0)
        self.assertEqual(len(forecast), 0)


class TestWeightedMovingAverage(BaseTest):
    """Unit test suite for the WeightedMovingAverage class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting WeightedMovingAverage", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.wma = WeightedMovingAverage(window=3)

    def test_initialization(self):
        """Test WeightedMovingAverage initialization."""
        self.assertEqual(self.wma.window, 3)
        self.assertIsNotNone(self.wma.weights)
        self.assertIsNone(self.wma.smoothed_values)
        self.assertIsNone(self.wma.model)

    def test_initialization_invalid_window(self):
        """Test WeightedMovingAverage initialization with invalid window."""
        with self.assertRaises(ValueError):
            WeightedMovingAverage(window=0)

    def test_initialization_invalid_weights(self):
        """Test WeightedMovingAverage initialization with invalid weights."""
        with self.assertRaises(ValueError):
            WeightedMovingAverage(window=3, weights=[0.5, 0.5])

    def test_fit(self):
        """Test fitting the model."""
        smoothed = self.wma.fit(self.time_series)
        self.assertIsNotNone(smoothed)
        self.assertEqual(len(smoothed), len(self.time_series))
        self.assertTrue(np.isnan(smoothed[:2]).all())  # First 2 values should be NaN

    def test_fit_empty_series(self):
        """Test fitting the model with an empty series."""
        smoothed = self.wma.fit(np.array([]))
        with self.assertRaises((ValueError, TypeError)):
            self.assertEqual(len(smoothed), 0)

    def test_forecast(self):
        """Test forecasting."""
        self.wma.fit(self.time_series)
        forecast = self.wma.forecast(5)
        self.assertEqual(len(forecast), 5)
        self.assertTrue(
            np.all(forecast == forecast[0])
        )  # All values should be the same

    def test_forecast_invalid_steps(self):
        """Test forecasting with invalid steps."""
        self.wma.fit(self.time_series)
        forecast = self.wma.forecast(0)
        self.assertEqual(len(forecast), 0)


class TestExponentialMovingAverage(BaseTest):
    """Unit test suite for the ExponentialMovingAverage class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting ExponentialMovingAverage", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.ema = ExponentialMovingAverage(alpha=0.5)

    def test_initialization(self):
        """Test ExponentialMovingAverage initialization."""
        self.assertEqual(self.ema.alpha, 0.5)
        self.assertIsNone(self.ema.smoothed_values)
        self.assertIsNone(self.ema.model)
        self.assertIsNone(self.ema._last_ema)

    def test_initialization_invalid_alpha(self):
        """Test ExponentialMovingAverage initialization with invalid alpha."""
        with self.assertRaises(ValueError):
            ExponentialMovingAverage(alpha=1.5)

    def test_fit(self):
        """Test fitting the model."""
        smoothed = self.ema.fit(self.time_series)
        self.assertIsNotNone(smoothed)
        self.assertEqual(len(smoothed), len(self.time_series))

    def test_fit_empty_series(self):
        """Test fitting the model with an empty series."""
        smoothed = self.ema.fit(np.array([]))
        with self.assertRaises((ValueError, TypeError)):
            self.assertEqual(len(smoothed), 0)

    def test_forecast(self):
        """Test forecasting."""
        self.ema.fit(self.time_series)
        forecast = self.ema.forecast(5)
        self.assertEqual(len(forecast), 5)
        self.assertTrue(
            np.all(forecast == forecast[0])
        )  # All values should be the same

    def test_forecast_invalid_steps(self):
        """Test forecasting with invalid steps."""
        self.ema.fit(self.time_series)
        forecast = self.ema.forecast(0)
        self.assertEqual(len(forecast), 0)


if __name__ == "__main__":
    unittest.main()
