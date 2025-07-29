import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.clustering import *
from tests.utils import BaseTest


class TestKMeans(BaseTest):
    """Unit test for the KMeans clustering class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting KMeans", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Sets up synthetic data and initializes the KMeans instance."""
        # Generate synthetic data for testing
        self.true_k = 3
        self.X = np.array(
            [
                [1.0, 2.0],
                [1.5, 1.8],
                [5.0, 8.0],
                [8.0, 8.0],
                [1.0, 0.6],
                [9.0, 11.0],
                [8.0, 2.0],
                [10.0, 2.0],
                [9.0, 3.0],
            ]
        )
        self.kmeans = KMeans(self.X, n_clusters=self.true_k)

    def test_initialization(self):
        """Tests the initialization of the KMeans class."""
        self.assertEqual(self.kmeans.n_clusters, self.true_k)
        self.assertEqual(self.kmeans.max_iter, 300)
        self.assertEqual(self.kmeans.tol, 1e-4)
        self.assertIsNone(self.kmeans.centroids)
        self.assertIsNone(self.kmeans.labels)

    def test_initialization_fail_n_clusters_zero(self):
        """Tests that initialization fails when n_clusters is zero."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=0)

    def test_initialization_fail_n_clusters_negative(self):
        """Tests that initialization fails when n_clusters is negative."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=-1)

    def test_initialization_fail_n_clusters_too_large(self):
        """Tests that initialization fails when n_clusters is larger than the dataset size."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=10)

    def test_initialization_fail_n_clusters_non_integer(self):
        """Tests that initialization fails when n_clusters is not an integer."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=2.5)

    def test_initialization_fail_n_clusters_string(self):
        """Tests that initialization fails when n_clusters is a string."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters="3")

    def test_initialization_fail_n_clusters_none(self):
        """Tests that initialization fails when n_clusters is None."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=None)

    def test_initialization_fail_n_clusters_list(self):
        """Tests that initialization fails when n_clusters is a list."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=[3])

    def test_initialization_fail_n_clusters_tuple(self):
        """Tests that initialization fails when n_clusters is a tuple."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=(3,))

    def test_initialization_fail_max_iter_zero(self):
        """Tests that initialization fails when max_iter is zero."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, max_iter=0)

    def test_initialization_fail_max_iter_negative(self):
        """Tests that initialization fails when max_iter is negative."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, max_iter=-1)

    def test_initialization_fail_max_iter_non_integer(self):
        """Tests that initialization fails when max_iter is not an integer."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, max_iter=300.5)

    def test_initialization_fail_max_iter_string(self):
        """Tests that initialization fails when max_iter is a string."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, max_iter="300")

    def test_initialization_fail_max_iter_none(self):
        """Tests that initialization fails when max_iter is None."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, max_iter=None)

    def test_initialization_fail_max_iter_list(self):
        """Tests that initialization fails when max_iter is a list."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, max_iter=[300])

    def test_initialization_fail_max_iter_tuple(self):
        """Tests that initialization fails when max_iter is a tuple."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, max_iter=(300,))

    def test_initialization_fail_tol_zero(self):
        """Tests that initialization fails when tol is zero."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, tol=0)

    def test_initialization_fail_tol_negative(self):
        """Tests that initialization fails when tol is negative."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, tol=-1)

    def test_initialization_fail_tol_string(self):
        """Tests that initialization fails when tol is a string."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, tol="1e-4")

    def test_initialization_fail_tol_none(self):
        """Tests that initialization fails when tol is None."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, tol=None)

    def test_initialization_fail_tol_list(self):
        """Tests that initialization fails when tol is a list."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, tol=[1e-4])

    def test_initialization_fail_tol_tuple(self):
        """Tests that initialization fails when tol is a tuple."""
        with self.assertRaises(ValueError):
            KMeans(self.X, n_clusters=self.true_k, tol=(1e-4,))

    def test_fit(self):
        """Tests the fit method of the KMeans class."""
        self.kmeans.fit()
        self.assertEqual(len(self.kmeans.centroids), self.true_k)
        self.assertEqual(len(self.kmeans.labels), len(self.X))

    def test_predict(self):
        """Tests the predict method of the KMeans class."""
        self.kmeans.fit()
        new_X = np.array([[0.0, 0.0], [12.0, 3.0]])
        labels = self.kmeans.predict(new_X)
        self.assertEqual(len(labels), len(new_X))

    def test_predict_fail_not_fitted(self):
        """Tests that predict fails when the model is not fitted."""
        with self.assertRaises(ValueError):
            self.kmeans.predict(np.array([[0.0, 0.0], [12.0, 3.0]]))

    def test_predict_fail_X_not_2d(self):
        """Tests that predict fails when X is not a 2D array."""
        with self.assertRaises(IndexError):
            self.kmeans.predict(np.array([0.0, 0.0]))

    def test_predict_fail_X_3d(self):
        """Tests that predict fails when X is a 3D array."""
        with self.assertRaises(ValueError):
            # X must be a 2D array, not a 3D array
            self.kmeans.predict(np.array([[[0.0, 0.0], [12.0, 3.0]]]))

    def test_elbow_method(self):
        """Tests the elbow method for determining the optimal number of clusters."""
        distortions = self.kmeans.elbow_method(max_k=5)
        self.assertEqual(len(distortions), 5)

    def test_find_optimal_clusters(self):
        """Tests the find_optimal_clusters method for determining the optimal number of clusters."""
        ch_optimal_k, db_optimal_k, silhouette_optimal_k = (
            self.kmeans.find_optimal_clusters(max_k=5, save_dir="tests/test_elbow.png")
        )
        self.assertTrue(1 <= ch_optimal_k <= 5)
        self.assertTrue(1 <= db_optimal_k <= 5)
        self.assertTrue(1 <= silhouette_optimal_k <= 5)

    def test_silhouette_score(self):
        """Tests the silhouette score method for evaluating clustering performance."""
        X = np.array([[1.0, 2.0], [1.5, 1.8], [5.0, 8.0]])
        labels = np.array([0, 0, 1])
        score = self.kmeans.silhouette_score(X, labels)
        self.assertTrue(-1 <= score <= 1)

    def test_calinski_harabasz_index(self):
        """Tests the Calinski-Harabasz index method for evaluating clustering performance."""
        X = np.array([[1.0, 2.0], [1.5, 1.8], [5.0, 8.0]])
        labels = np.array([0, 0, 1])
        centroids = np.array([[1.25, 1.9], [5.0, 8.0]])
        score = self.kmeans.calinski_harabasz_index(X, labels, centroids)
        self.assertTrue(score >= 0)

    def test_davies_bouldin_index(self):
        """Tests the Davies-Bouldin index method for evaluating clustering performance."""
        X = np.array([[1.0, 2.0], [1.5, 1.8], [5.0, 8.0]])
        labels = np.array([0, 0, 1])
        centroids = np.array([[1.25, 1.9], [5.0, 8.0]])
        score = self.kmeans.davies_bouldin_index(X, labels, centroids)
        self.assertTrue(score >= 0)

    def test_initialize_centroids(self):
        """Tests the initialize_centroids method for initializing centroids."""
        self.centroids = self.kmeans.initialize_centroids()
        self.assertEqual(len(self.centroids), self.true_k)

    def test_initialize_centroids_random(self):
        """Tests the initialize_centroids method for initializing centroids randomly."""
        # Run the test multiple times to ensure that the centroids are not equal
        for _ in range(10):
            self.X = np.random.rand(100, 2)
            self.kmeans = KMeans(self.X, n_clusters=self.true_k)
            self.centroids1 = self.kmeans.initialize_centroids()
            self.centroids2 = self.kmeans.initialize_centroids()
            if not np.array_equal(self.centroids1, self.centroids2):
                break
        self.assertFalse(np.array_equal(self.centroids1, self.centroids2))

    def tearDown(self):
        """Cleans up after each test method is run."""
        if os.path.exists("tests/test_elbow.png"):
            os.remove("tests/test_elbow.png")


