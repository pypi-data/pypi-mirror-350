import os
import sys
import unittest
import warnings

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.pipelines import ForecastingPipeline
from sega_learn.time_series import *
from sega_learn.utils import Metrics
from tests.utils import BaseTest, suppress_print


class TestForecastingPipeline(BaseTest):
    """Unit test suite for the ForecastingPipeline class."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting ForecastingPipeline", end="", flush=True)
        warnings.simplefilter("ignore", category=RuntimeWarning)
        warnings.simplefilter("ignore", category=UserWarning)

    def setUp(self):  # NOQA D201
        self.time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
        self.train_series = self.time_series[:8]
        self.test_series = self.time_series[8:]
        self.pipeline = ForecastingPipeline(preprocessors=[], model=[], evaluators=[])

    def test_initialization(self):
        """Test ForecastingPipeline initialization."""
        self.assertEqual(len(self.pipeline.preprocessors), 0)
        self.assertEqual(len(self.pipeline.models), 0)
        self.assertEqual(len(self.pipeline.evaluators), 0)

    def test_add_preprocessor(self):
        """Test adding a preprocessor to the pipeline."""
        preprocessor = SimpleMovingAverage(window=3)
        self.pipeline.add_preprocessor(preprocessor)
        self.assertEqual(len(self.pipeline.preprocessors), 1)
        self.assertIs(self.pipeline.preprocessors[0], preprocessor)

    def test_remove_preprocessor(self):
        """Test removing a preprocessor from the pipeline."""
        preprocessor = SimpleMovingAverage(window=3)
        self.pipeline.add_preprocessor(preprocessor)
        self.pipeline.remove_preprocessor(preprocessor)
        self.assertEqual(len(self.pipeline.preprocessors), 0)

    def test_remove_preprocessor_not_found(self):
        """Test removing a preprocessor not found in the pipeline."""
        preprocessor = SimpleMovingAverage(window=3)
        with self.assertRaises(ValueError):
            self.pipeline.remove_preprocessor(preprocessor)

    def test_add_evaluator(self):
        """Test adding an evaluator to the pipeline."""
        evaluator = Metrics.mean_squared_error
        self.pipeline.add_evaluator(evaluator)
        self.assertEqual(len(self.pipeline.evaluators), 1)
        self.assertIs(self.pipeline.evaluators[0], evaluator)

    def test_remove_evaluator(self):
        """Test removing an evaluator from the pipeline."""
        evaluator = Metrics.mean_squared_error
        self.pipeline.add_evaluator(evaluator)
        self.pipeline.remove_evaluator(evaluator)
        self.assertEqual(len(self.pipeline.evaluators), 0)

    def test_remove_evaluator_not_found(self):
        """Test removing an evaluator not found in the pipeline."""
        evaluator = Metrics.mean_squared_error
        with self.assertRaises(ValueError):
            self.pipeline.remove_evaluator(evaluator)

    def test_add_model(self):
        """Test adding a model to the pipeline."""
        model = SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
        self.pipeline.add_model(model)
        self.assertEqual(len(self.pipeline.models), 1)
        self.assertIs(self.pipeline.models[0], model)

    def test_remove_model(self):
        """Test removing a model from the pipeline."""
        model = SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
        self.pipeline.add_model(model)
        self.pipeline.remove_model(model)
        self.assertEqual(len(self.pipeline.models), 0)

    def test_fit(self):
        """Test fitting the pipeline."""
        self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
        self.pipeline.models = [SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_no_preprocessors(self):
        """Test fitting the pipeline with no preprocessors."""
        self.pipeline.models = [SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_no_model(self):
        """Test fitting the pipeline with no model."""
        self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
        with self.assertRaises(ValueError):
            self.pipeline.fit(self.train_series)

    def test_fit_arima(self):
        """Test fitting the pipeline with an ARIMA model."""
        self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
        self.pipeline.models = [ARIMA(order=(1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_sarima(self):
        """Test fitting the pipeline with an SARIMA model."""
        self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
        self.pipeline.models = [SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_sarimax(self):
        """Test fitting the pipeline with an SARIMAX model."""
        self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
        self.pipeline.models = [SARIMAX(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))]
        exog = np.random.rand(len(self.train_series), 1)  # Example exogenous variable
        self.pipeline.fit(self.train_series, exog)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_simple_moving_average(self):
        """Test fitting the pipeline with a Simple Moving Average model."""
        self.pipeline.preprocessors = [SimpleMovingAverage(window=3)]
        self.pipeline.models = [ARIMA(order=(1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_weighted_moving_average(self):
        """Test fitting the pipeline with a Weighted Moving Average model."""
        self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
        self.pipeline.models = [ARIMA(order=(1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_exponential_moving_average(self):
        """Test fitting the pipeline with an Exponential Moving Average model."""
        self.pipeline.preprocessors = [ExponentialMovingAverage(alpha=0.2)]
        self.pipeline.models = [ARIMA(order=(1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_exponential_smoothing(self):
        """Test fitting the pipeline with an Exponential Smoothing model."""
        self.pipeline.preprocessors = [SimpleExponentialSmoothing(alpha=0.2)]
        self.pipeline.models = [ARIMA(order=(1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_exponential_smoothing_model(self):
        """Test fitting the pipeline with an Exponential Smoothing model."""
        self.pipeline.preprocessors = [SimpleExponentialSmoothing(alpha=0.2)]
        self.pipeline.models = [SimpleExponentialSmoothing(alpha=0.2)]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_double_exponential_smoothing(self):
        """Test fitting the pipeline with a Double Exponential Smoothing model."""
        self.pipeline.preprocessors = [DoubleExponentialSmoothing(alpha=0.2, beta=0.1)]
        self.pipeline.models = [ARIMA(order=(1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_double_exponential_smoothing_model(self):
        """Test fitting the pipeline with a Double Exponential Smoothing model."""
        self.pipeline.preprocessors = [DoubleExponentialSmoothing(alpha=0.2, beta=0.1)]
        self.pipeline.models = [DoubleExponentialSmoothing(alpha=0.2, beta=0.1)]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_triple_exponential_smoothing(self):
        """Test fitting the pipeline with a Triple Exponential Smoothing model."""
        self.pipeline.preprocessors = [
            TripleExponentialSmoothing(alpha=0.2, beta=0.1, gamma=0.1, period=2)
        ]
        self.pipeline.models = [ARIMA(order=(1, 1, 1))]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_fit_triple_exponential_smoothing_model(self):
        """Test fitting the pipeline with a Triple Exponential Smoothing model."""
        self.pipeline.preprocessors = [
            TripleExponentialSmoothing(alpha=0.2, beta=0.1, gamma=0.1, period=2)
        ]
        self.pipeline.models = [
            TripleExponentialSmoothing(alpha=0.2, beta=0.1, gamma=0.1, period=2)
        ]
        self.pipeline.fit(self.train_series)
        self.assertIsNotNone(self.pipeline.models)

    def test_predict(self):
        """Test making predictions with the pipeline."""
        self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
        self.pipeline.models = [SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))]
        self.pipeline.fit(self.train_series)
        predictions = self.pipeline.predict(self.test_series, steps=2)
        self.assertEqual(len(predictions), 2)

    def test_predict_no_model(self):
        """Test making predictions with no model in the pipeline."""
        self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
        with self.assertRaises(ValueError):
            self.pipeline.predict(self.test_series, steps=2)

    def test_predict_no_preprocessors(self):
        """Test making predictions with no preprocessors in the pipeline."""
        self.pipeline.models = [SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))]
        self.pipeline.fit(self.train_series)
        predictions = self.pipeline.predict(self.test_series, steps=2)
        self.assertEqual(len(predictions), 2)

    def test_evaluate(self):
        """Test evaluating the pipeline."""
        self.pipeline.models = [SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))]
        self.pipeline.evaluators = [Metrics.mean_squared_error]
        self.pipeline.fit(self.train_series)
        predictions = self.pipeline.predict(self.test_series, steps=2)
        results = self.pipeline.evaluate(predictions, self.test_series)
        self.assertIn("mean_squared_error", results)

    def test_evaluate_no_evaluators(self):
        """Test evaluating the pipeline with no evaluators."""
        self.pipeline.models = [SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))]
        self.pipeline.fit(self.train_series)
        predictions = self.pipeline.predict(self.test_series, steps=2)
        with self.assertRaises(ValueError):
            self.pipeline.evaluate(predictions, self.test_series)

    def test_summary(self):
        """Test the summary method."""
        with suppress_print():
            self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
            self.pipeline.models = [
                SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
            ]
            self.pipeline.evaluators = [Metrics.mean_squared_error]
            self.pipeline.summary()

    def test_summary_no_model(self):
        """Test the summary method with no model."""
        with suppress_print():
            self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
            self.pipeline.evaluators = [Metrics.mean_squared_error]
            self.pipeline.summary()

    def test_summary_no_preprocessors(self):
        """Test the summary method with no preprocessors."""
        with suppress_print():
            self.pipeline.models = [
                SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
            ]
            self.pipeline.evaluators = [Metrics.mean_squared_error]
            self.pipeline.summary()

    def test_summary_no_evaluators(self):
        """Test the summary method with no evaluators."""
        with suppress_print():
            self.pipeline.models = [
                SARIMA(order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
            ]
            self.pipeline.preprocessors = [WeightedMovingAverage(window=3)]
            self.pipeline.summary()


if __name__ == "__main__":
    unittest.main()
