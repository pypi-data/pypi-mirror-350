import warnings

import numpy as np

from sega_learn.utils import Metrics

mean_squared_error = Metrics.mean_squared_error


class SimpleExponentialSmoothing:
    """Simple Exponential Smoothing (SES) for non-seasonal time series without trend.

    Forecasts are based on a weighted average of past observations, with weights decreasing exponentially over time.
    Forecast is a flat line, this is because SES does not account for trend or seasonality.

    Attributes:
        alpha (float): Smoothing parameter for the level (0 <= alpha <= 1).
        level (float): The final estimated level component after fitting.
        fitted_values (np.ndarray): The fitted values (one-step-ahead forecasts).
        model (np.ndarray): The original time series data.
    """

    def __init__(self, alpha):
        """Initialize SES model.

        Args:
            alpha (float): Smoothing parameter for the level. Must be between 0 and 1.
        """
        if not (0 <= alpha <= 1):
            raise ValueError("alpha must be between 0 and 1.")
        self.alpha = alpha
        self.level = None
        self.fitted_values = None
        self.model = None

    def __name__(self):
        return "Simple Exponential Smoothing (SES)"

    def __str__(self):
        return f"SimpleExponentialSmoothing(alpha={self.alpha})"

    def fit(self, time_series):
        """Fit the SES model to the data.

        Args:
            time_series (array-like): The time series data (1-dimensional).

        Returns:
            np.ndarray: The fitted values (one-step-ahead forecasts).
        """
        self.model = np.asarray(time_series, dtype=float).flatten()
        n = len(self.model)
        if n == 0:
            raise ValueError("Time series cannot be empty.")

        fitted = np.full(n, np.nan)
        level_history = np.full(n, np.nan)

        # Initialization: Use the first observation as the initial level
        current_level = self.model[0]
        level_history[0] = current_level
        # First fitted value is the initial level (forecast for y[1] based on y[0])
        if n > 1:
            fitted[1] = current_level

        # Iterate through the series
        for t in range(1, n):
            # Update level: l_t = alpha * y_t + (1 - alpha) * l_{t-1}
            current_level = (
                self.alpha * self.model[t] + (1 - self.alpha) * current_level
            )
            level_history[t] = current_level
            # Store the one-step-ahead forecast made *at* time t-1 for time t
            if t + 1 < n:
                fitted[t + 1] = current_level  # Forecast for y[t+1] is l_t

        self.level = current_level
        self.fitted_values = (
            fitted  # fitted[t] is the forecast for model[t] made at t-1
        )

        return self.fitted_values

    def forecast(self, steps):
        """Generate forecasts for future steps.

        Args:
            steps (int): The number of steps to forecast ahead.

        Returns:
            np.ndarray: An array of forecasted values.
        """
        if self.level is None:
            raise ValueError("Model must be fitted before forecasting.")
        if steps <= 0:
            return np.array([])

        # SES forecast is flat: equal to the last estimated level
        return np.full(steps, self.level)


