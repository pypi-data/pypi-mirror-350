import os
import sys
import unittest
import warnings
from unittest.mock import patch

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sega_learn.linear_models import LogisticRegression, Ridge
from sega_learn.time_series.moving_average import ExponentialMovingAverage
from sega_learn.utils import (
    Metrics,
    make_classification,
    make_regression,
    make_time_series,
)
from sega_learn.utils.animator import (
    ClassificationAnimation,
    ForcastingAnimation,
    RegressionAnimation,
)
from tests.utils import BaseTest, suppress_print


class TestForcastingAnimation(BaseTest):
    """Unit test for the ForcastingAnimation class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes the test suite."""
        print("\nTesting ForcastingAnimation Class", end="", flush=True)
        mpl.use("Agg")

    def setUp(self):  # NOQA D201
        """Prepares each test."""
        # Generate a synthetic time series
        self.time_series = make_time_series(
            n_samples=1,
            n_timestamps=100,
            n_features=1,
            trend="linear",
            seasonality="sine",
            seasonality_period=10,
            noise=0.1,
            random_state=42,
        ).flatten()

        # Split into training and testing sets
        train_size = int(len(self.time_series) * 0.8)
        self.train_series = self.time_series[:train_size]
        self.test_series = self.time_series[train_size:]
        self.forecast_steps = len(self.test_series)

    def test_init(self):
        """Test ForcastingAnimation initialization."""
        animator = ForcastingAnimation(
            model=ExponentialMovingAverage,
            train_series=self.train_series,
            test_series=self.test_series,
            forecast_steps=self.forecast_steps,
            dynamic_parameter="alpha",
            keep_previous=True,
        )
        self.assertEqual(animator.forecast_steps, self.forecast_steps)
        self.assertEqual(len(animator.train_indices), len(self.train_series))
        self.assertEqual(len(animator.forecast_indices), self.forecast_steps)
        self.assertTrue(hasattr(animator, "previous_forecast_lines"))
        self.assertTrue(hasattr(animator, "previous_fitted_lines"))

    def test_init_no_dynamic_parameter(self):
        """Test initialization with no dynamic parameter."""
        with self.assertRaises(ValueError):
            ForcastingAnimation(
                model=ExponentialMovingAverage,
                train_series=self.train_series,
                test_series=self.test_series,
                forecast_steps=self.forecast_steps,
                dynamic_parameter=None,
                keep_previous=True,
            )

    def test_init_no_static_parameters(self):
        """Test initialization with no static parameters."""
        animator = ForcastingAnimation(
            model=ExponentialMovingAverage,
            train_series=self.train_series,
            test_series=self.test_series,
            forecast_steps=self.forecast_steps,
            dynamic_parameter="alpha",
            static_parameters=None,
            keep_previous=True,
        )
        self.assertIsNotNone(animator)
        self.assertDictEqual(animator.static_parameters, {})

    def test_init_no_train_series(self):
        """Test initialization with no train series."""
        with self.assertRaises(ValueError):
            ForcastingAnimation(
                model=ExponentialMovingAverage,
                train_series=None,
                test_series=self.test_series,
                forecast_steps=self.forecast_steps,
                dynamic_parameter="alpha",
                keep_previous=True,
            )

    def test_setup_plot(self):
        """Test setup_plot with valid parameters."""
        animator = ForcastingAnimation(
            model=ExponentialMovingAverage,
            train_series=self.train_series,
            test_series=self.test_series,
            forecast_steps=self.forecast_steps,
            dynamic_parameter="alpha",
        )
        animator.setup_plot("Test Forecasting", "Time", "Value")
        self.assertIsNotNone(animator.fig)
        self.assertIsNotNone(animator.ax)
        self.assertEqual(animator.ax.get_title(), "Test Forecasting")
        self.assertIsNotNone(animator.fitted_line)
        self.assertIsNotNone(animator.forecast_line)
        plt.close(animator.fig)

    def test_update_model(self):
        """Test update_model with valid frame parameter."""
        animator = ForcastingAnimation(
            model=ExponentialMovingAverage,
            train_series=self.train_series,
            test_series=self.test_series,
            forecast_steps=self.forecast_steps,
            dynamic_parameter="alpha",
        )
        with suppress_print():
            # Test with a specific alpha value
            animator.update_model(0.3)
        self.assertIsInstance(animator.model_instance, ExponentialMovingAverage)
        self.assertEqual(animator.model_instance.alpha, 0.3)
        self.assertEqual(len(animator.fitted_values), len(self.train_series))
        self.assertEqual(len(animator.forecast_values), self.forecast_steps)

    def test_update_plot_with_metrics(self):
        """Test update_plot with metrics."""
        animator = ForcastingAnimation(
            model=ExponentialMovingAverage,
            train_series=self.train_series,
            test_series=self.test_series,
            forecast_steps=self.forecast_steps,
            dynamic_parameter="alpha",
            metric_fn=[Metrics.mean_squared_error],
        )
        with suppress_print():
            animator.setup_plot("Test Forecasting", "Time", "Value")
            animator.update_model(0.3)

            # Check that update_plot returns a list of artists
            artists = animator.update_plot(0.3)

        self.assertIsInstance(artists, list)
        self.assertTrue(all(isinstance(artist, plt.Line2D) for artist in artists))
        plt.close(animator.fig)


