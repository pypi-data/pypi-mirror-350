# TODO: Add tests for all these imputers

# HIGH LEVEL STRUCTURE OF IMPUTATION CLASSES
# --------------------------------------------------------------------------------------------
# BaseImputer: a base class for common interface and utility functions
# fit, fit_transform, transform, ...
# StatisticalImputer: a class for statistical imputation (mean, median, mode)
# DirectionalImputer: a class for directional imputation (forward, backward)
# InterpolationImputer: a class for interpolation imputation (linear, polynomial, etc.)
# KNNImputer: a class for KNN imputation
# CustomImputer: a class for custom imputation, take estimator as input and use it for imputation

import contextlib
from collections import Counter

import numpy as np
import pandas as pd

from sega_learn.nearest_neighbors.knn_classifier import KNeighborsClassifier
from sega_learn.nearest_neighbors.knn_regressor import KNeighborsRegressor
from sega_learn.utils.dataPreprocessing import Encoder, one_hot_encode

# Suppress FutureWarning about downcasting in .replace()
pd.set_option("future.no_silent_downcasting", True)


class BaseImputer:
    """Base class for imputers providing a common interface."""

    def fit(self, X, y=None):
        """Fit the imputer on the data."""
        # Default implementation for imputers that don't require fitting beyond storing data
        # or calculating simple statistics immediately usable in transform.
        # Subclasses like StatisticalImputer will override this.
        # KNNImputer doesn't need a complex fit step as the 'training' data is used directly during transform.
        self._check_input(X)
        return self

    def transform(self, X):
        """Transform the data using the fitted imputer."""
        raise NotImplementedError(
            "The transform method must be implemented by subclasses."
        )

    def fit_transform(self, X, y=None):
        """Fit the imputer and transform the data."""
        self.fit(X, y)
        return self.transform(X)

    def _check_input(self, X):
        """Basic input validation."""
        if not isinstance(X, (np.ndarray, list, tuple)):
            # Add more types like pandas DataFrame if needed
            raise TypeError("Input must be array-like (numpy array, list, tuple).")
        # Allow empty input? For now, let's assume non-empty.
        # if np.asarray(X).size == 0:
        #     raise ValueError("Input array is empty.")
        # Further checks can be added (e.g., dimensions)

    def _get_mask(self, X):
        """Get boolean mask for missing values, handling object arrays."""
        X_arr = np.asarray(X)  # Ensure array

        if self.missing_values is np.nan:
            # For object arrays, np.isnan doesn't work reliably. Check element-wise for float NaN.
            if X_arr.dtype == "object":
                # Vectorized check is faster if possible
                # Check if element is float AND is nan
                is_float_nan = np.vectorize(
                    lambda x: isinstance(x, float) and np.isnan(x)
                )
                mask = is_float_nan(X_arr)
                # Optionally, also treat None as missing
                # is_none = np.vectorize(lambda x: x is None)
                # mask = mask | is_none(X_arr)
                return mask
            else:
                # If not object, assume numeric and try isnan directly (safer)
                try:
                    # Suppress warning if casting non-float types (like int) to float for isnan
                    with np.errstate(invalid="ignore"):
                        return np.isnan(X_arr.astype(float))
                except (TypeError, ValueError):
                    # Fallback if astype float fails entirely (e.g. pure string array without np.nan)
                    return np.zeros(X_arr.shape, dtype=bool)
        else:  # missing_values is something else (e.g., 0, '?', -1)
            if X_arr.dtype == "object":
                # Element-wise comparison needed for object arrays to avoid dtype errors
                mask = np.zeros(X_arr.shape, dtype=bool)
                for index, value in np.ndenumerate(X_arr):
                    try:
                        # Handle potential comparison errors
                        if value == self.missing_values:
                            mask[index] = True
                    except TypeError:
                        pass  # Cannot compare, so not equal
                return mask
            else:
                # Can likely compare directly for non-object arrays
                try:
                    return X_arr == self.missing_values
                except (
                    TypeError,
                    ValueError,
                ):  # Safety for mixed numeric types or comparison issues
                    # Fallback to element-wise if direct comparison fails
                    mask = np.zeros(X_arr.shape, dtype=bool)
                    for index, value in np.ndenumerate(X_arr):
                        try:
                            if value == self.missing_values:
                                mask[index] = True
                        except TypeError:
                            pass
                    return mask