class DoubleExponentialSmoothing:
    """Double Exponential Smoothing (DES) / Holt's Linear Trend Method.

    Extends SES to handle time series with a trend component (additive trend).

    Attributes:
        alpha (float): Smoothing parameter for the level (0 <= alpha <= 1).
        beta (float): Smoothing parameter for the trend (0 <= beta <= 1).
        level (float): The final estimated level component after fitting.
        trend (float): The final estimated trend component after fitting.
        fitted_values (np.ndarray): The one-step-ahead forecasts made during fitting.
        model (np.ndarray): The original time series data.
    """

    def __init__(self, alpha, beta):
        """Initialize DES model.

        Args:
            alpha (float): Smoothing parameter for the level (0 <= alpha <= 1).
            beta (float): Smoothing parameter for the trend (0 <= beta <= 1).
        """
        if not (0 <= alpha <= 1):
            raise ValueError("alpha must be between 0 and 1.")
        if not (0 <= beta <= 1):
            raise ValueError("beta must be between 0 and 1.")
        self.alpha = alpha
        self.beta = beta
        self.level = None
        self.trend = None
        self.fitted_values = None
        self.model = None

    def __name__(self):
        return "Double Exponential Smoothing (DES)"

    def __str__(self):
        return f"DoubleExponentialSmoothing(alpha={self.alpha}, beta={self.beta})"

    def fit(self, time_series):
        """Fit the DES model to the data.

        Args:
            time_series (array-like): The time series data (1-dimensional). Requires at least 2 points.

        Returns:
            np.ndarray: The fitted values (one-step-ahead forecasts).
        """
        self.model = np.asarray(time_series, dtype=float).flatten()
        n = len(self.model)
        if n < 2:
            raise ValueError("Time series must have at least 2 observations for DES.")

        fitted = np.full(n, np.nan)
        level_history = np.full(n, np.nan)
        trend_history = np.full(n, np.nan)

        # Initialization (simple approach)
        current_level = self.model[0]
        current_trend = (
            self.model[1] - self.model[0]
        )  # Initial trend based on first two points
        level_history[0] = current_level
        trend_history[0] = current_trend  # Trend at time 0

        # Calculate forecast for y[1] (based on l[0] and b[0])
        fitted[1] = current_level + current_trend

        # Iterate through the series from the second point
        for t in range(1, n):
            # Previous level and trend
            prev_level = current_level
            prev_trend = current_trend

            # Update level: l_t = alpha * y_t + (1 - alpha) * (l_{t-1} + b_{t-1})
            current_level = self.alpha * self.model[t] + (1 - self.alpha) * (
                prev_level + prev_trend
            )

            # Update trend: b_t = beta * (l_t - l_{t-1}) + (1 - beta) * b_{t-1}
            current_trend = (
                self.beta * (current_level - prev_level) + (1 - self.beta) * prev_trend
            )

            level_history[t] = current_level
            trend_history[t] = current_trend

            # Store the one-step-ahead forecast made *at* time t for time t+1
            if t + 1 < n:
                fitted[t + 1] = (
                    current_level + current_trend
                )  # Forecast y_{t+1} = l_t + b_t

        self.level = current_level
        self.trend = current_trend
        self.fitted_values = fitted

        return self.fitted_values

    def forecast(self, steps):
        """Generate forecasts for future steps.

        Args:
            steps (int): The number of steps to forecast ahead.

        Returns:
            np.ndarray: An array of forecasted values.
        """
        if self.level is None or self.trend is None:
            raise ValueError("Model must be fitted before forecasting.")
        if steps <= 0:
            return np.array([])

        # Forecast formula: y_{T+h} = l_T + h * b_T
        h_values = np.arange(1, steps + 1)
        return self.level + h_values * self.trend

    def find_best_alpha_beta(
        self,
        train_series,
        test_series,
        alpha_values=None,
        beta_values=None,
        set_best=False,
    ):
        """Find the best alpha and beta values for the DES model.

        Args:
            train_series (array-like): The training time series data (1-dimensional).
            test_series (array-like): The testing time series data (1-dimensional).
            alpha_values (list, optional): List of alpha values to evaluate. Defaults to [0.1, 0.2, ..., 0.9].
            beta_values (list, optional): List of beta values to evaluate. Defaults to [0.1, 0.2, ..., 0.9].
            set_best (bool, optional): If True, set the best alpha and beta values to the model. Defaults to False.

        Returns:
            tuple: Best alpha and beta values based on mean squared error.
        """
        if alpha_values is None:
            alpha_values = np.arange(0.1, 1.0, 0.1)
        if beta_values is None:
            beta_values = np.arange(0.1, 1.0, 0.1)

        best_alpha = None
        best_beta = None
        best_mse = float("inf")

        for alpha in alpha_values:
            for beta in beta_values:
                self.alpha = alpha
                self.beta = beta
                self.fit(train_series)
                forecast_steps = len(test_series)
                forecasted_values = self.forecast(steps=forecast_steps)
                mse = mean_squared_error(test_series, forecasted_values)

                if mse < best_mse:
                    best_mse = mse
                    best_alpha = alpha
                    best_beta = beta

        if set_best:
            self.alpha = best_alpha
            self.beta = best_beta
        return best_alpha, best_beta


