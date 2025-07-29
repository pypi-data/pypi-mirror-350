import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
from sega_learn.linear_models import *
from sega_learn.linear_models import make_sample_data
from sega_learn.utils import Metrics, make_classification
from tests.utils import BaseTest, suppress_print, synthetic_data_regression

r2_score = Metrics.r_squared
accuracy_score = Metrics.accuracy


class TestOrdinaryLeastSquares(BaseTest):
    """Unit test for the Ordinary Least Squares regression class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Ordinary Least Squares Model", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.model = OrdinaryLeastSquares()

    def test_fit_predict(self):
        """Tests the fit and predict methods of the Ordinary Least Squares class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        y_pred = self.model.predict(X)
        self.assertGreater(r2_score(y, y_pred), 0.5)

    def test_fit_intercept(self):
        """Tests the fit_intercept parameter of the Ordinary Least Squares class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = OrdinaryLeastSquares(fit_intercept=True)
        self.model.fit(X, y)
        self.assertTrue(self.model.fit_intercept)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.fit(None, None)

    def test_invalid_predict(self):
        """Tests the predict method with invalid input."""
        with self.assertRaises(AttributeError):
            self.model.predict(None)

    def test_get_formula(self):
        """Tests the get_formula method of the Ordinary Least Squares class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_get_formula_with_intercept(self):
        """Tests the get_formula method with intercept of the Ordinary Least Squares class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_coef_(self):
        """Tests the coef_ attribute of the Ordinary Least Squares class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        self.assertEqual(len(self.model.coef_), 5)

    def test_get_params(self):
        """Tests the get_params method of the Ordinary Least Squares class."""
        params = self.model.get_params()
        self.assertIn("fit_intercept", params)

    def test_set_params(self):
        """Tests the set_params method of the Ordinary Least Squares class."""
        self.model.set_params(fit_intercept=False)
        self.assertFalse(self.model.fit_intercept)

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.set_params(invalid_param=0.1)


class TestRidge(BaseTest):
    """Unit test for the Ridge regression class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Ridge Regression Model", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.model = Ridge()

    def test_fit_predict(self):
        """Tests the fit and predict methods of the Ridge class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        y_pred = self.model.predict(X)
        self.assertGreater(r2_score(y, y_pred), 0.5)

    def test_fit_intercept(self):
        """Tests the fit_intercept parameter of the Ridge class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Ridge(fit_intercept=True)
        self.model.fit(X, y)
        self.assertTrue(self.model.fit_intercept)

    def test_fit_max_iter(self):
        """Tests the max_iter parameter of the Ridge class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Ridge(max_iter=1000)
        self.model.fit(X, y)
        self.assertEqual(self.model.max_iter, 1000)

    def test_fit_tol(self):
        """Tests the tol parameter of the Ridge class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Ridge(tol=0.0001)
        self.model.fit(X, y)
        self.assertEqual(self.model.tol, 0.0001)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.fit(None, None)

    def test_invalid_predict(self):
        """Tests the predict method with invalid input."""
        with self.assertRaises(AttributeError):
            self.model.predict(None)

    def test_get_formula(self):
        """Tests the get_formula method of the Ridge class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_get_formula_with_intercept(self):
        """Tests the get_formula method with intercept of the Ridge class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_coef_(self):
        """Tests the coef_ attribute of the Ridge class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        self.assertEqual(len(self.model.coef_), 5)

    def test_fit_predict_numba(self):
        """Test the fit and predict methods with numba implementation."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Ridge(alpha=1.0, fit_intercept=True, max_iter=1000, tol=1e-4)
        self.model.fit(X, y, numba=True)
        y_pred = self.model.predict(X)
        self.assertGreater(r2_score(y, y_pred), 0.5)

    def test_fit_no_intercept_numba(self):
        """Test the fit method with numba implementation and no intercept."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Ridge(alpha=1.0, fit_intercept=False, max_iter=1000, tol=1e-4)
        self.model.fit(X, y, numba=True)
        self.assertEqual(self.model.intercept_, 0.0)

    def test_invalid_fit_numba(self):
        """Test the fit method with invalid input using numba implementation."""
        self.model = Ridge(alpha=1.0, fit_intercept=True, max_iter=1000, tol=1e-4)
        with self.assertRaises(ValueError):
            self.model.fit(None, None, numba=True)

    def test_get_params(self):
        """Tests the get_params method of the Ridge class."""
        params = self.model.get_params()
        self.assertIn("alpha", params)
        self.assertIn("fit_intercept", params)

    def test_set_params(self):
        """Tests the set_params method of the Ridge class."""
        self.model.set_params(alpha=0.5)
        self.assertEqual(self.model.alpha, 0.5)

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.set_params(invalid_param=0.1)


