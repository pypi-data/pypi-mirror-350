import os
import sys
import unittest

import numpy as np

# Adjust the path to locate the generalizedSVM module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.svm.generalizedSVM import GeneralizedSVC, GeneralizedSVR
from sega_learn.utils import make_classification, make_regression
from tests.utils import BaseTest


class TestGeneralizedSVR(BaseTest):
    """Unit test suite for the GeneralizedSVR class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting GeneralizedSVR", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.utility = GeneralizedSVR(kernel="linear")

    def test_fit_regression(self):
        """Test fitting GeneralizedSVR on regression data with linear kernel."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = GeneralizedSVR(kernel="linear")
        model.fit(X, y)
        self.assertIsNotNone(model.w, "Weights should be initialized after fitting")
        self.assertIsNotNone(model.b, "Bias should be initialized after fitting")
        self.assertEqual(
            model.w.shape, (20,), "Weight shape should match number of features"
        )
        self.assertTrue(np.isscalar(model.b), "Bias should be a scalar")

    def test_predict_regression(self):
        """Test prediction on regression data with linear kernel."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = GeneralizedSVR(kernel="linear")
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertEqual(
            y_pred.shape, (100,), "Prediction shape should match number of samples"
        )
        self.assertTrue(np.all(np.isfinite(y_pred)), "Predictions should be finite")

    def test_decision_function_regression(self):
        """Test decision function on regression data with linear kernel."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = GeneralizedSVR(kernel="linear")
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
        self.assertTrue(
            np.allclose(decisions, model.predict(X)),
            "Decision function should match predictions",
        )

    def test_score_regression(self):
        """Test R² score computation for regression data with linear kernel."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = GeneralizedSVR(kernel="linear")
        model.fit(X, y)
        score = model.score(X, y)
        self.assertTrue(np.isfinite(score), "Score should be a finite number")
        self.assertTrue(
            -1 <= score <= 1, "R² score should typically be between -1 and 1"
        )

    def test_nonlinear_kernel_regression(self):
        """Test fitting and prediction on regression data with a non-linear kernel."""
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model = GeneralizedSVR(kernel="rbf")
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertEqual(
            y_pred.shape, (100,), "Prediction shape should match number of samples"
        )
        self.assertTrue(np.all(np.isfinite(y_pred)), "Predictions should be finite")

    def test_is_fitted(self):
        """Test the __sklearn_is_fitted__ method for regression."""
        model = GeneralizedSVR(kernel="linear")
        self.assertFalse(
            model.__sklearn_is_fitted__(), "Model should not be fitted before fit"
        )
        X, y = make_regression(n_samples=100, n_features=20, random_state=42)
        model.fit(X, y)
        self.assertTrue(
            model.__sklearn_is_fitted__(), "Model should be fitted after fit"
        )

    def test_get_set_params(self):
        """Test parameter getting and setting for regression."""
        model = GeneralizedSVR(kernel="linear", C=2.0, tol=1e-3)
        params = model.get_params()
        self.assertIn("C", params, "C should be in parameters")
        self.assertIn("tol", params, "tol should be in parameters")
        self.assertEqual(params["C"], 2.0, "C value should match initialization")
        self.assertEqual(params["tol"], 1e-3, "tol value should match initialization")
        model.set_params(C=3.0)
        self.assertEqual(model.C, 3.0, "C should be updated after set_params")

    def test_epsilon(self):
        """Test epsilon parameter initialization."""
        model = GeneralizedSVR(kernel="linear", epsilon=0.5)
        self.assertEqual(
            model.epsilon, 0.5, "Epsilon should match initialization value"
        )


class TestGeneralizedSVC(BaseTest):
    """Unit test suite for the GeneralizedSVC class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting GeneralizedSVC", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.utility = GeneralizedSVC(kernel="linear")

    def test_fit_binary(self):
        """Test fitting GeneralizedSVC on binary classification data with linear kernel."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = GeneralizedSVC(kernel="linear")
        model.fit(X, y)
        self.assertIsNotNone(
            model.w, "Weights should be initialized after fitting for linear kernel"
        )
        self.assertIsNotNone(
            model.b, "Bias should be initialized after fitting for linear kernel"
        )
        self.assertEqual(
            model.w.shape, (20,), "Weight shape should match number of features"
        )
        self.assertTrue(np.isscalar(model.b), "Bias should be a scalar")

    def test_predict_binary(self):
        """Test prediction on binary classification data with linear kernel."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = GeneralizedSVC(kernel="linear")
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertEqual(
            y_pred.shape, (100,), "Prediction shape should match number of samples"
        )
        self.assertTrue(np.all(np.isin(y_pred, [0, 1])), "Predictions should be 0 or 1")

    def test_decision_function_binary(self):
        """Test decision function on binary classification data with linear kernel."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = GeneralizedSVC(kernel="linear")
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
        """Test accuracy score on binary classification data with linear kernel."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = GeneralizedSVC(kernel="linear")
        model.fit(X, y)
        score = model.score(X, y)
        self.assertTrue(0 <= score <= 1, "Accuracy score should be between 0 and 1")

    def test_fit_multiclass(self):
        """Test fitting GeneralizedSVC on multi-class data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=3, random_state=42
        )
        model = GeneralizedSVC(kernel="linear")
        model.fit(X, y)
        # Check if multiclass strategy is applied; this depends on BaseSVM's implementation
        if hasattr(model, "models_"):
            self.assertEqual(len(model.models_), 3, "Should have one model per")
            for submodel in model.models_:
                self.assertIsNotNone(
                    submodel.w, "Submodel weights should be initialized"
                )
                self.assertIsNotNone(submodel.b, "Submodel bias should be initialized")

    def test_predict_multiclass(self):
        """Test prediction on multi-class data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=3, random_state=42
        )
        model = GeneralizedSVC(kernel="linear")
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertEqual(
            y_pred.shape, (100,), "Prediction shape should match number of samples"
        )
        if hasattr(model, "classes_"):
            self.assertTrue(
                np.all(np.isin(y_pred, model.classes_)),
                "Predictions should be valid class labels",
            )

    def test_score_multiclass(self):
        """Test accuracy score on multi-class data."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=3, random_state=42
        )
        model = GeneralizedSVC(kernel="linear")
        model.fit(X, y)
        score = model.score(X, y)
        self.assertTrue(0 <= score <= 1, "Accuracy score should be between 0 and 1")

    def test_nonlinear_kernel_classification(self):
        """Test fitting and prediction on classification data with a non-linear kernel."""
        X, y = make_classification(
            n_samples=100, n_features=20, n_classes=2, random_state=42
        )
        model = GeneralizedSVC(kernel="rbf")
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertEqual(
            y_pred.shape, (100,), "Prediction shape should match number of samples"
        )
        self.assertTrue(np.all(np.isin(y_pred, [0, 1])), "Predictions should be 0 or 1")

    def test_fit_predict_simple_binary(self):
        """Test fitting and prediction on a simple linearly separable dataset."""
        X = np.array([[-1], [1]], dtype=np.float64)
        y = np.array([-1, 1], dtype=np.float64)
        model = GeneralizedSVC(
            kernel="linear", C=1.0, max_iter=1000, learning_rate=0.01
        )
        model.fit(X, y)
        y_pred = model.predict(X)
        self.assertTrue(np.all(y_pred == y), "Predictions should match true labels")
        decisions = model.decision_function(X)
        self.assertTrue(
            np.all(decisions * y > 0), "Decision values should have correct sign"
        )

    def test_is_fitted(self):
        """Test the __sklearn_is_fitted__ method for classification."""
        model = GeneralizedSVC(kernel="linear")
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
        """Test parameter getting and setting for classification."""
        model = GeneralizedSVC(kernel="linear", C=2.0, tol=1e-3)
        params = model.get_params()
        self.assertIn("C", params, "C should be in parameters")
        self.assertIn("tol", params, "tol should be in parameters")
        self.assertEqual(params["C"], 2.0, "C value should match initialization")
        self.assertEqual(params["tol"], 1e-3, "tol value should match initialization")
        model.set_params(C=3.0)
        self.assertEqual(model.C, 3.0, "C should be updated after set_params")


if __name__ == "__main__":
    unittest.main()
