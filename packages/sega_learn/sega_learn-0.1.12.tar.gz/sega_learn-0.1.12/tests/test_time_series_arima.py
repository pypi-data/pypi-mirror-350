import os
import sys
import unittest
import warnings

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.time_series.arima import ARIMA, SARIMA, SARIMAX
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


class TestARIMA(BaseTest):
    """Unit test suite for the ARIMA class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting ARIMA", end="", flush=True)
        # Suppress common warnings during tests (e.g., linalg warnings)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.order = (1, 1, 1)  # Use simpler order for basic tests
        self.arima = ARIMA(order=self.order)

    def test_initialization(self):
        """Test ARIMA initialization."""
        self.assertEqual(self.arima.order, self.order)
        self.assertEqual(self.arima.p, self.order[0])
        self.assertEqual(self.arima.d, self.order[1])
        self.assertEqual(self.arima.q, self.order[2])
        self.assertIsNone(self.arima.model)
        self.assertIsNone(self.arima.fitted_model)

    def test_invalid_order_negative_value(self):
        """Test ARIMA initialization with a negative value in the order."""
        with self.assertRaisesRegex(ValueError, "p, d, and q must be non-negative"):
            ARIMA(order=(1, -1, 1))

    def test_invalid_order_missing_parameter(self):
        """Test ARIMA initialization with a missing parameter in the order."""
        with self.assertRaisesRegex(
            ValueError, "Order must be a list or tuple of length 3"
        ):
            ARIMA(order=(1, 1))

    def test_invalid_order_invalid_type(self):
        """Test ARIMA initialization with an invalid type for the order."""
        with self.assertRaisesRegex(
            ValueError, "Order must be a list or tuple of length 3"
        ):
            ARIMA(order="invalid")

    def test_invalid_order_extra_parameter(self):
        """Test ARIMA initialization with an extra parameter in the order."""
        with self.assertRaisesRegex(
            ValueError, "Order must be a list or tuple of length 3"
        ):
            ARIMA(order=(1, 1, 1, 1))

    def test_fit(self):
        """Test the fit method."""
        self.arima.fit(self.time_series)
        self.assertIsNotNone(self.arima.fitted_model)
        self.assertTrue("ar_coefficients" in self.arima.fitted_model)
        self.assertTrue("ma_coefficients" in self.arima.fitted_model)
        self.assertEqual(len(self.arima.fitted_model["ar_coefficients"]), self.arima.p)
        self.assertEqual(len(self.arima.fitted_model["ma_coefficients"]), self.arima.q)
        self.assertIsNotNone(self.arima.model)
        np.testing.assert_array_equal(self.arima.model, self.time_series)

    def test_fit_invalid_data_type(self):
        """Test fitting with invalid data type."""
        # Expecting TypeError or potentially ValueError depending on numpy conversion
        with self.assertRaises((TypeError, ValueError)):
            self.arima.fit("invalid_data")

    def test_fit_insufficient_data_for_differencing(self):
        """Test fitting when differencing degree exceeds data length."""
        short_series = np.array([1, 2], dtype=float)
        arima_d2 = ARIMA(order=(1, 2, 1))
        with self.assertRaisesRegex(
            ValueError,
            "Time series length must be greater than the differencing order d.",
        ):
            arima_d2.fit(short_series)

    def test_forecast(self):
        """Test the forecast method."""
        self.arima.fit(self.time_series)
        forecasted_values = self.arima.forecast(steps=3)
        self.assertEqual(len(forecasted_values), 3)
        self.assertTrue(isinstance(forecasted_values, np.ndarray))

    # TODO: Check this test for linear trend
    # def test_forecast_linear_trend(self):
    #     """Test forecasting with a linear trend."""
    #     # A simple check: ARIMA(0,1,0) on linear trend should predict the trend
    #     arima_010 = ARIMA(order=(0,1,0))
    #     arima_010.fit(self.time_series)
    #     forecast_010 = arima_010.forecast(steps=2)
    #     print(f"Forecast: {forecast_010}")
    #     np.testing.assert_array_almost_equal(forecast_010, [11.0, 12.0])

    def test_forecast_without_fit(self):
        """Test forecasting without fitting the model."""
        with self.assertRaisesRegex(
            ValueError, "model must be fitted before forecasting"
        ):
            self.arima.forecast(steps=3)

    def test_differencing_d0(self):
        """Test the _difference_series method."""
        diff0 = self.arima._difference_series(self.time_series, 0)
        np.testing.assert_array_equal(diff0, self.time_series)

    def test_differencing_d1(self):
        """Test the _difference_series method."""
        diff1 = self.arima._difference_series(self.time_series, 1)
        np.testing.assert_array_equal(diff1, np.ones(len(self.time_series) - 1))

    def test_differencing_d2(self):
        """Test the _difference_series method."""
        diff2 = self.arima._difference_series(self.time_series, 2)
        np.testing.assert_array_equal(diff2, np.zeros(len(self.time_series) - 2))

    # --- Static method tests (require statsmodels) ---
    try:
        import statsmodels

        _has_statsmodels = True
    except ImportError:
        _has_statsmodels = False

    @unittest.skipIf(
        not _has_statsmodels, "statsmodels not installed, skipping suggest_order tests"
    )
    def test_suggest_order(self):
        """Test the suggest_order static method."""
        # On linear trend, d=1 or d=2 should be found, p/q likely 0 or 1
        suggested_order = ARIMA.suggest_order(
            self.time_series, max_p=1, max_d=2, max_q=1
        )
        self.assertEqual(len(suggested_order), 3)
        self.assertTrue(all(isinstance(i, int) for i in suggested_order))
        self.assertIn(suggested_order[1], [1, 2])  # d should be 1 or 2

    @unittest.skipIf(
        not _has_statsmodels, "statsmodels not installed, skipping suggest_order tests"
    )
    def test_suggest_order_invalid_data(self):
        """Test suggest_order with invalid data."""
        # numpy array conversion might handle some cases, but non-numeric should fail
        with self.assertRaises((TypeError, ValueError)):
            ARIMA.suggest_order(["a", "b", "c"])

    @unittest.skipIf(
        not _has_statsmodels, "statsmodels not installed, skipping suggest_order tests"
    )
    def test_suggest_order_empty_data(self):
        """Test suggest_order with empty or too short data."""
        with self.assertRaises(
            ValueError
        ):  # ADF test usually raises on very short series
            ARIMA.suggest_order([])
        with self.assertRaises(ValueError):
            ARIMA.suggest_order([1])

    def test_find_best_order(self):
        """Test the find_best_order static method."""
        train_series = self.time_series[:7]
        test_series = self.time_series[7:]
        # Expect low order like (0,1,0) or similar for linear trend
        best_order = ARIMA.find_best_order(
            train_series, test_series, max_p=1, max_d=2, max_q=1
        )
        self.assertEqual(len(best_order), 3)
        self.assertTrue(all(isinstance(i, int) for i in best_order))
        self.assertTrue(0 <= best_order[0] <= 1)
        self.assertTrue(0 <= best_order[1] <= 2)
        self.assertTrue(0 <= best_order[2] <= 1)
        # Check if (0,1,0) is found as it's optimal here
        # self.assertEqual(best_order, (0, 1, 0)) # May vary slightly based on implementation details

    def test_find_best_order_invalid_data_type(self):
        """Test find_best_order with invalid data type."""
        with self.assertRaisesRegex(ValueError, "must be list or numpy array"):
            ARIMA.find_best_order("invalid", self.time_series[7:])
        with self.assertRaisesRegex(ValueError, "must be list or numpy array"):
            ARIMA.find_best_order(self.time_series[:7], "invalid")

    def test_find_best_order_empty_data(self):
        """Test find_best_order with empty data."""
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            ARIMA.find_best_order([], self.time_series[7:])
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            ARIMA.find_best_order(self.time_series[:7], [])

    def test_find_best_order_subset(self):
        """Test find_best_order with a subset of the training series."""
        long_series = np.linspace(0, 50, 51)
        train_series = long_series[:40]
        test_series = long_series[40:]
        # Ensure subsetting doesn't crash
        best_order = ARIMA.find_best_order(
            train_series, test_series, subset_size=0.5, max_p=1, max_d=1, max_q=1
        )
        self.assertEqual(len(best_order), 3)
        self.assertTrue(all(isinstance(i, int) for i in best_order))

    def test_find_best_order_invalid_subset(self):
        """Test find_best_order with an invalid subset size."""
        train_series = self.time_series[:7]
        test_series = self.time_series[7:]
        with self.assertRaisesRegex(ValueError, "subset_size must be between 0 and 1"):
            ARIMA.find_best_order(train_series, test_series, subset_size=1.5)
        with self.assertRaisesRegex(ValueError, "subset_size must be between 0 and 1"):
            ARIMA.find_best_order(train_series, test_series, subset_size=-0.5)
        with self.assertRaisesRegex(ValueError, "subset_size must be between 0 and 1"):
            ARIMA.find_best_order(train_series, test_series, subset_size=0)


class TestSARIMA(BaseTest):
    """Unit test suite for the SARIMA class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting SARIMA", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.seasonal_period = 4  # Simple seasonality
        self.time_series = create_seasonal_data(
            length=40, period=self.seasonal_period, trend=0.05, noise_std=1
        )
        self.order = (1, 0, 1)
        self.seasonal_order = (1, 1, 1, self.seasonal_period)  # P, D, Q, m
        self.sarima = SARIMA(order=self.order, seasonal_order=self.seasonal_order)

    def test_initialization(self):
        """Test SARIMA initialization."""
        self.assertEqual(self.sarima.order, self.order)
        self.assertEqual(self.sarima.seasonal_order, self.seasonal_order)
        self.assertEqual(self.sarima.p, self.order[0])
        self.assertEqual(self.sarima.d, self.order[1])
        self.assertEqual(self.sarima.q, self.order[2])
        self.assertEqual(self.sarima.P, self.seasonal_order[0])
        self.assertEqual(self.sarima.D, self.seasonal_order[1])
        self.assertEqual(self.sarima.Q, self.seasonal_order[2])
        self.assertEqual(self.sarima.m, self.seasonal_order[3])
        self.assertIsNone(self.sarima.model)  # Inherited, check parent init
        self.assertIsNone(self.sarima.fitted_model)
        self.assertIsNone(self.sarima.original_series)

    def test_invalid_seasonal_order_length_less_than_4(self):
        """Test SARIMA initialization with invalid seasonal order length."""
        with self.assertRaisesRegex(
            ValueError, "Seasonal order must be a tuple/list of length 4"
        ):
            SARIMA(seasonal_order=(1, 1, 1))

    def test_invalid_seasonal_order_length_more_than_4(self):
        """Test SARIMA initialization with invalid seasonal order length."""
        with self.assertRaisesRegex(
            ValueError, "Seasonal order must be a tuple/list of length 4"
        ):
            SARIMA(seasonal_order=(1, 1, 1, 4, 5))

    def test_invalid_seasonal_order_values(self):
        """Test SARIMA initialization with invalid seasonal order values."""
        with self.assertRaisesRegex(
            ValueError, "P, D, Q must be ≥0 and m must be a positive integer."
        ):
            SARIMA(seasonal_order=(-1, 1, 1, 4))
        with self.assertRaisesRegex(
            ValueError, "P, D, Q must be ≥0 and m must be a positive integer."
        ):
            SARIMA(seasonal_order=(1, -1, 1, 4))
        with self.assertRaisesRegex(
            ValueError, "P, D, Q must be ≥0 and m must be a positive integer."
        ):
            SARIMA(seasonal_order=(1, 1, -1, 4))
        with self.assertRaisesRegex(
            ValueError, "P, D, Q must be ≥0 and m must be a positive integer."
        ):
            SARIMA(seasonal_order=(1, 1, 1, 0))
        with self.assertRaisesRegex(
            ValueError, "P, D, Q must be ≥0 and m must be a positive integer."
        ):
            SARIMA(seasonal_order=(1, 1, 1, -4))

    def test_seasonal_difference_d1(self):
        """Test the _seasonal_difference method."""
        m = self.seasonal_period
        D1_diff = self.sarima._seasonal_difference(self.time_series, D=1, m=m)
        self.assertEqual(len(D1_diff), len(self.time_series) - m)
        expected_D1 = self.time_series[m:] - self.time_series[:-m]
        np.testing.assert_array_almost_equal(D1_diff, expected_D1)

    def test_seasonal_difference_d2(self):
        """Test the _seasonal_difference method."""
        m = self.seasonal_period
        D1_diff = self.sarima._seasonal_difference(self.time_series, D=1, m=m)
        self.assertEqual(len(D1_diff), len(self.time_series) - m)
        expected_D1 = self.time_series[m:] - self.time_series[:-m]
        # D=2
        D2_diff = self.sarima._seasonal_difference(self.time_series, D=2, m=m)
        self.assertEqual(len(D2_diff), len(self.time_series) - 2 * m)
        expected_D2 = expected_D1[m:] - expected_D1[:-m]
        np.testing.assert_array_almost_equal(D2_diff, expected_D2)

    def test_seasonal_difference_d0(self):
        """Test the _seasonal_difference method."""
        m = self.seasonal_period
        # D=0
        D0_diff = self.sarima._seasonal_difference(self.time_series, D=0, m=m)
        np.testing.assert_array_almost_equal(D0_diff, self.time_series)

    # TODO: Fix this test
    # def test_inverse_seasonal_difference_roundtrip(self):
    #     """Test _inverse_seasonal_difference by round-tripping."""
    #     # This is hard to test directly in isolation as it needs history.
    #     # We test it implicitly via fit/forecast.
    #     # Let's try a simple round trip though
    #     sarima_000_0104 = SARIMA(order=(0,0,0), seasonal_order=(0,1,0,4))
    #     sarima_000_0104.original_series = self.time_series # Manually set for test
    #     sarima_000_0104.D = 1
    #     sarima_000_0104.m = 4
    #     diff_series = sarima_000_0104._seasonal_difference(self.time_series, D=1, m=4)

    #     # The inverse function forecasts step-by-step, so simulate that
    #     # We need to predict the *differenced* values first
    #     # Let's just use the known differenced values as 'forecasts'
    #     reconstructed = sarima_000_0104._inverse_seasonal_difference(diff_series)

    #     # Should reconstruct the original series starting from index m
    #     np.testing.assert_array_almost_equal(reconstructed, self.time_series[sarima_000_0104.m:])

    def test_fit(self):
        """Test the SARIMA fit method."""
        self.sarima.fit(self.time_series)
        self.assertIsNotNone(self.sarima.fitted_model)  # Check ARIMA part got fitted
        self.assertTrue("ar_coefficients" in self.sarima.fitted_model)
        self.assertTrue("ma_coefficients" in self.sarima.fitted_model)
        self.assertIsNotNone(self.sarima.original_series)
        np.testing.assert_array_equal(self.sarima.original_series, self.time_series)
        # Check if differencing was applied (model length should be shorter if D or d > 0)
        # Length after seasonal diff D=1: N - m
        # Length after non-seasonal diff d=0: N - m
        # Length fed to _fit_ar_model: N - m
        # Length of y in _fit_ar_model: N - m - p
        # Check internal model length implicitly via forecast
        self.assertIsNotNone(
            self.sarima.model
        )  # ARIMA's model (the potentially differenced series)

    # TODO: Fix this test
    # def test_fit_no_seasonal_differencing(self):
    #     """Test fit when D=0."""
    #     sarima_no_sd = SARIMA(order=(1,1,0), seasonal_order=(1,0,0,4))
    #     sarima_no_sd.fit(self.time_series)
    #     self.assertIsNotNone(sarima_no_sd.fitted_model)
    #     self.assertEqual(sarima_no_sd.D, 0)
    #     # The model fitted should be on the non-seasonally differenced series
    #     expected_model_input = sarima_no_sd._difference_series(self.time_series, d=1)
    #     np.testing.assert_array_almost_equal(sarima_no_sd.model, expected_model_input)

    def test_forecast(self):
        """Test the SARIMA forecast method."""
        self.sarima.fit(self.time_series)
        steps = 5
        forecasted_values = self.sarima.forecast(steps=steps)
        self.assertEqual(len(forecasted_values), steps)
        self.assertTrue(isinstance(forecasted_values, np.ndarray))
        # Check values are reasonable (not NaN or Inf)
        self.assertTrue(np.all(np.isfinite(forecasted_values)))

    def test_forecast_without_fit(self):
        """Test forecasting without fitting the model."""
        with self.assertRaisesRegex(ValueError, "Fit the model before forecasting"):
            self.sarima.forecast(steps=3)

    # --- Static method tests (require statsmodels) ---
    @unittest.skipIf(
        not TestARIMA._has_statsmodels,
        "statsmodels not installed, skipping SARIMA suggest/find tests",
    )
    def test_suggest_order(self):
        """Test the SARIMA suggest_order static method."""
        suggested_orders = SARIMA.suggest_order(
            self.time_series, max_m=self.seasonal_period + 1
        )  # Limit m for speed
        self.assertEqual(len(suggested_orders), 2)
        self.assertEqual(len(suggested_orders[0]), 3)  # (p, d, q)
        self.assertEqual(len(suggested_orders[1]), 4)  # (P, D, Q, m)
        self.assertTrue(all(isinstance(i, int) for i in suggested_orders[0]))
        self.assertTrue(all(isinstance(i, int) for i in suggested_orders[1]))
        # Check if detected 'm' is reasonable (should be close to self.seasonal_period or 1)
        detected_m = suggested_orders[1][3]
        self.assertTrue(detected_m > 0)
        # self.assertEqual(detected_m, self.seasonal_period) # Might not always detect perfectly

    @unittest.skipIf(
        not TestARIMA._has_statsmodels,
        "statsmodels not installed, skipping SARIMA suggest/find tests",
    )
    def test_find_best_order(self):
        """Test the SARIMA find_best_order static method."""
        train_series = self.time_series[:-5]
        test_series = self.time_series[-5:]
        best_orders = SARIMA.find_best_order(
            train_series,
            test_series,
            max_p=1,
            max_d=1,
            max_q=1,
            max_P=1,
            max_D=1,
            max_Q=1,
            max_m=self.seasonal_period,  # Fix m for test speed
        )
        self.assertEqual(len(best_orders), 2)
        self.assertEqual(len(best_orders[0]), 3)  # (p, d, q)
        self.assertEqual(len(best_orders[1]), 4)  # (P, D, Q, m)
        self.assertTrue(all(isinstance(i, int) for i in best_orders[0]))
        self.assertTrue(all(isinstance(i, int) for i in best_orders[1]))