class StatisticalImputer(BaseImputer):
    """Statistical imputer for handling missing values using mean, median, or mode."""

    def __init__(
        self, strategy="mean", nan_policy="omit", missing_values=np.nan, warn=True
    ):
        """Initialize the StatisticalImputer with a specified strategy.

        The strategy can be "mean", "median", or "mode".
        The nan_policy can be "omit", "propagate", or "raise".
        Nan policy determines how to handle NaN values in the data.
            - "omit": Ignore NaN values when calculating the statistic.
            - "propagate": Keep NaN values in the data. Treat NaN values as 0.
            - "raise": Raise an error if NaN values are found in the data.

        Args:
            strategy (str): The imputation strategy ("mean", "median", or "mode").
            nan_policy (str): Policy for handling NaN values ("omit", "propagate", or "raise").
            missing_values (float): The value to replace missing values with.
            warn (bool, default=True): Whether to print warnings.
        """
        if strategy not in ["mean", "median", "mode"]:
            raise ValueError("Strategy must be one of 'mean', 'median', or 'mode'.")
        if nan_policy not in ["omit", "propagate", "raise"]:
            raise ValueError(
                "nan_policy must be one of 'omit', 'propagate', or 'raise'."
            )

        self.strategy = strategy
        self.nan_policy = nan_policy
        self.statistic_ = None
        self.missing_values = missing_values
        self.statistic_ = None
        self.is_fitted_ = False
        self.warn = warn

    def _calculate_mode(self, a):
        """Calculate the mode of a 1D array. Handles mixed types.

        Returns the smallest value in case of ties.
        Returns np.nan if the input is empty or mode cannot be determined.
        """
        if a.size == 0:
            return np.nan  # Cannot compute mode for empty array

        try:
            # Use collections.Counter for robust frequency counting with mixed types
            counts = Counter(a)
            if not counts:  # Should not happen if a.size > 0, but check
                return np.nan

            max_count = max(counts.values())

            # Find all items with the max count
            modes = [item for item, count in counts.items() if count == max_count]

            if not modes:  # Should not happen
                return np.nan

            # Return the smallest mode if possible (handle potential unorderable types)
            try:  # noqa: SIM105
                # Sort the modes to find the smallest
                # This might fail if modes contains unorderable types (e.g., int vs None)
                # Note: In Python 3, mixed type comparisons often raise TypeError
                modes.sort()
            except TypeError:
                # If sorting fails (mixed types like numbers and strings),
                # just return the first mode found.
                pass  # Keep modes list as is

            return modes[0]  # Return the first element (smallest if sorted)

        except Exception as e:
            # Catch potential errors during counting or sorting
            if self.warn:
                print(f"Warning: Error calculating mode: {e}. Returning NaN.")
            return np.nan

    def fit(self, X, y=None):
        """Compute the statistic to be used for imputation.

        Args:
            X (array-like): The input data with missing values.
            y (ignored): Not used, present for compatibility.
        """
        self._check_input(X)
        # Convert pandas to numpy object array for flexibility
        if isinstance(X, (pd.DataFrame, pd.Series)):
            X_arr = X.to_numpy(dtype=object)
        else:
            # Ensure object dtype if input isn't clearly numeric, otherwise keep original
            temp_arr = np.asarray(X)
            if temp_arr.dtype.kind not in "ifub":  # Not int, float, uint, bool
                X_arr = np.array(X, dtype=object)
            else:
                X_arr = temp_arr  # Keep numeric type

        mask = self._get_mask(X_arr)  # Use the array version

        # Determine feature types for appropriate calculation
        # Assuming 2D input for now
        if X.ndim != 2:
            raise ValueError("StatisticalImputer currently expects 2D input.")

        n_features = X.shape[1]
        self.statistic_ = np.empty(
            n_features, dtype=object
        )  # Use object dtype for mixed stats

        for i in range(n_features):
            feature = X[:, i]
            feature_mask = mask[:, i]
            valid_values = feature[~feature_mask]

            if valid_values.size == 0:
                # All values are missing, cannot compute statistic
                # We could raise an error, or fill with a default (e.g., 0 for numeric, 'missing' for object)
                # Let's store None and handle it in transform (or raise here)
                # raise ValueError(f"Feature {i} contains only missing values.")
                self.statistic_[i] = (
                    np.nan
                )  # Store NaN, will be replaced later if possible
                continue

            # Attempt calculations based on strategy
            try:
                if self.strategy == "mean":
                    # Convert valid values to float for calculation
                    # Ensure NaN representation is float NaN
                    numeric_vals = pd.to_numeric(valid_values, errors="coerce")
                    # Calculate mean ignoring NaNs that might have resulted from coercion
                    mean_val = np.nanmean(numeric_vals)
                    self.statistic_[i] = (
                        mean_val if not np.isnan(mean_val) else 0
                    )  # Default to 0 if all were non-numeric
                elif self.strategy == "median":
                    numeric_vals = pd.to_numeric(valid_values, errors="coerce")
                    median_val = np.nanmedian(numeric_vals)
                    self.statistic_[i] = (
                        median_val if not np.isnan(median_val) else 0
                    )  # Default to 0
                elif self.strategy == "mode":
                    # --- USE CUSTOM MODE FUNCTION ---
                    mode_value = self._calculate_mode(valid_values)
                    self.statistic_[i] = mode_value
            except Exception as e:
                # Error during calculation (e.g., mean/median on incompatible type not caught by coerce)
                if self.warn:
                    print(
                        f"Warning: Could not apply strategy '{self.strategy}' to feature {i}. Error: {e}. Setting statistic to NaN."
                    )
                self.statistic_[i] = np.nan  # Fallback statistic

        # Handle cases where statistic could not be computed (remained NaN)
        stat_array_float = pd.to_numeric(
            self.statistic_, errors="coerce"
        )  # Try converting stats to numeric
        nan_stats_indices = np.where(np.isnan(stat_array_float))[0]

        if len(nan_stats_indices) > 0 and self.strategy != "mode":
            if self.warn:
                print(
                    f"Warning: Could not compute statistic for features {nan_stats_indices} (all values missing or type error?). Filling with defaults."
                )
            for idx in nan_stats_indices:
                # Check original column type again for better default
                original_col_valid = X_arr[:, idx][~mask[:, idx]]
                try:
                    _ = pd.to_numeric(original_col_valid, errors="raise")
                    is_numeric_col = True
                except (ValueError, TypeError):
                    is_numeric_col = False

                # Use 0 for numeric, 'missing' for categorical default
                self.statistic_[idx] = 0 if is_numeric_col else "missing"

        self.is_fitted_ = True
        return self

    def transform(self, X):
        """Impute missing values in X.

        Using the statistic computed during fit.
        This method replaces NaN values in X with the corresponding statistic.

        Args:
            X (array-like): The input data with missing values.
        """
        if not self.is_fitted_:
            raise RuntimeError(
                "The imputer has not been fitted yet. Call fit() before transform()."
            )
        self._check_input(X)
        # Use object dtype for the copy to allow filling mixed types
        if isinstance(X, (pd.DataFrame, pd.Series)):
            X_copy = X.to_numpy(copy=True, dtype=object)
        else:
            X_copy = np.array(X, copy=True, dtype=object)

        mask = self._get_mask(X_copy)

        if X_copy.ndim != 2:
            raise ValueError(
                "StatisticalImputer currently expects 2D input for transform."
            )
        if X_copy.shape[1] != len(self.statistic_):
            raise ValueError(
                f"Input has {X_copy.shape[1]} features, but imputer was fitted with {len(self.statistic_)} features."
            )

        for i in range(X_copy.shape[1]):
            feature_mask = mask[:, i]
            # Fill missing values using the calculated statistic for the column
            fill_value = self.statistic_[i]
            # Handle case where the statistic itself is NaN (all missing column during fit)
            # Decide on a final fill value (e.g., 0 or 'missing' based on inferred type)
            if isinstance(fill_value, float) and np.isnan(fill_value):
                # This case should ideally be handled by the default filling in fit,
                # but as a safeguard:
                try:
                    _ = pd.to_numeric(X_copy[:, i], errors="raise")
                    fill_value = 0
                except (ValueError, TypeError):
                    fill_value = "missing"
                if self.warn:
                    print(
                        f"Warning: Statistic for column {i} was NaN, filling with default '{fill_value}' during transform."
                    )

            X_copy[feature_mask, i] = fill_value

        # Attempt to infer a common dtype if possible, otherwise return object
        try:
            # Use pandas to infer dtype - more robust for mixed types
            return pd.DataFrame(X_copy).infer_objects().to_numpy()
        except Exception:
            # Fallback to object if inference fails
            return X_copy