class TestLasso(BaseTest):
    """Unit test for the Lasso regression class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Lasso Regression Model", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.model = Lasso()

    def test_fit_predict(self):
        """Tests the fit and predict methods of the Lasso class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        y_pred = self.model.predict(X)
        self.assertGreater(r2_score(y, y_pred), 0.5)

    def test_fit_intercept(self):
        """Tests the fit_intercept parameter of the Lasso class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Lasso(fit_intercept=True)
        self.model.fit(X, y)
        self.assertTrue(self.model.fit_intercept)

    def test_fit_max_iter(self):
        """Tests the max_iter parameter of the Lasso class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Lasso(max_iter=1000)
        self.model.fit(X, y)
        self.assertEqual(self.model.max_iter, 1000)

    def test_fit_tol(self):
        """Tests the tol parameter of the Lasso class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Lasso(tol=0.0001)
        self.model.fit(X, y)
        self.assertEqual(self.model.tol, 0.0001)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.fit(None, None)

    def test_invalid_predict(self):
        """Tests the predict method with invalid input."""
        with self.assertRaises(AttributeError):
            self.model.predict(None)

    def test_get_formula(self):
        """Tests the get_formula method of the Lasso class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_get_formula_with_intercept(self):
        """Tests the get_formula method with intercept of the Lasso class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_coef_(self):
        """Tests the coef_ attribute of the Lasso class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        self.assertEqual(len(self.model.coef_), 5)

    def test_fit_predict_numba(self):
        """Test the fit and predict methods with numba implementation."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Lasso(alpha=1.0, fit_intercept=True, max_iter=1000, tol=1e-4)
        self.model.fit(X, y, numba=True)
        y_pred = self.model.predict(X)
        self.assertGreater(r2_score(y, y_pred), 0.5)

    def test_fit_no_intercept_numba(self):
        """Test the fit method with numba implementation and no intercept."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Lasso(alpha=1.0, fit_intercept=False, max_iter=1000, tol=1e-4)
        self.model.fit(X, y, numba=True)
        self.assertEqual(self.model.intercept_, 0.0)

    def test_invalid_fit_numba(self):
        """Test the fit method with invalid input using numba implementation."""
        self.model = Lasso(alpha=1.0, fit_intercept=True, max_iter=1000, tol=1e-4)
        with self.assertRaises(ValueError):
            self.model.fit(None, None, numba=True)

    def test_get_params(self):
        """Tests the get_params method of the Lasso class."""
        params = self.model.get_params()
        self.assertIn("alpha", params)
        self.assertIn("fit_intercept", params)

    def test_set_params(self):
        """Tests the set_params method of the Lasso class."""
        self.model.set_params(alpha=0.5)
        self.assertEqual(self.model.alpha, 0.5)

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.set_params(invalid_param=0.1)


