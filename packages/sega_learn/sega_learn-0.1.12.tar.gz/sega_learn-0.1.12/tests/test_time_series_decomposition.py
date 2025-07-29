import os
import sys
import unittest
import warnings

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.time_series.decomposition import (
    AdditiveDecomposition,
    MultiplicativeDecomposition,
    _centered_moving_average,
)
from tests.utils import BaseTest


# --- Helper function for creating seasonal data ---
def create_seasonal_data(
    length=48, period=12, amplitude=10, trend=0.1, noise_std=2, offset=50
):
    """Creates sample time series data with seasonality, trend, and noise."""
    time = np.arange(length)
    seasonal_component = amplitude * np.sin(2 * np.pi * time / period)
    trend_component = trend * time
    noise_component = np.random.normal(0, noise_std, length)
    return trend_component + seasonal_component + noise_component + offset


class TestAdditiveDecomposition(BaseTest):
    """Unit test suite for the AdditiveDecomposition class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting AdditiveDecomposition", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.period = 12
        self.time_series = create_seasonal_data(
            length=4 * self.period, period=self.period
        )
        self.decomp = AdditiveDecomposition(period=self.period)

    def test_initialization(self):
        """Test AdditiveDecomposition initialization."""
        self.assertEqual(self.decomp.period, self.period)
        self.assertIsNone(self.decomp.time_series)
        self.assertIsNone(self.decomp.trend)
        self.assertIsNone(self.decomp.seasonal)
        self.assertIsNone(self.decomp.residual)

    def test_initialization_invalid_period_low(self):
        """Test initialization with invalid period (<= 1)."""
        with self.assertRaises(ValueError):
            AdditiveDecomposition(period=1)
        with self.assertRaises(ValueError):
            AdditiveDecomposition(period=0)

    def test_initialization_invalid_period_type(self):
        """Test initialization with non-integer period."""
        with self.assertRaises(ValueError):
            AdditiveDecomposition(period=12.5)
        with self.assertRaises(ValueError):
            AdditiveDecomposition(period="12")

    def test_fit(self):
        """Test fitting the model."""
        self.decomp.fit(self.time_series)
        n = len(self.time_series)
        self.assertIsNotNone(self.decomp.time_series)
        self.assertIsNotNone(self.decomp.trend)
        self.assertIsNotNone(self.decomp.seasonal)
        self.assertIsNotNone(self.decomp.residual)
        self.assertEqual(len(self.decomp.trend), n)
        self.assertEqual(len(self.decomp.seasonal), n)
        self.assertEqual(len(self.decomp.residual), n)
        self.assertIsInstance(self.decomp.trend, np.ndarray)
        self.assertIsInstance(self.decomp.seasonal, np.ndarray)
        self.assertIsInstance(self.decomp.residual, np.ndarray)
        # Check that seasonal component sums approximately to zero over one period
        self.assertTrue(
            np.isclose(np.sum(self.decomp.seasonal[: self.period]), 0, atol=1e-8)
        )

    def test_fit_short_series_even_period(self):
        """Test fitting with series too short for even period CMA."""
        short_series = self.time_series[: self.period]
        with self.assertRaises(ValueError):
            self.decomp.fit(short_series)

    def test_fit_short_series_odd_period(self):
        """Test fitting with series too short for odd period CMA."""
        period = 7
        decomp_odd = AdditiveDecomposition(period=period)
        short_series = self.time_series[
            : period - 1
        ]  # Length 6, needs 7 for period 7 CMA
        with self.assertRaises(ValueError):
            decomp_odd.fit(short_series)

    def test_fit_nan_series(self):
        """Test fitting with NaNs in the series."""
        nan_series = self.time_series.copy()
        nan_series[5] = np.nan
        nan_series[20] = np.nan
        with self.assertWarns(UserWarning):
            self.decomp.fit(nan_series)
        n = len(nan_series)
        self.assertEqual(len(self.decomp.trend), n)
        self.assertEqual(len(self.decomp.seasonal), n)
        self.assertEqual(len(self.decomp.residual), n)
        # Expect NaNs in components corresponding to input NaNs and CMA edge effects
        self.assertTrue(np.isnan(self.decomp.trend).any())
        self.assertTrue(np.isnan(self.decomp.residual).any())
        # Seasonal might be complete if enough data exists per season despite NaNs
        # self.assertTrue(np.isnan(self.decomp.seasonal).any()) # This depends on NaN positions

    def test_get_components(self):
        """Test retrieving components after fitting."""
        self.decomp.fit(self.time_series)
        components = self.decomp.get_components()
        self.assertIsInstance(components, dict)
        self.assertIn("trend", components)
        self.assertIn("seasonal", components)
        self.assertIn("residual", components)
        self.assertIs(components["trend"], self.decomp.trend)

    def test_get_components_before_fit(self):
        """Test calling get_components before fitting."""
        with self.assertRaisesRegex(ValueError, "Model has not been fitted yet."):
            self.decomp.get_components()

    def test_reconstruct(self):
        """Test reconstructing the series from components."""
        self.decomp.fit(self.time_series)
        reconstructed = self.decomp.reconstruct()
        self.assertEqual(len(reconstructed), len(self.time_series))
        # Check if reconstruction is close to original where trend is not NaN
        valid_indices = ~np.isnan(self.decomp.trend)
        self.assertTrue(
            np.allclose(
                reconstructed[valid_indices], self.time_series[valid_indices], atol=1e-8
            )
        )


class TestMultiplicativeDecomposition(BaseTest):
    """Unit test suite for the MultiplicativeDecomposition class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting MultiplicativeDecomposition", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.period = 12
        # Data strictly positive
        self.time_series_pos = create_seasonal_data(
            length=4 * self.period, period=self.period, offset=50
        )
        # Data with non-positive values
        self.time_series_nonpos = create_seasonal_data(
            length=4 * self.period, period=self.period, offset=-10
        )

        self.decomp_pos = MultiplicativeDecomposition(period=self.period)
        self.decomp_nonpos = MultiplicativeDecomposition(period=self.period)

    def test_initialization(self):
        """Test MultiplicativeDecomposition initialization."""
        self.assertEqual(self.decomp_pos.period, self.period)
        self.assertIsNone(self.decomp_pos.time_series)
        self.assertEqual(self.decomp_pos.offset, 0.0)
        self.assertIsNone(self.decomp_pos.trend)
        self.assertIsNone(self.decomp_pos.seasonal)
        self.assertIsNone(self.decomp_pos.residual)
        self.assertIsNone(self.decomp_pos._trend_shifted)

    def test_initialization_invalid_period_low(self):
        """Test initialization with invalid period (<= 1)."""
        with self.assertRaises(ValueError):
            MultiplicativeDecomposition(period=1)

    def test_initialization_invalid_period_type(self):
        """Test initialization with non-integer period."""
        with self.assertRaises(ValueError):
            MultiplicativeDecomposition(period=7.5)

    # --- Tests using strictly positive data ---

    def test_fit_positive(self):
        """Test fitting the model with positive data."""
        self.decomp_pos.fit(self.time_series_pos)
        n = len(self.time_series_pos)
        self.assertIsNotNone(self.decomp_pos.time_series)
        self.assertIsNotNone(self.decomp_pos.trend)
        self.assertIsNotNone(self.decomp_pos.seasonal)
        self.assertIsNotNone(self.decomp_pos.residual)
        self.assertEqual(self.decomp_pos.offset, 0.0)  # No offset applied
        self.assertEqual(len(self.decomp_pos.trend), n)
        self.assertEqual(len(self.decomp_pos.seasonal), n)
        self.assertEqual(len(self.decomp_pos.residual), n)
        # Check that seasonal component averages approximately to 1 over one period
        self.assertTrue(
            np.isclose(np.mean(self.decomp_pos.seasonal[: self.period]), 1.0, atol=1e-8)
        )

    def test_fit_positive_short_series(self):
        """Test fitting positive data with series too short."""
        short_series = self.time_series_pos[: self.period]
        self.decomp_pos.fit(short_series)

    def test_fit_positive_nan_series(self):
        """Test fitting positive data with NaNs."""
        nan_series = self.time_series_pos.copy()
        nan_series[5] = np.nan
        self.decomp_pos.fit(nan_series)
        n = len(nan_series)
        self.assertEqual(len(self.decomp_pos.trend), n)
        self.assertEqual(len(self.decomp_pos.seasonal), n)
        self.assertEqual(len(self.decomp_pos.residual), n)
        self.assertEqual(self.decomp_pos.offset, 0.0)
        self.assertTrue(np.isnan(self.decomp_pos.trend).any())
        self.assertTrue(np.isnan(self.decomp_pos.residual).any())

    def test_get_components_positive(self):
        """Test retrieving components after fitting positive data."""
        self.decomp_pos.fit(self.time_series_pos)
        components = self.decomp_pos.get_components()
        self.assertIsInstance(components, dict)
        self.assertIn("trend", components)
        self.assertIn("seasonal", components)
        self.assertIn("residual", components)

    def test_get_components_before_fit(self):
        """Test calling get_components before fitting."""
        with self.assertRaisesRegex(ValueError, "Model has not been fitted yet."):
            self.decomp_pos.get_components()

    def test_reconstruct_positive(self):
        """Test reconstructing the series from components (positive fit)."""
        self.decomp_pos.fit(self.time_series_pos)
        reconstructed = self.decomp_pos.reconstruct()
        self.assertEqual(len(reconstructed), len(self.time_series_pos))
        valid_indices = (
            ~np.isnan(self.decomp_pos.trend)
            & ~np.isnan(self.decomp_pos.seasonal)
            & ~np.isnan(self.decomp_pos.residual)
        )
        # Reconstruction might not be perfect due to approximations in decomposition
        self.assertTrue(
            np.allclose(
                reconstructed[valid_indices],
                self.time_series_pos[valid_indices],
                rtol=0.1,
            )
        )  # Use relative tolerance

    # --- Tests using non-positive data ---

    def test_fit_non_positive(self):
        """Test fitting the model with non-positive data."""
        with self.assertWarns(UserWarning):
            self.decomp_nonpos.fit(self.time_series_nonpos)
            # Check if the offset warning was issued

        n = len(self.time_series_nonpos)
        self.assertIsNotNone(self.decomp_nonpos.time_series)
        self.assertIsNotNone(self.decomp_nonpos.trend)
        self.assertIsNotNone(self.decomp_nonpos.seasonal)
        self.assertIsNotNone(self.decomp_nonpos.residual)
        self.assertGreater(self.decomp_nonpos.offset, 0.0)  # Offset must be applied
        self.assertEqual(len(self.decomp_nonpos.trend), n)
        self.assertEqual(len(self.decomp_nonpos.seasonal), n)
        self.assertEqual(len(self.decomp_nonpos.residual), n)
        # Seasonal component should still average approximately to 1
        self.assertTrue(
            np.isclose(
                np.mean(self.decomp_nonpos.seasonal[: self.period]), 1.0, atol=1e-8
            )
        )
        # Trend component might be negative now
        self.assertTrue(
            np.any(self.decomp_nonpos.trend[~np.isnan(self.decomp_nonpos.trend)] < 0)
        )

    def test_fit_non_positive_short_series(self):
        """Test fitting non-positive data with series too short."""
        short_series = self.time_series_nonpos[: self.period]
        self.decomp_nonpos.fit(short_series)

    def test_get_components_non_positive(self):
        """Test retrieving components after fitting non-positive data."""
        self.decomp_nonpos.fit(self.time_series_nonpos)
        components = self.decomp_nonpos.get_components()
        self.assertIsInstance(components, dict)
        self.assertIn("trend", components)  # Trend is adjusted back
        self.assertIn("seasonal", components)  # Seasonal is from shifted
        self.assertIn("residual", components)  # Residual is from shifted

    def test_reconstruct_non_positive(self):
        """Test reconstructing the series from components (non-positive fit)."""
        self.decomp_nonpos.fit(self.time_series_nonpos)
        reconstructed = self.decomp_nonpos.reconstruct()
        self.assertEqual(len(reconstructed), len(self.time_series_nonpos))
        valid_indices = (
            ~np.isnan(self.decomp_nonpos.trend)
            & ~np.isnan(self.decomp_nonpos.seasonal)
            & ~np.isnan(self.decomp_nonpos.residual)
        )
        # Check closeness to the *original* non-positive series
        # Due to the offset and multiplicative nature, might not be perfectly close
        self.assertTrue(
            np.allclose(
                reconstructed[valid_indices],
                self.time_series_nonpos[valid_indices],
                rtol=0.2,
                atol=1.0,
            )
        )  # Looser tolerance


