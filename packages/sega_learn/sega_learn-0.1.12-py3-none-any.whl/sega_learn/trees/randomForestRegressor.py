# Importing the required libraries
import multiprocessing
from datetime import datetime

import numpy as np
from joblib import Parallel, delayed

from .treeRegressor import RegressorTree


def _fit_single_tree(
    X,
    y,
    max_depth,
    min_samples_split,
    sample_weight,
    tree_index,
    random_state_base,
    verbose,
):
    """Helper function for parallel tree fitting. Fits a single tree on abootstrapped sample.

    Args:
        X (np.ndarray): The input features.
        y (np.ndarray): The target labels.
        max_depth (int): The maximum depth of the tree.
        min_samples_split (int): The minimum samples required to split a node.
        sample_weight (array-like): Sample weights for each instance in X.
        tree_index (int): Index of the tree for seeding.
        random_state_base (int): Base random seed.
        verbose (bool): If True, print detailed logs during fitting.

    Returns:
        tuple: (tree_index, fitted_tree_instance, bootstrap_indices)
    """
    # Ensure reproducibility for each tree if random_state is set
    if random_state_base is not None:
        np.random.seed(random_state_base + tree_index)

    # Create bootstrapped sample indices
    n_samples = X.shape[0]
    indices = np.random.choice(n_samples, size=n_samples, replace=True)
    X_sample = X[indices]
    y_sample = y[indices]

    # Instantiate and fit the tree
    tree = RegressorTree(max_depth=max_depth, min_samples_split=min_samples_split)
    tree.fit(X_sample, y_sample, sample_weight, verbose)  # Use the fit method

    return tree_index, tree, indices  # Return the instance and indices


class RandomForestRegressor:
    """A class representing a Random Forest model for regression.

    Attributes:
        n_estimators (int): The number of trees in the forest.
        max_depth (int): The maximum depth of each tree.
        min_samples_split (int): The minimum number of samples required to split an internal node.
        n_jobs (int): The number of jobs to run in parallel for fitting.
        random_state (int): Seed for random number generation for reproducibility.
        trees (list): List holding the fitted RegressorTree instances.
        X (numpy.ndarray or None): The feature matrix used for training.
        y (numpy.ndarray or None): The target labels used for training.

    Methods:
        fit(X=None, y=None, verbose=False): Fits the random forest to the data.
        calculate_metrics(y_true, y_pred): Calculates the evaluation metrics.
        predict(X): Predicts the target values for the input features.
        get_stats(verbose=False): Returns the evaluation metrics.
    """

    def __init__(
        self,
        n_estimators=100,
        max_depth=10,
        min_samples_split=2,
        n_jobs=-1,
        random_seed=None,
        X=None,
        y=None,
    ):
        """Initialize the Random Forest Regressor."""
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split  # Store this parameter
        self.n_jobs = n_jobs if n_jobs != 0 else max(1, multiprocessing.cpu_count())
        if n_jobs == -1:
            self.n_jobs = max(1, multiprocessing.cpu_count())
        self.random_state = random_seed
        self.trees = []  # Will store RegressorTree instances
        self._X_fit_shape = None  # Store shape for predict validation
        self.X = X
        self.y = y

    def get_params(self):
        """Get the parameters of the Random Forest Regressor.

        Returns:
            dict: A dictionary containing the parameters of the model.
        """
        return {
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "n_jobs": self.n_jobs,
            "random_seed": self.random_state,
        }

    def fit(self, X=None, y=None, sample_weight=None, verbose=False):
        """Fit the random forest to the training data X and y.

        Args:
            X (array-like): Training input features of shape (n_samples, n_features).
            y (array-like): Training target values of shape (n_samples,).
            sample_weight (array-like): Sample weights for each instance in X.
            verbose (bool): Whether to print progress messages.

        Returns:
            self: The fitted RandomForestRegressor instance.
        """
        if X is None and self.X is None:
            raise ValueError(
                "X must be provided either during initialization or fitting."
            )
        if y is None and self.y is None:
            raise ValueError(
                "y must be provided either during initialization or fitting."
            )
        start_time = datetime.now()

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

        if verbose:
            print(
                f"Fitting {self.n_estimators} trees in parallel using {self.n_jobs} jobs..."
            )

        # Fit trees in parallel
        # Pass necessary parameters and a way to seed each job differently
        results = Parallel(n_jobs=self.n_jobs)(
            delayed(_fit_single_tree)(
                X,
                y,
                self.max_depth,
                self.min_samples_split,
                sample_weight,
                i,
                self.random_state,
                verbose,
            )
            for i in range(self.n_estimators)
        )

        # Process results - results are tuples: (tree_index, tree_instance, bootstrap_indices)
        # Sort results by tree_index to maintain order if needed, though usually not critical for RF
        results.sort(key=lambda item: item[0])
        self.trees = [result[1] for result in results]

        if verbose:
            elapsed = datetime.now() - start_time
            print(f"Forest fitting completed in {elapsed}.")

        return self

    def predict(self, X):
        """Predict target values for input features X using the trained random forest.

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
            raise RuntimeError("The forest has no trees. Please fit the model first.")

        # Make predictions using each tree's predict method
        # Each tree.predict(X) returns an array of shape (n_samples,)
        all_predictions = np.array([tree.predict(X) for tree in self.trees])

        # Check for NaNs which might occur from tree._traverse_tree if nodes are bad
        if np.isnan(all_predictions).any():
            print(
                "Warning: NaN predictions encountered from some trees. Averaging will ignore NaNs."
            )
            # Average predictions across trees, ignoring NaNs
            # np.nanmean computes the mean ignoring NaNs
            return np.nanmean(all_predictions, axis=0)
        else:
            # Average predictions across trees (axis=0)
            return np.mean(all_predictions, axis=0)

    def get_stats(self, y_true, y_pred, verbose=False):
        """Calculate and optionally print evaluation metrics.

        Args:
            y_true (array-like): True target values.
            y_pred (array-like): Predicted target values.
            verbose (bool): Whether to print progress messages (e.g., residuals).

        Returns:
            dict: A dictionary containing calculated metrics (MSE, R^2, MAE, RMSE, MAPE).
        """
        stats = self.calculate_metrics(y_true, y_pred)
        if verbose:
            print("Evaluation Metrics:")
            for metric, value in stats.items():
                print(f"  {metric}: {value:.4f}")
        return stats

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

        # R^2 calculation
        sst = np.sum((y_true - np.mean(y_true)) ** 2)
        ssr = np.sum((y_true - y_pred) ** 2)
        r2 = (
            1 - (ssr / sst) if sst != 0 else (1.0 if ssr == 0 else 0.0)
        )  # Handle constant y_true

        # MAPE calculation
        mask = y_true != 0
        if np.any(mask):
            mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        elif np.allclose(y_true, y_pred):  # All true are zero, check if preds match
            mape = 0.0
        else:
            mape = np.inf  # Or np.nan, depends on definition preference when true is 0

        return {"MSE": mse, "R^2": r2, "MAE": mae, "RMSE": rmse, "MAPE": mape}
