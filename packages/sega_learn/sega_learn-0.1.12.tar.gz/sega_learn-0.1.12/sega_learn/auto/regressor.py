import time
import warnings

import numpy as np

try:
    from tqdm.auto import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

from sega_learn.utils.metrics import Metrics
from sega_learn.utils.modelSelection import (
    GridSearchCV,
    RandomSearchCV,
)

from ..linear_models import (
    RANSAC,
    Bayesian,
    Lasso,
    OrdinaryLeastSquares,
    PassiveAggressiveRegressor,
    Ridge,
)
from ..nearest_neighbors import KNeighborsRegressor
from ..neural_networks import (
    AdamOptimizer,
    BaseBackendNeuralNetwork,
    MeanSquaredErrorLoss,
)
from ..svm import GeneralizedSVR, LinearSVR
from ..trees import (
    AdaBoostRegressor,
    GradientBoostedRegressor,
    RandomForestRegressor,
    RegressorTree,
)
from ..utils import Scaler

r_squared = Metrics.r_squared
root_mean_squared_error = Metrics.root_mean_squared_error
mean_absolute_percentage_error = Metrics.mean_absolute_percentage_error


class AutoRegressor:
    """A class to automatically select and evaluate the best regression model.

    Includes optional automated hyperparameter tuning using GridSearchCV or RandomSearchCV.
    """

    def __init__(
        self,
        all_kernels=False,
        tune_hyperparameters=False,
        tuning_method="random",  # 'random' or 'grid'
        tuning_iterations=10,  # For Random Search
        cv=3,  # Cross-validation folds for tuning
        tuning_metric="r2",  # Metric to optimize during tuning
    ):
        """Initializes the AutoRegressor.

        Args:
            all_kernels (bool): If True, include all SVM kernels. Default False.
            tune_hyperparameters (bool): If True, perform hyperparameter tuning. Default False.
            tuning_method (str): Method for tuning ('random' or 'grid'). Default 'random'.
            tuning_iterations (int): Number of iterations for Random Search. Default 10.
            cv (int): Number of cross-validation folds for tuning. Default 3.
            tuning_metric (str): Metric to optimize ('r2', 'neg_mean_squared_error', 'rmse', 'mae', 'mape'). Default 'r2'.
                               Note: for minimization use 'neg_mean_squared_error', 'rmse', 'mae', 'mape'.
        """
        self.all_kernels = all_kernels
        self.tune_hyperparameters = tune_hyperparameters
        self.tuning_method = tuning_method
        self.tuning_iterations = tuning_iterations
        self.cv = cv
        self.tuning_metric = tuning_metric
        self.tuning_results = {}  # To store tuning outcomes

        # --- Default Models & Classes ---
        self._model_classes_map = {
            # Linear Models
            "OrdinaryLeastSquares": OrdinaryLeastSquares,
            "Ridge": Ridge,
            "Lasso": Lasso,
            "Bayesian": Bayesian,
            "RANSAC": RANSAC,
            "PassiveAggressive": PassiveAggressiveRegressor,
            # SVM
            "LinearSVR": LinearSVR,
            "GeneralizedSVR - Linear": GeneralizedSVR,
            # Nearest Neighbors
            "KNeighborsRegressor": KNeighborsRegressor,
            # Trees
            "RegressorTree": RegressorTree,
            "RandomForestRegressor": RandomForestRegressor,
            "GradientBoostedRegressor": GradientBoostedRegressor,
            "AdaBoostRegressor": AdaBoostRegressor,
            # Neural Networks
            "BaseBackendNeuralNetwork": BaseBackendNeuralNetwork,
        }

        self._default_model_instances = {
            "OrdinaryLeastSquares": OrdinaryLeastSquares(),
            "Ridge": Ridge(),
            "Lasso": Lasso(),
            "Bayesian": Bayesian(),
            "RANSAC": RANSAC(),
            "PassiveAggressive": PassiveAggressiveRegressor(),
            "LinearSVR": LinearSVR(),
            "GeneralizedSVR - Linear": GeneralizedSVR(kernel="linear"),
            "KNeighborsRegressor": KNeighborsRegressor(),
            "RegressorTree": RegressorTree(),
            "RandomForestRegressor": RandomForestRegressor(),
            "GradientBoostedRegressor": GradientBoostedRegressor(),
            "AdaBoostRegressor": AdaBoostRegressor(),
            "BaseBackendNeuralNetwork": None,  # Placeholder, defined in fit()
        }

        self.model_types = {  # Categorization for summary
            "OrdinaryLeastSquares": "Linear",
            "Ridge": "Linear",
            "Lasso": "Linear",
            "Bayesian": "Linear",
            "RANSAC": "Linear",
            "PassiveAggressive": "Linear",
            "LinearSVR": "SVM",
            "GeneralizedSVR - Linear": "SVM",
            "GeneralizedSVR - RBF": "SVM",
            "GeneralizedSVR - Polynomial": "SVM",
            "KNeighborsRegressor": "Nearest Neighbors",
            "RegressorTree": "Trees",
            "RandomForestRegressor": "Trees",
            "GradientBoostedRegressor": "Trees",
            "AdaBoostRegressor": "Trees",
            "BaseBackendNeuralNetwork": "Neural Networks",
        }

        # Add kernel variations if needed
        if self.all_kernels:
            self._model_classes_map["GeneralizedSVR - RBF"] = GeneralizedSVR
            self._model_classes_map["GeneralizedSVR - Polynomial"] = GeneralizedSVR
            self._default_model_instances["GeneralizedSVR - RBF"] = GeneralizedSVR(
                kernel="rbf"
            )
            self._default_model_instances["GeneralizedSVR - Polynomial"] = (
                GeneralizedSVR(kernel="poly")
            )

        # Models dictionary will store the *actual* model instances used (default or tuned)
        self.models = self._default_model_instances.copy()

        # --- Default Hyperparameter Search Spaces ---
        self._param_grids = {
            "OrdinaryLeastSquares": [{"fit_intercept": [True, False]}],
            "Ridge": [
                {"alpha": np.logspace(-3, 3, 7)},
                {"fit_intercept": [True, False]},
                {"max_iter": [500, 1000, 10_000, 20_000]},
                {"tol": [1e-4, 1e-3, 1e-2]},
            ],
            "Lasso": [
                {"alpha": np.logspace(-3, 3, 7)},
                {"fit_intercept": [True, False]},
                {"max_iter": [500, 1000, 10_000, 20_000]},
                {"tol": [1e-4, 1e-3, 1e-2]},
            ],
            "Bayesian": [
                {"fit_intercept": [True, False]},
                {"max_iter": [500, 1000, 10_000, 20_000]},
                {"tol": [1e-4, 1e-3, 1e-2]},
                {"alpha_1": [1e-6, 1e-5, 1e-4, 1e-3]},
                {"alpha_2": [1e-6, 1e-5, 1e-4, 1e-3]},
                {"lambda_1": [1e-6, 1e-5, 1e-4, 1e-3]},
                {"lambda_2": [1e-6, 1e-5, 1e-4, 1e-3]},
            ],
            "RANSAC": [
                {"n": [5, 10, 25, 50, 100]},
                {"k": [5, 10, 100]},
                {"t": [0.01, 0.05, 0.1, 0.5, 1.0]},
                {"d": [5, 10, 25, 50]},
                {"model": [OrdinaryLeastSquares()]},
                # {"model": [OrdinaryLeastSquares(),Ridge(),Lasso()]}, <- supports multiple models (using just OrdinaryLeastSquares for simplicity)
            ],
            "PassiveAggressive": [
                {"C": [0.01, 0.1, 1, 10]},
                {"max_iter": [500, 1000, 2000]},
            ],
            "LinearSVR": [{"C": [0.1, 1, 10, 100]}, {"epsilon": [0.01, 0.1, 0.5]}],
            "GeneralizedSVR - Linear": [
                {"C": [0.1, 1, 10, 100]},
                {"epsilon": [0.01, 0.1, 0.5]},
            ],
            "GeneralizedSVR - RBF": [
                {"C": [0.1, 1, 10, 100]},
                {"gamma": ["scale", "auto", 0.1, 1]},
            ],
            "GeneralizedSVR - Polynomial": [
                {"C": [0.1, 1, 10, 100]},
                {"degree": [2, 3, 4]},
                {"gamma": ["scale", "auto"]},
            ],
            "KNeighborsRegressor": [
                {"n_neighbors": [3, 5, 7, 9]},
                {"distance_metric": ["euclidean", "manhattan"]},
            ],
            "RegressorTree": [
                {"max_depth": [5, 10, 15, 20, 25, 50]},
                {"min_samples_split": [2, 5, 10, 20, 25, 50]},
            ],
            "RandomForestRegressor": [
                {"n_estimators": [50, 100, 200]},
                {"max_depth": [5, 10, 15]},
                {"min_samples_split": [2, 5, 10, 20, 25, 50]},
            ],
            "GradientBoostedRegressor": [
                {"num_trees": [50, 100, 200]},
                {"max_depth": [3, 5, 7]},
                {"min_samples_split": [2, 5, 10, 20, 25, 50]},
                {"learning_rate": [0.01, 0.1, 0.5, 1.0]},
            ],
            "AdaBoostRegressor": [
                {"n_estimators": [50, 100, 200]},
                {"learning_rate": [0.001, 0.01, 0.1]},
                {"min_samples_split": [2, 5, 10]},
                {"max_depth": [1, 3, 5]},
            ],
        }
        # Note: Neural Network is excluded from this grid/random search tuning loop.

        self.predictions = {}
        self.results = []  # Stores fitting/evaluation results

    def fit(
        self,
        X_train,
        y_train,
        X_test=None,
        y_test=None,
        custom_metrics=None,
        verbose=False,
    ):
        """Fits the regression models, optionally performing hyperparameter tuning.

        Args:
            X_train: (np.ndarray) - Training feature data.
            y_train: (np.ndarray) - Training target data.
            X_test: (np.ndarray), optional - Testing feature data. Default None.
            y_test: (np.ndarray), optional - Testing target data. Default None.
            custom_metrics: (dict: str -> callable), optional - Custom metrics.
            verbose: (bool), optional - If True, prints progress. Default False.

        Returns:
            results: (list) - Performance metrics for each model.
            predictions: (dict) - Predictions for each model on the test/train set.
        """
        # --- Input Validation (as before) ---
        if not isinstance(X_train, np.ndarray) or not isinstance(y_train, np.ndarray):
            raise TypeError("X_train and y_train must be NumPy arrays.")
        if X_train.size == 0 or y_train.size == 0:
            raise ValueError("X_train and y_train cannot be empty.")
        if len(X_train) != len(y_train):
            raise ValueError(
                "X_train and y_train must have the same number of samples."
            )
        # Check for NaN/inf
        if np.any(np.isnan(X_train)) or np.any(np.isnan(y_train)):
            raise ValueError("X_train and y_train cannot contain NaN values.")
        if np.any(np.isinf(X_train)) or np.any(np.isinf(y_train)):
            raise ValueError("X_train and y_train cannot contain infinite values.")

        # Determine direction for tuning metric optimization
        if self.tuning_metric in ["r2", "r_squared"]:
            tuning_direction = "maximize"
        elif self.tuning_metric in [
            "mse",
            "mean_squared_error",
            "rmse",
            "root_mean_squared_error",
            "mae",
            "mean_absolute_error",
            "mape",
            "mean_absolute_percentage_error",
            "neg_mean_squared_error",
        ]:
            tuning_direction = "minimize"
            # Handle neg_mean_squared_error internally if needed by search CV
            if self.tuning_metric == "neg_mean_squared_error":
                self.tuning_metric = (
                    "mse"  # Use mse for calculation, direction handles minimization
                )
        else:
            warnings.warn(
                f"Unknown tuning_metric '{self.tuning_metric}'. Defaulting to maximization.",
                stacklevel=2,
            )
            tuning_direction = "maximize"

        # Reset results and predictions
        self.results = []
        self.predictions = {}
        self.tuning_results = {}

        # --- Handle NN Initialization & Scaling ---
        scaler_X_nn, scaler_y_nn = None, None
        X_train_nn_scaled, y_train_nn_scaled = (
            X_train,
            y_train,
        )  # Default to original if NN fails/skipped
        X_test_nn_scaled = X_test
        y_test_nn_scaled = y_test
        if (
            "BaseBackendNeuralNetwork" in self.models
            and self.models["BaseBackendNeuralNetwork"] is None
        ):
            try:
                input_size = X_train.shape[1]
                output_size = 1  # Regression
                layers = [128, 64]  # Default hidden layers
                activations = ["relu"] * len(layers) + [
                    "none"
                ]  # Linear output for regression
                self.models["BaseBackendNeuralNetwork"] = BaseBackendNeuralNetwork(
                    [input_size] + layers + [output_size],
                    dropout_rate=0.1,
                    reg_lambda=0.01,
                    activations=activations,
                    loss_function=MeanSquaredErrorLoss(),  # Default to MSE
                    regressor=True,
                )
                # Prepare scaled data *only* for NN
                scaler_X_nn = Scaler(method="standard")
                X_train_nn_scaled = scaler_X_nn.fit_transform(X_train)
                if X_test is not None:
                    X_test_nn_scaled = scaler_X_nn.transform(X_test)

                scaler_y_nn = Scaler(method="standard")
                # Reshape y if it's 1D
                y_train_reshaped = (
                    y_train.reshape(-1, 1) if y_train.ndim == 1 else y_train
                )
                y_train_nn_scaled = scaler_y_nn.fit_transform(
                    y_train_reshaped
                ).flatten()
                if y_test is not None:
                    y_test_reshaped = (
                        y_test.reshape(-1, 1) if y_test.ndim == 1 else y_test
                    )
                    y_test_nn_scaled = scaler_y_nn.transform(y_test_reshaped).flatten()

            except Exception as e:
                warnings.warn(
                    f"Could not initialize BaseBackendNeuralNetwork: {e}. Skipping NN.",
                    stacklevel=2,
                )
                if "BaseBackendNeuralNetwork" in self.models:
                    del self.models["BaseBackendNeuralNetwork"]  # Remove if init fails

        # --- Model Fitting Loop ---
        model_items = list(self.models.items())  # Use list to allow modification
        progress_bar = (
            tqdm(
                model_items,
                desc="Fitting Models",
                disable=not verbose or not TQDM_AVAILABLE,
            )
            if TQDM_AVAILABLE
            else model_items
        )
        for name, model_instance in progress_bar:
            if TQDM_AVAILABLE:
                progress_bar.set_description(f"Processing {name}")

            start_time = time.time()
            model_to_fit = model_instance
            best_params_tuning = None
            best_score_tuning = None

            # --- Hyperparameter Tuning ---
            # Exclude NN from generic tuning loop
            excluded_from_tuning = ["BaseBackendNeuralNetwork"]
            if (
                self.tune_hyperparameters
                and name in self._param_grids
                and name not in excluded_from_tuning
            ):
                if verbose and not TQDM_AVAILABLE:
                    print(f"\n  Tuning {name}...")

                # Define search space and method
                param_grid = self._param_grids[name]
                model_class = self._model_classes_map[name]

                SearchClass = (
                    RandomSearchCV if self.tuning_method == "random" else GridSearchCV
                )
                search_kwargs = {
                    "model": model_class,
                    "param_grid": param_grid,
                    "cv": self.cv,
                    "metric": self.tuning_metric,
                    "direction": tuning_direction,
                }
                if self.tuning_method == "random":
                    search_kwargs["iter"] = self.tuning_iterations

                # --- Try CV Search ---
                try:
                    search = SearchClass(**search_kwargs)
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        best_model_tuned = search.fit(X_train, y_train, verbose=False)

                    if hasattr(search, "best_model") and search.best_model is not None:
                        model_to_fit = best_model_tuned
                        best_params_tuning = search.best_params_
                        best_score_tuning = search.best_score_
                        self.models[name] = model_to_fit
                        self.tuning_results[name] = {
                            "best_score": best_score_tuning,
                            "best_params": best_params_tuning,
                            "method": self.tuning_method,
                        }
                        if verbose and TQDM_AVAILABLE:
                            tqdm.write(
                                f"    Best {name} params: {best_params_tuning}, Score ({self.tuning_metric}): {best_score_tuning:.4f}"
                            )
                        elif verbose:
                            print(
                                f"    Best {name} params: {best_params_tuning}, Score ({self.tuning_metric}): {best_score_tuning:.4f}"
                            )
                    else:
                        if verbose and TQDM_AVAILABLE:
                            tqdm.write(
                                f"    Tuning failed for {name}, using default parameters."
                            )
                        elif verbose:
                            print(
                                f"    Tuning failed for {name}, using default parameters."
                            )

                except Exception as e:
                    warnings.warn(
                        f"Hyperparameter tuning failed for {name}: {e}. Using default parameters.",
                        stacklevel=2,
                    )

            # --- Model Fitting (using default or tuned model) ---
            if model_to_fit is not None:
                try:
                    # Special handling for NN train method signature and scaled data
                    if name == "BaseBackendNeuralNetwork":
                        optimizer_nn = AdamOptimizer(
                            learning_rate=0.001
                        )  # Default for auto
                        # Use scaled data
                        X_train_current = X_train_nn_scaled
                        y_train_current = y_train_nn_scaled
                        X_test_current = X_test_nn_scaled
                        y_test_current = y_test_nn_scaled
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            model_to_fit.train(
                                X_train_current,
                                y_train_current,
                                X_val=X_test_current,
                                y_val=y_test_current,
                                optimizer=optimizer_nn,
                                epochs=50,
                                batch_size=32,
                                early_stopping_threshold=5,
                                p=False,
                                use_tqdm=False,
                            )
                    elif hasattr(model_to_fit, "fit") and callable(model_to_fit.fit):
                        # If model is GradientBoostedRegressor, reinit with parameters (if tuned)
                        if name == "GradientBoostedRegressor":
                            if best_params_tuning:
                                model_to_fit = GradientBoostedRegressor(
                                    **best_params_tuning
                                )
                            else:
                                model_to_fit = GradientBoostedRegressor()
                        model_to_fit.fit(X_train, y_train)
                    else:
                        raise TypeError(
                            f"Model {name} does not have a callable 'fit' method."
                        )

                except Exception as e:
                    warnings.warn(
                        f"Fitting failed for {name}: {e}. Skipping model.",
                        stacklevel=2,
                    )
                    self.results.append(
                        {
                            "Model": name,
                            "Error": str(e),
                            "Time Taken": time.time() - start_time,
                        }
                    )
                    continue

                # --- Prediction & Evaluation ---
                try:
                    # Use test set if available, otherwise train set for evaluation
                    eval_X = X_test if X_test is not None else X_train
                    eval_y = y_test if y_test is not None else y_train

                    # Use scaled data for NN prediction, then inverse transform
                    if name == "BaseBackendNeuralNetwork":
                        eval_X_current = (
                            X_test_nn_scaled
                            if X_test is not None
                            else X_train_nn_scaled
                        )
                        y_pred_scaled = model_to_fit.predict(eval_X_current)
                        # Inverse transform predictions
                        if scaler_y_nn:
                            y_pred = scaler_y_nn.inverse_transform(
                                y_pred_scaled.reshape(-1, 1)
                            ).flatten()
                        else:
                            y_pred = (
                                y_pred_scaled  # Should not happen if scaling worked
                            )
                        # Store train reference for scaler
                        self.X_train_ref = X_train
                        self.y_train_ref = y_train
                    else:
                        y_pred = model_to_fit.predict(eval_X)

                    self.predictions[name] = y_pred
                    elapsed_time = time.time() - start_time

                    metrics = {}
                    if custom_metrics:
                        for metric_name, metric_func in custom_metrics.items():
                            try:
                                metrics[metric_name] = metric_func(eval_y, y_pred)
                            except Exception as e:
                                metrics[metric_name] = f"Error: {e}"
                    else:
                        try:
                            metrics["R-Squared"] = r_squared(eval_y, y_pred)
                        except Exception as _e:
                            metrics["R-Squared"] = "N/A"
                        try:
                            metrics["RMSE"] = root_mean_squared_error(eval_y, y_pred)
                        except Exception as _e:
                            metrics["RMSE"] = "N/A"
                        try:
                            metrics["MAPE"] = mean_absolute_percentage_error(
                                eval_y, y_pred
                            )
                        except Exception as _e:
                            metrics["MAPE"] = "N/A"

                    tuning_info = self.tuning_results.get(name, {})
                    self.results.append(
                        {
                            "Model": name,
                            **metrics,
                            "Time Taken": elapsed_time,
                            "Tuned": name in self.tuning_results,
                            "Best Score (Tuning)": tuning_info.get("best_score"),
                            "Best Params (Tuning)": tuning_info.get("best_params"),
                        }
                    )

                except Exception as e:
                    warnings.warn(
                        f"Prediction or evaluation failed for {name}: {e}. Skipping metrics.",
                        stacklevel=2,
                    )
                    self.results.append(
                        {
                            "Model": name,
                            "Error": f"Eval Error: {e}",
                            "Time Taken": time.time() - start_time,
                        }
                    )
            else:  # Model instance was None
                self.results.append(
                    {"Model": name, "Error": "Model not initialized", "Time Taken": 0}
                )

            # If last model in loop and progress bar is available
            if TQDM_AVAILABLE and name == model_items[-1][0]:
                progress_bar.set_description("All models processed")

        if TQDM_AVAILABLE and progress_bar:
            progress_bar.set_description("Fitting Completed")

        return self.results, self.predictions

    def predict(self, X, model=None):
        """Generates predictions using fitted models.

        Args:
            X: (np.ndarray) - Input feature data.
            model: (str), optional - Specific model name. Default None (predict with all).

        Returns:
            dict or np.ndarray: Predictions for specified model(s).
        """
        if not self.results:  # Check if fit was called by checking results
            raise ValueError("No models have been fitted yet. Call fit() first.")

        if model:
            if model not in self.models:
                raise ValueError(f"Model '{model}' not found or not fitted.")
            fitted_model_instance = self.models.get(model)
            if fitted_model_instance is None:
                raise ValueError(
                    f"Fitted instance for model '{model}' not found (initialization or fitting might have failed)."
                )

            # Handle NN scaling for prediction
            if model == "BaseBackendNeuralNetwork":
                scaler_X_nn = Scaler(method="standard")
                scaler_X_nn.fit(
                    self.X_train_ref
                )  # Assuming X_train was stored or accessible
                X_scaled = scaler_X_nn.transform(X)
                y_pred_scaled = fitted_model_instance.predict(X_scaled)
                # Inverse transform if scaler is available
                scaler_y_nn = Scaler(method="standard")
                scaler_y_nn.fit(
                    self.y_train_ref.reshape(-1, 1)
                )  # Assuming y_train was stored
                if scaler_y_nn:
                    return scaler_y_nn.inverse_transform(
                        y_pred_scaled.reshape(-1, 1)
                    ).flatten()
                else:
                    return y_pred_scaled  # Return scaled if scaler unavailable (warning needed?)
            else:
                return fitted_model_instance.predict(X)

        # Predict with all models
        all_predictions = {}
        for name, fitted_instance in self.models.items():
            if fitted_instance is not None:  # Check instance exists
                try:
                    if name == "BaseBackendNeuralNetwork":
                        scaler_X_nn = Scaler(method="standard")
                        scaler_X_nn.fit(
                            self.X_train_ref
                        )  # Need reference to original X_train
                        X_scaled = scaler_X_nn.transform(X)
                        y_pred_scaled = fitted_instance.predict(X_scaled)
                        scaler_y_nn = Scaler(method="standard")
                        scaler_y_nn.fit(
                            self.y_train_ref.reshape(-1, 1)
                        )  # Need reference to original y_train
                        if scaler_y_nn:
                            all_predictions[name] = scaler_y_nn.inverse_transform(
                                y_pred_scaled.reshape(-1, 1)
                            ).flatten()
                        else:
                            all_predictions[name] = y_pred_scaled  # Fallback
                    else:
                        all_predictions[name] = fitted_instance.predict(X)
                except Exception as e:
                    warnings.warn(
                        f"Prediction failed for {name} during multi-predict: {e}",
                        stacklevel=2,
                    )
                    all_predictions[name] = f"Prediction Error: {e}"
        return all_predictions

    def evaluate(self, y_true, custom_metrics=None, model=None):
        """Evaluates performance using stored predictions.

        Args:
            y_true: (np.ndarray) - True target values.
            custom_metrics: (dict), optional - Custom metrics. Default None.
            model: (str), optional - Specific model name. Default None (evaluate all).

        Returns:
            dict: Evaluation metrics.
        """
        if not self.predictions:
            raise ValueError("No predictions available. Call fit() first.")

        evaluation_results = {}
        models_to_evaluate = list(self.predictions.keys()) if model is None else [model]

        if model and model not in self.predictions:
            raise ValueError(
                f"Predictions for model '{model}' not found. Ensure it was fitted."
            )

        for name in models_to_evaluate:
            if name not in self.predictions:
                warnings.warn(
                    f"Predictions for {name} missing, skipping evaluation.",
                    stacklevel=2,
                )
                continue

            y_pred = self.predictions[name]
            if not isinstance(y_pred, np.ndarray):
                evaluation_results[name] = {"Error": "Prediction failed during fit"}
                continue

            metrics = {}
            if custom_metrics:
                for metric_name, metric_func in custom_metrics.items():
                    try:
                        metrics[metric_name] = metric_func(y_true, y_pred)
                    except Exception as e:
                        metrics[metric_name] = f"Error: {e}"
            else:
                # Default regression metrics
                try:
                    metrics["R-Squared"] = r_squared(y_true, y_pred)
                except Exception as _e:
                    metrics["R-Squared"] = "N/A"
                try:
                    metrics["RMSE"] = root_mean_squared_error(y_true, y_pred)
                except Exception as _e:
                    metrics["RMSE"] = "N/A"
                try:
                    metrics["MAPE"] = mean_absolute_percentage_error(y_true, y_pred)
                except Exception as _e:
                    metrics["MAPE"] = "N/A"

            evaluation_results[name] = metrics

        return evaluation_results

    def get_model(self, model_name):
        """Returns the final fitted model instance (potentially tuned)."""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found.")
        model_instance = self.models.get(model_name)
        if model_instance is None:
            raise ValueError(
                f"Model '{model_name}' instance is None (initialization or fitting might have failed)."
            )
        # Basic check if fitted
        if not (
            hasattr(model_instance, "fit")
            and (
                hasattr(model_instance, "w")
                or hasattr(model_instance, "coef_")
                or hasattr(model_instance, "best_fit")
                or hasattr(model_instance, "trees")
                or hasattr(model_instance, "layer_outputs")
            )
        ):
            warnings.warn(
                f"Model '{model_name}' is available but may not be fitted.",
                stacklevel=2,
            )
        return model_instance

    def summary(self):
        """Prints a summary of model performance, including tuning results."""
        if not self.results:
            print("No models have been fitted or evaluated yet.")
            return

        # --- Dynamic metric extraction and sorting ---
        non_metric_keys = {
            "Model",
            "Model Class",
            "Time Taken",
            "Error",
            "Tuned",
            "Best Score (Tuning)",
            "Best Params (Tuning)",
        }
        metric_keys = []
        if self.results:
            sample_result = next((r for r in self.results if "Error" not in r), None)
            if sample_result:
                metric_keys = [k for k in sample_result if k not in non_metric_keys]

        primary_metric = "R-Squared" if "R-Squared" in metric_keys else None
        secondary_metric = "RMSE" if "RMSE" in metric_keys else None  # Lower is better
        if not primary_metric and metric_keys:
            primary_metric = metric_keys[0]  # Fallback

        if primary_metric:
            sorted_results = sorted(
                self.results,
                key=lambda x: (
                    -x.get(primary_metric, float("-inf"))
                    if isinstance(x.get(primary_metric), (int, float))
                    else float("-inf"),  # Desc R2
                    x.get(secondary_metric, float("inf"))
                    if isinstance(x.get(secondary_metric), (int, float))
                    else float("inf"),  # Asc RMSE
                    x.get("Time Taken", float("inf")),  # Asc Time
                ),
            )
        else:
            sorted_results = sorted(
                self.results, key=lambda x: x.get("Time Taken", float("inf"))
            )

        # Add model type categorization
        for result in sorted_results:
            result["Model Class"] = self.model_types.get(result["Model"], "Unknown")

        # --- Tabulate Output ---
        try:
            from tabulate import tabulate

            headers = ["Model Class", "Model"] + metric_keys + ["Time Taken", "Tuned"]
            tuned_models_exist = any(r.get("Tuned", False) for r in sorted_results)
            if tuned_models_exist:
                headers.extend(["Best Score (Tuning)", "Best Params (Tuning)"])
            table_data = []
            for result in sorted_results:
                if "Error" in result:
                    row = (
                        [result.get("Model Class", "N/A"), result["Model"]]
                        + ["Error"] * len(metric_keys)
                        + [result.get("Time Taken", "N/A"), result.get("Tuned", "N/A")]
                    )
                    if tuned_models_exist:
                        row += ["N/A", f"Error: {result['Error']}"]
                else:
                    row = [result["Model Class"], result["Model"]]
                    for key in metric_keys:
                        val = result.get(key)
                        row.append(
                            f"{val:.4f}" if isinstance(val, (int, float)) else str(val)
                        )
                    row.append(
                        f"{result.get('Time Taken', 'N/A'):.4f}"
                        if isinstance(result.get("Time Taken"), (int, float))
                        else str(result.get("Time Taken", "N/A"))
                    )
                    row.append(result.get("Tuned", False))
                    if tuned_models_exist:
                        tuning_score = result.get("Best Score (Tuning)")
                        tuning_params = result.get("Best Params (Tuning)")
                        row.append(
                            f"{tuning_score:.4f}"
                            if isinstance(tuning_score, (int, float))
                            else "N/A"
                        )
                        params_str = str(tuning_params)
                        row.append(
                            params_str[:47] + "..."
                            if len(params_str) > 50
                            else params_str
                            if tuning_params
                            else "N/A"
                        )
                table_data.append(row)
            print("\n--- AutoRegressor Summary ---")
            print(tabulate(table_data, headers=headers, tablefmt="rounded_outline"))
        except Exception as _e:
            print(
                "\n--- AutoRegressor Summary (Install tabulate for better formatting) ---"
            )
            header_parts = (
                ["Model Class", "Model"] + metric_keys + ["Time Taken", "Tuned"]
            )
            if tuned_models_exist:
                header_parts.extend(["Best Score (Tune)", "Best Params (Tune)"])
            print(" | ".join(f"{h:<15}" for h in header_parts))
            print("-" * (len(header_parts) * 17))
            for result in sorted_results:
                row_parts = [
                    f"{result.get('Model Class', 'N/A'):<15}",
                    f"{result['Model']:<15}",
                ]
                if "Error" in result:
                    row_parts += [f"{'Error':<15}"] * len(metric_keys) + [
                        f"{str(result.get('Time Taken', 'N/A')):<15}",
                        f"{str(result.get('Tuned', False)):<15}",
                    ]
                    if tuned_models_exist:
                        row_parts += [f"{'N/A':<15}", f"{'Error':<15}"]
                else:
                    for key in metric_keys:
                        val = result.get(key)
                        row_parts.append(
                            f"{val:<15.4f}"
                            if isinstance(val, (int, float))
                            else f"{str(val):<15}"
                        )
                    row_parts.append(
                        f"{result.get('Time Taken', 'N/A'):<15.4f}"
                        if isinstance(result.get("Time Taken"), (int, float))
                        else f"{str(result.get('Time Taken', 'N/A')):<15}"
                    )
                    row_parts.append(f"{str(result.get('Tuned', False)):<15}")
                    if tuned_models_exist:
                        tuning_score = result.get("Best Score (Tuning)")
                        tuning_params = result.get("Best Params (Tuning)")
                        row_parts.append(
                            f"{tuning_score:<15.4f}"
                            if isinstance(tuning_score, (int, float))
                            else f"{'N/A':<15}"
                        )
                        params_str = str(tuning_params)
                        row_parts.append(
                            f"{params_str[:12] + '...' if len(params_str) > 15 else params_str if tuning_params else 'N/A':<15}"
                        )
                print(" | ".join(row_parts))
            print("---------------------------------")
