import numpy as np


class BaseSVM:
    """BaseSVM: A base class for Support Vector Machines (SVM) with kernel support.

    This class provides the foundation for implementing SVM models with various kernels
    and supports both classification and regression tasks.

    Attributes:
        C (float): Regularization parameter. Default is 1.0.
        tol (float): Tolerance for stopping criteria. Default is 1e-4.
        max_iter (int): Maximum number of iterations for optimization. Default is 1000.
        learning_rate (float): Step size for optimization. Default is 0.01.
        kernel (str): Kernel type ('linear', 'poly', 'rbf', or 'sigmoid'). Default is 'linear'.
        degree (int): Degree for polynomial kernel. Default is 3.
        gamma (str or float): Kernel coefficient ('scale', 'auto', or float). Default is 'scale'.
        coef0 (float): Independent term in poly and sigmoid kernels. Default is 0.0.
        regression (bool): Whether to use regression (SVR) or classification (SVC). Default is False.
        w (ndarray): Weight vector for linear kernel.
        b (float): Bias term.
        support_vectors_ (ndarray): Support vectors identified during training.
        support_vector_labels_ (ndarray): Labels of the support vectors.
        support_vector_alphas_ (ndarray): Lagrange multipliers for the support vectors.

    Methods:
        __init__(self, C=1.0, tol=1e-4, max_iter=1000, learning_rate=0.01, kernel='linear', degree=3, gamma='scale', coef0=0.0, regression=False):
            Initializes the BaseSVM instance with specified hyperparameters.
        fit(self, X, y=None):
            Fits the SVM model to the training data.
        _fit(self, X, y):
            Abstract method to be implemented by subclasses for training.
        _compute_kernel(self, X1, X2):
            Computes the kernel function between two input matrices.
        decision_function(self, X):
            Computes the decision function for input samples.
        predict(self, X):
            Predicts class labels for input samples.
        score(self, X, y):
            Computes the mean accuracy of the model on the given test data.
        get_params(self, deep=True):
            Retrieves the hyperparameters of the model.
        set_params(self, **parameters):
            Sets the hyperparameters of the model.
        __sklearn_is_fitted__(self):
            Checks if the model has been fitted (for sklearn compatibility).
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
        regression=False,
    ):
        """Initializes the BaseSVM instance with specified hyperparameters.

        Args:
            C: (float) - Regularization parameter. Default is 1.0.
            tol: (float) - Tolerance for stopping criteria. Default is 1e-4.
            max_iter: (int) - Maximum number of iterations for optimization. Default is 1000.
            learning_rate: (float) - Step size for optimization. Default is 0.01.
            kernel: (str) - Kernel type ('linear', 'poly', 'rbf', or 'sigmoid'). Default is 'linear'.
            degree: (int) - Degree for polynomial kernel. Default is 3.
            gamma: (str or float) - Kernel coefficient ('scale', 'auto', or float). Default is 'scale'.
            coef0: (float) - Independent term in poly and sigmoid kernels. Default is 0.0.
            regression: (bool) - Whether to use regression (SVR) or classification (SVC). Default is False.
        """
        self.C = C
        self.tol = tol
        self.max_iter = max_iter
        self.learning_rate = learning_rate
        self.kernel = kernel
        self.degree = degree
        self.gamma = gamma
        self.coef0 = coef0
        self.regression = regression
        self.w = None  # Weight vector for linear kernel
        self.b = None  # Bias term
        self.support_vectors_ = None
        self.support_vector_labels_ = None
        self.support_vector_alphas_ = None

    def fit(self, X, y=None):
        """Fits the SVM model to the training data.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Training vectors.
            y: (array-like of shape (n_samples,)) - Target values. Default is None.

        Returns:
            self: (BaseSVM) - The fitted instance.
        """
        X = np.asarray(X, dtype=np.float64)
        if y is not None:
            y = np.asarray(y)
            if X.shape[0] != y.shape[0]:
                raise ValueError(
                    f"X and y have incompatible shapes: X has {X.shape[0]} samples, "
                    f"but y has {y.shape[0]} elements"
                )
        if X.ndim != 2:
            raise ValueError(f"Expected 2D array, got {X.ndim}D array instead")

        # Handle gamma parameter
        if self.gamma == "scale":
            self.gamma = 1 / (X.shape[1] * X.var()) if X.var() != 0 else 1.0
        elif self.gamma == "auto":
            self.gamma = 1 / X.shape[1]
        elif not isinstance(self.gamma, (int, float)):
            raise ValueError("gamma must be 'scale', 'auto', or a numeric value")

        # Handle multi-class classification using one-vs-rest strategy
        self.classes_ = np.unique(y)
        if len(self.classes_) > 2 and not self.regression:
            self.models_ = []
            for cls in self.classes_:
                y_binary = np.where(y == cls, 1, -1)
                model = self.__class__(
                    C=self.C,
                    tol=self.tol,
                    max_iter=self.max_iter,
                    learning_rate=self.learning_rate,
                )
                model._fit(X, y_binary)
                self.models_.append(model)
        else:
            self._fit(X, y)
        return self

    def _fit(self, X, y):
        """Abstract method to be implemented by subclasses for training.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Training vectors.
            y: (array-like of shape (n_samples,)) - Target values.

        Raises:
            NotImplementedError: If the method is not overridden by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this!")

    def _compute_kernel(self, X1, X2):
        """Computes the kernel function between two input matrices.

        Args:
            X1: (array-like of shape (n_samples1, n_features)) - First input matrix.
            X2: (array-like of shape (n_samples2, n_features)) - Second input matrix.

        Returns:
            kernel_matrix: (ndarray of shape (n_samples1, n_samples2)) - Computed kernel matrix.
        """
        if self.kernel == "linear":
            return np.dot(X1, X2.T)
        elif self.kernel == "poly":
            return (self.gamma * np.dot(X1, X2.T) + self.coef0) ** self.degree
        elif self.kernel == "rbf":
            # Compute squared Euclidean distances
            dist = (
                np.sum(X1**2, axis=1)[:, np.newaxis]
                + np.sum(X2**2, axis=1)
                - 2 * np.dot(X1, X2.T)
            )
            dist = np.clip(dist, 0, 1e6)  # Clip to avoid overflow
            return np.exp(-self.gamma * dist)
        elif self.kernel == "sigmoid":
            return np.tanh(self.gamma * np.dot(X1, X2.T) + self.coef0)
        else:
            raise ValueError(f"Unsupported kernel type: {self.kernel}")

    def decision_function(self, X):
        """Computes the decision function for input samples.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Input samples.

        Returns:
            decision_values: (ndarray of shape (n_samples,)) - Decision function values.
        """
        if self.kernel == "linear" and self.w is not None:
            return np.dot(X, self.w) + self.b
        else:
            K = self._compute_kernel(X, self.support_vectors_)
            return (
                np.dot(K, self.support_vector_alphas_ * self.support_vector_labels_)
                + self.b
            )

    def predict(self, X):
        """Predicts class labels for input samples.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Input samples.

        Returns:
            predicted_labels: (ndarray of shape (n_samples,)) - Predicted class labels.
        """
        if len(self.classes_) > 2:
            return self._predict_multiclass(X)
        else:
            return self._predict_binary(X)

    def score(self, X, y):
        """Computes the mean accuracy of the model on the given test data.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Test samples.
            y: (array-like of shape (n_samples,)) - True class labels.

        Returns:
            score: (float) - Mean accuracy of predictions.
        """
        if len(self.classes_) > 2:
            return self._score_multiclass(X, y)
        else:
            return self._score_binary(X, y)

    def get_params(self, deep=True):
        """Retrieves the hyperparameters of the model.

        Args:
            deep: (bool) - If True, returns parameters of subobjects as well. Default is True.

        Returns:
            params: (dict) - Dictionary of hyperparameter names and values.
        """
        return {
            "C": self.C,
            "tol": self.tol,
            "max_iter": self.max_iter,
            "learning_rate": self.learning_rate,
        }

    def set_params(self, **parameters):
        """Sets the hyperparameters of the model.

        Args:
            **parameters: (dict) - Hyperparameter names and values.

        Returns:
            self: (BaseSVM) - The updated estimator instance.
        """
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

    def __sklearn_is_fitted__(self):
        """Checks if the model has been fitted (for sklearn compatibility).

        Returns:
            fitted: (bool) - True if the model has been fitted, otherwise False.
        """
        return hasattr(self, "w") and self.w is not None
