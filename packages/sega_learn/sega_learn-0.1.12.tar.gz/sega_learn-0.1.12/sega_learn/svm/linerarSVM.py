import numpy as np

from .baseSVM import BaseSVM


class LinearSVC(BaseSVM):
    """LinearSVC is a linear Support Vector Classifier (SVC) implementation that uses gradient descent for optimization.

    It supports binary and multi-class classification using a one-vs-rest strategy.

    Attributes:
        C (float): Regularization parameter. Default is 1.0.
        tol (float): Tolerance for stopping criteria. Default is 1e-4.
        max_iter (int): Maximum number of iterations for gradient descent. Default is 1000.
        learning_rate (float): Learning rate for gradient descent. Default is 0.01.
        numba (bool): Whether to use Numba-accelerated computations. Default is False.
        w (ndarray): Weight vector for the linear model.
        b (float): Bias term for the linear model.
        numba_available (bool): Indicates if Numba is available for use.

    Methods:
        __init__(self, C=1.0, tol=1e-4, max_iter=1000, learning_rate=0.01, numba=False):
            Initializes the LinearSVC instance with hyperparameters and checks for Numba availability.
        _fit(self, X, y):
            Fits the LinearSVC model to the training data using gradient descent.
        _predict_binary(self, X):
            Predicts class labels {-1, 1} for binary classification.
        _predict_multiclass(self, X):
            Predicts class labels for multi-class classification using one-vs-rest strategy.
        decision_function(self, X):
            Computes raw decision function values before thresholding.
        _score_binary(self, X, y):
            Computes the mean accuracy of predictions for binary classification.
        _score_multiclass(self, X, y):
            Computes the mean accuracy of predictions for multi-class classification.
    """

    def __init__(self, C=1.0, tol=1e-4, max_iter=1000, learning_rate=0.01, numba=False):
        """Initializes the LinearSVC instance with hyperparameters and checks for Numba availability.

        Args:
            C: (float) - Regularization parameter. Default is 1.0.
            tol: (float) - Tolerance for stopping criteria. Default is 1e-4.
            max_iter: (int) - Maximum number of iterations for gradient descent. Default is 1000.
            learning_rate: (float) - Learning rate for gradient descent. Default is 0.01.
            numba: (bool) - Whether to use Numba-accelerated computations. Default is False.
        """
        super().__init__(C, tol, max_iter, learning_rate)

        if numba:
            try:
                from ._LinearSVM_jit_utils import _linearSVC_minibatches

                # Run once to compile
                _linearSVC_minibatches(
                    np.zeros((2, 2)), np.zeros(2), np.zeros(2), 0.0, 1.0, 0.9, 0.01, 2
                )

                self._linearSVC_minibatches = _linearSVC_minibatches
                self.numba_available = True
            except Exception as e:
                print(f"Numba not available: {e}")
                self.numba_available = False
        else:
            self.numba_available = False

    def _fit(self, X, y):
        """Implement the fitting procedure for LinearSVC using gradient descent.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Training vectors.
            y: (array-like of shape (n_samples,)) - Target labels in {-1, 1}.

        Returns:
            self: (LinearSVC) - The fitted instance.

        Algorithm:
            Initialize Parameters: Initialize the weight vector w and bias b.
            Set Hyperparameters: Define the learning rate and the number of iterations.
            Gradient Descent Loop: Iterate over the dataset to update the weights and bias using gradient descent.
            Compute Hinge Loss: Calculate the hinge loss and its gradient.
            Update Parameters: Update the weights and bias using the gradients.
            Stopping Criteria: Check for convergence based on the tolerance level
        """
        if self.kernel != "linear":
            raise ValueError("LinearSVC only supports linear kernel")

        # Initialize parameters
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0
        momentum_w = np.zeros(n_features)
        momentum_b = 0.0
        beta = 0.9  # Momentum factor

        # Convert y to {-1, 1} if not already
        y = np.where(y <= 0, -1, 1)

        # Mini-batch size
        batch_size = min(64, n_samples)

        for _iteration in range(self.max_iter):
            # Shuffle data for mini-batch
            indices = np.random.permutation(n_samples)
            X_shuffled = X[indices]
            y_shuffled = y[indices]

            if self.numba_available:
                self.w, self.b, dw, db = self._linearSVC_minibatches(
                    X_shuffled,
                    y_shuffled,
                    self.w,
                    self.b,
                    self.C,
                    beta,
                    self.learning_rate,
                    batch_size,
                )
            else:
                # Mini-batch gradient descent
                for start in range(0, n_samples, batch_size):
                    end = start + batch_size
                    X_batch = X_shuffled[start:end]
                    y_batch = y_shuffled[start:end]

                    # Compute the margin
                    margin = y_batch * (np.dot(X_batch, self.w) + self.b)

                    # Compute the hinge loss gradient
                    violated_indices = margin < 1
                    dw = self.C * self.w  # L2 regularization gradient
                    db = 0.0

                    if np.any(violated_indices):
                        X_violated = X_batch[violated_indices]
                        y_violated = y_batch[violated_indices]
                        dw -= (
                            np.sum(X_violated * y_violated[:, np.newaxis], axis=0)
                            / batch_size
                        )
                        db -= np.sum(y_violated) / batch_size

                    # Apply momentum
                    momentum_w = beta * momentum_w + (1 - beta) * dw
                    momentum_b = beta * momentum_b + (1 - beta) * db

                    # Update weights and bias
                    self.w -= self.learning_rate * momentum_w
                    self.b -= self.learning_rate * momentum_b

            # NOT USED: using gradient norm for convergence check
            # Calculate current loss for convergence check
            # margin_full = y * (np.dot(X, self.w) + self.b)
            # loss = self.C * 0.5 * np.dot(self.w, self.w) + np.sum(np.maximum(0, 1 - margin_full)) / n_samples
            # print(f"Iteration {iteration + 1}, Loss: {loss}")

            # Check for convergence
            if np.linalg.norm(dw) < self.tol and abs(db) < self.tol:
                break

        return self

    def _predict_binary(self, X):
        """Predict class labels for binary classification.

        Args:
            X (array-like of shape (n_samples, n_features)): Input samples.

        Returns:
            y_pred (array of shape (n_samples,)): Predicted class labels {-1, 1}.
        """
        return np.sign(self.decision_function(X))

    def _predict_multiclass(self, X):
        """Predict class labels for multi-class classification using one-vs-rest strategy.

        Args:
            X (array-like of shape (n_samples, n_features)): Input samples.

        Returns:
            predicted_labels (array of shape (n_samples,)): Predicted class labels.
        """
        decision_values = np.array(
            [model.decision_function(X) for model in self.models_]
        ).T
        return self.classes_[np.argmax(decision_values, axis=1)]

    def decision_function(self, X):
        """Compute raw decision function values before thresholding.

        Args:
            X (array-like of shape (n_samples, n_features)): Input samples.

        Returns:
            scores (array of shape (n_samples,)): Decision function values.
        """
        return super().decision_function(X)

    def _score_binary(self, X, y):
        """Compute the mean accuracy of predictions for binary classification.

        Args:
            X (array-like of shape (n_samples, n_features)): Test samples.
            y (array-like of shape (n_samples,)): True labels.

        Returns:
            score (float): Mean accuracy of predictions.
        """
        y_true = np.where(y <= 0, -1, 1)
        y_pred = self.predict(X)
        return np.mean(y_true == y_pred)

    def _score_multiclass(self, X, y):
        """Compute the mean accuracy of predictions for multi-class classification.

        Args:
            X (array-like of shape (n_samples, n_features)): Test samples.
            y (array-like of shape (n_samples,)): True labels.

        Returns:
            score (float): Mean accuracy of predictions.
        """
        y_pred = self.predict(X)
        return np.mean(y == y_pred)