class TestBayesian(BaseTest):
    """Unit test for the Bayesian regression class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Bayesian Regression Model", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.model = Bayesian()

    def test_fit_predict(self):
        """Tests the fit and predict methods of the Bayesian class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        y_pred = self.model.predict(X)
        self.assertGreater(r2_score(y, y_pred), 0.5)

    def test_fit_intercept(self):
        """Tests the fit_intercept parameter of the Bayesian class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Bayesian(fit_intercept=True)
        self.model.fit(X, y)
        self.assertTrue(self.model.fit_intercept)

    def test_fit_max_iter(self):
        """Tests the max_iter parameter of the Bayesian class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Bayesian(max_iter=1000)
        self.model.fit(X, y)
        self.assertEqual(self.model.max_iter, 1000)

    def test_fit_tol(self):
        """Tests the tol parameter of the Bayesian class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = Bayesian(tol=0.0001)
        self.model.fit(X, y)
        self.assertEqual(self.model.tol, 0.0001)

    def test_tune(self):
        """Tests the tune method of the Bayesian class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        with suppress_print():
            alpha_1, alpha_2, lambda_1, lambda_2 = self.model.tune(
                X, y, beta1=0.9, beta2=0.999, iter=1000
            )
        self.assertIsNotNone(alpha_1)
        self.assertIsNotNone(alpha_2)
        self.assertIsNotNone(lambda_1)
        self.assertIsNotNone(lambda_2)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.fit(None, None)

    def test_invalid_predict(self):
        """Tests the predict method with invalid input."""
        with self.assertRaises(TypeError):
            self.model.predict(None)

    def test_get_formula(self):
        """Tests the get_formula method of the Bayesian class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_get_formula_with_intercept(self):
        """Tests the get_formula method with intercept of the Bayesian class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_coef_(self):
        """Tests the coef_ attribute of the Bayesian class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        self.assertEqual(len(self.model.coef_), 5)

    def test_get_params(self):
        """Tests the get_params method of the Bayesian class."""
        params = self.model.get_params()
        self.assertIn("alpha_1", params)
        self.assertIn("alpha_2", params)
        self.assertIn("fit_intercept", params)

    def test_set_params(self):
        """Tests the set_params method of the Bayesian class."""
        self.model.set_params(alpha_1=0.5, alpha_2=0.5)
        self.assertEqual(self.model.alpha_1, 0.5)
        self.assertEqual(self.model.alpha_2, 0.5)

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.set_params(invalid_param=0.1)


class TestRANSAC(BaseTest):
    """Unit test for the RANSAC regression class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting RANSAC Regression Model", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.model = RANSAC()

    def test_fit_predict(self):
        """Tests the fit and predict methods of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model.fit(X, y)
        y_pred = self.model.predict(X)
        self.assertGreater(r2_score(y, y_pred), 0.5)

    def test_fit_n(self):
        """Tests the n parameter of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = RANSAC(n=100)
        self.model.fit(X, y)
        self.assertEqual(self.model.n, 100)

    def test_fit_k(self):
        """Tests the k parameter of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = RANSAC(k=10)
        self.model.fit(X, y)
        self.assertEqual(self.model.k, 10)

    def test_fit_t(self):
        """Tests the t parameter of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = RANSAC(t=2.0)
        self.model.fit(X, y)
        self.assertEqual(self.model.t, 2.0)

    def test_fit_d(self):
        """Tests the d parameter of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = RANSAC(d=10)
        self.model.fit(X, y)
        self.assertEqual(self.model.d, 10)

    def test_fit_auto_scale_t(self):
        """Tests the auto_scale_t parameter of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = RANSAC(auto_scale_t=True)
        self.model.fit(X, y)
        self.assertTrue(self.model.scale_threshold)

    def test_fit_auto_scale_n(self):
        """Tests the auto_scale_n parameter of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = RANSAC(auto_scale_n=True)
        self.model.fit(X, y)
        self.assertTrue(self.model.scale_n)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.fit(None, None)

    def test_invalid_predict(self):
        """Tests the predict method with invalid input."""
        with self.assertRaises(AttributeError):
            self.model.predict(None)

    def test_get_formula(self):
        """Tests the get_formula method of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_get_formula_with_intercept(self):
        """Tests the get_formula method with intercept of the RANSAC class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_get_params(self):
        """Tests the get_params method of the RANSAC class."""
        params = self.model.get_params()
        self.assertIn("n", params)
        self.assertIn("k", params)
        self.assertIn("t", params)
        self.assertIn("d", params)
        self.assertIn("auto_scale_t", params)
        self.assertIn("auto_scale_n", params)

    def test_set_params(self):
        """Tests the set_params method of the RANSAC class."""
        self.model.set_params(n=200)
        self.assertEqual(self.model.n, 200)

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.set_params(invalid_param=0.1)


class TestPassiveAggressiveRegressor(BaseTest):
    """Unit test for the Passive Aggressive Regressor class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Passive Aggressive Regressor Model", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.model = PassiveAggressiveRegressor()

    def test_fit_predict(self):
        """Tests the fit and predict methods of the Passive Aggressive Regressor class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        with suppress_print():
            self.model.fit(X, y)
        y_pred = self.model.predict(X)
        self.assertGreater(r2_score(y, y_pred), 0.5)

    def test_fit_all_steps(self):
        """Tests the fit method with save_steps parameter of the Passive Aggressive Regressor class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        with suppress_print():
            self.model.fit(X, y, save_steps=True)
        self.assertTrue(len(self.model.steps_) > 0)

    def test_predict_all_steps(self):
        """Tests the predict_all_steps method of the Passive Aggressive Regressor class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        with suppress_print():
            self.model.fit(X, y, save_steps=True)
        y_preds = self.model.predict_all_steps(X)
        self.assertGreater(len(y_preds), 0)

    def test_fit_max_iter(self):
        """Tests the max_iter parameter of the Passive Aggressive Regressor class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = PassiveAggressiveRegressor(max_iter=1000)
        with suppress_print():
            self.model.fit(X, y)
        self.assertEqual(self.model.max_iter, 1000)

    def test_fit_tol(self):
        """Tests the tol parameter of the Passive Aggressive Regressor class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        self.model = PassiveAggressiveRegressor(tol=0.0001)
        with suppress_print():
            self.model.fit(X, y)
        self.assertEqual(self.model.tol, 0.0001)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.fit(None, None)

    def test_invalid_predict(self):
        """Tests the predict method with invalid input."""
        with self.assertRaises(TypeError):
            self.model.predict(None)

    def test_get_formula(self):
        """Tests the get_formula method of the Passive Aggressive Regressor class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        with suppress_print():
            self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_get_formula_with_intercept(self):
        """Tests the get_formula method with intercept of the Passive Aggressive Regressor class."""
        X, y = synthetic_data_regression(n_samples=100, n_features=2, noise=0.1)
        with suppress_print():
            self.model.fit(X, y)
        formula = self.model.get_formula()
        self.assertIsNotNone(formula)
        self.assertIn("y = ", formula)

    def test_coef_(self):
        """Tests the coef_ attribute of the Passive Aggressive Regressor class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=5, noise=0.1)
        with suppress_print():
            self.model.fit(X, y)
        self.assertEqual(len(self.model.coef_), 5)

    def test_get_params(self):
        """Tests the get_params method of the Passive Aggressive Regressor class."""
        params = self.model.get_params()
        self.assertIn("max_iter", params)
        self.assertIn("tol", params)

    def test_set_params(self):
        """Tests the set_params method of the Passive Aggressive Regressor class."""
        self.model.set_params(max_iter=200)
        self.assertEqual(self.model.max_iter, 200)

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        with self.assertRaises(ValueError):
            self.model.set_params(invalid_param=0.1)


class TestLinearDiscriminantAnalysis(BaseTest):
    """Unit test for the Linear Discriminant Analysis class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Linear Discriminant Analysis", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.cov_class_1 = (
            np.array([[0.0, -1.0], [2.5, 0.7]]) * 2.0
        )  # Covariance matrix for class 1, scaled by 2.0
        self.cov_class_2 = (
            self.cov_class_1.T
        )  # Covariance matrix for class 2, same as class 1 but transposed

        # Generate data
        self.X, self.y = make_sample_data(
            n_samples=1000,
            n_features=2,
            cov_class_1=self.cov_class_1,
            cov_class_2=self.cov_class_2,
            shift=[4, 1],
            seed=1,
        )

    def test_lda(self):
        """Tests the fit and predict methods of the Linear Discriminant Analysis class."""
        lda = LinearDiscriminantAnalysis()
        lda.fit(self.X, self.y)
        y_pred = lda.predict(self.X)
        acc = accuracy_score(self.y, y_pred)
        self.assertGreaterEqual(acc, 0.50)

    def test_lda_svd(self):
        """Tests the fit and predict methods with svd solver of the Linear Discriminant Analysis class."""
        lda = LinearDiscriminantAnalysis(solver="svd")
        lda.fit(self.X, self.y)
        y_pred = lda.predict(self.X)
        acc = accuracy_score(self.y, y_pred)
        self.assertGreater(acc, 0)

    def test_lda_lsqr(self):
        """Tests the fit and predict methods with lsqr solver of the Linear Discriminant Analysis class."""
        lda = LinearDiscriminantAnalysis(solver="lsqr")
        lda.fit(self.X, self.y)
        y_pred = lda.predict(self.X)
        acc = accuracy_score(self.y, y_pred)
        self.assertGreater(acc, 0)

    def test_lda_eigen(self):
        """Tests the fit and predict methods with eigen solver of the Linear Discriminant Analysis class."""
        lda = LinearDiscriminantAnalysis(solver="eigen")
        lda.fit(self.X, self.y)
        y_pred = lda.predict(self.X)
        acc = accuracy_score(self.y, y_pred)
        self.assertGreater(acc, 0)

    def test_lda_bad_solver(self):
        """Tests the fit method with invalid solver of the Linear Discriminant Analysis class."""
        lda = LinearDiscriminantAnalysis(solver="bad_solver")
        with self.assertRaises(ValueError):
            lda.fit(self.X, self.y)

    def test_lda_no_solver(self):
        """Tests the fit method with no solver of the Linear Discriminant Analysis class."""
        lda = LinearDiscriminantAnalysis(solver=None)
        with self.assertRaises(ValueError):
            lda.fit(self.X, self.y)

    def test_lda_no_data(self):
        """Tests the fit method with invalid input."""
        lda = LinearDiscriminantAnalysis()
        with self.assertRaises(ValueError):
            lda.fit(None, None)

    def test_get_params(self):
        """Tests the get_params method of the Linear Discriminant Analysis class."""
        lda = LinearDiscriminantAnalysis()
        params = lda.get_params()
        self.assertIn("solver", params)
        self.assertIn("priors", params)

    def test_set_params(self):
        """Tests the set_params method of the Linear Discriminant Analysis class."""
        lda = LinearDiscriminantAnalysis()
        lda.set_params(solver="svd")
        self.assertEqual(lda.solver, "svd")

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        lda = LinearDiscriminantAnalysis()
        with self.assertRaises(ValueError):
            lda.set_params(invalid_param=0.1)


