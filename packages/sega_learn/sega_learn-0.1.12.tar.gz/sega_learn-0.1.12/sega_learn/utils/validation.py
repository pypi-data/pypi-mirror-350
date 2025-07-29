from inspect import isclass

import numpy as np


def check_is_fitted(estimator, attributes=None, msg=None):
    """Perform is_fitted validation for an estimator.

    Checks if the estimator is fitted by verifying the presence of
    fitted attributes (attributes that are typically added after fit).

    Args:
        estimator: object
            Instance of an estimator to check.
        attributes: str, list or tuple of str, optional (default=None)
            Attribute(s) name(s) given as string or a list/tuple of strings
            Eg.: ``["coef_", "estimator_", ...], "coef_"``
            If `None`, performs a check looking for any attribute that
            ends with an underscore and does not start with double underscore.
        msg: str, optional (default=None)
            The default error message is, "This {estimator_name} instance is not
            fitted yet. Call 'fit' with appropriate arguments before using
            this estimator."

            For custom messages if "%s" is present in the message string,
            it is substituted for the estimator name.
            Eg. : "Estimator, %s, must be fitted before predicting."

    Raises:
        RuntimeError: If the estimator has not been fitted yet.
    """
    if isclass(estimator):
        raise TypeError(f"{estimator} is a class, not an instance.")

    estimator_name = type(estimator).__name__

    if msg is None:
        msg = (
            f"This {estimator_name} instance is not fitted yet. "
            "Call 'fit' with appropriate arguments before using this estimator."
        )

    if attributes is not None:
        if not isinstance(attributes, (list, tuple)):
            attributes = [attributes]
        attrs_present = all(hasattr(estimator, attr) for attr in attributes)
    else:
        # Default check: look for any attribute ending in '_'
        attrs_present = any(
            attr.endswith("_") and not attr.startswith("__") for attr in vars(estimator)
        )

    if not attrs_present:
        raise RuntimeError(msg % estimator_name if "%s" in msg else msg)


def check_X_y(X, y):
    """Input validation for standard estimators.

    Checks X and y for consistent length, enforces X to be 2D and y 1D or 2D(n,1),
    and ensures that data is numeric and finite.

    Args:
        X : array-like of shape (n_samples, n_features)
            Input data.
        y : array-like of shape (n_samples,) or (n_samples, 1)
            Target values.

    Returns:
        X_converted : ndarray of shape (n_samples, n_features)
            The converted and validated X.
        y_converted : ndarray of shape (n_samples,) or (n_samples, 1)
            The converted and validated y.

    Raises:
        ValueError: If X and y have inconsistent lengths, shapes are incorrect,
                    data is empty, or contains NaNs or infinite values.
        TypeError: If X or y are not array-like or cannot be converted to numeric.
    """
    if X is None or y is None:
        raise ValueError("X and y cannot be None.")

    try:
        # Attempt conversion to NumPy arrays, allows lists, pandas Series/DataFrames etc.
        X_converted = np.asarray(X, dtype=np.float64)  # Ensure float for numeric ops
        y_converted = np.asarray(y)  # Keep original dtype for y initially
    except (TypeError, ValueError) as e:
        raise TypeError(
            f"X and y must be array-like structures convertible to NumPy arrays. Error: {e}"
        ) from e

    if X_converted.shape[0] != y_converted.shape[0]:
        raise ValueError(
            f"Found input variables with inconsistent numbers of samples: "
            f"[{X_converted.shape[0]}, {y_converted.shape[0]}]"
        )

    if X_converted.shape[0] == 0:
        raise ValueError("Found array with 0 sample(s).")

    if X_converted.ndim != 2:
        raise ValueError(
            f"Expected 2D array for X, got {X_converted.ndim}D array instead."
        )

    # Allow y to be 1D or 2D (n_samples, 1)
    if y_converted.ndim == 2 and y_converted.shape[1] != 1:
        raise ValueError(
            f"Expected 1D array or 2D array with shape (n_samples, 1) for y, got shape {y_converted.shape} instead."
        )
    elif y_converted.ndim > 2:
        raise ValueError(
            f"Expected 1D array or 2D array with shape (n_samples, 1) for y, got {y_converted.ndim}D array instead."
        )

    # Check for NaN or infinite values
    if np.isnan(X_converted).any() or np.isinf(X_converted).any():
        raise ValueError("Input X contains NaN or infinite values.")
    # Check y only if it's expected to be numeric (e.g., regression)
    # For classification, NaNs might indicate missing labels, which could be handled differently.
    # Let's check for inf always, but NaN only if dtype suggests numeric.
    if np.isinf(y_converted).any():
        raise ValueError("Input y contains infinite values.")
    if np.issubdtype(y_converted.dtype, np.number) and np.isnan(y_converted).any():
        raise ValueError("Input y contains NaN values.")

    # Check if X is numeric after conversion attempt
    if not np.issubdtype(X_converted.dtype, np.number):
        raise ValueError("Input X must contain numeric values.")

    return X_converted, y_converted