class TestRegressionAnimation(BaseTest):
    """Unit test for the RegressionAnimation class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes the test suite."""
        print("\nTesting RegressionAnimation Class", end="", flush=True)
        mpl.use("Agg")

    def setUp(self):  # NOQA D201
        """Prepares each test."""
        # Generate synthetic regression data
        self.X, self.y = make_regression(
            n_samples=100, n_features=1, noise=0.5, random_state=42
        )
        warnings.filterwarnings("ignore", category=UserWarning)

    def test_init(self):
        """Test RegressionAnimation initialization."""
        animator = RegressionAnimation(
            model=Ridge,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters={"alpha": 1.0},
            keep_previous=True,
        )
        self.assertIsInstance(animator.X_train, np.ndarray)
        self.assertIsInstance(animator.y_train, np.ndarray)
        self.assertIsInstance(animator.X_test, np.ndarray)
        self.assertIsInstance(animator.y_test, np.ndarray)

    def test_init_with_pca(self):
        """Test initialization with PCA for multi-feature data."""
        # Create multi-feature data
        X_multi = np.random.rand(100, 5)
        y_multi = np.random.rand(100)

        with suppress_print():
            animator = RegressionAnimation(
                model=Ridge,
                X=X_multi,
                y=y_multi,
                test_size=0.25,
                dynamic_parameter="max_iter",
                pca_components=1,
            )
        self.assertTrue(animator.needs_pca)
        self.assertIsNotNone(animator.pca_instance)
        self.assertEqual(
            animator.X_train.shape[1], 1
        )  # Should be reduced to 1 component

    def test_init_no_dynamic_parameter(self):
        """Test initialization with no dynamic parameter."""
        with self.assertRaises(ValueError):
            RegressionAnimation(
                model=Ridge,
                X=self.X,
                y=self.y,
                test_size=0.25,
                dynamic_parameter=None,
                keep_previous=True,
            )

    def test_init_no_static_parameters(self):
        """Test initialization with no static parameters."""
        animator = RegressionAnimation(
            model=Ridge,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters=None,
            keep_previous=True,
        )
        self.assertIsNotNone(animator)
        self.assertDictEqual(animator.static_parameters, {})

    def test_init_no_X(self):
        """Test initialization with no X."""
        with self.assertRaises(ValueError):
            RegressionAnimation(
                model=Ridge,
                X=None,
                y=self.y,
                test_size=0.25,
                dynamic_parameter="max_iter",
                keep_previous=True,
            )

    def test_init_no_y(self):
        """Test initialization with no y."""
        with self.assertRaises(ValueError):
            RegressionAnimation(
                model=Ridge,
                X=self.X,
                y=None,
                test_size=0.25,
                dynamic_parameter="max_iter",
                keep_previous=True,
            )

    def test_setup_plot(self):
        """Test setup_plot with valid parameters."""
        animator = RegressionAnimation(
            model=Ridge,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
        )
        animator.setup_plot("Test Regression", "Feature", "Target")
        self.assertIsNotNone(animator.fig)
        self.assertIsNotNone(animator.ax)
        self.assertEqual(animator.ax.get_title(), "Test Regression")
        self.assertIsNotNone(animator.scatter_points)
        self.assertIsNotNone(animator.scatter_points_test)
        self.assertIsNotNone(animator.predicted_line)
        plt.close(animator.fig)

    def test_update_model(self):
        """Test update_model with valid frame parameter."""
        animator = RegressionAnimation(
            model=Ridge,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters={"alpha": 1.0},
        )
        with suppress_print():
            # Test with a specific max_iter value
            animator.update_model(1000)
        self.assertIsInstance(animator.model_instance, Ridge)
        self.assertEqual(animator.model_instance.max_iter, 1000)
        self.assertEqual(animator.model_instance.alpha, 1.0)
        self.assertIsInstance(animator.X_test_sorted, np.ndarray)
        self.assertIsInstance(animator.predicted_values, np.ndarray)

    def test_update_plot_with_metrics(self):
        """Test update_plot with metrics."""
        animator = RegressionAnimation(
            model=Ridge,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters={"alpha": 1.0},
            metric_fn=[Metrics.mean_squared_error, Metrics.r_squared],
        )
        with suppress_print():
            animator.setup_plot("Test Regression", "Feature", "Target")
            animator.update_model(1000)

            # Check that update_plot returns a tuple of artists
            artists = animator.update_plot(1000)

        self.assertIsInstance(artists, tuple)
        self.assertEqual(len(artists), 1)
        self.assertIsInstance(artists[0], plt.Line2D)
        plt.close(animator.fig)


