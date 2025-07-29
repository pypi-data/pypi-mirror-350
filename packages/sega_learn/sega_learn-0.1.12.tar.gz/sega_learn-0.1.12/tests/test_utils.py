import os
import sys
import unittest

import numpy as np
import pandas as pd
from sklearn import metrics as sk_metrics

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.linear_models import *
from sega_learn.svm import *
from sega_learn.time_series import *
from sega_learn.trees import *
from sega_learn.utils import *
from sega_learn.utils import make_classification, make_regression, train_test_split
from tests.utils import BaseTest, suppress_print, synthetic_data_regression


# --- Helper function for creating seasonal data ---
def create_seasonal_data(length=100, period=12, amplitude=10, trend=0.1, noise_std=2):
    """Creates sample time series data with seasonality, trend, and noise."""
    time = np.arange(length)
    seasonal_component = amplitude * np.sin(2 * np.pi * time / period)
    trend_component = trend * time
    noise_component = np.random.normal(0, noise_std, length)
    return (
        trend_component + seasonal_component + noise_component + 50
    )  # Add constant offset


class TestPolynomialTransform(BaseTest):
    """Unit tests for the PolynomialTransform class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Polynomial Transform", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the PolynomialTransform instance for testing."""
        self.transform = PolynomialTransform(degree=2)

    def test_fit_transform(self):
        """Tests the fit_transform method of the Polynomial Transform class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=2, noise=0.1)
        X_transformed = self.transform.fit_transform(X)
        self.assertEqual(X_transformed.shape[1], 6)

    def test_fit(self):
        """Tests the fit method of the Polynomial Transform class."""
        X, y = synthetic_data_regression(n_samples=1000, n_features=2, noise=0.1)
        self.transform.fit(X)
        self.assertEqual(self.transform.degree, 2)

    def test_invalid_fit(self):
        """Tests the fit method with invalid input."""
        with self.assertRaises(AttributeError):
            self.transform.fit(None)

    def test_invalid_transform(self):
        """Tests the transform method with invalid input."""
        with self.assertRaises(AttributeError):
            self.transform.transform(None)


class TestDataPrep(BaseTest):
    """Unit tests for the DataPrep class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Data Prep", end="", flush=True)

    def test_one_hot_encode(self):
        """Tests the one_hot_encode method with one categorical column."""
        df = pd.DataFrame(
            {"A": [1, 2, 3, 4], "B": [5, 6, 7, 8], "C": ["a", "b", "a", "b"]}
        )
        df_encoded = DataPrep.one_hot_encode(df, [2])
        self.assertEqual(df_encoded.shape[1], 4)

    def test_one_hot_encode_multiple(self):
        """Tests the one_hot_encode method with multiple categorical columns."""
        df = pd.DataFrame(
            {"A": [1, 2, 3, 4], "B": ["a", "b", "a", "b"], "C": ["x", "y", "x", "y"]}
        )
        df_encoded = DataPrep.one_hot_encode(df, [1, 2])
        self.assertEqual(df_encoded.shape[1], 5)

    def test_one_hot_encode_invalid(self):
        """Tests the one_hot_encode method with no categorical columns."""
        df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8]})
        df_encoded = DataPrep.one_hot_encode(df, [])
        self.assertEqual(df_encoded.shape[1], 2)

    def test_one_hot_encode_empty(self):
        """Tests the one_hot_encode method with an empty DataFrame."""
        df = pd.DataFrame()
        df_encoded = DataPrep.one_hot_encode(df, [])
        self.assertEqual(df_encoded.shape[1], 0)

    def test_one_hot_encode_invalid_col(self):
        """Tests the one_hot_encode method with an invalid column index."""
        df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8]})
        with self.assertRaises(IndexError):
            DataPrep.one_hot_encode(df, [2])

    def test_one_hot_encode_dtype_pd(self):
        """Tests the one_hot_encode method with a non-numeric column."""
        df = pd.DataFrame({"A": [1, 2, 3, 4], "B": ["a", "b", "a", "b"]})
        df_encoded = DataPrep.one_hot_encode(df, [1])
        self.assertIsInstance(df_encoded, pd.DataFrame)

    def test_one_hot_encode_dtype_np(self):
        """Tests the one_hot_encode method with a numpy array."""
        data = np.array([[1, "a"], [2, "b"], [3, "a"], [4, "b"]])
        data_encoded = DataPrep.one_hot_encode(data, [1])
        self.assertIsInstance(data_encoded, np.ndarray)

    def test_find_categorical_columns(self):
        """Tests the find_categorical_columns method with one categorical column."""
        df = pd.DataFrame(
            {"A": [1, 2, 3, 4], "B": ["a", "b", "a", "b"], "C": [5, 6, 7, 8]}
        )
        categorical_cols = DataPrep.find_categorical_columns(df)
        self.assertEqual(categorical_cols, [1])

    def test_find_categorical_columns_multiple(self):
        """Tests the find_categorical_columns method with multiple categorical columns."""
        df = pd.DataFrame(
            {"A": ["a", "b", "a", "b"], "B": ["x", "y", "x", "y"], "C": [5, 6, 7, 8]}
        )
        categorical_cols = DataPrep.find_categorical_columns(df)
        self.assertEqual(categorical_cols, [0, 1])

    def test_find_categorical_columns_empty(self):
        """Tests the find_categorical_columns method with an empty DataFrame."""
        df = pd.DataFrame()
        categorical_cols = DataPrep.find_categorical_columns(df)
        self.assertEqual(categorical_cols, [])

    def test_find_categorical_columns_invalid(self):
        """Tests the find_categorical_columns method with no categorical columns."""
        df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8]})
        categorical_cols = DataPrep.find_categorical_columns(df)
        self.assertEqual(categorical_cols, [])

    def test_write_data(self):
        """Tests the write_data method."""
        df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8]})
        DataPrep.write_data(df, "test.csv")
        self.assertTrue(os.path.exists("test.csv"))
        os.remove("test.csv")

    def test_df_to_ndarray(self):
        """Tests the df_to_ndarray method."""
        df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8], "C": [9, 10, 11, 12]})
        X, y = DataPrep.df_to_ndarray(df, y_col=2)
        self.assertEqual(X.shape[1], 2)
        self.assertEqual(y.shape[0], 4)

    def test_k_split(self):
        """Tests the k_split method."""
        X = np.random.rand(100, 5)
        y = np.random.rand(100)
        X_folds, y_folds = DataPrep.k_split(X, y, k=5)
        self.assertEqual(len(X_folds), 5)
        self.assertEqual(len(y_folds), 5)
        self.assertEqual(X_folds[0].shape[0], 20)
        self.assertEqual(y_folds[0].shape[0], 20)

    def test_k_split_invalid(self):
        """Tests the k_split method with invalid input."""
        with self.assertRaises(TypeError):
            DataPrep.k_split(None, None, k=5)