class LinearSVR(BaseSVM):
    """LinearSVR: A linear Support Vector Regression (SVR) model using epsilon-insensitive loss.

    This class implements a linear SVR model with support for mini-batch gradient descent
    and optional acceleration using Numba. It is designed for regression tasks and uses
    epsilon-insensitive loss to handle errors within a specified margin.

    Attributes:
        C (float): Regularization parameter. Default is 1.0.
        tol (float): Tolerance for stopping criteria. Default is 1e-4.
        max_iter (int): Maximum number of iterations for gradient descent. Default is 1000.
        learning_rate (float): Learning rate for gradient descent. Default is 0.01.
        epsilon (float): Epsilon parameter for epsilon-insensitive loss. Default is 0.1.
        numba (bool): Whether to use Numba for acceleration. Default is False.
        w (ndarray): Weight vector of the model.
        b (float): Bias term of the model.
        numba_available (bool): Indicates if Numba is available for acceleration.
        X_train (ndarray): Training data used for fitting.
        y_train (ndarray): Target values used for fitting.

    Methods:
        __init__(self, C=1.0, tol=1e-4, max_iter=1000, learning_rate=0.01, epsilon=0.1, numba=False):
            Initialize the LinearSVR model with specified hyperparameters.
        _fit(self, X, y):
            Fit the LinearSVR model to the training data using mini-batch gradient descent.
        predict(self, X):
            Predict continuous target values for input samples.
        decision_function(self, X):
            Compute raw decision function values for input samples.
        score(self, X, y):
            Compute the coefficient of determination (R² score) for the model's predictions.

    Raises:
        ValueError: If a non-linear kernel is specified, as LinearSVR only supports linear kernels.
    """

    def __init__(
        self,
        C=1.0,
        tol=1e-4,
        max_iter=1000,
        learning_rate=0.01,
        epsilon=0.1,
        numba=False,
    ):
        """Initializes the LinearSVR instance with hyperparameters and checks for Numba availability.

        Args:
            C: (float) - Regularization parameter. Default is 1.0.
            tol: (float) - Tolerance for stopping criteria. Default is 1e-4.
            max_iter: (int) - Maximum number of iterations for gradient descent. Default is 1000.
            learning_rate: (float) - Learning rate for gradient descent. Default is 0.01.
            epsilon: (float) - Epsilon parameter for epsilon-insensitive loss. Default is 0.1.
            numba: (bool) - Whether to use Numba-accelerated computations. Default is False.

        Returns:
            None
        """
        super().__init__(C, tol, max_iter, learning_rate, regression=True)
        self.epsilon = epsilon

        if numba:
            try:
                from ._LinearSVM_jit_utils import _linearSVR_minibatches

                # Run once to compile
                _linearSVR_minibatches(
                    np.zeros((2, 2)),
                    np.zeros(2),
                    np.zeros(2),
                    0.0,
                    1.0,
                    0.9,
                    0.01,
                    2,
                    0.1,
                )
                self._linearSVC_minibatches = _linearSVR_minibatches
                self.numba_available = True
            except Exception as e:
                print(f"Numba not available: {e}")
                self.numba_available = False
        else:
            self.numba_available = False

    def _fit(self, X, y):
        """Implement the fitting procedure for LinearSVR using the epsilon-insensitive loss.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Training vectors.
            y: (array-like of shape (n_samples,)) - Target values.

        Returns:
            self: (LinearSVR) - The fitted instance.

        Algorithm:
            Initialize Parameters: Initialize the weight vector w and bias b.
            Set Hyperparameters: Define the learning rate and the number of iterations.
            Gradient Descent Loop: Iterate over the dataset to update the weights and bias using gradient descent.
            Compute Epsilon-Insensitive Loss: Calculate the epsilon-insensitive loss and its gradient.
            Update Parameters: Update the weights and bias using the gradients.
            Stopping Criteria: Check for convergence based on the tolerance level
        """
        if self.kernel != "linear":
            raise ValueError("LinearSVR only supports linear kernel")

        # Initialize parameters
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0
        momentum_w = np.zeros(n_features)
        momentum_b = 0.0
        beta = 0.9  # Momentum factor

        # Store for prediction
        self.X_train = X
        self.y_train = y

        # Mini-batch size
        batch_size = min(64, n_samples)

        for _iteration in range(self.max_iter):
            # Shuffle data for mini-batch
            indices = np.random.permutation(n_samples)
            X_shuffled = X[indices]
            y_shuffled = y[indices]

            if self.numba_available:
                self.w, self.b, dw, db = self._linearSVC_minibatches(
                    X_shuffled,
                    y_shuffled,
                    self.w,
                    self.b,
                    self.C,
                    beta,
                    self.learning_rate,
                    batch_size,
                    self.epsilon,
                )
            else:
                # Mini-batch gradient descent
                for start in range(0, n_samples, batch_size):
                    end = start + batch_size
                    X_batch = X_shuffled[start:end]
                    y_batch = y_shuffled[start:end]

                    # Compute the prediction
                    prediction = np.dot(X_batch, self.w) + self.b

                    # Compute the epsilon-insensitive loss and its gradient
                    errors = y_batch - prediction
                    dw = self.C * self.w  # Regularization gradient
                    db = 0.0

                    # Samples outside the epsilon tube (positive errors)
                    pos_idx = errors > self.epsilon
                    if np.any(pos_idx):
                        dw -= np.sum(X_batch[pos_idx], axis=0) / batch_size
                        db -= np.sum(np.ones(np.sum(pos_idx))) / batch_size

                    # Samples outside the epsilon tube (negative errors)
                    neg_idx = errors < -self.epsilon
                    if np.any(neg_idx):
                        dw += np.sum(X_batch[neg_idx], axis=0) / batch_size
                        db += np.sum(np.ones(np.sum(neg_idx))) / batch_size

                    # Apply momentum
                    momentum_w = beta * momentum_w + (1 - beta) * dw
                    momentum_b = beta * momentum_b + (1 - beta) * db

                    # Update weights and bias
                    self.w -= self.learning_rate * momentum_w
                    self.b -= self.learning_rate * momentum_b

            # NOT USED: using gradient norm for convergence check
            # Calculate current loss for convergence check
            # epsilon_loss = np.sum(np.maximum(0, abs_errors - self.epsilon)) / n_samples
            # reg_loss = self.C * 0.5 * np.dot(self.w, self.w)
            # total_loss = epsilon_loss + reg_loss

            # Check for convergence based on gradient norm
            if np.linalg.norm(dw) < self.tol and abs(db) < self.tol:
                break

        return self

    def predict(self, X):
        """Predict continuous target values for input samples.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Input samples.

        Returns:
            y_pred: (array of shape (n_samples,)) - Predicted values.
        """
        return self.decision_function(X)

    def decision_function(self, X):
        """Compute raw decision function values.

        Args:
            X: (array-like of shape (n_samples, n_features)) - Input samples.

        Returns:
            scores: (array of shape (n_samples,)) - Predicted values.
        """
        return super().decision_function(X)

    def score(self, X, y):
        """Compute the coefficient of determination (R² score).

        Args:
            X: (array-like of shape (n_samples, n_features)) - Test samples.
            y: (array-like of shape (n_samples,)) - True target values.

        Returns:
            score: (float) - R² score of predictions.
        """
        y_pred = self.predict(X)
        u = ((y - y_pred) ** 2).sum()
        v = ((y - y.mean()) ** 2).sum()
        return 1 - u / v if v > 0 else 0