class TestClassificationAnimation(BaseTest):
    """Unit test for the ClassificationAnimation class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes the test suite."""
        print("\nTesting ClassificationAnimation Class", end="", flush=True)
        mpl.use("Agg")

    def setUp(self):  # NOQA D201
        """Prepares each test."""
        # Generate synthetic classification data
        self.X, self.y = make_classification(
            n_samples=100,
            n_features=2,
            n_redundant=0,
            n_informative=2,
            n_classes=2,
            random_state=42,
        )

    def test_init(self):
        """Test ClassificationAnimation initialization."""
        animator = ClassificationAnimation(
            model=LogisticRegression,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters={"learning_rate": 0.001},
            keep_previous=True,
        )
        self.assertIsInstance(animator.X_train, np.ndarray)
        self.assertIsInstance(animator.y_train, np.ndarray)
        self.assertIsInstance(animator.X_test, np.ndarray)
        self.assertIsInstance(animator.y_test, np.ndarray)
        self.assertIsInstance(animator.xx, np.ndarray)
        self.assertIsInstance(animator.yy, np.ndarray)
        self.assertIsInstance(animator.unique_classes, np.ndarray)
        self.assertIsInstance(animator.colors, np.ndarray)

    def test_init_with_pca(self):
        """Test initialization with PCA for multi-feature data."""
        # Create multi-feature data
        X_multi = np.random.rand(100, 5)
        y_multi = np.random.randint(0, 2, 100)

        with suppress_print():
            animator = ClassificationAnimation(
                model=LogisticRegression,
                X=X_multi,
                y=y_multi,
                test_size=0.25,
                dynamic_parameter="max_iter",
                pca_components=2,
            )
        self.assertTrue(animator.needs_pca)
        self.assertIsNotNone(animator.pca_instance)
        self.assertEqual(
            animator.X_train.shape[1], 2
        )  # Should be reduced to 2 components

    def test_init_no_dynamic_parameter(self):
        """Test initialization with no dynamic parameter."""
        with self.assertRaises(ValueError):
            ClassificationAnimation(
                model=LogisticRegression,
                X=self.X,
                y=self.y,
                test_size=0.25,
                dynamic_parameter=None,
                keep_previous=True,
            )

    def test_init_no_static_parameters(self):
        """Test initialization with no static parameters."""
        animator = ClassificationAnimation(
            model=LogisticRegression,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters=None,
            keep_previous=True,
        )
        self.assertIsNotNone(animator)
        self.assertDictEqual(animator.static_parameters, {})

    def test_init_no_X(self):
        """Test initialization with no X."""
        with self.assertRaises(ValueError):
            ClassificationAnimation(
                model=LogisticRegression,
                X=None,
                y=self.y,
                test_size=0.25,
                dynamic_parameter="max_iter",
                keep_previous=True,
            )

    def test_init_no_y(self):
        """Test initialization with no y."""
        with self.assertRaises(ValueError):
            ClassificationAnimation(
                model=LogisticRegression,
                X=self.X,
                y=None,
                test_size=0.25,
                dynamic_parameter="max_iter",
                keep_previous=True,
            )

    def test_setup_plot(self):
        """Test setup_plot with valid parameters."""
        animator = ClassificationAnimation(
            model=LogisticRegression,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
        )
        animator.setup_plot("Test Classification", "Feature 1", "Feature 2")
        self.assertIsNotNone(animator.fig)
        self.assertIsNotNone(animator.ax)
        self.assertEqual(animator.ax.get_title(), "Test Classification")
        self.assertGreater(len(animator.scatter_train_dict), 0)
        self.assertGreater(len(animator.scatter_test_dict), 0)
        plt.close(animator.fig)

    def test_update_model(self):
        """Test update_model with valid frame parameter."""
        animator = ClassificationAnimation(
            model=LogisticRegression,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters={"learning_rate": 0.001},
        )
        with suppress_print():
            # Test with a specific max_iter value
            animator.update_model(1000)
        self.assertIsInstance(animator.model_instance, LogisticRegression)
        self.assertEqual(animator.model_instance.max_iter, 1000)
        self.assertEqual(animator.model_instance.learning_rate, 0.001)

    def test_update_plot_with_metrics(self):
        """Test update_plot with metrics."""
        animator = ClassificationAnimation(
            model=LogisticRegression,
            X=self.X,
            y=self.y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters={"learning_rate": 0.001},
            metric_fn=[Metrics.accuracy, Metrics.precision],
        )
        with suppress_print():
            animator.setup_plot("Test Classification", "Feature 1", "Feature 2")
            animator.update_model(1000)

            # Check that update_plot returns a tuple of artists
            artists = animator.update_plot(1000)

        self.assertIsInstance(artists, tuple)
        self.assertEqual(
            len(artists), 2
        )  # For binary classification, returns decision boundary and boundary lines
        plt.close(animator.fig)