class TestDBSCAN(BaseTest):
    """Unit test for the DBSCAN clustering class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting DBSCAN", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Sets up synthetic data and initializes the DBSCAN instance."""
        # Generate synthetic data for testing
        self.X = np.array(
            [
                [1.0, 2.0],
                [1.5, 1.8],
                [5.0, 8.0],
                [8.0, 8.0],
                [1.0, 0.6],
                [9.0, 11.0],
                [8.0, 2.0],
                [10.0, 2.0],
                [9.0, 3.0],
            ]
        )
        self.dbscan = DBSCAN(self.X, eps=1.5, min_samples=2)

    def test_initialization(self):
        """Tests the initialization of the DBSCAN class."""
        self.assertEqual(self.dbscan.eps, 1.5)
        self.assertEqual(self.dbscan.min_samples, 2)
        self.assertIsNone(self.dbscan.labels)

    def test_initialization_fail_eps_zero(self):
        """Tests that initialization fails when eps is zero."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=0)

    def test_initialization_fail_eps_negative(self):
        """Tests that initialization fails when eps is negative."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=-1)

    def test_initialization_fail_eps_string(self):
        """Tests that initialization fails when eps is a string."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps="1.5")

    def test_initialization_fail_eps_none(self):
        """Tests that initialization fails when eps is None."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=None)

    def test_initialization_fail_min_samples_zero(self):
        """Tests that initialization fails when min_samples is zero."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=0)

    def test_initialization_fail_min_samples_negative(self):
        """Tests that initialization fails when min_samples is negative."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=-1)

    def test_initialization_fail_min_samples_string(self):
        """Tests that initialization fails when min_samples is a string."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples="2")

    def test_initialization_fail_min_samples_none(self):
        """Tests that initialization fails when min_samples is None."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=None)

    def test_initialization_fail_min_samples_list(self):
        """Tests that initialization fails when min_samples is a list."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=[2])

    def test_initialization_fail_min_samples_tuple(self):
        """Tests that initialization fails when min_samples is a tuple."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=(2,))

    def test_fit(self):
        """Tests the fit method of the DBSCAN class."""
        labels = self.dbscan.fit()
        self.assertEqual(len(labels), len(self.X))
        self.assertTrue(all(label >= -1 for label in labels))

    def test_predict(self):
        """Tests the predict method of the DBSCAN class."""
        self.dbscan.fit()
        new_X = np.array([[0.0, 0.0], [12.0, 3.0]])
        labels = self.dbscan.predict(new_X)
        self.assertEqual(len(labels), len(new_X))
        self.assertTrue(all(label >= -1 for label in labels))

    def test_silhouette_score(self):
        """Tests the silhouette score method for evaluating clustering performance."""
        self.dbscan.fit()
        score = self.dbscan.silhouette_score()
        self.assertTrue(-1 <= score <= 1)

    def test_auto_eps(self):
        """Tests the auto_eps method for automatically determining the optimal epsilon value."""
        best_eps, scores_dict = self.dbscan.auto_eps(return_scores=True)
        self.assertTrue(0.1 <= best_eps <= 1.1)
        self.assertTrue(all(-1 <= score <= 1 for score in scores_dict.values()))