class DirectionalImputer(BaseImputer):
    """Directional imputer for handling missing values using forward or backward fill."""

    def __init__(self, direction="forward", missing_values=np.nan, warn=True):
        """Initialize the DirectionalImputer with a specified direction.

        The direction can be "forward" or "backward".

        Args:
            direction (str): The imputation direction ("forward" or "backward").
            missing_values (float): The value to replace missing values with.
            warn (bool, default=True): Whether to print warnings.
        """
        if direction not in ["forward", "backward"]:
            raise ValueError("Direction must be either 'forward' or 'backward'.")
        self.direction = direction
        self.missing_values = missing_values
        self.is_fitted_ = False  # Fit does nothing, but good practice
        self.warn = warn

    def fit(self, X=None, y=None):
        """Fit the imputer. No operation needed for directional imputer."""
        if X is not None:
            self._check_input(X)  # Minimal check
        self.is_fitted_ = True
        return self

    def transform(self, X):
        """Impute missing values in X using the specified direction.

        Args:
            X (array-like): The input data with missing values.
        """
        if not self.is_fitted_:
            raise RuntimeError(
                "The imputer has not been fitted yet. Call fit() before transform()."
            )
        self._check_input(X)

        original_input_is_numpy = isinstance(X, np.ndarray)
        original_input_dtype = X.dtype if original_input_is_numpy else None

        X_copy = np.array(
            X, copy=True, dtype=object
        )  # Use object dtype for mixed stats
        mask = self._get_mask(X_copy)

        if X_copy.ndim == 1:  # Handle 1D array
            X_copy = X_copy.reshape(-1, 1)
            mask = mask.reshape(-1, 1)

        if X_copy.ndim != 2:
            raise ValueError("DirectionalImputer currently expects 1D or 2D input.")

        n_rows, n_cols = X_copy.shape

        if self.direction == "forward":
            for j in range(n_cols):  # Iterate through columns
                last_valid = None
                for i in range(n_rows):
                    if not mask[i, j]:
                        last_valid = X_copy[i, j]
                    elif last_valid is not None:  # If missing and have a value to fill
                        X_copy[i, j] = last_valid
        elif self.direction == "backward":
            for j in range(n_cols):  # Iterate through columns
                next_valid = None
                for i in range(n_rows - 1, -1, -1):  # Iterate backwards
                    if not mask[i, j]:
                        next_valid = X_copy[i, j]
                    elif next_valid is not None:  # If missing and have a value to fill
                        X_copy[i, j] = next_valid

        # Attempt to restore original shape if input was 1D
        if X.ndim == 1:
            X_copy = X_copy.flatten()

        # Attempt to convert to a more specific dtype using NumPy's inference.
        try:
            # Convert the object array (X_copy) to a list of Python objects.
            # Then, np.array() will infer the tightest possible dtype.
            # E.g., if X_copy contains [1, 2.0, 3] (as Python objects),
            # np.array([1, 2.0, 3]) results in a float64 array.
            # If X_copy contains [1, 'hello', 3.0], it results in an object array.
            list_representation = X_copy.tolist()
            inferred_array = np.array(list_representation)

            # If the original input X was a NumPy array with a numeric dtype,
            # and the newly inferred_array is also numeric,
            # promote their types to ensure the output can accommodate both.
            if (
                original_input_is_numpy
                and np.issubdtype(original_input_dtype, np.number)
                and np.issubdtype(inferred_array.dtype, np.number)
            ):
                final_dtype = np.promote_types(
                    original_input_dtype, inferred_array.dtype
                )

                # Cast to the promoted type if it's different from the inferred type.
                if final_dtype != inferred_array.dtype:
                    return inferred_array.astype(final_dtype)

            return inferred_array
        except (TypeError, ValueError):
            # Fallback if conversion via tolist() and np.array() fails for any reason
            # (e.g., complex nested objects not intended for simple array conversion,
            # or issues during astype if the promotion logic had a subtle flaw for an edge case).
            return X_copy


