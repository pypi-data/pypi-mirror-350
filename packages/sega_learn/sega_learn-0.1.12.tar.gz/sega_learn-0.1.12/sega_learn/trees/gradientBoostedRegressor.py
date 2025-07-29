import numpy as np

from .treeRegressor import RegressorTree


class GradientBoostedRegressor:
    """A class to represent a Gradient Boosted Decision Tree Regressor.

    Attributes:
        random_seed (int): The random seed for the random number generator.
        num_trees (int): The number of decision trees in the ensemble.
        max_depth (int): The maximum depth of each decision tree.
        learning_rate (float): The learning rate for the gradient boosted model.
        min_samples_split (int): The minimum number of samples required to split a node.
        random_seed (int): The random seed for the random number generator.

    Methods:
        fit(X=None, y=None, verbose=0): Fits the gradient boosted decision tree regressor to the training data.
        predict(X): Predicts the target values for the input features.
        calculate_metrics(y_true, y_pred): Calculates the evaluation metrics.
        get_stats(y_true, y_pred, verbose=False): Returns the evaluation metrics.
    """

    def __init__(
        self,
        X=None,
        y=None,
        num_trees: int = 100,
        max_depth: int = 3,  # Default max_depth for GBR is usually smaller
        learning_rate: float = 0.1,  # Added learning rate
        min_samples_split: int = 2,  # Added min_samples_split
        random_seed: int = None,  # Added random_state (though not used yet)
    ):
        """Initializes the Gradient Boosted Decision Tree Regressor.

        Args:
            X: (np.ndarray), optional - Input feature data (default is None).
            y: (np.ndarray), optional - Target data (default is None).
            num_trees (int): Number of boosting stages (trees).
            max_depth (int): Maximum depth of each individual tree regressor.
            learning_rate (float): Step size shrinkage to prevent overfitting.
            min_samples_split (int): Minimum samples required to split a node.
            random_seed (int): Seed for reproducibility (currently affects feature selection within trees).
        """
        self.n_estimators = num_trees
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.min_samples_split = min_samples_split  # Store this parameter
        self.random_state = random_seed  # Store, passed to tree if needed later

        self.trees = []  # Will store RegressorTree instances
        self.mean_absolute_residuals_ = []  # Store mean absolute residuals for each tree
        self.initial_prediction_ = None  # Store initial prediction (mean)
        self._X_fit_shape = None  # Store shape for predict validation

        if X is not None:
            self.X = np.asarray(X)
        if y is not None:
            self.y = np.asarray(y).astype(float)  # Ensure y is float for residuals

    def get_params(self):
        """Get the parameters of the GradientBoostedRegressor."""
        return {
            "num_trees": self.n_estimators,
            "max_depth": self.max_depth,
            "learning_rate": self.learning_rate,
            "min_samples_split": self.min_samples_split,
            "random_seed": self.random_state,
        }

    def fit(self, X=None, y=None, sample_weight=None, verbose=0):
        """Fits the gradient boosted decision tree regressor to the training data.

        This method trains the ensemble of decision trees by iteratively fitting each tree to the residuals
        of the previous iteration. The residuals are updated after each iteration by subtracting the predictions
        made by the current tree from the :target values.

        Args:
            X (array-like): Training input features of shape (n_samples, n_features).
            y (array-like): Training target values of shape (n_samples,).
            sample_weight (array-like): Sample weights for each instance (not used in this implementation).
            verbose (int): Whether to print progress messages (e.g., residuals). 0 for no output, 1 for output, >1 for detailed output

        Returns:
            self: The fitted GradientBoostedRegressor instance.
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

        if X.ndim != 2:
            raise ValueError("X must be a 2D array.")
        if y.ndim != 1:
            raise ValueError("y must be a 1D array.")
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have the same number of samples.")
        if X.shape[0] == 0:
            raise ValueError("X and y must not be empty.")

        # Sample weight handling
        if sample_weight is None:
            sample_weight = np.ones(len(y), dtype=np.float64)
        else:
            sample_weight = np.asarray(sample_weight, dtype=np.float64)
            if sample_weight.shape[0] != len(y):
                raise ValueError("sample_weight length mismatch.")

        self._X_fit_shape = X.shape
        n_samples = X.shape[0]

        # Initialize predictions: Start with the mean of y
        self.initial_prediction_ = np.mean(y)
        current_predictions = np.full(n_samples, self.initial_prediction_, dtype=float)

        self.trees = []  # Clear any previous trees

        for i in range(self.n_estimators):
            # Calculate residuals (negative gradient for squared error loss)
            residuals = y - current_predictions

            # Instantiate and fit a tree to the residuals
            # Note: random_state could be used here if RegressorTree utilizes it
            # for feature/split point selection randomness control.
            tree = RegressorTree(
                max_depth=self.max_depth, min_samples_split=self.min_samples_split
            )

            tree.fit(
                X,
                residuals,
                sample_weight,
                verbose=True if verbose > 1 else False,  # noqa: SIM210
            )  # Fit tree on current residuals

            # Get predictions from the new tree
            # Predict expects 2D array, returns 1D
            update = tree.predict(X)

            # Update current predictions with shrunk contribution from the new tree
            current_predictions += self.learning_rate * update

            # Store the fitted tree
            self.trees.append(tree)

            # Calculate mean absolute residual for monitoring
            self.mean_absolute_residuals_.append(
                np.mean(np.abs(y - current_predictions))
            )
            if verbose > 0:
                print(
                    f"Tree {i + 1}/{self.n_estimators} fitted. Mean Absolute Residual: {self.mean_absolute_residuals_[-1]:.4f}"
                )

        return self

    def predict(self, X):
        """Predicts target values for input features X using the fitted GBR model.

        Args:
            X (array-like): Input features of shape (n_samples, n_features).

        Returns:
            np.ndarray: Predicted target values of shape (n_samples,).
        """
        X = np.asarray(X)
        if self._X_fit_shape is None:
            raise RuntimeError("The model has not been fitted yet.")
        if X.ndim != 2:
            raise ValueError("Input X must be a 2D array.")
        if X.shape[1] != self._X_fit_shape[1]:
            raise ValueError(
                f"Input data must have {self._X_fit_shape[1]} features, but got {X.shape[1]}."
            )
        if X.shape[0] == 0:
            return np.array([])
        if not self.trees:
            # If fit wasn't called or n_estimators=0, return initial prediction
            if self.initial_prediction_ is None:
                raise RuntimeError(
                    "The model has not been fitted yet and initial prediction is unknown."
                )
            return np.full(X.shape[0], self.initial_prediction_)

        # Start with the initial prediction
        predictions = np.full(X.shape[0], self.initial_prediction_, dtype=float)

        # Add predictions from each tree, scaled by learning rate
        for tree in self.trees:
            predictions += self.learning_rate * tree.predict(X)

        return predictions

    def calculate_metrics(self, y_true, y_pred):
        """Calculate common regression metrics.

        Args:
            y_true (array-like): True target values.
            y_pred (array-like): Predicted target values.

        Returns:
            dict: A dictionary containing calculated metrics (MSE, R^2, MAE, RMSE, MAPE).
        """
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)

        if y_true.shape != y_pred.shape:
            raise ValueError("y_true and y_pred must have the same shape.")
        if len(y_true) == 0:
            return {
                "MSE": np.nan,
                "R^2": np.nan,
                "MAE": np.nan,
                "RMSE": np.nan,
                "MAPE": np.nan,
            }

        mse = np.mean((y_true - y_pred) ** 2)
        mae = np.mean(np.abs(y_true - y_pred))
        rmse = np.sqrt(mse)

        sst = np.sum((y_true - np.mean(y_true)) ** 2)
        ssr = np.sum((y_true - y_pred) ** 2)
        r2 = 1 - (ssr / sst) if sst != 0 else (1.0 if ssr == 0 else 0.0)

        mask = y_true != 0
        if np.any(mask):
            mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        elif np.allclose(y_true, y_pred):
            mape = 0.0
        else:
            mape = np.inf

        return {"MSE": mse, "R^2": r2, "MAE": mae, "RMSE": rmse, "MAPE": mape}

    def get_stats(self, y_true, y_pred, verbose=False):
        """Calculate and optionally print evaluation metrics.

        Args:
            y_true (array-like): True target values.
            y_pred (array-like): Predicted target values.
            verbose (bool): Whether to print progress messages (e.g., residuals).

        Returns:
            dict: A dictionary containing calculated metrics (MSE, R^2, MAE, RMSE, MAPE).
        """
        # Ensure y_true is the original target values corresponding to the predictions
        stats = self.calculate_metrics(y_true, y_pred)
        if verbose:
            print("Evaluation Metrics:")
            for metric, value in stats.items():
                # Handle potential NaN/inf in MAPE nicely
                print(
                    f"  {metric}: {value:.4f}"
                    if np.isfinite(value)
                    else f"  {metric}: {value}"
                )
        return stats
