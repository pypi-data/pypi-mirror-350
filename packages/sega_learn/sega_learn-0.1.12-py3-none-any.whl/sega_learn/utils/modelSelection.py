from itertools import product

import numpy as np

from sega_learn.pipelines import Pipeline

from .dataPrep import DataPrep
from .metrics import Metrics


class ModelSelectionUtility:
    """A utility class for hyperparameter tuning and cross-validation of machine learning models."""

    @staticmethod
    def get_param_combinations(param_grid):
        """Generates all possible combinations of hyperparameters.

        Returns:
            param_combinations (list): A list of dictionaries containing hyperparameter combinations.
        """
        all_params = {}
        for grid in param_grid:
            all_params.update(grid)

        keys, values = zip(*all_params.items())
        param_combinations = [dict(zip(keys, v)) for v in product(*values)]
        return param_combinations

    @staticmethod
    def cross_validate(
        model, X, y, params, cv=5, metric="mse", direction="minimize", verbose=False
    ):
        """Implements a custom cross-validation for hyperparameter tuning.

        Args:
            model: The model Object to be tuned.
            X: (numpy.ndarray) - The feature columns.
            y: (numpy.ndarray) - The label column.
            params: (dict) - The hyperparameters to be tuned.
            cv: (int) - The number of folds for cross-validation. Default is 5.
            metric: (str) - The metric to be used for evaluation. Default is 'mse'.
                - Regression Metrics: 'mse', 'r2', 'mae', 'rmse', 'mape', 'mpe'
                - Classification Metrics: 'accuracy', 'precision', 'recall', 'f1', 'log_loss'
            direction: (str) - The direction to optimize the metric. Default is 'minimize'.
            verbose: (bool) - A flag to display the training progress. Default is False.

        Returns:
            tuple: A tuple containing the scores (list) and the trained model.
        """
        scores = []
        if verbose:
            print(f"Training Model with Params: {params}")
        for i in range(cv):
            # If model is Pipeline, set params
            if isinstance(model, Pipeline):
                active_model = model.set_params(**params)
            else:
                active_model = model(**params)

            X_folds, y_folds = DataPrep.k_split(X, y, k=cv)
            X_train, y_train = (
                np.concatenate(X_folds[:i] + X_folds[i + 1 :]),
                np.concatenate(y_folds[:i] + y_folds[i + 1 :]),
            )
            X_test, y_test = X_folds[i], y_folds[i]

            active_model.fit(X_train, y_train)
            y_pred = active_model.predict(X_test)

            # Regression Metrics
            if metric in ["mse", "mean_squared_error"]:
                s = Metrics.mean_squared_error(y_test, y_pred)
            elif metric in ["r2", "r_squared"]:
                s = Metrics.r_squared(y_test, y_pred)
            elif metric in ["mae", "mean_absolute_error"]:
                s = Metrics.mean_absolute_error(y_test, y_pred)
            elif metric in ["rmse", "root_mean_squared_error"]:
                s = Metrics.root_mean_squared_error(y_test, y_pred)
            elif metric in ["mape", "mean_absolute_percentage_error"]:
                s = Metrics.mean_absolute_percentage_error(y_test, y_pred)
            elif metric in ["mpe", "mean_percentage_error"]:
                s = Metrics.mean_percentage_error(y_test, y_pred)

            # Classification Metrics
            elif metric == "accuracy":
                s = Metrics.accuracy(y_test, y_pred)
            elif metric == "precision":
                s = Metrics.precision(y_test, y_pred)
            elif metric == "recall":
                s = Metrics.recall(y_test, y_pred)
            elif metric == "f1":
                s = Metrics.f1_score(y_test, y_pred)
            elif metric == "log_loss":
                s = Metrics.log_loss(y_test, y_pred)

            scores.append(s)

            if verbose:
                print(f"\tCV Fold {i + 1}: - {metric}: {s:.2f}")

        return scores, active_model


