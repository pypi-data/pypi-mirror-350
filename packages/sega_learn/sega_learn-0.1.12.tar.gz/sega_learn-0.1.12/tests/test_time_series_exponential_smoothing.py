import os
import sys
import unittest
import warnings

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.time_series.exponential_smoothing import (
    DoubleExponentialSmoothing,
    SimpleExponentialSmoothing,
    TripleExponentialSmoothing,
)
from tests.utils import BaseTest


# --- Helper function for creating seasonal data ---
def create_seasonal_data(length=100, period=12, amplitude=10, trend=0.1, noise_std=2):
    """Creates sample time series data with seasonality, trend, and noise."""
    time = np.arange(length)
    seasonal_component = amplitude * np.sin(2 * np.pi * time / period)
    trend_component = trend * time
    noise_component = np.random.normal(0, noise_std, length)
    return (
        trend_component + seasonal_component + noise_component + 50
    )  # Add constant offset


class TestSimpleExponentialSmoothing(BaseTest):
    """Unit test suite for the SimpleExponentialSmoothing class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting SimpleExponentialSmoothing", end="", flush=True)
        # Suppress common warnings during tests (e.g., linalg warnings)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.ses = SimpleExponentialSmoothing(alpha=0.5)

    def test_initialization(self):
        """Test SimpleExponentialSmoothing initialization."""
        self.assertEqual(self.ses.alpha, 0.5)
        self.assertIsNone(self.ses.level)
        self.assertIsNone(self.ses.fitted_values)
        self.assertIsNone(self.ses.model)

    def test_initialization_invalid_alpha_high(self):
        """Test SimpleExponentialSmoothing initialization with invalid alpha."""
        with self.assertRaises(ValueError):
            SimpleExponentialSmoothing(alpha=1.5)

    def test_initialization_invalid_alpha_low(self):
        """Test SimpleExponentialSmoothing initialization with invalid alpha."""
        with self.assertRaises(ValueError):
            SimpleExponentialSmoothing(alpha=-0.1)

    def test_initialization_invalid_alpha_type(self):
        """Test SimpleExponentialSmoothing initialization with invalid alpha."""
        with self.assertRaises((ValueError, TypeError)):
            SimpleExponentialSmoothing(alpha="invalid")

    def test_fit(self):
        """Test fitting the model."""
        self.ses.fit(self.time_series)
        self.assertIsNotNone(self.ses.level)
        self.assertIsNotNone(self.ses.fitted_values)
        self.assertEqual(len(self.ses.fitted_values), len(self.time_series))
        self.assertEqual(len(self.ses.model), len(self.time_series))

    def test_fit_empty_series(self):
        """Test fitting the model with an empty series."""
        with self.assertRaises(ValueError):
            self.ses.fit(np.array([]))

    def test_fit_invalid_series(self):
        """Test fitting the model with an invalid series."""
        with self.assertRaises(ValueError):
            self.ses.fit("invalid_series")

    def test_forecast(self):
        """Test forecasting."""
        self.ses.fit(self.time_series)
        forecast = self.ses.forecast(5)
        self.assertEqual(len(forecast), 5)
        self.assertIsInstance(forecast, np.ndarray)

    def test_forecast_invalid_steps(self):
        """Test forecasting with invalid steps."""
        self.ses.fit(self.time_series)
        self.ses.forecast(0)

    def test_forecast_invalid_steps_type(self):
        """Test forecasting with invalid steps."""
        self.ses.fit(self.time_series)
        with self.assertRaises((ValueError, TypeError)):
            self.ses.forecast("invalid_steps")

    def test_forecast_negative_steps(self):
        """Test forecasting with negative steps."""
        self.ses.fit(self.time_series)
        self.ses.forecast(-5)


class TestDoubleExponentialSmoothing(BaseTest):
    """Unit test suite for the DoubleExponentialSmoothing class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting DoubleExponentialSmoothing", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.des = DoubleExponentialSmoothing(alpha=0.5, beta=0.5)

    def test_initialization(self):
        """Test DoubleExponentialSmoothing initialization."""
        self.assertEqual(self.des.alpha, 0.5)
        self.assertEqual(self.des.beta, 0.5)
        self.assertIsNone(self.des.level)
        self.assertIsNone(self.des.trend)
        self.assertIsNone(self.des.fitted_values)
        self.assertIsNone(self.des.model)

    def test_initialization_invalid_alpha(self):
        """Test DoubleExponentialSmoothing initialization with invalid alpha."""
        with self.assertRaises(ValueError):
            DoubleExponentialSmoothing(alpha=1.5, beta=0.5)

    def test_initialization_invalid_beta(self):
        """Test DoubleExponentialSmoothing initialization with invalid beta."""
        with self.assertRaises(ValueError):
            DoubleExponentialSmoothing(alpha=0.5, beta=-0.1)

    def test_fit(self):
        """Test fitting the model."""
        self.des.fit(self.time_series)
        self.assertIsNotNone(self.des.level)
        self.assertIsNotNone(self.des.trend)
        self.assertIsNotNone(self.des.fitted_values)
        self.assertEqual(len(self.des.fitted_values), len(self.time_series))

    def test_fit_empty_series(self):
        """Test fitting the model with an empty series."""
        with self.assertRaises(ValueError):
            self.des.fit(np.array([]))

    def test_fit_insufficient_series(self):
        """Test fitting the model with insufficient data points."""
        with self.assertRaises(ValueError):
            self.des.fit(np.array([1]))

    def test_forecast(self):
        """Test forecasting."""
        self.des.fit(self.time_series)
        forecast = self.des.forecast(5)
        self.assertEqual(len(forecast), 5)
        self.assertIsInstance(forecast, np.ndarray)

    def test_forecast_invalid_steps(self):
        """Test forecasting with invalid steps."""
        self.des.fit(self.time_series)
        self.assertEqual(len(self.des.forecast(0)), 0)

    def test_forecast_negative_steps(self):
        """Test forecasting with negative steps."""
        self.des.fit(self.time_series)
        self.des.forecast(-5)