class TestVotingRegressor(BaseTest):
    """Unit tests for the VotingRegressor class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Voting Regressor", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the VotingRegressor instance for testing."""
        self.X, self.y = make_regression(
            n_samples=100, n_features=5, noise=25, random_state=42
        )
        ols = OrdinaryLeastSquares()
        ols.fit(self.X, self.y)
        reg_tree = RegressorTree(max_depth=2)
        reg_tree.fit(self.X, self.y)
        gbr = GradientBoostedRegressor(num_trees=2)
        gbr.fit(self.X, self.y)
        self.voter = VotingRegressor(
            models=[ols, reg_tree, gbr], model_weights=[0.3, 0.3, 0.4]
        )

    def test_init(self):
        """Tests the initialization of the Voting Regressor class."""
        self.assertEqual(len(self.voter.models), 3)
        self.assertEqual(len(self.voter.model_weights), 3)

    def test_predict(self):
        """Tests the predict method of the Voting Regressor class."""
        y_pred = self.voter.predict(self.X)
        self.assertEqual(y_pred.shape[0], self.y.shape[0])

    def test_get_params(self):
        """Tests the get_params method of the Voting Regressor class."""
        params = self.voter.get_params()
        self.assertEqual(len(params), 2)

    def test_show_models(self):
        """Tests the show_models method of the Voting Regressor class."""
        with suppress_print():
            self.voter.show_models()


class TestForecastRegressor(BaseTest):
    """Unit tests for the ForecastRegressor class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Forcast Regressor", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the ForecastRegressor instance for testing."""
        self.seasonal_period = 4  # Simple seasonality
        self.time_series = create_seasonal_data(
            length=40, period=self.seasonal_period, trend=0.05, noise_std=1
        )
        self.time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.order = (1, 1, 1)  # Use simpler order for basic tests
        self.arima = ARIMA(order=self.order)
        self.arima.fit(self.time_series)

        self.order = (1, 1, 1)
        self.seasonal_order = (1, 1, 1, self.seasonal_period)  # P, D, Q, m
        self.sarima = SARIMA(order=self.order, seasonal_order=self.seasonal_order)
        self.sarima.fit(self.time_series)

        self.voter = ForecastRegressor(
            models=[self.arima, self.sarima], model_weights=[0.5, 0.5]
        )

    def test_init(self):
        """Tests the initialization of the Forcast Regressor class."""
        self.assertEqual(len(self.voter.models), 2)
        self.assertEqual(len(self.voter.model_weights), 2)

    def test_forecast(self):
        """Tests the forecast method of the Forcast Regressor class."""
        y_pred = self.voter.forecast(steps=2)
        self.assertEqual(y_pred.shape[0], 2)

    def test_get_params(self):
        """Tests the get_params method of the Forcast Regressor class."""
        params = self.voter.get_params()
        self.assertEqual(len(params), 2)

    def test_show_models(self):
        """Tests the show_models method of the Forcast Regressor class."""
        with suppress_print():
            self.voter.show_models()


class TestVotingClassifier(BaseTest):
    """Unit tests for the VotingClassifier class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Voting Classifier", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the VotingClassifier instance for testing."""
        self.X, self.y = make_classification(
            n_samples=100, n_features=5, n_classes=2, random_state=42
        )
        # Fit some base classifiers
        log = LogisticRegression(max_iter=100)
        log.fit(self.X, self.y)
        self.clf1 = log

        clf_tree = ClassifierTree(max_depth=3)
        clf_tree.fit(self.X, self.y)
        self.clf2 = clf_tree

        # Ensure LinearSVC uses {-1, 1} labels if needed, or adapt if it uses 0/1
        y_svm = np.where(self.y == 0, -1, 1)
        linear_svc = LinearSVC(max_iter=100)
        linear_svc.fit(self.X, y_svm)
        self.clf3 = linear_svc

        # Wrap LinearSVC predict to return consistent 0/1 output for testing hard voting
        original_predict_svc = self.clf3.predict
        self.clf3.predict = lambda x: np.where(original_predict_svc(x) == -1, 0, 1)

        self.estimators_hard = [self.clf1, self.clf2, self.clf3]
        self.weights = [0.2, 0.5, 0.3]

        self.voter_hard = VotingClassifier(estimators=self.estimators_hard)
        self.voter_hard_weighted = VotingClassifier(
            estimators=self.estimators_hard, weights=self.weights
        )

    def test_init_hard(self):
        """Tests the initialization of the Voting Classifier (hard)."""
        self.assertEqual(len(self.voter_hard.estimators), 3)
        self.assertIsNone(self.voter_hard.weights)  # Default weights are None

    def test_init_weights_mismatch(self):
        """Tests error if number of weights mismatches estimators."""
        with self.assertRaises(ValueError):
            VotingClassifier(
                estimators=self.estimators_hard, weights=[0.5, 0.5]
            )  # Need 3 weights

    def test_init_invalid_estimators(self):
        """Tests error if estimators list is empty or invalid."""
        with self.assertRaises(ValueError):
            VotingClassifier(estimators=[])
        with self.assertRaises(ValueError):
            VotingClassifier(estimators="not_a_list")
        with self.assertRaises(TypeError):  # If an object doesn't have predict
            VotingClassifier(estimators=[self.clf1, "not_a_classifier"])

    def test_predict_hard(self):
        """Tests the predict method (hard voting)."""
        y_pred = self.voter_hard.predict(self.X)
        self.assertEqual(y_pred.shape[0], self.y.shape[0])
        self.assertTrue(np.all(np.isin(y_pred, [0, 1])))  # Check labels are 0 or 1

    def test_predict_hard_weighted(self):
        """Tests the predict method (hard voting with weights)."""
        y_pred = self.voter_hard_weighted.predict(self.X)
        self.assertEqual(y_pred.shape[0], self.y.shape[0])
        self.assertTrue(np.all(np.isin(y_pred, [0, 1])))
        # Verify weights are used (predictions might differ from unweighted)
        y_pred_unweighted = self.voter_hard.predict(self.X)
        # It's possible they are the same by chance, but unlikely for many samples
        if len(self.X) > 100:  # Only assert difference if enough samples
            self.assertFalse(
                np.array_equal(y_pred, y_pred_unweighted),
                "Weighted prediction should differ from unweighted",
            )

    def test_get_params(self):
        """Tests the get_params method."""
        params = self.voter_hard_weighted.get_params()
        self.assertEqual(len(params), 2)  # Only estimators and weights now
        self.assertIn("estimators", params)
        self.assertIn("weights", params)
        np.testing.assert_array_equal(params["weights"], self.weights)

    def test_show_models(self):
        """Tests the show_models method."""
        with suppress_print():
            self.voter_hard.show_models()
            self.voter_hard_weighted.show_models()