class GridSearchCV:
    """Implements a grid search cross-validation for hyperparameter tuning."""

    def __init__(self, model, param_grid, cv=5, metric="mse", direction="minimize"):
        """Initializes the GridSearchCV object.

        Args:
            model: The model Object to be tuned.
            param_grid: (list) - A list of dictionaries containing hyperparameters to be tuned.
            cv: (int) - The number of folds for cross-validation. Default is 5.
            metric: (str) - The metric to be used for evaluation. Default is 'mse'.
                - Regression Metrics: 'mse', 'r2', 'mae', 'rmse', 'mape', 'mpe'
                - Classification Metrics: 'accuracy', 'precision', 'recall', 'f1', 'log_loss'
            direction: (str) - The direction to optimize the metric. Default is 'minimize'.
        """
        self.model = model
        self.param_grid = param_grid
        self.cv = cv
        self.metric = metric
        self.direction = direction

        assert self.param_grid, "param_grid cannot be empty."

        # Generate all possible hyperparameter combinations
        self.param_combinations = ModelSelectionUtility.get_param_combinations(
            self.param_grid
        )

    def fit(self, X, y, verbose=False):
        """Fits the model to the data for all hyperparameter combinations.

        Args:
            X: (numpy.ndarray) - The feature columns.
            y: (numpy.ndarray) - The label column.
            verbose: (bool) - A flag to display the training progress. Default is True.

        Returns:
            model: The best model with the optimal hyperparameters.
        """
        if self.direction == "minimize":
            self.best_score_ = np.inf
        if self.direction == "maximize":
            self.best_score_ = -np.inf
        self.best_params_ = None

        for params in self.param_combinations:
            try:
                scores, self.active_model = ModelSelectionUtility.cross_validate(
                    self.model,
                    X,
                    y,
                    params,
                    cv=self.cv,
                    metric=self.metric,
                    direction=self.direction,
                    verbose=verbose,
                )
            except Exception as e:
                if verbose:
                    print(f"Error with params {params}: {e}")
                continue

            mean_score = np.mean(scores)
            if verbose:
                print(f"\t-Mean Score: {mean_score:.2f}")

            if self.direction == "minimize" and mean_score < self.best_score_:
                self.best_score_ = mean_score
                self.best_params_ = params
                self.best_model = self.active_model
            if self.direction == "maximize" and mean_score > self.best_score_:
                self.best_score_ = mean_score
                self.best_params_ = params
                self.best_model = self.active_model

        # If self.best_model exists, return it
        if hasattr(self, "best_model"):
            return self.best_model
        else:
            return None


