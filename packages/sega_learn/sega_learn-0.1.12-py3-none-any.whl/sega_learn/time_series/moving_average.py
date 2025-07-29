import warnings

import numpy as np


class SimpleMovingAverage:
    """Calculates the Simple Moving Average (SMA) of a time series.

    SMA smooths out fluctuations by averaging data over a defined window.

    Attributes:
        window (int): The number of periods in the moving average window.
        smoothed_values (np.ndarray): The calculated SMA values. NaNs prepended.
        model (np.ndarray): The original time series data.
    """

    def __init__(self, window):
        """Initialize SMA calculator.

        Args:
            window (int): The size of the moving window. Must be > 0.
        """
        if not isinstance(window, int) or window <= 0:
            raise ValueError("Window must be a positive integer.")
        self.window = window
        self.smoothed_values = None
        self.model = None
        self._last_ma = None  # Store the last calculated MA value for forecasting

    def __name__(self):
        return "SimpleMovingAverage"

    def __str__(self):
        return f"SimpleMovingAverage(window={self.window})"

    def fit(self, time_series):
        """Calculate the Simple Moving Average for the series.

        Args:
            time_series (array-like): The time series data (1-dimensional).
        """
        self.model = np.asarray(time_series, dtype=float).flatten()
        n = len(self.model)
        if n == 0:
            self.smoothed_values = np.array([])
            self._last_ma = np.nan
            return
        if n < self.window:
            warnings.warn(
                f"Series length ({n}) is shorter than window size ({self.window}). Result will be all NaNs.",
                UserWarning,
                stacklevel=2,
            )
            self.smoothed_values = np.full(n, np.nan)
            self._last_ma = np.nan
            return

        # Use convolution for efficient calculation
        weights = np.repeat(1.0, self.window) / self.window
        # 'valid' mode ensures only full windows are used
        ma_values = np.convolve(self.model, weights, "valid")

        # Prepend NaNs for the initial periods where MA isn't calculable
        num_nans = n - len(ma_values)
        self.smoothed_values = np.pad(ma_values, (num_nans, 0), constant_values=np.nan)
        self._last_ma = ma_values[-1] if len(ma_values) > 0 else np.nan

        return self.smoothed_values

    def get_smoothed(self):
        """Return the calculated moving average series."""
        if self.smoothed_values is None:
            raise ValueError("Model has not been fitted yet.")
        return self.smoothed_values

    def forecast(self, steps):
        """Generate forecasts using the last calculated moving average value.

        Note: This is a naive forecast where the future is predicted to be the
        last known smoothed value.

        Args:
            steps (int): The number of steps to forecast ahead.

        Returns:
            np.ndarray: An array of forecasted values (all the same).
        """
        if self.smoothed_values is None:
            raise ValueError("Model has not been fitted yet.")
        if steps <= 0:
            return np.array([])
        if np.isnan(self._last_ma):
            warnings.warn(
                "Last moving average value is NaN, cannot forecast.",
                UserWarning,
                stacklevel=2,
            )
            return np.full(steps, np.nan)

        return np.full(steps, self._last_ma)


