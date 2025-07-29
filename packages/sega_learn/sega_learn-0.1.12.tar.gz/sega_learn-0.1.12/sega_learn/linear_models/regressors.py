# Importing the required libraries
import warnings

import numpy as np
from scipy import linalg


def _validate_data(X, y):
    """Validates input data.

    Args:
        X : array-like of shape (n_samples, n_features): Training data.
        y : array-like of shape (n_samples,) or (n_samples, n_targets): Target values.

    Must be:
        - array-like
        - same number of samples
        - Not empty
    """
    if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
        raise ValueError("X and y must be numpy arrays")

    if X.shape[0] != y.shape[0]:
        raise ValueError("X and y must have the same number of samples")

    if X.shape[0] == 0 or y.shape[0] == 0:
        raise ValueError("X and y must not be empty")

    if np.any(np.isnan(X)) or np.any(np.isnan(y)):
        raise ValueError("X and y must not contain NaN values")

    if np.any(np.isinf(X)) or np.any(np.isinf(y)):
        raise ValueError("X and y must not contain infinite values")


class OrdinaryLeastSquares:
    """Ordinary Least Squares (OLS) linear regression model.

    Attributes:
        coef_ : ndarray of shape (n_features,) or (n_features + 1,) - Estimated coefficients for the linear regression problem. If `fit_intercept` is True, the first element is the intercept.
        intercept_ : float - Independent term in the linear model. Set to 0.0 if `fit_intercept` is False.

    Methods:
        fit(X, y): Fit the linear model to the data.
        predict(X): Predict using the linear model.
        get_formula(): Returns the formula of the model as a string.
    """

    def __init__(self, fit_intercept=True) -> None:
        """Initializes the OrdinaryLeastSquares object.

        Args:
            fit_intercept: (bool) - Whether to calculate the intercept for this model (default is True).
        """
        self.fit_intercept = fit_intercept
        self.coef_ = None
        self.intercept_ = None

    def __str__(self):
        """Returns the string representation of the model."""
        return "Ordinary Least Squares"

    def fit(self, X, y, warn=False):
        """Fits the linear regression model to the training data.

        Args:
            X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
            y: (np.ndarray) - Training target data of shape (n_samples,).
            warn: (bool), optional - Whether to print detailed warnings (default is False).

        Returns:
            self: (OrdinaryLeastSquares) - The fitted linear regression model.
        """
        _validate_data(X, y)

        # Try to use C compiled code for faster computation
        try:
            from .regressors_cython import fit_ols

            self.coef_ = fit_ols(X, y, self.fit_intercept)

            if self.fit_intercept:
                self.intercept_ = self.coef_[0]  # First element is the intercept
                self.coef_ = self.coef_[1:]  # Remaining elements are the coefficients
            else:
                self.intercept_ = 0.0  # No intercept
        except Exception as _e:
            if warn:
                warnings.warn(
                    "Tried to use C compiled code, but failed. Using Python code instead.",
                    stacklevel=2,
                )

            if self.fit_intercept:  # If fit_intercept is True
                X = np.hstack(
                    [np.ones((X.shape[0], 1)), X]
                )  # Add a column of ones to X, for the intercept

            self.coef_ = (
                np.linalg.inv(X.T @ X) @ X.T @ y
            )  # Compute the coefficients using the normal equation, w = (X^T * X)^-1 * X^T * y

            if self.fit_intercept:  # If fit_intercept is True
                self.intercept_ = self.coef_[
                    0
                ]  # Set the intercept to the first element of the coefficients
                self.coef_ = self.coef_[
                    1:
                ]  # Set the coefficients to the remaining elements

            else:  # Else if fit_intercept is False
                self.intercept_ = 0.0  # Set the intercept to 0.0

    def predict(self, X):
        """Predicts the target values using the linear model.

        Args:
            X: (np.ndarray) - Feature data of shape (n_samples, n_features).

        Returns:
            y_pred: (np.ndarray) - Predicted target values of shape (n_samples,).
        """
        if self.fit_intercept:  # If fit_intercept is True
            X = np.hstack(
                [np.ones((X.shape[0], 1)), X]
            )  # Add a column of ones to X, for the intercept
            return X @ np.hstack(
                [self.intercept_, self.coef_]
            )  # Return the predicted values

        else:  # Else if fit_intercept is False
            return X @ self.coef_  # Return the predicted values

    def get_formula(self):
        """Returns the formula of the model as a string.

        Returns:
            formula: (str) - The formula of the model.
        """
        terms = [
            f"{coef:.4f} * x_{i}" for i, coef in enumerate(self.coef_)
        ]  # Create the terms of the formula
        formula = " + ".join(terms)  # Join the terms with " + "
        if self.fit_intercept:  # If fit_intercept is True
            formula = (
                f"{self.intercept_:.2f} + " + formula
            )  # Add the intercept to the formula
        return f"y = {formula}"

    def get_params(self):
        """Returns the parameters of the model.

        Returns:
            params: (dict) - Dictionary of parameters.
        """
        params = {
            "fit_intercept": self.fit_intercept,
            "coef_": self.coef_,
            "intercept_": self.intercept_,
        }
        return params

    def set_params(self, **params):
        """Sets the parameters of the model.

        Args:
            params: (dict) - Dictionary of parameters to set.
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(
                    f"Invalid parameter {key} for {self.__class__.__name__}"
                )


class Ridge:
    """Fits the Ridge Regression model to the training data.

    Ridge regression implements L2 regularization, which helps to prevent overfitting by adding a penalty term to the loss function.

    Args:
        alpha: (float) - Regularization strength; must be a positive float (default is 1.0).
        fit_intercept: (bool), optional - Whether to calculate the intercept for this model (default is True).
        max_iter: (int), optional - Maximum number of iterations for the coordinate descent solver (default is 10000).
        tol: (float), optional - Tolerance for the optimization. The optimization stops when the change in the coefficients is less than this tolerance (default is 1e-4).

    Attributes:
        coef_: (np.ndarray) - Estimated coefficients for the linear regression problem. If `fit_intercept` is True, the first element is the intercept.
        intercept_: (float) - Independent term in the linear model. Set to 0.0 if `fit_intercept` is False.

    Methods:
        fit(X, y): Fits the Ridge Regression model to the training data.
        predict(X): Predicts using the Ridge Regression model.
        get_formula(): Returns the formula of the model as a string.
    """

    def __init__(
        self,
        alpha=1.0,
        fit_intercept=True,
        max_iter=10000,
        tol=1e-4,
        compile_numba=False,
    ):
        """Initializes the Ridge Regression model.

        Ridge regression implements L2 regularization, which helps to prevent overfitting by adding a penalty term to the loss function.

        Args:
            alpha: (float) - Regularization strength; must be a positive float (default is 1.0).
            fit_intercept: (bool), optional - Whether to calculate the intercept for this model (default is True).
            max_iter: (int), optional - Maximum number of iterations for the coordinate descent solver (default is 10000).
            tol: (float), optional - Tolerance for the optimization. The optimization stops when the change in the coefficients is less than this tolerance (default is 1e-4).
            compile_numba: (bool), optional - Whether to precompile the numba functions (default is False). If True, the numba fitting functions will be compiled before use.
        """
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.max_iter = max_iter
        self.tol = tol
        self.coef_ = None
        self.intercept_ = None

        if compile_numba:
            # Try to compile the numba functions
            try:
                from ._ridge_jit_utils import (
                    _fit_numba_intercept,
                    _fit_numba_no_intercept,
                )

                _fit_numba_no_intercept(
                    np.zeros((1, 1)),
                    np.zeros((1,)),
                    self.alpha,
                    self.max_iter,
                    self.tol,
                )
                _fit_numba_intercept(
                    np.zeros((1, 1)),
                    np.zeros((1,)),
                    self.alpha,
                    self.max_iter,
                    self.tol,
                )
            except ImportError:
                raise ImportError(
                    "Numba is not installed. Please install numba to use this feature."
                ) from None
            except Exception as e:
                print(f"Error compiling numba functions: {e}")

    def __str__(self):
        """Returns the string representation of the model."""
        return "Ridge Regression"

    def fit(self, X, y, numba=False, warn=False):
        """Fits the Ridge Regression model to the training data.

        Args:
            X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
            y: (np.ndarray) - Training target data of shape (n_samples,).
            numba: (bool), optional - Whether to use numba for faster computation (default is False).
            warn: (bool), optional - Whether to print detailed warnings (default is False).

        Returns:
            self: (Ridge) - The fitted Ridge Regression model.
        """
        _validate_data(X, y)

        if not numba:
            # Try to use C compiled code for faster computation
            try:
                from .regressors_cython import fit_ridge  # type: ignore

                self.coef_ = fit_ridge(
                    X, y, self.alpha, self.fit_intercept, self.max_iter, self.tol
                )

                if self.fit_intercept:
                    self.intercept_ = self.coef_[0]  # First element is the intercept
                    self.coef_ = self.coef_[
                        1:
                    ]  # Remaining elements are the coefficients
                else:
                    self.intercept_ = 0.0  # No intercept

                return
            except Exception as _e:
                if warn:
                    warnings.warn(
                        "Tried to use C compiled code, but failed. Using Python code instead.",
                        stacklevel=2,
                    )

        if numba:
            # Try to use numba for faster computation
            try:
                from ._ridge_jit_utils import (
                    _fit_numba_intercept,
                    _fit_numba_no_intercept,
                )

                if self.fit_intercept:
                    self.coef_, self.intercept_ = _fit_numba_intercept(
                        X, y, self.alpha, self.max_iter, self.tol
                    )
                else:
                    self.coef_ = _fit_numba_no_intercept(
                        X, y, self.alpha, self.max_iter, self.tol
                    )
                    self.intercept_ = 0.0

            # Else if numba is not available, try to use the compiled version (not as optimized)
            except Exception as _e:
                try:
                    from .compiled_ridge_jit_utils import (  # type: ignore
                        compiled_fit_numba_intercept,
                        compiled_fit_numba_no_intercept,
                    )

                    if self.fit_intercept:
                        self.coef_, self.intercept_ = compiled_fit_numba_intercept(
                            X, y, self.alpha, self.max_iter, self.tol
                        )
                    else:
                        self.coef_ = compiled_fit_numba_no_intercept(
                            X, y, self.alpha, self.max_iter, self.tol
                        )
                        self.intercept_ = 0.0
                except ImportError:
                    raise ImportError(
                        "Numba is not installed. Please install numba to use this feature."
                    ) from None
            return

        if self.fit_intercept:  # If fit_intercept is True
            X = np.hstack(
                [np.ones((X.shape[0], 1)), X]
            )  # Add a column of ones to X, for the intercept

        n_samples, n_features = X.shape  # Get the number of samples and features
        self.coef_ = np.zeros(n_features)  # Initialize the coefficients to zeros

        for _ in range(self.max_iter):  # For each iteration
            coef_old = self.coef_.copy()  # Copy the coefficients

            for j in range(n_features):  # For each feature
                residual = y - X @ self.coef_  # Compute the residuals
                rho = (
                    X[:, j] @ residual
                )  # Compute rho, the correlation between the feature and the residuals

                if j == 0 and self.fit_intercept:  # If it's the intercept term
                    self.coef_[j] = rho / (X[:, j] @ X[:, j])  # Update the coefficient

                else:  # Else, update the coefficient using the Ridge formula
                    self.coef_[j] = rho / (X[:, j] @ X[:, j] + self.alpha)

            if (
                np.sum(np.abs(self.coef_ - coef_old)) < self.tol
            ):  # If the coefficients have converged
                break

        if self.fit_intercept:  # If fit_intercept is True
            self.intercept_ = self.coef_[
                0
            ]  # Set the intercept to the first element of the coefficients
            self.coef_ = self.coef_[
                1:
            ]  # Set the coefficients to the remaining elements

        else:  # Else if fit_intercept is False
            self.intercept_ = 0.0  # Set the intercept to 0.0

    def predict(self, X):
        """Predicts the target values using the Ridge Regression model.

        Args:
            X: (np.ndarray) - Feature data of shape (n_samples, n_features).

        Returns:
            y_pred: (np.ndarray) - Predicted target values of shape (n_samples,).
        """
        if self.fit_intercept:  # If fit_intercept is True
            X = np.hstack(
                [np.ones((X.shape[0], 1)), X]
            )  # Add a column of ones to X, for the intercept
            return X @ np.hstack(
                [self.intercept_, self.coef_]
            )  # Return the predicted values

        else:  # Else if fit_intercept is False
            return X @ self.coef_  # Return the predicted values

    def get_formula(self):
        """Computes the formula of the model.

        Returns:
            formula: (str) - The formula of the model as a string.
        """
        terms = [
            f"{coef:.4f} * x_{i}" for i, coef in enumerate(self.coef_)
        ]  # Create the terms of the formula
        formula = " + ".join(terms)  # Join the terms with " + "
        if self.fit_intercept:  # If fit_intercept is True
            formula = (
                f"{self.intercept_:.2f} + " + formula
            )  # Add the intercept to the formula
        return f"y = {formula}"

    def get_params(self):
        """Returns the parameters of the model.

        Returns:
            params: (dict) - Dictionary of parameters.
        """
        params = {
            "alpha": self.alpha,
            "fit_intercept": self.fit_intercept,
            "max_iter": self.max_iter,
            "tol": self.tol,
            "coef_": self.coef_,
            "intercept_": self.intercept_,
        }
        return params

    def set_params(self, **params):
        """Sets the parameters of the model.

        Args:
            params: (dict) - Dictionary of parameters to set.
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(
                    f"Invalid parameter {key} for {self.__class__.__name__}"
                )


