# SEGA_LEARN

[![PyPI version](https://badge.fury.io/py/sega_learn.svg)](https://badge.fury.io/py/sega_learn)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/SantiagoEnriqueGA/sega_learn/.github/workflows/core-tests.yml?branch=main)](https://github.com/SantiagoEnriqueGA/sega_learn/actions/workflows/core-tests.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/sega_learn.svg)](https://pypi.org/project/sega_learn/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-blue.svg)](https://github.com/charliermarsh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SEGA_LEARN is a custom package implementating machine learning algorithms built from the Python standard library as well as NumPy and SciPy.
It includes scratch implementations of various machine learning algorithms, including clustering, linear models, neural networks, and trees.
The project also includes scripts for testing, documentation generation, and other tasks.

The project is organized into several directories, each with its own purpose.
The `SEGA_LEARN/` directory contains the main library code, while the `tests/` directory contains unit and performance tests.
The `examples/` directory contains example usages of the library, and the `docs/` directory contains the generated documentation.
The `scripts/` directory contains PowerShell scripts to help with various tasks.

This project was created with the goal of learning about the internals of machine learning algorithms and how they work under the hood.
As well as for exploration of Python packages for speed and performance.
It is not intended for production use and should be used for educational purposes only (See performance tests for scalability).
Many of the algorithms are not optimized for performance and may not be suitable for large datasets.

This project was heavily inspired by [scikit-learn](https://scikit-learn.org/stable/), and [pytorch](https://pytorch.org/).

## Navigation
<!-- Add Links to Other Sections Here! -->
- [Features](#features)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Helper Scripts](#helper-scripts)
- [Documentation](#documentation)
- [Tests](#tests)
- [Installation](#installation)

### Module Level READMEs
For more detailed information on each module, see the following READMEs:
- [Automated Machine Learning Module](sega_learn/auto/README.md)
- [Clustering Module](sega_learn/clustering/README.md)
- [Linear Models Module](sega_learn/linear_models/README.md)
- [Nearest Neighbors Module](sega_learn/nearest_neighbors/README.MD)
- [Neural Networks Module](sega_learn/neural_networks/README.md)
- [Pipelines Module](sega_learn/pipelines/README.MD)
- [Trees Module](sega_learn/trees/README.md)
- [Time Series Module](sega_learn/time_series/README.md)
- [SVM Module](sega_learn/svm/README.md)
- [Utilities Module](sega_learn/utils/README.md)

## Features
The SEGA_LEARN library includes the following features:

### Automated Machine Learning
*   **Automated ML (`auto`)**: Simplified `AutoClassifier` and `AutoRegressor` interfaces for automatically selecting and training suitable models from the Sega Learn library, providing quick baselines for classification and regression tasks.

### Clustering
- **DBSCAN**: Density-Based Spatial Clustering of Applications with Noise (DBSCAN) is a clustering algorithm that groups together points that are closely packed, marking as outliers points that lie alone in low-density regions.
- **KMeans**: KMeans is a clustering algorithm that partitions n data points into k clusters in which each point belongs to the cluster with the nearest mean.

### Linear Models
- **Bayesian Regression**: Bayesian regression is a probabilistic approach to linear regression that allows incorporating prior knowledge about the model parameters.
- **Lasso Regression**: Lasso (Least Absolute Shrinkage and Selection Operator) regression is a linear regression model that uses L1 regularization to perform feature selection.
- **Ridge Regression**: Ridge regression is a linear regression model that uses L2 regularization to prevent overfitting by penalizing large coefficients.
- **Linear Discriminant Analysis**: Linear Discriminant Analysis (LDA) is a classification algorithm that finds the linear combination of features that best separates two or more classes.
- **Ordinary Least Squares**: Ordinary Least Squares (OLS) is a linear regression model that minimizes the sum of the squared differences between the observed and predicted values.
- **Passive Aggressive Regressor**: Passive Aggressive Regressor is a linear regression model that updates its parameters using a passive or aggressive strategy based on the loss function.
- **Quadratic Discriminant Analysis**: Quadratic Discriminant Analysis (QDA) is a classification algorithm that finds the quadratic combination of features that best separates two or more classes.
- **RANSAC Regression**: Random Sample Consensus (RANSAC) regression is a linear regression model that fits a model to the data by iteratively selecting a subset of inliers and estimating the model parameters.
- **Logistic Regression**: Logistic regression is a linear model for binary classification that uses the logistic function to model the probability of a class label.
- **Perceptron**: The Perceptron is a simple linear binary classifier that makes its predictions based on a linear predictor function combining a set of weights with the feature vector.

### Nearest Neighbors
- **KNeighborsClassifier**: Implements the K-Nearest Neighbors algorithm for classification tasks.
- **KNeighborsRegressor**: Implements the K-Nearest Neighbors algorithm for regression tasks.

### Neural Networks
- **Neural Networks:** Flexible implementation with support for various layers, activations, optimizers, and backends (NumPy, Numba, CuPy), now supporting both **classification and regression** tasks.
  - **Optimizers**: Implements various optimizers like Adadelta, Adam, and SGD.
  - **Loss Functions**: Implements loss functions like BCEWithLogitsLoss, CrossEntropyLoss, MeanSquaredErrorLoss, MeanAbsoluteErrorLoss, and HuberLoss.
  - **Schedulers**: Implements learning rate schedulers like StepLR and ReduceLROnPlateau.
  - **Activation Functions**: Implements activation functions like ReLU, Sigmoid, Softmax and more.

### Support Vector Machines (SVMs)
- **Linear SVM Classifier**: A linear SVM classifier for binary and multi-class classification tasks.
- **Linear SVM Regressor**: A linear SVM regressor for predicting continuous target values.
- **Generalized SVM Classifier**: Supports multiple kernels (e.g., RBF, polynomial) for binary and multi-class classification.
- **Generalized SVM Regressor**: Supports multiple kernels for regression tasks.
- **One-Class SVM**: Used for anomaly detection by identifying inliers and outliers in the data.
- **Kernel Functions**: Includes linear, polynomial, RBF, and sigmoid kernels for handling non-linear problems.

### Trees
- **Classifier Tree**: Implements a decision tree classifier that recursively splits the data based on the feature that maximizes the information gain.
- **Regressor Tree**: Implements a decision tree regressor that recursively splits the data based on the feature that minimizes the variance.
- **Random Forest Classifier**: Implements an ensemble classifier that fits multiple decision trees on random subsets of the data and averages their predictions.
- **Random Forest Regressor**: Implements an ensemble regressor that fits multiple decision trees on random subsets of the data and averages their predictions.
- **Gradient Boosted Regressor**: Implements a gradient boosted regressor that fits multiple decision trees sequentially, each one correcting the errors of the previous trees.
- **Gradient Boosted Classifier**: Implements a gradient boosted classifier that fits multiple decision trees sequentially, each one correcting the errors of the previous trees.
- **Isolation Forest**: Implements an anomaly detection algorithm that isolates anomalies by randomly partitioning the data.
- **AdaBoost Classifier**: Implements an ensemble classifier that combines multiple weak classifiers to create a strong classifier.
- **AdaBoost Regressor**: Implements an ensemble regressor that combines multiple weak regressors to create a strong regressor.

### Time Series
- **ARIMA**: Implements the AutoRegressive Integrated Moving Average (ARIMA) model for time series forecasting.
- **SARIMA**: Implements the Seasonal AutoRegressive Integrated Moving Average (SARIMA) model for time series forecasting with seasonality.
- **SARIMAX**: Implements the Seasonal AutoRegressive Integrated Moving Average with eXogenous variables (SARIMAX) model for time series forecasting with seasonality and exogenous variables.
- **Additive Decomposition**: Implements the additive decomposition of time series data into trend, seasonal, and residual components.
- **Multiplicative Decomposition**: Implements the multiplicative decomposition of time series data into trend, seasonal, and residual components.
- **Simple Exponential Smoothing**: Implements simple exponential smoothing for time series forecasting.
- **Double Exponential Smoothing**: Implements double exponential smoothing for time series forecasting, also known as Holt's linear trend method.
- **Triple Exponential Smoothing**: Implements triple exponential smoothing for time series forecasting, also known as Holt-Winters seasonal method.
- **Simple Moving Average**: Implements the simple moving average for time series forecasting.
- **Weighted Moving Average**: Implements the weighted moving average for time series forecasting.
- **Exponential Moving Average**: Implements the exponential moving average for time series forecasting.

### Pipelines
- **Generic Pipeline**: Implements a generic pipeline for machine learning tasks: Classification and Regression.
- **Forecasting Pipeline**: Implements a custom forecasting pipeline for time series forecasting.

### Utilities
- **Animator**: Implements a custom animation class for visualizing machine learning models, updating one parameter and observing the changes in the model's performance.
- **Data Preparation**: Implements utility functions for data preparation like train-test split, normalization, and standardization.
- **Voting Regressor**: Implements a voting regressor that combines the predictions of multiple regressors using a weighted average.
- **Voting Classifier**: Implements a voting classifier that combines the predictions of multiple classifiers using a weighted average.
- **Voting Forcaster**: Implements a voting forecaster that combines the predictions of multiple forecasters using a weighted average.
- **Polynomial Transformation**: Implements polynomial transformation of features to create higher-order polynomial features.
- **Evaluation Metrics**: Implements evaluation metrics like mean squared error, mean absolute error, and R-squared.
- **Model Selection Algorithms**: Implements model selection algorithms like Grid Search Cross Validation and Random Search Cross Validation.
- **Data Augmentation**: Implements data augmentation for imbalanced classification tasks using SMOTE (Synthetic Minority Over-sampling Technique), Under-sampling, Over-sampling, and/or a combination of each.
- **Imputation**: Implements imputation techniques like mean imputation, median imputation, and KNN imputation.


### Planned Features - Future Work
- Implement OPTICS clustering algorithm


## Project Structure
The project directory structure is as follows:

```
sega_learn/
|
├── sega_learn/      # Main library source code
│   ├── auto/               # Automated model creation/comparison
│   ├── clustering/         # Clustering algorithms
│   ├── linear_models/      # Linear models
│   ├── nearest_neighbors/  # K-Nearest Neighbors
│   ├── neural_networks/    # Neural Network components
│   ├── pipelines/          # Pipelines for machine learning tasks
│   ├── svm/                # Support Vector Machines
│   ├── trees/              # Tree-based models
│   ├── time_series/        # Time series models
│   └── utils/              # Utility functions (metrics, data prep, etc.)
|
├── examples/           # Usage examples for different modules
|
├── tests/              # Unit tests for the library code
|
├── tests_performance/  # Performance benchmark tests
|
├── docs/               # Documentation source files (e.g., Markdown)
|
├── scripts/            # Helper scripts (e.g., for building docs, environment setup)
|
├── .github/                      # GitHub specific files (workflows for CI)
│   ├── PULL_REQUEST_TEMPLATE.md  # Pull request template
│   └── workflows/
|       ├── lint-format.yml       # Ruff CI check workflow
│       └── run-tests.yml         # Unit tests CI check workflow
|
├── .gitattributes          # Git attributes for the repository
├── .gitignore              # Files/directories ignored by Git
├── .pre-commit-config.yaml # Configuration for pre-commit hooks
├── DEVELOPMENT.md          # This file: Guide for developers
├── environment.yml         # Conda environment definition
├── environment_pypy.yml    # Conda environment definition for pypy
├── pyproject.toml          # Project metadata, build config, Ruff config
├── pypdoc-markdown.yml     # Pydoc markdown config
├── README.md               # Main project README for users
└── uv.lock                 # Lock file for uv
```

## Usage Examples

### Automated Machine Learning
- [`classifier.py`](examples/auto/classifier.py): Demonstrates the AutoClassifier on a simple classification problem.
- [`regressor.py`](examples/auto/regressor.py): Demonstrates the AutoRegressor on a simple regression problem.

### Clustering
- [`kmeans.py`](examples/clustering/kmeans.py): Demonstrates KMeans.
- [`dbscan.py`](examples/clustering/dbscan.py): Demonstrates DBSCAN.
- [`dbscan_3d.py`](examples/clustering/dbscan_3d.py): Demonstrates DBSCAN with 3D data.
- [`dbscan_3d_aimated.py`](examples/clustering/dbscan_3d_aimated.py): Demonstrates DBSCAN with 3D data and animated plot.

### Linear Models
- [`bayes.py`](examples/linear_models/bayes.py): Demonstrates Bayesian Regression.
- [`lasso.py`](examples/linear_models/lasso.py): Demonstrates Lasso Regression.
- [`lda.py`](examples/linear_models/lda.py): Demonstrates Linear Discriminant Analysis.
- [`lda_comparison.py`](examples/linear_models/lda_comparison.py): Demonstrates Linear Discriminant Analysis with different solvers.
- [`lda_vs_qda_comparison.py`](examples/linear_models/lda_vs_qda_comparison.py): Demonstrates Linear Discriminant Analysis vs Quadratic Discriminant Analysis.
- [`logisticRegression.py`](examples/linear_models/logisticRegression.py): Demonstrates Logistic Regression.
- [`ols.py`](examples/linear_models/ols.py): Demonstrates Ordinary Least Squares.
- [`passiveAggressive_vis.py`](examples/linear_models/passiveAggressive_vis.py): Demonstrates Passive Aggressive Regressor with visualization.
- [`passiveAggressive.py`](examples/linear_models/passiveAggressive.py): Demonstrates Passive Aggressive Regressor.
- [`perceptron.py`](examples/linear_models/perceptron.py): Demonstrates Perceptron.
- [`qda.py`](examples/linear_models/qda.py): Demonstrates Quadratic Discriminant Analysis.
- [`ransac_vis.py`](examples/linear_models/ransac_vis.py): Demonstrates RANSAC Regression with visualization.
- [`ransac.py`](examples/linear_models/ransac.py): Demonstrates RANSAC Regression.
- [`ridge.py`](examples/linear_models/ridge.py): Demonstrates Ridge Regression.

### Nearest Neighbors
- [`nearestNeighborsClassifier.py`](examples/nearest_neighbors/nearestNeighborsClassifier.py): Demonstrates KNeighborsClassifier.
- [`nearestNeighborsRegressor.py`](examples/nearest_neighbors/nearestNeighborsRegressor.py): Demonstrates KNeighborsRegressor.

### Neural Networks
- [`neuralNetwork_cancer.py`](examples/neural_networks/neuralNetwork_cancer.py): Demonstrates the NeuralNetwork class on the breast cancer dataset.
- [`neuralNetwork_classifier_hyper.py`](examples/neural_networks/neuralNetwork_classifier_hyper.py): Demonstrates the NeuralNetwork class for hyper-parameter tuning on classification tasks.
- [`neuralNetwork_classifier.py`](examples/neural_networks/neuralNetwork_classifier.py): Demonstrates the NeuralNetwork class for classification tasks.
- [`neuralNetwork_diabetes.py`](examples/neural_networks/neuralNetwork_diabetes.py): Demonstrates the NeuralNetwork class on the diabetes dataset.
- [`neuralNetwork_hyper.py`](examples/neural_networks/neuralNetwork_hyper.py): Demonstrates the NeuralNetwork class for hyper-parameter tuning on regression tasks.
- [`neuralNetwork_iris.py`](examples/neural_networks/neuralNetwork_iris.py): Demonstrates the NeuralNetwork class on the iris dataset.
- [`neuralNetwork_layers_conv_cifar.py`](examples/neural_networks/neuralNetwork_layers_conv_cifar.py): Demonstrates the NeuralNetwork class with convolutional layers on CIFAR dataset.
- [`neuralNetwork_layers_conv.py`](examples/neural_networks/neuralNetwork_layers_conv.py): Demonstrates the NeuralNetwork class with convolutional layers.
- [`neuralNetwork_layers_numba.py`](examples/neural_networks/neuralNetwork_layers_numba.py): Demonstrates the NeuralNetwork class with Numba optimization.
- [`neuralNetwork_layers.py`](examples/neural_networks/neuralNetwork_layers.py): Demonstrates the NeuralNetwork class with multiple layer creation.
- [`neuralNetwork_metrics_anim.py`](examples/neural_networks/neuralNetwork_metrics_anim.py): Demonstrates the NeuralNetwork class with animated metrics.
- [`neuralNetwork_regressor.py`](examples/neural_networks/neuralNetwork_regressor.py): Demonstrates the NeuralNetwork class for regression tasks.

### SVM
- [`generalizedSCV_binary.py`](examples/svm/generalizedSVC_binary.py): Demonstrates the Generalized SVC for binary classification.
- [`generalizedSCV_multi.py`](examples/svm/generalizedSVC_multi.py): Demonstrates the Generalized SVC for multi-class classification.
- [`generalizedSVR.py`](examples/svm/generalizedSVR.py): Demonstrates the Generalized SVR for regression tasks.
- [`linearSVC_binary.py`](examples/svm/linearSVC_binary.py): Demonstrates the Linear SVC for binary classification.
- [`linearSVC_multi.py`](examples/svm/linearSVC_multi.py): Demonstrates the Linear SVC for multi-class classification.
- [`linearSVR.py`](examples/svm/linearSVR.py): Demonstrates the Linear SVR for regression tasks.
- [`oneClassSVM.py`](examples/svm/oneClassSVM.py): Demonstrates the One-Class SVM for anomaly detection.

### Trees
- [`adaBoostClassifier.py`](examples/trees/adaBoostClassifier.py): Demonstrates AdaBoost Classifier.
- [`adaBoostRegressor.py`](examples/trees/adaBoostRegressor.py): Demonstrates AdaBoost Regressor.
- [`gradientBoostedRegressor.py`](examples/trees/gradientBoostedRegressor.py): Demonstrates Gradient Boosted Regressor.
- [`gradientBoostedClassifier.py`](examples/trees/gradientBoostedClassifier.py): Demonstrates Gradient Boosted Classifier.
- [`isolationForest_blob.py`](examples/utils/isolationForest_blob.py): Demonstrates Isolation Forest for anomaly detection.
- [`isolationForest_boundary.py`](examples/utils/isolationForest_boundary.py): Demonstrates Isolation Forest for anomaly detection with boundary visualization.
- [`isolationForest_reg.py`](examples/utils/isolationForest_reg.py): Demonstrates Isolation Forest for regression tasks.
- [`randomForestClassifier.py`](examples/trees/randomForestClassifier.py): Demonstrates Random Forest Classifier.
- [`randomForestRegressor.py`](examples/trees/randomForestRegressor.py): Demonstrates Random Forest Regressor.

### Time Series
- [`arima_arima.py`](examples/time_series/arima_arima.py): Demonstrates ARIMA model for time series forecasting.
- [`arima_sarima.py`](examples/time_series/arima_sarima.py): Demonstrates SARIMA model for time series forecasting.
- [`arima_sarimax.py`](examples/time_series/arima_sarimax.py): Demonstrates SARIMAX model for time series forecasting.
- [`decom_additiveDecomposition.py`](examples/time_series/decom_additiveDecomposition.py): Demonstrates additive decomposition of time series data.
- [`decom_multiplicativeDecomposition.py`](examples/time_series/decom_multiplicativeDecomposition.py): Demonstrates multiplicative decomposition of time series data.
- [`mvg_simpleMovingAverage.py`](examples/time_series/mvg_simpleMovingAverage.py): Demonstrates simple moving average for time series forecasting.
- [`mvg_weightedMovingAverage.py`](examples/time_series/mvg_weightedMovingAverage.py): Demonstrates weighted moving average for time series forecasting.
- [`mvg_exponentialMovingAverage.py`](examples/time_series/mvg_exponentialMovingAverage.py): Demonstrates exponential moving average for time series forecasting.
- [`smth_simpleExponentialSmoothing.py`](examples/time_series/smth_simpleExponentialSmoothing.py): Demonstrates simple exponential smoothing for time series forecasting.
- [`smth_doubleExponentialSmoothing.py`](examples/time_series/smth_doubleExponentialSmoothing.py): Demonstrates double exponential smoothing for time series forecasting.
- [`smth_tripleExponentialSmoothing.py`](examples/time_series/smth_tripleExponentialSmoothing.py): Demonstrates triple exponential smoothing for time series forecasting.

### Pipelines
- [`pipeline_classification_tuning.py`](examples/pipelines/pipeline_classification_tuning.py): Demonstrates a custom pipeline for classification with hyperparameter tuning.
- [`pipeline_classification.py`](examples/pipelines/pipeline_classification.py): Demonstrates a custom pipeline for classification.
- [`pipeline_regression_tuning.py`](examples/pipelines/pipeline_regression_tuning.py): Demonstrates a custom pipeline for regression with hyperparameter tuning.
- [`pipeline_regression.py`](examples/pipelines/pipeline_regression.py): Demonstrates a custom pipeline for regression.
- [`pipeline_forecasting.py`](examples/pipelines/pipeline_forecasting.py): Demonstrates a custom pipeline for time series forecasting.

### Utils
- [`animator_exponentialMovingAverage.py`](examples/utils/animator_exponentialMovingAverage.py): Demonstrates the Animator class for visualizing the ExponentialMovingAverage model.
- [`animator_logisticRegression.py`](examples/utils/animator_logisticRegression.py): Demonstrates the Animator class for visualizing the LogisticRegression model.
- [`animator_perceptron.py`](examples/utils/animator_perceptron.py): Demonstrates the Animator class for visualizing the Perceptron model.
- [`animator_ridge.py`](examples/utils/animator_ridge.py): Demonstrates the Animator class for visualizing the Ridge model.
- [`animator_weightedMovingAverage.py`](examples/utils/animator_weightedMovingAverage.py): Demonstrates the Animator class for visualizing the WeightedMovingAverage model.
- [`dataAugmentation_combined.py`](examples/utils/dataAugmentation_combined.py): Demonstrates a combination of Random Over Sampling and SMOTE for imbalanced classification tasks.
- [`dataAugmentation_randOver.py`](examples/utils/dataAugmentation_randOver.py): Demonstrates Random Over Sampling for imbalanced classification tasks.
- [`dataAugmentation_randUnder.py`](examples/utils/dataAugmentation_randUnder.py): Demonstrates Random Under Sampling for imbalanced classification tasks.
- [`dataAugmentation_smote.py`](examples/utils/dataAugmentation_smote.py): Demonstrates SMOTE (Synthetic Minority Over-sampling Technique) for imbalanced classification tasks.
- ['dataPreprocessing.py'](examples/utils/dataPreprocessing.py): Demonstrates data preprocessing techniques.
- [`encoder_binarizer.py`](examples/utils/encoder_binarizer.py): Demonstrates Binarizer and LabelEncoder.
- [`encoder_label.py`](examples/utils/encoder_label.py): Demonstrates LabelEncoder.
- [`gridSearchCV_bayes.py`](examples/utils/gridSearchCV_bayes.py): Demonstrates Grid Search Cross Validation with Bayesian Regression.
- [`gridSearchCV_gbr.py`](examples/utils/gridSearchCV_gbr.py): Demonstrates Grid Search Cross Validation with Gradient Boosted Regressor.
- [`gridSearchCV_passiveAggressive.py`](examples/utils/gridSearchCV_passiveAggressive.py): Demonstrates Grid Search Cross Validation with Passive Aggressive Regressor.
- [`gridSearchCV_rfc.py`](examples/utils/gridSearchCV_rfc.py): Demonstrates Grid Search Cross Validation with Random Forest Classifier.
- [`gridSearchCV_rfr.py`](examples/utils/gridSearchCV_rfr.py): Demonstrates Grid Search Cross Validation with Random Forest Regressor.
- [`imputater_custom.py`](examples/utils/imputater_custom.py): Demonstrates Custom Imputer.
- [`imputater_directional.py`](examples/utils/imputater_directional.py): Demonstrates Directional Imputer.
- [`imputater_interpolation.py`](examples/utils/imputater_interpolation.py): Demonstrates Interpolation Imputer.
- [`imputater_knn.py`](examples/utils/imputater_knn.py): Demonstrates KNN Imputer.
- [`imputater_statistical.py`](examples/utils/imputater_statistical.py): Demonstrates Statistical Imputer.
- [`makeData.py`](examples/utils/makeData.py): Demonstrates data generation for testing purposes.
- [`pca_classification.py`](examples/utils/pca_classification.py): Demonstrates PCA for classification tasks.
- [`pca_regression.py`](examples/utils/pca_regression.py): Demonstrates PCA for regression tasks.
- [`polynomialTransform.py`](examples/utils/polynomialTransform.py): Demonstrates Polynomial Transform.
- [`randomSearchCV_bayes.py`](examples/utils/randomSearchCV_bayes.py): Demonstrates Random Search Cross Validation with Bayesian Regression.
- [`randomSearchCV_gbr.py`](examples/utils/randomSearchCV_gbr.py): Demonstrates Random Search Cross Validation with Gradient Boosted Regressor.
- [`randomSearchCV_passiveAggressive.py`](examples/utils/randomSearchCV_passiveAggressive.py): Demonstrates Random Search Cross Validation with Passive Aggressive Regressor.
- [`randomSearchCV_rfc.py`](examples/utils/randomSearchCV_rfc.py): Demonstrates Random Search Cross Validation with Random Forest Classifier.
- [`randomSearchCV_rfr.py`](examples/utils/randomSearchCV_rfr.py): Demonstrates Random Search Cross Validation with Random Forest Regressor.
- ['segaSearchCV_rfr.py'](examples/utils/segaSearchCV_rfr.py): Demonstrates SEGA Search Cross Validation with Random Forest Regressor.
- [`svd_classification.py`](examples/utils/svd_classification.py): Demonstrates SVD for classification tasks.
- [`svd_regression.py`](examples/utils/svd_regression.py): Demonstrates SVD for regression tasks.
- [`votingRegressor.py`](examples/utils/votingRegressor.py): Demonstrates Voting Regressor.
- [`votingClassifier.py`](examples/utils/votingClassifier.py): Demonstrates Voting Classifier.

## Helper Scripts
The following PowerShell scripts are included in the `scripts/` folder to help with various tasks:

- **_run_all_scripts.ps1**: Runs all PowerShell scripts in the `scripts/` folder sequentially.
- **todo_comments.ps1**: Finds and lists all TODO comments in Python files.
- **count_lines.ps1**: Counts the number of lines in each Python file, sorts the files by line count in descending order, and calculates the total number of lines.
- **comment_density.ps1**: Calculates the comment density (percentage of lines that are comments) in Python files.
- **documentation_html.ps1**: Generates HTML documentation for Python files in the `SEGA_LEARN/` folder, and moves the generated HTML files to the `docs/` folder.
- **documentation_md.ps1**: Generates markdown documentation for Python files in the `SEGA_LEARN/` folder.
- **export_env.ps1**: Exports the conda environment to a YAML file. Remove the prefix from the environment name to make it compatible with other systems.
- **file_contents.ps1**: Exports the contents of all python files in the `SEGA_LEARN/` folder to a text file.

## Documentation
### HTML Documentation
Pydoc documentation is generated from the PowerShell script `documentation_html.ps1`.
To see live version: https://santiagoenriquega.github.io/sega_learn/sega_learn

Self host documentation, run the following command in the terminal: `python -m pydoc -p 8080`
Then open a web browser and navigate to http://localhost:8080/SEGA_LEARN.html

### Markdown Documentation
Pydoc Markdown is also availible and is generated from the PowerShell script `documentation_md.ps1`.
The output file is located in [`docs/documentation.md`](docs/documentation.md)

## Tests
An extensive suite of unit tests is included in the `tests/` directory.
These tests ensure the functionality and reliability of each module in the library, as well as the overall package.
The tests are organized into subdirectories based on the module they test. Each module is tested for imports, functionality, and example usage.

### Test Logic
- **Imports**: Tests to ensure that all modules can be imported without errors.
- **Functionality**: Tests to ensure that the functions and classes in each module work as expected.
- **Examples**: Tests to ensure that the example scripts run without errors.

### Running Tests
To run the tests, use the following command: `python -m unittest discover -s tests`
Or run the all tests file: `python run_all_tests.py`

### Test Results
The following are the results of running the tests:
```
(sega_learn) PS .../sega_learn/tests/run_all_tests.py
Testing Imports - Auto....
Testing Imports - Clustering....
Testing Imports - Main Package............
Testing Imports - Linear Models.............
Testing Imports - Nearest Neighbors....
Testing Imports - Neural Networks.........................
Testing Imports - Pipelines....
Testing Imports - SVM........
Testing Imports - Time Series.............
Testing Imports - Trees............
Testing Imports - Utils....................................
Testing AutoClassifier Model...................
Testing AutoRegressor Model.......................
Testing DBSCAN...............
Testing DBSCAN Numba...............
Testing KMeans..................................
Testing Bayesian Regression Model.............
Testing Lasso Regression Model...............
Testing Linear Discriminant Analysis..........
Testing Logistic Regression.......     
Testing Ordinary Least Squares Model..........
Testing Passive Aggressive Regressor Model.............
Testing Perceptron.......
Testing Quadratic Discriminant Analysis..........
Testing RANSAC Regression Model..............
Testing Ridge Regression Model...............
Testing KNeighborsClassifierKNeighborsBase............
Testing KNeighborsRegressor............
Testing TrainingAnimator...........
Testing NeuralNetwork class with base backend.......................
Testing Comparing NeuralNetwork Base and Numba Activations............
Testing Comparing NeuralNetwork Base and Numba Loss Functions........
Testing Comparing NeuralNetwork Base and Numba Optimizers.........
Testing Comparing NeuralNetwork Base and Numba Train Functions.......
Testing Comparing NeuralNetwork Base and Numba Utilities......
Testing ConvLayer.................     
Testing DenseLayer.....................
Testing FlattenLayer....
Testing BCEWithLogitsLoss...
Testing CrossEntropyLoss.....
Testing HuberLoss.....
Testing MeanAbsoluteErrorLoss...       
Testing MeanSquaredErrorLoss...        
Testing JITHuberLoss.....     
Testing JITBCEWithLogitsLoss...
Testing JITCrossEntropyLoss.....
Testing Comparing JIT and non-JIT loss implementations.....
Testing JITMeanAbsoluteErrorLoss...
Testing JITMeanSquaredErrorLoss...
Testing NeuralNetwork class with Numba backend.........................
Testing AdadeltaOptimizer.....
Testing AdamOptimizer.....    
Testing SGDOptimizer.....     
Testing JITAdadeltaOptimizer.....
Testing JITAdamOptimizer.....
Testing JITSGDOptimizer..... 
Testing General Pipeline................  
Testing ForecastingPipeline.................................
Testing GeneralizedSVC...........
Testing GeneralizedSVR........
Testing LinearSVC...........
Testing LinearSVR........
Testing OneClassSVM......
Testing ARIMA.....................
Testing SARIMA............
Testing SARIMAX..........
Testing AdditiveDecomposition..........      
Testing _centered_moving_average.............
Testing MultiplicativeDecomposition.............
Testing DoubleExponentialSmoothing.........     
Testing SimpleExponentialSmoothing...........   
Testing TripleExponentialSmoothing...........   
Testing ExponentialMovingAverage......
Testing SimpleMovingAverage......     
Testing WeightedMovingAverage.......  
Testing AdaBoostClassifier..................
Testing AdaBoostRegressor................
Testing Gradient Boosted Classifier..........................
Testing Classifier Tree.................
Testing Classifier Tree Utility...................................
Testing Random Forest Classifier..................
Testing Isolation Forest.....
Testing Isolation Tree....        
Testing Isolation Tree Utility.   
Testing Gradient Boosted Regressor................
Testing Random Forest Regressor...............
Testing Regressor Tree................ 
Testing Regressor Tree Utility.......................................
Testing Data Augmentation......................
Testing Decomposition.....
Testing Data Prep...............
Testing Forcast Regressor....   
Testing GridSearchCV.......................
Testing Metrics...............
Testing Model Selection Utils..........
Testing Polynomial Transform....       
Testing RandomSearchCV.........................
Testing Voting Classifier.......
Testing Voting Regressor....    
Testing Animation Integration....
Testing ClassificationAnimation Class.........
Testing ForcastingAnimation Class.......
Testing RegressionAnimation Class.........
Testing Categorical Preprocessing Functions.........      
Testing Encoder...........................................
Testing Scaler..........
Testing train_test_split function..........
Testing CustomImputer.........
Testing DirectionalImputer..........
Testing InterpolationImputer..........
Testing KNNImputer..........
Testing StatisticalImputer...........
Testing makeData Utilities...................................
Testing example file: classifier.py.
Testing example file: regressor.py.
Testing example file: dbscan.py.
Testing example file: dbscan_3d.py.
Testing example file: dbscan_3d_aimated.py.
Testing example file: kmeans.py.
Testing example file: bayes.py.
Testing example file: lasso.py.
Testing example file: lda.py.
Testing example file: lda_comparison.py.
Testing example file: lda_vs_qda_comparison.py.
Testing example file: logisticRegression.py.
Testing example file: ols.py.
Testing example file: passiveAggressive.py.
Testing example file: passiveAggressive_vis.py.
Testing example file: perceptron.py.
Testing example file: qda.py.
Testing example file: ransac.py.
Testing example file: ransac_vis.py.
Testing example file: ridge.py.
Testing example file: nearestNeighborsClassifier.py.
Testing example file: nearestNeighborsRegressor.py.
Testing example file: neuralNetwork_cancer.py.
Testing example file: neuralNetwork_classifier.py.
Testing example file: neuralNetwork_classifier_hyper.py.
Testing example file: neuralNetwork_diabetes.py.
Testing example file: neuralNetwork_hyper.py.
Testing example file: neuralNetwork_iris.py.
Testing example file: neuralNetwork_layers.py...
Testing example file: neuralNetwork_layers_numba.py..
Testing example file: neuralNetwork_regressor.py.
Testing example file: pipeline_classification.py.
Testing example file: pipeline_classification_tuning.py.
Testing example file: pipeline_forecasting.py.
Testing example file: pipeline_regression.py.
Testing example file: pipeline_regression_tuning.py.
Testing example file: generalizedSVC_binary.py.
Testing example file: generalizedSVC_multi.py.
Testing example file: generalizedSVR.py.
Testing example file: linearSVC_binary.py.
Testing example file: linearSVC_multi.py.
Testing example file: linearSVR.py.
Testing example file: oneClassSVM.py.
Testing example file: arima_arima.py.
Testing example file: arima_sarima.py.
Testing example file: arima_sarimax.py.
Testing example file: decom_additiveDecomposition.py.
Testing example file: decom_multiplicativeDecomposition.py.
Testing example file: mvg_exponentialMovingAverage.py.
Testing example file: mvg_exponentialMovingAverage_anim.py.
Testing example file: mvg_simpleMovingAverage.py.
Testing example file: mvg_simpleMovingAverage_anim.py.
Testing example file: mvg_weightedMovingAverage.py.
Testing example file: mvg_weightedMovingAverage_anim.py.
Testing example file: smth_doubleExponentialSmoothing.py.
Testing example file: smth_simpleExponentialSmoothing.py.
Testing example file: smth_tripleExponentialSmoothing.py.
Testing example file: adaBoostClassifier.py.
Testing example file: adaBoostRegressor.py.
Testing example file: gradientBoostedClassifier.py.
Testing example file: gradientBoostedRegressor.py.
Testing example file: isolationForest_blob.py.
Testing example file: isolationForest_boundary.py.
Testing example file: isolationForest_reg.py.
Testing example file: randomForestClassifier.py.
Testing example file: randomForestRegressor.py.
Testing example file: treeClassifier.py.
Testing example file: treeRegressor.py.
Testing example file: animator_exponentialMovingAverage.py.
Testing example file: animator_logisticRegression.py.
Testing example file: animator_perceptron.py.
Testing example file: animator_ridge.py.
Testing example file: animator_weightedMovingAverage.py.
Testing example file: dataAugmentation_combined.py.
Testing example file: dataAugmentation_randOver.py.
Testing example file: dataAugmentation_randUnder.py.
Testing example file: dataAugmentation_smote.py.
Testing example file: dataPreprocessing.py.
Testing example file: encoder_binarizer.py.
Testing example file: encoder_label.py.
Testing example file: gridSearchCV_bayes.py.
Testing example file: gridSearchCV_gbr.py.
Testing example file: gridSearchCV_passiveAggReg.py.
Testing example file: gridSearchCV_rfc.py.
Testing example file: gridSearchCV_rfr.py.
Testing example file: imputer_KNN.py.
Testing example file: imputer_custom.py.
Testing example file: imputer_directional.py.
Testing example file: imputer_interpolation.py.
Testing example file: imputer_statistical.py.
Testing example file: makeData.py.
Testing example file: pca_classification.py.
Testing example file: pca_regression.py.
Testing example file: polynomialTransform.py.
Testing example file: randomSearchCV_bayes.py.
Testing example file: randomSearchCV_gbr.py.
Testing example file: randomSearchCV_passiveAggReg.py.
Testing example file: randomSearchCV_rfc.py.
Testing example file: randomSearchCV_rfr.py.
Testing example file: segaSearchCV_rfr.py.
Testing example file: svd_classification.py.
Testing example file: svd_regression.py.
Testing example file: votingClassifier.py.
Testing example file: votingRegressor.py.
----------------------------------------------------------------------
Ran 1455 tests in 558.587s

OK
```

## Installation

To set up the project environment, you can use the provided `environment.yml` file to create a conda environment with all the necessary dependencies.

1. Open a terminal or command prompt.
2. Navigate to the directory where your repository is located.
3. Run the following command to create the conda environment: `conda env create -f environment.yml`
4. Activate the newly created environment: `conda activate sega_learn`