class TestTripleExponentialSmoothing(BaseTest):
    """Unit test suite for the TripleExponentialSmoothing class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting TripleExponentialSmoothing", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.time_series = create_seasonal_data(length=24, period=12)
        self.tes = TripleExponentialSmoothing(alpha=0.5, beta=0.5, gamma=0.5, period=12)

    def test_initialization(self):
        """Test TripleExponentialSmoothing initialization."""
        self.assertEqual(self.tes.alpha, 0.5)
        self.assertEqual(self.tes.beta, 0.5)
        self.assertEqual(self.tes.gamma, 0.5)
        self.assertEqual(self.tes.period, 12)
        self.assertIsNone(self.tes.level)
        self.assertIsNone(self.tes.trend)
        self.assertIsNone(self.tes.season)
        self.assertIsNone(self.tes.fitted_values)
        self.assertIsNone(self.tes.model)

    def test_initialization_invalid_alpha(self):
        """Test TripleExponentialSmoothing initialization with invalid alpha."""
        with self.assertRaises(ValueError):
            TripleExponentialSmoothing(alpha=1.5, beta=0.5, gamma=0.5, period=12)

    def test_initialization_invalid_beta(self):
        """Test TripleExponentialSmoothing initialization with invalid beta."""
        with self.assertRaises(ValueError):
            TripleExponentialSmoothing(alpha=0.5, beta=-0.1, gamma=0.5, period=12)

    def test_initialization_invalid_gamma(self):
        """Test TripleExponentialSmoothing initialization with invalid gamma."""
        with self.assertRaises(ValueError):
            TripleExponentialSmoothing(alpha=0.5, beta=0.5, gamma=1.5, period=12)

    def test_initialization_invalid_period(self):
        """Test TripleExponentialSmoothing initialization with invalid period."""
        with self.assertRaises(ValueError):
            TripleExponentialSmoothing(alpha=0.5, beta=0.5, gamma=0.5, period=1)

    def test_fit(self):
        """Test fitting the model."""
        self.tes.fit(self.time_series)
        self.assertIsNotNone(self.tes.level)
        self.assertIsNotNone(self.tes.trend)
        self.assertIsNotNone(self.tes.season)
        self.assertIsNotNone(self.tes.fitted_values)
        self.assertEqual(len(self.tes.fitted_values), len(self.time_series))

    def test_fit_empty_series(self):
        """Test fitting the model with an empty series."""
        with self.assertRaises(ValueError):
            self.tes.fit(np.array([]))

    def test_fit_insufficient_series(self):
        """Test fitting the model with insufficient data points."""
        with self.assertRaises(ValueError):
            self.tes.fit(np.array([1, 2, 3]))

    def test_forecast(self):
        """Test forecasting."""
        self.tes.fit(self.time_series)
        forecast = self.tes.forecast(5)
        self.assertEqual(len(forecast), 5)
        self.assertIsInstance(forecast, np.ndarray)

    def test_forecast_invalid_steps(self):
        """Test forecasting with invalid steps."""
        self.tes.fit(self.time_series)
        self.assertEqual(len(self.tes.forecast(0)), 0)

    def test_forecast_negative_steps(self):
        """Test forecasting with negative steps."""
        self.tes.fit(self.time_series)
        self.tes.forecast(-5)


if __name__ == "__main__":
    unittest.main()