class Lasso:
    """Fits the Lasso Regression model to the training data.

    Lasso regression implements L1 regularization, which helps to prevent overfitting by adding a penalty term to the loss function.

    Args:
        X_train: (np.ndarray) - Training feature data of shape (n_samples, n_features).
        y_train: (np.ndarray) - Training target data of shape (n_samples,).
        X_test: (np.ndarray), optional - Testing feature data (default is None).
        y_test: (np.ndarray), optional - Testing target data (default is None).
        custom_metrics: (dict: str -> callable), optional - Custom metrics for evaluation (default is None).
        verbose: (bool), optional - If True, prints progress (default is False).

    Attributes:
        coef_: (np.ndarray) - Estimated coefficients for the linear regression problem. If `fit_intercept` is True, the first element is the intercept.
        intercept_: (float) - Independent term in the linear model. Set to 0.0 if `fit_intercept` is False.

    Returns:
        results: (list) - A list of dictionaries containing model performance metrics.
        predictions: (dict) - A dictionary of predictions for each model.
    """

    def __init__(
        self,
        alpha=1.0,
        fit_intercept=True,
        max_iter=10000,
        tol=1e-4,
        compile_numba=False,
    ):
        """Initializes the Lasso Regression model.

        Lasso regression implements L1 regularization, which helps to prevent overfitting by adding a penalty term to the loss function.

        Args:
            alpha: (float) - Regularization strength; must be a positive float (default is 1.0).
            fit_intercept: (bool), optional - Whether to calculate the intercept for this model (default is True).
            max_iter: (int), optional - Maximum number of iterations for the coordinate descent solver (default is 10000).
            tol: (float), optional - Tolerance for the optimization. The optimization stops when the change in the coefficients is less than this tolerance (default is 1e-4).
            compile_numba: (bool), optional - Whether to precompile the numba functions (default is False). If True, the numba fitting functions will be compiled before use.
        """
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.max_iter = max_iter
        self.tol = tol
        self.coef_ = None
        self.intercept_ = None

        if compile_numba:
            # Try to compile the numba functions
            try:
                from ._lasso_jit_utils import (
                    _fit_numba_intercept,
                    _fit_numba_no_intercept,
                )

                _fit_numba_no_intercept(
                    np.zeros((1, 1)),
                    np.zeros((1,)),
                    self.alpha,
                    self.max_iter,
                    self.tol,
                )
                _fit_numba_intercept(
                    np.zeros((1, 1)),
                    np.zeros((1,)),
                    self.alpha,
                    self.max_iter,
                    self.tol,
                )
            except ImportError:
                raise ImportError(
                    "Numba is not installed. Please install numba to use this feature."
                ) from None
            except Exception as e:
                print(f"Error compiling numba functions: {e}")

    def __str__(self):
        """Returns the string representation of the model."""
        return "Lasso Regression"

    def fit(self, X, y, numba=False, warn=False):
        """Fits the Lasso Regression model to the training data using coordinate descent.

        Args:
            X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
            y: (np.ndarray) - Training target data of shape (n_samples,).
            numba: (bool), optional - Whether to use numba for faster computation (default is False).
            warn: (bool), optional - Whether to print detailed warnings (default is False).

        Returns:
            self: (Lasso) - The fitted Lasso Regression model.
        """
        _validate_data(X, y)

        if not numba:
            # Try to use C compiled code for faster computation
            try:
                from .regressors_cython import fit_lasso  # type: ignore

                self.coef_ = fit_lasso(
                    X, y, self.alpha, self.fit_intercept, self.max_iter, self.tol
                )

                if self.fit_intercept:
                    self.intercept_ = self.coef_[0]  # First element is the intercept
                    self.coef_ = self.coef_[
                        1:
                    ]  # Remaining elements are the coefficients
                else:
                    self.intercept_ = 0.0  # No intercept

                return
            except Exception as _e:
                if warn:
                    warnings.warn(
                        "Tried to use C compiled code, but failed. Using Python code instead.",
                        stacklevel=2,
                    )

        if numba:
            # Try to use numba for faster computation
            try:
                from ._lasso_jit_utils import (
                    _fit_numba_intercept,
                    _fit_numba_no_intercept,
                )

                if self.fit_intercept:
                    self.coef_, self.intercept_ = _fit_numba_intercept(
                        X, y, self.alpha, self.max_iter, self.tol
                    )
                else:
                    self.coef_ = _fit_numba_no_intercept(
                        X, y, self.alpha, self.max_iter, self.tol
                    )
                    self.intercept_ = 0.0

            # Else if numba is not available, try to use the compiled version (not as optimized)
            except Exception as _e:
                try:
                    from .compiled_lasso_jit_utils import (  # type: ignore
                        compiled_fit_numba_intercept,
                        compiled_fit_numba_no_intercept,
                    )

                    if self.fit_intercept:
                        self.coef_, self.intercept_ = compiled_fit_numba_intercept(
                            X, y, self.alpha, self.max_iter, self.tol
                        )
                    else:
                        self.coef_ = compiled_fit_numba_no_intercept(
                            X, y, self.alpha, self.max_iter, self.tol
                        )
                        self.intercept_ = 0.0
                except ImportError:
                    raise ImportError(
                        "Numba is not installed. Please install numba to use this feature."
                    ) from None
            return

        if self.fit_intercept:  # If fit_intercept is True
            X = np.hstack(
                [np.ones((X.shape[0], 1)), X]
            )  # Add a column of ones to X, for the intercept

        n_samples, n_features = X.shape  # Get the number of samples and features
        self.coef_ = np.zeros(n_features)  # Initialize the coefficients to zeros

        for _ in range(self.max_iter):  # For each iteration
            coef_old = self.coef_.copy()  # Copy the coefficients

            for j in range(n_features):  # For each feature
                residual = y - X @ self.coef_  # Compute the residuals
                rho = X[:, j] @ residual  # Compute rho

                if j == 0 and self.fit_intercept:  # If it's the intercept term
                    self.coef_[j] = rho / n_samples  # Update the coefficient
                else:  # Else, update the coefficient using the Lasso formula
                    self.coef_[j] = (
                        np.sign(rho)
                        * max(0, abs(rho) - self.alpha)
                        / (X[:, j] @ X[:, j])
                    )

            if (
                np.sum(np.abs(self.coef_ - coef_old)) < self.tol
            ):  # If the coefficients have converged
                break

        if self.fit_intercept:  # If fit_intercept is True
            self.intercept_ = self.coef_[
                0
            ]  # Set the intercept to the first element of the coefficients
            self.coef_ = self.coef_[
                1:
            ]  # Set the coefficients to the remaining elements

        else:  # Else if fit_intercept is False
            self.intercept_ = 0.0  # Set the intercept to 0.0

    def predict(self, X):
        """Predicts the target values using the Lasso Regression model.

        Args:
            X: (np.ndarray) - Feature data of shape (n_samples, n_features).

        Returns:
            y_pred: (np.ndarray) - Predicted target values of shape (n_samples,).
        """
        if self.fit_intercept:  # If fit_intercept is True
            X = np.hstack(
                [np.ones((X.shape[0], 1)), X]
            )  # Add a column of ones to X, for the intercept
            return X @ np.hstack(
                [self.intercept_, self.coef_]
            )  # Return the predicted values

        else:  # Else if fit_intercept is False
            return X @ self.coef_  # Return the predicted values

    def get_formula(self):
        """Computes the formula of the model.

        Returns:
        - formula : str: The formula of the model.
        """
        terms = [
            f"{coef:.4f} * x_{i}" for i, coef in enumerate(self.coef_)
        ]  # Create the terms of the formula
        formula = " + ".join(terms)  # Join the terms with " + "
        if self.fit_intercept:  # If fit_intercept is True
            formula = (
                f"{self.intercept_:.2f} + " + formula
            )  # Add the intercept to the formula
        return f"y = {formula}"

    def get_params(self):
        """Returns the parameters of the model.

        Returns:
            params: (dict) - Dictionary of parameters.
        """
        params = {
            "alpha": self.alpha,
            "fit_intercept": self.fit_intercept,
            "max_iter": self.max_iter,
            "tol": self.tol,
            "coef_": self.coef_,
            "intercept_": self.intercept_,
        }
        return params

    def set_params(self, **params):
        """Sets the parameters of the model.

        Args:
            params: (dict) - Dictionary of parameters to set.
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(
                    f"Invalid parameter {key} for {self.__class__.__name__}"
                )


class Bayesian:
    """Fits the Bayesian Regression model to the training data using Coordinate Descent.

    Args:
        X_train: (np.ndarray) - Training feature data.
        y_train: (np.ndarray) - Training target data.
        X_test: (np.ndarray), optional - Testing feature data (default is None).
        y_test: (np.ndarray), optional - Testing target data (default is None).
        max_iter: (int), optional - The maximum number of iterations to perform (default is 300).
        tol: (float), optional - The convergence threshold. The algorithm stops when the coefficients change less than this threshold (default is 0.001).
        alpha_1: (float), optional - The shape parameter for the prior on the weights (default is 1e-06).
        alpha_2: (float), optional - The scale parameter for the prior on the weights (default is 1e-06).
        lambda_1: (float), optional - The shape parameter for the prior on the noise (default is 1e-06).
        lambda_2: (float), optional - The scale parameter for the prior on the noise (default is 1e-06).
        fit_intercept: (bool), optional - Whether to calculate the intercept for this model (default is True).

    Returns:
        intercept_: (float) - The intercept of the model.
        coef_: (np.ndarray) - Estimated coefficients for the linear regression problem. If `fit_intercept` is True, the first element is the intercept.
        n_iter_: (int) - The number of iterations performed.
        alpha_: (float) - The precision of the weights.
        lambda_: (float) - The precision of the noise.
        sigma_: (np.ndarray) - The posterior covariance of the weights.
    """

    def __init__(
        self,
        max_iter=300,
        tol=0.001,
        alpha_1=1e-06,
        alpha_2=1e-06,
        lambda_1=1e-06,
        lambda_2=1e-06,
        fit_intercept=None,
    ):
        """Implements Bayesian Regression using Coordinate Descent.

        Bayesian regression applies both L1 and L2 regularization to prevent overfitting by adding penalty terms to the loss function.

        Args:
            max_iter: (int) - The maximum number of iterations to perform (default is 300).
            tol: (float) - The convergence threshold. The algorithm stops when the coefficients change less than this threshold (default is 0.001).
            alpha_1: (float) - The shape parameter for the prior on the weights (default is 1e-06).
            alpha_2: (float) - The scale parameter for the prior on the weights (default is 1e-06).
            lambda_1: (float) - The shape parameter for the prior on the noise (default is 1e-06).
            lambda_2: (float) - The scale parameter for the prior on the noise (default is 1e-06).
            fit_intercept: (bool), optional - Whether to calculate the intercept for this model (default is True).

        Returns:
            intercept_: (float) - The intercept of the model.
            coef_: (np.ndarray) - Estimated coefficients for the linear regression problem. If `fit_intercept` is True, the first element is the intercept.
            n_iter_: (int) - The number of iterations performed.
            alpha_: (float) - The precision of the weights.
            lambda_: (float) - The precision of the noise.
            sigma_: (np.ndarray) - The posterior covariance of the weights.
        """
        self.max_iter = max_iter
        self.tol = tol
        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2
        self.lambda_1 = lambda_1
        self.lambda_2 = lambda_2
        self.fit_intercept = fit_intercept

        self.intercept_ = None
        self.coef_ = None

    def __str__(self):
        """Returns the string representation of the model."""
        return "Bayesian Regression"

    def fit(self, X, y):
        """Fits the Bayesian Regression model to the training data.

        Args:
            X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
            y: (np.ndarray) - Training target data of shape (n_samples,).

        Returns:
            self: (Bayesian) - The fitted Bayesian Regression model.
        """
        _validate_data(X, y)

        # Initialization of the values of the parameters
        eps = np.finfo(
            np.float64
        ).eps  # Machine epsilon, the smallest number that can be added to 1.0 to get a larger number

        # alpha_ is the precision of the weights, lambda_ is the precision of the noise
        alpha_ = (
            1.0 / (np.var(y) + eps)
        )  # Add `eps` in the denominator to omit division by zero if `np.var(y)` is zero
        lambda_ = 1.0  # Initialize the noise precision to 1.0

        lambda_1 = self.lambda_1
        lambda_2 = self.lambda_2
        alpha_1 = self.alpha_1
        alpha_2 = self.alpha_2

        # Variables to store the values of the parameters from the previous iteration
        self.scores_ = []
        coef_old_ = None

        XT_y = np.dot(X.T, y)  # Compute X^T * y
        U, S, Vh = linalg.svd(
            X, full_matrices=False
        )  # Compute the Singular Value Decomposition of X, X = U * S * Vh
        eigen_vals_ = S**2  # Compute the eigenvalues of X

        # Main loop for the algorithm
        for _iter in range(self.max_iter):
            # Update the coefficients
            # coef_ formula: coef_ = Vh * (S^2 / (S^2 + lambda_ / alpha_)) * U^T * y
            coef_ = np.linalg.multi_dot(
                [Vh.T, Vh / (eigen_vals_ + lambda_ / alpha_)[:, np.newaxis], XT_y]
            )

            # Update alpha and lambda according to (MacKay, 1992)
            gamma_ = np.sum(1 - alpha_ * eigen_vals_) / np.sum(
                coef_**2
            )  # Compute gamma
            lambda_ = (gamma_ + 2 * lambda_1 - 1) / (
                np.sum(coef_**2) + 2 * lambda_2
            )  # Update lambda
            alpha_ = (X.shape[0] - gamma_ + 2 * alpha_1 - 1) / (
                np.sum(y**2) + 2 * alpha_2
            )  # Update alpha

            # Check for convergence
            if coef_old_ is not None and np.sum(np.abs(coef_ - coef_old_)) < self.tol:
                break
            coef_old_ = np.copy(coef_)  # Copy the coefficients

        self.n_iter_ = _iter + 1
        self.coef_ = coef_
        self.alpha_ = alpha_
        self.lambda_ = lambda_

        # posterior covariance is given by 1/alpha_ * scaled_sigma_
        self.sigma_ = np.linalg.inv(
            np.dot(X.T, X) + lambda_ / alpha_ * np.eye(X.shape[1])
        )

        if self.fit_intercept:  # If fit_intercept is True
            self.intercept_ = self.coef_[
                0
            ]  # Set the intercept to the first element of the coefficients

        return self

    def tune(self, X, y, beta1=0.9, beta2=0.999, iter=1000):
        """Tunes the hyperparameters alpha_1, alpha_2, lambda_1, and lambda_2 using ADAM optimizer.

        Args:
            X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
            y: (np.ndarray) - Training target data of shape (n_samples,).
            beta1: (float), optional - The exponential decay rate for the first moment estimates (default is 0.9).
            beta2: (float), optional - The exponential decay rate for the second moment estimates (default is 0.999).
            iter: (int), optional - The maximum number of iterations to perform (default is 1000).

        Returns:
            best_alpha_1: (float) - The best value of alpha_1.
            best_alpha_2: (float) - The best value of alpha_2.
            best_lambda_1: (float) - The best value of lambda_1.
            best_lambda_2: (float) - The best value of lambda_2.
        """
        # Initialize the best values of the hyperparameters
        best_alpha_1 = None
        best_alpha_2 = None
        best_lambda_1 = None
        best_lambda_2 = None

        self.alpha_1 = 1e-02
        self.alpha_2 = 1e-02
        self.lambda_1 = 1e-02
        self.lambda_2 = 1e-02

        # Initialize the best MSE
        best_mse = float("inf")

        # Use ADAM optimizer to tune the hyperparameters
        beta1 = beta1  # Exponential decay rate for the first moment estimates
        beta2 = beta2  # Exponential decay rate for the second moment estimates
        epsilon = 1e-8  # A small constant to prevent division by zero
        m_alpha_1 = 0  # The first moment for alpha_1
        v_alpha_1 = 0  # The second moment for alpha_1
        m_alpha_2 = 0  # The first moment for alpha_2
        v_alpha_2 = 0  # The second moment for alpha_2
        m_lambda_1 = 0  # The first moment for lambda_1
        v_lambda_1 = 0  # The second moment for lambda_1
        m_lambda_2 = 0  # The first moment for lambda_2
        v_lambda_2 = 0  # The second moment for lambda_2
        t = 0  # The time step

        def _compute_gradient_alpha_1():
            """Compute the gradient of the loss function with respect to alpha_1."""
            return -0.5 * (np.sum(self.coef_**2) + 2 * self.alpha_2)

        def _compute_gradient_alpha_2():
            """Compute the gradient of the loss function with respect to alpha_2."""
            return -0.5 * (self.alpha_1 / self.alpha_2**2)

        def _compute_gradient_lambda_1():
            """Compute the gradient of the loss function with respect to lambda_1."""
            return -0.5 * (np.sum(self.coef_**2) + 2 * self.lambda_2)

        def _compute_gradient_lambda_2():
            """Compute the gradient of the loss function with respect to lambda_2."""
            return -0.5 * (self.lambda_1 / self.lambda_2**2)

        # loop until convergence
        while True:
            # Fit the model
            self.fit(X, y)

            # Compute the mean squared error
            mse = np.mean((y - self.predict(X)) ** 2)
            if mse < best_mse:
                print(f"\tImproved after, No of iterations: {t}, MSE: {mse:.2f}")
                best_mse = mse
                best_alpha_1 = self.alpha_1
                best_alpha_2 = self.alpha_2
                best_lambda_1 = self.lambda_1
                best_lambda_2 = self.lambda_2

            # Compute the gradients
            grad_alpha_1 = _compute_gradient_alpha_1()
            grad_alpha_2 = _compute_gradient_alpha_2()
            grad_lambda_1 = _compute_gradient_lambda_1()
            grad_lambda_2 = _compute_gradient_lambda_2()

            # Update the moving averages of the gradients
            m_alpha_1 = beta1 * m_alpha_1 + (1 - beta1) * grad_alpha_1
            v_alpha_1 = beta2 * v_alpha_1 + (1 - beta2) * grad_alpha_1**2
            m_alpha_2 = beta1 * m_alpha_2 + (1 - beta1) * grad_alpha_2
            v_alpha_2 = beta2 * v_alpha_2 + (1 - beta2) * grad_alpha_2**2
            m_lambda_1 = beta1 * m_lambda_1 + (1 - beta1) * grad_lambda_1
            v_lambda_1 = beta2 * v_lambda_1 + (1 - beta2) * grad_lambda_1**2
            m_lambda_2 = beta1 * m_lambda_2 + (1 - beta1) * grad_lambda_2
            v_lambda_2 = beta2 * v_lambda_2 + (1 - beta2) * grad_lambda_2**2

            # Compute the bias-corrected estimates
            m_alpha_1_hat = m_alpha_1 / (1 - beta1 ** (t + 1))
            v_alpha_1_hat = v_alpha_1 / (1 - beta2 ** (t + 1))
            m_alpha_2_hat = m_alpha_2 / (1 - beta1 ** (t + 1))
            v_alpha_2_hat = v_alpha_2 / (1 - beta2 ** (t + 1))
            m_lambda_1_hat = m_lambda_1 / (1 - beta1 ** (t + 1))
            v_lambda_1_hat = v_lambda_1 / (1 - beta2 ** (t + 1))
            m_lambda_2_hat = m_lambda_2 / (1 - beta1 ** (t + 1))
            v_lambda_2_hat = v_lambda_2 / (1 - beta2 ** (t + 1))

            # Update the hyperparameters
            self.alpha_1 -= 0.01 * m_alpha_1_hat / (np.sqrt(v_alpha_1_hat) + epsilon)
            self.alpha_2 -= 0.01 * m_alpha_2_hat / (np.sqrt(v_alpha_2_hat) + epsilon)
            self.lambda_1 -= 0.01 * m_lambda_1_hat / (np.sqrt(v_lambda_1_hat) + epsilon)
            self.lambda_2 -= 0.01 * m_lambda_2_hat / (np.sqrt(v_lambda_2_hat) + epsilon)

            # Check for convergence, if the gradients are close to zero
            if (
                np.abs(grad_alpha_1) < 1e-6
                and np.abs(grad_alpha_2) < 1e-6
                and np.abs(grad_lambda_1) < 1e-6
                and np.abs(grad_lambda_2) < 1e-6
            ):
                print(f"Converged in {t} iterations.")
                break
            elif t >= iter:
                print(f"Stopped after {t} iterations.")
                break
            t += 1

        # Fit the model with the best hyperparameters
        self.alpha_1 = best_alpha_1
        self.alpha_2 = best_alpha_2
        self.lambda_1 = best_lambda_1
        self.lambda_2 = best_lambda_2
        self.fit(X, y)

        # Return the best hyperparameters, and fitted model
        return best_alpha_1, best_alpha_2, best_lambda_1, best_lambda_2

    def predict(self, X):
        """Predicts the target values using the Bayesian Regression model.

        Args:
            X: (np.ndarray) - Feature data of shape (n_samples, n_features).

        Returns:
            y_pred: (np.ndarray) - Predicted target values of shape (n_samples,).
        """
        return np.dot(X, self.coef_)

    def get_formula(self):
        """Computes the formula of the model.

        Returns:
            formula: (str) - The formula of the model as a string.
        """
        terms = [
            f"{coef:.4f} * x_{i}" for i, coef in enumerate(self.coef_)
        ]  # Create the terms of the formula
        formula = " + ".join(terms)  # Join the terms with " + "
        if self.fit_intercept:  # If fit_intercept is True
            formula = (
                f"{self.intercept_:.2f} + " + formula
            )  # Add the intercept to the formula
        return f"y = {formula}"

    def get_params(self):
        """Returns the parameters of the model.

        Returns:
            params: (dict) - Dictionary of parameters.
        """
        params = {
            "alpha_1": self.alpha_1,
            "alpha_2": self.alpha_2,
            "lambda_1": self.lambda_1,
            "lambda_2": self.lambda_2,
            "fit_intercept": self.fit_intercept,
            "max_iter": self.max_iter,
            "tol": self.tol,
            "coef_": self.coef_,
            "intercept_": self.intercept_,
        }
        return params

    def set_params(self, **params):
        """Sets the parameters of the model.

        Args:
            params: (dict) - Dictionary of parameters to set.
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(
                    f"Invalid parameter {key} for {self.__class__.__name__}"
                )


