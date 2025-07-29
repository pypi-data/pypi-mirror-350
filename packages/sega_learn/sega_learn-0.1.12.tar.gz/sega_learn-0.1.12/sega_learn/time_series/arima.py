import warnings

import numpy as np
from scipy.optimize import minimize


class ARIMA:
    """ARIMA model for time series forecasting.

    ARIMA is a class of models that explains a given time series based on its own past values,
    its own past forecast errors, and a number of lagged forecast errors.
    It is a combination of Auto-Regressive (AR), Moving Average (MA) models, and differencing (I) to make the series stationary.

    The model is defined by three parameters: p, d, and q, which represent the order of the AR,
    the degree of differencing, and the order of the MA components, respectively.

    Attributes:
        order (tuple): The order of the ARIMA model (p, d, q).
        p (int): The order of the Auto-Regressive (AR) component.
        d (int): The degree of differencing.
        q (int): The order of the Moving Average (MA) component.
        model (array-like): The original time series data.
        fitted_model (dict): The fitted ARIMA model containing AR and MA components.
        _differenced_series (array-like): The differenced series used for fitting ARMA.
        _residuals (array-like): The residuals after fitting the AR component.
    """

    def __init__(self, order):
        """Initialize the ARIMA model.

        ARIMA(p, d, q) model where:
            - p: Order of the Auto-Regressive (AR) component.
            - d: Degree of differencing (number of times the series is differenced).
            - q: Order of the Moving Average (MA) component.

        Args:
            order (tuple): The order of the ARIMA model (p, d, q).

        Selecting the right values:
            - p: Use the Partial Autocorrelation Function (PACF) plot to determine the lag where the PACF cuts off.
            - d: Use the Augmented Dickey-Fuller (ADF) test to check stationarity. Increase `d` until the series becomes stationary.
            - q: Use the Autocorrelation Function (ACF) plot to determine the lag where the ACF cuts off.
        """
        # Validate input order
        if not isinstance(order, (list, tuple)) or len(order) != 3:
            raise ValueError("Order must be a list or tuple of length 3 (p, d, q).")
        if not all(isinstance(i, int) and i >= 0 for i in order):
            raise ValueError("p, d, and q must be non-negative integers.")

        self.order = order
        self.p = order[0]
        self.d = order[1]
        self.q = order[2]
        self.model = None
        self.fitted_model = None
        self._differenced_series = None
        self._residuals = None

    def __name__(self):
        return "ARIMA"

    def __str__(self):
        return f"ARIMA(order={self.order})"

    def fit(self, time_series):
        """Fit the ARIMA model to the given time series data.

        Args:
            time_series (array-like): The time series data to fit the model to.
        """
        # Store the original time series for inverse differencing during forecasting
        self.model = np.asarray(time_series, dtype=float)
        if len(self.model) <= self.d:
            raise ValueError(
                "Time series length must be greater than the differencing order d."
            )

        # Step 1: Perform differencing to make the series stationary
        self._differenced_series = self._difference_series(time_series, self.d)

        # Step 2: Fit the AR (Auto-Regressive) component
        ar_coefficients = self._fit_ar_model(self._differenced_series, self.p)

        # Step 3: Compute residuals from the AR model
        self._residuals = self._compute_residuals(
            self._differenced_series, ar_coefficients
        )

        # Step 4: Fit the MA (Moving Average) component
        ma_coefficients = self._fit_ma_model(self._residuals, self.q)

        # Step 5: Combine AR and MA components into a single model
        self.fitted_model = self._combine_ar_ma(ar_coefficients, ma_coefficients)

    def forecast(self, steps):
        """Forecast future values using the fitted ARIMA model.

        Args:
            steps (int): The number of steps to forecast.

        Returns:
            array-like: The forecasted values.
        """
        if self.fitted_model is None:
            raise ValueError("The model must be fitted before forecasting.")
        if steps <= 0:
            return np.array([])

        # Step 1: Forecast future values using the fitted ARIMA model
        forecasted_values = self._forecast_arima(self.fitted_model, steps)

        # Step 2: Apply inverse differencing to reconstruct the original scale
        forecasted_values = self._inverse_difference(
            self.model, forecasted_values, self.d
        )

        return forecasted_values

    def _compute_residuals(self, differenced_series, ar_coefficients):
        """Compute residuals from the AR model."""
        return differenced_series[self.p :] - np.dot(
            np.array(
                [
                    differenced_series[i : len(differenced_series) - self.p + i]
                    for i in range(self.p)
                ]
            ).T,
            ar_coefficients,
        )

    def _compute_ar_part(self, ar_coefficients, forecasted_values, p):
        """Compute the AR contribution to the forecast."""
        return sum(ar_coefficients[i] * forecasted_values[-i - 1] for i in range(p))

    def _compute_ma_part(self, ma_coefficients, residuals, q):
        """Compute the MA contribution to the forecast."""
        return sum(ma_coefficients[i] * residuals[-i - 1] for i in range(q))

    def _difference_series(self, time_series, d):
        """Perform differencing on the time series to make it stationary.

        Args:
            time_series (array-like): The original time series data.
            d (int): The degree of differencing.

        Returns:
            array-like: The differenced time series.
        """
        if len(time_series) <= d:
            raise ValueError("Differencing degree exceeds time series length.")

        # For each degree of differencing, compute the difference
        # between consecutive observations
        for _ in range(d):
            time_series = np.diff(time_series)
        return time_series

    def _fit_ar_model(self, time_series, p):
        """Fit the Auto-Regressive (AR) component of the model.

        Args:
            time_series (array-like): The stationary time series data.
            p (int): The order of the AR component.

        Returns:
            array-like: The AR coefficients.
        """
        # If p is 0, return an empty array (no AR component)
        if p == 0:
            return np.array([])

        # Construct the design matrix for AR(p)
        # X is a matrix where each row contains p lagged values of the time series
        # X[i] = [time_series[i], time_series[i-1], ..., time_series[i-p+1]]
        # X = np.array([time_series[i : len(time_series) - p + i] for i in range(p)]).T
        X = np.column_stack(
            [time_series[i : len(time_series) - p + i] for i in range(p)]
        )

        # # Reverse columns so X[t] = [y_{t-1}, y_{t-2}, ..., y_{t-p}]
        X = X[:, ::-1]

        # y is the current value of the time series
        # y[i] = time_series[i+p]
        y = time_series[p:]

        # Ensure X and y have matching lengths
        if len(X) != len(y):
            X = X[: len(y)]

        # First use OLS to get initial AR coefficients
        # Standard ARIMA often assumes zero mean for differenced series, so no intercept.
        # Validate X and y before calling np.linalg.lstsq
        if (
            np.any(np.isnan(X))
            or np.any(np.isnan(y))
            or np.any(np.isinf(X))
            or np.any(np.isinf(y))
        ):
            warnings.warn(
                "Input data contains NaN or Inf values. Returning zero coefficients.",
                UserWarning,
                stacklevel=2,
            )
            ar_coefficients = np.zeros(X.shape[1] if X.ndim > 1 else 0)
        else:
            try:
                ar_coefficients, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
            except np.linalg.LinAlgError:
                warnings.warn(
                    "Singular matrix encountered in AR fitting. Coefficients might be unstable.",
                    UserWarning,
                    stacklevel=2,
                )
                ar_coefficients = np.zeros(X.shape[1] if X.ndim > 1 else 0)

        # Use scipy's minimize to optimize the AR coefficients, non-linear optimization
        def objective_function(ar_params):
            """Objective function for AR fitting, sum of squared errors."""
            predicted_values = self._compute_ar_part(ar_params, y, p)
            return np.sum((y - predicted_values) ** 2)

        initial_guess = ar_coefficients
        result = minimize(objective_function, initial_guess, method="BFGS")
        ar_coefficients = result.x

        return ar_coefficients

    def _fit_ma_model(self, residuals, q):
        """Fit the Moving Average (MA) component of the model.

        Args:
            residuals (array-like): The residuals from the AR model.
            q (int): The order of the MA component.

        Returns:
            array-like: The MA coefficients.
        """
        # If q is 0, return an empty array (no MA component)
        if q == 0:
            return np.array([])

        # Construct the design matrix for MA(q)
        # X is a matrix where each row contains q lagged residuals
        # X[i] = [residuals[i], residuals[i-1], ..., residuals[i-q+1]]
        # X = np.array([residuals[i : len(residuals) - q + i] for i in range(q)]).T
        X = np.column_stack([residuals[i : len(residuals) - q + i] for i in range(q)])

        # y is the current value of the residuals
        # y[i] = residuals[i+q]
        # Note: We need to shift the residuals by q to align with the design matrix
        y = residuals[q:]

        # Ensure X and y have matching lengths
        if len(X) != len(y):
            X = X[: len(y)]

        # First use OLS to get initial MA coefficients
        # Validate X and y before calling np.linalg.lstsq
        if (
            np.any(np.isnan(X))
            or np.any(np.isnan(y))
            or np.any(np.isinf(X))
            or np.any(np.isinf(y))
        ):
            warnings.warn(
                "Input data contains NaN or Inf values. Returning zero coefficients.",
                UserWarning,
                stacklevel=2,
            )
            ma_coefficients = np.zeros(q)
        else:
            try:
                ma_coefficients, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
            except np.linalg.LinAlgError:
                warnings.warn(
                    "Singular matrix encountered in MA fitting. Coefficients might be unstable.",
                    UserWarning,
                    stacklevel=2,
                )
                ma_coefficients = np.zeros(q)
            except ValueError as _e:
                ma_coefficients = np.zeros(q)

        # Use scipy's minimize to optimize the MA coefficients, non-linear optimization
        def objective_function(ma_params):
            """Objective function for MA fitting, sum of squared errors."""
            predicted_residuals = self._compute_ma_part(ma_params, residuals, q)
            return np.sum((residuals[q:] - predicted_residuals) ** 2)

        initial_guess = ma_coefficients
        result = minimize(objective_function, initial_guess, method="BFGS")
        ma_coefficients = result.x

        return ma_coefficients

    def _combine_ar_ma(self, ar_coefficients, ma_coefficients):
        """Combine AR and MA components into a single model.

        Args:
            ar_coefficients (array-like): The AR coefficients.
            ma_coefficients (array-like): The MA coefficients.

        Returns:
            dict: The combined ARIMA model.
        """
        # Store the AR and MA coefficients in a dictionary to represent the model
        return {
            "ar_coefficients": ar_coefficients,
            "ma_coefficients": ma_coefficients,
            "order": self.order,
        }

    def _forecast_arima(self, fitted_model, steps):
        """Forecast future values using the fitted ARIMA model.

        Args:
            fitted_model (dict): The fitted ARIMA model containing AR and MA components.
            steps (int): The number of steps to forecast.

        Returns:
            array-like: The forecasted values.
        """
        # Get AR and MA coefficients from the fitted model
        ar_coefficients = fitted_model["ar_coefficients"]
        ma_coefficients = fitted_model["ma_coefficients"]
        # Get p and q from length of coefficients (can also be obtained from order)
        p = len(ar_coefficients)
        q = len(ma_coefficients)

        # Initialize forecasted values and residuals
        forecasted_values = list(self.model[-p:])  # Start with the last `p` values
        residuals = list(
            self.model[-self.q :]
        )  # Use the last `q` residuals from the fitted model

        for _ in range(steps):
            # Compute AR and MA contributions
            ar_part = self._compute_ar_part(ar_coefficients, forecasted_values, p)
            ma_part = self._compute_ma_part(ma_coefficients, residuals, q)

            # Forecast next value
            next_value = ar_part + ma_part
            forecasted_values.append(next_value)

            # Update residuals (assume zero error for forecasted steps)
            residuals.append(next_value - ar_part)

        # Return the last `steps` forecasted values
        return np.array(forecasted_values[-steps:])

    def _inverse_difference(self, original_series, differenced_series, d):
        """Reconstruct the original series from the differenced series.

        Args:
            original_series (array-like): The original time series data.
            differenced_series (array-like): The differenced time series.
            d (int): The degree of differencing.

        Returns:
            array-like: The reconstructed time series.
        """
        if len(original_series) < d:
            raise ValueError(
                "Original series length is insufficient for inverse differencing."
            )

        # For each degree of differencing, compute the cumulative sum
        # to reconstruct the original series
        for _ in range(d):
            # Add back the last value of the original series to reconstruct the scale
            differenced_series = np.r_[original_series[-1], differenced_series].cumsum()
            original_series = original_series[:-1]
        # Return the reconstructed series
        return differenced_series[d:]

    @staticmethod
    def suggest_order(time_series, max_p=5, max_d=2, max_q=5):
        """Suggest the optimal ARIMA order (p, d, q) for the given time series.

        Args:
            time_series (array-like): The time series data.
            max_p (int): Maximum order for AR component.
            max_d (int): Maximum degree of differencing.
            max_q (int): Maximum order for MA component.

        Returns:
            tuple: The optimal order (p, d, q).
        """
        try:
            from statsmodels.tsa.stattools import acf, adfuller, pacf
        except ImportError as e:
            raise ImportError(
                "Please install the required dependencies for this function: statsmodels."
            ) from e

        # Step 1: Determine d (degree of differencing) using the ADF test
        d = 0
        while True:
            try:
                adf_test = adfuller(time_series)
                if adf_test[1] <= 0.05:  # p-value <= 0.05 indicates stationarity
                    break
                time_series = np.diff(time_series, prepend=time_series[0])
                d += 1
            except Exception as e:
                raise ValueError(f"Error during ADF test: {e}") from e

        # Step 2: Determine p (AR order) using the PACF plot
        try:
            pacf_values = pacf(time_series, nlags=20)
            p = min(
                next(
                    (
                        i
                        for i, val in enumerate(pacf_values)
                        if abs(val) < 1.96 / np.sqrt(len(time_series))
                    ),
                    max_p,
                ),
                max_p,
            )
        except Exception as e:
            p = 0  # Default to 0 if PACF fails
            warnings.warn(
                f"Error determining p using PACF: {e}. Defaulting p to 0.",
                UserWarning,
                stacklevel=2,
            )

        # Step 3: Determine q (MA order) using the ACF plot
        try:
            acf_values = acf(time_series, nlags=20)
            q = min(
                next(
                    (
                        i
                        for i, val in enumerate(acf_values)
                        if abs(val) < 1.96 / np.sqrt(len(time_series))
                    ),
                    max_q,
                ),
                max_q,
            )
        except Exception as e:
            q = 0  # Default to 0 if ACF fails
            warnings.warn(
                f"Error determining q using ACF: {e}. Defaulting q to 0.",
                UserWarning,
                stacklevel=2,
            )

        return (p, min(d, max_d), q)

    @staticmethod
    def find_best_order(
        train_series, test_series, max_p=5, max_d=2, max_q=5, subset_size=1.0
    ):
        """Find the best ARIMA order using grid search.

        Args:
            train_series (array-like): The training time series data.
            test_series (array-like): The testing time series data.
            max_p (int): Maximum order for AR component.
            max_d (int): Maximum degree of differencing.
            max_q (int): Maximum order for MA component.
            subset_size (float): Proportion of the training set to use for fitting.

        Returns:
            tuple: The best order (p, d, q).
        """
        # Validate input data
        if not isinstance(train_series, (list, np.ndarray)) or not isinstance(
            test_series, (list, np.ndarray)
        ):
            raise ValueError(
                "train_series and test_series must be list or numpy array."
            )
        if len(train_series) < 1 or len(test_series) < 1:
            raise ValueError("train_series and test_series must not be empty.")
        if not (0 < subset_size <= 1.0):
            raise ValueError("subset_size must be between 0 and 1.")

        best_order = None
        best_mse = float("inf")

        if subset_size < 1.0:
            # Randomly sample a subset of the training series
            subset_size = int(len(train_series) * subset_size)
            train_series = np.random.choice(
                train_series, size=subset_size, replace=False
            )

        # Loop through all combinations of (p, d, q) within the specified limits
        for p in range(max_p + 1):
            for d in range(max_d + 1):
                for q in range(max_q + 1):
                    # For each combination, create an ARIMA model and fit it
                    try:
                        arima_model = ARIMA(order=(p, d, q))
                        arima_model.fit(train_series)
                        forecasted_values = arima_model.forecast(steps=len(test_series))
                        mse = np.mean((test_series - forecasted_values) ** 2)

                        # If the MSE is lower than the best found so far, update best order
                        if mse < best_mse:
                            best_mse = mse
                            best_order = (p, d, q)

                    # Handle any exceptions that may arise during fitting or forecasting
                    except Exception as _e:
                        continue
        return best_order


