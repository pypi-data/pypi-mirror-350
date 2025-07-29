import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.svm import LinearSVC, LinearSVR
from sega_learn.utils import make_classification, make_regression
from tests.utils import BaseTest


class TestLinearSVR(BaseTest):
    """Unit test suite for the LinearSVR class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting LinearSVR", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.utility = LinearSVR()

    def test_fit_regression(self):
        """Test fitting LinearSVR on regression data."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = LinearSVR()
        model.fit(X, y)
        self.assertIsNotNone(model.w, "Weights should be initialized after fitting")
        self.assertIsNotNone(model.b, "Bias should be initialized after fitting")
        self.assertEqual(
            model.w.shape, (20,), "Weight shape should match number of features"
        )
        self.assertTrue(np.isscalar(model.b), "Bias should be a scalar")

    def test_predict_regression(self):
        """Test prediction on regression data."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = LinearSVR()
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertEqual(
            y_pred.shape, (100,), "Prediction shape should match number of samples"
        )
        self.assertTrue(np.all(np.isfinite(y_pred)), "Predictions should be finite")

    def test_decision_function_regression(self):
        """Test decision function on regression data."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = LinearSVR()
        model.fit(X, y)
        decisions = model.decision_function(X)
        self.assertEqual(
            decisions.shape,
            (100,),
            "Decision function output shape should match number of samples",
        )
        self.assertTrue(
            np.all(np.isfinite(decisions)), "Decision values should be finite"
        )
        # Since LinearSVR's decision_function and predict are the same for linear kernel
        self.assertTrue(
            np.allclose(decisions, model.predict(X)),
            "Decision function should match predictions",
        )

    def test_score_regression(self):
        """Test R² score computation."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = LinearSVR()
        model.fit(X, y)
        score = model.score(X, y)
        self.assertTrue(np.isfinite(score), "Score should be a finite number")
        # R² can be negative, but for synthetic data with default params, expect reasonable fit
        self.assertTrue(
            -1 <= score <= 1, "R² score should typically be between -1 and 1"
        )

    def test_invalid_kernel_svr(self):
        """Test that non-linear kernel raises TypeError."""
        with self.assertRaises(TypeError):
            model = LinearSVR(kernel="rbf")
            X, y = make_regression(n_samples=100, n_features=20, random_state=42)
            model.fit(X, y)

    def test_is_fitted(self):
        """Test the __sklearn_is_fitted__ method."""
        model = LinearSVR()
        self.assertFalse(
            model.__sklearn_is_fitted__(), "Model should not be fitted before fit"
        )
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model.fit(X, y)
        self.assertTrue(
            model.__sklearn_is_fitted__(), "Model should be fitted after fit"
        )

    def test_get_set_params(self):
        """Test parameter getting and setting."""
        model = LinearSVR(C=2.0, tol=1e-3)
        params = model.get_params()
        self.assertIn("C", params, "C should be in parameters")
        self.assertIn("tol", params, "tol should be in parameters")
        self.assertEqual(params["C"], 2.0, "C value should match initialization")
        self.assertEqual(params["tol"], 1e-3, "tol value should match initialization")
        model.set_params(C=3.0)
        self.assertEqual(model.C, 3.0, "C should be updated after set_params")

    def test_epsilon(self):
        """Test epsilon parameter initialization."""
        model = LinearSVR(epsilon=0.5)
        self.assertEqual(
            model.epsilon, 0.5, "Epsilon should match initialization value"
        )


class TestLinearSVC(BaseTest):
    """Unit test suite for the LinearSVC class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting LinearSVC", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.utility = LinearSVC()

    def test_fit_binary(self):
        """Test fitting LinearSVC on binary classification data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = LinearSVC()
        model.fit(X, y)
        self.assertIsNotNone(model.w, "Weights should be initialized after fitting")
        self.assertIsNotNone(model.b, "Bias should be initialized after fitting")
        self.assertEqual(
            model.w.shape, (20,), "Weight shape should match number of features"
        )
        self.assertTrue(np.isscalar(model.b), "Bias should be a scalar")

    def test_predict_binary(self):
        """Test prediction on binary classification data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = LinearSVC()
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertEqual(
            y_pred.shape, (100,), "Prediction shape should match number of samples"
        )
        self.assertTrue(
            np.all(np.isin(y_pred, [-1, 1])), "Predictions should be -1 or 1"
        )

    def test_decision_function_binary(self):
        """Test decision function on binary classification data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = LinearSVC()
        model.fit(X, y)
        decisions = model.decision_function(X)
        self.assertEqual(
            decisions.shape,
            (100,),
            "Decision function output shape should match number of samples",
        )
        self.assertTrue(
            np.all(np.isfinite(decisions)), "Decision values should be finite"
        )

    def test_score_binary(self):
        """Test accuracy score on binary classification data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = LinearSVC()
        model.fit(X, y)
        score = model.score(X, y)
        self.assertTrue(0 <= score <= 1, "Accuracy score should be between 0 and 1")

    def test_fit_multiclass(self):
        """Test fitting LinearSVC on multi-class data with one-vs-rest strategy."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=3, random_state=42
        )
        model = LinearSVC()
        model.fit(X, y)
        self.assertTrue(
            hasattr(model, "models_"), "Multi-class models should be stored"
        )
        self.assertEqual(len(model.models_), 3, "Should have one model per")
        for submodel in model.models_:
            self.assertIsInstance(
                submodel, LinearSVC, "Submodels should be LinearSVC instances"
            )
            self.assertIsNotNone(submodel.w, "Submodel weights should be initialized")
            self.assertIsNotNone(submodel.b, "Submodel bias should be initialized")

    def test_predict_multiclass(self):
        """Test prediction on multi-class data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=3, random_state=42
        )
        model = LinearSVC()
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertEqual(
            y_pred.shape, (100,), "Prediction shape should match number of samples"
        )
        self.assertTrue(
            np.all(np.isin(y_pred, model.classes_)),
            "Predictions should be valid class labels",
        )

    def test_score_multiclass(self):
        """Test accuracy score on multi-class data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=3, random_state=42
        )
        model = LinearSVC()
        model.fit(X, y)
        score = model.score(X, y)
        self.assertTrue(0 <= score <= 1, "Accuracy score should be between 0 and 1")

    def test_invalid_kernel(self):
        """Test that non-linear kernel raises TypeError."""
        with self.assertRaises(TypeError):
            model = LinearSVC(kernel="rbf")
            X, y = make_classification(
                n_samples=100, n_features=20, n_classes=2, random_state=42
            )
            model.fit(X, y)

    def test_fit_predict_simple_binary(self):
        """Test fitting and prediction on a simple linearly separable dataset."""
        X = np.array([[-1], [1]], dtype=np.float64)
        y = np.array([-1, 1], dtype=np.float64)
        model = LinearSVC(C=1.0, max_iter=1000, learning_rate=0.01)
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertTrue(np.all(y_pred == y), "Predictions should match true labels")
        decisions = model.decision_function(X)
        self.assertTrue(
            np.all(decisions * y > 0), "Decision values should have correct sign"
        )

    def test_is_fitted(self):
        """Test the __sklearn_is_fitted__ method."""
        model = LinearSVC()
        self.assertFalse(
            model.__sklearn_is_fitted__(), "Model should not be fitted before fit"
        )
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model.fit(X, y)
        self.assertTrue(
            model.__sklearn_is_fitted__(), "Model should be fitted after fit"
        )

    def test_get_set_params(self):
        """Test parameter getting and setting."""
        model = LinearSVC(C=2.0, tol=1e-3)
        params = model.get_params()
        self.assertIn("C", params, "C should be in parameters")
        self.assertIn("tol", params, "tol should be in parameters")
        self.assertEqual(params["C"], 2.0, "C value should match initialization")
        self.assertEqual(params["tol"], 1e-3, "tol value should match initialization")
        model.set_params(C=3.0)
        self.assertEqual(model.C, 3.0, "C should be updated after set_params")


if __name__ == "__main__":
    unittest.main()
