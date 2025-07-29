import numpy as np

from .baseSVM import BaseSVM


class GeneralizedSVR(BaseSVM):
    """GeneralizedSVR: A Support Vector Regression (SVR) model with support for multiple kernels.

    This class implements an SVR model using gradient descent for optimization. It supports
    linear and non-linear kernels, including polynomial and RBF kernels.

    Attributes:
        C (float): Regularization parameter. Default is 1.0.
        tol (float): Tolerance for stopping criteria. Default is 1e-4.
        max_iter (int): Maximum number of iterations for gradient descent. Default is 1000.
        learning_rate (float): Learning rate for gradient descent. Default is 0.01.
        epsilon (float): Epsilon parameter for epsilon-insensitive loss. Default is 0.1.
        kernel (str): Kernel type ('linear', 'poly', 'rbf'). Default is 'linear'.
        degree (int): Degree of the polynomial kernel function ('poly'). Ignored by other kernels. Default is 3.
        gamma (str or float): Kernel coefficient for 'rbf' and 'poly'. Default is 'scale'.
        coef0 (float): Independent term in kernel function ('poly'). Default is 0.0.

    Methods:
        __init__(self, C=1.0, tol=1e-4, max_iter=1000, learning_rate=0.01, epsilon=0.1, kernel="linear", degree=3, gamma="scale", coef0=0.0):
            Initialize the GeneralizedSVR model with specified hyperparameters.
        _fit(self, X, y):
            Fit the GeneralizedSVR model to the training data using gradient descent.
        predict(self, X):
            Predict continuous target values for input samples.
        decision_function(self, X):
            Compute raw decision function values for input samples.
        score(self, X, y):
            Compute the coefficient of determination (R² score) for the model's predictions.

    Raises:
        ValueError: If numerical instability is detected during training.
    """

    def __init__(
        self,
        C=1.0,
        tol=1e-4,
        max_iter=1000,
        learning_rate=0.01,
        epsilon=0.1,
        kernel="linear",
        degree=3,
        gamma="scale",
        coef0=0.0,
    ):
        """Initializes the GeneralizedSVR model with specified hyperparameters.

        Args:
            C: (float) - Regularization parameter. Default is 1.0.
            tol: (float) - Tolerance for stopping criteria. Default is 1e-4.
            max_iter: (int) - Maximum number of iterations for gradient descent. Default is 1000.
            learning_rate: (float) - Learning rate for gradient descent. Default is 0.01.
            epsilon: (float) - Epsilon parameter for epsilon-insensitive loss. Default is 0.1.
            kernel: (str) - Kernel type ('linear', 'poly', 'rbf'). Default is 'linear'.
            degree: (int) - Degree of the polynomial kernel function ('poly'). Ignored by other kernels. Default is 3.
            gamma: (str or float) - Kernel coefficient for 'rbf' and 'poly'. Default is 'scale'.
            coef0: (float) - Independent term in kernel function ('poly'). Default is 0.0.
        """
        super().__init__(
            C,
            tol,
            max_iter,
            learning_rate,
            kernel,
            degree,
            gamma,
            coef0,
            regression=True,
        )
        self.epsilon = epsilon

    def _fit(self, X, y):
        """Fit the GeneralizedSVR model to the training data using gradient descent."""
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features) if self.kernel == "linear" else None
        self.b = 0.0

        # Store for prediction - these become the support vectors
        self.X_train = X
        self.support_vectors_ = X
        self.support_vector_labels_ = y

        # Initialize alphas for all kernels
        self.support_vector_alphas_ = np.zeros(n_samples)

        for _ in range(self.max_iter):
            # Compute predictions
            if self.kernel == "linear":
                prediction = np.dot(X, self.w) + self.b
            else:
                K = self._compute_kernel(X, self.support_vectors_)
                prediction = np.dot(K, self.support_vector_alphas_) + self.b

            # Compute epsilon-insensitive loss and gradients
            errors = y - prediction
            _abs_errors = np.abs(errors)

            if self.kernel == "linear":
                dw = self.C * self.w
                db = 0.0

                pos_idx = errors > self.epsilon
                neg_idx = errors < -self.epsilon

                if np.any(pos_idx):
                    dw -= np.dot(X[pos_idx].T, np.ones(np.sum(pos_idx))) / n_samples
                    db -= np.sum(np.ones(np.sum(pos_idx))) / n_samples
                if np.any(neg_idx):
                    dw += np.dot(X[neg_idx].T, np.ones(np.sum(neg_idx))) / n_samples
                    db += np.sum(np.ones(np.sum(neg_idx))) / n_samples

                # Update weights and bias
                self.w -= self.learning_rate * dw
                self.b -= self.learning_rate * db
            else:
                # Gradient update for non-linear kernels
                pos_idx = errors > self.epsilon
                neg_idx = errors < -self.epsilon

                # Create alpha gradient vector
                dalpha = np.zeros(n_samples)

                # For points outside the epsilon tube, update alphas
                if np.any(pos_idx):
                    dalpha[pos_idx] = 1.0
                if np.any(neg_idx):
                    dalpha[neg_idx] = -1.0

                # Apply regularization to alphas
                dalpha = dalpha - self.C * self.support_vector_alphas_

                # Update alphas
                self.support_vector_alphas_ += self.learning_rate * dalpha / n_samples

                # Update bias term
                db = (
                    -np.mean(errors[(pos_idx | neg_idx)])
                    if np.any(pos_idx | neg_idx)
                    else 0
                )
                self.b -= self.learning_rate * db

            # Check for convergence
            if (
                self.kernel == "linear"
                and np.linalg.norm(dw) < self.tol
                and abs(db) < self.tol
                or self.kernel != "linear"
                and np.max(np.abs(dalpha)) < self.tol
                and abs(db) < self.tol
            ):
                break

            # Check for numerical stability
            if np.any(np.isnan(self.support_vector_alphas_)) or np.isnan(self.b):
                raise ValueError(
                    "Numerical instability detected during training. Consider normalizing the data or reducing the learning rate."
                )

        # Prune support vectors with near-zero alphas
        if self.kernel != "linear":
            mask = np.abs(self.support_vector_alphas_) > 1e-5
            if np.any(mask):
                self.support_vectors_ = self.support_vectors_[mask]
                self.support_vector_labels_ = self.support_vector_labels_[mask]
                self.support_vector_alphas_ = self.support_vector_alphas_[mask]

        return self

    def predict(self, X):
        """Predict continuous target values for input samples."""
        return self.decision_function(X)

    def decision_function(self, X):
        """Compute raw decision function values for input samples."""
        if self.kernel == "linear":
            return np.dot(X, self.w) + self.b
        else:
            K = self._compute_kernel(X, self.support_vectors_)
            return np.dot(K, self.support_vector_alphas_) + self.b

    def score(self, X, y):
        """Compute the coefficient of determination (R² score) for the model's predictions."""
        y_pred = self.predict(X)
        u = ((y - y_pred) ** 2).sum()
        v = ((y - y.mean()) ** 2).sum()
        return 1 - u / v if v > 0 else 0


