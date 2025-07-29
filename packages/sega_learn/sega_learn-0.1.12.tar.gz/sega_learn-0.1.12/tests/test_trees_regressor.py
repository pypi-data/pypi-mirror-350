import os
import sys
import unittest

import numpy as np

# Ensure the module path is correct
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.trees import *
from tests.utils import BaseTest

# Import utility functions if available
try:
    from tests.utils import suppress_print, synthetic_data_regression
except ImportError:
    # Define simple versions if utils are not available
    print("Warning: tests.utils not found, using basic implementations.")
    import contextlib
    import io

    @contextlib.contextmanager
    def suppress_print():
        """Suppress print output."""
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            yield
        finally:
            sys.stdout = old_stdout

    def synthetic_data_regression(n_samples=50, n_features=5, random_state=42):
        """Generate synthetic data for testing."""
        rng = np.random.RandomState(random_state)
        X = rng.rand(n_samples, n_features)
        true_coef = rng.rand(n_features)
        y = X @ true_coef + rng.normal(0, 0.5, n_samples)
        return X, y


# Consistent parameters for tests
N_SAMPLES = 50
N_FEATURES = 4
RANDOM_STATE = 42
MIN_SAMPLES_SPLIT = 5


class TestRegressorTreeUtility(BaseTest):
    """Tests for the updated RegressorTreeUtility class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Regressor Tree Utility", end="", flush=True)
        cls.X, cls.y = synthetic_data_regression(
            n_samples=N_SAMPLES, n_features=N_FEATURES, random_state=RANDOM_STATE
        )
        cls.n_features = cls.X.shape[1]
        # Initialize utility once for class if methods are static or pure
        # Or initialize in setUp for each test if state matters (it does here due to _X, _y)

    def setUp(self):
        """Sets up the RegressorTreeUtility instance for testing."""
        # Need to reinstantiate for each test as it holds refs to X, y
        self.utility = RegressorTreeUtility(
            self.X,
            self.y,
            min_samples_split=MIN_SAMPLES_SPLIT,
            n_features=self.n_features,
        )
        self.all_indices = np.arange(self.X.shape[0])

    def test_init(self):
        """Tests the initialization of the RegressorTreeUtility class."""
        self.assertEqual(self.utility.min_samples_split, MIN_SAMPLES_SPLIT)
        self.assertIsInstance(self.utility._X, np.ndarray)
        self.assertIsInstance(self.utility._y, np.ndarray)
        self.assertEqual(self.utility._X.shape, (N_SAMPLES, N_FEATURES))
        self.assertEqual(self.utility._y.shape, (N_SAMPLES,))

    def test_calculate_variance(self):
        """Tests calculate_variance with all indices."""
        indices = self.all_indices
        expected_variance = np.var(self.y[indices])
        calculated_variance = self.utility.calculate_variance(indices)
        self.assertAlmostEqual(calculated_variance, expected_variance, places=6)

    def test_calculate_variance_invalid_indices(self):
        """Tests calculate_variance with invalid indices."""
        indices = np.array([0, 1, 2, 3, 4, N_SAMPLES + 1])
        with self.assertRaises(IndexError):
            self.utility.calculate_variance(indices)

    def test_calculate_variance_single_index(self):
        """Tests calculate_variance with a single index."""
        indices = np.array([0])
        expected_variance = 0.0
        calculated_variance = self.utility.calculate_variance(indices)
        self.assertEqual(calculated_variance, expected_variance)

    def test_calculate_variance_multiple_indices(self):
        """Tests calculate_variance with multiple indices."""
        indices = np.array([0, 1, 2, 3, 4])
        if len(indices) > N_SAMPLES:
            indices = indices[:N_SAMPLES]
        expected_variance = np.var(self.y[indices])
        calculated_variance = self.utility.calculate_variance(indices)
        self.assertAlmostEqual(calculated_variance, expected_variance, places=6)

    def test_calculate_variance_sample_weights(self):
        """Tests calculate_variance with sample weights."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array([1, 2, 3, 4, 5])
        if len(indices) > N_SAMPLES:
            indices = indices[:N_SAMPLES]
        calculated_variance = self.utility.calculate_variance(indices, sample_weights)
        self.assertGreater(calculated_variance, 0)  # Variance should be positive

    def test_calculate_variance_invalid_sample_weights(self):
        """Tests calculate_variance with invalid sample weights."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array([1, 2])
        with self.assertRaises((ValueError, IndexError)):
            self.utility.calculate_variance(indices, sample_weights)

    def test_calculate_variance_non_numeric_sample_weights(self):
        """Tests calculate_variance with non-numeric sample weights."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array(["a", "b", "c", "d", "e"])
        with self.assertRaises(TypeError):
            self.utility.calculate_variance(indices, sample_weights)

    def test_calculate_variance_non_numeric_indices(self):
        """Tests calculate_variance with non-numeric indices."""
        indices = np.array(["a", "b", "c", "d", "e"])
        with self.assertRaises((TypeError, IndexError)):
            self.utility.calculate_variance(indices)

    def test_calculate_variance_sample_weights_shape_mismatch(self):
        """Tests calculate_variance with sample weights of different shape."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.utility.calculate_variance(indices, sample_weights)

    def test_calculate_variance_sample_weights_empty(self):
        """Tests calculate_variance with empty sample weights."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array([])
        with self.assertRaises((ValueError, IndexError)):
            self.utility.calculate_variance(indices, sample_weights)

    def test_calculate_variance_subset(self):
        """Tests calculate_variance with a subset of indices."""
        indices = np.array([0, 5, 10, 15, 20])
        if len(indices) > N_SAMPLES:
            indices = indices[:N_SAMPLES]  # Adjust if N_SAMPLES is small
        expected_variance = np.var(self.y[indices])
        calculated_variance = self.utility.calculate_variance(indices)
        self.assertAlmostEqual(calculated_variance, expected_variance, places=6)

    def test_calculate_variance_empty(self):
        """Tests calculate_variance with an empty index list."""
        indices = np.array([], dtype=int)
        expected_variance = 0.0
        calculated_variance = self.utility.calculate_variance(indices)
        self.assertEqual(calculated_variance, expected_variance)

    def test_calculate_variance_single_value_indices(self):
        """Tests calculate_variance with indices pointing to the same value (if possible)."""
        # Create data where some values are identical
        X_const, y_const = synthetic_data_regression(n_samples=10, n_features=2)
        y_const[:5] = 5.0
        utility_const = RegressorTreeUtility(X_const, y_const, 2, 2)
        indices = np.arange(5)  # Indices pointing to the value 5.0
        expected_variance = 0.0
        calculated_variance = utility_const.calculate_variance(indices)
        self.assertEqual(calculated_variance, expected_variance)

    def test_calculate_leaf_value(self):
        """Tests calculate_leaf_value with all indices."""
        indices = self.all_indices
        expected_value = np.mean(self.y[indices])
        calculated_value = self.utility.calculate_leaf_value(indices)
        self.assertAlmostEqual(calculated_value, expected_value, places=6)

    def test_calculate_leaf_value_subset(self):
        """Tests calculate_leaf_value with a subset of indices."""
        indices = np.array([1, 6, 11, 16, 21])
        if len(indices) > N_SAMPLES:
            indices = indices[:N_SAMPLES]
        expected_value = np.mean(self.y[indices])
        calculated_value = self.utility.calculate_leaf_value(indices)
        self.assertAlmostEqual(calculated_value, expected_value, places=6)

    def test_calculate_leaf_value_empty(self):
        """Tests calculate_leaf_value with empty indices."""
        indices = np.array([], dtype=int)
        calculated_value = self.utility.calculate_leaf_value(indices)
        self.assertTrue(np.isnan(calculated_value))

    def test_calculate_leaf_value_single_index(self):
        """Tests calculate_leaf_value with a single index."""
        indices = np.array([0])
        expected_value = self.y[0]
        calculated_value = self.utility.calculate_leaf_value(indices)
        self.assertEqual(calculated_value, expected_value)

    def test_calculate_leaf_value_invalid_indices(self):
        """Tests calculate_leaf_value with invalid indices."""
        indices = np.array([0, 1, 2, 3, 4, N_SAMPLES + 1])
        with self.assertRaises(IndexError):
            self.utility.calculate_leaf_value(indices)

    def test_calculate_leaf_value_non_numeric_indices(self):
        """Tests calculate_leaf_value with non-numeric indices."""
        indices = np.array(["a", "b", "c", "d", "e"])
        with self.assertRaises((TypeError, IndexError)):
            self.utility.calculate_leaf_value(indices)

    def test_calculate_leaf_value_sample_weights(self):
        """Tests calculate_leaf_value with sample weights."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array([1, 2, 3, 4, 5])
        if len(indices) > N_SAMPLES:
            indices = indices[:N_SAMPLES]
        calculated_value = self.utility.calculate_leaf_value(indices, sample_weights)
        expected_value = np.average(
            self.y[indices], weights=sample_weights[: len(indices)]
        )
        self.assertAlmostEqual(calculated_value, expected_value, places=6)

    def test_calculate_leaf_value_invalid_sample_weights(self):
        """Tests calculate_leaf_value with invalid sample weights."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array([1, 2])
        with self.assertRaises((ValueError, IndexError)):
            self.utility.calculate_leaf_value(indices, sample_weights)

    def test_calculate_leaf_value_non_numeric_sample_weights(self):
        """Tests calculate_leaf_value with non-numeric sample weights."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array(["a", "b", "c", "d", "e"])
        with self.assertRaises(TypeError):
            self.utility.calculate_leaf_value(indices, sample_weights)

    def test_calculate_leaf_value_sample_weights_shape_mismatch(self):
        """Tests calculate_leaf_value with sample weights of different shape."""
        indices = np.array([0, 1, 2, 3, 4])
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.utility.calculate_leaf_value(indices, sample_weights)

    def test_best_split(self):
        """Tests the best_split method returns the correct structure."""
        indices = self.all_indices
        # Ensure enough samples to potentially split
        if len(indices) >= self.utility.min_samples_split:
            best_split = self.utility.best_split(indices)

            # Check if a split was found (possible not to find one, e.g., pure node)
            if best_split is not None:
                self.assertIsInstance(best_split, dict)
                self.assertIn("feature_idx", best_split)
                self.assertIn("threshold", best_split)
                self.assertIn("indices_left", best_split)
                self.assertIn("indices_right", best_split)
                self.assertIn("info_gain", best_split)
                self.assertIsInstance(best_split["feature_idx"], (int, np.integer))
                self.assertIsInstance(
                    best_split["threshold"], (float, np.floating, np.integer)
                )  # Percentile can be int
                self.assertIsInstance(best_split["indices_left"], np.ndarray)
                self.assertIsInstance(best_split["indices_right"], np.ndarray)
                self.assertIsInstance(best_split["info_gain"], float)
                self.assertGreater(
                    best_split["info_gain"], 0
                )  # A valid split must have positive gain

                # Check if indices partition correctly
                left_set = set(best_split["indices_left"])
                right_set = set(best_split["indices_right"])
                original_set = set(indices)
                self.assertEqual(left_set.union(right_set), original_set)
                self.assertTrue(left_set.isdisjoint(right_set))
                self.assertGreater(len(left_set), 0)
                self.assertGreater(len(right_set), 0)
            else:
                # Handle case where no split is found (e.g., node is pure or nearly pure)
                pass  # Okay if no split found
        else:
            # If not enough samples, best_split should return None
            best_split = self.utility.best_split(indices)
            self.assertIsNone(best_split)

    def test_best_split_empty_indices(self):
        """Tests best_split with empty indices."""
        indices = np.array([], dtype=int)
        best_split = self.utility.best_split(indices)
        self.assertIsNone(best_split)  # Should return None if not enough samples

    def test_best_split_insufficient_samples(self):
        """Tests best_split when n_samples < min_samples_split."""
        indices = self.all_indices[: self.utility.min_samples_split - 1]
        if len(indices) > 0:  # Only run if we can actually select fewer samples
            best_split = self.utility.best_split(indices)
            self.assertIsNone(best_split)

    def test_best_split_single_index(self):
        """Tests best_split with a single index."""
        indices = np.array([0])
        best_split = self.utility.best_split(indices)
        self.assertIsNone(best_split)

    def test_best_split_single_value(self):
        """Tests best_split with a single value dataset."""
        X_single = self.X[0:1, :]
        y_single = self.y[0:1]
        utility_single = RegressorTreeUtility(X_single, y_single, 2, 2)
        indices = np.array([0])
        best_split = utility_single.best_split(indices)
        self.assertIsNone(best_split)

    def test_best_split_non_numeric_indices(self):
        """Tests best_split with non-numeric indices."""
        indices = np.array(["a", "b", "c", "d", "e"])
        with self.assertRaises((TypeError, IndexError)):
            self.utility.best_split(indices)

    def test_best_split_invalid_indices(self):
        """Tests best_split with invalid indices."""
        indices = np.array([0, 1, 2, 3, 4, N_SAMPLES + 1])
        with self.assertRaises(IndexError):
            self.utility.best_split(indices)

    def test_best_split_sample_weights(self):
        """Tests best_split with sample weights."""
        indices = self.all_indices
        sample_weights = np.random.rand(len(indices))  # Random weights for testing
        best_split = self.utility.best_split(indices, sample_weights)

        if best_split is not None:
            self.assertIsInstance(best_split, dict)
            self.assertIn("feature_idx", best_split)
            self.assertIn("threshold", best_split)
            self.assertIn("indices_left", best_split)
            self.assertIn("indices_right", best_split)
            self.assertIn("info_gain", best_split)
            self.assertGreater(best_split["info_gain"], 0)

            left_set = set(best_split["indices_left"])
            right_set = set(best_split["indices_right"])
            original_set = set(indices)
            self.assertEqual(left_set.union(right_set), original_set)
            self.assertTrue(left_set.isdisjoint(right_set))
            self.assertGreater(len(left_set), 0)
            self.assertGreater(len(right_set), 0)
        else:
            self.assertIsNone(best_split)  # Handle case where no split is found

    def test_best_split_invalid_sample_weights(self):
        """Tests best_split with invalid sample weights."""
        indices = self.all_indices
        sample_weights = np.array([1, 2])
        with self.assertRaises((ValueError, IndexError)):
            self.utility.best_split(indices, sample_weights)

    def test_best_split_non_numeric_sample_weights(self):
        """Tests best_split with non-numeric sample weights."""
        indices = self.all_indices
        sample_weights = np.array(["a", "b", "c", "d", "e"])
        with self.assertRaises((TypeError, IndexError)):
            self.utility.best_split(indices, sample_weights)

    def test_best_split_sample_weights_shape_mismatch(self):
        """Tests best_split with sample weights of different shape."""
        indices = self.all_indices
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.utility.best_split(indices, sample_weights)

    def test_best_split_sample_weights_empty(self):
        """Tests best_split with empty sample weights."""
        indices = self.all_indices
        sample_weights = np.array([])
        with self.assertRaises((ValueError, IndexError)):
            self.utility.best_split(indices, sample_weights)

    def test_best_split_min_samples_split(self):
        """Tests best_split with min_samples_split."""
        indices = self.all_indices[: self.utility.min_samples_split - 1]
        best_split = self.utility.best_split(indices)
        self.assertIsNone(best_split)

    def test_best_split_min_samples_split_large(self):
        """Tests best_split with a large min_samples_split."""
        indices = self.all_indices[: self.utility.min_samples_split + 1]
        best_split = self.utility.best_split(indices)
        self.assertIsNotNone(best_split)

    def test_best_split_single_value_indices(self):
        """Tests best_split with indices pointing to the same value."""
        # Create data where some values are identical
        X_const, y_const = synthetic_data_regression(n_samples=10, n_features=2)
        y_const[:5] = 5.0
        utility_const = RegressorTreeUtility(X_const, y_const, 2, 2)
        indices = np.arange(5)
        best_split = utility_const.best_split(indices)
        self.assertIsNone(best_split)  # No split should be found


class TestRegressorTree(BaseTest):
    """Tests for the updated RegressorTree class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Regressor Tree", end="", flush=True)
        cls.X, cls.y = synthetic_data_regression(
            n_samples=N_SAMPLES, n_features=N_FEATURES, random_state=RANDOM_STATE
        )
        # Create a separate test set
        cls.X_test, cls.y_test = synthetic_data_regression(
            n_samples=20, n_features=N_FEATURES, random_state=RANDOM_STATE + 1
        )

    def setUp(self):
        """Sets up the RegressorTree instance for testing."""
        self.tree = RegressorTree(max_depth=3, min_samples_split=MIN_SAMPLES_SPLIT)

    def test_init(self):
        """Tests the initialization of the RegressorTree class."""
        self.assertEqual(self.tree.max_depth, 3)
        self.assertEqual(self.tree.min_samples_split, MIN_SAMPLES_SPLIT)
        self.assertDictEqual(self.tree.tree, {})
        self.assertIsNone(self.tree._X)  # Should be None before fit

    def test_fit(self):
        """Tests the fit method populates the tree."""
        self.tree.fit(self.X, self.y)
        self.assertIsInstance(self.tree.tree, dict)
        self.assertGreater(len(self.tree.tree), 0)  # Tree should not be empty
        self.assertIsNotNone(self.tree._X)  # Should be set after fit
        self.assertEqual(self.tree._X.shape, self.X.shape)

    def test_fit_empty(self):
        """Tests the fit method with an empty dataset."""
        X_empty = np.empty((0, N_FEATURES))
        y_empty = np.empty((0,))
        # Expect ValueError due to check inside fit now
        with self.assertRaises(ValueError):
            self.tree.fit(X_empty, y_empty)

    def test_fit_single_value(self):
        """Tests the fit method with a single value dataset."""
        X_single = self.X[0:1, :]
        y_single = self.y[0:1]
        self.tree.fit(X_single, y_single)
        # Single value, leaf node expected immediately
        self.assertIn("value", self.tree.tree)
        self.assertAlmostEqual(self.tree.tree["value"], y_single[0])

    def test_fit_pure_values(self):
        """Tests fitting when all target values are the same."""
        X_pure = self.X[:10]
        y_pure = np.full(10, self.y[0])  # All same value
        self.tree.fit(X_pure, y_pure)
        self.assertIn("value", self.tree.tree)
        self.assertAlmostEqual(self.tree.tree["value"], self.y[0])

    def test_fit_max_depth_limit(self):
        """Tests fitting stops at max_depth."""
        self.tree = RegressorTree(max_depth=1, min_samples_split=2)  # Very shallow
        self.tree.fit(self.X, self.y)
        self.assertIn("feature_idx", self.tree.tree)  # Should have split at root
        self.assertIn("left", self.tree.tree)
        self.assertIn("right", self.tree.tree)
        # Children should be leaf nodes
        self.assertIn("value", self.tree.tree["left"])
        self.assertIn("value", self.tree.tree["right"])

    def test_fit_sample_weights(self):
        """Tests fitting with sample weights."""
        sample_weights = np.random.rand(self.X.shape[0])
        self.tree.fit(self.X, self.y, sample_weight=sample_weights)
        # Check if tree structure is still valid
        self.assertIsInstance(self.tree.tree, dict)
        self.assertGreater(len(self.tree.tree), 0)

    def test_fit_invalid_sample_weights(self):
        """Tests fitting with invalid sample weights."""
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.tree.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_non_numeric_sample_weights(self):
        """Tests fitting with non-numeric sample weights."""
        sample_weights = np.array(["a", "b", "c"])
        with self.assertRaises((ValueError, IndexError)):
            self.tree.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_sample_weights_shape_mismatch(self):
        """Tests fitting with sample weights of different shape."""
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.tree.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_sample_weights_empty(self):
        """Tests fitting with empty sample weights."""
        sample_weights = np.array([])
        with self.assertRaises((ValueError, IndexError)):
            self.tree.fit(self.X, self.y, sample_weight=sample_weights)

    def test_predict_before_fit(self):
        """Tests prediction before fitting."""
        with self.assertRaises(RuntimeError):
            self.tree.predict(self.X_test)

    def test_predict_after_fit(self):
        """Tests prediction after fitting returns correct shape."""
        self.tree.fit(self.X, self.y)
        predictions = self.tree.predict(self.X_test)
        self.assertIsInstance(predictions, np.ndarray)
        self.assertEqual(predictions.shape, (self.X_test.shape[0],))

    def test_predict_single_sample(self):
        """Tests prediction for a single sample."""
        self.tree.fit(self.X, self.y)
        single_sample = self.X_test[0, :]
        prediction = self.tree.predict(single_sample)  # Pass 1D array
        self.assertIsInstance(prediction, np.ndarray)
        self.assertEqual(prediction.shape, (1,))
        self.assertIsInstance(prediction[0], (float, np.floating))

    def test_predict_batch(self):
        """Tests prediction for a batch of samples."""
        self.tree.fit(self.X, self.y)
        batch_samples = self.X_test[:5]
        predictions = self.tree.predict(batch_samples)
        self.assertIsInstance(predictions, np.ndarray)
        self.assertEqual(predictions.shape, (5,))

    def test_predict_returns_float(self):
        """Tests that predictions are numeric."""
        self.tree.fit(self.X, self.y)
        predictions = self.tree.predict(self.X_test)
        self.assertTrue(np.issubdtype(predictions.dtype, np.number))
        # Check for NaNs which might indicate traversal issues
        self.assertFalse(np.isnan(predictions).any(), "NaN values found in prediction")