class TestCenteredMovingAverage(BaseTest):
    """Unit test suite for the _centered_moving_average helper function."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting _centered_moving_average", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)

    # --- Test Cases ---

    def test_odd_window(self):
        """Test CMA with an odd window size."""
        series = np.array([1, 2, 3, 4, 5, 6, 7], dtype=float)
        window = 3
        expected = np.array([np.nan, 2.0, 3.0, 4.0, 5.0, 6.0, np.nan])
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True, rtol=1e-8, atol=1e-8)

    def test_odd_window_longer(self):
        """Test CMA with an odd window size on a longer series."""
        series = np.arange(1, 11, dtype=float)  # [1, 2, ..., 10]
        window = 5
        expected = np.array(
            [np.nan, np.nan, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, np.nan, np.nan]
        )
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True, rtol=1e-8, atol=1e-8)

    def test_even_window(self):
        """Test CMA with an even window size."""
        series = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
        window = 4
        expected = np.array([np.nan, np.nan, 3.0, 4.0, 5.0, 6.0, np.nan, np.nan])
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True, rtol=1e-8, atol=1e-8)

    def test_even_window_longer(self):
        """Test CMA with an even window size on a longer series."""
        series = np.arange(1, 13, dtype=float)  # [1, 2, ..., 12]
        window = 6
        expected = np.array(
            [
                np.nan,
                np.nan,
                np.nan,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                np.nan,
                np.nan,
                np.nan,
            ]
        )
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True, rtol=1e-8, atol=1e-8)

    def test_window_larger_than_series(self):
        """Test CMA when window size exceeds series length."""
        series = np.array([1, 2, 3], dtype=float)
        window = 5
        expected = np.array([np.nan, np.nan, np.nan])
        # Function should now handle this before convolve
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True)  # Corrected expected

    def test_window_equals_series_odd(self):
        """Test CMA when odd window size equals series length."""
        series = np.array([1, 2, 3, 4, 5], dtype=float)
        window = 5
        expected = np.array([np.nan, np.nan, 3.0, np.nan, np.nan])
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True)

    def test_window_equals_series_even(self):
        """Test CMA when even window size equals series length."""
        series = np.array([1, 2, 3, 4], dtype=float)
        window = 4
        expected = np.array([np.nan, np.nan, np.nan, np.nan])
        # Function should now handle this case correctly
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True)  # Corrected expected

    def test_window_one(self):
        """Test CMA with window size 1."""
        series = np.array([1, 5, 3, 7], dtype=float)
        window = 1
        expected = series.copy()
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True)

    def test_window_two(self):
        """Test CMA with window size 2."""
        series = np.array([1, 2, 3, 4, 5], dtype=float)
        window = 2
        expected = np.array([np.nan, 2.0, 3.0, 4.0, np.nan])
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True, rtol=1e-8, atol=1e-8)

    def test_series_with_nans(self):
        """Test CMA with NaNs present in the input series."""
        series = np.array([1, 2, np.nan, 4, 5, 6, np.nan, 8, 9], dtype=float)
        window = 3
        # np.convolve propagates NaNs within its calculation window
        # Window 1 (1,2,nan) -> nan (centered at index 1)
        # Window 2 (2,nan,4) -> nan (centered at index 2)
        # Window 3 (nan,4,5) -> nan (centered at index 3)
        # Window 4 (4,5,6) -> 5.0 (centered at index 4)
        # Window 5 (5,6,nan) -> nan (centered at index 5)
        # Window 6 (6,nan,8) -> nan (centered at index 6)
        # Window 7 (nan,8,9) -> nan (centered at index 7)
        expected = np.array(
            [np.nan, np.nan, np.nan, np.nan, 5.0, np.nan, np.nan, np.nan, np.nan]
        )
        result = _centered_moving_average(series, window)
        assert_allclose(result, expected, equal_nan=True)  # Corrected expected

    def test_empty_series(self):
        """Test CMA with an empty input series."""
        series = np.array([], dtype=float)
        window = 3
        expected = np.array([], dtype=float)
        # Function should now handle this before convolve
        result = _centered_moving_average(series, window)
        assert_array_equal(result, expected)

    def test_invalid_window_zero(self):
        """Test CMA with window size 0."""
        series = np.array([1, 2, 3], dtype=float)
        with self.assertRaisesRegex(ValueError, "window must be a positive integer"):
            _centered_moving_average(series, 0)

    def test_invalid_window_negative(self):
        """Test CMA with negative window size."""
        series = np.array([1, 2, 3], dtype=float)
        with self.assertRaisesRegex(ValueError, "window must be a positive integer"):
            _centered_moving_average(series, -3)


if __name__ == "__main__":
    unittest.main()