class InterpolationImputer(BaseImputer):
    """Interpolation imputer for handling missing values using linear or polynomial interpolation."""

    def __init__(self, method="linear", degree=1, missing_values=np.nan, warn=True):
        """Initialize the InterpolationImputer with a specified method.

        The method can be "linear" or "polynomial"

        Args:
            method (str): The interpolation method ("linear", "polynomial").
            degree (int): The degree of the polynomial for polynomial interpolation.
            missing_values (float): The value to replace missing values with.
            warn (bool, default=True): Whether to print warnings.
        """
        if method not in ["linear", "polynomial"]:
            raise ValueError("Method must be either 'linear' or 'polynomial'.")
        if method == "polynomial" and not isinstance(degree, int) or degree < 0:
            raise ValueError(
                "Degree must be a non-negative integer for polynomial interpolation."
            )
        # While possible to replace other values, standard interpolation libraries expect NaN
        if missing_values is not np.nan and self.warn:
            print(
                "Warning: Interpolation usually works best with np.nan as missing_values."
            )

        self.method = method
        self.degree = degree
        self.missing_values = missing_values
        self.is_fitted_ = False  # Fit does nothing here
        self.warn = warn

    def fit(self, X=None, y=None):
        """Fit the imputer on the data. No operation needed for interpolation imputer."""
        if X is not None:
            self._check_input(X)
        self.is_fitted_ = True
        return self

    def transform(self, X):
        """Impute missing values in X using interpolation.

        Args:
            X (array-like): The input data with missing values.
        """
        if not self.is_fitted_:
            raise RuntimeError(
                "The imputer has not been fitted yet. Call fit() before transform()."
            )

        self._check_input(X)
        # Ensure numeric data and float type for NaN handling
        try:
            X_copy = np.array(X, copy=True, dtype=float)
        except ValueError:
            raise TypeError(
                "InterpolationImputer requires numeric input data."
            ) from None

        if X_copy.ndim == 1:
            X_copy = X_copy.reshape(-1, 1)
        if X_copy.ndim != 2:
            raise ValueError("InterpolationImputer currently expects 1D or 2D input.")

        n_rows, n_cols = X_copy.shape
        mask = self._get_mask(
            X_copy
        )  # Handles replacing missing_values with NaN if needed

        x_indices = np.arange(n_rows)

        for j in range(n_cols):  # Process each column
            col_data = X_copy[:, j]
            col_mask = mask[:, j]
            valid_mask = ~col_mask

            if not np.any(valid_mask):  # Skip column if all values are missing
                if self.warn:
                    print(
                        f"Warning: Column {j} has no valid values for interpolation. Skipping."
                    )
                continue
            if not np.any(col_mask):  # Skip column if no values are missing
                continue

            valid_indices = x_indices[valid_mask]
            valid_values = col_data[valid_mask]

            if len(valid_indices) < 2 and self.method == "linear":
                if self.warn:
                    print(
                        f"Warning: Column {j} has fewer than 2 valid values. Cannot perform linear interpolation. Skipping."
                    )
                continue
            if len(valid_indices) <= self.degree and self.method == "polynomial":
                if self.warn:
                    print(
                        f"Warning: Column {j} has {len(valid_indices)} valid values, insufficient for polynomial interpolation of degree {self.degree}. Skipping."
                    )
                continue

            if self.method == "linear":
                # np.interp handles extrapolation at ends by default (repeats end values)
                interpolated_values = np.interp(x_indices, valid_indices, valid_values)
                X_copy[:, j] = interpolated_values  # Overwrites the whole column

            elif self.method == "polynomial":
                # Fit polynomial to valid data points
                coeffs = np.polyfit(valid_indices, valid_values, self.degree)
                # Evaluate polynomial at all indices
                poly_values = np.polyval(coeffs, x_indices)
                # Only replace missing values
                X_copy[col_mask, j] = poly_values[col_mask]

        # Attempt to restore original shape if input was 1D
        if X.ndim == 1:
            X_copy = X_copy.flatten()

        return X_copy


