import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.linear_models import LogisticRegression, Ridge
from sega_learn.pipelines import Pipeline
from sega_learn.trees import AdaBoostClassifier, RandomForestClassifier
from sega_learn.utils import Scaler, make_classification, make_regression
from tests.utils import BaseTest


class SimpleTransformer:
    """Basic transformer for testing."""

    def fit(self, X, y=None):  # noqa: D102
        self.mean_ = X.mean(axis=0)
        return self

    def transform(self, X):  # noqa: D102
        return X - self.mean_

    def fit_transform(self, X, y=None):  # noqa: D102
        self.fit(X, y)
        return self.transform(X)

    def get_params(self, deep=True):  # noqa: D102
        return {}

    def set_params(self, **params):  # noqa: D102
        return self


class TestPipeline(BaseTest):
    """Unit tests for the general-purpose Pipeline class."""

    @classmethod
    def setUpClass(cls):  # noqa: D102
        print("\nTesting General Pipeline", end="", flush=True)

    def test_initialization(self):
        """Test pipeline initialization."""
        steps = [("scaler", SimpleTransformer()), ("clf", LogisticRegression())]
        pipe = Pipeline(steps)
        self.assertEqual(len(pipe.steps), 2)
        self.assertIsInstance(pipe.named_steps["scaler"], SimpleTransformer)
        self.assertIsInstance(pipe.named_steps["clf"], LogisticRegression)

    def test_invalid_steps_not_list(self):
        """Test error when steps is not a list."""
        with self.assertRaises(TypeError):
            Pipeline(steps="not a list")

    def test_invalid_steps_tuple_format(self):
        """Test error when step format is incorrect."""
        with self.assertRaises(TypeError):
            Pipeline(
                steps=[("scaler", SimpleTransformer()), ("clf")]
            )  # Missing estimator
        with self.assertRaises(TypeError):
            Pipeline(steps=[("scaler", SimpleTransformer(), "extra")])  # Too many items

    def test_invalid_steps_names(self):
        """Test error for duplicate or invalid step names."""
        with self.assertRaises(ValueError):
            Pipeline(
                steps=[("step", SimpleTransformer()), ("step", LogisticRegression())]
            )
        with self.assertRaises(ValueError):
            Pipeline(
                steps=[
                    ("step__one", SimpleTransformer()),
                    ("clf", LogisticRegression()),
                ]
            )
        with self.assertRaises(TypeError):
            Pipeline(steps=[(123, SimpleTransformer()), ("clf", LogisticRegression())])

    def test_invalid_intermediate_step(self):
        """Test error when an intermediate step is not a transformer."""

        class NotATransformer:
            def fit(self, X, y=None):
                return self

            # Missing transform

        with self.assertRaises(TypeError):
            Pipeline(steps=[("bad", NotATransformer()), ("clf", LogisticRegression())])

    def test_invalid_final_step(self):
        """Test error when the final step does not have 'fit'."""

        class NotAnEstimator:
            # Missing fit
            def predict(self, X):
                return X

        with self.assertRaises(TypeError):
            Pipeline(steps=[("scaler", SimpleTransformer()), ("bad", NotAnEstimator())])

    def test_fit_predict_classification(self):
        """Test fit and predict for a classification pipeline."""
        X, y = make_classification(n_samples=50, n_features=5, random_state=42)
        steps = [("scaler", Scaler()), ("clf", LogisticRegression(max_iter=50))]
        pipe = Pipeline(steps)

        pipe.fit(X, y)
        self.assertTrue(pipe._is_fitted, "Pipeline should be marked as fitted")
        y_pred = pipe.predict(X)
        self.assertEqual(y_pred.shape, (50,))

    def test_fit_predict_regression(self):
        """Test fit and predict for a regression pipeline."""
        X, y = make_regression(n_samples=50, n_features=5, random_state=42)
        steps = [("scaler", Scaler()), ("reg", Ridge(alpha=0.5))]
        pipe = Pipeline(steps)

        pipe.fit(X, y)
        self.assertTrue(pipe._is_fitted)
        y_pred = pipe.predict(X)
        self.assertEqual(y_pred.shape, (50,))

    def test_predict_before_fit(self):
        """Test calling predict before fit raises an error."""
        X, _ = make_classification(n_samples=10, n_features=5, random_state=42)
        steps = [("scaler", Scaler()), ("clf", LogisticRegression())]
        pipe = Pipeline(steps)
        with self.assertRaises(RuntimeError):
            pipe.predict(X)

    def test_get_set_params(self):
        """Test getting and setting parameters."""
        steps = [("scaler", Scaler()), ("clf", LogisticRegression(max_iter=100))]
        pipe = Pipeline(steps)

        params = pipe.get_params()
        self.assertIn("steps", params)
        self.assertIn("clf__max_iter", params)
        self.assertEqual(params["clf__max_iter"], 100)

        pipe.set_params(clf__max_iter=200, scaler__method="minmax")
        new_params = pipe.get_params()
        self.assertEqual(new_params["clf__max_iter"], 200)
        self.assertEqual(pipe.named_steps["clf"].max_iter, 200)
        self.assertEqual(pipe.named_steps["scaler"].method, "minmax")

        # Test setting steps (less common but should work)
        new_steps = [
            ("scaler2", Scaler(method="minmax")),
            ("rf", RandomForestClassifier(n_estimators=10)),
        ]
        pipe.set_params(steps=new_steps)
        self.assertEqual(len(pipe.steps), 2)
        self.assertIsInstance(pipe.named_steps["rf"], RandomForestClassifier)
        self.assertEqual(pipe.named_steps["rf"].n_estimators, 10)

    def test_set_params_invalid(self):
        """Test setting invalid parameters."""
        steps = [("scaler", Scaler()), ("clf", LogisticRegression())]
        pipe = Pipeline(steps)
        with self.assertRaises(ValueError):
            pipe.set_params(invalid_step__param=1)
        with self.assertRaises(ValueError):
            pipe.set_params(clf__invalid_param=1)

    def test_transform_only(self):
        """Test using the pipeline for transformations only."""
        X, _ = make_classification(n_samples=50, n_features=5, random_state=42)
        steps = [
            ("scaler1", Scaler(method="standard")),
            ("scaler2", Scaler(method="minmax")),
        ]
        pipe = Pipeline(steps)  # Note: Last step IS a transformer here

        # Fitting the transformers
        pipe.fit(X)  # Fit needs to be called even if no final estimator
        Xt = pipe.transform(X)
        self.assertEqual(Xt.shape, X.shape)

    def test_predict_proba(self):
        """Test predict_proba functionality."""
        X, y = make_classification(
            n_samples=50, n_features=5, n_classes=2, random_state=42
        )
        steps = [("scaler", Scaler()), ("ada", AdaBoostClassifier(n_estimators=5))]
        pipe = Pipeline(steps)
        pipe.fit(X, y)
        y_prob = pipe.predict_proba(X)
        self.assertEqual(y_prob.shape, (50, 2))
        self.assertTrue(np.allclose(np.sum(y_prob, axis=1), 1.0))

    def test_predict_proba_no_method(self):
        """Test predict_proba when final estimator lacks the method."""
        X, y = make_regression(n_samples=50, n_features=5, random_state=42)
        steps = [
            ("scaler", Scaler()),
            ("reg", Ridge()),
        ]  # Ridge doesn't have predict_proba
        pipe = Pipeline(steps)
        pipe.fit(X, y)
        with self.assertRaises(AttributeError):
            pipe.predict_proba(X)

    # TODO: No score method for any estimators, rethink
    # def test_score(self):
    #     """Test score functionality."""
    #     X, y = make_classification(
    #         n_samples=50, n_features=5, n_classes=2, random_state=42
    #     )
    #     steps = [("scaler", Scaler()), ("clf", LogisticRegression(max_iter=50))]
    #     pipe = Pipeline(steps)
    #     pipe.fit(X, y)
    #     score = pipe.score(X, y)
    #     self.assertTrue(0 <= score <= 1)

    def test_fit_predict(self):
        """Test fit_predict functionality (if final estimator supports it)."""

        # Using RandomForestClassifier which typically doesn't have fit_predict
        # Let's create a dummy one that does for the test
        class DummyEstimatorWithFitPredict:
            def fit(self, X, y, **kwargs):
                self.classes_ = np.unique(y)
                return self

            def predict(self, X, **kwargs):
                return np.random.choice(self.classes_, size=X.shape[0])

            def fit_predict(self, X, y, **kwargs):
                self.fit(X, y)
                # Simulate some combined process
                return self.predict(X) + 10  # Return something different from predict

        X, y = make_classification(
            n_samples=50, n_features=5, n_classes=2, random_state=42
        )
        steps = [("scaler", Scaler()), ("clf", DummyEstimatorWithFitPredict())]
        pipe = Pipeline(steps)
        y_fit_pred = pipe.fit_predict(X, y)
        self.assertEqual(y_fit_pred.shape, (50,))
        # Check if values are different from simple predict (as per our dummy impl)
        self.assertTrue(np.any(y_fit_pred > 1))

    def test_fit_predict_no_method(self):
        """Test fit_predict when final estimator lacks the method."""
        X, y = make_classification(
            n_samples=50, n_features=5, n_classes=2, random_state=42
        )
        steps = [
            ("scaler", Scaler()),
            ("clf", LogisticRegression()),
        ]  # LogisticRegression doesn't have fit_predict
        pipe = Pipeline(steps)
        with self.assertRaises(AttributeError):
            pipe.fit_predict(X, y)


if __name__ == "__main__":
    unittest.main()