class TestDBSCANNumba(BaseTest):
    """Unit test for the DBSCAN clustering class using Numba."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting DBSCAN Numba", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Sets up synthetic data and initializes the DBSCAN instance with Numba."""
        # Generate synthetic data for testing
        self.X = np.array(
            [
                [1.0, 2.0],
                [1.5, 1.8],
                [5.0, 8.0],
                [8.0, 8.0],
                [1.0, 0.6],
                [9.0, 11.0],
                [8.0, 2.0],
                [10.0, 2.0],
                [9.0, 3.0],
            ]
        )
        self.dbscan = DBSCAN(self.X, eps=1.5, min_samples=2, compile_numba=True)

    def test_initialization(self):
        """Tests the initialization of the DBSCAN class."""
        self.assertEqual(self.dbscan.eps, 1.5)
        self.assertEqual(self.dbscan.min_samples, 2)
        self.assertIsNone(self.dbscan.labels)

    def test_initialization_fail_eps_zero(self):
        """Tests that initialization fails when eps is zero."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=0)

    def test_initialization_fail_eps_negative(self):
        """Tests that initialization fails when eps is negative."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=-1)

    def test_initialization_fail_eps_string(self):
        """Tests that initialization fails when eps is a string."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps="1.5")

    def test_initialization_fail_eps_none(self):
        """Tests that initialization fails when eps is None."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=None)

    def test_initialization_fail_min_samples_zero(self):
        """Tests that initialization fails when min_samples is zero."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=0)

    def test_initialization_fail_min_samples_negative(self):
        """Tests that initialization fails when min_samples is negative."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=-1)

    def test_initialization_fail_min_samples_string(self):
        """Tests that initialization fails when min_samples is a string."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples="2")

    def test_initialization_fail_min_samples_none(self):
        """Tests that initialization fails when min_samples is None."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=None)

    def test_initialization_fail_min_samples_list(self):
        """Tests that initialization fails when min_samples is a list."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=[2])

    def test_initialization_fail_min_samples_tuple(self):
        """Tests that initialization fails when min_samples is a tuple."""
        with self.assertRaises(ValueError):
            DBSCAN(self.X, eps=1.5, min_samples=(2,))

    def test_fit(self):
        """Tests the fit method of the DBSCAN class."""
        labels = self.dbscan.fit(numba=True)
        self.assertEqual(len(labels), len(self.X))
        self.assertTrue(all(label >= -1 for label in labels))

    def test_predict(self):
        """Tests the predict method of the DBSCAN class."""
        self.dbscan.fit(numba=True)
        new_X = np.array([[0.0, 0.0], [12.0, 3.0]])
        labels = self.dbscan.predict(new_X)
        self.assertEqual(len(labels), len(new_X))
        self.assertTrue(all(label >= -1 for label in labels))

    def test_silhouette_score(self):
        """Tests the silhouette score method for evaluating clustering performance."""
        self.dbscan.fit(numba=True)
        score = self.dbscan.silhouette_score()
        self.assertTrue(-1 <= score <= 1)

    def test_auto_eps(self):
        """Tests the auto_eps method for automatically determining the optimal epsilon value."""
        best_eps, scores_dict = self.dbscan.auto_eps(return_scores=True)
        self.assertTrue(0.1 <= best_eps <= 1.1)
        self.assertTrue(all(-1 <= score <= 1 for score in scores_dict.values()))


if __name__ == "__main__":
    unittest.main()
