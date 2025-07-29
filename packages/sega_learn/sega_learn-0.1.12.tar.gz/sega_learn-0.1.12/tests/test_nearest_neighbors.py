import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.linear_models import *
from sega_learn.nearest_neighbors.knn_classifier import KNeighborsClassifier
from sega_learn.nearest_neighbors.knn_regressor import KNeighborsRegressor
from tests.utils import BaseTest


class TestKNeighborsClassifier(BaseTest):
    """Unit tests for the KNeighborsClassifier class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting KNeighborsClassifierKNeighborsBase", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Sets up the test environment before each test."""
        pass

    def test_fit(self):
        """Tests the fit method of the KNeighborsClassifier class."""
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0, 1, 0, 1])
        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X_train, y_train)
        # Assert that the training data and labels are stored correctly
        self.assertIsNotNone(knn.X_train)
        self.assertIsNotNone(knn.y_train)
        np.testing.assert_array_equal(knn.X_train, X_train)
        np.testing.assert_array_equal(knn.y_train, y_train)

    def test_predict(self):
        """Tests the predict method of the KNeighborsClassifier class."""
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0, 1, 0, 1])
        X_test = np.array([[1, 2], [2, 2], [3, 3]])
        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X_train, y_train)
        predictions = knn.predict(X_test)
        expected_predictions = np.array([0, 0, 0])
        np.testing.assert_array_equal(predictions, expected_predictions)

    def test_invalid_n_neighbors(self):
        """Tests the behavior when an invalid number of neighbors is provided."""
        with self.assertRaises(ValueError):
            KNeighborsClassifier(n_neighbors=0)

    def test_invalid_n_neighbors_greater_than_samples(self):
        """Tests the behavior when n_neighbors is greater than the number of samples."""
        X_train = np.array([[1, 2], [2, 3], [3, 4]])
        y_train = np.array([0, 1, 0])
        knn = KNeighborsClassifier(n_neighbors=4)
        with self.assertRaises(ValueError):
            knn.fit(X_train, y_train)

    def test_distance_metric(self):
        """Tests the behavior when a valid distance metric is provided."""
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0, 1, 0, 1])
        X_test = np.array([[1, 2], [2, 2], [3, 3]])
        knn = KNeighborsClassifier(n_neighbors=3, distance_metric="euclidean")
        knn.fit(X_train, y_train)
        predictions = knn.predict(X_test)
        expected_predictions = np.array([0, 0, 0])
        np.testing.assert_array_equal(predictions, expected_predictions)

    def test_invalid_distance_metric(self):
        """Tests the behavior when an invalid distance metric is provided."""
        knn = KNeighborsClassifier(distance_metric="invalid_metric")
        with self.assertRaises(ValueError):
            knn._compute_distances(np.array([[1, 2], [2, 3]]))

    def test_data_precision(self):
        """Tests the behavior when a valid floating point precision is provided."""
        knn = KNeighborsClassifier(n_neighbors=3, fp_precision=np.float32)
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]], dtype=np.float64)
        y_train = np.array([0, 1, 0, 1], dtype=np.float64)
        knn.fit(X_train, y_train)
        self.assertEqual(knn.X_train.dtype, np.float32)
        self.assertEqual(knn.y_train.dtype, np.float32)

    def test_invalid_fp_precision(self):
        """Tests the behavior when an invalid floating point precision is provided."""
        with self.assertRaises(ValueError):
            KNeighborsClassifier(fp_precision=int)

    def test_one_hot_encoding(self):
        """Tests the behavior when one-hot encoding is applied to the input data."""
        X_train = np.array([[1, "a"], [2, "b"], [3, "a"], [4, "b"]])
        y_train = np.array([0, 1, 0, 1])
        knn = KNeighborsClassifier(n_neighbors=3, one_hot_encode=True)
        knn.fit(X_train, y_train)
        self.assertIsNotNone(knn.X_train)
        self.assertIsNotNone(knn.y_train)

    def test_invalid_one_hot_encoding(self):
        """Tests the behavior when an invalid one-hot encoding is provided."""
        with self.assertRaises(ValueError):
            KNeighborsClassifier(one_hot_encode="invalid_value")

    def test_predict_with_one_hot_encoding(self):
        """Tests the behavior when one-hot encoding is applied to the input data during prediction."""
        X_train = np.array([[1, "a"], [2, "b"], [3, "a"], [4, "b"]])
        y_train = np.array([0, 1, 0, 1])
        X_test = np.array([[1, "a"], [2, "b"], [3, "a"]])
        knn = KNeighborsClassifier(n_neighbors=3, one_hot_encode=True)
        knn.fit(X_train, y_train)
        _predictions = knn.predict(X_test)

    def test_predict_with_invalid_one_hot_encoding(self):
        """Tests the behavior when an invalid one-hot encoding is provided during prediction."""
        with self.assertRaises(ValueError):
            _knn = KNeighborsClassifier(n_neighbors=3, one_hot_encode="invalid_value")


