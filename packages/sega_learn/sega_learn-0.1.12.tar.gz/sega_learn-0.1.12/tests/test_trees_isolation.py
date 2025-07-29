import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.trees import *
from tests.utils import BaseTest


class TestIsolationUtils(BaseTest):
    """Unit test for the IsolationTreeUtility class."""

    @classmethod
    def setUpClass(cls):
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Isolation Tree Utility", end="", flush=True)

    def test_compute_avg_path_length(self):
        """Tests the compute_avg_path_length method of the IsolationTreeUtility class."""
        self.assertAlmostEqual(IsolationUtils.compute_avg_path_length(1), 0)
        self.assertAlmostEqual(
            IsolationUtils.compute_avg_path_length(2), 0.15443132979999996
        )
        self.assertAlmostEqual(
            IsolationUtils.compute_avg_path_length(256), 10.244770920116851
        )


class TestIsolationTree(BaseTest):
    """Unit test for the IsolationTree class."""

    @classmethod
    def setUpClass(cls):
        """Initializes a new instance of the class before each test method is run."""
        print("\nTesting Isolation Tree", end="", flush=True)

    def setUp(self):
        """Sets up test data and initializes an IsolationTree instance."""
        self.X = np.random.randn(100, 2)
        self.tree = IsolationTree(max_depth=10)
        self.tree.fit(self.X)

    def test_fit(self):
        """Tests the fit method of the IsolationTree class."""
        self.assertIsNotNone(self.tree.tree)

    def test_fit_with_empty_data(self):
        """Tests the fit method with empty data."""
        with self.assertRaises(ValueError):
            empty_data = np.empty((0, 2))
            tree = IsolationTree(max_depth=10)
            tree.fit(empty_data)

    def test_path_length(self):
        """Tests the path_length method of the IsolationTree class."""
        sample = np.random.randn(2)
        path_length = self.tree.path_length(sample)
        self.assertGreaterEqual(path_length, 0)

    def test_path_length_with_empty_data(self):
        """Tests the path_length method with empty data."""
        with self.assertRaises(ValueError):
            sample = np.empty((0, 2))
            self.tree.path_length(sample)


class TestIsolationForest(BaseTest):
    """Unit test for the IsolationForest class."""

    @classmethod
    def setUpClass(cls):
        """Initializes a new instance of the class before each test method is run."""
        print("\nTesting Isolation Forest", end="", flush=True)

    def setUp(self):
        """Sets up test data and initializes an IsolationForest instance."""
        self.X = np.random.randn(100, 2)
        self.forest = IsolationForest(n_trees=10, max_samples=50, max_depth=10)
        self.forest.fit(self.X)

    def test_fit(self):
        """Tests the fit method of the IsolationForest class."""
        self.assertEqual(len(self.forest.trees), 10)

    def test_fit_with_empty_data(self):
        """Tests the fit method with empty data."""
        with self.assertRaises(ValueError):
            empty_data = np.empty((0, 2))
            forest = IsolationForest(n_trees=10, max_samples=50, max_depth=10)
            forest.fit(empty_data)

    def test_anomaly_score(self):
        """Tests the anomaly_score method of the IsolationForest class."""
        sample = np.random.randn(2)
        score = self.forest.anomaly_score(sample)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_anomaly_score_with_empty_data(self):
        """Tests the anomaly_score method with empty data."""
        with self.assertRaises(ValueError):
            sample = np.empty((0, 2))
            self.forest.anomaly_score(sample)

    def test_predict(self):
        """Tests the predict method of the IsolationForest class."""
        sample = np.random.randn(2)
        prediction = self.forest.predict(sample)
        self.assertIn(prediction, [0, 1])


if __name__ == "__main__":
    unittest.main()