class GeneralizedSVC(BaseSVM):
    """GeneralizedSVC: A Support Vector Classifier (SVC) model with support for multiple kernels.

    This class implements an SVC model using gradient descent for optimization. It supports
    linear and non-linear kernels, including polynomial and RBF kernels.

    Attributes:
        C (float): Regularization parameter. Default is 1.0.
        tol (float): Tolerance for stopping criteria. Default is 1e-4.
        max_iter (int): Maximum number of iterations for gradient descent. Default is 1000.
        learning_rate (float): Learning rate for gradient descent. Default is 0.01.
        kernel (str): Kernel type ('linear', 'poly', 'rbf'). Default is 'linear'.
        degree (int): Degree of the polynomial kernel function ('poly'). Ignored by other kernels. Default is 3.
        gamma (str or float): Kernel coefficient for 'rbf' and 'poly'. Default is 'scale'.
        coef0 (float): Independent term in kernel function ('poly'). Default is 0.0.

    Methods:
        __init__(self, C=1.0, tol=1e-4, max_iter=1000, learning_rate=0.01, kernel="linear", degree=3, gamma="scale", coef0=0.0):
            Initialize the GeneralizedSVC model with specified hyperparameters.
        _fit(self, X, y):
            Fit the GeneralizedSVC model to the training data using gradient descent.
        _predict_binary(self, X):
            Predict binary class labels for input samples.
        _predict_multiclass(self, X):
            Predict multi-class labels using one-vs-rest strategy.
        decision_function(self, X):
            Compute raw decision function values for input samples.
        _score_binary(self, X, y):
            Compute the accuracy score for binary classification.
        _score_multiclass(self, X, y):
            Compute the accuracy score for multi-class classification.

    Raises:
        ValueError: If numerical instability is detected during training.
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
        """Initializes the GeneralizedSVC model with specified hyperparameters.

        Args:
            C: (float) - Regularization parameter. Default is 1.0.
            tol: (float) - Tolerance for stopping criteria. Default is 1e-4.
            max_iter: (int) - Maximum number of iterations for gradient descent. Default is 1000.
            learning_rate: (float) - Learning rate for gradient descent. Default is 0.01.
            kernel: (str) - Kernel type ('linear', 'poly', 'rbf'). Default is 'linear'.
            degree: (int) - Degree of the polynomial kernel function ('poly'). Ignored by other kernels. Default is 3.
            gamma: (str or float) - Kernel coefficient for 'rbf' and 'poly'. Default is 'scale'.
            coef0: (float) - Independent term in kernel function ('poly'). Default is 0.0.
        """
        super().__init__(
            C,
            tol,
            max_iter,
            learning_rate,
            kernel,
            degree,
            gamma,
            coef0,
            regression=False,
        )

    def _fit(self, X, y):
        """Fit the GeneralizedSVC model to the training data using gradient descent."""
        n_samples, n_features = X.shape
        # For binary classification, convert labels to {-1, 1}
        y_binary = np.where(y > 0, 1, -1)

        self.w = np.zeros(n_features) if self.kernel == "linear" else None
        self.b = 0.0

        # Store data for kernel methods
        self.support_vectors_ = X
        self.support_vector_labels_ = y_binary
        self.support_vector_alphas_ = np.zeros(n_samples)

        for _ in range(self.max_iter):
            # Compute predictions
            if self.kernel == "linear":
                prediction = np.dot(X, self.w) + self.b
            else:
                K = self._compute_kernel(X, self.support_vectors_)
                prediction = (
                    np.dot(K, self.support_vector_alphas_ * self.support_vector_labels_)
                    + self.b
                )

            # Compute hinge loss margins
            margins = y_binary * prediction
            misclassified = margins < 1

            if self.kernel == "linear":
                # Gradient for linear kernel (primal formulation)
                dw = self.C * self.w
                db = 0.0

                if np.any(misclassified):
                    dw -= (
                        np.dot(X[misclassified].T, y_binary[misclassified]) / n_samples
                    )
                    db -= np.sum(y_binary[misclassified]) / n_samples

                # Update weights and bias
                self.w -= self.learning_rate * dw
                self.b -= self.learning_rate * db
            else:
                # Gradient update for non-linear kernels (dual formulation)
                dalpha = np.zeros(n_samples)

                if np.any(misclassified):
                    dalpha[misclassified] = y_binary[misclassified]

                # Apply regularization to alphas
                dalpha = dalpha - self.C * self.support_vector_alphas_

                # Update alphas - ensure they stay positive (characteristic of SVC)
                self.support_vector_alphas_ += self.learning_rate * dalpha / n_samples
                self.support_vector_alphas_ = np.clip(
                    self.support_vector_alphas_, 0, np.inf
                )

                # Update bias term
                if np.any(misclassified):
                    db = -np.mean(y_binary[misclassified] - prediction[misclassified])
                    self.b -= self.learning_rate * db

            # Check for convergence
            if (
                self.kernel == "linear"
                and np.linalg.norm(dw) < self.tol
                and abs(db) < self.tol
                or self.kernel != "linear"
                and np.max(np.abs(dalpha)) < self.tol
            ):
                break

            # Check for numerical stability
            if np.any(np.isnan(self.support_vector_alphas_)) or np.isnan(self.b):
                raise ValueError(
                    "Numerical instability detected during training. Consider normalizing the data or reducing the learning rate."
                )

        # Prune support vectors with near-zero alphas for non-linear kernels
        if self.kernel != "linear":
            mask = np.abs(self.support_vector_alphas_) > 1e-5
            if np.any(mask):
                self.support_vectors_ = self.support_vectors_[mask]
                self.support_vector_labels_ = self.support_vector_labels_[mask]
                self.support_vector_alphas_ = self.support_vector_alphas_[mask]

        return self

    def _predict_binary(self, X):
        """Predict binary class labels for input samples."""
        decision = self.decision_function(X)
        return np.where(decision >= 0, self.classes_[1], self.classes_[0])

    def _predict_multiclass(self, X):
        """Predict multi-class labels using one-vs-rest strategy."""
        # Get decision values for each binary classifier
        decision_values = np.array(
            [model.decision_function(X) for model in self.models_]
        )
        # Return class with highest decision value
        return self.classes_[np.argmax(decision_values, axis=0)]

    def _score_binary(self, X, y):
        """Compute the accuracy score for binary classification."""
        return np.mean(self.predict(X) == y)

    def _score_multiclass(self, X, y):
        """Compute the accuracy score for multi-class classification."""
        return np.mean(self.predict(X) == y)

    def decision_function(self, X):
        """Compute raw decision function values for input samples."""
        if self.kernel == "linear" and self.w is not None:
            return np.dot(X, self.w) + self.b
        else:
            K = self._compute_kernel(X, self.support_vectors_)
            return (
                np.dot(K, self.support_vector_alphas_ * self.support_vector_labels_)
                + self.b
            )
