import warnings

import numpy as np


def _centered_moving_average(series, window):
    """Calculates centered moving average, handling even/odd windows."""
    series = np.asarray(series, dtype=float)
    n = len(series)

    # --- Start: Added Edge Case Handling ---
    if not isinstance(window, int) or window <= 0:
        raise ValueError("window must be a positive integer")
    if n == 0:
        return np.array([], dtype=float)  # Handle empty series
    if window == 1:
        return series.copy()  # MA of 1 is the series itself
    if window > n:
        # Cannot compute any full window average
        return np.full(n, np.nan)  # Handle window > series length
    # --- End: Added Edge Case Handling ---

    if window % 2 == 1:  # Odd window
        weights = np.repeat(1.0, window) / window
        cma = np.convolve(series, weights, "valid")
        # Check if convolution result is empty (shouldn't happen if window <= n)
        if len(cma) == 0:
            return np.full(n, np.nan)
        pad_size = (n - len(cma)) // 2
        right_pad = n - len(cma) - pad_size
        return np.pad(cma, (pad_size, right_pad), constant_values=np.nan)
    else:  # Even window -> 2xMA
        # First MA of window `window`
        ma1 = np.convolve(series, np.repeat(1.0, window) / window, "valid")

        # --- Start: Corrected Even Window Logic ---
        # Check if enough points exist for the second MA(2)
        if len(ma1) < 2:
            # This happens if n = window or n = window + 1
            return np.full(n, np.nan)
        # --- End: Corrected Even Window Logic ---

        # Second MA of order 2 on the result, centered correctly
        weights2 = np.repeat(1.0, 2) / 2
        cma = np.convolve(ma1, weights2, "valid")
        # Check if second convolution result is empty (shouldn't happen if len(ma1) >= 2)
        if len(cma) == 0:
            return np.full(n, np.nan)

        # Correct padding for 2xMA centered
        pad_size = window // 2  # Effective padding from start and end
        right_pad = n - len(cma) - pad_size
        return np.pad(cma, (pad_size, right_pad), constant_values=np.nan)