class TestModelSelectionUtils(BaseTest):
    """Unit tests for the Model Selection Utility class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Model Selection Utils", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the Model Selection Utility instance for testing."""
        self.X, self.y = make_regression(
            n_samples=100, n_features=5, noise=25, random_state=42
        )
        self.num_tests = 100

    def test_get_param_combinations(self):
        """Tests the get_param_combinations method of the Model Selection Utility class."""
        param_grid = [{"alpha": [0.1, 1, 10], "fit_intercept": [True, False]}]
        param_combinations = ModelSelectionUtility.get_param_combinations(param_grid)
        self.assertEqual(len(param_combinations), 6)

    def test_get_param_combinations_invalid(self):
        """Tests the get_param_combinations method with invalid input."""
        with self.assertRaises(TypeError):
            ModelSelectionUtility.get_param_combinations(None)

    def test_get_param_combinations_empty(self):
        """Tests the get_param_combinations method with empty input."""
        with self.assertRaises(ValueError):
            ModelSelectionUtility.get_param_combinations([])

    def test_get_param_combinations_single(self):
        """Tests the get_param_combinations method with a single parameter."""
        param_grid = [{"alpha": [0.1, 1, 10]}]
        param_combinations = ModelSelectionUtility.get_param_combinations(param_grid)
        self.assertEqual(len(param_combinations), 3)

    def test_cross_validate(self):
        """Tests the cross_validate method of the Model Selection Utility class."""
        ols = OrdinaryLeastSquares
        mse_scores, _ = ModelSelectionUtility.cross_validate(
            ols, self.X, self.y, params={"fit_intercept": [True]}, cv=5
        )
        self.assertEqual(len(mse_scores), 5)
        for score in mse_scores:
            self.assertIsInstance(score, float)

    def test_cross_validate_invalid(self):
        """Tests the cross_validate method with invalid input."""
        with self.assertRaises(TypeError):
            ModelSelectionUtility.cross_validate(None, None, None, params=None, cv=5)

    def test_cross_validate_invalid_cv(self):
        """Tests the cross_validate method with invalid cv."""
        with self.assertRaises(UnboundLocalError):
            ModelSelectionUtility.cross_validate(
                OrdinaryLeastSquares, self.X, self.y, params=None, cv=0
            )

    def test_cross_validate_invalid_params(self):
        """Tests the cross_validate method with invalid params."""
        with self.assertRaises(TypeError):
            ModelSelectionUtility.cross_validate(
                OrdinaryLeastSquares, self.X, self.y, params=None, cv=5
            )

    def test_cross_validate_invalid_params_type(self):
        """Tests the cross_validate method with invalid params type."""
        with self.assertRaises(TypeError):
            ModelSelectionUtility.cross_validate(
                OrdinaryLeastSquares, self.X, self.y, params="params", cv=5
            )

    def test_cross_validate_cv_1(self):
        """Tests the cross_validate method with cv=1."""
        ols = OrdinaryLeastSquares
        with self.assertRaises(ValueError):
            mse_scores, _ = ModelSelectionUtility.cross_validate(
                ols, self.X, self.y, params={"fit_intercept": [True]}, cv=1
            )