class KNNImputer(BaseImputer):
    """K-Nearest Neighbors imputer for handling missing values.

    This imputer treats each feature with missing values as a target variable (y)
    and uses the other features as predictors (X) to impute the missing values.
    It uses KNN regression for numerical features and KNN classification for
    categorical features.

    Important Note: Standard KNN distance metrics (Euclidean, Manhattan) do not
    handle missing values directly. This implementation uses a preliminary
    simple imputation (mean/median/mode) to create a complete dataset, which is
    then used for finding neighbors. The actual imputation for a missing value
    in feature `j` is predicted using a KNN model trained on rows where `j` was
    originally *not* missing, using the initially imputed dataset for feature values.
    """

    def __init__(
        self,
        n_neighbors=5,
        distance_metric="euclidean",
        missing_values=np.nan,
        warn=True,
    ):
        """Initialize the KNNImputer.

        Args:
            n_neighbors (int): Number of neighbors to use for imputation.
            distance_metric (str): Distance metric for KNN ('euclidean', 'manhattan', 'minkowski').
            missing_values (scalar, str, None, default=np.nan): Placeholder for missing values.
            warn (bool, default=True): Whether to print warnings.
        """
        if n_neighbors <= 0:
            raise ValueError("n_neighbors must be a positive integer.")
        if distance_metric not in ["euclidean", "manhattan", "minkowski"]:
            raise ValueError(
                "distance_metric must be one of 'euclidean', 'manhattan', or 'minkowski'."
            )

        self.n_neighbors = n_neighbors
        self.distance_metric = distance_metric
        self.missing_values = missing_values
        self.is_fitted_ = False  # Fit does nothing beyond checks

        # Internal state - determined during transform, not fit
        self._initial_imputer_num = None
        self._initial_imputer_cat = None
        self._column_types = None  # To store whether each col is numeric or categorical
        self._cat_feature_indices = None
        self._num_feature_indices = None
        self._encoder = None
        self.warn = warn

    def fit(self, X, y=None):
        """Fit the imputer on the data.

        For KNNImputer, 'fit' primarily validates input and determines
        feature types needed for the transform step. No actual KNN model
        is trained here.

        Args:
            X (array-like): The input data potentially containing missing values.
            y (ignored): Not used, present for compatibility.
        """
        self._check_input(X)
        # Use pandas to reliably handle mixed types and infer
        try:
            X_df = pd.DataFrame(X)
        except ValueError:  # Handle cases where X cannot be directly converted
            # Try converting potential string 'nan' back to np.nan first
            X_arr = np.asarray(X, dtype=object)
            X_arr[X_arr == "nan"] = np.nan
            X_df = pd.DataFrame(X_arr)

        if X_df.ndim != 2:
            raise ValueError("KNNImputer currently expects 2D input.")

        self._column_types = []
        self._num_feature_indices = []
        self._cat_feature_indices = []

        for i in range(X_df.shape[1]):
            col = X_df.iloc[:, i]
            # Use pandas inference, more robust
            try:
                # Attempt conversion to numeric, ignore errors for check
                pd.to_numeric(col, errors="raise")
                # Check if it wasn't *all* NaN initially (difficult to be certain without original mask)
                # Let's assume numeric if conversion succeeds
                self._column_types.append("numeric")
                self._num_feature_indices.append(i)
            except (ValueError, TypeError):
                self._column_types.append("categorical")
                self._cat_feature_indices.append(i)

        # Setup initial imputers (fitted during transform)
        self._initial_imputer_num = StatisticalImputer(
            strategy="mean", missing_values=self.missing_values, warn=self.warn
        )
        self._initial_imputer_cat = StatisticalImputer(
            strategy="mode", missing_values=self.missing_values, warn=self.warn
        )
        # self._encoder = OneHotEncoder(
        #     handle_unknown="ignore", sparse_output=False
        # )  # Keep sparse=False for simplicity with numpy hstack
        self._encoder = one_hot_encode

        self.is_fitted_ = True
        return self

    def transform(self, X):
        """Impute missing values in X using KNN.

        Args:
            X (array-like): The input data with missing values.
        """
        if not self.is_fitted_:
            raise RuntimeError("Call fit() before transform().")
        self._check_input(X)

        if isinstance(X, pd.DataFrame):
            X_imputed = X.to_numpy(copy=True, dtype=object)
        else:
            X_imputed = np.array(X, copy=True, dtype=object)

        if X_imputed.ndim != 2:
            raise ValueError("KNNImputer expects 2D input.")
        if X_imputed.shape[1] != len(self._column_types):
            raise ValueError(
                f"Input features ({X_imputed.shape[1]}) != fitted features ({len(self._column_types)})."
            )

        original_mask = self._get_mask(X_imputed)
        if not np.any(original_mask):
            try:
                return pd.DataFrame(X_imputed).infer_objects().to_numpy()
            except Exception:
                return X_imputed

        # 1. Initial Imputation
        X_filled_initial = X_imputed.copy()
        if self._num_feature_indices:
            num_cols_idx = self._num_feature_indices
            num_data = X_filled_initial[:, num_cols_idx]
            if self._get_mask(num_data).any():
                try:
                    self._initial_imputer_num.fit(num_data)
                    imputed_num = self._initial_imputer_num.transform(num_data)
                    X_filled_initial[:, num_cols_idx] = imputed_num.astype(float)
                except Exception as e:
                    print(f"Warning: Initial numeric imputation failed: {e}")

        if self._cat_feature_indices:
            cat_cols_idx = self._cat_feature_indices
            cat_data = X_filled_initial[:, cat_cols_idx]
            if self._get_mask(cat_data).any():
                try:
                    self._initial_imputer_cat.fit(cat_data)
                    X_filled_initial[:, cat_cols_idx] = (
                        self._initial_imputer_cat.transform(cat_data)
                    )
                except Exception as e:
                    print(f"Warning: Initial categorical imputation failed: {e}")

        # 2. Secondary Fill
        final_check_mask = self._get_mask(X_filled_initial)
        if np.any(final_check_mask):
            print(
                "Warning: NaNs remain after initial imputation. Applying secondary fill (0/missing)."
            )
            for j in range(X_filled_initial.shape[1]):
                if np.any(final_check_mask[:, j]):
                    fill_val = 0 if j in self._num_feature_indices else "missing"
                    X_filled_initial[final_check_mask[:, j], j] = fill_val

        # 3. One-Hot Encode Features for Distance Calculation
        X_numeric_part = X_filled_initial[:, self._num_feature_indices].astype(float)
        if self._cat_feature_indices:
            X_cat_part = X_filled_initial[:, self._cat_feature_indices]
            try:
                self._encoder(X_cat_part)
                X_cat_encoded = self._encoder(X_cat_part)
                X_knn_features = np.hstack((X_numeric_part, X_cat_encoded))
            except Exception as e:
                raise RuntimeError(
                    f"Categorical feature encoding failed: {e}"
                ) from None
        elif X_numeric_part.size > 0:
            X_knn_features = X_numeric_part
        else:
            raise ValueError("No features available for KNN.")

        try:
            X_knn_features = X_knn_features.astype(float)
        except ValueError as e:
            raise TypeError(
                f"Could not convert final features to numeric: {e}"
            ) from None

        # 4. Iterate through columns and impute using KNN
        output_X = X_imputed.copy()

        for j in range(output_X.shape[1]):
            col_mask = original_mask[:, j]
            if not np.any(col_mask):
                continue

            rows_to_impute_idx = np.where(col_mask)[0]
            rows_for_training_idx = np.where(~col_mask)[0]

            if len(rows_for_training_idx) < self.n_neighbors:
                if self.warn:
                    print(
                        f"Warning: Not enough samples ({len(rows_for_training_idx)}) for col {j} KNN. Using initial fill."
                    )
                output_X[rows_to_impute_idx, j] = X_filled_initial[
                    rows_to_impute_idx, j
                ]
                continue

            X_train_knn = X_knn_features[rows_for_training_idx, :]
            X_predict_knn = X_knn_features[rows_to_impute_idx, :]
            y_train_original = output_X[rows_for_training_idx, j]  # Original values

            try:
                if self._column_types[j] == "numeric":
                    knn = KNeighborsRegressor(
                        n_neighbors=self.n_neighbors,
                        distance_metric=self.distance_metric,
                    )
                    y_train_knn = y_train_original.astype(float)
                    knn.fit(X_train_knn, y_train_knn)
                    imputed_values = knn.predict(X_predict_knn)

                else:  # Categorical column
                    knn = KNeighborsClassifier(
                        n_neighbors=self.n_neighbors,
                        distance_metric=self.distance_metric,
                    )

                    # Create mapping from category to int
                    unique_categories = np.unique(y_train_original)
                    cat_to_int = {cat: i for i, cat in enumerate(unique_categories)}
                    int_to_cat = {
                        i: cat for cat, i in cat_to_int.items()
                    }  # Reverse mapping

                    # Encode y_train to integers
                    y_train_int = np.array(
                        [cat_to_int[cat] for cat in y_train_original]
                    )

                    # Fit classifier with integer labels
                    knn.fit(X_train_knn, y_train_int)

                    # Predict integer labels
                    predicted_ints = knn.predict(X_predict_knn)

                    # Decode predicted integers back to original categories
                    imputed_values = np.array(
                        [int_to_cat.get(i, "unknown_pred") for i in predicted_ints]
                    )
                    # Handle potential unknown predictions if necessary (though KNN usually predicts existing labels)
                    if "unknown_pred" in imputed_values and self.warn:
                        print(
                            f"Warning: KNNClassifier predicted an unknown integer label for column {j}."
                        )
                        # Fallback strategy: replace 'unknown_pred' with mode or initial fill?
                        # For now, let it be 'unknown_pred'

                output_X[rows_to_impute_idx, j] = imputed_values  # Fill imputed values

            except Exception as e:
                if self.warn:
                    print(
                        f"Error during KNN imputation for col {j}: {e}. Using initial fill."
                    )
                output_X[rows_to_impute_idx, j] = X_filled_initial[
                    rows_to_impute_idx, j
                ]  # Fallback

        # 5. Return imputed data
        try:
            return pd.DataFrame(output_X).infer_objects().to_numpy()
        except Exception:  # Fallback to object if inference fails
            return output_X