class TestQuadraticDiscriminantAnalysis(BaseTest):
    """Unit test for the Quadratic Discriminant Analysis class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Quadratic Discriminant Analysis", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.cov_class_1 = (
            np.array([[0.0, -1.0], [2.5, 0.7]]) * 2.0
        )  # Covariance matrix for class 1, scaled by 2.0
        self.cov_class_2 = (
            self.cov_class_1.T
        )  # Covariance matrix for class 2, same as class 1 but transposed

        # Generate data
        self.X, self.y = make_sample_data(
            n_samples=1000,
            n_features=2,
            cov_class_1=self.cov_class_1,
            cov_class_2=self.cov_class_2,
            shift=[4, 1],
            seed=1,
        )

    def test_qda(self):
        """Tests the fit and predict methods of the Quadratic Discriminant Analysis class."""
        qda = QuadraticDiscriminantAnalysis()
        qda.fit(self.X, self.y)
        y_pred = qda.predict(self.X)
        acc = accuracy_score(self.y, y_pred)
        self.assertGreaterEqual(acc, 0.50)

    def test_qda_prior(self):
        """Tests the fit and predict methods with priors parameter of the Quadratic Discriminant Analysis class."""
        qda = QuadraticDiscriminantAnalysis(priors=[0.5, 0.5])
        self.y = self.y.astype(int)  # Ensure class labels are integers
        qda.fit(self.X, self.y)
        y_pred = qda.predict(self.X)
        acc = accuracy_score(self.y, y_pred)
        self.assertGreaterEqual(acc, 0.50)

    def test_qda_reg_param(self):
        """Tests the fit and predict methods with reg_param parameter of the Quadratic Discriminant Analysis class."""
        qda = QuadraticDiscriminantAnalysis(reg_param=0.1)
        qda.fit(self.X, self.y)
        y_pred = qda.predict(self.X)
        acc = accuracy_score(self.y, y_pred)
        self.assertGreaterEqual(acc, 0.50)

    def test_qda_bad_reg_param(self):
        """Tests the fit method with invalid reg_param parameter of the Quadratic Discriminant Analysis class."""
        with self.assertRaises(AssertionError):
            qda = QuadraticDiscriminantAnalysis(reg_param=-0.1)
            qda.fit(self.X, self.y)

    def test_qda_no_data(self):
        """Tests the fit method with invalid input."""
        qda = QuadraticDiscriminantAnalysis()
        with self.assertRaises(ValueError):
            qda.fit(None, None)

    def test_qda_no_priors(self):
        """Tests the fit method with no priors parameter of the Quadratic Discriminant Analysis class."""
        qda = QuadraticDiscriminantAnalysis(priors=None)
        qda.fit(self.X, self.y)
        self.assertEqual(qda.priors, None)

    def test_qda_bad_priors(self):
        """Tests the fit method with invalid priors parameter of the Quadratic Discriminant Analysis class."""
        with self.assertRaises(TypeError):
            qda = QuadraticDiscriminantAnalysis(priors=[0.5, 0.5, 0.5])
            qda.fit(self.X, self.y)

    def test_get_params(self):
        """Tests the get_params method of the Quadratic Discriminant Analysis class."""
        qda = QuadraticDiscriminantAnalysis()
        params = qda.get_params()
        self.assertIn("priors", params)
        self.assertIn("reg_param", params)

    def test_set_params(self):
        """Tests the set_params method of the Quadratic Discriminant Analysis class."""
        qda = QuadraticDiscriminantAnalysis()
        qda.set_params(priors=[0.5, 0.5])
        self.assertEqual(qda.priors, [0.5, 0.5])

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        qda = QuadraticDiscriminantAnalysis()
        with self.assertRaises(ValueError):
            qda.set_params(invalid_param=0.1)


class TestLogisticRegression(BaseTest):
    """Unit test for the Logistic Regression class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Logistic Regression", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.cov_class_1 = (
            np.array([[0.0, -1.0], [2.5, 0.7]]) * 2.0
        )  # Covariance matrix for class 1, scaled by 2.0
        self.cov_class_2 = (
            self.cov_class_1.T
        )  # Covariance matrix for class 2, same as class 1 but transposed

        # Generate binary data
        self.X_binary, self.y_binary = make_classification(
            n_samples=300,
            n_features=2,
            n_redundant=0,
            n_informative=2,
            n_classes=2,
            random_state=42,
            n_clusters_per_class=1,
            class_sep=2,
        )

        # Generate multiclass data
        self.X_multiclass, self.y_multiclass = make_classification(
            n_samples=300,
            n_features=2,
            n_redundant=0,
            n_informative=2,
            n_classes=4,
            random_state=42,
            n_clusters_per_class=1,
            class_sep=2,
        )

    def test_fit_predict_binary(self):
        """Tests the fit and predict methods of the Logistic Regression class for binary classification."""
        model = LogisticRegression(learning_rate=0.01, max_iter=1000)
        model.fit(self.X_binary, self.y_binary)
        y_pred = model.predict(self.X_binary)
        acc = accuracy_score(self.y_binary, y_pred)
        self.assertGreaterEqual(acc, 0.50)

    def test_fit_predict_multiclass(self):
        """Tests the fit and predict methods of the Logistic Regression class for multiclass classification."""
        model = LogisticRegression(learning_rate=0.01, max_iter=1000)
        model.fit(self.X_multiclass, self.y_multiclass)
        y_pred = model.predict(self.X_multiclass)
        acc = accuracy_score(self.y_multiclass, y_pred)
        self.assertGreaterEqual(acc, 0.50)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        model = LogisticRegression()
        with self.assertRaises(ValueError):
            model.fit(None, None)

    def test_invalid_predict(self):
        """Tests the predict method with invalid input."""
        model = LogisticRegression()
        with self.assertRaises(TypeError):
            model.predict(None)

    def test_get_params(self):
        """Tests the get_params method of the Logistic Regression class."""
        model = LogisticRegression(learning_rate=0.01, max_iter=1000)
        params = model.get_params()
        self.assertIn("learning_rate", params)
        self.assertIn("max_iter", params)

    def test_set_params(self):
        """Tests the set_params method of the Logistic Regression class."""
        model = LogisticRegression(learning_rate=0.01, max_iter=1000)
        model.set_params(learning_rate=0.1)
        self.assertEqual(model.learning_rate, 0.1)

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        model = LogisticRegression(learning_rate=0.01, max_iter=1000)
        with self.assertRaises(ValueError):
            model.set_params(invalid_param=0.1)