class TestGridSearchCV(BaseTest):
    """Unit tests for the GridSearchCV class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting GridSearchCV", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the GridSearchCV instance for testing."""
        self.X_reg, self.y_reg = make_regression(
            n_samples=10, n_features=5, noise=25, random_state=42
        )
        self.X_class, self.y_class = make_classification(
            n_samples=10, n_features=5, n_classes=2, random_state=42
        )

    def test_init(self):
        """Tests the initialization of the GridSearchCV class."""
        grid_search = GridSearchCV(model=Ridge, param_grid=[{"alpha": [0.1, 1, 10]}])
        self.assertEqual(grid_search.model, Ridge)
        self.assertEqual(grid_search.param_grid, [{"alpha": [0.1, 1, 10]}])
        self.assertEqual(grid_search.cv, 5)
        self.assertEqual(grid_search.metric, "mse")
        self.assertEqual(grid_search.direction, "minimize")

    def test_param_combinations(self):
        """Tests the _get_param_combinations method of the GridSearchCV class."""
        grid_search = GridSearchCV(
            model=Ridge,
            param_grid=[{"alpha": [0.1, 1, 10], "fit_intercept": [True, False]}],
        )
        self.assertEqual(len(grid_search.param_combinations), 6)

    ### Linear Models ###
    def test_ols(self):
        """Tests the GridSearchCV class with the Ordinary Least Squares model."""
        ols = OrdinaryLeastSquares
        param_grid = [{"fit_intercept": [True, False]}]
        grid_search = GridSearchCV(model=ols, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_ridge(self):
        """Tests the GridSearchCV class with the Ridge model."""
        ridge = Ridge
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(model=ridge, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_lasso(self):
        """Tests the GridSearchCV class with the Lasso model."""
        lasso = Lasso
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(model=lasso, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_bayesian(self):
        """Tests the GridSearchCV class with the Bayesian Ridge model."""
        bayesian_ridge = Bayesian
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(model=bayesian_ridge, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_passiveAggReg(self):
        """Tests the GridSearchCV class with the Passive Aggressive Regressor model."""
        passive_agg = PassiveAggressiveRegressor
        param_grid = [{"C": [0.1, 1]}]
        grid_search = GridSearchCV(model=passive_agg, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_ransac(self):
        """Tests the GridSearchCV class with the RANSAC model."""
        ransac = RANSAC
        param_grid = [{"n": [2, 3], "d": [1, 2]}]
        grid_search = GridSearchCV(model=ransac, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_perceptron(self):
        """Tests the GridSearchCV class with the Perceptron model."""
        perceptron = Perceptron
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(model=perceptron, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_class, self.y_class)

    def test_logisticRegression(self):
        """Tests the GridSearchCV class with the Logistic Regression model."""
        logistic_regression = LogisticRegression
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(
            model=logistic_regression, param_grid=param_grid, cv=2
        )
        grid_search.fit(self.X_class, self.y_class)

    ### SVM ###
    def test_generalizedLinearSVC(self):
        """Tests the GridSearchCV class with the Generalized Linear SVC model."""
        generalized_linear_svc = GeneralizedSVC
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(
            model=generalized_linear_svc, param_grid=param_grid, cv=2
        )
        grid_search.fit(self.X_class, self.y_class)

    def test_generalizedLinearSVR(self):
        """Tests the GridSearchCV class with the Generalized Linear SVR model."""
        generalized_linear_svr = GeneralizedSVR
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(
            model=generalized_linear_svr, param_grid=param_grid, cv=2
        )
        grid_search.fit(self.X_reg, self.y_reg)

    def test_linearSVC(self):
        """Tests the GridSearchCV class with the Linear SVC model."""
        linear_svc = LinearSVC
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(model=linear_svc, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_class, self.y_class)

    def test_linearSVR(self):
        """Tests the GridSearchCV class with the Linear SVR model."""
        linear_svr = LinearSVR
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(model=linear_svr, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_oneClassSVM(self):
        """Tests the GridSearchCV class with the One Class SVM model."""
        one_class_svm = OneClassSVM
        param_grid = [{"max_iter": [10, 20]}]
        grid_search = GridSearchCV(model=one_class_svm, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_class, self.y_class)

    ### Trees ###
    def test_classifierTree(self):
        """Tests the GridSearchCV class with the Classifier Tree model."""
        classifier_tree = ClassifierTree
        param_grid = [{"max_depth": [2, 3]}]
        grid_search = GridSearchCV(model=classifier_tree, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_class, self.y_class)

    def test_regressorTree(self):
        """Tests the GridSearchCV class with the Regressor Tree model."""
        regressor_tree = RegressorTree
        param_grid = [{"max_depth": [2, 3], "min_samples_split": [2, 3]}]
        grid_search = GridSearchCV(model=regressor_tree, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_randomForestClassifier(self):
        """Tests the GridSearchCV class with the Random Forest Classifier model."""
        decision_tree = RandomForestClassifier
        param_grid = [{"n_estimators": [2, 3], "max_depth": [2], "n_jobs": [1]}]
        grid_search = GridSearchCV(model=decision_tree, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_class, self.y_class)

    def test_randomForestRegressor(self):
        """Tests the GridSearchCV class with the Random Forest Regressor model."""
        decision_tree = RandomForestRegressor
        param_grid = [{"n_estimators": [2, 3], "max_depth": [2], "n_jobs": [1]}]
        grid_search = GridSearchCV(model=decision_tree, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_gradientBoostiedRegressor(self):
        """Tests the GridSearchCV class with the Gradient Boosted Regressor model."""
        decision_tree = GradientBoostedRegressor
        param_grid = [{"num_trees": [3, 4]}]
        grid_search = GridSearchCV(model=decision_tree, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_reg, self.y_reg)

    def test_gradientBoostiedClassifier(self):
        """Tests the GridSearchCV class with the Gradient Boosted Classifier model."""
        decision_tree = GradientBoostedClassifier
        param_grid = [{"n_estimators": [3, 4]}]
        grid_search = GridSearchCV(model=decision_tree, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_class, self.y_class)

    def test_isoForest(self):
        """Tests the GridSearchCV class with the Isolation Forest model."""
        iso_forest = IsolationForest
        param_grid = [{"n_trees": [10, 20]}, {"n_jobs": [1]}]
        grid_search = GridSearchCV(model=iso_forest, param_grid=param_grid, cv=2)
        grid_search.fit(self.X_class, self.y_class)

    def test_invalid_param_grid(self):
        """Tests the GridSearchCV class with invalid param_grid."""
        with self.assertRaises(AssertionError):
            grid_search = GridSearchCV(model=Ridge, param_grid=None)
            grid_search.fit(self.X_reg, self.y_reg)


class TestRandomSearchCV(BaseTest):
    """Unit tests for the RandomSearchCV class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting RandomSearchCV", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the RandomSearchCV instance for testing."""
        self.X_reg, self.y_reg = make_regression(
            n_samples=10, n_features=5, noise=25, random_state=42
        )
        self.X_class, self.y_class = make_classification(
            n_samples=10, n_features=5, n_classes=2, random_state=42
        )

    def test_init(self):
        """Tests the initialization of the RandomSearchCV class."""
        rand_search = RandomSearchCV(
            model=Ridge, param_grid=[{"alpha": [0.1, 1, 10]}], iter=3
        )
        self.assertEqual(rand_search.model, Ridge)
        self.assertEqual(rand_search.param_grid, [{"alpha": [0.1, 1, 10]}])
        self.assertEqual(rand_search.cv, 5)
        self.assertEqual(rand_search.metric, "mse")
        self.assertEqual(rand_search.direction, "minimize")

    def test_param_combinations(self):
        """Tests the _get_param_combinations method of the RandomSearchCV class."""
        rand_search = RandomSearchCV(
            model=Ridge,
            param_grid=[{"alpha": [0.1, 1, 10], "fit_intercept": [True, False]}],
            iter=2,
        )
        self.assertEqual(len(rand_search.param_combinations), 6)

    ### Linear Models ###
    def test_ols(self):
        """Tests the RandomSearchCV class with the Ordinary Least Squares model."""
        ols = OrdinaryLeastSquares
        param_grid = [{"fit_intercept": [True, False]}]
        rand_search = RandomSearchCV(model=ols, param_grid=param_grid, cv=3, iter=2)
        rand_search.fit(self.X_reg, self.y_reg)

    def test_ridge(self):
        """Tests the RandomSearchCV class with the Ridge model."""
        ridge = Ridge
        param_grid = [{"max_iter": [10, 20, 30]}]
        rand_search = RandomSearchCV(model=ridge, param_grid=param_grid, cv=3, iter=2)
        rand_search.fit(self.X_reg, self.y_reg)

    def test_lasso(self):
        """Tests the RandomSearchCV class with the Lasso model."""
        lasso = Lasso
        param_grid = [{"max_iter": [10, 20, 30]}]
        rand_search = RandomSearchCV(model=lasso, param_grid=param_grid, cv=3, iter=2)
        rand_search.fit(self.X_reg, self.y_reg)

    def test_bayesian(self):
        """Tests the RandomSearchCV class with the Bayesian Ridge model."""
        bayesian_ridge = Bayesian
        param_grid = [{"max_iter": [10, 20, 30]}]
        rand_search = RandomSearchCV(
            model=bayesian_ridge, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_reg, self.y_reg)

    def test_passiveAggReg(self):
        """Tests the RandomSearchCV class with the Passive Aggressive Regressor model."""
        passive_agg = PassiveAggressiveRegressor
        param_grid = [{"C": [0.1, 1, 10]}]
        rand_search = RandomSearchCV(
            model=passive_agg, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_reg, self.y_reg)

    def test_perceptron(self):
        """Tests the RandomSearchCV class with the Perceptron model."""
        perceptron = Perceptron
        param_grid = [{"max_iter": [10, 20]}]
        rand_search = RandomSearchCV(
            model=perceptron, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    def test_logisticRegression(self):
        """Tests the RandomSearchCV class with the Logistic Regression model."""
        logistic_regression = LogisticRegression
        param_grid = [{"max_iter": [10, 20]}]
        rand_search = RandomSearchCV(
            model=logistic_regression, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    def test_ransac(self):
        """Tests the RandomSearchCV class with the RANSAC model."""
        ransac = RANSAC
        param_grid = [{"n": [2, 3], "d": [1], "k": [2]}]
        rand_search = RandomSearchCV(model=ransac, param_grid=param_grid, cv=3, iter=2)
        rand_search.fit(self.X_reg, self.y_reg)

    ### SVM ###
    def test_generalizedLinearSVC(self):
        """Tests the RandomSearchCV class with the Generalized Linear SVC model."""
        generalized_linear_svc = GeneralizedSVC
        param_grid = [{"max_iter": [10, 20]}]
        rand_search = RandomSearchCV(
            model=generalized_linear_svc, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    def test_generalizedLinearSVR(self):
        """Tests the RandomSearchCV class with the Generalized Linear SVR model."""
        generalized_linear_svr = GeneralizedSVR
        param_grid = [{"max_iter": [10, 20]}]
        rand_search = RandomSearchCV(
            model=generalized_linear_svr, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_reg, self.y_reg)

    def test_linearSVC(self):
        """Tests the RandomSearchCV class with the Linear SVC model."""
        linear_svc = LinearSVC
        param_grid = [{"max_iter": [10, 20]}]
        rand_search = RandomSearchCV(
            model=linear_svc, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    def test_linearSVR(self):
        """Tests the RandomSearchCV class with the Linear SVR model."""
        linear_svr = LinearSVR
        param_grid = [{"max_iter": [10, 20]}]
        rand_search = RandomSearchCV(
            model=linear_svr, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_reg, self.y_reg)

    def test_oneClassSVM(self):
        """Tests the RandomSearchCV class with the One Class SVM model."""
        one_class_svm = OneClassSVM
        param_grid = [{"max_iter": [10, 20]}]
        rand_search = RandomSearchCV(
            model=one_class_svm, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    ### Trees ###
    def test_classifierTree(self):
        """Tests the RandomSearchCV class with the Classifier Tree model."""
        classifier_tree = ClassifierTree
        param_grid = [{"max_depth": [2, 3]}]
        rand_search = RandomSearchCV(
            model=classifier_tree, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    def test_regressorTree(self):
        """Tests the RandomSearchCV class with the Regressor Tree model."""
        regressor_tree = RegressorTree
        param_grid = [{"max_depth": [2, 3], "min_samples_split": [2, 3]}]
        rand_search = RandomSearchCV(
            model=regressor_tree, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_reg, self.y_reg)

    def test_gradientBoostiedClassifier(self):
        """Tests the RandomSearchCV class with the Gradient Boosted Classifier model."""
        decision_tree = GradientBoostedClassifier
        param_grid = [{"n_estimators": [3, 4]}]
        rand_search = RandomSearchCV(
            model=decision_tree, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    def test_randomForestClassifier(self):
        """Tests the RandomSearchCV class with the Random Forest Classifier model."""
        decision_tree = RandomForestClassifier
        param_grid = [{"n_estimators": [2, 3], "max_depth": [2], "n_jobs": [1]}]
        rand_search = RandomSearchCV(
            model=decision_tree, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    def test_randomForestRegressor(self):
        """Tests the RandomSearchCV class with the Random Forest Regressor model."""
        decision_tree = RandomForestRegressor
        param_grid = [{"n_estimators": [2, 3], "max_depth": [2], "n_jobs": [1]}]
        rand_search = RandomSearchCV(
            model=decision_tree, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_reg, self.y_reg)

    def test_gradientBoostiedRegressor(self):
        """Tests the RandomSearchCV class with the Gradient Boosted Regressor model."""
        decision_tree = GradientBoostedRegressor
        param_grid = [{"num_trees": [3, 4]}]
        rand_search = RandomSearchCV(
            model=decision_tree, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_reg, self.y_reg)

    def test_isoForest(self):
        """Tests the RandomSearchCV class with the Isolation Forest model."""
        iso_forest = IsolationForest
        param_grid = [{"n_trees": [10, 20]}, {"n_jobs": [1]}]
        rand_search = RandomSearchCV(
            model=iso_forest, param_grid=param_grid, cv=3, iter=2
        )
        rand_search.fit(self.X_class, self.y_class)

    def test_invalid_iter(self):
        """Tests the RandomSearchCV class with invalid iter."""
        with self.assertRaises(AssertionError):
            rand_search = RandomSearchCV(
                model=Ridge, param_grid=[{"alpha": [0.1, 1, 10]}], iter=0
            )
            rand_search.fit(self.X_reg, self.y_reg)

    def test_iter_larger_than_param_combinations(self):
        """Tests the RandomSearchCV class with iter larger than param combinations."""
        with suppress_print():
            rand_search = RandomSearchCV(
                model=Ridge, param_grid=[{"max_iter": [10, 20, 30]}], iter=100_000_000
            )
            rand_search.fit(self.X_reg, self.y_reg)

    def test_invalid_param_grid(self):
        """Tests the RandomSearchCV class with invalid param_grid."""
        with self.assertRaises(AssertionError):
            rand_search = RandomSearchCV(model=Ridge, param_grid=None, iter=3)
            rand_search.fit(self.X_reg, self.y_reg)


class TestMetrics(BaseTest):
    """Unit tests for the Metrics class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Metrics", end="", flush=True)
        cls.num_tests = 100  # Define the variable for the number of tests

    def setUp(self):  # NOQA D201
        """Set up the Metrics instance for testing."""
        self.metrics = Metrics()

    def generate_regression_data(self):
        """Generate random regression data."""
        y_true, y_pred = make_regression(
            n_samples=100, n_features=1, noise=0.1, random_state=None
        )
        return y_true.flatten(), y_pred.flatten()

    def generate_classification_data(self):
        """Generate random classification data."""
        X, y_true = make_classification(
            n_samples=100, n_features=5, n_classes=2, random_state=None
        )
        y_pred = np.random.randint(0, 2, size=y_true.shape)
        y_pred_prob = np.random.rand(100, 2)
        y_pred_prob = y_pred_prob / y_pred_prob.sum(axis=1, keepdims=True)
        return y_true, y_pred, y_pred_prob

    # Regression Metrics
    def test_mse(self):
        """Tests the mean squared error method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred = self.generate_regression_data()
                mse = self.metrics.mean_squared_error(y_true, y_pred)
                sk_mse = sk_metrics.mean_squared_error(y_true, y_pred)
                self.assertEqual(mse, sk_mse)

    def test_r2(self):
        """Tests the r squared method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred = self.generate_regression_data()
                r2 = self.metrics.r_squared(y_true, y_pred)
                sk_r2 = sk_metrics.r2_score(y_true, y_pred)
                self.assertAlmostEqual(r2, sk_r2, places=4)

    def test_mae(self):
        """Tests the mean absolute error method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred = self.generate_regression_data()
                mae = self.metrics.mean_absolute_error(y_true, y_pred)
                sk_mae = sk_metrics.mean_absolute_error(y_true, y_pred)
                self.assertEqual(mae, sk_mae)

    def test_rmse(self):
        """Tests the root mean squared error method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred = self.generate_regression_data()
                rmse = self.metrics.root_mean_squared_error(y_true, y_pred)
                sk_rmse = np.sqrt(sk_metrics.mean_squared_error(y_true, y_pred))
                self.assertAlmostEqual(rmse, sk_rmse, places=4)

    def test_mape(self):
        """Tests the mean absolute percentage error method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred = self.generate_regression_data()
                mape = self.metrics.mean_absolute_percentage_error(y_true, y_pred)
                sk_mape = sk_metrics.mean_absolute_percentage_error(y_true, y_pred)
                self.assertEqual(mape, sk_mape)

    def test_mpe(self):
        """Tests the mean percentage error method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred = self.generate_regression_data()
                mpe = self.metrics.mean_percentage_error(y_true, y_pred)
                sk_mpe = np.mean((y_true - y_pred) / y_true)
                self.assertEqual(mpe, sk_mpe)

    # Classification Metrics
    def test_accuracy(self):
        """Tests the accuracy method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred, _ = self.generate_classification_data()
                accuracy = self.metrics.accuracy(y_true, y_pred)
                sk_accuracy = sk_metrics.accuracy_score(y_true, y_pred)
                self.assertEqual(accuracy, sk_accuracy)

    def test_precision(self):
        """Tests the precision method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred, _ = self.generate_classification_data()
                precision = self.metrics.precision(y_true, y_pred)
                sk_precision = sk_metrics.precision_score(y_true, y_pred)
                self.assertAlmostEqual(precision, sk_precision, places=4)

    def test_recall(self):
        """Tests the recall method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred, _ = self.generate_classification_data()
                recall = self.metrics.recall(y_true, y_pred)
                sk_recall = sk_metrics.recall_score(y_true, y_pred)
                self.assertAlmostEqual(recall, sk_recall, places=4)

    def test_f1_score(self):
        """Tests the f1 score method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred, _ = self.generate_classification_data()
                f1 = self.metrics.f1_score(y_true, y_pred)
                sk_f1 = sk_metrics.f1_score(y_true, y_pred)
                self.assertAlmostEqual(f1, sk_f1, places=4)

    def test_log_loss(self):
        """Tests the log loss method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, _, y_pred_prob = self.generate_classification_data()
                log_loss = self.metrics.log_loss(y_true, y_pred_prob)
                sk_log_loss = sk_metrics.log_loss(y_true, y_pred_prob)
                self.assertAlmostEqual(log_loss, sk_log_loss, places=4)

    def test_confusion_matrix(self):
        """Tests the confusion matrix method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred, _ = self.generate_classification_data()
                cm = self.metrics.confusion_matrix(y_true, y_pred)
                sk_cm = sk_metrics.confusion_matrix(y_true, y_pred)
                self.assertTrue(np.array_equal(cm, sk_cm))

    def test_show_confusion_matrix(self):
        """Tests the show confusion matrix method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred, _ = self.generate_classification_data()
                with suppress_print():
                    self.metrics.show_confusion_matrix(y_true, y_pred)

    def test_classification_report(self):
        """Tests the classification report method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred, _ = self.generate_classification_data()
                report = self.metrics.classification_report(y_true, y_pred)
                sk_report = sk_metrics.classification_report(
                    y_true, y_pred, output_dict=True
                )
                for cls in report:
                    self.assertAlmostEqual(
                        report[cls]["recall"], sk_report[str(cls)]["recall"], places=4
                    )
                    self.assertAlmostEqual(
                        report[cls]["precision"],
                        sk_report[str(cls)]["precision"],
                        places=4,
                    )
                    self.assertAlmostEqual(
                        report[cls]["f1-score"],
                        sk_report[str(cls)]["f1-score"],
                        places=4,
                    )
                    self.assertAlmostEqual(
                        report[cls]["support"], sk_report[str(cls)]["support"], places=4
                    )

    def test_show_classification_report(self):
        """Tests the show classification report method of the Metrics class."""
        for _ in range(self.num_tests):
            with self.subTest(i=_):
                y_true, y_pred, _ = self.generate_classification_data()
                with suppress_print():
                    self.metrics.show_classification_report(y_true, y_pred)


class TestDataAugmentation(BaseTest):
    """Unit tests for the Data Augmentation class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Data Augmentation", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the Data Augmentation instance for testing."""
        self.X, self.y = make_classification(
            n_samples=1000,
            n_features=20,
            n_classes=2,
            weights=[0.7, 0.3],
            random_state=42,
            class_sep=0.5,
        )
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        self.ros = RandomOverSampler(random_state=42)
        self.smote = SMOTE(random_state=42)
        self.rus = RandomUnderSampler(random_state=42)
        self.augmenter = Augmenter(
            techniques=[self.ros, self.smote, self.rus], verbose=False
        )

    def test_random_over_sampler(self):
        """Tests the Random Over Sampler method of the Data Augmentation class."""
        X_resampled, y_resampled = self.ros.fit_resample(self.X_train, self.y_train)
        self.assertEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))
        self.assertEqual(X_resampled.shape[0], 2 * np.sum(y_resampled == 0))

    def test_random_over_sampler_invalid(self):
        """Tests the Random Over Sampler method with invalid input."""
        with self.subTest("Invalid input"), self.assertRaises(TypeError):
            self.ros.fit_resample(None, None)
        with self.subTest("Invalid input type"), self.assertRaises(ValueError):
            self.ros.fit_resample("invalid_input", "invalid_input")
        with self.subTest("Invalid input shape"), self.assertRaises(ValueError):
            self.ros.fit_resample(np.random.rand(101, 20), np.random.rand(100, 20))

    def test_random_over_sampler_invalid_params(self):
        """Tests the Random Over Sampler method with invalid params."""
        with self.assertRaises(TypeError):
            ros = RandomOverSampler(
                random_state=42, sampling_strategy="invalid_strategy"
            )
            ros.fit_resample(self.X_train, self.y_train)

    def test_fit_random_over_sampler_invalid(self):
        """Tests the fit method of the Random Over Sampler with invalid input."""
        with self.assertRaises(AttributeError):
            ros = RandomOverSampler(random_state=42)
            ros.fit(None, None)

    def test_fit_random_over_sampler_invalid_params(self):
        """Tests the fit method of the Random Over Sampler with invalid params."""
        with self.assertRaises(AttributeError):
            ros = RandomOverSampler(random_state=42)
            ros.fit(self.X_train, None)

    def test_smote(self):
        """Tests the SMOTE method of the Data Augmentation class."""
        X_resampled, y_resampled = self.smote.fit_resample(self.X_train, self.y_train)
        self.assertGreaterEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))

    def test_smote_equal(self):
        """Tests the SMOTE method with force_equal parameter."""
        X_resampled, y_resampled = self.smote.fit_resample(
            self.X_train, self.y_train, force_equal=True
        )
        self.assertEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))

    def test_smote_invalid(self):
        """Tests the SMOTE method with invalid input."""
        with self.subTest("Invalid input"), self.assertRaises(TypeError):
            self.smote.fit_resample(None, None)
        with self.subTest("Invalid input type"), self.assertRaises(ValueError):
            self.smote.fit_resample("invalid_input", "invalid_input")
        with self.subTest("Invalid input shape"), self.assertRaises(ValueError):
            self.smote.fit_resample(np.random.rand(101, 20), np.random.rand(100, 20))

    def test_random_under_sampler(self):
        """Tests the Random Under Sampler method of the Data Augmentation class."""
        X_resampled, y_resampled = self.rus.fit_resample(self.X_train, self.y_train)
        self.assertEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))
        self.assertEqual(X_resampled.shape[0], 2 * np.sum(y_resampled == 0))

    def test_random_under_sampler_invalid(self):
        """Tests the Random Under Sampler method with invalid input."""
        with self.subTest("Invalid input"), self.assertRaises(TypeError):
            self.rus.fit_resample(None, None)
        with self.subTest("Invalid input type"), self.assertRaises(ValueError):
            self.rus.fit_resample("invalid_input", "invalid_input")
        with self.subTest("Invalid input shape"), self.assertRaises(ValueError):
            self.rus.fit_resample(np.random.rand(101, 20), np.random.rand(100, 20))

    def test_random_under_sampler_invalid_params(self):
        """Tests the Random Under Sampler method with invalid params."""
        with self.assertRaises(TypeError):
            rus = RandomUnderSampler(
                random_state=42, sampling_strategy="invalid_strategy"
            )
            rus.fit_resample(self.X_train, self.y_train)

    def test_fit_random_under_sampler_invalid(self):
        """Tests the fit method of the Random Under Sampler with invalid input."""
        with self.assertRaises(AttributeError):
            rus = RandomUnderSampler(random_state=42)
            rus.fit(None, None)

    def test_fit_random_under_sampler_invalid_params(self):
        """Tests the fit method of the Random Under Sampler with invalid params."""
        with self.assertRaises(AttributeError):
            rus = RandomUnderSampler(random_state=42)
            rus.fit(self.X_train, None)

    def test_augment(self):
        """Tests the augment method of the Data Augmentation class."""
        X_resampled, y_resampled = self.augmenter.augment(self.X, self.y)
        self.assertEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))

    def test_augment_with_multiple_techniques(self):
        """Tests the augment method with multiple techniques."""
        augmenter = Augmenter(techniques=[self.ros, self.smote], verbose=False)
        X_resampled, y_resampled = augmenter.augment(self.X, self.y)
        self.assertEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))

    def test_augment_with_one_technique(self):
        """Tests the augment method with one technique."""
        augmenter = Augmenter(techniques=[self.rus], verbose=False)
        X_resampled, y_resampled = augmenter.augment(self.X, self.y)
        self.assertEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))

    def test_augment_with_invalid_technique(self):
        """Tests the augment method with invalid technique."""
        invalid_technique = "invalid_technique"
        with self.assertRaises(ValueError):
            augmenter = Augmenter(techniques=[invalid_technique], verbose=False)
            augmenter.augment(self.X, self.y)

    def test_augment_with_invalid_input(self):
        """Tests the augment method with invalid input."""
        with self.assertRaises(IndexError):
            self.augmenter.augment(None, None)

    def test_augment_with_balanced_data(self):
        """Tests the augment method with balanced data."""
        X_balanced, y_balanced = self.ros.fit_resample(self.X, self.y)
        X_resampled, y_resampled = self.augmenter.augment(X_balanced, y_balanced)
        self.assertEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))

    def test_smote_with_force_equal(self):
        """Tests the SMOTE method with force_equal parameter."""
        X_resampled, y_resampled = self.smote.fit_resample(
            self.X_train, self.y_train, force_equal=True
        )
        self.assertEqual(np.sum(y_resampled == 0), np.sum(y_resampled == 1))

    def test_augment_with_empty_techniques(self):
        """Tests the augment method with an empty list of techniques."""
        augmenter = Augmenter(techniques=[], verbose=False)
        X_resampled, y_resampled = augmenter.augment(self.X, self.y)
        self.assertEqual(X_resampled.shape, self.X.shape)
        self.assertEqual(y_resampled.shape, self.y.shape)

    def test_augment_with_invalid_techniques(self):
        """Tests the augment method with invalid techniques."""
        invalid_technique = "invalid_technique"
        with self.assertRaises(ValueError):
            augmenter = Augmenter(
                techniques=[self.rus, invalid_technique], verbose=False
            )
            augmenter.augment(self.X, self.y)


class TestDataDecomposition(BaseTest):
    """Unit tests for the Data Decomposition class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Decomposition", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the Decomposition instance for testing."""
        self.X = np.random.rand(100, 5)

    def test_pca_fit_transform(self):
        """Tests the fit_transform method of the PCA class."""
        pca = PCA(n_components=2)
        X_transformed = pca.fit_transform(self.X)
        self.assertEqual(X_transformed.shape[1], 2)
        self.assertEqual(pca.get_components().shape[1], 2)

    def test_svd_fit_transform(self):
        """Tests the fit_transform method of the SVD class."""
        svd = SVD(n_components=2)
        X_transformed = svd.fit_transform(self.X)
        self.assertEqual(X_transformed.shape[1], 2)
        self.assertEqual(svd.get_singular_values().shape[0], 2)

    def test_svd_get_singular_values(self):
        """Tests the get_singular_values method of the SVD class."""
        svd = SVD(n_components=2)
        svd.fit(self.X)
        singular_values = svd.get_singular_values()
        self.assertEqual(singular_values.shape[0], 2)

    def test_pca_invalid_input(self):
        """Tests the PCA class with invalid input."""
        pca = PCA(n_components=2)
        with self.assertRaises(ValueError):
            pca.fit("invalid_input")
        with self.assertRaises(ValueError):
            pca.fit(np.random.rand(100))
        with self.assertRaises(ValueError):
            pca.fit(np.random.rand(100, 1))
        with self.assertRaises(ValueError):
            pca.transform("invalid_input")
        with self.assertRaises(ValueError):
            pca.transform(np.random.rand(100))
        with self.assertRaises(ValueError):
            pca.inverse_transform("invalid_input")
        with self.assertRaises(ValueError):
            pca.inverse_transform(np.random.rand(100))

    def test_svd_invalid_input(self):
        """Tests the SVD class with invalid input."""
        svd = SVD(n_components=2)
        with self.assertRaises(ValueError):
            svd.fit("invalid_input")
        with self.assertRaises(ValueError):
            svd.fit(np.random.rand(100))
        with self.assertRaises(ValueError):
            svd.fit(np.random.rand(1, 100))
        with self.assertRaises(ValueError):
            svd.transform("invalid_input")
        with self.assertRaises(ValueError):
            svd.transform(np.random.rand(100))


if __name__ == "__main__":
    unittest.main()
