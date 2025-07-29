# sega_learn/auto/classifier.py
import time
import warnings

import numpy as np

try:
    from tqdm.auto import tqdm

    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

from sega_learn.utils.metrics import Metrics
from sega_learn.utils.modelSelection import (  # Import search methods
    GridSearchCV,
    RandomSearchCV,
)

from ..linear_models import LogisticRegression, Perceptron
from ..nearest_neighbors import KNeighborsClassifier
from ..neural_networks import AdamOptimizer, BaseBackendNeuralNetwork
from ..svm import GeneralizedSVC, LinearSVC, OneClassSVM
from ..trees import AdaBoostClassifier, ClassifierTree, RandomForestClassifier

# from ..linear_models import LogisticRegression, SGDClassifier # Uncomment if implemented

accuracy = Metrics.accuracy
precision = Metrics.precision
recall = Metrics.recall
f1 = Metrics.f1_score


class AutoClassifier:
    """A class to automatically select and evaluate the best classification model.

    Includes optional automated hyperparameter tuning using GridSearchCV or RandomSearchCV.
    """

    def __init__(
        self,
        all_kernels=False,
        tune_hyperparameters=False,
        tuning_method="random",  # 'random' or 'grid'
        tuning_iterations=10,  # For Random Search
        cv=3,  # Cross-validation folds for tuning
        tuning_metric="f1",  # Metric to optimize during tuning
    ):
        """Initializes the AutoClassifier.

        Args:
            all_kernels (bool): If True, include all SVM kernels. Default False.
            tune_hyperparameters (bool): If True, perform hyperparameter tuning. Default False.
            tuning_method (str): Method for tuning ('random' or 'grid'). Default 'random'.
            tuning_iterations (int): Number of iterations for Random Search. Default 10.
            cv (int): Number of cross-validation folds for tuning. Default 3.
            tuning_metric (str): Metric to optimize ('accuracy', 'precision', 'recall', 'f1'). Default 'f1'.
        """
        self.all_kernels = all_kernels
        self.tune_hyperparameters = tune_hyperparameters
        self.tuning_method = tuning_method
        self.tuning_iterations = tuning_iterations
        self.cv = cv
        self.tuning_metric = tuning_metric
        self.tuning_results = {}  # To store tuning outcomes

        # --- Default Models & Classes ---
        # Store model *classes* and their default *instances* separately
        self._model_classes_map = {
            # SVM
            "LinearSVC": LinearSVC,
            "GeneralizedSVC - Linear": GeneralizedSVC,
            # KNeighborsClassifier
            "KNeighborsClassifier": KNeighborsClassifier,
            # Trees
            "ClassifierTree": ClassifierTree,
            "RandomForestClassifier": RandomForestClassifier,
            "AdaBoostClassifier": AdaBoostClassifier,
            # Neural Networks (will be initialized in fit if needed)
            "BaseBackendNeuralNetwork": BaseBackendNeuralNetwork,
            # Linear Models
            "LogisticRegression": LogisticRegression,
            "Perceptron": Perceptron,
            # Add other classifiers here if needed
        }

        self._default_model_instances = {
            "LinearSVC": LinearSVC(),
            "GeneralizedSVC - Linear": GeneralizedSVC(kernel="linear"),
            "KNeighborsClassifier": KNeighborsClassifier(),
            "ClassifierTree": ClassifierTree(),
            "RandomForestClassifier": RandomForestClassifier(),
            "AdaBoostClassifier": AdaBoostClassifier(),
            "BaseBackendNeuralNetwork": None,  # Placeholder
            "LogisticRegression": LogisticRegression(),
            "Perceptron": Perceptron(),
        }

        self.model_types = {  # Categorization for summary
            "LinearSVC": "SVM",
            "GeneralizedSVC - Linear": "SVM",
            "GeneralizedSVC - RBF": "SVM",
            "GeneralizedSVC - Polynomial": "SVM",
            "OneClassSVM - Linear": "SVM",
            "OneClassSVM - RBF": "SVM",
            "OneClassSVM - Polynomial": "SVM",
            "KNeighborsClassifier": "Nearest Neighbors",
            "ClassifierTree": "Trees",
            "RandomForestClassifier": "Trees",
            "AdaBoostClassifier": "Trees",
            "BaseBackendNeuralNetwork": "Neural Networks",
            "LogisticRegression": "Linear Models",
            "Perceptron": "Linear Models",
        }

        # Add kernel variations if needed
        if self.all_kernels:
            self._model_classes_map["GeneralizedSVC - RBF"] = GeneralizedSVC
            self._model_classes_map["GeneralizedSVC - Polynomial"] = GeneralizedSVC
            self._default_model_instances["GeneralizedSVC - RBF"] = GeneralizedSVC(
                kernel="rbf"
            )
            self._default_model_instances["GeneralizedSVC - Polynomial"] = (
                GeneralizedSVC(kernel="poly")
            )

        # Models dictionary will store the *actual* model instances used (default or tuned)
        self.models = self._default_model_instances.copy()

        # --- Default Hyperparameter Search Spaces ---
        self._param_grids = {
            "LinearSVC": [
                {"C": [0.1, 1, 10, 100]},
                {"tol": [1e-4, 1e-3, 1e-2]},
                {"max_iter": [1000, 2000, 3000]},
                {"learning_rate": [0.001, 0.01, 0.1]},
            ],
            "GeneralizedSVC - Linear": [
                {"C": [0.1, 1, 10, 100]},
                {"tol": [1e-4, 1e-3, 1e-2]},
                {"max_iter": [1000, 2000, 3000]},
                {"learning_rate": [0.001, 0.01, 0.1]},
            ],
            "GeneralizedSVC - RBF": [
                {"C": [0.1, 1, 10, 100]},
                {"tol": [1e-4, 1e-3, 1e-2]},
                {"gamma": ["scale", "auto", 0.1, 1]},
                {"learning_rate": [0.001, 0.01, 0.1]},
            ],
            "GeneralizedSVC - Polynomial": [
                {"C": [0.1, 1, 10, 100]},
                {"tol": [1e-4, 1e-3, 1e-2]},
                {"degree": [2, 3, 4]},
                {"gamma": ["scale", "auto"]},
                {"learning_rate": [0.001, 0.01, 0.1]},
            ],
            "KNeighborsClassifier": [
                {"n_neighbors": [3, 5, 7, 9]},
                {"distance_metric": ["euclidean", "manhattan"]},
            ],
            "ClassifierTree": [{"max_depth": [5, 10, 15, 20, 25, 50]}],
            "RandomForestClassifier": [
                {"n_estimators": [50, 100, 200]},
                {"max_depth": [5, 10, 15]},
            ],
            "AdaBoostClassifier": [
                {"n_estimators": [50, 100, 200]},
                {"learning_rate": [0.001, 0.01, 0.1]},
                {"min_samples_split": [2, 5, 10]},
                {"max_depth": [1, 3, 5]},
            ],
            # Note: OneClassSVM tuning is often complex/specific, adding basic grid for demonstration
            "OneClassSVM - Linear": [
                {"C": [0.1, 1, 10, 100]},
                {"tol": [1e-4, 1e-3, 1e-2]},
                {"max_iter": [1000, 2000, 3000]},
                {"learning_rate": [0.001, 0.01, 0.1]},
            ],
            "OneClassSVM - RBF": [
                {"C": [0.1, 1, 10, 100]},
                {"tol": [1e-4, 1e-3, 1e-2]},
                {"gamma": ["scale", "auto", 0.1, 1]},
                {"learning_rate": [0.001, 0.01, 0.1]},
            ],
            "OneClassSVM - Polynomial": [
                {"C": [0.1, 1, 10, 100]},
                {"tol": [1e-4, 1e-3, 1e-2]},
                {"degree": [2, 3, 4]},
                {"gamma": ["scale", "auto"]},
                {"learning_rate": [0.001, 0.01, 0.1]},
            ],
            "LogisticRegression": [
                {"learning_rate": [0.001, 0.01, 0.1]},
                {"max_iter": [1000, 2000, 3000]},
            ],
            "Perceptron": [
                {"learning_rate": [0.001, 0.01, 0.1]},
                {"max_iter": [1000, 2000, 3000]},
            ],
            # Add grids for other models here
        }
        # Note: Neural Network is excluded from this grid/random search tuning loop.

        self.predictions = {}
        self.results = []

    def fit(
        self,
        X_train,
        y_train,
        X_test=None,
        y_test=None,
        custom_metrics=None,
        verbose=False,
    ):
        """Fits the classification models, optionally performing hyperparameter tuning.

        Args:
            X_train: (np.ndarray) - Training feature data.
            y_train: (np.ndarray) - Training target data.
            X_test: (np.ndarray), optional - Testing feature data. Default None.
            y_test: (np.ndarray), optional - Testing target data. Default None.
            custom_metrics: (dict: str -> callable), optional - Custom metrics for evaluation.
            verbose: (bool), optional - If True, prints progress. Default False.

        Returns:
            results: (list) - A list of dictionaries containing model performance metrics.
            predictions: (dict) - A dictionary of predictions for each model on the test/train set.
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
        n_classes = len(np.unique(y_train))
        if n_classes < 2:
            raise ValueError("y_train must contain at least two classes.")
        if np.any(np.isnan(X_train)) or np.any(np.isnan(y_train)):
            raise ValueError("X_train and y_train cannot contain NaN values.")
        if np.any(np.isinf(X_train)) or np.any(np.isinf(y_train)):
            raise ValueError("X_train and y_train cannot contain infinite values.")

        # Determine direction for tuning metric optimization
        tuning_direction = (
            "maximize"
            if self.tuning_metric in ["accuracy", "precision", "recall", "f1"]
            else "minimize"
        )

        # Reset results and predictions
        self.results = []
        self.predictions = {}
        self.tuning_results = {}

        # --- Handle NN Initialization ---
        if self.models["BaseBackendNeuralNetwork"] is None:
            try:
                input_size = X_train.shape[1]
                # Ensure output_size matches number of classes
                output_size = n_classes if n_classes > 2 else 1
                layers = [128, 64, 32]  # Default hidden layers
                activations = ["relu"] * len(layers) + [
                    "softmax" if n_classes > 2 else "sigmoid"
                ]
                self.models["BaseBackendNeuralNetwork"] = BaseBackendNeuralNetwork(
                    [input_size] + layers + [output_size],
                    dropout_rate=0.1,
                    reg_lambda=0.0,
                    activations=activations,
                )
            except Exception as e:
                warnings.warn(
                    f"Could not initialize BaseBackendNeuralNetwork: {e}. Skipping NN.",
                    stacklevel=2,
                )
                if "BaseBackendNeuralNetwork" in self.models:
                    del self.models["BaseBackendNeuralNetwork"]  # Remove if init fails

        # --- Handle OneClassSVM ---
        one_class_models = {}
        if n_classes == 2:
            one_class_models["OneClassSVM - Linear"] = OneClassSVM(kernel="linear")
            self._model_classes_map["OneClassSVM - Linear"] = OneClassSVM
            if self.all_kernels:
                one_class_models["OneClassSVM - RBF"] = OneClassSVM(kernel="rbf")
                self._model_classes_map["OneClassSVM - RBF"] = OneClassSVM
                one_class_models["OneClassSVM - Polynomial"] = OneClassSVM(
                    kernel="poly"
                )
                self._model_classes_map["OneClassSVM - Polynomial"] = OneClassSVM
            # Add OneClassSVM models to the main models dict for this run
            self.models.update(one_class_models)
        else:
            # Remove OneClassSVM if it exists and not binary
            for key in list(self.models.keys()):
                if "OneClassSVM" in key:
                    del self.models[key]

        # --- Model Fitting Loop ---
        model_items = list(
            self.models.items()
        )  # Use list to allow modification during iteration if needed
        progress_bar = (
            tqdm(
                model_items,
                desc="Fitting Models",
                disable=not verbose or not TQDM_AVAILABLE,
            )
            if TQDM_AVAILABLE
            else model_items
        )

        for (
            name,
            model_instance,
        ) in progress_bar:  # model_instance is the default instance
            if TQDM_AVAILABLE:
                progress_bar.set_description(f"Processing {name}")

            start_time = time.time()
            model_to_fit = model_instance  # Start with the default instance
            best_params_tuning = None
            best_score_tuning = None

            # --- Hyperparameter Tuning ---
            if (
                self.tune_hyperparameters
                and name in self._param_grids
                and name != "BaseBackendNeuralNetwork"
            ):
                if verbose and not TQDM_AVAILABLE:
                    print(f"\n  Tuning {name}...")

                param_grid = self._param_grids[name]
                model_class = self._model_classes_map[name]  # Get the class

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

                try:
                    search = SearchClass(**search_kwargs)
                    with (
                        warnings.catch_warnings()
                    ):  # Suppress potential internal warnings during search
                        warnings.simplefilter("ignore")
                        best_model_tuned = search.fit(
                            X_train, y_train, verbose=False
                        )  # Fit the search

                    # Check if tuning actually found a model
                    if hasattr(search, "best_model") and search.best_model is not None:
                        model_to_fit = (
                            best_model_tuned  # Use the best tuned model instance
                        )
                        best_params_tuning = search.best_params_
                        best_score_tuning = search.best_score_
                        self.models[name] = (
                            model_to_fit  # Update the stored model instance
                        )
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
                        # Keep model_to_fit as the default instance

                except Exception as e:
                    warnings.warn(
                        f"Hyperparameter tuning failed for {name}: {e}. Using default parameters.",
                        stacklevel=2,
                    )
                    # Keep model_to_fit as the default instance

            # --- Model Fitting (using default or tuned model) ---
            if (
                model_to_fit is not None
            ):  # Check if model exists (e.g., NN might fail init)
                try:
                    # Special handling for NN train method signature
                    if name == "BaseBackendNeuralNetwork":
                        # Basic NN training for Auto module - no extensive tuning here
                        optimizer = AdamOptimizer(learning_rate=0.001)
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            model_to_fit.train(
                                X_train,
                                y_train,
                                X_val=X_test,
                                y_val=y_test,
                                optimizer=optimizer,
                                epochs=50,
                                batch_size=32,  # Fixed short training
                                early_stopping_threshold=5,
                                p=False,
                                use_tqdm=False,
                            )
                        # Store the fitted model instance
                        self.models[name] = model_to_fit
                    elif hasattr(model_to_fit, "fit") and callable(model_to_fit.fit):
                        # Standard fit method for most models
                        model_to_fit.fit(X_train, y_train)
                        # Store the fitted model instance
                        self.models[name] = model_to_fit
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
                    continue  # Skip to next model

                # --- Prediction & Evaluation ---
                try:
                    # Use test set if available, otherwise train set for evaluation
                    eval_X = X_test if X_test is not None else X_train
                    eval_y = y_test if y_test is not None else y_train

                    y_pred = model_to_fit.predict(eval_X)
                    # Ensure predictions are in the expected format (np.ndarray) (flatten if needed)
                    self.predictions[name] = np.array(y_pred).flatten()
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
                            metrics["Accuracy"] = accuracy(eval_y, y_pred)
                        except Exception as _e:
                            metrics["Accuracy"] = "N/A"
                        try:
                            metrics["Precision"] = precision(eval_y, y_pred)
                        except Exception as _e:
                            metrics["Precision"] = "N/A"
                        try:
                            metrics["Recall"] = recall(eval_y, y_pred)
                        except Exception as _e:
                            metrics["Recall"] = "N/A"
                        try:
                            metrics["F1 Score"] = f1(eval_y, y_pred)
                        except Exception as _e:
                            metrics["F1 Score"] = "N/A"

                    # Add tuning info to results if available
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

            else:  # If model_to_fit is None (e.g. failed NN init)
                self.results.append(
                    {"Model": name, "Error": "Model not initialized", "Time Taken": 0}
                )

            # If last model in loop and progress bar is available
            if TQDM_AVAILABLE and name == model_items[-1][0]:
                progress_bar.set_description("All models processed")

        if TQDM_AVAILABLE and progress_bar:
            progress_bar.refresh()
            progress_bar.close()

        return self.results, self.predictions

    def predict(self, X, model=None):
        """Generates predictions using fitted models.

        Args:
            X: (np.ndarray) - Input feature data.
            model: (str), optional - Specific model name. Default None (predict with all).

        Returns:
            dict or np.ndarray: Predictions for specified model(s).
        """
        if not self.predictions and not model:  # Check if fit was called
            raise ValueError("No models have been fitted yet. Call fit() first.")

        if model:
            if model not in self.models:  # Check if model name is valid
                raise ValueError(f"Model '{model}' not found or not fitted.")
            if (
                model not in self.predictions
            ):  # Check if prediction exists for this model
                raise ValueError(
                    f"Model '{model}' was fitted, but no predictions were stored. Predict might have failed."
                )
            # Need to get the *actual* fitted model instance (could be tuned)
            fitted_model_instance = None
            for res in self.results:
                if res["Model"] == model and "Error" not in res:
                    fitted_model_instance = self.models.get(
                        model
                    )  # Fetch the final fitted model instance
                    if fitted_model_instance:
                        return fitted_model_instance.predict(X)
                    else:
                        raise ValueError(
                            f"Fitted instance for model '{model}' not found."
                        )
            if fitted_model_instance is None:
                raise ValueError(
                    f"Could not retrieve fitted instance or stored predictions for model '{model}'."
                )

        # Predict with all models that have stored predictions
        all_predictions = {}
        for name, fitted_instance in self.models.items():
            if (
                name in self.predictions and fitted_instance is not None
            ):  # Check if predictions exist and model instance is valid
                try:
                    all_predictions[name] = np.array(
                        fitted_instance.predict(X)
                    ).flatten()
                except Exception as e:
                    warnings.warn(
                        f"Prediction failed for {name} during multi-predict: {e}",
                        stacklevel=2,
                    )
                    all_predictions[name] = f"Prediction Error: {e}"
        return all_predictions

    def evaluate(self, y_true, custom_metrics=None, model=None):
        """Evaluates the performance using stored predictions.

        Args:
            y_true: (np.ndarray) - True target values.
            custom_metrics: (dict), optional - Custom metrics. Default None.
            model: (str), optional - Specific model name. Default None (evaluate all).

        Returns:
            dict: Evaluation metrics for the specified model(s).
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
            if (
                name not in self.predictions
            ):  # Should not happen if logic is correct, but safe check
                warnings.warn(
                    f"Predictions for {name} missing, skipping evaluation.",
                    stacklevel=2,
                )
                continue

            y_pred = self.predictions[name]
            # Ensure y_pred is usable (not an error string from predict step)
            if not isinstance(y_pred, np.ndarray):
                print(f"y_pred is type: {type(y_pred)}")
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
                # Default classification metrics
                try:
                    metrics["Accuracy"] = accuracy(y_true, y_pred)
                except Exception as _e:
                    metrics["Accuracy"] = "N/A"
                try:
                    metrics["Precision"] = precision(y_true, y_pred)
                except Exception as _e:
                    metrics["Precision"] = "N/A"
                try:
                    metrics["Recall"] = recall(y_true, y_pred)
                except Exception as _e:
                    metrics["Recall"] = "N/A"
                try:
                    metrics["F1 Score"] = f1(y_true, y_pred)
                except Exception as _e:
                    metrics["F1 Score"] = "N/A"

            evaluation_results[name] = metrics

        return evaluation_results

    def get_model(self, model_name):
        """Returns the final fitted model instance (potentially tuned).

        Args:
            model_name (str): The name of the model.

        Returns:
            model_instance: The fitted model instance.
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found.")
        # Return the instance stored in self.models, which is updated during tuning
        model_instance = self.models[model_name]
        if model_instance is None:
            raise ValueError(
                f"Model '{model_name}' instance is None (initialization or fitting might have failed)."
            )
        # Check if the model instance appears to be fitted (basic check)
        if not (
            hasattr(model_instance, "fit")
            and (
                hasattr(model_instance, "w")
                or hasattr(model_instance, "coef_")
                or hasattr(model_instance, "support_vectors_")
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
        """Prints a summary of model performance, including tuning results if available."""
        if not self.results:
            print("No models have been fitted or evaluated yet.")
            return

        # Extract all metric keys dynamically from the results, excluding non-metric keys
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

        # Sort results by primary metric (e.g., F1 Score or Accuracy), then Time Taken
        primary_metric = "F1 Score" if "F1 Score" in metric_keys else "Accuracy"
        if (
            primary_metric not in metric_keys
        ):  # Fallback if neither F1 nor Accuracy is present
            primary_metric = metric_keys[0] if metric_keys else None

        if primary_metric:
            sorted_results = sorted(
                self.results,
                key=lambda x: (
                    -x.get(primary_metric, float("-inf"))
                    if isinstance(x.get(primary_metric), (int, float))
                    else float("-inf"),  # Descending sort, handle N/A
                    x.get("Time Taken", float("inf")),  # Ascending Time Taken
                ),
            )
        else:
            sorted_results = sorted(
                self.results, key=lambda x: x.get("Time Taken", float("inf"))
            )  # Sort by time if no metrics

        # Add model type categorization
        for result in sorted_results:
            result["Model Class"] = self.model_types.get(result["Model"], "Unknown")

        try:
            from tabulate import tabulate

            headers = ["Model Class", "Model"] + metric_keys + ["Time Taken", "Tuned"]
            # Only add tuning columns if tuning was performed for at least one model
            tuned_models_exist = any(r.get("Tuned", False) for r in sorted_results)
            if tuned_models_exist:
                headers.extend(["Best Score (Tuning)", "Best Params (Tuning)"])

            table_data = []
            for result in sorted_results:
                if "Error" in result:
                    row = [result.get("Model Class", "N/A"), result["Model"]]
                    row += ["Error"] * len(metric_keys)  # Fill metric cells with Error
                    row += [result.get("Time Taken", "N/A"), result.get("Tuned", "N/A")]
                    if tuned_models_exist:
                        row += [
                            "N/A",
                            f"Error: {result['Error']}",
                        ]  # Add placeholders for tuning columns
                else:
                    row = [result["Model Class"], result["Model"]]
                    # Format metrics, handle N/A or errors gracefully
                    for key in metric_keys:
                        val = result.get(key)
                        if isinstance(val, (int, float)):
                            row.append(f"{val:.4f}")
                        else:
                            row.append(str(val))  # Display N/A or error string

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
                        # Limit param display length
                        params_str = str(tuning_params)
                        if len(params_str) > 50:
                            params_str = params_str[:47] + "..."
                        row.append(params_str if tuning_params else "N/A")

                table_data.append(row)

            print("\n--- AutoClassifier Summary ---")
            print(tabulate(table_data, headers=headers, tablefmt="rounded_outline"))

        except Exception as _e:
            print(
                "\n--- AutoClassifier Summary (Install tabulate for better formatting) ---"
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
                    row_parts += [f"{'Error':<15}"] * len(metric_keys)
                    row_parts += [
                        f"{result.get('Time Taken', 'N/A'):<15.4f}"
                        if isinstance(result.get("Time Taken"), (int, float))
                        else f"{str(result.get('Time Taken', 'N/A')):<15}",
                        f"{str(result.get('Tuned', False)):<15}",
                    ]
                    if tuned_models_exist:
                        row_parts += [f"{'N/A':<15}", f"{'Error':<15}"]
                else:
                    for key in metric_keys:
                        val = result.get(key)
                        if isinstance(val, (int, float)):
                            row_parts.append(f"{val:<15.4f}")
                        else:
                            row_parts.append(f"{str(val):<15}")

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
                        if len(params_str) > 15:
                            params_str = params_str[:12] + "..."
                        row_parts.append(
                            f"{params_str if tuning_params else 'N/A':<15}"
                        )

                print(" | ".join(row_parts))
            print("---------------------------------")
