import os
import sys
import unittest
import warnings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from sega_learn.auto import AutoClassifier, AutoRegressor
from sega_learn.linear_models import LogisticRegression, OrdinaryLeastSquares
from sega_learn.trees import ClassifierTree, RegressorTree
from sega_learn.utils import Metrics, make_classification, make_regression
from tests.utils import BaseTest, suppress_print

# Suppress warnings
warnings.filterwarnings(
    "ignore",
    message="Tried to use C compiled code, but failed. Using Python code instead.",
)

r2_score = Metrics.r_squared
accuracy_score = Metrics.accuracy


class TestAutoRegressor(BaseTest):
    """Unit test for the AutoRegressor class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the AutoRegressor class before each test method is run."""
        print("\nTesting AutoRegressor Model", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.model = AutoRegressor()
        self.hp_tuned_model_rand = AutoRegressor(
            all_kernels=True,
            tune_hyperparameters=True,
            tuning_method="random",
            tuning_iterations=2,
            cv=2,
            tuning_metric="r2",
        )
        self.hp_tuned_model_grid = AutoRegressor(
            all_kernels=True,
            tune_hyperparameters=True,
            tuning_method="grid",
            tuning_iterations=2,
            cv=2,
            tuning_metric="r2",
        )
        self.X_train, self.y_train = make_regression(n_samples=50, n_features=3)
        self.X_test, self.y_test = make_regression(n_samples=5, n_features=3)

        warnings.filterwarnings("ignore", category=RuntimeWarning)

    def test_initialization(self):
        """Test that the AutoRegressor initializes with the correct models."""
        self.assertIsInstance(self.model.models, dict)
        self.assertGreater(len(self.model.models), 0)

    def test_fit(self):
        """Test the fit method of AutoRegressor."""
        results, predictions = self.model.fit(
            self.X_train, self.y_train, self.X_test, self.y_test, verbose=False
        )
        self.assertIsInstance(results, list)
        self.assertIsInstance(predictions, dict)
        self.assertGreater(len(results), 0)
        self.assertGreater(len(predictions), 0)

    def test_predict(self):
        """Test the predict method of AutoRegressor."""
        self.model.fit(self.X_train, self.y_train, verbose=False)
        warnings.filterwarnings("ignore", category=UserWarning)
        predictions = self.model.predict(self.X_test)
        self.assertIsInstance(predictions, dict)
        self.assertEqual(len(predictions), len(self.model.models))

    def test_predict_specific_model(self):
        """Test prediction with a specific model."""
        self.model.fit(self.X_train, self.y_train, verbose=False)
        specific_model = list(self.model.models.keys())[0]
        prediction = self.model.predict(self.X_test, model=specific_model)
        self.assertIsInstance(prediction, np.ndarray)

    def test_evaluate(self):
        """Test the evaluate method of AutoRegressor."""
        self.model.fit(
            self.X_train, self.y_train, self.X_test, self.y_test, verbose=False
        )
        evaluation_results = self.model.evaluate(self.y_test)
        self.assertIsInstance(evaluation_results, dict)
        self.assertGreater(len(evaluation_results), 0)

    def test_get_model(self):
        """Test the get_model method of AutoRegressor."""
        specific_model = list(self.model.models.keys())[0]
        model_instance = self.model.get_model(specific_model)
        self.assertIsNotNone(model_instance)

    def test_summary(self):
        """Test the summary method of AutoRegressor."""
        self.model.fit(
            self.X_train, self.y_train, self.X_test, self.y_test, verbose=False
        )
        with suppress_print():
            self.model.summary()

    def test_empty_dataset(self):
        """Test behavior with an empty dataset."""
        with self.assertRaises(ValueError):
            self.model.fit(np.array([]), np.array([]))

    def test_mismatched_feature_target_lengths(self):
        """Test behavior when feature and target lengths do not match."""
        X_train = np.random.rand(10, 5)
        y_train = np.random.rand(8)  # Mismatched length
        with self.assertRaises(ValueError):
            self.model.fit(X_train, y_train)

    def test_invalid_model_name_in_predict(self):
        """Test predict method with an invalid model name."""
        self.model.fit(self.X_train, self.y_train, verbose=False)
        with self.assertRaises(ValueError):
            self.model.predict(self.X_test, model="InvalidModelName")

    def test_invalid_model_name_in_get_model(self):
        """Test get_model method with an invalid model name."""
        with self.assertRaises(ValueError):
            self.model.get_model("InvalidModelName")

    def test_no_fitted_models_in_evaluate(self):
        """Test evaluate method when no models have been fitted."""
        with self.assertRaises(ValueError):
            self.model.evaluate(self.y_test)

    def test_no_fitted_models_in_summary(self):
        """Test summary method when no models have been fitted."""
        with suppress_print():
            self.model.summary()  # Should not raise an exception but print a warning

    def test_fit_with_custom_metrics(self):
        """Test fit method with custom metrics."""

        def custom_metric(y_true, y_pred):
            return np.mean(np.abs(y_true - y_pred))  # Mean Absolute Error

        custom_metrics = {"MAE": custom_metric}
        results, _ = self.model.fit(
            self.X_train,
            self.y_train,
            self.X_test,
            self.y_test,
            custom_metrics=custom_metrics,
            verbose=False,
        )
        self.assertIn("MAE", results[0])

    def test_predict_before_fit(self):
        """Test predict method before any model is fitted."""
        with self.assertRaises(ValueError):
            self.model.predict(self.X_test)

    def test_evaluate_with_custom_metrics(self):
        """Test evaluate method with custom metrics."""
        self.model.fit(
            self.X_train, self.y_train, self.X_test, self.y_test, verbose=False
        )

        def custom_metric(y_true, y_pred):
            return np.mean(np.abs(y_true - y_pred))  # Mean Absolute Error

        custom_metrics = {"MAE": custom_metric}
        evaluation_results = self.model.evaluate(
            self.y_test, custom_metrics=custom_metrics
        )
        for model_name in evaluation_results:
            self.assertIn("MAE", evaluation_results[model_name])

    def test_invalid_input_types(self):
        """Test behavior when input data types are invalid."""
        with self.assertRaises(TypeError):
            self.model.fit("invalid_input", self.y_train)
        with self.assertRaises(TypeError):
            self.model.fit(self.X_train, "invalid_input")

    def test_nan_values_in_data(self):
        """Test behavior when data contains NaN values."""
        X_train = self.X_train.copy()
        X_train[0, 0] = np.nan  # Introduce NaN
        with self.assertRaises(ValueError):
            self.model.fit(X_train, self.y_train)

    def test_inf_values_in_data(self):
        """Test behavior when data contains infinite values."""
        X_train = self.X_train.copy()
        X_train[0, 0] = np.inf  # Introduce infinity
        with self.assertRaises(ValueError):
            self.model.fit(X_train, self.y_train)

    def test_single_sample(self):
        """Test behavior with a single sample."""
        X_train = np.random.rand(1, 5)  # Single sample
        y_train = np.random.rand(1)
        warnings.filterwarnings("ignore", category=UserWarning)
        self.model.fit(X_train, y_train)

    def test_single_feature(self):
        """Test behavior with a single feature."""
        X_train = np.random.rand(100, 1)  # Single feature
        y_train = np.random.rand(100)
        X_test = np.random.rand(50, 1)
        y_test = np.random.rand(50)
        results, predictions = self.model.fit(
            X_train, y_train, X_test, y_test, verbose=False
        )
        self.assertGreater(len(results), 0)
        self.assertGreater(len(predictions), 0)

    def test_hp_tuning_random(self):
        """Test hyperparameter tuning with random search."""
        models_to_test = {
            "OrdinaryLeastSquares": OrdinaryLeastSquares(),
            "RegressorTree": RegressorTree(),
        }
        self.hp_tuned_model_rand.models = models_to_test
        self.hp_tuned_model_rand.fit(self.X_train, self.y_train, verbose=False)
        with suppress_print():
            self.hp_tuned_model_rand.summary()
        self.assertIsNotNone(self.hp_tuned_model_rand.results)
        self.assertIsNotNone(self.hp_tuned_model_rand.predictions)

    def test_hp_tuning_grid(self):
        """Test hyperparameter tuning with grid search."""
        # Set models to subset for testing
        models_to_test = {
            "OrdinaryLeastSquares": OrdinaryLeastSquares(),
            "RegressorTree": RegressorTree(),
        }
        param_grids = {
            "OrdinaryLeastSquares": [{"fit_intercept": [True, False]}],
            "RegressorTree": [
                {"max_depth": [2, 3]},
                {"min_samples_split": [2, 3]},
            ],
        }
        self.hp_tuned_model_grid.models = models_to_test
        self._param_grids = param_grids
        with suppress_print():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.hp_tuned_model_grid.fit(self.X_train, self.y_train, verbose=False)
            self.hp_tuned_model_grid.summary()
        self.assertIsNotNone(self.hp_tuned_model_grid.results)
        self.assertIsNotNone(self.hp_tuned_model_grid.predictions)


class TestAutoClassifier(BaseTest):
    """Unit test for the AutoClassifier class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the AutoClassifier class before each test method is run."""
        print("\nTesting AutoClassifier Model", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.model = AutoClassifier()
        self.hp_tuned_model_rand = AutoClassifier(
            all_kernels=True,
            tune_hyperparameters=True,
            tuning_method="random",
            tuning_iterations=2,
            cv=2,
            tuning_metric="accuracy",
        )
        self.hp_tuned_model_grid = AutoClassifier(
            all_kernels=True,
            tune_hyperparameters=True,
            tuning_method="grid",
            tuning_iterations=2,
            cv=2,
            tuning_metric="accuracy",
        )
        self.X_train, self.y_train = make_classification(
            n_samples=50, n_features=5, n_classes=3
        )
        self.X_test, self.y_test = make_classification(
            n_samples=5, n_features=5, n_classes=3
        )

    def test_initialization(self):
        """Test that the AutoClassifier initializes with the correct models."""
        self.assertIsInstance(self.model.models, dict)
        self.assertGreater(len(self.model.models), 0)

    def test_fit(self):
        """Test the fit method of AutoClassifier."""
        models_to_test = {
            "LogisticRegression": LogisticRegression(),
            "ClassifierTree": ClassifierTree(),
            "BaseBackendNeuralNetwork": 1,
        }
        self.model.models = models_to_test
        with suppress_print():
            warnings.filterwarnings("ignore", category=UserWarning)
            results, predictions = self.model.fit(
                self.X_train, self.y_train, verbose=False
            )
        self.assertIsInstance(results, list)
        self.assertIsInstance(predictions, dict)
        self.assertGreater(len(results), 0)
        self.assertGreater(len(predictions), 0)

    def test_predict(self):
        """Test the predict method of AutoClassifier."""
        models_to_test = {
            "LogisticRegression": LogisticRegression(),
            "ClassifierTree": ClassifierTree(),
            "BaseBackendNeuralNetwork": 1,
        }
        self.model.models = models_to_test
        with suppress_print():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.model.fit(self.X_train, self.y_train, verbose=False)
        predictions = self.model.predict(self.X_test)
        self.assertIsInstance(predictions, dict)
        self.assertEqual(
            len(predictions), len(self.model.models) - 1
        )  # Skip BaseBackendNeuralNetwork

    def test_predict_specific_model(self):
        """Test prediction with a specific model."""
        models_to_test = {
            "LogisticRegression": LogisticRegression(),
            "ClassifierTree": ClassifierTree(),
            "BaseBackendNeuralNetwork": 1,
        }
        self.model.models = models_to_test
        with suppress_print():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.model.fit(self.X_train, self.y_train, verbose=False)
        specific_model = list(self.model.models.keys())[0]
        prediction = self.model.predict(self.X_test, model=specific_model)
        self.assertIsInstance(prediction, np.ndarray)

    def test_evaluate(self):
        """Test the evaluate method of AutoClassifier."""
        models_to_test = {
            "LogisticRegression": LogisticRegression(),
            "ClassifierTree": ClassifierTree(),
            "BaseBackendNeuralNetwork": 1,
        }
        self.model.models = models_to_test
        with suppress_print():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.model.fit(self.X_train, self.y_train, verbose=False)
        evaluation_results = self.model.evaluate(self.y_test)
        self.assertIsInstance(evaluation_results, dict)
        self.assertGreater(len(evaluation_results), 0)

    def test_summary(self):
        """Test the summary method of AutoClassifier."""
        self.model.fit(
            self.X_train, self.y_train, self.X_test, self.y_test, verbose=False
        )
        with suppress_print():
            self.model.summary()

    def test_empty_dataset(self):
        """Test behavior with an empty dataset."""
        with self.assertRaises(ValueError):
            self.model.fit(np.array([]), np.array([]))

    def test_mismatched_feature_target_lengths(self):
        """Test behavior when feature and target lengths do not match."""
        X_train = np.random.rand(10, 5)
        y_train = np.random.rand(8)  # Mismatched length
        with self.assertRaises(ValueError):
            self.model.fit(X_train, y_train)

    def test_invalid_model_name_in_predict(self):
        """Test predict method with an invalid model name."""
        self.model.fit(self.X_train, self.y_train, verbose=False)
        with self.assertRaises(ValueError):
            self.model.predict(self.X_test, model="InvalidModelName")

    def test_no_fitted_models_in_evaluate(self):
        """Test evaluate method when no models have been fitted."""
        with self.assertRaises(ValueError):
            self.model.evaluate(self.y_test)

    def test_fit_with_custom_metrics(self):
        """Test fit method with custom metrics."""

        def custom_metric(y_true, y_pred):
            return np.mean(y_true == y_pred)  # Custom accuracy

        custom_metrics = {"Custom Accuracy": custom_metric}
        results, _ = self.model.fit(
            self.X_train,
            self.y_train,
            self.X_test,
            self.y_test,
            custom_metrics=custom_metrics,
            verbose=False,
        )
        self.assertIn("Custom Accuracy", results[0])

    def test_evaluate_with_custom_metrics(self):
        """Test evaluate method with custom metrics."""
        models_to_test = {
            "LogisticRegression": LogisticRegression(),
            "ClassifierTree": ClassifierTree(),
            "BaseBackendNeuralNetwork": 1,
        }
        self.model.models = models_to_test
        with suppress_print():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.model.fit(self.X_train, self.y_train, verbose=False)

        def custom_metric(y_true, y_pred):
            return np.mean(y_true == y_pred)  # Custom accuracy

        custom_metrics = {"Custom Accuracy": custom_metric}
        evaluation_results = self.model.evaluate(
            self.y_test, custom_metrics=custom_metrics
        )
        for model_name in evaluation_results:
            self.assertIn("Custom Accuracy", evaluation_results[model_name])

    def test_invalid_input_types(self):
        """Test behavior when input data types are invalid."""
        with self.assertRaises(TypeError):
            self.model.fit("invalid_input", self.y_train)
        with self.assertRaises(TypeError):
            self.model.fit(self.X_train, "invalid_input")

    def test_nan_values_in_data(self):
        """Test behavior when data contains NaN values."""
        X_train = self.X_train.copy()
        X_train[0, 0] = np.nan  # Introduce NaN
        with self.assertRaises(ValueError):
            self.model.fit(X_train, self.y_train)

    def test_inf_values_in_data(self):
        """Test behavior when data contains infinite values."""
        X_train = self.X_train.copy()
        X_train[0, 0] = np.inf  # Introduce infinity
        with self.assertRaises(ValueError):
            self.model.fit(X_train, self.y_train)

    def test_single_sample(self):
        """Test behavior with a single sample."""
        X_train = np.random.rand(1, 5)  # Single sample
        y_train = np.random.randint(0, 3, size=1)
        with self.assertRaises(ValueError):
            self.model.fit(X_train, y_train)

    def test_single_feature(self):
        """Test behavior with a single feature."""
        X_train = np.random.rand(100, 1)  # Single feature
        y_train = np.random.randint(0, 3, size=100)
        X_test = np.random.rand(50, 1)
        y_test = np.random.randint(0, 3, size=50)
        results, predictions = self.model.fit(
            X_train, y_train, X_test, y_test, verbose=False
        )
        self.assertGreater(len(results), 0)
        self.assertGreater(len(predictions), 0)

    def test_hp_tuning_random(self):
        """Test hyperparameter tuning with random search."""
        models_to_test = {
            "LogisticRegression": LogisticRegression(),
            "ClassifierTree": ClassifierTree(),
            "BaseBackendNeuralNetwork": 1,
        }
        self.hp_tuned_model_rand.models = models_to_test
        with suppress_print():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.hp_tuned_model_rand.fit(self.X_train, self.y_train, verbose=False)
            self.hp_tuned_model_rand.summary()
        self.assertIsNotNone(self.hp_tuned_model_rand.results)
        self.assertIsNotNone(self.hp_tuned_model_rand.predictions)

    def test_hp_tuning_grid(self):
        """Test hyperparameter tuning with grid search."""
        # Set models to subset for testing
        models_to_test = {
            "LogisticRegression": LogisticRegression(),
            "ClassifierTree": ClassifierTree(),
            "BaseBackendNeuralNetwork": 1,
        }
        param_grids = {
            "LogisticRegression": [
                {"learning_rate": [0.001, 0.01]},
                {"max_iter": [5]},
            ],
            "ClassifierTree": [
                {"max_depth": [2]},
                {"min_samples_split": [2, 3]},
            ],
        }
        self.hp_tuned_model_grid.models = models_to_test
        self._param_grids = param_grids
        with suppress_print():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.hp_tuned_model_grid.fit(self.X_train, self.y_train, verbose=False)
        self.assertIsNotNone(self.hp_tuned_model_grid.results)
        self.assertIsNotNone(self.hp_tuned_model_grid.predictions)


if __name__ == "__main__":
    unittest.main()
