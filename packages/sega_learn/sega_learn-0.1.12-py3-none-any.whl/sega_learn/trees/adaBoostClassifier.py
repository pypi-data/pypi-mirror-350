import inspect
import warnings

import numpy as np
from scipy.special import expit as sigmoid

from sega_learn.trees.treeClassifier import ClassifierTree
from sega_learn.utils.metrics import Metrics


class AdaBoostClassifier:
    """AdaBoost classifier.

    Builds an additive model by sequentially fitting weak classifiers (default: decision stumps)
    on modified versions of the data. Each subsequent classifier focuses more on samples
    that were misclassified by the previous ensemble.

    Uses the SAMME algorithm which supports multi-class classification.

    Attributes:
        base_estimator_ (object): The base estimator template used for fitting.
        n_estimators (int): The maximum number of estimators at which boosting is terminated.
        learning_rate (float): Weight applied to each classifier's contribution.
        estimators_ (list): The collection of fitted base estimators.
        estimator_weights_ (np.ndarray): Weights for each estimator.
        estimator_errors_ (np.ndarray): Classification error for each estimator.
        classes_ (np.ndarray): The class labels.
        n_classes_ (int): The number of classes.
    """

    def __init__(
        self,
        base_estimator=None,
        n_estimators=50,
        learning_rate=1.0,
        random_state=None,
        max_depth=3,
        min_samples_split=2,
    ):
        """Initialize the AdaBoostClassifier.

        Args:
            base_estimator (object, optional): The base estimator from which the boosted ensemble is built.
                                              Support for sample weighting is required. If None, then
                                              the base estimator is DecisionTreeClassifier(max_depth=1).
            n_estimators (int, optional): The maximum number of estimators at which boosting is terminated.
                                          In case of perfect fit, the learning procedure is stopped early. Defaults to 50.
            learning_rate (float, optional): Weight applied to each classifier's contribution. Defaults to 1.0.
            random_state (int, optional): Controls the random seed given to the base estimator at each boosting iteration.
                                          Defaults to None.
            max_depth (int, optional): The maximum depth of the base estimator. Defaults to 3.
            min_samples_split (int, optional): The minimum number of samples required to split an internal node
                                               when using the default `ClassifierTree` base estimator. Defaults to 2.
        """
        if base_estimator is None:
            # Default to a decision stump (depth=3) and pass min_samples_split
            self.base_estimator_ = ClassifierTree(
                max_depth=max_depth, min_samples_split=min_samples_split
            )
        else:
            # Check if the base_estimator supports sample_weight
            if not self._supports_sample_weight(base_estimator):
                raise ValueError(
                    "The provided base_estimator does not support sample_weight. "
                    "Please provide an estimator that supports sample weighting."
                )
            self.base_estimator_ = base_estimator

        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.random_state = random_state  # Currently not used directly in boosting logic but could be for base estimator seeding

        # Store min_samples_split for potential use if recreating default estimator
        self._min_samples_split_default = min_samples_split

        self.estimators_ = []
        self.estimator_weights_ = np.zeros(self.n_estimators, dtype=np.float64)
        self.estimator_errors_ = np.zeros(self.n_estimators, dtype=np.float64)
        self.classes_ = None
        self.n_classes_ = None

    def _supports_sample_weight(self, estimator):
        """Check if the estimator's fit method supports sample_weight."""
        fit_signature = inspect.signature(estimator.fit)
        return "sample_weight" in fit_signature.parameters

    def _fit(self, X, y):
        """Build a boosted classifier from the training set (X, y)."""
        n_samples = X.shape[0]
        self.classes_, y_encoded = np.unique(
            y, return_inverse=True
        )  # Use encoded y internally
        self.n_classes_ = len(self.classes_)

        # Initialize weights
        sample_weight = np.full(n_samples, 1 / n_samples)
        self.estimators_ = []  # Reset estimators for each fit

        for iboost in range(self.n_estimators):
            # Fit a classifier on the current weighted sample

            # Create a new instance of the base estimator for this iteration
            # Ensure parameters like max_depth and min_samples_split are correctly passed
            # from the template (self.base_estimator_)
            if isinstance(self.base_estimator_, ClassifierTree):
                # If default tree, instantiate with stored params
                estimator = ClassifierTree(
                    max_depth=self.base_estimator_.max_depth,
                    min_samples_split=self.base_estimator_.min_samples_split,
                )
            else:
                try:
                    estimator = self.base_estimator_.__class__(
                        **self.base_estimator_.get_params()
                    )
                except Exception as e:  # Catch any exception and handle it
                    raise ValueError(f"Error creating estimator: {e}") from "_fit"

            estimator.fit(
                X, y_encoded, sample_weight=sample_weight
            )  # Fit on encoded labels

            # Predict
            y_pred = estimator.predict(X)

            # Identify misclassified samples
            incorrect = y_pred != y_encoded

            # Calculate weighted error
            estimator_error = np.dot(sample_weight, incorrect) / np.sum(sample_weight)

            # Stop if perfect fit or error is too high/low
            if estimator_error <= 0:
                # Perfect fit, assign max weight and stop
                self.estimator_weights_[iboost] = 1.0
                self.estimator_errors_[iboost] = 0.0
                self.estimators_.append(estimator)
                break
            elif estimator_error >= 1.0 - (1.0 / self.n_classes_):
                # Worse than random guessing or error is 1 (all wrong)
                # Stop if only one estimator is fitted
                if len(self.estimators_) == 0:
                    # Don't add the failed estimator
                    warnings.warn(
                        "Base estimator initial fit failed or had error >= 1 - 1/K. Stopping.",
                        UserWarning,
                        stacklevel=2,
                    )
                    break  # Stop without adding estimator
                # Otherwise, stop boosting (don't add this poor estimator)
                warnings.warn(
                    f"Estimator error {estimator_error:.4f} >= {1.0 - (1.0 / self.n_classes_):.4f}. Stopping.",
                    UserWarning,
                    stacklevel=2,
                )
                break

            # Calculate estimator weight (alpha) using SAMME formula
            # Add epsilon to avoid log(0) if error is very close to 0
            epsilon = 1e-10
            alpha = self.learning_rate * (
                np.log((1.0 - estimator_error + epsilon) / (estimator_error + epsilon))
                + np.log(self.n_classes_ - 1.0)
            )

            # Update sample weights
            # SAMME update: w_i *= exp(alpha * I(y_i != h_m(x_i)))
            # Multiply weights of misclassified samples by exp(alpha)
            sample_weight *= np.exp(alpha * incorrect)

            # Normalize weights
            sample_weight_sum = np.sum(sample_weight)
            if sample_weight_sum <= 0:  # Avoid division by zero if all weights became 0
                warnings.warn(
                    "Sample weights sum to zero. Stopping.", UserWarning, stacklevel=2
                )
                break
            sample_weight /= sample_weight_sum

            # Store estimator and its weight
            self.estimators_.append(estimator)
            self.estimator_weights_[iboost] = alpha
            self.estimator_errors_[iboost] = estimator_error

            # Early termination if error is zero (already handled above)
            # if estimator_error == 0: break

        # Trim arrays if boosting stopped early
        actual_n_estimators = len(self.estimators_)
        if actual_n_estimators < self.n_estimators:
            self.estimator_weights_ = self.estimator_weights_[:actual_n_estimators]
            self.estimator_errors_ = self.estimator_errors_[:actual_n_estimators]
            self.estimators_ = self.estimators_[:actual_n_estimators]

        # Ensure the number of weights matches the number of estimators
        self.n_estimators = len(self.estimators_)

        return self

    def fit(self, X, y):
        """Build a boosted classifier from the training set (X, y)."""
        X, y = np.asarray(X), np.asarray(y)
        unique_classes = np.unique(y)
        n_classes = len(unique_classes)
        if n_classes < 2:
            raise ValueError("Need at least 2 classes for classification.")

        # Store original classes before fitting
        self.classes_ = unique_classes
        self.n_classes_ = n_classes

        self._fit(X, y)
        return self

    def decision_function(self, X):
        """Compute the decision function of X."""
        X = np.asarray(X)
        n_classes = self.n_classes_
        n_samples = X.shape[0]

        if not hasattr(self, "estimators_") or not self.estimators_:
            # Return zero scores if not fitted or no estimators were added
            if n_classes == 2:
                return np.zeros(n_samples)
            else:
                return np.zeros((n_samples, n_classes))

        pred = np.zeros((n_samples, n_classes))

        for i, estimator in enumerate(self.estimators_):
            # Get predictions from the weak learner (expecting encoded 0, 1, ..., K-1)
            estimator_pred_encoded_list = estimator.predict(X)
            # Convert list prediction to numpy array
            estimator_pred_encoded = np.array(estimator_pred_encoded_list)

            # Handle potential None predictions if tree couldn't classify some samples
            if np.any(estimator_pred_encoded is None):  # Check for None
                warnings.warn(
                    f"Estimator {i} produced None predictions. Skipping its contribution.",
                    UserWarning,
                    stacklevel=2,
                )
                continue  # Skip this estimator if predictions are bad

            # Ensure predictions are integers for indexing
            try:
                estimator_pred_encoded = estimator_pred_encoded.astype(int)
            except ValueError:
                warnings.warn(
                    f"Estimator {i} predictions could not be cast to int. Skipping contribution.",
                    UserWarning,
                    stacklevel=2,
                )
                continue

            # Ensure predictions are within the valid range of indices
            if not np.all(
                (estimator_pred_encoded >= 0) & (estimator_pred_encoded < n_classes)
            ):
                warnings.warn(
                    f"Estimator {i} produced out-of-bounds class indices. Skipping its contribution.",
                    UserWarning,
                    stacklevel=2,
                )
                continue  # Skip this estimator if predictions are bad

            # Convert predictions to one-hot encoding
            y_pred_coded = np.zeros((n_samples, n_classes))
            y_pred_coded[np.arange(n_samples), estimator_pred_encoded] = (
                1  # Use the numpy array directly
            )

            # Add weighted prediction to the total score
            # Ensure estimator_weights_ has the right length
            if i < len(self.estimator_weights_):
                pred += self.estimator_weights_[i] * y_pred_coded
            else:
                # This case shouldn't happen if trimming in _fit is correct
                warnings.warn(
                    f"Mismatch between estimators and weights at index {i}. Stopping decision function loop.",
                    UserWarning,
                    stacklevel=2,
                )
                break

        # Normalize? SAMME doesn't require normalization for argmax, but might affect decision scores range
        # pred /= self.estimator_weights_.sum() # Optional normalization

        if n_classes == 2:
            # Return score difference for the positive class (class at index 1)
            return pred[:, 1] - pred[:, 0]
        else:
            return pred

    def predict_proba(self, X):
        """Predict class probabilities for X."""
        X = np.asarray(X)
        decision = self.decision_function(X)

        if self.n_classes_ == 2:
            # Convert binary decision function score to probabilities
            proba = sigmoid(
                decision * 2
            )  # Scale decision for better probability separation
            return np.vstack([1 - proba, proba]).T
        else:
            # Apply softmax to the multi-class decision scores
            from scipy.special import softmax

            return softmax(decision, axis=1)

    def predict(self, X):
        """Predict classes for X."""
        X = np.asarray(X)
        pred = self.decision_function(X)

        if self.n_classes_ == 2:
            # Use sign of decision function for binary
            return self.classes_[(pred > 0).astype(int)]
        else:
            # Use argmax for multi-class
            return self.classes_[np.argmax(pred, axis=1)]

    def get_stats(self, y_true, X=None, y_pred=None, verbose=False):
        """Calculate and optionally print evaluation metrics. Requires either X or y_pred."""
        if y_pred is None and X is None:
            raise ValueError("Either X or y_pred must be provided.")
        if y_pred is None:
            y_pred = self.predict(X)
            y_prob = self.predict_proba(X)
        else:
            y_prob = None  # Cannot calculate log loss reliably without predict_proba

        stats = self._calculate_metrics(y_true, y_pred, y_prob)
        if verbose:
            print("Evaluation Metrics:")
            for metric, value in stats.items():
                print(
                    f"  {metric}: {value:.4f}"
                    if isinstance(value, (float, int)) and np.isfinite(value)
                    else f"  {metric}: {value}"
                )
        return stats

    def _calculate_metrics(self, y_true, y_pred, y_prob=None):
        """Calculate common classification metrics."""
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
        metrics = {
            "Accuracy": Metrics.accuracy(y_true, y_pred),
            "Precision": Metrics.precision(y_true, y_pred),
            "Recall": Metrics.recall(y_true, y_pred),
            "F1 Score": Metrics.f1_score(y_true, y_pred),
        }
        if y_prob is not None and self.n_classes_ == 2:
            try:
                metrics["Log Loss"] = Metrics.log_loss(y_true, y_prob)
            except Exception as e:
                metrics["Log Loss"] = f"Error ({e})"
        else:
            metrics["Log Loss"] = "N/A (Multi-class or Probs not available)"
        return metrics