class CustomImputer(BaseImputer):
    """Imputes missing values using a user-provided estimator(s).

    Each feature with missing values is treated as a target. Features for the
    estimators are created from other columns after an initial simple imputation
    (mean/mode) and one-hot encoding of categorical features among them.
    """

    def __init__(
        self,
        regressor=None,
        classifier=None,
        missing_values=np.nan,
        one_hot_encode_features=True,
        warn=True,
    ):
        """Initialize the CustomImputer.

        Args:
            regressor (estimator object, optional): Estimator for numeric targets.
            classifier (estimator object, optional): Estimator for categorical targets.
            missing_values (scalar, str, None, default=np.nan): Placeholder for missing values.
            one_hot_encode_features (bool, default=True): Whether to one-hot encode
                categorical features in the matrix X used by the custom estimators.
                If False, custom estimators must handle mixed-type features.
            warn (bool, default=True): Whether to print warnings.
        """
        self.missing_values = missing_values
        self.warn = warn

        if regressor is None and classifier is None:
            raise ValueError(
                "At least one estimator (regressor or classifier) must be provided."
            )

        if regressor is not None and not (
            hasattr(regressor, "fit") and hasattr(regressor, "predict")
        ):
            raise TypeError("Regressor must have fit and predict methods.")
        if classifier is not None and not (
            hasattr(classifier, "fit") and hasattr(classifier, "predict")
        ):
            raise TypeError("Classifier must have fit and predict methods.")

        self.regressor = regressor
        self.classifier = classifier
        self.one_hot_encode_features = one_hot_encode_features
        self.is_fitted_ = False
        self._initial_imputer_num = None
        self._initial_imputer_cat = None
        self._column_types = None  # Overall column types (numeric/categorical)
        # For features fed to custom estimators:
        self._feature_cat_indices_for_ohe = (
            None  # Indices of categorical cols *within the feature set* for OHE
        )
        self._feature_num_indices_for_ohe = (
            None  # Indices of numeric cols *within the feature set* for OHE
        )
        self._ohe_feature_encoder = None  # OneHotEncoder for the feature matrix X

    def fit(self, X, y=None):
        """Fit the imputer: validate input, determine overall column types, and prepare for one-hot encoding of features if enabled."""
        self._check_input(X)
        try:
            X_df = pd.DataFrame(X).copy()
        except Exception as e:
            raise ValueError(
                f"Could not convert input X to DataFrame. Error: {e}"
            ) from None

        for col in X_df.columns:
            with contextlib.suppress(TypeError):
                current_col_series = X_df[col]
                replaced_series = current_col_series.replace(
                    ["nan", "NaN", "None", "null", "", "NA", "<NA>"], np.nan
                )
                # Address the FutureWarning by explicitly calling infer_objects.
                # This ensures that types are inferred after replacement,
                # e.g., an object column with "1", "2", "nan" might become numeric.
                X_df[col] = replaced_series.infer_objects(copy=False)

        if X_df.ndim != 2:
            raise ValueError("CustomImputer expects 2D input.")

        # Determine overall column types (numeric/categorical)
        self._column_types = []
        self._num_feature_indices = []  # Indices of numeric columns in the original X
        self._cat_feature_indices = []  # Indices of categorical columns in the original X
        for i, col_name in enumerate(X_df.columns):
            col = X_df[col_name]
            try:
                inferred_col = pd.to_numeric(col, errors="raise")
                if not inferred_col.isnull().all():
                    self._column_types.append("numeric")
                    self._num_feature_indices.append(i)
                else:
                    self._column_types.append("categorical")
                    self._cat_feature_indices.append(i)
            except (ValueError, TypeError):
                self._column_types.append("categorical")
                self._cat_feature_indices.append(i)

        if self._num_feature_indices and self.regressor is None and self.warn:
            print(
                "Warning: Numeric columns found, no regressor. Numeric imputation skipped."
            )
        if self._cat_feature_indices and self.classifier is None and self.warn:
            print(
                "Warning: Categorical columns found, no classifier. Categorical imputation skipped."
            )

        self._initial_imputer_num = StatisticalImputer(
            strategy="mean", missing_values=self.missing_values, warn=self.warn
        )
        self._initial_imputer_cat = StatisticalImputer(
            strategy="mode", missing_values=self.missing_values, warn=self.warn
        )

        if self.one_hot_encode_features:
            # self._ohe_feature_encoder = OneHotEncoder(
            #     handle_unknown="ignore", sparse_output=False
            # )
            self._ohe_feature_encoder = one_hot_encode
            # Note: The actual fitting of this OHE will happen dynamically within transform
            # for each set of features used by the custom estimators, as the feature set changes.
            # However, we determine general categorical/numerical features of the *input X* here.

        self.is_fitted_ = True
        return self

    def _prepare_features_for_estimator(self, X_data_filled, current_target_col_idx):
        """Prepares the feature matrix X for the custom estimator. Handles selection of other columns and optional one-hot encoding."""
        # Select all *other* columns to be features
        feature_indices_orig = [
            idx
            for idx in range(X_data_filled.shape[1])
            if idx != current_target_col_idx
        ]

        if not feature_indices_orig:
            return None  # No features available (e.g., if X has only 1 column)

        X_features_raw = X_data_filled[:, feature_indices_orig]

        if not self.one_hot_encode_features:
            # Estimator must handle mixed types if OHE is off
            return X_features_raw.astype(object)  # Ensure object type for mixed

        # --- One-Hot Encode features if enabled ---
        # Determine numeric and categorical columns *within this X_features_raw set*
        num_cols_in_features = []
        cat_cols_in_features = []

        for local_idx, orig_idx in enumerate(feature_indices_orig):
            if self._column_types[orig_idx] == "numeric":
                num_cols_in_features.append(local_idx)
            else:
                cat_cols_in_features.append(local_idx)

        X_features_numeric_part = X_features_raw[:, num_cols_in_features].astype(float)

        if cat_cols_in_features:
            X_features_cat_part = X_features_raw[:, cat_cols_in_features]
            # Fit OHE specifically on these categorical feature columns
            current_ohe = self._ohe_feature_encoder
            current_ohe(X_features_cat_part)
            X_features_cat_encoded = current_ohe(X_features_cat_part)

            if X_features_numeric_part.size > 0:
                X_features_processed = np.hstack(
                    (X_features_numeric_part, X_features_cat_encoded)
                )
            else:
                X_features_processed = X_features_cat_encoded
        elif X_features_numeric_part.size > 0:  # Only numeric features
            X_features_processed = X_features_numeric_part
        else:  # No features (should be caught by empty feature_indices_orig)
            return None

        return X_features_processed.astype(float)

    def transform(self, X):
        """Impute missing values in X using the provided custom estimator(s)."""
        if not self.is_fitted_:
            raise RuntimeError("Call fit() before transform().")
        self._check_input(X)

        if isinstance(X, pd.DataFrame):
            X_imputed = X.to_numpy(copy=True, dtype=object)
        else:
            X_imputed = np.array(X, copy=True, dtype=object)

        if X_imputed.ndim != 2:
            raise ValueError("CustomImputer expects 2D input.")
        if X_imputed.shape[1] != len(self._column_types):
            raise ValueError(
                f"Input features ({X_imputed.shape[1]}) != fitted features ({len(self._column_types)})."
            )

        original_mask = self._get_mask(X_imputed)
        if not np.any(original_mask):
            try:
                return pd.DataFrame(X_imputed).infer_objects().to_numpy()
            except Exception:
                return X_imputed

        # 1. Initial Imputation (Mean/Mode)
        X_filled_initial = X_imputed.copy()
        if self._num_feature_indices:  # Use original indices of num/cat columns
            num_cols_idx_orig = self._num_feature_indices
            if num_cols_idx_orig:  # Check if list is not empty
                num_data = X_filled_initial[:, num_cols_idx_orig]
                if self._get_mask(num_data).any():
                    try:
                        self._initial_imputer_num.fit(num_data)
                        imputed_num = self._initial_imputer_num.transform(num_data)
                        X_filled_initial[:, num_cols_idx_orig] = (
                            imputed_num  # Maintain type from imputer
                        )
                    except Exception as e:
                        if self.warn:
                            print(f"Warning: Initial numeric fill failed: {e}")
        if self._cat_feature_indices:
            cat_cols_idx_orig = self._cat_feature_indices
            if cat_cols_idx_orig:  # Check if list is not empty
                cat_data = X_filled_initial[:, cat_cols_idx_orig]
                if self._get_mask(cat_data).any():
                    try:
                        self._initial_imputer_cat.fit(cat_data)
                        X_filled_initial[:, cat_cols_idx_orig] = (
                            self._initial_imputer_cat.transform(cat_data)
                        )
                    except Exception as e:
                        if self.warn:
                            print(f"Warning: Initial categorical fill failed: {e}")

        # 2. Secondary Fill
        final_check_mask = self._get_mask(X_filled_initial)
        if np.any(final_check_mask):
            if self.warn:
                print(
                    "Warning: NaNs after initial fill. Applying secondary fill (0/missing)."
                )
            for j_orig in range(X_filled_initial.shape[1]):
                if np.any(final_check_mask[:, j_orig]):
                    fill_val = (
                        0 if self._column_types[j_orig] == "numeric" else "missing"
                    )
                    X_filled_initial[final_check_mask[:, j_orig], j_orig] = fill_val

        # 3. Iterate through columns and impute
        output_X = X_imputed.copy()

        for j_target_orig_idx in range(
            output_X.shape[1]
        ):  # j_target_orig_idx is the index in original X
            col_mask_orig = original_mask[:, j_target_orig_idx]
            if not np.any(col_mask_orig):
                continue

            is_numeric_target = self._column_types[j_target_orig_idx] == "numeric"
            estimator_to_use = None
            if is_numeric_target and self.regressor:
                estimator_to_use = self.regressor
            elif not is_numeric_target and self.classifier:
                estimator_to_use = self.classifier
            else:
                if self.warn:
                    print(
                        f"Warning: No suitable estimator for col {j_target_orig_idx} (type: {self._column_types[j_target_orig_idx]}). Using initial fill."
                    )
                output_X[col_mask_orig, j_target_orig_idx] = X_filled_initial[
                    col_mask_orig, j_target_orig_idx
                ]
                continue

            rows_to_impute_idx = np.where(col_mask_orig)[0]
            rows_for_training_idx = np.where(~col_mask_orig)[0]

            min_samples_required = 2
            if len(rows_for_training_idx) < min_samples_required:
                if self.warn:
                    print(
                        f"Warning: Insufficient samples ({len(rows_for_training_idx)}) for col {j_target_orig_idx}. Using initial fill."
                    )
                output_X[rows_to_impute_idx, j_target_orig_idx] = X_filled_initial[
                    rows_to_impute_idx, j_target_orig_idx
                ]
                continue

            # --- Prepare features for THIS estimator ---
            # X_filled_initial is the fully imputed dataset (mean/mode/secondary)
            X_features_processed = self._prepare_features_for_estimator(
                X_filled_initial, j_target_orig_idx
            )

            if X_features_processed is None or X_features_processed.shape[1] == 0:
                if self.warn:
                    print(
                        f"Warning: No features available for imputing column {j_target_orig_idx}. Using initial fill."
                    )
                output_X[rows_to_impute_idx, j_target_orig_idx] = X_filled_initial[
                    rows_to_impute_idx, j_target_orig_idx
                ]
                continue

            X_train_est = X_features_processed[rows_for_training_idx, :]
            X_predict_est = X_features_processed[rows_to_impute_idx, :]
            y_train_original = output_X[rows_for_training_idx, j_target_orig_idx]

            try:
                y_train_processed = y_train_original
                label_encoder = None
                if is_numeric_target:
                    y_train_processed = y_train_original.astype(float)
                else:  # Categorical target
                    label_encoder = Encoder()
                    y_train_processed = label_encoder.fit_transform(y_train_original)

                estimator_to_use.fit(X_train_est, y_train_processed)
                predicted_values = estimator_to_use.predict(X_predict_est)

                # Ensure predicted_values are np.ndarray
                if not isinstance(predicted_values, np.ndarray):
                    predicted_values = np.array(predicted_values)

                if label_encoder:
                    predicted_values = predicted_values.astype(
                        int
                    )  # Ensure int for inverse_transform
                    # Handle cases where prediction might be outside of fitted classes
                    # by transforming back only known predicted labels
                    known_preds_mask = np.isin(
                        predicted_values,
                        label_encoder.transform(label_encoder.classes_),
                    )
                    decoded_values = np.full_like(
                        predicted_values,
                        fill_value=label_encoder.classes_[0],
                        dtype=object,
                    )  # Fallback to first class
                    if np.any(
                        known_preds_mask
                    ):  # Check if there are any known predictions
                        decoded_values[known_preds_mask] = (
                            label_encoder.inverse_transform(
                                predicted_values[known_preds_mask]
                            )
                        )
                    if not np.all(known_preds_mask) and self.warn:
                        print(
                            f"Warning: Classifier predicted unknown labels for col {j_target_orig_idx}. Used fallback."
                        )
                    predicted_values = decoded_values

                output_X[rows_to_impute_idx, j_target_orig_idx] = predicted_values
            except Exception as e:
                if self.warn:
                    print(
                        f"Error during custom imputation for col {j_target_orig_idx} with {type(estimator_to_use).__name__}: {e}. Using initial fill."
                    )
                output_X[rows_to_impute_idx, j_target_orig_idx] = X_filled_initial[
                    rows_to_impute_idx, j_target_orig_idx
                ]

        # 4. Return
        try:
            return pd.DataFrame(output_X).infer_objects().to_numpy()
        except Exception:
            return output_X