class RandomSearchCV:
    """Implements a random search cross-validation for hyperparameter tuning."""

    def __init__(
        self, model, param_grid, iter=10, cv=5, metric="mse", direction="minimize"
    ):
        """Initializes the RandomSearchCV object.

        Args:
            model: The model Object to be tuned.
            param_grid: (list) - A list of dictionaries containing hyperparameters to be tuned.
            iter: (int) - The number of iterations for random search. Default is 10.
            cv: (int) - The number of folds for cross-validation. Default is 5.
            metric: (str) - The metric to be used for evaluation. Default is 'mse'.
                - Regression Metrics: 'mse', 'r2', 'mae', 'rmse', 'mape', 'mpe'
                - Classification Metrics: 'accuracy', 'precision', 'recall', 'f1', 'log_loss'
            direction: (str) - The direction to optimize the metric. Default is 'minimize'.
        """
        self.model = model
        self.param_grid = param_grid
        self.iter = iter
        self.cv = cv
        self.metric = metric
        self.direction = direction

        assert self.iter > 0, "iter must be greater than 0."
        assert self.param_grid, "param_grid cannot be empty."

        # Generate all possible hyperparameter combinations
        self.param_combinations = ModelSelectionUtility.get_param_combinations(
            self.param_grid
        )

    def fit(self, X, y, verbose=False):
        """Fits the model to the data for iter random hyperparameter combinations.

        Args:
            X: (numpy.ndarray) - The feature columns.
            y: (numpy.ndarray) - The label column.
            verbose: (bool) - A flag to display the training progress. Default is True.

        Returns:
            model: The best model with the optimal hyperparameters.
        """
        if self.direction == "minimize":
            self.best_score_ = np.inf
        if self.direction == "maximize":
            self.best_score_ = -np.inf
        self.best_params_ = None

        # Store tried combinations
        self.tried_params = []

        for _i in range(self.iter):
            # Check if all parameter combinations have been tried
            if len(self.tried_params) >= len(self.param_combinations):
                if verbose:
                    print("All parameter combinations have been tried.")
                break

            # Randomly select hyperparameters
            params = np.random.choice(self.param_combinations)
            while params in self.tried_params:
                params = np.random.choice(self.param_combinations)

            # Store tried combinations
            self.tried_params.append(params)

            try:
                scores, self.active_model = ModelSelectionUtility.cross_validate(
                    self.model,
                    X,
                    y,
                    params,
                    cv=self.cv,
                    metric=self.metric,
                    direction=self.direction,
                    verbose=verbose,
                )
            except Exception as e:
                if verbose:
                    print(f"Error with params {params}: {e}")
                continue

            mean_score = np.mean(scores)
            if verbose:
                print(f"\t-Mean Score: {mean_score:.2f}")

            if self.direction == "minimize" and mean_score < self.best_score_:
                self.best_score_ = mean_score
                self.best_params_ = params
                self.best_model = self.active_model
            if self.direction == "maximize" and mean_score > self.best_score_:
                self.best_score_ = mean_score
                self.best_params_ = params
                self.best_model = self.active_model

        # If self.best_model exists, return it
        if hasattr(self, "best_model"):
            return self.best_model
        else:
            return None