class RANSAC:
    """Fits the RANSAC (RANdom SAmple Consensus) algorithm for robust linear regression.

    Args:
        X_train: (np.ndarray) - Training feature data.
        y_train: (np.ndarray) - Training target data.
        X_test: (np.ndarray), optional - Testing feature data (default is None).
        y_test: (np.ndarray), optional - Testing target data (default is None).
        n: (int), optional - Number of data points to estimate parameters (default is 10).
        k: (int), optional - Maximum iterations allowed (default is 100).
        t: (float), optional - Threshold value to determine if points are fit well, in terms of residuals (default is 0.05).
        d: (int), optional - Number of close data points required to assert model fits well (default is 10).
        model: (object), optional - The model to use for fitting. If None, uses Ordinary Least Squares (default is None).
        auto_scale_t: (bool), optional - Whether to automatically scale the threshold until a model is fit (default is False).
        scale_t_factor: (float), optional - Factor by which to scale the threshold until a model is fit (default is 2).
        auto_scale_n: (bool), optional - Whether to automatically scale the number of data points until a model is fit (default is False).
        scale_n_factor: (float), optional - Factor by which to scale the number of data points until a model is fit (default is 2).

    Returns:
        best_fit: (object) - The best model fit.
        best_error: (float) - The best error achieved by the model.
        best_n: (int) - The best number of data points used to fit the model.
        best_t: (float) - The best threshold value used to determine if points are fit well, in terms of residuals.
        best_model: (object) - The best model fit.
    """

    def __init__(
        self,
        n=10,
        k=100,
        t=0.05,
        d=10,
        model=None,
        auto_scale_t=False,
        scale_t_factor=2,
        auto_scale_n=False,
        scale_n_factor=2,
    ):
        """Fits the RANSAC (RANdom SAmple Consensus) algorithm for robust linear regression.

        Args:
            X_train: (np.ndarray) - Training feature data.
            y_train: (np.ndarray) - Training target data.
            X_test: (np.ndarray), optional - Testing feature data (default is None).
            y_test: (np.ndarray), optional - Testing target data (default is None).
            n: (int), optional - Number of data points to estimate parameters (default is 10).
            k: (int), optional - Maximum iterations allowed (default is 100).
            t: (float), optional - Threshold value to determine if points are fit well, in terms of residuals (default is 0.05).
            d: (int), optional - Number of close data points required to assert model fits well (default is 10).
            model: (object), optional - The model to use for fitting. If None, uses Ordinary Least Squares (default is None).
            auto_scale_t: (bool), optional - Whether to automatically scale the threshold until a model is fit (default is False).
            scale_t_factor: (float), optional - Factor by which to scale the threshold until a model is fit (default is 2).
            auto_scale_n: (bool), optional - Whether to automatically scale the number of data points until a model is fit (default is False).
            scale_n_factor: (float), optional - Factor by which to scale the number of data points until a model is fit (default is 2).

        Returns:
            best_fit: (object) - The best model fit.
            best_error: (float) - The best error achieved by the model.
            best_n: (int) - The best number of data points used to fit the model.
            best_t: (float) - The best threshold value used to determine if points are fit well, in terms of residuals.
            best_model: (object) - The best model fit.
        """
        # Can only scale one of the threshold or the number of data points
        assert not (auto_scale_t and auto_scale_n), (
            "Can only scale one of the threshold or the number of data points"
        )

        # Default model is Ordinary Least Squares
        self.model = (
            OrdinaryLeastSquares(fit_intercept=True) if model is None else model
        )

        self.n = n  # Number of data points to estimate parameters
        self.k = k  # Maximum iterations allowed
        self.t = t  # Threshold value to determine if points are fit well, in terms of residuals
        self.d = d  # Number of close data points required to assert model fits well

        self.best_fit = None  # Best model fit
        self.best_error = np.inf  # Best error

        # If after all iterations, the model was not fit, scale the threshold until it fits
        self.scale_threshold = auto_scale_t
        self.scale_t_factor = scale_t_factor

        # If after all iterations, the model was not fit, scale the number of data points until it fits
        self.scale_n = auto_scale_n
        self.scale_n_factor = scale_n_factor

    def __str__(self):
        """Returns the string representation of the model."""
        return "RANSAC"

    def _square_loss(self, y_true, y_pred):
        """Compute the square loss."""
        return (y_true - y_pred) ** 2

    def _mean_square_loss(self, y_true, y_pred):
        """Compute the mean square loss."""
        return np.mean(self._square_loss(y_true, y_pred))

    def fit(self, X, y):
        """Fits the RANSAC model to the training data.

        Args:
            X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
            y: (np.ndarray) - Training target data of shape (n_samples,).

        Returns:
            None
        """
        _validate_data(X, y)

        for _ in range(self.k):
            # Randomly select n data points
            idx = np.random.choice(X.shape[0], self.n, replace=False)
            X_subset, y_subset = X[idx], y[idx]

            # Fit the model
            self.model.fit(X_subset, y_subset)

            # Compute the residuals
            y_pred = self.model.predict(X)
            residuals = np.abs(y - y_pred)

            # Compute the inliers, the data points that are fit well
            inliers = residuals < self.t

            # Check if the model fits well
            if np.sum(inliers) > self.d:
                # Update the best model
                error = np.sum(self._square_loss(y, y_pred))
                if error < self.best_error:
                    self.best_error = error
                    self.best_fit = self.model

        # If the model was not fit, scale the threshold
        if self.best_fit is None and self.scale_threshold:
            print(
                f"\tNo model fit, scaling threshold from {self.t:.2} to {(self.scale_t_factor * self.t):.2}"
            )
            self.t *= self.scale_t_factor
            self.fit(X, y)

        # If the model was not fit, scale the number of data points
        if self.best_fit is None and self.scale_n:
            if (self.scale_n_factor * self.n) > X.shape[0]:
                raise ValueError(
                    "Cannot scale number of data points beyond the number of data points available."
                )

            print(
                f"\tNo model fit, scaling number of data points from {self.n} to {self.scale_n_factor * self.n}"
            )
            self.n *= self.scale_n_factor
            self.fit(X, y)

    def predict(self, X):
        """Predicts the target values using the best fit model.

        Args:
            X: (np.ndarray) - Feature data of shape (n_samples, n_features).

        Returns:
            y_pred: (np.ndarray) - Predicted target values of shape (n_samples,).
        """
        return self.best_fit.predict(X)

    def get_formula(self):
        """Computes the formula of the model if fit, else returns "No model fit available"."""
        try:
            return self.best_fit.get_formula()
        except Exception as _e:
            return "No model fit available"

    def get_params(self):
        """Returns the parameters of the model.

        Returns:
            params: (dict) - Dictionary of parameters.
        """
        params = {
            "n": self.n,
            "k": self.k,
            "t": self.t,
            "d": self.d,
            "model": self.model,
            "auto_scale_t": self.scale_threshold,
            "scale_t_factor": self.scale_t_factor,
            "auto_scale_n": self.scale_n,
            "scale_n_factor": self.scale_n_factor,
        }
        return params

    def set_params(self, **params):
        """Sets the parameters of the model.

        Args:
            params: (dict) - Dictionary of parameters to set.
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(
                    f"Invalid parameter {key} for {self.__class__.__name__}"
                )


class PassiveAggressiveRegressor:
    """Fits the Passive Aggressive Regression model to the training data.

    Args:
        X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
        y: (np.ndarray) - Training target data of shape (n_samples,).
        save_steps: (bool), optional - Whether to save the weights and intercept at each iteration (default is False).
        verbose: (bool), optional - If True, prints progress during training (default is False).

    Attributes:
        coef_: (np.ndarray) - Estimated coefficients for the regression problem.
        intercept_: (float) - Independent term in the linear model.
        steps_: (list of tuples), optional - The weights and intercept at each iteration if `save_steps` is True.
    """

    def __init__(self, C=1.0, max_iter=1000, tol=1e-3):
        """Fits the Passive Aggressive Regression model to the training data.

        Args:
            C: (float) - Regularization parameter/step size (default is 1.0).
            max_iter: (int) - The maximum number of passes over the training data (default is 1000).
            tol: (float) - The stopping criterion (default is 1e-3).

        Attributes:
            coef_: (np.ndarray) - Estimated coefficients for the regression problem.
            intercept_: (float) - Independent term in the linear model.
        """
        self.C = C  # Regularization parameter/step size
        self.max_iter = max_iter  # The maximum number of passes over the training data
        self.tol = tol  # The stopping criterion

        self.coef_ = None  # The learned weights
        self.intercept_ = None  # The learned intercept

    def __str__(self):
        """Returns the string representation of the model."""
        return "Passive Aggressive Regressor"

    def fit(self, X, y, save_steps=False, verbose=False):
        """Fits the Passive Aggressive Regression model to the training data.

        Args:
            X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
            y: (np.ndarray) - Training target data of shape (n_samples,).
            save_steps: (bool), optional - Whether to save the weights and intercept at each iteration (default is False).
            verbose: (bool), optional - If True, prints progress during training (default is False).

        Returns:
            None
        """
        _validate_data(X, y)

        # Initialize the weights and the intercept
        self.coef_ = np.zeros(X.shape[1])
        self.intercept_ = 0.0

        # Initialize lists to store the weights and intercept at each iteration
        if save_steps:
            self.steps_ = []

        # For each iteration
        for _ in range(self.max_iter):
            if verbose:
                print(f"\tIteration: {_}")
            # Copy the weights for the previous iteration
            prev_coef = self.coef_.copy()

            # For each sample, each sample is a pass over the training data
            for i in range(X.shape[0]):
                y_pred = (
                    np.dot(X[i], self.coef_) + self.intercept_
                )  # Compute the predicted value

                loss = max(
                    0, np.abs(y[i] - y_pred) - self.tol
                )  # Compute the hinge loss (max(0, |y - y_pred| - tol))
                learning_rate = loss / (
                    np.dot(X[i], X[i]) + 1 / (2 * self.C)
                )  # Compute the learning rate (loss / (||X||^2 + 1 / (2 * C)))

                # If loss is greater than 0, update the weights
                if loss > 0:
                    self.coef_ += (
                        learning_rate * X[i] * np.sign(y[i] - y_pred)
                    )  # Update the weights (w = w + learning_rate * x * sign(y - y_pred))
                    self.intercept_ += learning_rate * np.sign(
                        y[i] - y_pred
                    )  # Update the intercept (b = b + learning_rate * sign(y - y_pred))

            # Save the weights and intercept at each iteration
            if save_steps:
                self.steps_.append((self.coef_.copy(), self.intercept_))

            # Check for convergence
            weight_diff = np.linalg.norm(self.coef_ - prev_coef)
            if weight_diff < self.tol:
                break

    def predict(self, X):
        """Predict using the linear model. Dot product of X and the coefficients."""
        return np.dot(X, self.coef_) + self.intercept_

    def predict_all_steps(self, X):
        """Predict using the linear model at each iteration. (save_steps=True)."""
        assert hasattr(self, "steps_"), "Model has not been fitted with save_steps=True"

        predictions = []
        for coef, intercept in self.steps_:
            predictions.append(np.dot(X, coef) + intercept)

        return predictions

    def get_formula(self):
        """Computes the formula of the model.

        Returns:
            formula : str: The formula of the model.
        """
        terms = [
            f"{coef:.4f} * x_{i}" for i, coef in enumerate(self.coef_)
        ]  # Create the terms of the formula
        formula = " + ".join(terms)  # Join the terms with " + "
        return f"y = {formula} + {self.intercept_:.2f}"

    def get_params(self):
        """Returns the parameters of the model.

        Returns:
            params: (dict) - Dictionary of parameters.
        """
        params = {
            "C": self.C,
            "max_iter": self.max_iter,
            "tol": self.tol,
            "coef_": self.coef_,
            "intercept_": self.intercept_,
        }
        return params

    def set_params(self, **params):
        """Sets the parameters of the model.

        Args:
            params: (dict) - Dictionary of parameters to set.
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(
                    f"Invalid parameter {key} for {self.__class__.__name__}"
                )
