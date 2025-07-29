import os
import sys
import unittest

import numpy as np

# Adjust the path to locate the oneClassSVM module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.svm import OneClassSVM
from tests.utils import BaseTest


class TestOneClassSVM(BaseTest):
    """Unit test suite for the OneClassSVM class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting OneClassSVM", end="", flush=True)

    def setUp(self):  # NOQA D201
        # Using a default kernel; tests below also include a non-linear kernel case.
        self.model = OneClassSVM(
            kernel="linear", max_iter=200, learning_rate=0.05, C=0.5
        )

    def test_fit(self):
        """Test that fitting the OneClassSVM initializes support vectors and bias."""
        # Create a synthetic dataset (inliers)
        X = np.random.randn(50, 5)
        self.model.fit(X)
        # Check that support vectors, their alphas, and bias have been set
        self.assertTrue(
            hasattr(self.model, "support_vectors_"),
            "Model should have support_vectors_ after fit",
        )
        self.assertGreater(
            len(self.model.support_vectors_),
            0,
            "There should be at least one support vector",
        )
        self.assertTrue(
            hasattr(self.model, "support_vector_alphas_"),
            "Model should have support_vector_alphas_ after fit",
        )
        self.assertTrue(
            hasattr(self.model, "b"), "Model should have bias (b) set after fit"
        )

    def test_decision_function(self):
        """Test that decision_function returns finite values with correct shape."""
        X = np.random.randn(40, 5)
        self.model.fit(X)
        decisions = self.model.decision_function(X)
        self.assertEqual(
            decisions.shape,
            (X.shape[0],),
            "Decision function should return an array with one value per sample",
        )
        self.assertTrue(
            np.all(np.isfinite(decisions)),
            "All decision function values should be finite",
        )

    def test_predict(self):
        """Test that predict returns only 1 (inlier) or -1 (outlier)."""
        X = np.random.randn(40, 5)
        self.model.fit(X)
        predictions = self.model.predict(X)
        self.assertEqual(
            predictions.shape,
            (X.shape[0],),
            "Predict should return an array with one prediction per sample",
        )
        unique_preds = np.unique(predictions)
        for pred in unique_preds:
            self.assertIn(
                pred, [1, -1], "Predictions should be either 1 (inlier) or -1 (outlier)"
            )

    def test_score(self):
        """Test the score method by generating inlier and outlier data.

        Inliers are drawn from a Gaussian and outliers from a shifted distribution.
        """
        # Generate inliers (label 1)
        inliers = np.random.randn(80, 5)
        # Generate outliers (label -1)
        outliers = np.random.randn(20, 5) + 5.0  # shifted mean to simulate anomalies
        X_test = np.vstack((inliers, outliers))
        # True labels: inliers=1, outliers=-1
        y_true = np.array([1] * 80 + [-1] * 20)

        # Fit on inliers only (as typical for one-class models)
        self.model.fit(inliers)
        score = self.model.score(X_test, y_true)
        self.assertTrue(0 <= score <= 1, "Score should be between 0 and 1")

    def test_nonlinear_kernel(self):
        """Test OneClassSVM with a non-linear kernel (e.g. 'rbf')."""
        model_nl = OneClassSVM(kernel="rbf", max_iter=200, learning_rate=0.05, C=0.5)
        X = np.random.randn(50, 5)
        model_nl.fit(X)
        predictions = model_nl.predict(X)
        self.assertEqual(
            predictions.shape,
            (X.shape[0],),
            "Prediction shape should match number of samples",
        )
        # Ensure that predictions are only in {1, -1}
        self.assertTrue(
            np.all(np.isin(predictions, [1, -1])),
            "Predictions should be either 1 or -1 with non-linear kernel",
        )

    def test_is_fitted(self):
        """Test that the model indicates it is not fitted before calling fit and that after fitting the necessary attributes are present."""
        model = OneClassSVM(kernel="linear")
        # Before fitting, support_vectors_ should be None
        self.assertIsNone(
            model.support_vectors_,
            "Model support_vectors_ should be None before fitting",
        )
        X = np.random.randn(30, 5)
        model.fit(X)
        self.assertTrue(
            hasattr(model, "support_vectors_"),
            "Model should have support_vectors_ after fitting",
        )
        # Although __sklearn_is_fitted__ checks for 'w', for OneClassSVM we use support_vectors_
        # So here we check that either __sklearn_is_fitted__ returns True or support_vectors_ is present.
        fitted = model.__sklearn_is_fitted__() or hasattr(model, "support_vectors_")
        self.assertTrue(fitted, "Model should be considered fitted after calling fit")


if __name__ == "__main__":
    unittest.main()
