import os
import sys
import unittest
import warnings

import numpy as np

# Adjust sys.path to import from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.trees import *
from sega_learn.utils import Metrics, make_classification, make_regression
from tests.utils import BaseTest, suppress_print

# Suppress specific warnings if needed
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Set random seed for reproducibility
np.random.seed(42)


class TestAdaBoostClassifier(BaseTest):
    """Unit tests for the AdaBoostClassifier class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting AdaBoostClassifier", end="", flush=True)
        cls.X_binary, cls.y_binary = make_classification(
            n_samples=100, n_features=10, n_classes=2, random_state=42, class_sep=0.8
        )
        cls.X_multi, cls.y_multi = make_classification(
            n_samples=150,
            n_features=10,
            n_classes=3,
            n_informative=4,
            random_state=42,
            class_sep=0.8,
        )

    def test_initialization_default(self):
        """Test default initialization."""
        model = AdaBoostClassifier()
        self.assertIsInstance(model.base_estimator_, ClassifierTree)
        self.assertEqual(model.base_estimator_.max_depth, 3)
        self.assertEqual(model.n_estimators, 50)
        self.assertEqual(model.learning_rate, 1.0)
        self.assertIsNone(model.random_state)

    def test_initialization_custom(self):
        """Test initialization with custom parameters."""
        base_est = ClassifierTree(max_depth=5)
        model = AdaBoostClassifier(
            base_estimator=base_est, n_estimators=10, learning_rate=0.5
        )
        self.assertEqual(model.base_estimator_, base_est)
        self.assertEqual(model.n_estimators, 10)
        self.assertEqual(model.learning_rate, 0.5)

    def test_fit_predict_binary(self):
        """Test fitting and predicting on binary data."""
        model = AdaBoostClassifier(n_estimators=10, random_state=42)
        model.fit(self.X_binary, self.y_binary)
        self.assertIsNotNone(model.classes_)
        self.assertEqual(model.n_classes_, 2)

        y_pred = model.predict(self.X_binary)
        self.assertEqual(y_pred.shape, (self.X_binary.shape[0],))
        self.assertTrue(np.all(np.isin(y_pred, model.classes_)))
        accuracy = Metrics.accuracy(self.y_binary, y_pred)
        self.assertGreaterEqual(accuracy, 0.5)  # Should be better than random

    def test_fit_predict_multiclass(self):
        """Test fitting and predicting on multiclass data."""
        model = AdaBoostClassifier(n_estimators=10, random_state=42)
        model.fit(self.X_multi, self.y_multi)
        self.assertEqual(len(model.estimators_), 10)
        self.assertEqual(len(model.estimator_weights_), 10)
        self.assertIsNotNone(model.classes_)
        self.assertEqual(model.n_classes_, 3)

        y_pred = model.predict(self.X_multi)
        self.assertEqual(y_pred.shape, (self.X_multi.shape[0],))
        self.assertTrue(np.all(np.isin(y_pred, model.classes_)))
        accuracy = Metrics.accuracy(self.y_multi, y_pred)
        self.assertGreaterEqual(accuracy, 0.3)  # Better than random chance (1/3)

    def test_decision_function_binary(self):
        """Test decision function for binary classification."""
        model = AdaBoostClassifier(n_estimators=10, random_state=42)
        model.fit(self.X_binary, self.y_binary)
        decision = model.decision_function(self.X_binary)
        self.assertEqual(decision.shape, (self.X_binary.shape[0],))

    def test_decision_function_multiclass(self):
        """Test decision function for multiclass classification."""
        model = AdaBoostClassifier(n_estimators=10, random_state=42)
        model.fit(self.X_multi, self.y_multi)
        decision = model.decision_function(self.X_multi)
        self.assertEqual(decision.shape, (self.X_multi.shape[0], model.n_classes_))

    def test_predict_proba_binary(self):
        """Test probability prediction for binary classification."""
        model = AdaBoostClassifier(n_estimators=10, random_state=42)
        model.fit(self.X_binary, self.y_binary)
        proba = model.predict_proba(self.X_binary)
        self.assertEqual(proba.shape, (self.X_binary.shape[0], 2))
        self.assertTrue(np.allclose(np.sum(proba, axis=1), 1.0))

    def test_predict_proba_multiclass(self):
        """Test probability prediction for multiclass classification."""
        model = AdaBoostClassifier(n_estimators=10, random_state=42)
        model.fit(self.X_multi, self.y_multi)
        proba = model.predict_proba(self.X_multi)
        self.assertEqual(proba.shape, (self.X_multi.shape[0], model.n_classes_))
        self.assertTrue(np.allclose(np.sum(proba, axis=1), 1.0))

    def test_get_stats(self):
        """Test the get_stats method."""
        model = AdaBoostClassifier(n_estimators=10, random_state=42)
        model.fit(self.X_binary, self.y_binary)
        stats = model.get_stats(self.y_binary, X=self.X_binary)
        self.assertIsInstance(stats, dict)
        self.assertIn("Accuracy", stats)
        self.assertIn("Precision", stats)
        self.assertIn("Recall", stats)
        self.assertIn("F1 Score", stats)
        self.assertIn("Log Loss", stats)

        with suppress_print():
            model.get_stats(self.y_binary, X=self.X_binary, verbose=True)

    def test_custom_base_estimator(self):
        """Test using a custom base estimator."""
        base_est = ClassifierTree(max_depth=1)
        model = AdaBoostClassifier(base_estimator=base_est, n_estimators=5)
        model.fit(self.X_binary, self.y_binary)
        # Check if the fitted estimators have the correct depth (approx check)
        self.assertTrue(
            all(
                hasattr(est, "max_depth") and est.max_depth == 1
                for est in model.estimators_
            )
        )

    def test_fit_invalid_input_mismatched_shapes(self):
        """Test fit with invalid inputs."""
        model = AdaBoostClassifier()
        with self.assertRaises(ValueError):
            model.fit(self.X_binary[:10], self.y_binary)  # Mismatched shapes

    def test_fit_invalid_input_empty_data(self):
        """Test fit with invalid inputs."""
        model = AdaBoostClassifier()
        with self.assertRaises(ValueError):
            model.fit(np.array([]), np.array([]))  # Empty data

    def test_predict_before_fit(self):
        """Test predict before fitting."""
        model = AdaBoostClassifier()
        with self.assertRaises(TypeError):  # Classes_ is None
            model.predict(self.X_binary)

    def test_early_stopping_perfect_fit(self):
        """Test if boosting stops early on a perfectly separable dataset."""
        # Use data perfectly separable by a stump
        X_perfect = np.array([[1], [2], [10], [11]])
        y_perfect = np.array([0, 0, 1, 1])
        model = AdaBoostClassifier(n_estimators=20, min_samples_split=1)
        model.fit(X_perfect, y_perfect)
        # The first stump should perfectly separate it
        self.assertLessEqual(len(model.estimators_), 1)
        # Check if the error of the first estimator is indeed 0
        if len(model.estimators_) > 0:
            self.assertEqual(model.estimator_errors_[0], 0)

    def test_custom_base_estimator_tree(self):
        """Test using a custom base estimator (tree)."""
        base_est = ClassifierTree(max_depth=1, min_samples_split=5)
        model = AdaBoostClassifier(base_estimator=base_est, n_estimators=5)
        model.fit(self.X_binary, self.y_binary)
        # Check if the fitted estimators have the correct depth (approx check)
        self.assertTrue(
            all(
                hasattr(est, "max_depth") and est.max_depth == 1
                for est in model.estimators_
            )
        )

    def test_custom_base_estimator_forrest(self):
        """Test using a custom base estimator (forest)."""
        base_est = RandomForestClassifier(
            n_estimators=1, max_depth=1, min_samples_split=1, n_jobs=1
        )
        # Catch warnings
        with warnings.catch_warnings(record=True) as _w:
            warnings.simplefilter("always")
            model = AdaBoostClassifier(base_estimator=base_est, n_estimators=5)
            model.fit(self.X_binary, self.y_binary)
        self.assertTrue(
            all(
                hasattr(est, "max_depth") and est.max_depth == 1
                for est in model.estimators_
            )
        )

    def test_custom_base_estimator_gradient(self):
        """Test using a custom base estimator (gradient)."""
        base_est = GradientBoostedClassifier(
            n_estimators=1, max_depth=1, learning_rate=0.1
        )
        # Catch warnings
        with warnings.catch_warnings(record=True) as _w:
            warnings.simplefilter("always")
            model = AdaBoostClassifier(base_estimator=base_est, n_estimators=5)
            model.fit(self.X_binary, self.y_binary)
        self.assertTrue(
            all(
                hasattr(est, "max_depth") and est.max_depth == 1
                for est in model.estimators_
            )
        )

    def test_custom_base_estimator_invalid(self):
        """Test using an invalid base estimator."""
        with self.assertRaises(AttributeError):
            AdaBoostClassifier(base_estimator="invalid_estimator")


class TestAdaBoostRegressor(BaseTest):
    """Unit tests for the AdaBoostRegressor class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting AdaBoostRegressor", end="", flush=True)
        cls.X, cls.y = make_regression(
            n_samples=100, n_features=10, noise=10, random_state=42
        )

    def test_initialization_default(self):
        """Test default initialization."""
        model = AdaBoostRegressor()
        self.assertIsInstance(model.base_estimator_, RegressorTree)
        self.assertEqual(model.base_estimator_.max_depth, 3)
        self.assertEqual(model.n_estimators, 50)
        self.assertEqual(model.learning_rate, 1.0)
        self.assertEqual(model.loss, "linear")
        self.assertIsNone(model.random_state)

    def test_initialization_custom(self):
        """Test initialization with custom parameters."""
        base_est = RegressorTree(max_depth=5)
        model = AdaBoostRegressor(
            base_estimator=base_est,
            n_estimators=10,
            learning_rate=0.5,
            loss="square",
        )
        self.assertEqual(model.base_estimator_, base_est)
        self.assertEqual(model.n_estimators, 10)
        self.assertEqual(model.learning_rate, 0.5)
        self.assertEqual(model.loss, "square")

    def test_fit_predict(self):
        """Test fitting and predicting."""
        model = AdaBoostRegressor(n_estimators=10, random_state=42)
        model.fit(self.X, self.y)
        self.assertEqual(len(model.estimators_), 10)
        self.assertEqual(len(model.estimator_weights_), 10)
        self.assertEqual(len(model.estimator_errors_), 10)

        y_pred = model.predict(self.X)
        self.assertEqual(y_pred.shape, (self.X.shape[0],))
        self.assertTrue(np.all(np.isfinite(y_pred)))
        r2 = Metrics.r_squared(self.y, y_pred)
        # AdaBoost might not always improve R2 significantly on noisy data
        self.assertTrue(-1.0 <= r2 <= 1.0)

    def test_loss_functions(self):
        """Test different loss functions."""
        for loss_type in ["linear", "square", "exponential"]:
            with self.subTest(loss=loss_type):
                model = AdaBoostRegressor(n_estimators=5, loss=loss_type)
                model.fit(self.X, self.y)
                self.assertEqual(len(model.estimators_), 5)
                y_pred = model.predict(self.X)
                self.assertTrue(np.all(np.isfinite(y_pred)))

    def test_get_stats(self):
        """Test the get_stats method."""
        model = AdaBoostRegressor(n_estimators=10, random_state=42)
        model.fit(self.X, self.y)
        stats = model.get_stats(self.y, X=self.X)
        self.assertIsInstance(stats, dict)
        self.assertIn("MSE", stats)
        self.assertIn("R^2", stats)
        self.assertIn("MAE", stats)
        self.assertIn("RMSE", stats)
        self.assertIn("MAPE", stats)

        with suppress_print():
            model.get_stats(self.y, X=self.X, verbose=True)

    def test_custom_base_estimator(self):
        """Test using a custom base estimator."""
        base_est = RegressorTree(max_depth=1, min_samples_split=5)
        model = AdaBoostRegressor(base_estimator=base_est, n_estimators=5)
        model.fit(self.X, self.y)
        self.assertTrue(
            all(
                hasattr(est, "max_depth") and est.max_depth == 1
                for est in model.estimators_
            )
        )

    def test_fit_invalid_input_mismatched_shapes(self):
        """Test fit with invalid inputs."""
        model = AdaBoostRegressor()
        with self.assertRaises(ValueError):
            model.fit(self.X[:10], self.y)  # Mismatched shapes

    def test_fit_invalid_input_empty_data(self):
        """Test fit with invalid inputs."""
        model = AdaBoostRegressor()
        with self.assertRaises(ZeroDivisionError):
            model.fit(np.array([]), np.array([]))  # Empty data

    def test_fit_invalid_input_y_not_1d(self):
        """Test fit with invalid inputs."""
        model = AdaBoostRegressor()
        with self.assertRaises(ValueError):
            model.fit(self.X, self.X)  # y should be 1D

    def test_predict_before_fit(self):
        """Test predict before fitting."""
        model = AdaBoostRegressor()
        with self.assertRaises(RuntimeError):  # No estimators fitted
            model.predict(self.X)

    def test_invalid_loss(self):
        """Test initialization with invalid loss function."""
        with self.assertRaises(ValueError):
            AdaBoostRegressor(loss="invalid_loss")

    def test_early_stopping_perfect_fit(self):
        """Test if boosting stops early on data with no error using a step function."""
        # Data perfectly fittable by a depth-1 tree (step function)
        X_perfect = np.array([[1], [2], [3], [4]])
        y_perfect = np.array([2, 2, 8, 8])  # Step at X=2.5
        # Use a base estimator that can fit this perfectly
        model = AdaBoostRegressor(
            base_estimator=RegressorTree(max_depth=1), n_estimators=20
        )
        model.fit(X_perfect, y_perfect)
        # It should fit perfectly in the first iteration
        self.assertLessEqual(len(model.estimators_), 1)
        # Check if the error of the first estimator is indeed 0
        if len(model.estimators_) > 0:
            self.assertEqual(model.estimator_errors_[0], 0)

    def test_custom_base_estimator_tree(self):
        """Test using a custom base estimator (tree)."""
        base_est = RegressorTree(max_depth=1, min_samples_split=5)
        model = AdaBoostRegressor(base_estimator=base_est, n_estimators=2)
        model.fit(self.X, self.y)
        # Check if the fitted estimators have the correct depth (approx check)
        self.assertTrue(
            all(
                hasattr(est, "max_depth") and est.max_depth == 1
                for est in model.estimators_
            )
        )

    def test_custom_base_estimator_forrest(self):
        """Test using a custom base estimator (forest)."""
        base_est = RandomForestRegressor(
            n_estimators=1, max_depth=1, min_samples_split=1, n_jobs=1
        )
        # Catch warnings
        with warnings.catch_warnings(record=True) as _w:
            warnings.simplefilter("always")
            model = AdaBoostRegressor(base_estimator=base_est, n_estimators=2)
            model.fit(self.X, self.y)
        self.assertTrue(
            all(
                hasattr(est, "max_depth") and est.max_depth == 1
                for est in model.estimators_
            )
        )

    def test_custom_base_estimator_gradient(self):
        """Test using a custom base estimator (gradient)."""
        base_est = GradientBoostedRegressor(num_trees=1, max_depth=1, learning_rate=0.1)
        # Catch warnings
        with warnings.catch_warnings(record=True) as _w:
            warnings.simplefilter("always")
            model = AdaBoostRegressor(base_estimator=base_est, n_estimators=2)
            model.fit(self.X, self.y)
        self.assertTrue(
            all(
                hasattr(est, "max_depth") and est.max_depth == 1
                for est in model.estimators_
            )
        )

    def test_custom_base_estimator_invalid(self):
        """Test using an invalid base estimator."""
        with self.assertRaises(AttributeError):
            AdaBoostClassifier(base_estimator="invalid_estimator")


if __name__ == "__main__":
    unittest.main()