class SARIMA(ARIMA):
    """SARIMA model for time series forecasting.

    SARIMA extends ARIMA by including seasonal components.

    Attributes:
        order (tuple): The non-seasonal order of the ARIMA model (p, d, q).
        seasonal_order (tuple): The seasonal order of the SARIMA model (P, D, Q, m).
        p (int): The order of the Auto-Regressive (AR) component.
        d (int): The degree of differencing.
        q (int): The order of the Moving Average (MA) component.
        P (int): The order of the seasonal Auto-Regressive (SAR) component.
        D (int): The degree of seasonal differencing.
        Q (int): The order of the seasonal Moving Average (SMA) component.
        m (int): The number of time steps in a seasonal period.
    """

    def __init__(self, order=(0, 0, 0), seasonal_order=(0, 0, 0, 1)):
        """Initialize the SARIMA model.

        Args:
            order (tuple): Non-seasonal ARIMA order (p, d, q).
            seasonal_order (tuple): Seasonal order (P, D, Q, m).
        """
        # Validate seasonal_order
        if not isinstance(seasonal_order, (list, tuple)) or len(seasonal_order) != 4:
            raise ValueError(
                "Seasonal order must be a tuple/list of length 4: (P, D, Q, m)."
            )

        P, D, Q, m = seasonal_order
        if any(x < 0 for x in (P, D, Q)) or m <= 0:
            raise ValueError("P, D, Q must be ≥0 and m must be a positive integer.")

        super().__init__(order)
        # Store the seasonal components
        self.seasonal_order = seasonal_order
        self.P, self.D, self.Q, self.m = seasonal_order
        self.original_series = None

    def __name__(self):
        return "SARIMA"

    def __str__(self):
        return f"SARIMA(order={self.order}, seasonal_order={self.seasonal_order})"

    def fit(self, time_series):
        """Fit the SARIMA model to the given time series data.

        First fits the ARIMA model on the seasonally-differenced series.
        Then, forecasts the seasonally-differenced series and inverts the seasonal differencing.

        Args:
            time_series (array-like): The time series data to fit the model to.
        """
        # Keep the raw series for inversion later
        self.original_series = np.asarray(time_series, dtype=float)

        # Apply seasonal differencing if needed
        if self.D > 0:
            ts_sd = self._seasonal_difference(self.original_series, self.D, self.m)
        else:
            ts_sd = self.original_series.copy()

        # Fit the ARIMA(p,d,q) on the seasonally-differenced series
        super().fit(ts_sd)

    def forecast(self, steps):
        """Forecast future values using the fitted SARIMA model.

        Args:
            steps (int): The number of steps to forecast.

        Returns:
            array-like: The forecasted values.
        """
        if self.fitted_model is None:
            raise ValueError("Fit the model before forecasting.")

        # Get forecasts on the seasonally differenced scale
        fc_sd = super().forecast(steps)

        # Invert seasonal differencing
        return self._inverse_seasonal_difference(fc_sd)

    def _seasonal_difference(self, series, D, m):
        """Apply D rounds of lag-m differencing.

        Args:
            series (array-like): The time series data.
            D (int): The degree of seasonal differencing.
            m (int): The seasonal period.

        Returns:
            array-like: The seasonally differenced time series.
        """
        arr = series.copy()
        # For each degree of differencing, compute the difference
        # between consecutive observations
        for _ in range(D):
            arr = arr[m:] - arr[:-m]
        return arr

    def _inverse_seasonal_difference(self, diff_forecast):
        """Reconstruct original scale from seasonally differenced forecasts.

        Args:
            diff_forecast (array-like): The seasonally differenced forecasts.

        Returns:
            array-like: The original time series.
        """
        history = list(self.original_series)
        result = []
        # For each degree of differencing, compute the cumulative sum
        # to reconstruct the original series
        for f in diff_forecast:
            # add back the last seasonal value D times
            val = f
            for _ in range(self.D):
                val += history[-self.m]
            history.append(val)
            result.append(val)
        return np.array(result)

    @staticmethod
    def suggest_order(
        time_series, max_p=3, max_d=2, max_q=3, max_P=2, max_D=1, max_Q=2, max_m=100
    ):
        """Suggest the optimal SARIMA order for the given time series.

        Args:
            time_series (array-like): The time series data.
            max_p (int): Maximum order for AR component.
            max_d (int): Maximum degree of differencing.
            max_q (int): Maximum order for MA component.
            max_P (int): Maximum order for seasonal AR component.
            max_D (int): Maximum degree of seasonal differencing.
            max_Q (int): Maximum order for seasonal MA component.
            max_m (int): Maximum seasonal period to consider.

        Returns:
            tuple: The optimal orders (p, d, q, P, D, Q, m).
        """
        try:
            from statsmodels.tsa.stattools import acf, adfuller, pacf
        except ImportError as e:
            raise ImportError(
                "Please install the required dependencies for this function: statsmodels."
            ) from e

        # Step 1: Determine seasonal period (m) based on autocorrelation
        try:
            acf_values = acf(time_series, nlags=min(len(time_series) // 2, 100))
            # Find peaks in ACF
            potential_m = []
            for i in range(1, len(acf_values) - 1):
                if (
                    acf_values[i] > acf_values[i - 1]
                    and acf_values[i] > acf_values[i + 1]
                    and acf_values[i] > 0.2
                ):
                    potential_m.append(i)

            if potential_m:
                m = potential_m[0]  # Use the first peak as the seasonal period
                m = min(m, max_m)  # Limit to max_m
            else:
                m = 1  # No clear seasonality detected
        except Exception as e:
            warnings.warn(
                f"Error determining seasonal period: {e}. Defaulting to m=1.",
                UserWarning,
                stacklevel=2,
            )
            m = 1

        # Step 2: Apply seasonal differencing if necessary
        seasonally_differenced = time_series.copy()
        D = 0
        if m > 1:
            # Test for seasonal differencing
            try:
                adf_test = adfuller(time_series)
                if adf_test[1] > 0.05:  # Not stationary
                    # Apply seasonal differencing
                    seasonally_differenced = np.array(
                        [
                            time_series[i] - time_series[i - m]
                            for i in range(m, len(time_series))
                        ]
                    )
                    D = 1

                    # Test if more differencing is needed
                    adf_test = adfuller(seasonally_differenced)
                    if adf_test[1] > 0.05 and len(seasonally_differenced) > 2 * m:
                        # Apply one more seasonal differencing
                        seasonally_differenced = np.array(
                            [
                                seasonally_differenced[i]
                                - seasonally_differenced[i - m]
                                for i in range(m, len(seasonally_differenced))
                            ]
                        )
                        D = 2
            except Exception as e:
                warnings.warn(
                    f"Error during seasonal differencing test: {e}. No seasonal differencing applied.",
                    UserWarning,
                    stacklevel=2,
                )

        # Step 3: Determine d (regular differencing)
        d = 0
        while True:
            try:
                adf_test = adfuller(seasonally_differenced)
                if adf_test[1] <= 0.05 or d >= max_d:  # Stationary or max d reached
                    break
                seasonally_differenced = np.diff(seasonally_differenced)
                d += 1
            except Exception as e:
                warnings.warn(
                    f"Error during ADF test: {e}. No regular differencing applied.",
                    UserWarning,
                    stacklevel=2,
                )
                break

        # Step 4: Determine p, q, P, Q
        try:
            # For non-seasonal components
            pacf_values = pacf(
                seasonally_differenced, nlags=min(len(seasonally_differenced) // 2, 20)
            )
            p = 0
            for i in range(1, min(len(pacf_values), max_p + 1)):
                if abs(pacf_values[i]) > 1.96 / np.sqrt(len(seasonally_differenced)):
                    p = i

            acf_values = acf(
                seasonally_differenced, nlags=min(len(seasonally_differenced) // 2, 20)
            )
            q = 0
            for i in range(1, min(len(acf_values), max_q + 1)):
                if abs(acf_values[i]) > 1.96 / np.sqrt(len(seasonally_differenced)):
                    q = i

            # For seasonal components
            P = 0
            Q = 0
            if m > 1 and len(seasonally_differenced) > 2 * m:
                # Look at seasonal lags
                for i in range(m, min(len(pacf_values), m * (max_P + 1)), m):
                    if abs(pacf_values[i]) > 1.96 / np.sqrt(
                        len(seasonally_differenced)
                    ):
                        P = i // m

                for i in range(m, min(len(acf_values), m * (max_Q + 1)), m):
                    if abs(acf_values[i]) > 1.96 / np.sqrt(len(seasonally_differenced)):
                        Q = i // m
        except Exception as e:
            warnings.warn(
                f"Error determining p, q, P, Q: {e}. Using default values.",
                UserWarning,
                stacklevel=2,
            )
            p = min(1, max_p)
            q = min(1, max_q)
            P = 0
            Q = 0

        # Ensure P and Q don't exceed their maximums
        P = min(P, max_P)
        Q = min(Q, max_Q)

        # # Since this is a SARIMA model, ensure that P, D, Q, m are all greater than 0 ?
        # P = max(P, 1)
        # D = max(D, 1)
        # Q = max(Q, 1)
        # m = max(m, 1)

        return ((p, d, q), (P, D, Q, m))

    @staticmethod
    def find_best_order(  # noqa: D417
        train_series,
        test_series,
        max_p=2,
        max_d=1,
        max_q=2,
        max_P=1,
        max_D=1,
        max_Q=1,
        max_m=100,
    ):
        """Find the best SARIMA order using grid search.

        Args:
            train_series (array-like): The training time series data.
            test_series (array-like): The testing time series data.
            max_p, max_d, max_q: Maximum values for non-seasonal components.
            max_P, max_D, max_Q, max_m: Maximum values for seasonal components.

        Returns:
            tuple: The best orders as ((p,d,q), (P,D,Q,m)).
        """
        # Convert inputs to numpy arrays
        train_series = np.array(train_series)
        test_series = np.array(test_series)

        best_aic = float("inf")
        best_order = ((0, 0, 0), (0, 0, 0, 1))

        # First check if there's seasonality
        potential_m = [1]  # Start with no seasonality
        if len(train_series) > 20:
            try:
                from statsmodels.tsa.stattools import acf

                acf_values = acf(train_series, nlags=min(len(train_series) // 2, 50))

                # Find peaks in ACF
                for i in range(2, min(len(acf_values), max_m + 1)):
                    if (
                        acf_values[i] > acf_values[i - 1]
                        and acf_values[i] > acf_values[i + 1]
                        and acf_values[i] > 0.2
                    ):
                        potential_m.append(i)

                # Only keep up to 3 most likely seasonal periods
                potential_m = potential_m[:3]
            except Exception:
                # If there's an error, just use m=1
                potential_m = [1]

        # If only testing m=1, use full grid search
        if len(potential_m) == 1 and potential_m[0] == 1:
            # Only need to search ARIMA models
            for p in range(max_p + 1):
                for d in range(max_d + 1):
                    for q in range(max_q + 1):
                        try:
                            model = SARIMA(order=(p, d, q), seasonal_order=(0, 0, 0, 1))
                            model.fit(train_series)
                            forecast = model.forecast(len(test_series))
                            # Calculate error metrics
                            mse = np.mean((test_series - forecast) ** 2)
                            aic = mse * len(test_series)  # Simple AIC approximation

                            if aic < best_aic:
                                best_aic = aic
                                best_order = ((p, d, q), (0, 0, 0, 1))
                        except Exception:
                            continue
        else:
            # Try different seasonal periods
            for m in potential_m:
                if m > 1:
                    # Try SARIMA models
                    for p in range(max_p + 1):
                        for d in range(max_d + 1):
                            for q in range(max_q + 1):
                                for P in range(max_P + 1):
                                    for D in range(max_D + 1):
                                        for Q in range(max_Q + 1):
                                            try:
                                                model = SARIMA(
                                                    order=(p, d, q),
                                                    seasonal_order=(P, D, Q, m),
                                                )
                                                model.fit(train_series)
                                                forecast = model.forecast(
                                                    len(test_series)
                                                )
                                                # Calculate error metrics
                                                mse = np.mean(
                                                    (test_series - forecast) ** 2
                                                )
                                                aic = mse * len(
                                                    test_series
                                                )  # Simple AIC approximation

                                                if aic < best_aic:
                                                    best_aic = aic
                                                    best_order = (
                                                        (p, d, q),
                                                        (P, D, Q, m),
                                                    )
                                            except Exception:
                                                continue
                else:
                    # For m=1, just do ARIMA
                    for p in range(max_p + 1):
                        for d in range(max_d + 1):
                            for q in range(max_q + 1):
                                try:
                                    model = SARIMA(
                                        order=(p, d, q), seasonal_order=(0, 0, 0, 1)
                                    )
                                    model.fit(train_series)
                                    forecast = model.forecast(len(test_series))
                                    # Calculate error metrics
                                    mse = np.mean((test_series - forecast) ** 2)
                                    aic = mse * len(
                                        test_series
                                    )  # Simple AIC approximation

                                    if aic < best_aic:
                                        best_aic = aic
                                        best_order = ((p, d, q), (0, 0, 0, 1))
                                except Exception:
                                    continue

        return best_order


class SARIMAX(SARIMA):
    """SARIMAX model with exogenous regressors.

    SARIMAX takes the same time_series input as SARIMA, but also allows for exogenous regressors.
    These are additional variables that can help explain the time series.

    Two-step approach:
      1. OLS regression of y on exog to get beta + residuals
        - beta = (X'X)^-1 X'y
        - resid = y - X @ beta
      2. SARIMA fit on the residuals of the OLS regression

    Forecast = SARIMA_forecast(resid) + exog_future @ beta

    Attributes:
        beta (np.ndarray): The beta coefficients.
        k_exog (int): The number of exogenous variables.
    """

    def __init__(self, order=(0, 0, 0), seasonal_order=(0, 0, 0, 1)):
        """Initialize the SARIMAX model.

        Args:
            order (tuple): Non-seasonal ARIMA order (p, d, q).
            seasonal_order (tuple): Seasonal order (P, D, Q, m).
        """
        super().__init__(order=order, seasonal_order=seasonal_order)
        self.beta = None
        self.k_exog = None

    def __name__(self):
        return "SARIMAX"

    def __str__(self):
        return f"SARIMAX(order={self.order}, seasonal_order={self.seasonal_order})"

    def fit(self, time_series, exog, bound_lower=None, bound_upper=None):
        """Fit the SARIMAX model to the given time series and exogenous regressors.

        Args:
            time_series (array-like): The time series data.
            exog (array-like): The exogenous regressors.
            bound_lower (float): Lower bound for beta coefficients.
            bound_upper (float): Upper bound for beta coefficients.

        Returns:
            self: The fitted SARIMAX model.
        """
        y = np.asarray(time_series, dtype=float)
        X = np.asarray(exog, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if len(y) != len(X):
            raise ValueError("y and exog must have the same length")

        # Step 1: OLS to estimate initial beta
        beta_ols, *_ = np.linalg.lstsq(X, y, rcond=None)

        # Step 2: Non-linear optimization of beta using scipy's minimize
        def objective_function(beta):
            """Objective function for beta optimization: sum of squared residuals."""
            residuals = y - X.dot(beta)
            return np.sum(residuals**2)

        bounds = [(bound_lower, bound_upper) for _ in range(X.shape[1])]
        # Use L-BFGS-B method for bounded optimization
        result = minimize(
            objective_function, beta_ols, method="L-BFGS-B", bounds=bounds
        )
        self.beta = result.x
        self.k_exog = X.shape[1]

        # Step 3: Compute residuals using optimized beta
        resid = y - X.dot(self.beta)

        # Step 4: Fit SARIMA on residuals
        super().fit(resid)

        # Keep full y for seasonal inversion
        self.original_series = y.copy()
        return self

    def forecast(self, steps, exog_future):
        """Forecast future values using the fitted SARIMAX model.

        Args:
            steps (int): The number of steps to forecast.
            exog_future (array-like): The exogenous regressors for the future values.

        Returns:
            array-like: The forecasted values.
        """
        if self.beta is None or self.fitted_model is None:
            raise ValueError("Fit model before forecasting")

        # Validate exog_future
        Xf = np.asarray(exog_future, dtype=float)
        if Xf.ndim == 1:
            Xf = Xf.reshape(-1, 1)
        if Xf.shape[1] != self.k_exog:
            raise ValueError(f"exog_future must have {self.k_exog} columns")

        # SARIMA forecast on residuals
        resid_fc = super().forecast(steps)

        # Add exogenous effect back
        return resid_fc + Xf.dot(self.beta)

    @staticmethod
    def suggest_order(  # noqa: D417
        endog,
        exog,
        max_p=3,
        max_d=2,
        max_q=3,
        max_P=2,
        max_D=1,
        max_Q=2,
        max_m=100,
    ):
        """Suggest ((p,d,q),(P,D,Q,m)) for SARIMAX.

        Regress endog on exog to get residuals, then call SARIMA.suggest_order on residuals.

        Args:
            endog (array-like): The endogenous variable.
            exog (array-like): The exogenous regressors.
            max_p, max_d, max_q: Maximum values for non-seasonal components.
            max_P, max_D, max_Q, max_m: Maximum values for seasonal components.

        Returns:
            tuple: The optimal orders (p, d, q, P, D, Q, m).
        """
        y = np.asarray(endog, dtype=float)
        X = np.asarray(exog, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X.dot(beta)
        return SARIMA.suggest_order(
            resid,
            max_p=max_p,
            max_d=max_d,
            max_q=max_q,
            max_P=max_P,
            max_D=max_D,
            max_Q=max_Q,
            max_m=max_m,
        )

    @staticmethod
    def find_best_order(  # noqa: D417
        train_endog,
        test_endog,
        train_exog,
        test_exog,
        max_p=2,
        max_d=1,
        max_q=2,
        max_P=1,
        max_D=1,
        max_Q=1,
        max_m=100,
    ):
        """Grid-search over ((p,d,q),(P,D,Q,m)) to minimize MSE on test set.

        Args:
            train_endog (array-like): The training endogenous variable.
            test_endog (array-like): The testing endogenous variable.
            train_exog (array-like): The training exogenous regressors.
            test_exog (array-like): The testing exogenous regressors.
            max_p, max_d, max_q: Maximum values for non-seasonal components.
            max_P, max_D, max_Q, max_m: Maximum values for seasonal components.

        Returns:
            tuple: The best orders ((p,d,q),(P,D,Q,m)).
        """
        y_train = np.asarray(train_endog, dtype=float)
        y_test = np.asarray(test_endog, dtype=float)
        X_train = np.asarray(train_exog, dtype=float)
        X_test = np.asarray(test_exog, dtype=float)
        if X_train.ndim == 1:
            X_train = X_train.reshape(-1, 1)
            X_test = X_test.reshape(-1, 1)

        best_mse = float("inf")
        best_order = ((0, 0, 0), (0, 0, 0, 1))

        # Determine candidate seasonal periods
        m_candidates = [1]
        if len(y_train) > 2:
            from statsmodels.tsa.stattools import acf

            acf_vals = acf(y_train, nlags=min(len(y_train) // 2, max_m))
            peaks = [
                i
                for i in range(2, len(acf_vals) - 1)
                if acf_vals[i] > acf_vals[i - 1]
                and acf_vals[i] > acf_vals[i + 1]
                and acf_vals[i] > 0.2
            ]
            m_candidates = [1] + peaks[:2]

        # Grid search
        for m in m_candidates:
            for p in range(max_p + 1):
                for d in range(max_d + 1):
                    for q in range(max_q + 1):
                        for P in range(max_P + 1):
                            for D in range(max_D + 1):
                                for Q in range(max_Q + 1):
                                    try:
                                        model = SARIMAX(
                                            order=(p, d, q), seasonal_order=(P, D, Q, m)
                                        )
                                        model.fit(y_train, X_train)
                                        fc = model.forecast(len(y_test), X_test)
                                        mse = np.mean((y_test - fc) ** 2)
                                        if mse < best_mse:
                                            best_mse = mse
                                            best_order = ((p, d, q), (P, D, Q, m))
                                    except Exception:
                                        continue

        return best_order