class TripleExponentialSmoothing:
    """Triple Exponential Smoothing (TES) / Holt-Winters Method (Additive Seasonality).

    Extends DES to handle time series with both trend and seasonality (additive).

    Attributes:
        alpha (float): Smoothing parameter for the level (0 <= alpha <= 1).
        beta (float): Smoothing parameter for the trend (0 <= beta <= 1).
        gamma (float): Smoothing parameter for seasonality (0 <= gamma <= 1).
        period (int): The seasonal period (must be > 1).
        level (float): The final estimated level component after fitting.
        trend (float): The final estimated trend component after fitting.
        season (np.ndarray): The final estimated seasonal components (length `period`).
        fitted_values (np.ndarray): The one-step-ahead forecasts made during fitting.
        model (np.ndarray): The original time series data.
    """

    def __init__(self, alpha, beta, gamma, period):
        """Initialize TES model (Additive Seasonality).

        Args:
            alpha (float): Smoothing parameter for the level (0 <= alpha <= 1).
            beta (float): Smoothing parameter for the trend (0 <= beta <= 1).
            gamma (float): Smoothing parameter for seasonality (0 <= gamma <= 1).
            period (int): The seasonal period (e.g., 12 for monthly). Must be > 1.
        """
        if not (0 <= alpha <= 1):
            raise ValueError("alpha must be between 0 and 1.")
        if not (0 <= beta <= 1):
            raise ValueError("beta must be between 0 and 1.")
        if not (0 <= gamma <= 1):
            raise ValueError("gamma must be between 0 and 1.")
        if not isinstance(period, int) or period <= 1:
            raise ValueError("period must be an integer greater than 1.")

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.period = period
        self.level = None
        self.trend = None
        self.season = None  # Array of seasonal factors
        self.fitted_values = None
        self.model = None

    def __name__(self):
        return "Triple Exponential Smoothing (TES)"

    def __str__(self):
        return f"TripleExponentialSmoothing(alpha={self.alpha}, beta={self.beta}, gamma={self.gamma}, period={self.period})"

    def _initial_seasonal_components(self, series, m):
        """Estimate initial seasonal components."""
        if len(series) < 2 * m:
            raise ValueError(
                "Series too short for seasonal initialization (< 2*period)."
            )
        # Simple approach: Average over first few full seasons after removing rough trend
        len(series) // m
        seasonal_averages = np.zeros(m)
        # Rough trend removal (optional but helpful)
        trend_approx = np.convolve(
            series, np.ones(m) / m, mode="valid"
        )  # Simple MA for trend hint
        detrended_approx = (
            series[m // 2 : m // 2 + len(trend_approx)] - trend_approx
        )  # Approximate detrended

        # Calculate average for each season index from the approximate detrended series
        # This part needs careful alignment and handling of shorter initial data
        seasonal_vals = [[] for _ in range(m)]
        for i in range(len(detrended_approx)):
            # Align index relative to start of detrended_approx
            original_index = i + m // 2
            season_index = original_index % m
            seasonal_vals[season_index].append(detrended_approx[i])

        for i in range(m):
            if seasonal_vals[i]:
                seasonal_averages[i] = np.mean(seasonal_vals[i])
            else:  # Fallback if a season had no data (unlikely with len >= 2m)
                seasonal_averages[i] = 0  # Or use overall mean?

        # Normalize: sum to zero for additive seasonality
        seasonal_averages -= np.mean(seasonal_averages)
        return seasonal_averages

    def fit(self, time_series):
        """Fit the TES model (additive seasonality) to the data.

        Args:
            time_series (array-like): The time series data (1-dimensional).
                                      Length should be >= 2 * period.

        Returns:
            np.ndarray: The fitted values for the time series.
        """
        self.model = np.asarray(time_series, dtype=float).flatten()
        n = len(self.model)
        m = self.period

        if n < m:  # Need at least one full period for seasonal init
            raise ValueError(
                f"Time series length ({n}) must be at least the period ({m})."
            )
        if n < 2 * m:
            warnings.warn(
                f"Time series length ({n}) is less than 2 * period ({m}). Initial seasonal estimates might be less reliable.",
                UserWarning,
                stacklevel=2,
            )

        fitted = np.full(n, np.nan)
        level_hist = np.full(n, np.nan)
        trend_hist = np.full(n, np.nan)
        season_hist = np.full(
            (n + m), np.nan
        )  # Store history including initial estimates

        # --- Initialization ---
        # Level: Average of the first period
        initial_level = np.mean(self.model[:m])
        # Trend: Average slope over the first period (or first two periods if available)
        if n >= 2 * m:
            initial_trend = (
                np.mean(self.model[m : 2 * m]) - np.mean(self.model[:m])
            ) / m
        else:  # Less reliable trend estimate if only one period available
            initial_trend = (
                (self.model[m - 1] - self.model[0]) / (m - 1) if m > 1 else 0
            )

        # Seasonal: Use helper function or simple difference from first period average
        try:
            initial_seasonals = self._initial_seasonal_components(self.model, m)
        except ValueError:  # Fallback if _initial_seasonal_components fails
            warnings.warn(
                "Using simpler seasonal initialization (Y[i] - initial_level).",
                UserWarning,
                stacklevel=2,
            )
            initial_seasonals = self.model[:m] - initial_level

        # Store initial values
        # Level and Trend are considered at time t=m-1 (end of first period)
        level_hist[m - 1] = initial_level
        trend_hist[m - 1] = initial_trend
        season_hist[:m] = initial_seasonals  # Initial seasonals apply to times 0..m-1

        # --- Iteration ---
        current_level = initial_level
        current_trend = initial_trend
        current_seasonals = initial_seasonals.copy()  # Use a copy

        # Iterate from the start of the second period (index m)
        for t in range(m, n):
            # Previous values needed
            prev_level = current_level
            prev_trend = current_trend
            # Seasonal index for y[t] is (t % m), need seasonal factor from t-m
            season_idx_lag = (t - m) % m
            prev_seasonal_factor = current_seasonals[season_idx_lag]

            # Update level: l_t = alpha*(y_t - s_{t-m}) + (1-alpha)*(l_{t-1} + b_{t-1})
            current_level = self.alpha * (self.model[t] - prev_seasonal_factor) + (
                1 - self.alpha
            ) * (prev_level + prev_trend)

            # Update trend: b_t = beta*(l_t - l_{t-1}) + (1-beta)*b_{t-1}
            current_trend = (
                self.beta * (current_level - prev_level) + (1 - self.beta) * prev_trend
            )

            # Update seasonal: s_t = gamma*(y_t - l_t) + (1-gamma)*s_{t-m}
            season_idx_current = t % m
            current_seasonals[season_idx_current] = (
                self.gamma * (self.model[t] - current_level)
                + (1 - self.gamma) * prev_seasonal_factor
            )

            # Store history
            level_hist[t] = current_level
            trend_hist[t] = trend_hist[
                t - 1
            ]  # Trend is based on t-1 state (update after using prev) - CORRECTION: use current_trend
            trend_hist[t] = current_trend
            season_hist[t] = current_seasonals[
                season_idx_current
            ]  # Store the updated seasonal factor

            # Store one-step-ahead forecast made at t-1 for time t
            # Need l_{t-1}, b_{t-1}, s_{t-m}
            forecast_for_t = prev_level + prev_trend + prev_seasonal_factor
            fitted[t] = forecast_for_t

        self.level = current_level
        self.trend = current_trend
        # Final seasonal factors are the last `m` calculated/updated ones
        self.season = current_seasonals  # The array after the loop finishes
        self.fitted_values = fitted

        return self.fitted_values

    def forecast(self, steps):
        """Generate forecasts for future steps (Additive Seasonality).

        Args:
            steps (int): The number of steps to forecast ahead.

        Returns:
            np.ndarray: An array of forecasted values.
        """
        if self.level is None or self.trend is None or self.season is None:
            raise ValueError("Model must be fitted before forecasting.")
        if steps <= 0:
            return np.array([])

        forecasts = np.full(steps, np.nan)
        last_n = len(self.model)

        # Forecast formula: y_{T+h} = l_T + h * b_T + s_{T+h-m}
        for h in range(1, steps + 1):
            # Determine the index for the seasonal component needed
            # Season index = (T + h - 1) mod m
            season_idx = (last_n + h - 1) % self.period
            seasonal_component = self.season[season_idx]

            forecasts[h - 1] = self.level + h * self.trend + seasonal_component

        return forecasts

    def find_best_alpha_beta_gamma(
        self,
        train_series,
        test_series,
        alpha_values=None,
        beta_values=None,
        gamma_values=None,
        set_best=False,
    ):
        """Find the best alpha, beta, and gamma values for the TES model.

        Args:
            train_series (array-like): The training time series data (1-dimensional).
            test_series (array-like): The testing time series data (1-dimensional).
            alpha_values (list, optional): List of alpha values to evaluate. Defaults to [0.1, 0.2, ..., 0.9].
            beta_values (list, optional): List of beta values to evaluate. Defaults to [0.1, 0.2, ..., 0.9].
            gamma_values (list, optional): List of gamma values to evaluate. Defaults to [0.1, 0.2, ..., 0.9].
            set_best (bool, optional): If True, set the best alpha, beta, and gamma values to the model. Defaults to False.

        Returns:
            tuple: Best alpha, beta, and gamma values based on mean squared error.
        """
        if alpha_values is None:
            alpha_values = np.arange(0.1, 1.0, 0.1)
        if beta_values is None:
            beta_values = np.arange(0.1, 1.0, 0.1)
        if gamma_values is None:
            gamma_values = np.arange(0.1, 1.0, 0.1)

        best_alpha = None
        best_beta = None
        best_gamma = None
        best_mse = float("inf")

        for alpha in alpha_values:
            for beta in beta_values:
                for gamma in gamma_values:
                    self.alpha = alpha
                    self.beta = beta
                    self.gamma = gamma
                    self.fit(train_series)
                    forecast_steps = len(test_series)
                    forecasted_values = self.forecast(steps=forecast_steps)
                    mse = mean_squared_error(test_series, forecasted_values)

                    if mse < best_mse:
                        best_mse = mse
                        best_alpha = alpha
                        best_beta = beta
                        best_gamma = gamma

        if set_best:
            self.alpha = best_alpha
            self.beta = best_beta
            self.gamma = best_gamma

        return best_alpha, best_beta, best_gamma
