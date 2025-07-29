import inspect

import numpy as np

from sega_learn.trees.treeRegressor import RegressorTree  # Base estimator
from sega_learn.utils.metrics import Metrics  # For R2 etc.


class AdaBoostRegressor:
    """AdaBoost regressor.

    Builds an additive model by sequentially fitting weak regressors (default: decision trees)
    on modified versions of the data. The weights of instances are adjusted at each iteration
    so that subsequent regressors focus more on instances with larger errors.

    Uses the AdaBoost.R2 algorithm.

    Attributes:
        base_estimator_ (object): The base estimator template used for fitting.
        n_estimators (int): The maximum number of estimators at which boosting is terminated.
        learning_rate (float): Contribution of each regressor to the final prediction.
        loss (str): The loss function to use when updating the weights ('linear', 'square', 'exponential').
        estimators_ (list): The collection of fitted base estimators.
        estimator_weights_ (np.ndarray): Weights for each estimator (alpha values, specifically log(1/beta)).
        estimator_errors_ (np.ndarray): Loss value for each estimator on the weighted training data.
    """

    def __init__(
        self,
        base_estimator=None,
        n_estimators=50,
        learning_rate=1.0,
        loss="linear",
        random_state=None,
        max_depth=3,
        min_samples_split=2,
    ):
        """Initialize the AdaBoostRegressor.

        Args:
            base_estimator (object, optional): The base estimator from which the boosted ensemble is built.
                                              Support for sample weighting is required. If None, then
                                              the base estimator is DecisionTreeRegressor(max_depth=3).
            n_estimators (int, optional): The maximum number of estimators. Defaults to 50.
            learning_rate (float, optional): Shrinks the contribution of each regressor by learning_rate. Defaults to 1.0.
            loss (str, optional): The loss function to use when updating sample weights ('linear', 'square', 'exponential').
                                  Defaults to 'linear'.
            random_state (int, optional): Controls the random seed. Defaults to None.
            max_depth (int, optional): Maximum depth of the base estimator. Defaults to 3.
            min_samples_split (int, optional): Minimum number of samples required to split an internal node. Defaults to 2.
        """
        if base_estimator is None:
            # Default to a slightly deeper tree than for classifier
            self.base_estimator_ = RegressorTree(
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
        if loss not in ("linear", "square", "exponential"):
            raise ValueError("Loss must be 'linear', 'square', or 'exponential'")
        self.loss = loss
        self.random_state = random_state  # Not used directly in boosting, but for potential base estimator seeding

        self.estimators_ = []
        self.estimator_weights_ = np.zeros(self.n_estimators, dtype=np.float64)
        self.estimator_errors_ = np.zeros(self.n_estimators, dtype=np.float64)

    def _supports_sample_weight(self, estimator):
        """Check if the estimator's fit method supports sample_weight."""
        fit_signature = inspect.signature(estimator.fit)
        return "sample_weight" in fit_signature.parameters

    def _fit(self, X, y):
        """Build a boosted regressor from the training set (X, y)."""
        n_samples = X.shape[0]

        # Initialize weights
        sample_weight = np.full(n_samples, 1 / n_samples)
        self.estimators_ = []  # Reset estimators for each fit

        for iboost in range(self.n_estimators):
            # Create a new instance of the base estimator for this iteration
            # Ensure parameters like max_depth and min_samples_split are correctly passed
            # from the template (self.base_estimator_)
            if isinstance(self.base_estimator_, RegressorTree):
                # If default tree, instantiate with stored params
                estimator = RegressorTree(
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

            estimator.fit(X, y, sample_weight=sample_weight)  # Pass weights

            # Predict
            y_pred = estimator.predict(X)

            # Calculate absolute errors
            errors = np.abs(y - y_pred)
            max_error = np.max(errors)

            # Handle case where all predictions are perfect
            if max_error == 0:
                # Perfect fit, assign max weight and stop (or continue if needed?)
                self.estimator_weights_[iboost] = (
                    1.0  # Use alpha = log(1/beta) -> beta=exp(-alpha)
                )
                self.estimator_errors_[iboost] = 0.0
                self.estimators_.append(estimator)
                break

            # Calculate loss based on chosen type
            if self.loss == "linear":
                loss_sample = errors / max_error
            elif self.loss == "square":
                loss_sample = (errors / max_error) ** 2
            else:  # exponential
                loss_sample = 1.0 - np.exp(-errors / max_error)

            # Clip loss to avoid numerical issues (e.g., loss >= 1)
            loss_sample = np.clip(loss_sample, 0.0, 1.0 - 1e-7)

            # Calculate weighted average loss
            estimator_error = np.dot(sample_weight, loss_sample)  # This is L_m

            # Stop if error is too high (e.g., >= 0.5)
            if estimator_error >= 0.5:
                # If it's the first estimator, raise error. Otherwise, stop boosting.
                if len(self.estimators_) == 0:
                    raise ValueError(
                        "Base estimator initial fit failed or had error >= 0.5."
                    )
                break

            # Calculate beta
            beta = estimator_error / (1.0 - estimator_error)

            # Calculate estimator weight (alpha)
            alpha = self.learning_rate * np.log(1.0 / beta)

            # Update sample weights
            # w_i *= beta**(1 - loss_i)
            sample_weight *= np.power(beta, 1.0 - loss_sample)

            # Normalize weights
            sample_weight_sum = np.sum(sample_weight)
            if sample_weight_sum <= 0:  # Avoid division by zero
                break
            sample_weight /= sample_weight_sum

            # Store estimator and its weight (alpha)
            self.estimators_.append(estimator)
            self.estimator_weights_[iboost] = alpha
            self.estimator_errors_[iboost] = estimator_error

            # Early termination (optional, based on error or other criteria)
            # if estimator_error == 0: break # Already handled by max_error check

        # Trim arrays if boosting stopped early
        actual_n_estimators = len(self.estimators_)
        self.estimator_weights_ = self.estimator_weights_[:actual_n_estimators]
        self.estimator_errors_ = self.estimator_errors_[:actual_n_estimators]

        return self

    def fit(self, X, y):
        """Build a boosted regressor from the training set (X, y)."""
        X, y = np.asarray(X), np.asarray(y)
        if y.ndim != 1:
            raise ValueError("y must be a 1D array for regression.")

        self._fit(X, y)
        return self

    def predict(self, X):
        """Predict regression target for X."""
        X = np.asarray(X)
        n_samples = X.shape[0]
        n_estimators = len(self.estimators_)

        if n_estimators == 0:
            # Handle case where no estimators were fitted (e.g., early stopping on first try)
            # Return mean of y? Or raise error? Let's raise error.
            raise RuntimeError("AdaBoostRegressor not fitted.")

        # Get predictions from all estimators
        predictions = np.array(
            [est.predict(X) for est in self.estimators_]
        ).T  # Shape (n_samples, n_estimators)
        weights = self.estimator_weights_  # Shape (n_estimators,)

        # Calculate weighted median for each sample
        sorted_indices = np.argsort(predictions, axis=1)
        sorted_weights = weights[sorted_indices]
        sorted_predictions = np.take_along_axis(predictions, sorted_indices, axis=1)

        # Cumulative weights
        weight_cdf = np.cumsum(sorted_weights, axis=1)
        total_weight = np.sum(weights)

        # Find the median point
        median_or_above = weight_cdf >= 0.5 * total_weight
        median_idx = np.argmax(median_or_above, axis=1)

        # Extract the weighted median prediction for each sample
        weighted_median = sorted_predictions[np.arange(n_samples), median_idx]

        return weighted_median

    def get_stats(self, y_true, X=None, y_pred=None, verbose=False):
        """Calculate and optionally print evaluation metrics. Requires either X or y_pred."""
        if y_pred is None and X is None:
            raise ValueError("Either X or y_pred must be provided.")
        if y_pred is None:
            y_pred = self.predict(X)

        stats = self._calculate_metrics(y_true, y_pred)
        if verbose:
            print("Evaluation Metrics:")
            for metric, value in stats.items():
                print(
                    f"  {metric}: {value:.4f}"
                    if np.isfinite(value)
                    else f"  {metric}: {value}"
                )
        return stats

    def _calculate_metrics(self, y_true, y_pred):
        """Calculate common regression metrics."""
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
        metrics = {
            "MSE": Metrics.mean_squared_error(y_true, y_pred),
            "R^2": Metrics.r_squared(y_true, y_pred),
            "MAE": Metrics.mean_absolute_error(y_true, y_pred),
            "RMSE": Metrics.root_mean_squared_error(y_true, y_pred),
            "MAPE": Metrics.mean_absolute_percentage_error(y_true, y_pred),
        }
        return metrics
