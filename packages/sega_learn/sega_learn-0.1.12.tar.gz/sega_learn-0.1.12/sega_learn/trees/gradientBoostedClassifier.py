# sega_learn/trees/gradientBoostedClassifier.py

import numpy as np
from scipy.special import expit as sigmoid  # Sigmoid function
from scipy.special import softmax

from sega_learn.trees.treeRegressor import (
    RegressorTree,  # Use RegressorTree to fit gradients
)
from sega_learn.utils.metrics import Metrics


class GradientBoostedClassifier:
    """A Gradient Boosted Decision Tree Classifier.

    This model builds an ensemble of regression trees sequentially. Each tree
    is trained to predict the pseudo-residuals (gradients of the loss function)
    of the previous model's predictions.

    Attributes:
        X (np.ndarray): Training input features of shape (n_samples, n_features).
        y (np.ndarray): Training target class labels of shape (n_samples,).
        n_estimators (int): The number of boosting stages (trees) to perform.
        learning_rate (float): Step size shrinkage to prevent overfitting.
        max_depth (int): Maximum depth of the individual regression tree estimators.
        min_samples_split (int): Minimum number of samples required to split an internal node in a tree.
        random_seed (int or None): Controls the randomness for reproducibility (currently affects feature selection within trees if applicable).
        trees_ (list): List storing the fitted regression tree instances for each boosting stage (and for each class in multiclass).
        classes_ (np.ndarray): The unique class labels found in the target variable `y`.
        n_classes_ (int): The number of unique classes.
        init_estimator_ (float or np.ndarray): The initial prediction model (predicts log-odds).
        loss_ (str): The loss function used ('log_loss' for binary, 'multinomial' for multi-class).
    """

    def __init__(
        self,
        X=None,
        y=None,
        n_estimators: int = 100,
        learning_rate: float = 0.1,
        max_depth: int = 3,
        min_samples_split: int = 2,
        random_seed: int = None,
    ):
        """Initializes the Gradient Boosted Classifier.

        Args:
            X (array-like): Training input features of shape (n_samples, n_features).
            y (array-like): Training target class labels of shape (n_samples,).
            n_estimators (int): Number of boosting stages (trees).
            learning_rate (float): Step size shrinkage to prevent overfitting.
            max_depth (int): Maximum depth of each individual regression tree estimator.
            min_samples_split (int): Minimum samples required to split a node in a tree.
            random_seed (int, optional): Seed for reproducibility. Defaults to None.
        """
        if n_estimators <= 0:
            raise ValueError("n_estimators must be positive.")
        if learning_rate <= 0.0:
            raise ValueError("learning_rate must be positive.")
        if max_depth <= 0:
            raise ValueError("max_depth must be positive.")
        if min_samples_split < 2:
            raise ValueError("min_samples_split must be at least 2.")

        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_seed  # Note: Currently not used for boosting process itself, but passed to trees if they use it.

        self.trees_ = []  # Stores lists of trees (one list per class for multiclass)
        self.classes_ = None
        self.n_classes_ = None
        self.init_estimator_ = None  # Initial prediction (log-odds)
        self.loss_ = None  # Determined during fit
        self._X_fit_shape = None

        if X is not None:
            self.X = np.asarray(X)
        if y is not None:
            self.y = np.asarray(y).astype(float)  # Ensure y is float for residuals

    def get_params(self):
        """Get the parameters of the GradientBoostedClassifier."""
        return {
            "n_estimators": self.n_estimators,
            "learning_rate": self.learning_rate,
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "random_seed": self.random_state,
        }

    def _validate_input(self, X, y):
        """Validates input data X and y."""
        if not isinstance(X, np.ndarray):
            X = np.asarray(X)
        if not isinstance(y, np.ndarray):
            y = np.asarray(y)

        if X.ndim != 2:
            raise ValueError("X must be a 2D array.")
        if y.ndim != 1:
            raise ValueError("y must be a 1D array.")
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have the same number of samples.")
        if X.shape[0] == 0:
            raise ValueError("X and y must not be empty.")

        return X, y

    def _init_predict(self, y):
        """Calculate the initial prediction (log-odds)."""
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)

        if self.n_classes_ == 2:
            self.loss_ = "log_loss"  # Binary classification
            # Convert y to 0/1 if necessary
            y_binary = np.where(y == self.classes_[1], 1, 0)
            prob = np.mean(y_binary)
            # Avoid log(0) or log(1)
            prob = np.clip(prob, 1e-15, 1 - 1e-15)
            # Initial prediction is log-odds
            initial_log_odds = np.log(prob / (1 - prob))
            self.init_estimator_ = initial_log_odds
        else:
            self.loss_ = "multinomial"  # Multi-class classification
            # One-hot encode y
            y_ohe = np.eye(self.n_classes_)[np.searchsorted(self.classes_, y)]
            class_counts = y_ohe.sum(axis=0)
            # Calculate prior probabilities, clip for numerical stability
            priors = np.clip(class_counts / len(y), 1e-15, 1 - 1e-15)
            # Initial predictions are prior log-odds for each class
            # Note: Direct log(priors) is often used, assuming equal priors implicitly or handling differently.
            # Let's use a simpler approach of initializing log-odds to 0 for multi-class for now,
            # or optionally use log(priors). Sklearn's default init predicts class priors.
            # Using log(priors) is more aligned with the theory.
            self.init_estimator_ = np.log(priors)
            # Center log-odds so they sum approximately to 0? Not strictly necessary due to softmax.

    def fit(self, X=None, y=None, sample_weight=None, verbose=0):
        """Fits the gradient boosted classifier to the training data.

        Args:
            X (array-like): Training input features of shape (n_samples, n_features).
            y (array-like): Training target class labels of shape (n_samples,).
            sample_weight (array-like, optional): Sample weights for the training data.
            verbose (int): Controls the verbosity of the fitting process.
                           0 for no output, 1 for basic output.

        Returns:
            self: The fitted GradientBoostedClassifier instance.
        """
        if X is None and self.X is None:
            raise ValueError(
                "X must be provided either during initialization or fitting."
            )
        if y is None and self.y is None:
            raise ValueError(
                "y must be provided either during initialization or fitting."
            )

        X = np.asarray(self.X if X is None else X)
        y = np.asarray(self.y if y is None else y)

        X, y = self._validate_input(X, y)
        self._X_fit_shape = X.shape
        n_samples = X.shape[0]

        # Sample weight handling
        if sample_weight is None:
            sample_weight = np.ones(len(y), dtype=np.float64)
        else:
            sample_weight = np.asarray(sample_weight, dtype=np.float64)
            if sample_weight.shape[0] != len(y):
                raise ValueError("sample_weight length mismatch.")

        self._init_predict(y)  # Determine classes, n_classes, loss, init_estimator_

        # Initialize predictions (raw scores/log-odds)
        if self.loss_ == "log_loss":
            current_raw_predictions = np.full(
                n_samples, self.init_estimator_, dtype=float
            )
            self.trees_ = []  # Single list for binary
            y_binary = np.where(y == self.classes_[1], 1, 0)  # Ensure 0/1 coding

        elif self.loss_ == "multinomial":
            current_raw_predictions = np.full(
                (n_samples, self.n_classes_), self.init_estimator_, dtype=float
            )
            self.trees_ = [
                [] for _ in range(self.n_classes_)
            ]  # List of lists for multi-class
            y_ohe = np.eye(self.n_classes_)[
                np.searchsorted(self.classes_, y)
            ]  # One-hot encode

        else:
            raise ValueError(f"Unsupported loss type derived: {self.loss_}")

        for i in range(self.n_estimators):
            if verbose > 0:
                print(f"Fitting tree {i + 1}/{self.n_estimators}...")

            if self.loss_ == "log_loss":
                # Calculate probabilities
                current_proba = sigmoid(current_raw_predictions)
                # Calculate pseudo-residuals (gradients) for binary log loss: y - p
                residuals = y_binary - current_proba

                # Fit a regression tree to the residuals
                tree = RegressorTree(
                    max_depth=self.max_depth, min_samples_split=self.min_samples_split
                )
                tree.fit(X, residuals, sample_weight=sample_weight)

                # Get leaf values (updates for log-odds)
                update = tree.predict(X)

                # Update raw predictions (log-odds)
                current_raw_predictions += self.learning_rate * update
                self.trees_.append(tree)

            elif self.loss_ == "multinomial":
                # Calculate current probabilities using softmax
                current_proba = softmax(current_raw_predictions, axis=1)

                # Fit one tree per class
                for k in range(self.n_classes_):
                    # Calculate pseudo-residuals (gradients) for class k: y_k - p_k
                    residuals_k = y_ohe[:, k] - current_proba[:, k]

                    # Fit a regression tree to the residuals for class k
                    tree_k = RegressorTree(
                        max_depth=self.max_depth,
                        min_samples_split=self.min_samples_split,
                    )
                    tree_k.fit(X, residuals_k)

                    # Get leaf values (updates for log-odds) for class k
                    update_k = tree_k.predict(X)

                    # Update raw predictions (log-odds) for class k
                    current_raw_predictions[:, k] += self.learning_rate * update_k
                    self.trees_[k].append(tree_k)

        return self

    def decision_function(self, X):
        """Compute the raw decision scores (log-odds) for samples in X.

        Args:
            X (array-like): Input features of shape (n_samples, n_features).

        Returns:
            np.ndarray: The raw decision scores. Shape (n_samples,) for binary
                        or (n_samples, n_classes) for multi-class.
        """
        X = np.asarray(X)
        if self._X_fit_shape is None:
            raise RuntimeError("The model has not been fitted yet.")
        if X.ndim != 2:
            raise ValueError("Input X must be a 2D array.")
        if X.shape[1] != self._X_fit_shape[1]:
            raise ValueError(
                f"Input data must have {self._X_fit_shape[1]} features, got {X.shape[1]}."
            )

        n_samples = X.shape[0]

        if self.loss_ == "log_loss":
            # Start with initial log-odds
            raw_predictions = np.full(n_samples, self.init_estimator_, dtype=float)
            # Add predictions from each tree, scaled by learning rate
            for tree in self.trees_:
                raw_predictions += self.learning_rate * tree.predict(X)
            return raw_predictions  # Return log-odds for binary

        elif self.loss_ == "multinomial":
            # Start with initial log-odds (shape n_samples, n_classes)
            raw_predictions = np.full(
                (n_samples, self.n_classes_), self.init_estimator_, dtype=float
            )
            # Add predictions from each tree for each class
            for k in range(self.n_classes_):
                for tree in self.trees_[k]:
                    raw_predictions[:, k] += self.learning_rate * tree.predict(X)
            return raw_predictions  # Return log-odds matrix for multi-class

        else:
            raise RuntimeError("Model loss function not properly set.")

    def predict_proba(self, X):
        """Predict class probabilities for samples in X.

        Args:
            X (array-like): Input features of shape (n_samples, n_features).

        Returns:
            np.ndarray: Predicted class probabilities. Shape (n_samples, n_classes).
                        For binary, columns are [P(class 0), P(class 1)].
        """
        raw_predictions = self.decision_function(X)

        if self.loss_ == "log_loss":
            # Convert log-odds to probabilities using sigmoid
            proba_class1 = sigmoid(raw_predictions)
            proba_class0 = 1.0 - proba_class1
            return np.vstack((proba_class0, proba_class1)).T  # Shape (n_samples, 2)
        elif self.loss_ == "multinomial":
            # Convert log-odds to probabilities using softmax
            return softmax(raw_predictions, axis=1)
        else:
            raise RuntimeError("Model loss function not properly set.")

    def predict(self, X):
        """Predicts class labels for input features X.

        Args:
            X (array-like): Input features of shape (n_samples, n_features).

        Returns:
            np.ndarray: Predicted class labels of shape (n_samples,).
        """
        proba = self.predict_proba(X)
        # Get the index of the class with the highest probability
        indices = np.argmax(proba, axis=1)
        # Map index back to original class label
        return self.classes_[indices]

    def calculate_metrics(self, y_true, y_pred, y_prob=None):
        """Calculate common classification metrics.

        Args:
            y_true (array-like): True class labels.
            y_pred (array-like): Predicted class labels.
            y_prob (array-like, optional): Predicted probabilities for Log Loss calculation.

        Returns:
            dict: A dictionary containing calculated metrics (Accuracy, Precision, Recall, F1 Score, Log Loss if applicable).
        """
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)

        if y_true.shape != y_pred.shape:
            raise ValueError("y_true and y_pred must have the same shape.")
        if len(y_true) == 0:
            return {
                "Accuracy": np.nan,
                "Precision": np.nan,
                "Recall": np.nan,
                "F1 Score": np.nan,
                "Log Loss": np.nan,
            }

        metrics = {
            "Accuracy": Metrics.accuracy(y_true, y_pred),
            "Precision": Metrics.precision(
                y_true, y_pred
            ),  # Uses default positive label (1)
            "Recall": Metrics.recall(y_true, y_pred),  # Uses default positive label (1)
            "F1 Score": Metrics.f1_score(
                y_true, y_pred
            ),  # Uses default positive label (1)
        }

        # Calculate Log Loss if probabilities are provided
        if y_prob is not None:
            try:
                metrics["Log Loss"] = Metrics.log_loss(y_true, y_prob)
            except Exception:
                # print(f"Warning: Could not calculate Log Loss: {e}")
                metrics["Log Loss"] = np.nan  # Or handle as appropriate
        else:
            metrics["Log Loss"] = np.nan  # Not applicable if no probabilities

        return metrics

    def get_stats(self, y_true, X=None, y_pred=None, verbose=False):
        """Calculate and optionally print evaluation metrics. Requires either X or y_pred.

        Args:
            y_true (array-like): True target values.
            X (array-like, optional): Input features to generate predictions if y_pred is not provided.
            y_pred (array-like, optional): Pre-computed predicted class labels.
            verbose (bool): Whether to print the metrics.

        Returns:
            dict: A dictionary containing calculated metrics.
        """
        if y_pred is None and X is None:
            raise ValueError("Either X or y_pred must be provided to calculate stats.")
        if y_pred is None:
            y_pred = self.predict(X)
            y_prob = self.predict_proba(
                X
            )  # Calculate probabilities needed for log loss
        else:
            # If only y_pred is given, we cannot calculate log loss reliably without probabilities
            y_prob = None

        stats = self.calculate_metrics(y_true, y_pred, y_prob)
        if verbose:
            print("Evaluation Metrics:")
            for metric, value in stats.items():
                print(
                    f"  {metric}: {value:.4f}"
                    if isinstance(value, (float, int)) and np.isfinite(value)
                    else f"  {metric}: {value}"
                )
        return stats
