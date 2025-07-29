import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sega_learn.utils import (
    make_blobs,
    make_classification,
    make_regression,
    make_time_series,
)
from tests.utils import BaseTest


class TestMakeData(BaseTest):
    """Unit test for the data generation utilities make_regression, make_classification, and make_blobs."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting makeData Utilities", end="", flush=True)

    def setUp(self):  # NOQA D201
        self.random_state = 42  # Fixed random state for reproducibility

    # === Tests for make_regression ===
    def test_make_regression_basic(self):
        """Test basic functionality of make_regression."""
        n_samples, n_features = 100, 10
        X, y = make_regression(
            n_samples=n_samples, n_features=n_features, random_state=self.random_state
        )

        self.assertEqual(X.shape, (n_samples, n_features))
        self.assertEqual(y.shape, (n_samples,))
        self.assertTrue(np.issubdtype(X.dtype, np.floating))
        self.assertTrue(np.issubdtype(y.dtype, np.floating))

    def test_make_regression_informative(self):
        """Test that n_informative parameter works as expected."""
        n_samples, n_features, n_informative = 200, 20, 5
        X, y, coef = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_informative,
            coef=True,
            random_state=self.random_state,
        )

        # Count non-zero coefficients
        non_zero_coefs = np.count_nonzero(coef)
        self.assertEqual(non_zero_coefs, n_informative)

    def test_make_regression_multi_target(self):
        """Test multi-target regression."""
        n_samples, n_features, n_targets = 150, 15, 3
        X, y = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            n_targets=n_targets,
            random_state=self.random_state,
        )

        self.assertEqual(X.shape, (n_samples, n_features))
        self.assertEqual(y.shape, (n_samples, n_targets))

    def test_make_regression_bias(self):
        """Test bias parameter affects output."""
        n_samples, bias = 100, 5.0
        X, y = make_regression(
            n_samples=n_samples, bias=bias, noise=0.0, random_state=self.random_state
        )

        # With zero noise, mean of y should be close to bias
        self.assertAlmostEqual(np.mean(y), bias, delta=0.5)

    def test_make_regression_noise(self):
        """Test noise parameter affects output variance."""
        n_samples, noise_low, noise_high = 500, 0.1, 10.0

        # Generate datasets with different noise levels
        X_low, y_low = make_regression(
            n_samples=n_samples, noise=noise_low, random_state=self.random_state
        )
        X_high, y_high = make_regression(
            n_samples=n_samples, noise=noise_high, random_state=self.random_state
        )

        # Higher noise should result in higher variance
        self.assertLess(np.var(y_low), np.var(y_high))

    def test_make_regression_shuffle(self):
        """Test shuffle parameter works."""
        n_samples = 100

        # Generate data with and without shuffling
        X_shuffled, y_shuffled = make_regression(
            n_samples=n_samples, shuffle=True, random_state=self.random_state
        )
        X_unshuffled, y_unshuffled = make_regression(
            n_samples=n_samples, shuffle=False, random_state=self.random_state
        )

        # Check if datasets are different
        self.assertFalse(
            np.array_equal(X_shuffled, X_unshuffled)
            and np.array_equal(y_shuffled, y_unshuffled)
        )

    def test_make_regression_effective_rank(self):
        """Test effective_rank parameter affects feature correlation."""
        n_samples, n_features = 100, 20
        effective_rank = 5

        X, _ = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            effective_rank=effective_rank,
            random_state=self.random_state,
        )

        # Compute covariance matrix eigenvalues
        cov = np.cov(X, rowvar=False)
        eigenvalues = np.linalg.eigvalsh(cov)
        eigenvalues = np.sort(eigenvalues)[::-1]

        # Check that eigenvalues decay rapidly, consistent with low effective rank
        eigenvalue_ratio = eigenvalues[effective_rank] / eigenvalues[0]
        self.assertLess(eigenvalue_ratio, 0.1)

    # === Tests for make_classification ===
    def test_make_classification_basic(self):
        """Test basic functionality of make_classification."""
        n_samples, n_features = 100, 10
        X, y = make_classification(
            n_samples=n_samples, n_features=n_features, random_state=self.random_state
        )

        self.assertEqual(X.shape, (n_samples, n_features))
        self.assertEqual(y.shape, (n_samples,))
        self.assertTrue(np.issubdtype(X.dtype, np.floating))
        self.assertTrue(np.issubdtype(y.dtype, np.integer))

        # Check classes are 0 and 1 for binary classification
        unique_classes = np.unique(y)
        self.assertEqual(len(unique_classes), 2)
        self.assertTrue(np.array_equal(unique_classes, np.array([0, 1])))

    def test_make_classification_n_classes(self):
        """Test n_classes parameter works as expected."""
        n_samples, n_classes = 300, 4
        X, y = make_classification(
            n_samples=n_samples, n_classes=n_classes, random_state=self.random_state
        )

        unique_classes = np.unique(y)
        self.assertEqual(len(unique_classes), n_classes)
        self.assertTrue(np.array_equal(unique_classes, np.arange(n_classes)))

    def test_make_classification_weights(self):
        """Test weights parameter affects class distribution."""
        n_samples, n_classes = 1000, 3
        weights = [0.2, 0.3, 0.5]

        X, y = make_classification(
            n_samples=n_samples,
            n_classes=n_classes,
            weights=weights,
            random_state=self.random_state,
        )

        # Check class distribution
        class_counts = np.bincount(y, minlength=n_classes)
        class_proportions = class_counts / n_samples

        # Class proportions should be close to weights
        for i in range(n_classes):
            self.assertAlmostEqual(class_proportions[i], weights[i], delta=0.05)

    def test_make_classification_informative_features(self):
        """Test n_informative parameter affects feature importance."""
        n_samples, n_features, n_informative = 500, 20, 5
        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_informative,
            n_redundant=0,
            n_repeated=0,
            random_state=self.random_state,
        )

        # Calculate feature importance using correlation with y
        correlations = np.abs(
            np.array([np.corrcoef(X[:, i], y)[0, 1] for i in range(n_features)])
        )
        sorted_indices = np.argsort(correlations)[::-1]

        # Top n_informative features should have high correlation
        top_correlations = correlations[sorted_indices[:n_informative]]
        other_correlations = correlations[sorted_indices[n_informative:]]

        self.assertGreater(np.mean(top_correlations), np.mean(other_correlations))

    def test_make_classification_redundant_features(self):
        """Test n_redundant parameter creates correlated features."""
        n_samples, n_features = 500, 10
        n_informative, n_redundant = 3, 3

        X, _ = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_informative,
            n_redundant=n_redundant,
            n_repeated=0,
            random_state=self.random_state,
        )

        # Calculate correlation matrix between features
        corr_matrix = np.corrcoef(X, rowvar=False)

        # Count highly correlated feature pairs
        high_corr_count = (
            np.sum(np.abs(corr_matrix) > 0.7) - n_features
        )  # Subtract diagonal

        # Should have some highly correlated features due to redundancy
        self.assertGreaterEqual(high_corr_count, n_redundant)

    def test_make_classification_repeated_features(self):
        """Test n_repeated parameter creates duplicate features."""
        n_samples, n_features = 100, 10
        n_informative, n_redundant, n_repeated = 3, 2, 2

        X, _ = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_informative,
            n_redundant=n_redundant,
            n_repeated=n_repeated,
            random_state=self.random_state,
        )

        # Calculate correlation matrix
        corr_matrix = np.corrcoef(X, rowvar=False)

        # Count perfectly correlated feature pairs (correlation = 1)
        perfect_corr_count = (
            np.sum(np.abs(corr_matrix) > 0.99) - n_features
        )  # Subtract diagonal

        # Should have at least n_repeated perfect correlations
        self.assertGreaterEqual(
            perfect_corr_count / 2, n_repeated
        )  # Divide by 2 because matrix is symmetric

    def test_make_classification_class_sep(self):
        """Test class_sep parameter affects class separation."""
        n_samples = 200

        # Generate datasets with different class separations and no label flipping
        X_low_sep, y_low_sep = make_classification(
            n_samples=n_samples,
            class_sep=1.0,
            flip_y=0.0,  # Disable label flipping
            random_state=self.random_state,
        )
        X_high_sep, y_high_sep = make_classification(
            n_samples=n_samples,
            class_sep=10.0,
            flip_y=0.0,  # Disable label flipping
            random_state=self.random_state,
        )

        # Define function to measure class separation
        def measure_separation(X, y):
            class_0 = X[y == 0]
            class_1 = X[y == 1]
            centroid_0 = np.mean(class_0, axis=0)
            centroid_1 = np.mean(class_1, axis=0)
            return np.linalg.norm(centroid_0 - centroid_1)

        # Calculate separations
        sep_low = measure_separation(X_low_sep, y_low_sep)
        sep_high = measure_separation(X_high_sep, y_high_sep)

        # Higher class_sep should result in greater separation
        self.assertLess(sep_low, sep_high)

    def test_make_classification_flip_y(self):
        """Test flip_y parameter introduces label noise."""
        # Estimate difficulty using cross-validation
        try:
            from sklearn.linear_model import LogisticRegression
            from sklearn.model_selection import cross_val_score
        except ImportError:  # Skip if sklearn is not installed
            return

        n_samples = 1000
        flip_y_low, flip_y_high = 0.01, 0.3

        # Generate datasets with different flip rates
        X_low_flip, y_low_flip = make_classification(
            n_samples=n_samples,
            flip_y=flip_y_low,
            class_sep=5.0,
            random_state=self.random_state,
        )
        X_high_flip, y_high_flip = make_classification(
            n_samples=n_samples,
            flip_y=flip_y_high,
            class_sep=5.0,
            random_state=self.random_state,
        )

        def get_accuracy(X, y):
            model = LogisticRegression(solver="liblinear")
            scores = cross_val_score(model, X, y, cv=5)  # 5-fold cross-validation
            return scores.mean()  # Return average accuracy across folds

        # Higher flip_y should result in lower accuracy
        try:
            acc_low = get_accuracy(X_low_flip, y_low_flip)
            acc_high = get_accuracy(X_high_flip, y_high_flip)
            self.assertGreater(acc_low, acc_high)
        except ImportError:
            # Skip if sklearn is not installed
            pass

    # === Tests for make_blobs ===
    def test_make_blobs_basic(self):
        """Test basic functionality of make_blobs."""
        n_samples, n_features, centers = 100, 2, 3
        X, y, centers_out = make_blobs(
            n_samples=n_samples,
            n_features=n_features,
            centers=centers,
            random_state=self.random_state,
        )

        self.assertEqual(X.shape, (n_samples, n_features))
        self.assertEqual(y.shape, (n_samples,))
        self.assertEqual(centers_out.shape, (centers, n_features))

        # Check clusters are labeled 0 to centers-1
        unique_clusters = np.unique(y)
        self.assertEqual(len(unique_clusters), centers)
        self.assertTrue(np.array_equal(unique_clusters, np.arange(centers)))

    def test_make_blobs_specified_centers(self):
        """Test make_blobs with specified centers."""
        n_samples = 100
        centers_in = np.array([[0, 0], [10, 10], [-10, -10]])
        n_centers = centers_in.shape[0]

        X, y, centers_out = make_blobs(
            n_samples=n_samples, centers=centers_in, random_state=self.random_state
        )

        # Check dimensions
        self.assertEqual(X.shape, (n_samples, 2))
        self.assertEqual(y.shape, (n_samples,))
        self.assertEqual(centers_out.shape, (n_centers, 2))

        # Centers output should match input
        np.testing.assert_allclose(centers_in, centers_out)

        # Check data points are clustered around centers
        for i in range(n_centers):
            cluster_points = X[y == i]
            cluster_center = np.mean(cluster_points, axis=0)
            np.testing.assert_allclose(cluster_center, centers_in[i], rtol=0, atol=0.5)

    def test_make_blobs_cluster_std(self):
        """Test cluster_std parameter affects cluster variance."""
        n_samples, centers = 500, 2
        std_low, std_high = 0.5, 5.0

        # Generate datasets with different standard deviations
        X_low_std, y_low_std, _ = make_blobs(
            n_samples=n_samples,
            centers=centers,
            cluster_std=std_low,
            random_state=self.random_state,
        )
        X_high_std, y_high_std, _ = make_blobs(
            n_samples=n_samples,
            centers=centers,
            cluster_std=std_high,
            random_state=self.random_state,
        )

        # Calculate average distance to cluster center
        def avg_distance_to_center(X, y):
            distances = []
            for i in range(centers):
                cluster_points = X[y == i]
                cluster_center = np.mean(cluster_points, axis=0)
                cluster_distances = np.linalg.norm(
                    cluster_points - cluster_center, axis=1
                )
                distances.append(np.mean(cluster_distances))
            return np.mean(distances)

        # Higher std should result in larger average distance
        dist_low = avg_distance_to_center(X_low_std, y_low_std)
        dist_high = avg_distance_to_center(X_high_std, y_high_std)
        self.assertLess(dist_low, dist_high)

    def test_make_blobs_different_stds(self):
        """Test make_blobs with different standard deviations per cluster."""
        n_samples, centers = 500, 3
        cluster_std = [0.5, 2.0, 4.0]

        X, y, _ = make_blobs(
            n_samples=n_samples,
            centers=centers,
            cluster_std=cluster_std,
            random_state=self.random_state,
        )

        # Calculate variance for each cluster
        variances = []
        for i in range(centers):
            cluster_points = X[y == i]
            cluster_center = np.mean(cluster_points, axis=0)
            cluster_distances = np.linalg.norm(cluster_points - cluster_center, axis=1)
            variances.append(np.var(cluster_distances))

        # Variances should be in ascending order
        self.assertLess(variances[0], variances[1])
        self.assertLess(variances[1], variances[2])

    def test_make_blobs_n_samples_per_center(self):
        """Test make_blobs with specified samples per center."""
        n_samples = [30, 40, 50]
        n_features = 2

        X, y, _ = make_blobs(
            n_samples=n_samples, n_features=n_features, random_state=self.random_state
        )

        # Check total number of samples
        self.assertEqual(X.shape, (sum(n_samples), n_features))

        # Check number of samples per cluster
        for i, expected_count in enumerate(n_samples):
            actual_count = np.sum(y == i)
            self.assertEqual(actual_count, expected_count)

    def test_make_blobs_center_box(self):
        """Test center_box parameter controls center locations."""
        n_samples, centers = 100, 5
        center_box_small = (-1, 1)
        center_box_large = (-100, 100)

        _, _, centers_small = make_blobs(
            n_samples=n_samples,
            centers=centers,
            center_box=center_box_small,
            random_state=self.random_state,
        )
        _, _, centers_large = make_blobs(
            n_samples=n_samples,
            centers=centers,
            center_box=center_box_large,
            random_state=self.random_state,
        )

        # Check centers are within bounds
        self.assertTrue(np.all(centers_small >= center_box_small[0]))
        self.assertTrue(np.all(centers_small <= center_box_small[1]))
        self.assertTrue(np.all(centers_large >= center_box_large[0]))
        self.assertTrue(np.all(centers_large <= center_box_large[1]))

        # Larger box should result in more spread out centers
        small_spread = np.max(np.linalg.norm(centers_small, axis=1))
        large_spread = np.max(np.linalg.norm(centers_large, axis=1))
        self.assertLess(small_spread, large_spread)

    def test_make_blobs_shuffle(self):
        """Test shuffle parameter works."""
        n_samples_per_center = [30, 30, 40]

        # Generate data with and without shuffling
        X_shuffled, y_shuffled, _ = make_blobs(
            n_samples=n_samples_per_center,
            centers=None,
            shuffle=True,
            random_state=self.random_state,
        )
        X_unshuffled, y_unshuffled, _ = make_blobs(
            n_samples=n_samples_per_center,
            centers=None,
            shuffle=False,
            random_state=self.random_state,
        )

        # Check if labels are different
        self.assertFalse(np.array_equal(y_shuffled, y_unshuffled))

        # Unshuffled data should have sorted labels
        expected_unshuffled = np.concatenate(
            [np.full(count, i) for i, count in enumerate(n_samples_per_center)]
        )
        self.assertTrue(np.array_equal(y_unshuffled, expected_unshuffled))

    # === Edge cases and error handling tests ===
    def test_make_regression_invalid_params(self):
        """Test error handling for invalid parameters in make_regression."""
        # Test invalid effective_rank
        with self.assertRaises(ValueError):
            make_regression(n_features=10, effective_rank=20)

    def test_make_classification_invalid_params(self):
        """Test error handling for invalid parameters in make_classification."""
        # Test too many features requested
        with self.assertRaises(ValueError):
            make_classification(
                n_features=5, n_informative=3, n_redundant=3, n_repeated=0
            )

        # Test invalid weights
        with self.assertRaises(ValueError):
            make_classification(n_classes=3, weights=[-1, 0.5, 0.5])

        with self.assertRaises(ValueError):
            make_classification(n_classes=3, weights=[0.3, 0.3])

    def test_make_blobs_invalid_params(self):
        """Test error handling for invalid parameters in make_blobs."""
        # Test inconsistent n_samples and centers
        centers_array = np.array([[0, 0], [1, 1], [2, 2]])
        with self.assertRaises(ValueError):
            make_blobs(n_samples=[30, 40], centers=centers_array)

    # === Performance tests ===
    def test_make_regression_large(self):
        """Test make_regression with a large dataset."""
        n_samples, n_features = 10000, 50

        # This should run without memory issues
        X, y = make_regression(
            n_samples=n_samples, n_features=n_features, random_state=self.random_state
        )

        self.assertEqual(X.shape, (n_samples, n_features))

    def test_make_classification_large(self):
        """Test make_classification with a large dataset."""
        n_samples, n_features = 10000, 50

        # This should run without memory issues
        X, y = make_classification(
            n_samples=n_samples, n_features=n_features, random_state=self.random_state
        )

        self.assertEqual(X.shape, (n_samples, n_features))

    def test_make_blobs_large(self):
        """Test make_blobs with a large dataset."""
        n_samples, n_features = 10000, 50

        # This should run without memory issues
        X, y, _ = make_blobs(
            n_samples=n_samples, n_features=n_features, random_state=self.random_state
        )

        self.assertEqual(X.shape, (n_samples, n_features))

    # === Tests for make_time_series ===
    def test_make_time_series_basic(self):
        """Test basic functionality of make_time_series."""
        n_samples, n_timestamps, n_features = 10, 50, 1
        X = make_time_series(
            n_samples=n_samples,
            n_timestamps=n_timestamps,
            n_features=n_features,
            random_state=self.random_state,
        )

        self.assertEqual(X.shape, (n_samples, n_timestamps, n_features))
        self.assertTrue(np.issubdtype(X.dtype, np.floating))

    def test_make_time_series_trend(self):
        """Test trend parameter affects time series shape."""
        n_samples, n_timestamps, n_features = 5, 100, 1

        X_linear = make_time_series(
            n_samples=n_samples,
            n_timestamps=n_timestamps,
            n_features=n_features,
            trend="linear",
            seasonality=None,
            noise=0,
            random_state=self.random_state,
        )
        X_quadratic = make_time_series(
            n_samples=n_samples,
            n_timestamps=n_timestamps,
            n_features=n_features,
            trend="quadratic",
            seasonality=None,
            noise=0,
            random_state=self.random_state,
        )

        # Check linear trend, all values should be increasing
        self.assertTrue(np.all(np.diff(X_linear[0, :, 0]) > 0))

        # Check quadratic trend, all second differences should be positiveW
        self.assertTrue(np.all(np.diff(np.diff(X_quadratic[0, :, 0])) > 0))

    def test_make_time_series_seasonality(self):
        """Test seasonality parameter affects time series periodicity."""
        n_samples, n_timestamps, n_features = 1, 100, 1
        seasonality_period = 50

        X_sine = make_time_series(
            n_samples=n_samples,
            n_timestamps=n_timestamps,
            n_features=n_features,
            trend=None,
            seasonality="sine",
            seasonality_period=seasonality_period,
            noise=0,
            random_state=self.random_state,
        )
        X_cosine = make_time_series(
            n_samples=n_samples,
            n_timestamps=n_timestamps,
            n_features=n_features,
            trend=None,
            seasonality="cosine",
            seasonality_period=seasonality_period,
            noise=0,
            random_state=self.random_state,
        )

        # Check sine seasonality
        self.assertAlmostEqual(X_sine[0, seasonality_period // 4, 0], 1, delta=0.1)
        self.assertAlmostEqual(X_sine[0, seasonality_period // 2, 0], 0, delta=0.1)
        self.assertAlmostEqual(X_sine[0, 3 * seasonality_period // 4, 0], -1, delta=0.1)
        self.assertAlmostEqual(X_sine[0, seasonality_period, 0], 0, delta=0.1)

        # Check cosine seasonality
        self.assertAlmostEqual(X_cosine[0, seasonality_period // 4, 0], 0, delta=0.1)
        self.assertAlmostEqual(X_cosine[0, seasonality_period // 2, 0], -1, delta=0.1)
        self.assertAlmostEqual(
            X_cosine[0, 3 * seasonality_period // 4, 0], 0, delta=0.1
        )
        self.assertAlmostEqual(X_cosine[0, seasonality_period, 0], 1, delta=0.1)

    def test_make_time_series_noise(self):
        """Test noise parameter affects time series variability."""
        n_samples, n_timestamps, n_features = 5, 100, 1
        noise_low, noise_high = 0.1, 1.0

        X_low_noise = make_time_series(
            n_samples=n_samples,
            n_timestamps=n_timestamps,
            n_features=n_features,
            noise=noise_low,
            random_state=self.random_state,
        )
        X_high_noise = make_time_series(
            n_samples=n_samples,
            n_timestamps=n_timestamps,
            n_features=n_features,
            noise=noise_high,
            random_state=self.random_state,
        )

        # Higher noise should result in higher variance
        self.assertLess(np.var(X_low_noise), np.var(X_high_noise))

    def test_make_time_series_multiple_features(self):
        """Test make_time_series with multiple features."""
        n_samples, n_timestamps, n_features = 5, 50, 3
        X = make_time_series(
            n_samples=n_samples,
            n_timestamps=n_timestamps,
            n_features=n_features,
            random_state=self.random_state,
        )

        self.assertEqual(X.shape, (n_samples, n_timestamps, n_features))

    def test_make_time_series_invalid_trend(self):
        """Test error handling for invalid trend parameter."""
        with self.assertRaises(ValueError):
            make_time_series(trend="invalid", random_state=self.random_state)

    def test_make_time_series_invalid_seasonality(self):
        """Test error handling for invalid seasonality parameter."""
        with self.assertRaises(ValueError):
            make_time_series(seasonality="invalid", random_state=self.random_state)


if __name__ == "__main__":
    unittest.main()
