import numpy as np

from .baseSVM import BaseSVM


class OneClassSVM(BaseSVM):
    """OneClassSVM is a custom implementation of a One-Class Support Vector Machine (SVM) for anomaly detection using gradient descent.

    It inherits from the BaseSVM class and supports various kernel functions.

    Attributes:
        support_vectors_ (array-like of shape (n_support_vectors, n_features)):
            The support vectors identified during training.
        support_vector_alphas_ (array-like of shape (n_support_vectors,)):
            The Lagrange multipliers (alpha) corresponding to the support vectors.
        b (float):
            The bias term (rho) computed during training.

    Methods:
        __init__(C=1.0, tol=1e-4, max_iter=1000, learning_rate=0.01, kernel="linear",
                 degree=3, gamma="scale", coef0=0.0):
            Initialize the OneClassSVM with hyperparameters.
        _fit(X, y=None):
            Fit the OneClassSVM model using gradient descent for anomaly detection.
        decision_function(X):
            Compute the decision function values for the input samples.
        predict(X):
            Predict whether the input samples are inliers (1) or outliers (-1).
        score(X, y):
            Compute the mean accuracy of predictions compared to true labels.
        __sklearn_is_fitted__():
            Check if the model has been fitted. For compatibility with sklearn.
    """

    def __init__(
        self,
        C=1.0,
        tol=1e-4,
        max_iter=1000,
        learning_rate=0.01,
        kernel="linear",
        degree=3,
        gamma="scale",
        coef0=0.0,
    ):
        """Initialize the OneClassSVM with hyperparameters.

        Args:
            C: (float) - Regularization parameter (default is 1.0).
            tol: (float) - Tolerance for stopping criteria (default is 1e-4).
            max_iter: (int) - Maximum number of iterations (default is 1000).
            learning_rate: (float) - Learning rate for gradient descent (default is 0.01).
            kernel: (str) - Kernel type ("linear", "poly", "rbf", "sigmoid") (default is "linear").
            degree: (int) - Degree for polynomial kernel (default is 3).
            gamma: (str or float) - Kernel coefficient ("scale", "auto", or float) (default is "scale").
            coef0: (float) - Independent term in kernel function (default is 0.0).
        """
        super().__init__(C, tol, max_iter, learning_rate, kernel, degree, gamma, coef0)

    def _fit(self, X, y=None):
        """Fit the OneClassSVM model using gradient descent for anomaly detection.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Training vectors.
            y: (array-like of shape (n_samples,)) - Target values (ignored).

        Returns:
            self: (OneClassSVM) - The fitted instance.

        Algorithm:
            - Initialize weights w and bias b.
            - Use gradient descent to minimize the One-Class SVM objective:
              (1/2) ||w|^2 + b + C * sum(max(0, -(w^T x_i + b))).
            - Update w and b based on subgradients.
            - Stop when gradients are below tolerance or max iterations reached.
        """
        n_samples, n_features = X.shape

        # Compute kernel matrix
        K = self._compute_kernel(X, X)

        # Initialize alpha, sum(alpha) = 1
        alpha = np.ones(n_samples) / n_samples

        # Gradient descent on dual objective: minimize 0.5 * sum(alpha_i alpha_j K(x_i, x_j))
        for _ in range(self.max_iter):
            grad = np.dot(K, alpha)
            alpha -= self.learning_rate * grad
            alpha = np.clip(alpha, 0, self.C)
            alpha /= (
                np.sum(alpha) if np.sum(alpha) > 0 else 1.0
            )  # Project to sum(alpha) = 1

        # Identify support vectors
        sv_idx = alpha > 1e-5
        self.support_vectors_ = X[sv_idx]
        self.support_vector_alphas_ = alpha[sv_idx]

        # Compute rho (bias)
        sv_margin_idx = (alpha > 1e-5) & (alpha < self.C - 1e-5)
        if np.any(sv_margin_idx):
            rho_list = []
            for i in np.where(sv_margin_idx)[0]:
                rho_i = np.sum(self.support_vector_alphas_ * K[i, sv_idx])
                rho_list.append(rho_i)
            self.b = -np.mean(rho_list)  # Decision function: K(x, sv) - rho
        else:
            self.b = 0.0

        return self

    def decision_function(self, X):
        """Compute the decision function values for the input samples."""
        K = self._compute_kernel(X, self.support_vectors_)
        return np.dot(K, self.support_vector_alphas_) + self.b

    def predict(self, X):
        """Predict whether the input samples are inliers (1) or outliers (-1)."""
        return np.where(
            self.decision_function(X) >= 0, 1, -1
        )  # 1 for inliers, -1 for outliers

    def score(self, X, y):
        """Compute the mean accuracy of predictions.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Test samples.
            y: (array-like of shape (n_samples,)) - True labels (+1 for inliers, -1 for outliers).

        Returns:
            score: (float) - Mean accuracy of predictions.
        """
        y_pred = self.predict(X)
        return np.mean(y_pred == y)

    def __sklearn_is_fitted__(self):
        """Check if the model has been fitted. For compatibility with sklearn.

        Returns:
            fitted: (bool) - True if the model has been fitted, otherwise False.
        """
        return hasattr(self, "w") and self.w is not None
