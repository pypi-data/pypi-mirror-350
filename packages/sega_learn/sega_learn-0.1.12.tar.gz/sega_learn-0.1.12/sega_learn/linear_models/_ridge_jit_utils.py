import numpy as np
from numba import njit, prange

# The following lines are used to compile the numba functions into shared library
# from numba.pycc import CC
# cc = CC('compiled_ridge_jit_utils')
# cc.verbose = True


@njit(parallel=True, fastmath=True)
# @cc.export("compiled_fit_numba_no_intercept", sig="float64[:](float64[:, :], float64[:], float64, int64, float64)")
def _fit_numba_no_intercept(X, y, alpha, max_iter, tol):
    """Fits the model to the data using coordinate descent with numba (no intercept).

    Args:
        X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
        y: (np.ndarray) - Target values of shape (n_samples,).
        alpha: (float) - Regularization strength.
        max_iter: (int) - Maximum number of iterations.
        tol: (float) - Tolerance for convergence.

    Returns:
        coef_: (np.ndarray) - Estimated coefficients of shape (n_features,).
    """
    n_samples, n_features = X.shape
    coef_ = np.zeros(n_features)  # Initialize coefficients to zeros

    for _ in range(max_iter):
        coef_old = coef_.copy()  # Save the old coefficients for convergence check

        for j in prange(n_features):
            # Compute the residual excluding the current feature
            residual = np.zeros(n_samples)
            for i in prange(n_samples):
                residual[i] = y[i] - np.dot(X[i, :], coef_) + X[i, j] * coef_[j]
            # Update the coefficient using the Ridge formula
            rho = 0.0
            norm = 0.0
            for i in prange(n_samples):
                rho += X[i, j] * residual[i]
                norm += X[i, j] * X[i, j]
            coef_[j] = rho / (norm + alpha)

        # Check for convergence
        diff = 0.0
        for j in prange(n_features):
            diff += abs(coef_[j] - coef_old[j])
        if diff < tol:
            break

    return coef_


@njit(parallel=True, fastmath=True)
# @cc.export("compiled_fit_numba_intercept", sig="Tuple((float64[:], float64))(float64[:, :], float64[:], float64, int64, float64)")
def _fit_numba_intercept(X, y, alpha, max_iter, tol):
    """Fits the model to the data using coordinate descent with numba (with intercept).

    Args:
        X: (np.ndarray) - Training feature data of shape (n_samples, n_features).
        y: (np.ndarray) - Target values of shape (n_samples,).
        alpha: (float) - Regularization strength.
        max_iter: (int) - Maximum number of iterations.
        tol: (float) - Tolerance for convergence.

    Returns:
        coef_: (np.ndarray) - Estimated coefficients of shape (n_features,).
        intercept_: (float) - Estimated intercept.
    """
    n_samples, n_features = X.shape
    coef_ = np.zeros(n_features)  # Initialize coefficients to zeros
    intercept_ = 0.0  # Initialize intercept to zero

    for _ in range(max_iter):
        coef_old = coef_.copy()  # Save the old coefficients for convergence check
        intercept_old = intercept_  # Save the old intercept for convergence check

        # Update the intercept
        residual = np.zeros(n_samples)
        for i in prange(n_samples):
            residual[i] = y[i] - np.dot(X[i, :], coef_)
        intercept_ = np.sum(residual) / n_samples

        for j in prange(n_features):
            # Compute the residual excluding the current feature
            residual = np.zeros(n_samples)
            for i in prange(n_samples):
                residual[i] = (
                    y[i] - (np.dot(X[i, :], coef_) + intercept_) + X[i, j] * coef_[j]
                )
            # Update the coefficient using the Ridge formula
            rho = 0.0
            norm = 0.0
            for i in prange(n_samples):
                rho += X[i, j] * residual[i]
                norm += X[i, j] * X[i, j]
            coef_[j] = rho / (norm + alpha)

        # Check for convergence
        diff = 0.0
        for j in prange(n_features):
            diff += abs(coef_[j] - coef_old[j])
        diff += abs(intercept_ - intercept_old)
        if diff < tol:
            break

    return coef_, intercept_


# if __name__ == "__main__":
#     cc.compile()