class TestKNeighborsRegressor(BaseTest):
    """Unit tests for the KNeighborsRegressor class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting KNeighborsRegressor", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Sets up the test environment before each test."""
        pass

    def test_fit(self):
        """Tests the fit method of the KNeighborsRegressor class."""
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0.5, 1.5, 0.5, 1.5])
        knn = KNeighborsRegressor(n_neighbors=3)
        knn.fit(X_train, y_train)
        # Assert that the training data and labels are stored correctly
        self.assertIsNotNone(knn.X_train)
        self.assertIsNotNone(knn.y_train)
        np.testing.assert_array_equal(knn.X_train, X_train)
        np.testing.assert_array_equal(knn.y_train, y_train)

    def test_predict(self):
        """Tests the predict method of the KNeighborsRegressor class."""
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0.5, 1.5, 0.5, 1.5])
        X_test = np.array([[1, 2], [2, 2], [3, 3]])
        knn = KNeighborsRegressor(n_neighbors=3)
        knn.fit(X_train, y_train)
        predictions = knn.predict(X_test)
        expected_predictions = np.array([0.83333333, 0.83333333, 0.83333333])
        np.testing.assert_array_almost_equal(predictions, expected_predictions)

    def test_invalid_n_neighbors(self):
        """Tests the behavior when an invalid number of neighbors is provided."""
        with self.assertRaises(ValueError):
            KNeighborsRegressor(n_neighbors=0)

    def test_invalid_n_neighbors_greater_than_samples(self):
        """Tests the behavior when n_neighbors is greater than the number of samples."""
        X_train = np.array([[1, 2], [2, 3], [3, 4]])
        y_train = np.array([0.5, 1.5, 0.5])
        knn = KNeighborsRegressor(n_neighbors=4)
        with self.assertRaises(ValueError):
            knn.fit(X_train, y_train)

    def test_distance_metric(self):
        """Tests the behavior when a valid distance metric is provided."""
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        y_train = np.array([0.5, 1.5, 0.5, 1.5])
        X_test = np.array([[1, 2], [2, 2], [3, 3]])
        knn = KNeighborsRegressor(n_neighbors=3, distance_metric="euclidean")
        knn.fit(X_train, y_train)
        predictions = knn.predict(X_test)
        expected_predictions = np.array([0.83333333, 0.83333333, 0.83333333])
        np.testing.assert_array_almost_equal(predictions, expected_predictions)

    def test_invalid_distance_metric(self):
        """Tests the behavior when an invalid distance metric is provided."""
        knn = KNeighborsRegressor(distance_metric="invalid_metric")
        with self.assertRaises(ValueError):
            knn._compute_distances(np.array([[1, 2], [2, 3]]))

    def test_data_precision(self):
        """Tests the behavior when a valid floating point precision is provided."""
        knn = KNeighborsRegressor(n_neighbors=3, fp_precision=np.float32)
        X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]], dtype=np.float64)
        y_train = np.array([0.5, 1.5, 0.5, 1.5], dtype=np.float64)
        knn.fit(X_train, y_train)
        self.assertEqual(knn.X_train.dtype, np.float32)
        self.assertEqual(knn.y_train.dtype, np.float32)

    def test_invalid_fp_precision(self):
        """Tests the behavior when an invalid floating point precision is provided."""
        with self.assertRaises(ValueError):
            KNeighborsRegressor(fp_precision=int)

    def test_one_hot_encoding(self):
        """Tests the behavior when one-hot encoding is applied to the input data."""
        X_train = np.array([[1, "a"], [2, "b"], [3, "a"], [4, "b"]])
        y_train = np.array([0.5, 1.5, 0.5, 1.5])
        knn = KNeighborsRegressor(n_neighbors=3, one_hot_encode=True)
        knn.fit(X_train, y_train)
        self.assertIsNotNone(knn.X_train)
        self.assertIsNotNone(knn.y_train)

    def test_invalid_one_hot_encoding(self):
        """Tests the behavior when an invalid one-hot encoding is provided."""
        with self.assertRaises(ValueError):
            KNeighborsRegressor(one_hot_encode="invalid_value")

    def test_predict_with_one_hot_encoding(self):
        """Tests the behavior when one-hot encoding is applied to the input data during prediction."""
        X_train = np.array([[1, "a"], [2, "b"], [3, "a"], [4, "b"]])
        y_train = np.array([0.5, 1.5, 0.5, 1.5])
        X_test = np.array([[1, "a"], [2, "b"], [3, "a"]])
        knn = KNeighborsRegressor(n_neighbors=3, one_hot_encode=True)
        knn.fit(X_train, y_train)
        _predictions = knn.predict(X_test)

    def test_predict_with_invalid_one_hot_encoding(self):
        """Tests the behavior when an invalid one-hot encoding is provided during prediction."""
        with self.assertRaises(ValueError):
            _knn = KNeighborsRegressor(n_neighbors=3, one_hot_encode="invalid_value")


if __name__ == "__main__":
    unittest.main()