class TestPerceptron(BaseTest):
    """Unit test for the Perceptron class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Perceptron", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.cov_class_1 = (
            np.array([[0.0, -1.0], [2.5, 0.7]]) * 2.0
        )  # Covariance matrix for class 1, scaled by 2.0
        self.cov_class_2 = (
            self.cov_class_1.T
        )  # Covariance matrix for class 2, same as class 1 but transposed

        # Generate binary data
        self.X_binary, self.y_binary = make_classification(
            n_samples=30,
            n_features=2,
            n_redundant=0,
            n_informative=2,
            n_classes=2,
            random_state=42,
            n_clusters_per_class=1,
            class_sep=2,
        )

        # Generate multiclass data
        self.X_multiclass, self.y_multiclass = make_classification(
            n_samples=30,
            n_features=2,
            n_redundant=0,
            n_informative=2,
            n_classes=4,
            random_state=42,
            n_clusters_per_class=1,
            class_sep=2,
        )

    def test_fit_predict_binary(self):
        """Tests the fit and predict methods of the Perceptron class for binary classification."""
        model = Perceptron(max_iter=1000, learning_rate=0.01)
        model.fit(self.X_binary, self.y_binary)
        y_pred = model.predict(self.X_binary)
        acc = accuracy_score(self.y_binary, y_pred)
        self.assertGreaterEqual(acc, 0.50)

    def test_fit_predict_multiclass(self):
        """Tests the fit and predict methods of the Perceptron class for multiclass classification."""
        model = Perceptron(max_iter=1000, learning_rate=0.01)
        model.fit(self.X_multiclass, self.y_multiclass)
        y_pred = model.predict(self.X_multiclass)
        acc = accuracy_score(self.y_multiclass, y_pred)
        self.assertGreaterEqual(acc, 0.50)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        model = Perceptron()
        with self.assertRaises(ValueError):
            model.fit(None, None)

    def test_invalid_predict(self):
        """Tests the predict method with invalid input."""
        model = Perceptron()
        with self.assertRaises(TypeError):
            model.predict(None)

    def test_get_params(self):
        """Tests the get_params method of the Perceptron class."""
        model = Perceptron(max_iter=1000, learning_rate=0.01)
        params = model.get_params()
        self.assertIn("max_iter", params)
        self.assertIn("learning_rate", params)

    def test_set_params(self):
        """Tests the set_params method of the Perceptron class."""
        model = Perceptron(max_iter=1000, learning_rate=0.01)
        model.set_params(max_iter=2000)
        self.assertEqual(model.max_iter, 2000)

    def test_set_params_invalid(self):
        """Tests the set_params method with invalid input."""
        model = Perceptron(max_iter=1000, learning_rate=0.01)
        with self.assertRaises(ValueError):
            model.set_params(invalid_param=0.1)


if __name__ == "__main__":
    unittest.main()