class AdditiveDecomposition:
    """Performs classical additive decomposition of a time series.

    Decomposes the series Y into Trend (T), Seasonal (S), and Residual (R) components
    such that Y = T + S + R. Assumes seasonality is constant over time.

    Attributes:
        period (int): The seasonal period.
        time_series (np.ndarray): The original time series data.
        trend (np.ndarray): The estimated trend component.
        seasonal (np.ndarray): The estimated seasonal component.
        residual (np.ndarray): The estimated residual component.
    """

    def __init__(self, period):
        """Initialize the AdditiveDecomposition model.

        Args:
            period (int): The seasonal period (e.g., 12 for monthly, 7 for daily). Must be > 1.
        """
        if not isinstance(period, int) or period <= 1:
            raise ValueError("Period must be an integer greater than 1.")
        self.period = period
        self.time_series = None
        self.trend = None
        self.seasonal = None
        self.residual = None

    def __name__(self):
        return "AdditiveDecomposition"

    def __str__(self):
        return f"AdditiveDecomposition(period={self.period})"

    def fit(self, time_series):
        """Perform additive decomposition on the time series.

        Args:
            time_series (array-like): The time series data. Must be 1-dimensional and have length >= 2 * period.

        Returns:
            tuple: The calculated trend, seasonal, and residual components.
        """
        self.time_series = np.asarray(time_series, dtype=float).flatten()
        n = len(self.time_series)

        if n < 2 * self.period:
            raise ValueError(
                f"Time series length ({n}) must be at least twice the period ({self.period})."
            )
        if np.isnan(self.time_series).any():
            warnings.warn(
                "Time series contains NaNs. Decomposition results may be affected.",
                UserWarning,
                stacklevel=2,
            )

        # 1. Estimate Trend (T) using centered moving average
        self.trend = _centered_moving_average(self.time_series, self.period)

        # 2. Detrend the series: Y_detrended = Y - T
        detrended = self.time_series - self.trend  # Contains NaNs where trend is NaN

        # 3. Estimate Seasonal component (S)
        # Average the detrended values for each season
        seasonal_factors = np.full(self.period, np.nan)
        for i in range(self.period):
            # Get all detrended values for season i (0, p, 2p, ...)
            season_values = detrended[i :: self.period]
            # Calculate mean ignoring NaNs
            if not np.all(np.isnan(season_values)):
                seasonal_factors[i] = np.nanmean(season_values)

        # Adjust seasonal factors to sum to zero
        if not np.isnan(seasonal_factors).any():
            seasonal_factors -= np.mean(seasonal_factors)
        else:
            warnings.warn(
                "Could not estimate all seasonal factors due to NaNs. Seasonal component might be incomplete.",
                UserWarning,
                stacklevel=2,
            )

        # Tile the seasonal factors to match the length of the series
        self.seasonal = np.tile(seasonal_factors, n // self.period + 1)[:n]

        # 4. Estimate Residual component (R): R = Y - T - S
        self.residual = self.time_series - self.trend - self.seasonal

        # Optionally, fill NaNs at ends of components if desired (e.g., with zeros or mean)
        # For simplicity, we leave them as NaNs here.

        return self.trend, self.seasonal, self.residual

    def get_components(self):
        """Return the calculated components."""
        if self.trend is None:
            raise ValueError("Model has not been fitted yet.")
        return {
            "trend": self.trend,
            "seasonal": self.seasonal,
            "residual": self.residual,
        }

    def reconstruct(self):
        """Reconstruct the series from components (Y = T + S + R)."""
        components = self.get_components()
        # Use nan_to_num to handle potential NaNs if adding them directly
        return np.nansum(
            [components["trend"], components["seasonal"], components["residual"]],
            axis=0,
        )


class MultiplicativeDecomposition:
    """Performs classical multiplicative decomposition of a time series.

    Decomposes the series Y into Trend (T), Seasonal (S), and Residual (R) components
    such that Y = T * S * R. Assumes seasonality changes proportionally to the trend.

    Handles non-positive values by shifting the data to be positive before decomposition.
    Note: This affects the interpretation of the components.

    Attributes:
        period (int): The seasonal period.
        time_series (np.ndarray): The original time series data.
        offset (float): The offset added to the series to make it positive (0 if originally positive).
        trend (np.ndarray): The estimated trend component (adjusted back to original scale).
        seasonal (np.ndarray): The estimated seasonal component (from shifted data).
        residual (np.ndarray): The estimated residual component (from shifted data).
        _trend_shifted (np.ndarray): Internal storage of trend from shifted data.
    """

    def __init__(self, period):
        """Initialize the MultiplicativeDecomposition model.

        Args:
            period (int): The seasonal period (e.g., 12 for monthly, 7 for daily). Must be > 1.
        """
        if not isinstance(period, int) or period <= 1:
            raise ValueError("Period must be an integer greater than 1.")
        self.period = period
        self.time_series = None
        self.offset = 0.0  # Initialize offset to 0
        self.trend = None
        self.seasonal = None
        self.residual = None
        self._trend_shifted = None  # To help with reconstruction

    def __name__(self):
        return "MultiplicativeDecomposition"

    def __str__(self):
        return f"MultiplicativeDecomposition(period={self.period})"

    def fit(self, time_series):
        """Perform multiplicative decomposition on the time series.

        If the series contains non-positive values, it is shifted before decomposition.
        This is done to ensure positivity of the seasonal component, but affects the
        interpretation of the components.

        Args:
            time_series (array-like): The time series data. Must be 1-dimensional,and have length >= 2 * period.

        Returns:
            tuple: The calculated trend, seasonal, and residual components.
        """
        original_series = np.asarray(time_series, dtype=float).flatten()
        n = len(original_series)
        self.time_series = original_series  # Store original

        # Check length relative to period first
        if n < self.period:
            raise ValueError(
                f"Time series length ({n}) must be at least the period ({self.period})."
            )

        # Basic check for enough data for CMA (period+1 for even window CMA)
        min_len_for_cma = self.period + (self.period % 2 == 0)
        if n < min_len_for_cma:
            # Allow continuation but results might be mostly NaN
            warnings.warn(
                f"Time series length ({n}) is very short relative to period ({self.period}). Trend estimation might be poor or fail.",
                UserWarning,
                stacklevel=2,
            )

        # Check for non-positive values and apply shift if necessary
        # Use nanmin to handle potential NaNs
        min_val = np.nanmin(original_series)
        if min_val <= 0:
            # Add 1 to ensure strict positivity
            self.offset = abs(min_val) + 1.0
            shifted_series = original_series + self.offset
            warnings.warn(
                f"Time series contains non-positive values. Applying an offset of {self.offset:.4f} before decomposition. Component interpretation is affected.",
                UserWarning,
                stacklevel=2,
            )
        else:
            self.offset = 0.0
            shifted_series = original_series.copy()

        # --- From here on, decomposition steps operate on shifted_series! ---

        # 1. Estimate Trend (T_shifted) using centered moving average on shifted data
        trend_shifted = _centered_moving_average(shifted_series, self.period)
        self._trend_shifted = trend_shifted  # Store for reconstruction

        # Check if trend calculation resulted in all NaNs (can happen if series is too short)
        if np.all(np.isnan(trend_shifted)):
            warnings.warn(
                "Trend estimation resulted in all NaNs. Decomposition cannot proceed meaningfully.",
                UserWarning,
                stacklevel=2,
            )
            # Set components to NaN and return
            self.trend = np.full(n, np.nan)
            self.seasonal = np.full(n, np.nan)
            self.residual = np.full(n, np.nan)
            return

        # 2. Detrend the shifted series: Y_detrended_shifted = Y_shifted / T_shifted
        with np.errstate(divide="ignore", invalid="ignore"):
            # Ensure trend_shifted has non-zero values where division happens
            safe_trend_shifted = trend_shifted.copy()
            # Avoid division by zero or near-zero, replace with NaN
            safe_trend_shifted[np.isclose(safe_trend_shifted, 0)] = np.nan
            detrended_shifted = shifted_series / safe_trend_shifted

        # 3. Estimate Seasonal component (S) from shifted detrended data
        seasonal_factors = np.full(self.period, np.nan)
        for i in range(self.period):
            season_values = detrended_shifted[i :: self.period]
            finite_season_values = season_values[np.isfinite(season_values)]
            if len(finite_season_values) > 0:
                seasonal_factors[i] = np.mean(finite_season_values)
            # If no finite values, seasonal_factors[i] remains NaN

        # Check if all seasonal factors could be estimated
        if np.isnan(seasonal_factors).any():
            warnings.warn(
                "Could not estimate all seasonal factors due to NaNs/Infs. Seasonal component might be incomplete or NaN.",
                UserWarning,
                stacklevel=2,
            )
            # Normalize only if all factors are finite
            if not np.isnan(
                seasonal_factors
            ).all():  # Check if at least one factor exists
                mean_sf = np.nanmean(seasonal_factors)
                if not np.isclose(mean_sf, 0):
                    seasonal_factors /= mean_sf  # Normalize towards 1
                else:  # Handle case where mean is zero (unlikely but possible)
                    warnings.warn(
                        "Mean of estimated seasonal factors is zero. Cannot normalize.",
                        UserWarning,
                        stacklevel=2,
                    )
        else:
            # Normalize seasonal factors to average to 1 (only if all are finite)
            mean_sf = np.mean(seasonal_factors)
            if not np.isclose(mean_sf, 0):
                seasonal_factors /= mean_sf
            else:
                warnings.warn(
                    "Mean of estimated seasonal factors is zero. Cannot normalize.",
                    UserWarning,
                    stacklevel=2,
                )

        # Tile the seasonal factors to match the length of the series
        self.seasonal = np.tile(seasonal_factors, n // self.period + 1)[:n]

        # 4. Estimate Residual component (R) from shifted data: R = Y_shifted / (T_shifted * S)
        with np.errstate(divide="ignore", invalid="ignore"):
            denominator = trend_shifted * self.seasonal
            # Avoid division by zero/NaN in denominator
            denominator[np.isclose(denominator, 0) | ~np.isfinite(denominator)] = np.nan
            self.residual = shifted_series / denominator
            # Ensure non-finite residuals are NaN
            self.residual[~np.isfinite(self.residual)] = np.nan

        # 5. Adjust Trend component back to the original scale
        # T = T_shifted - offset
        self.trend = trend_shifted - self.offset

        return self.trend, self.seasonal, self.residual

    def get_components(self):
        """Return the calculated components.

        Note: Trend is adjusted back to original scale. Seasonal and Residual
              are derived from the shifted data if an offset was applied.
        """
        if self.trend is None:
            raise ValueError("Model has not been fitted yet.")
        return {
            "trend": self.trend,  # Adjusted back
            "seasonal": self.seasonal,  # From shifted data
            "residual": self.residual,  # From shifted data
        }

    def reconstruct(self):
        """Reconstruct the series from components.

        Accounts for any offset applied during fitting.
        Reconstruction formula: Y_recon = T_shifted * S * R - offset
                                    = (T + offset) * S * R - offset
        """
        if self.trend is None or self.seasonal is None or self.residual is None:
            raise ValueError("Model has not been fitted yet. Cannot reconstruct.")

        # Use the stored shifted trend (_trend_shifted) or recalculate (T + offset)
        trend_shifted = (
            self._trend_shifted
            if self._trend_shifted is not None
            else self.trend + self.offset
        )

        # Calculate reconstruction on the shifted scale
        reconstructed_shifted = trend_shifted * self.seasonal * self.residual

        # Shift back to the original scale
        reconstructed_original = reconstructed_shifted - self.offset

        return reconstructed_original