class TestRandomForestRegressor(BaseTest):
    """Tests for the updated RandomForestRegressor class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Random Forest Regressor", end="", flush=True)
        cls.X, cls.y = synthetic_data_regression(
            n_samples=N_SAMPLES, n_features=N_FEATURES, random_state=RANDOM_STATE
        )
        cls.X_test, cls.y_test = synthetic_data_regression(
            n_samples=20, n_features=N_FEATURES, random_state=RANDOM_STATE + 1
        )

    def setUp(self):
        """Sets up the RandomForestRegressor instance for testing."""
        self.rf = RandomForestRegressor(
            n_estimators=5,  # Fewer trees for faster tests
            max_depth=3,
            min_samples_split=MIN_SAMPLES_SPLIT,
            random_seed=RANDOM_STATE,
            n_jobs=1,  # Use 1 job for deterministic testing if needed, -1 otherwise
        )

    def test_init(self):
        """Tests the initialization of the RandomForestRegressor class."""
        self.assertEqual(self.rf.n_estimators, 5)
        self.assertEqual(self.rf.max_depth, 3)
        self.assertEqual(self.rf.min_samples_split, MIN_SAMPLES_SPLIT)
        self.assertEqual(self.rf.random_state, RANDOM_STATE)
        self.assertIsInstance(self.rf.trees, list)
        self.assertEqual(len(self.rf.trees), 0)

    def test_fit(self):
        """Tests the fit method of the RandomForestRegressor class."""
        self.rf.fit(self.X, self.y)
        self.assertEqual(len(self.rf.trees), self.rf.n_estimators)
        self.assertIsInstance(self.rf.trees[0], RegressorTree)
        # Check if trees seem fitted (have structure)
        self.assertGreater(len(self.rf.trees[0].tree), 0)

    def test_fit_empty(self):
        """Tests the fit method with an empty dataset."""
        X_empty = np.empty((0, N_FEATURES))
        y_empty = np.empty((0,))
        with self.assertRaises(ValueError):
            self.rf.fit(X_empty, y_empty)

    def test_fit_single_value(self):
        """Tests the fit method with a single value dataset."""
        X_single = self.X[0:1, :]
        y_single = self.y[0:1]
        self.rf.fit(X_single, y_single)
        self.assertEqual(len(self.rf.trees), self.rf.n_estimators)
        self.assertIsInstance(self.rf.trees[0], RegressorTree)

    def test_fit_sample_weights(self):
        """Tests fitting with sample weights."""
        sample_weights = np.random.rand(self.X.shape[0])
        self.rf.fit(self.X, self.y, sample_weight=sample_weights)
        # Check if trees seem fitted (have structure)
        self.assertEqual(len(self.rf.trees), self.rf.n_estimators)

    def test_fit_invalid_sample_weights(self):
        """Tests fitting with invalid sample weights."""
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.rf.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_non_numeric_sample_weights(self):
        """Tests fitting with non-numeric sample weights."""
        sample_weights = np.array(["a", "b", "c"])
        with self.assertRaises((ValueError, IndexError)):
            self.rf.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_sample_weights_shape_mismatch(self):
        """Tests fitting with sample weights of different shape."""
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.rf.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_sample_weights_empty(self):
        """Tests fitting with empty sample weights."""
        sample_weights = np.array([])
        with self.assertRaises((ValueError, IndexError)):
            self.rf.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_sample_weights_none(self):
        """Tests fitting with None sample weights."""
        self.rf.fit(self.X, self.y, sample_weight=None)
        # Check if trees seem fitted (have structure)
        self.assertEqual(len(self.rf.trees), self.rf.n_estimators)

    def test_predict_before_fit(self):
        """Tests predict before fitting."""
        with self.assertRaises(RuntimeError):
            self.rf.predict(self.X_test)

    def test_predict(self):
        """Tests the predict method after fitting."""
        self.rf.fit(self.X, self.y)
        predictions = self.rf.predict(self.X_test)
        self.assertEqual(predictions.shape, (self.X_test.shape[0],))
        self.assertIsInstance(predictions, np.ndarray)
        self.assertTrue(np.issubdtype(predictions.dtype, np.number))
        self.assertFalse(np.isnan(predictions).any(), "NaN values found in prediction")

    def test_predict_empty_input(self):
        """Tests predict with an empty input array X."""
        self.rf.fit(self.X, self.y)
        predictions = self.rf.predict(np.empty((0, N_FEATURES)))
        self.assertEqual(predictions.shape, (0,))

    def test_predict_shape_mismatch(self):
        """Tests predict with incorrect number of features."""
        self.rf.fit(self.X, self.y)
        X_wrong_shape = self.X_test[:, :-1]  # One less feature
        with self.assertRaises(ValueError):
            self.rf.predict(X_wrong_shape)

    def test_get_stats(self):
        """Tests the get_stats method."""
        self.rf.fit(self.X, self.y)
        predictions = self.rf.predict(self.X_test)
        stats = self.rf.get_stats(self.y_test, predictions)
        self.assertIsInstance(stats, dict)
        self.assertIn("MSE", stats)
        self.assertIn("R^2", stats)
        self.assertIn("MAE", stats)
        self.assertIn("RMSE", stats)
        self.assertIn("MAPE", stats)
        self.assertTrue(
            all(np.isfinite(v) for v in stats.values() if isinstance(v, (float, int)))
        )


class TestGradientBoostedRegressor(BaseTest):
    """Tests for the updated GradientBoostedRegressor class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Gradient Boosted Regressor", end="", flush=True)
        cls.X, cls.y = synthetic_data_regression(
            n_samples=N_SAMPLES, n_features=N_FEATURES, random_state=RANDOM_STATE
        )
        cls.X_test, cls.y_test = synthetic_data_regression(
            n_samples=20, n_features=N_FEATURES, random_state=RANDOM_STATE + 1
        )

    def setUp(self):
        """Sets up the GradientBoostedRegressor instance for testing."""
        self.gbr = GradientBoostedRegressor(
            num_trees=5,  # Fewer trees for faster tests
            max_depth=2,  # Typically shallower for GBR
            min_samples_split=MIN_SAMPLES_SPLIT,
            learning_rate=0.1,
            random_seed=RANDOM_STATE,
        )

    def test_init(self):
        """Tests the initialization of the GradientBoostedRegressor class."""
        self.assertEqual(self.gbr.n_estimators, 5)
        self.assertEqual(self.gbr.max_depth, 2)
        self.assertEqual(self.gbr.min_samples_split, MIN_SAMPLES_SPLIT)
        self.assertEqual(self.gbr.learning_rate, 0.1)
        self.assertEqual(self.gbr.random_state, RANDOM_STATE)
        self.assertIsInstance(self.gbr.trees, list)
        self.assertEqual(len(self.gbr.trees), 0)
        self.assertIsNone(self.gbr.initial_prediction_)

    def test_fit(self):
        """Tests the fit method of the GradientBoostedRegressor class."""
        self.gbr.fit(self.X, self.y)
        self.assertEqual(len(self.gbr.trees), self.gbr.n_estimators)
        self.assertIsInstance(self.gbr.trees[0], RegressorTree)
        self.assertIsNotNone(self.gbr.initial_prediction_)
        self.assertIsInstance(self.gbr.initial_prediction_, float)
        # Check if trees seem fitted
        self.assertGreater(len(self.gbr.trees[0].tree), 0)

    def test_fit_verbose(self):
        """Tests the fit method with verbose output."""
        with suppress_print():
            self.gbr.fit(self.X, self.y, verbose=True)
        # Check if fitting completed successfully
        self.assertEqual(len(self.gbr.trees), self.gbr.n_estimators)
        self.assertIsNotNone(self.gbr.initial_prediction_)

    def test_fit_empty(self):
        """Tests the fit method with an empty dataset."""
        X_empty = np.empty((0, N_FEATURES))
        y_empty = np.empty((0,))
        with self.assertRaises(ValueError):
            self.gbr.fit(X_empty, y_empty)

    def test_fit_single_value(self):
        """Tests the fit method with a single value dataset."""
        X_single = self.X[0:1, :]
        y_single = self.y[0:1]
        self.gbr.fit(X_single, y_single)
        self.assertEqual(len(self.gbr.trees), self.gbr.n_estimators)
        self.assertIsInstance(self.gbr.trees[0], RegressorTree)
        self.assertAlmostEqual(self.gbr.initial_prediction_, y_single[0])

    def test_fit_sample_weights(self):
        """Tests fitting with sample weights."""
        sample_weights = np.random.rand(self.X.shape[0])
        self.gbr.fit(self.X, self.y, sample_weight=sample_weights)
        # Check if trees seem fitted (have structure)
        self.assertEqual(len(self.gbr.trees), self.gbr.n_estimators)

    def test_fit_invalid_sample_weights(self):
        """Tests fitting with invalid sample weights."""
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.gbr.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_non_numeric_sample_weights(self):
        """Tests fitting with non-numeric sample weights."""
        sample_weights = np.array(["a", "b", "c"])
        with self.assertRaises((ValueError, IndexError)):
            self.gbr.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_sample_weights_shape_mismatch(self):
        """Tests fitting with sample weights of different shape."""
        sample_weights = np.array([1, 2, 3])
        with self.assertRaises((ValueError, IndexError)):
            self.gbr.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_sample_weights_empty(self):
        """Tests fitting with empty sample weights."""
        sample_weights = np.array([])
        with self.assertRaises((ValueError, IndexError)):
            self.gbr.fit(self.X, self.y, sample_weight=sample_weights)

    def test_fit_sample_weights_none(self):
        """Tests fitting with None sample weights."""
        self.gbr.fit(self.X, self.y, sample_weight=None)
        # Check if trees seem fitted (have structure)
        self.assertEqual(len(self.gbr.trees), self.gbr.n_estimators)

    def test_predict_before_fit(self):
        """Tests predict before fitting."""
        with self.assertRaises(RuntimeError):  # Specific check added in predict
            self.gbr.predict(self.X_test)

    def test_predict(self):
        """Tests the predict method after fitting."""
        self.gbr.fit(self.X, self.y)
        predictions = self.gbr.predict(self.X_test)
        self.assertEqual(predictions.shape, (self.X_test.shape[0],))
        self.assertIsInstance(predictions, np.ndarray)
        self.assertTrue(np.issubdtype(predictions.dtype, np.number))
        self.assertFalse(np.isnan(predictions).any(), "NaN values found in prediction")

    def test_predict_empty_input(self):
        """Tests predict with an empty input array X."""
        self.gbr.fit(self.X, self.y)
        predictions = self.gbr.predict(np.empty((0, N_FEATURES)))
        self.assertEqual(predictions.shape, (0,))

    def test_predict_shape_mismatch(self):
        """Tests predict with incorrect number of features."""
        self.gbr.fit(self.X, self.y)
        X_wrong_shape = self.X_test[:, :-1]
        with self.assertRaises(ValueError):
            self.gbr.predict(X_wrong_shape)

    def test_get_stats(self):
        """Tests the get_stats method."""
        self.gbr.fit(self.X, self.y)
        predictions = self.gbr.predict(self.X_test)
        stats = self.gbr.get_stats(self.y_test, predictions)
        self.assertIsInstance(stats, dict)
        self.assertIn("MSE", stats)
        self.assertIn("R^2", stats)
        self.assertIn("MAE", stats)
        self.assertIn("RMSE", stats)
        self.assertIn("MAPE", stats)
        self.assertTrue(
            all(np.isfinite(v) for k, v in stats.items() if isinstance(v, (float, int)))
        )


if __name__ == "__main__":
    unittest.main(verbosity=1)  # Use verbosity=2 for more detailed output
