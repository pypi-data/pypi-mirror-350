import os
import sys
import unittest

import numpy as np
import pandas as pd
from scipy import sparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sega_learn.utils import train_test_split
from tests.utils import BaseTest


class TestTrainTestSplit(BaseTest):
    """Unit test for the train_test_split function."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes the test suite."""
        print("\nTesting train_test_split function", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Prepares data for each test."""
        # Create sample data for tests
        self.X = np.random.rand(100, 5)
        self.y = np.random.randint(0, 2, 100)
        self.stratify_y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1] * 10)

        # Create small dataset for exact size testing
        self.X_small = np.arange(10).reshape(-1, 1)
        self.y_small = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

        # Create pandas DataFrame
        self.X_df = pd.DataFrame(self.X, columns=[f"feature_{i}" for i in range(5)])
        self.y_df = pd.Series(self.y, name="target")

        # Create sparse matrix
        self.X_sparse = sparse.csr_matrix(self.X)

        # Create Python lists
        self.X_list = self.X.tolist()
        self.y_list = self.y.tolist()

    def test_basic_functionality(self):
        """Tests basic train_test_split functionality."""
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y)

        # Default test_size is 0.25
        self.assertEqual(len(X_train), 75)
        self.assertEqual(len(X_test), 25)
        self.assertEqual(len(y_train), 75)
        self.assertEqual(len(y_test), 25)

        # Check that all samples are preserved
        self.assertEqual(len(X_train) + len(X_test), len(self.X))
        self.assertEqual(len(y_train) + len(y_test), len(self.y))

    def test_different_test_sizes(self):
        """Tests with different test_size values."""
        # Test with float
        X_train, X_test = train_test_split(self.X, test_size=0.4)
        self.assertEqual(len(X_train), 60)
        self.assertEqual(len(X_test), 40)

        # Test with int
        X_train, X_test = train_test_split(self.X, test_size=30)
        self.assertEqual(len(X_train), 70)
        self.assertEqual(len(X_test), 30)

        # Test with zero test_size
        X_train, X_test = train_test_split(self.X_small, test_size=0)
        self.assertEqual(len(X_train), 10)
        self.assertEqual(len(X_test), 0)

        # Test with 100% test_size
        X_train, X_test = train_test_split(self.X_small, test_size=1.0)
        self.assertEqual(len(X_train), 0)
        self.assertEqual(len(X_test), 10)

    def test_different_train_sizes(self):
        """Tests with different train_size values."""
        # Test with float
        X_train, X_test = train_test_split(self.X, train_size=0.7)
        self.assertEqual(len(X_train), 70)
        self.assertEqual(len(X_test), 30)  # Updated to expect 30

        # Test with int
        X_train, X_test = train_test_split(self.X, train_size=80)
        self.assertEqual(len(X_train), 80)
        self.assertEqual(len(X_test), 20)

        # Test with zero train_size
        X_train, X_test = train_test_split(self.X_small, train_size=0)
        self.assertEqual(len(X_train), 0)
        self.assertEqual(len(X_test), 10)

        # Test with 100% train_size
        X_train, X_test = train_test_split(self.X_small, train_size=1.0)
        self.assertEqual(len(X_train), 10)
        self.assertEqual(len(X_test), 0)

    def test_combined_sizes(self):
        """Tests with both train_size and test_size specified."""
        # Both as float
        X_train, X_test = train_test_split(self.X, train_size=0.6, test_size=0.3)
        self.assertEqual(len(X_train), 60)
        self.assertEqual(len(X_test), 30)

        # Both as int
        X_train, X_test = train_test_split(self.X, train_size=50, test_size=40)
        self.assertEqual(len(X_train), 50)
        self.assertEqual(len(X_test), 40)

        # Mixed types
        X_train, X_test = train_test_split(self.X, train_size=0.6, test_size=20)
        self.assertEqual(len(X_train), 60)
        self.assertEqual(len(X_test), 20)

    def test_random_state(self):
        """Tests reproducibility with random_state."""
        # First split with random_state=42
        X_train1, X_test1 = train_test_split(self.X, random_state=42)

        # Second split with same random_state
        X_train2, X_test2 = train_test_split(self.X, random_state=42)

        # They should be identical
        np.testing.assert_array_equal(X_train1, X_train2)
        np.testing.assert_array_equal(X_test1, X_test2)

        # Split with different random_state
        X_train3, X_test3 = train_test_split(self.X, random_state=24)

        # Should be different (this could theoretically fail by chance, but very unlikely)
        with self.assertRaises(AssertionError):
            np.testing.assert_array_equal(X_train1, X_train3)

    def test_stratification(self):
        """Tests stratified splitting."""
        # Set a fixed random state for reproducibility in this test
        random_state = 42

        # Test with stratification
        X_train, X_test, y_train, y_test = train_test_split(
            self.X_small,
            self.y_small,
            test_size=0.5,
            stratify=self.y_small,
            random_state=random_state,
        )

        # Check class distribution is roughly maintained
        train_class_0 = np.sum(y_train == 0)
        train_class_1 = np.sum(y_train == 1)
        test_class_0 = np.sum(y_test == 0)
        test_class_1 = np.sum(y_test == 1)

        # There should be a balance of classes in both sets
        self.assertGreaterEqual(train_class_0, 2)
        self.assertGreaterEqual(train_class_1, 2)
        self.assertGreaterEqual(test_class_0, 2)
        self.assertGreaterEqual(test_class_1, 2)

        # Test with larger dataset
        X_train, X_test, y_train, y_test = train_test_split(
            self.X,
            self.stratify_y,
            test_size=0.3,
            stratify=self.stratify_y,
            random_state=random_state,
        )

        # Calculate original and split class proportions
        orig_prop = np.mean(self.stratify_y == 1)
        train_prop = np.mean(y_train == 1)
        test_prop = np.mean(y_test == 1)

        # The proportions should be approximately equal
        self.assertAlmostEqual(orig_prop, train_prop, delta=0.05)
        self.assertAlmostEqual(orig_prop, test_prop, delta=0.05)

    def test_without_shuffling(self):
        """Tests splitting without shuffling."""
        X_train, X_test = train_test_split(self.X_small, shuffle=False, test_size=0.3)

        # Check that the first 7 samples are in train and the last 3 in test
        np.testing.assert_array_equal(X_train, self.X_small[:7])
        np.testing.assert_array_equal(X_test, self.X_small[7:])

    def test_different_input_types(self):
        """Tests with different input types."""
        # Test with NumPy arrays
        X_train, X_test = train_test_split(self.X, test_size=0.2)
        self.assertIsInstance(X_train, np.ndarray)
        self.assertEqual(len(X_train), 80)

        # Test with pandas DataFrame
        X_train, X_test = train_test_split(self.X_df, test_size=0.2)
        self.assertIsInstance(X_train, pd.DataFrame)
        self.assertEqual(len(X_train), 80)

        # Test with pandas Series
        y_train, y_test = train_test_split(self.y_df, test_size=0.2)
        self.assertIsInstance(y_train, pd.Series)
        self.assertEqual(len(y_train), 80)

        # Test with Python list
        X_train, X_test = train_test_split(self.X_list, test_size=0.2)
        self.assertIsInstance(X_train, list)
        self.assertEqual(len(X_train), 80)

        # Test with sparse matrix
        X_train, X_test = train_test_split(self.X_sparse, test_size=0.2)
        self.assertTrue(sparse.issparse(X_train))
        self.assertEqual(X_train.shape[0], 80)

    def test_multiple_arrays(self):
        """Tests splitting multiple arrays."""
        # Split three arrays
        X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
            self.X, self.y, np.ones(100), test_size=0.25
        )

        # Check lengths
        self.assertEqual(len(X_train), 75)
        self.assertEqual(len(X_test), 25)
        self.assertEqual(len(y_train), 75)
        self.assertEqual(len(y_test), 25)
        self.assertEqual(len(w_train), 75)
        self.assertEqual(len(w_test), 25)

        # Check that the indices match (X and y should have the same split)
        X_indices = {tuple(x) for x in X_train}
        for i, y_val in enumerate(y_train):
            # Find the original index of this y value
            orig_indices = np.where(self.y == y_val)[0]
            # At least one of the X rows should match
            found = False
            for idx in orig_indices:
                if tuple(self.X[idx]) in X_indices:
                    found = True
                    break
            self.assertTrue(found, f"Could not find matching X for y at index {i}")

    def test_edge_cases(self):
        """Tests edge cases and error handling."""
        # Test input validation - arrays of different lengths
        with self.assertRaises(ValueError):
            train_test_split(self.X, self.y[:50])

        # Test invalid test_size (negative)
        with self.assertRaises(ValueError):
            train_test_split(self.X, test_size=-0.2)

        # Test invalid test_size (> 1)
        with self.assertRaises(ValueError):
            train_test_split(self.X, test_size=1.1)

        # Test invalid train_size (negative)
        with self.assertRaises(ValueError):
            train_test_split(self.X, train_size=-0.2)

        # Test invalid train_size (> 1)
        with self.assertRaises(ValueError):
            train_test_split(self.X, train_size=1.1)

        # Test train_size + test_size > n_samples
        with self.assertRaises(ValueError):
            train_test_split(self.X, train_size=0.8, test_size=0.3)

        # Test stratify with shuffle=False
        with self.assertRaises(ValueError):
            train_test_split(self.X, self.y, stratify=self.y, shuffle=False)

        # Test stratify with mismatched length
        with self.assertRaises(ValueError):
            train_test_split(self.X, stratify=self.y[:50])


if __name__ == "__main__":
    unittest.main()