class TestAnimationIntegration(BaseTest):
    """Integration tests for animation classes."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes the test suite."""
        print("\nTesting Animation Integration", end="", flush=True)
        mpl.use("Agg")

    @patch("matplotlib.animation.FuncAnimation")
    def test_forecasting_animate(self, mock_animation):
        """Test ForcastingAnimation animate method."""
        # Generate a synthetic time series
        time_series = make_time_series(
            n_samples=1,
            n_timestamps=100,
            n_features=1,
            trend="linear",
            seasonality="sine",
            seasonality_period=10,
            noise=0.1,
            random_state=42,
        ).flatten()

        # Split into training and testing sets
        train_size = int(len(time_series) * 0.8)
        train_series = time_series[:train_size]
        test_series = time_series[train_size:]
        forecast_steps = len(test_series)

        animator = ForcastingAnimation(
            model=ExponentialMovingAverage,
            train_series=train_series,
            test_series=test_series,
            forecast_steps=forecast_steps,
            dynamic_parameter="alpha",
            keep_previous=True,
            metric_fn=[Metrics.mean_squared_error],
        )

        animator.setup_plot("Test Forecasting", "Time", "Value")
        alpha_range = np.arange(0.01, 0.5, 0.1)

        # Test animate method with mock
        animation = animator.animate(
            frames=alpha_range, interval=150, blit=True, repeat=False
        )
        self.assertEqual(animation, animator.ani)
        mock_animation.assert_called_once()

    @patch("matplotlib.animation.FuncAnimation")
    def test_regression_animate(self, mock_animation):
        """Test RegressionAnimation animate method."""
        # Generate synthetic regression data
        X, y = make_regression(n_samples=100, n_features=1, noise=0.5, random_state=42)

        animator = RegressionAnimation(
            model=Ridge,
            X=X,
            y=y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters={"alpha": 1.0},
            keep_previous=True,
            metric_fn=[Metrics.mean_squared_error],
        )

        animator.setup_plot("Test Regression", "Feature", "Target")
        max_iter_range = range(100, 1000, 100)

        # Test animate method with mock
        animation = animator.animate(
            frames=max_iter_range, interval=150, blit=True, repeat=False
        )
        self.assertEqual(animation, animator.ani)
        mock_animation.assert_called_once()

    @patch("matplotlib.animation.FuncAnimation")
    def test_classification_animate(self, mock_animation):
        """Test ClassificationAnimation animate method."""
        # Generate synthetic classification data
        X, y = make_classification(
            n_samples=100,
            n_features=2,
            n_redundant=0,
            n_informative=2,
            n_classes=2,
            random_state=42,
        )

        animator = ClassificationAnimation(
            model=LogisticRegression,
            X=X,
            y=y,
            test_size=0.25,
            dynamic_parameter="max_iter",
            static_parameters={"learning_rate": 0.001},
            keep_previous=True,
            metric_fn=[Metrics.accuracy],
        )

        animator.setup_plot("Test Classification", "Feature 1", "Feature 2")
        max_iter_range = range(100, 1000, 100)

        # Test animate method with mock
        animation = animator.animate(
            frames=max_iter_range, interval=150, blit=True, repeat=False
        )
        self.assertEqual(animation, animator.ani)
        mock_animation.assert_called_once()

    @patch("builtins.print")
    @patch("matplotlib.animation.FuncAnimation.save")
    def test_save_functionality(self, mock_save, mock_print):
        """Test the save functionality of animation classes."""
        # Generate synthetic regression data
        X, y = make_regression(n_samples=100, n_features=1, noise=0.5, random_state=42)

        animator = RegressionAnimation(
            model=Ridge, X=X, y=y, dynamic_parameter="max_iter"
        )

        animator.setup_plot("Test Regression", "Feature", "Target")

        # Mock the animation creation
        with patch("matplotlib.animation.FuncAnimation") as mock_animation:
            mock_instance = mock_animation.return_value
            animator.ani = mock_instance  # Set the animation attribute

            # Test saving
            animator.save("test.gif", writer="pillow", fps=5, dpi=100)
            mock_instance.save.assert_called_once_with(
                "test.gif", writer="pillow", fps=5, dpi=100
            )
            mock_print.assert_called_with("Animation saved successfully to test.gif.")


if __name__ == "__main__":
    unittest.main()