class segaSearchCV:
    """Implements a custom search cross-validation for hyperparameter tuning."""

    def __init__(
        self, model, param_space, iter=10, cv=5, metric="mse", direction="minimize"
    ):
        """Initializes the segaSearchCV object.

        Args:
            model: The model Object to be tuned.
            param_space (list): A list of dictionaries containing hyperparameters to be tuned.
                Should be in the format: [{'param': [type, min, max]}, ...]
            iter (int): The number of iterations for random search. Default is 10.
            cv (int): The number of folds for cross-validation. Default is 5.
            metric (str): The metric to be used for evaluation. Default is 'mse'.
                - Regression Metrics: 'mse', 'r2', 'mae', 'rmse', 'mape', 'mpe'
                - Classification Metrics: 'accuracy', 'precision', 'recall', 'f1', 'log_loss'
            direction (str): The direction to optimize the metric. Default is 'minimize'.
        """
        self.model = model
        self.param_space = param_space
        self.iter = iter
        self.cv = cv
        self.metric = metric
        self.direction = direction

        assert self.iter > 0, "iter must be greater than 0."
        assert self.param_space, "param_space cannot be empty."

        self.param_lims = {}
        for param in self.param_space:
            key = list(param.keys())[0]
            self.param_lims[key] = param[key][1:]

    def fit(self, X, y, verbose=False):
        """Fits the model to the data for iter random hyperparameter combinations.

        Args:
            X: (numpy.ndarray)- The feature columns.
            y: (numpy.ndarray)- The label column.
            verbose: (bool) - A flag to display the training progress. Default is True.
        """
        # TODO: Store search path as binary tree, each has high, low
        if self.direction == "minimize":
            self.best_score_ = np.inf
        if self.direction == "maximize":
            self.best_score_ = -np.inf
        self.best_params_ = None

        params = {}
        param_high = {}
        param_mid = {}
        param_low = {}
        curr_h_l = None
        self.tried_params = []

        for _i in range(self.iter):
            # If params is empty, set to midpoint of param_space
            if not params:
                for param in self.param_space:
                    key = list(param.keys())[0]
                    if param[key][0] is int:
                        params[key] = (param[key][1] + param[key][2]) // 2
                    elif param[key][0] is float:
                        params[key] = (param[key][1] + param[key][2]) / 2

            if param_high:
                if param_mid == {}:
                    param_mid = params.copy()
                params = param_high.copy()
                param_high = {}
                curr_h_l = "high"
            elif param_low:
                if param_mid == {}:
                    param_mid = params.copy()
                params = param_low.copy()
                param_low = {}
                curr_h_l = "low"

            # If params were already tried, find closest untried params
            while params in self.tried_params:
                for param in self.param_space:
                    key = list(param.keys())[0]
                    # step_size = (self.param_lims[key][1] - self.param_lims[key][0]) // 2
                    step_size = 1
                    if np.random.rand() > 0.5:
                        params[key] = min(
                            params[key] + step_size, self.param_lims[key][1]
                        )
                    else:
                        params[key] = max(
                            params[key] - step_size, self.param_lims[key][0]
                        )

                    # If params are out of bounds break
                    if (
                        params[key] < self.param_lims[key][0]
                        or params[key] > self.param_lims[key][1]
                    ):
                        break

            # If params are out of bounds break
            if any(
                params[key] < self.param_lims[key][0]
                or params[key] > self.param_lims[key][1]
                for key in params
            ):
                break

            self.tried_params.append(params.copy())

            if verbose and curr_h_l is not None:
                print(f"\nParams {curr_h_l}:")

            scores, self.active_model = ModelSelectionUtility.cross_validate(
                self.model,
                X,
                y,
                params,
                cv=self.cv,
                metric=self.metric,
                direction=self.direction,
                verbose=verbose,
            )

            mean_score = np.mean(scores)
            if verbose:
                print(f"\t-Mean Score: {mean_score:.2f}")

            # Store param_high mean_score
            if curr_h_l == "high":
                p_high = params.copy()
                h_score = mean_score
            if curr_h_l == "low":
                p_low = params.copy()
                l_score = mean_score

            # Set best params and model
            if (
                self.direction == "minimize"
                and mean_score < self.best_score_
                or self.direction == "maximize"
                and mean_score > self.best_score_
            ):
                self.best_score_ = mean_score
                self.best_params_ = params.copy()
                self.best_model = self.active_model

            # If no high or low params, set them
            if param_high == {} and param_low == {}:
                if curr_h_l is None:
                    for param in params:
                        step_size = (params[param] - self.param_lims[param][0]) // 2
                        param_high[param] = min(
                            params[param] + step_size, self.param_lims[param][1]
                        )
                        param_low[param] = max(
                            params[param] - step_size, self.param_lims[param][0]
                        )
                elif h_score >= l_score:
                    if verbose:
                        print(f"\nParams High Better: {h_score:.2f} >= {l_score:.2f}")
                    for param in p_high:
                        # Step size is half distance between mid and high
                        step_size = (p_high[param] - param_mid[param]) // 2
                        param_high[param] = min(
                            p_high[param] + step_size, self.param_lims[param][1]
                        )
                        param_low[param] = max(
                            p_high[param] - step_size, self.param_lims[param][0]
                        )
                elif l_score > h_score:
                    if verbose:
                        print(f"\nParams Low Better: {l_score:.2f} > {h_score:.2f}")
                    for param in p_low:
                        # Step size is half distance between mid and low
                        step_size = (param_mid[param] - p_low[param]) // 2
                        param_high[param] = min(
                            p_low[param] + step_size, self.param_lims[param][1]
                        )
                        param_low[param] = max(
                            p_low[param] - step_size, self.param_lims[param][0]
                        )

        # If self.best_model exists, return it
        if hasattr(self, "best_model"):
            return self.best_model
        else:
            return None