class WeightedMovingAverage:
    """Calculates the Weighted Moving Average (WMA) of a time series.

    WMA assigns different weights to data points within the window, typically giving
    more importance to recent observations.

    Attributes:
        window (int): The number of periods in the moving average window.
        weights (np.ndarray): The weights assigned to observations in the window.
        smoothed_values (np.ndarray): The calculated WMA values. NaNs prepended.
        model (np.ndarray): The original time series data.
    """

    def __init__(self, window, weights=None):
        """Initialize WMA calculator.

        Args:
            window (int): The size of the moving window. Must be > 0.
            weights (array-like, optional): A sequence of weights for the window.
                Length must match `window`. If None, linear weights giving more
                importance to recent points are used (e.g., [1, 2, 3] for window=3).
                Weights are normalized to sum to 1.
        """
        if not isinstance(window, int) or window <= 0:
            raise ValueError("Window must be a positive integer.")
        self.window = window

        if weights is None:
            # Default to linear weights (1, 2, ..., window) -> recent points get higher weight
            raw_weights = np.arange(1, window + 1)
        else:
            raw_weights = np.asarray(weights, dtype=float)
            if len(raw_weights) != window:
                raise ValueError(
                    f"Length of weights ({len(raw_weights)}) must match window size ({window})."
                )
            if np.any(raw_weights < 0):
                warnings.warn(
                    "Weights contain negative values.", UserWarning, stacklevel=2
                )

        # Normalize weights to sum to 1
        weight_sum = np.sum(raw_weights)
        if np.isclose(weight_sum, 0):
            # Avoid division by zero if all weights are zero
            warnings.warn(
                "Sum of weights is close to zero. Using equal weights instead.",
                UserWarning,
                stacklevel=2,
            )
            self.weights = np.repeat(1.0 / window, window)
        else:
            self.weights = raw_weights / weight_sum
            # Weights are applied chronologically: weights[0] applies to oldest point in window
            # For convolution, weights need to be reversed.
            self._convolution_weights = self.weights[::-1]

        self.smoothed_values = None
        self.model = None
        self._last_ma = None

    def __name__(self):
        return "WeightedMovingAverage"

    def __str__(self):
        return f"WeightedMovingAverage(window={self.window}, weights={self.weights})"

    def fit(self, time_series):
        """Calculate the Weighted Moving Average for the series.

        Args:
            time_series (array-like): The time series data (1-dimensional).
        """
        self.model = np.asarray(time_series, dtype=float).flatten()
        n = len(self.model)
        if n == 0:
            self.smoothed_values = np.array([])
            self._last_ma = np.nan
            return
        if n < self.window:
            warnings.warn(
                f"Series length ({n}) is shorter than window size ({self.window}). Result will be all NaNs.",
                UserWarning,
                stacklevel=2,
            )
            self.smoothed_values = np.full(n, np.nan)
            self._last_ma = np.nan
            return

        # Use convolution with the reversed weights
        ma_values = np.convolve(self.model, self._convolution_weights, "valid")

        # Prepend NaNs
        num_nans = n - len(ma_values)
        self.smoothed_values = np.pad(ma_values, (num_nans, 0), constant_values=np.nan)
        self._last_ma = ma_values[-1] if len(ma_values) > 0 else np.nan

        return self.smoothed_values

    def get_smoothed(self):
        """Return the calculated moving average series."""
        if self.smoothed_values is None:
            raise ValueError("Model has not been fitted yet.")
        return self.smoothed_values

    def forecast(self, steps):
        """Generate forecasts using the last calculated weighted moving average value.

        Note: This is a naive forecast.

        Args:
            steps (int): The number of steps to forecast ahead.

        Returns:
            np.ndarray: An array of forecasted values (all the same).
        """
        if self.smoothed_values is None:
            raise ValueError("Model has not been fitted yet.")
        if steps <= 0:
            return np.array([])
        if np.isnan(self._last_ma):
            warnings.warn(
                "Last moving average value is NaN, cannot forecast.",
                UserWarning,
                stacklevel=2,
            )
            return np.full(steps, np.nan)

        return np.full(steps, self._last_ma)


class ExponentialMovingAverage:
    """Calculates the Exponential Moving Average (EMA) of a time series.

    EMA gives more weight to recent observations, making it more responsive to new information.

    Attributes:
        alpha (float): The smoothing factor (0 < alpha < 1).
        smoothed_values (np.ndarray): The calculated EMA values. NaNs prepended.
        model (np.ndarray): The original time series data.
    """

    def __init__(self, alpha):
        """Initialize EMA calculator.

        Args:
            alpha (float): The smoothing factor (0 < alpha < 1).
        """
        if not (0 < alpha < 1):
            raise ValueError("Alpha must be between 0 and 1 (exclusive).")
        self.alpha = alpha
        self.smoothed_values = None
        self.model = None
        self._last_ema = None  # Store the last calculated EMA value for forecasting

    def __name__(self):
        return "ExponentialMovingAverage"

    def __str__(self):
        return f"ExponentialMovingAverage(alpha={self.alpha})"

    def fit(self, time_series):
        """Calculate the Exponential Moving Average for the series.

        Args:
            time_series (array-like): The time series data (1-dimensional).
        """
        self.model = np.asarray(time_series, dtype=float).flatten()
        n = len(self.model)
        if n == 0:
            self.smoothed_values = np.array([])
            self._last_ema = np.nan
            return

        ema_values = np.empty(n)
        ema_values[:] = np.nan  # Initialize with NaNs

        # First EMA value is the first data point
        ema_values[0] = self.model[0]
        for i in range(1, n):
            ema_values[i] = (
                self.alpha * self.model[i] + (1 - self.alpha) * ema_values[i - 1]
            )

        self.smoothed_values = ema_values
        self._last_ema = ema_values[-1]

        return self.smoothed_values

    def get_smoothed(self):
        """Return the calculated EMA series."""
        if self.smoothed_values is None:
            raise ValueError("Model has not been fitted yet.")
        return self.smoothed_values

    def forecast(self, steps):
        """Generate forecasts using the last calculated EMA value.

        Note: This is a naive forecast where the future is predicted to be the
        last known smoothed value.

        Args:
            steps (int): The number of steps to forecast ahead.

        Returns:
            np.ndarray: An array of forecasted values (all the same).
        """
        if self.smoothed_values is None:
            raise ValueError("Model has not been fitted yet.")
        if steps <= 0:
            return np.array([])
        if np.isnan(self._last_ema):
            warnings.warn(
                "Last EMA value is NaN, cannot forecast.",
                UserWarning,
                stacklevel=2,
            )
            return np.full(steps, np.nan)

        return np.full(steps, self._last_ema)
