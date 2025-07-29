import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn import *
from tests.utils import BaseTest


class TestImports(BaseTest):
    """Tests that the main package can be imported correctly."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Imports - Main Package", end="", flush=True)

    def test_all_imports(self):  # NOQA D201
        import sega_learn

        assert sega_learn is not None
        assert sega_learn.linear_models is not None
        assert sega_learn.clustering is not None
        assert sega_learn.utils is not None
        assert sega_learn.trees is not None
        assert sega_learn.neural_networks is not None
        assert sega_learn.nearest_neighbors is not None
        assert sega_learn.svm is not None
        assert sega_learn.auto is not None
        assert sega_learn.time_series is not None
        assert sega_learn.make_sample_data is not None

    def test_module_imports(self):  # NOQA D201
        from sega_learn import (
            auto,
            clustering,
            linear_models,
            make_sample_data,
            nearest_neighbors,
            neural_networks,
            svm,
            time_series,
            trees,
            utils,
        )

        assert clustering is not None
        assert linear_models is not None
        assert utils is not None
        assert neural_networks is not None
        assert svm is not None
        assert trees is not None
        assert nearest_neighbors is not None
        assert auto is not None
        assert time_series is not None
        assert make_sample_data is not None

    def test_auto_imports(self):  # NOQA D201
        assert AutoClassifier is not None
        assert AutoRegressor is not None

    def test_clustering_imports(self):  # NOQA D201
        assert DBSCAN is not None
        assert KMeans is not None

    def test_linear_models_imports(self):  # NOQA D201
        assert RANSAC is not None
        assert Bayesian is not None
        assert Lasso is not None
        assert LinearDiscriminantAnalysis is not None
        assert LogisticRegression is not None
        assert OrdinaryLeastSquares is not None
        assert PassiveAggressiveRegressor is not None
        assert Perceptron is not None
        assert QuadraticDiscriminantAnalysis is not None
        assert Ridge is not None
        assert make_sample_data is not None

    def test_nearest_neighbors_imports(self):  # NOQA D201
        assert KNeighborsClassifier is not None
        assert KNeighborsRegressor is not None

    def test_neural_networks_imports(self):  # NOQA D201
        assert Activation is not None
        assert AdadeltaOptimizer is not None
        assert AdamOptimizer is not None
        assert BaseBackendNeuralNetwork is not None
        assert BCEWithLogitsLoss is not None
        assert ConvLayer is not None
        assert CrossEntropyLoss is not None
        assert DenseLayer is not None
        assert FlattenLayer is not None
        assert HuberLoss is not None
        assert MeanAbsoluteErrorLoss is not None
        assert MeanSquaredErrorLoss is not None
        assert NeuralNetworkBase is not None
        assert RNNLayer is not None
        assert SGDOptimizer is not None
        assert lr_scheduler_exp is not None
        assert lr_scheduler_plateau is not None
        assert lr_scheduler_step is not None

    def test_svm_imports(self):  # NOQA D201
        assert BaseSVM is not None
        assert GeneralizedSVC is not None
        assert GeneralizedSVR is not None
        assert LinearSVC is not None
        assert LinearSVR is not None
        assert OneClassSVM is not None

    def test_trees_imports(self):  # NOQA D201
        assert ClassifierTree is not None
        assert ClassifierTreeUtility is not None
        assert GradientBoostedClassifier is not None
        assert GradientBoostedRegressor is not None
        assert IsolationForest is not None
        assert IsolationTree is not None
        assert IsolationUtils is not None
        assert RandomForestClassifier is not None
        assert RandomForestRegressor is not None
        assert RegressorTree is not None
        assert RegressorTreeUtility is not None
        assert AdaBoostClassifier is not None
        assert AdaBoostRegressor is not None

    def test_time_series_imports(self):  # NOQA D201
        assert ARIMA is not None
        assert SARIMA is not None
        assert SARIMAX is not None
        assert DoubleExponentialSmoothing is not None
        assert SimpleExponentialSmoothing is not None
        assert TripleExponentialSmoothing is not None
        assert SimpleMovingAverage is not None
        assert WeightedMovingAverage is not None
        assert ExponentialMovingAverage is not None
        assert AdditiveDecomposition is not None
        assert MultiplicativeDecomposition is not None

    def test_utils_imports(self):  # NOQA D201
        assert AnimationBase is not None
        assert RegressionAnimation is not None
        assert ForcastingAnimation is not None
        assert ClassificationAnimation is not None
        assert PCA is not None
        assert SMOTE is not None
        assert SVD is not None
        assert Augmenter is not None
        assert DataPrep is not None
        assert GridSearchCV is not None
        assert Metrics is not None
        assert ModelSelectionUtility is not None
        assert PolynomialTransform is not None
        assert RandomOverSampler is not None
        assert RandomSearchCV is not None
        assert RandomUnderSampler is not None
        assert Scaler is not None
        assert Encoder is not None
        assert VotingRegressor is not None
        assert VotingClassifier is not None
        assert ForecastRegressor is not None
        assert StatisticalImputer is not None
        assert DirectionalImputer is not None
        assert InterpolationImputer is not None
        assert KNNImputer is not None
        assert CustomImputer is not None
        assert make_blobs is not None
        assert make_classification is not None
        assert make_regression is not None
        assert make_time_series is not None
        assert normalize is not None
        assert one_hot_encode is not None
        assert train_test_split is not None

    def test_jit_imports(self):  # NOQA D201
        assert JITAdamOptimizer is not None
        assert JITSGDOptimizer is not None
        assert JITAdadeltaOptimizer is not None
        assert JITBCEWithLogitsLoss is not None
        assert JITCrossEntropyLoss is not None
        assert JITMeanSquaredErrorLoss is not None
        assert JITMeanAbsoluteErrorLoss is not None
        assert JITHuberLoss is not None
        assert JITDenseLayer is not None
        assert JITFlattenLayer is not None
        assert JITConvLayer is not None
        assert JITRNNLayer is not None
        assert NumbaBackendNeuralNetwork is not None


if __name__ == "__main__":
    unittest.main()