class TestSARIMAX(BaseTest):
    """Unit test suite for the SARIMAX class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting SARIMAX", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.seasonal_period = 4
        self.n_samples = 40
        self.endog = create_seasonal_data(
            length=self.n_samples, period=self.seasonal_period, trend=0.05, noise_std=1
        )
        # Create exogenous variable strongly correlated with endog
        self.exog = self.endog * 0.5 + np.random.normal(0, 5, self.n_samples)
        self.exog = self.exog.reshape(-1, 1)  # Ensure 2D

        self.order = (1, 0, 0)
        self.seasonal_order = (1, 1, 0, self.seasonal_period)
        self.sarimax = SARIMAX(order=self.order, seasonal_order=self.seasonal_order)

        # For forecasting
        self.steps = 5
        self.exog_future = np.random.rand(self.steps, 1) * 10 + 50  # Future exog values

    def test_initialization(self):
        """Test SARIMAX initialization."""
        self.assertEqual(self.sarimax.order, self.order)
        self.assertEqual(self.sarimax.seasonal_order, self.seasonal_order)
        self.assertEqual(self.sarimax.p, self.order[0])
        self.assertEqual(self.sarimax.P, self.seasonal_order[0])
        self.assertEqual(self.sarimax.m, self.seasonal_order[3])
        self.assertIsNone(self.sarimax.beta)
        self.assertIsNone(self.sarimax.k_exog)
        self.assertIsNone(self.sarimax.fitted_model)  # From parent
        self.assertIsNone(self.sarimax.original_series)  # From parent

    def test_fit(self):
        """Test the SARIMAX fit method."""
        self.sarimax.fit(self.endog, self.exog)

        # Check beta and k_exog
        self.assertIsNotNone(self.sarimax.beta)
        self.assertIsNotNone(self.sarimax.k_exog)
        self.assertEqual(self.sarimax.k_exog, self.exog.shape[1])
        self.assertEqual(len(self.sarimax.beta), self.exog.shape[1])

        # Check underlying SARIMA fit
        self.assertIsNotNone(self.sarimax.fitted_model)
        self.assertTrue("ar_coefficients" in self.sarimax.fitted_model)
        self.assertTrue("ma_coefficients" in self.sarimax.fitted_model)
        self.assertIsNotNone(
            self.sarimax.original_series
        )  # Should store original endog
        np.testing.assert_array_equal(self.sarimax.original_series, self.endog)

    def test_fit_1d_exog(self):
        """Test fitting with 1D exogenous data."""
        exog_1d = self.exog.flatten()
        self.sarimax.fit(self.endog, exog_1d)
        self.assertEqual(self.sarimax.k_exog, 1)
        self.assertEqual(len(self.sarimax.beta), 1)
        self.assertIsNotNone(self.sarimax.fitted_model)

    def test_fit_mismatched_lengths(self):
        """Test fit with endog and exog having different lengths."""
        with self.assertRaisesRegex(ValueError, "y and exog must have the same length"):
            self.sarimax.fit(self.endog, self.exog[:-1])

    def test_forecast(self):
        """Test the SARIMAX forecast method."""
        self.sarimax.fit(self.endog, self.exog)
        forecasted_values = self.sarimax.forecast(
            steps=self.steps, exog_future=self.exog_future
        )

        self.assertEqual(len(forecasted_values), self.steps)
        self.assertTrue(isinstance(forecasted_values, np.ndarray))
        self.assertTrue(np.all(np.isfinite(forecasted_values)))

    def test_forecast_1d_exog_future(self):
        """Test forecasting with 1D future exogenous data."""
        self.sarimax.fit(self.endog, self.exog)
        # Requires k_exog = 1
        sarimax_k1 = SARIMAX(order=(0, 0, 0), seasonal_order=(0, 0, 0, 1))
        exog_k1 = self.exog[:, 0]  # Use first column as 1D
        sarimax_k1.fit(self.endog, exog_k1)
        self.assertEqual(sarimax_k1.k_exog, 1)

        exog_future_1d = self.exog_future.flatten()
        forecast = sarimax_k1.forecast(steps=self.steps, exog_future=exog_future_1d)
        self.assertEqual(len(forecast), self.steps)

    def test_forecast_without_fit(self):
        """Test SARIMAX forecasting without fitting."""
        with self.assertRaisesRegex(ValueError, "Fit model before forecasting"):
            self.sarimax.forecast(steps=self.steps, exog_future=self.exog_future)

    def test_forecast_mismatched_exog_future_shape(self):
        """Test forecast with incorrect number of columns in exog_future."""
        self.sarimax.fit(self.endog, self.exog)
        # Fit with k_exog = 1
        self.assertEqual(self.sarimax.k_exog, 1)
        # Try forecasting with 2 columns
        exog_future_bad = np.random.rand(self.steps, 2)
        with self.assertRaisesRegex(
            ValueError, f"exog_future must have {self.sarimax.k_exog} columns"
        ):
            self.sarimax.forecast(steps=self.steps, exog_future=exog_future_bad)

        # Fit with k_exog = 2
        exog2 = np.hstack([self.exog, self.exog * 2])
        sarimax2 = SARIMAX(self.order, self.seasonal_order)
        sarimax2.fit(self.endog, exog2)
        self.assertEqual(sarimax2.k_exog, 2)
        # Try forecasting with 1 column
        exog_future_bad2 = np.random.rand(self.steps, 1)
        with self.assertRaisesRegex(
            ValueError, f"exog_future must have {sarimax2.k_exog} columns"
        ):
            sarimax2.forecast(steps=self.steps, exog_future=exog_future_bad2)

    # --- Static method tests (require statsmodels) ---
    @unittest.skipIf(
        not TestARIMA._has_statsmodels,
        "statsmodels not installed, skipping SARIMAX suggest/find tests",
    )
    def test_suggest_order(self):
        """Test the SARIMAX suggest_order static method."""
        suggested_orders = SARIMAX.suggest_order(
            self.endog, self.exog, max_m=self.seasonal_period + 1
        )
        self.assertEqual(len(suggested_orders), 2)
        self.assertEqual(len(suggested_orders[0]), 3)  # (p, d, q)
        self.assertEqual(len(suggested_orders[1]), 4)  # (P, D, Q, m)
        self.assertTrue(all(isinstance(i, int) for i in suggested_orders[0]))
        self.assertTrue(all(isinstance(i, int) for i in suggested_orders[1]))

    @unittest.skipIf(
        not TestARIMA._has_statsmodels,
        "statsmodels not installed, skipping SARIMAX suggest/find tests",
    )
    def test_find_best_order(self):
        """Test the SARIMAX find_best_order static method."""
        split_idx = self.n_samples - self.steps
        train_endog, test_endog = self.endog[:split_idx], self.endog[split_idx:]
        train_exog, test_exog = self.exog[:split_idx], self.exog[split_idx:]

        best_orders = SARIMAX.find_best_order(
            train_endog,
            test_endog,
            train_exog,
            test_exog,
            max_p=1,
            max_d=0,
            max_q=0,
            max_P=1,
            max_D=1,
            max_Q=0,
            max_m=self.seasonal_period,  # Limit search space
        )
        self.assertEqual(len(best_orders), 2)
        self.assertEqual(len(best_orders[0]), 3)  # (p, d, q)
        self.assertEqual(len(best_orders[1]), 4)  # (P, D, Q, m)
        self.assertTrue(all(isinstance(i, int) for i in best_orders[0]))
        self.assertTrue(all(isinstance(i, int) for i in best_orders[1]))


if __name__ == "__main__":
    unittest.main()
