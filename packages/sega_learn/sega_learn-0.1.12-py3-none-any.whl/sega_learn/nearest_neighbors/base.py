from abc import ABC, abstractmethod

import numpy as np

from sega_learn.utils import DataPrep


# ABC is a module that provides tools for defining abstract base classes in Python.
# Used here to define a base class for KNN algorithms.
# This allows us to create a common interface for KNN classifiers and regressors.
class KNeighborsBase(ABC):
    """Abstract base class for implementing k-nearest neighbors (KNN) algorithms.

    Provides common functionality for fitting data, computing distances, and managing configurations.

    Attributes:
        n_neighbors (int): Number of neighbors to use for the KNN algorithm.
        distance_metric (str): Distance metric for calculating distances ('euclidean', 'manhattan', 'minkowski').
        one_hot_encode (bool): Whether to apply one-hot encoding to categorical columns.
        fp_precision (type): Floating point precision for calculations.
        numba (bool): Whether to use numba for performance optimization.
        X_train (np.ndarray): Training feature data.
        y_train (np.ndarray): Training target data.

    Methods:
        __init__(n_neighbors=5, distance_metric="euclidean", one_hot_encode=False,
                 fp_precision=np.float64, numba=False):
            Initializes the KNeighborsBase class with specified parameters.
        fit(X, y):
            Fits the model using the training data and target values.
        get_distance_indices(X):
            Computes distances and returns indices of the nearest points in the training data.
        _data_precision(X, y=None):
            Sets the floating point precision for the input data.
        _check_data(X, y):
            Validates input data to ensure it is numeric and consistent.
        _one_hot_encode(X):
            Applies one-hot encoding to categorical columns in the input data.
        _compute_distances(X):
            Computes distances between input data and training data using the specified distance metric.
        _compute_distances_euclidean(X):
            Computes distances using the Euclidean distance formula.
        _compute_distances_manhattan(X):
            Computes distances using the Manhattan distance formula.
        _compute_distances_minkowski(X, p=3):
            Computes distances using the Minkowski distance formula with specified order `p`.
        predict(X):
            Abstract method to be implemented by subclasses for making predictions based on input data.
    """

    def __init__(
        self,
        n_neighbors=5,
        distance_metric="euclidean",
        one_hot_encode=False,
        fp_precision=np.float64,
        numba=False,
    ):
        """Initialize the KNeighborsBase class.

        Args:
            n_neighbors: int, default=5. The number of neighbors to use for the KNN algorithm.
            distance_metric: str, default='euclidean'. The distance metric to use for calculating distances.
            one_hot_encode: bool, default=False. Whether to apply one-hot encoding to the categorical columns.
            fp_precision: data type, default=np.float64. The floating point precision to use for the calculations.
            numba: bool, default=True. Whether to use numba for speeding up the calculations.
        """
        if numba:
            try:
                from ._nearest_neighbors_jit_utils import (
                    _jit_compute_distances_euclidean,
                    _jit_compute_distances_manhattan,
                    _jit_compute_distances_minkowski,
                    _numba_predict_classifier,
                    _numba_predict_regressor,
                )

                # Precompile the numba functions
                _jit_compute_distances_euclidean(
                    np.array([[0.0, 0.0]]), np.array([[0.0, 0.0]])
                )
                _jit_compute_distances_manhattan(
                    np.array([[0.0, 0.0]]), np.array([[0.0, 0.0]])
                )
                _jit_compute_distances_minkowski(
                    np.array([[0.0, 0.0]]), np.array([[0.0, 0.0]]), p=3
                )

                _numba_predict_regressor(
                    np.array([[0.0, 0.0]]), np.array([0.0, 0.0]), 1
                )
                _numba_predict_classifier(
                    np.array([[0.0, 0.0]]), np.array([0.0, 0.0]), 1
                )

                self.numba = True
            except ImportError:
                self.numba = False
                raise ImportError(
                    "Numba is not installed. Please install numba to use the numba optimized version of the KNN algorithm."
                ) from None
            except Exception as e:
                self.numba = False
                print(f"Error compiling numba functions: {e}")
        else:
            self.numba = False

        if n_neighbors <= 0:
            raise ValueError("n_neighbors must be a positive integer.")
        if one_hot_encode and not isinstance(one_hot_encode, bool):
            raise ValueError("one_hot_encode must be a boolean value.")
        if not isinstance(fp_precision, type) or not np.issubdtype(
            fp_precision, np.floating
        ):
            raise ValueError("fp_precision must be a floating point data type.")

        self.n_neighbors = n_neighbors
        self.distance_metric = distance_metric
        self.one_hot_encode = one_hot_encode
        self.fp_precision = fp_precision

        # Initialize training data and labels to None
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        """Fit the model using the training data.

        Args:
            X: array-like, shape (n_samples, n_features) - The training data.
            y: array-like, shape (n_samples,) - The target values.
        """
        # Apply one-hot encoding if specified
        if self.one_hot_encode:
            X = self._one_hot_encode(X)

        # Set the floating point precision for the input data
        X, y = self._data_precision(X, y)

        # Check if the input data is valid
        self._check_data(X, y)

        # Store the training data and labels
        self.X_train = X
        self.y_train = y

    def get_distance_indices(self, X):
        """Compute the distances and return the indices of the nearest points im the training data.

        Args:
            X: array-like, shape (n_samples, n_features) - The input data.

        Returns:
            indices: array, shape (n_samples, n_neighbors) - The indices of the nearest neighbors.
        """
        # Apply one-hot encoding if specified
        if self.one_hot_encode:
            X = self._one_hot_encode(X)

        # Set the floating point precision for the input data
        X, _ = self._data_precision(X)

        # Compute the distances between all training samples and the input data
        distances = self._compute_distances(X)

        # Find the indices of the k nearest neighbors
        indices = np.argsort(distances, axis=1)[:, 1:]
        return indices

    def _data_precision(self, X, y=None):
        """Set the floating point precision for the input data.

        Args:
            X: array-like, shape (n_samples, n_features) - The training data.
            y: array-like, shape (n_samples,) - The target values.
        """
        # Convert the input data to the specified floating point precision
        X = np.array(X, dtype=self.fp_precision)
        if y is not None:
            y = np.array(y, dtype=self.fp_precision)
        return X, y

    def _check_data(self, X, y):
        """Check if the input data is valid.

        Args:
            X: array-like, shape (n_samples, n_features) - The input data.
            y: array-like, shape (n_samples,) - The target values.
        """
        # Ensure that all data is in NumPy array format
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)

        # Ensure that all data is numeric
        if not np.issubdtype(X.dtype, np.number):
            raise ValueError("All features in X must be numeric.")

        # Check if the number of samples in X and y match
        if X.shape[0] != y.shape[0]:
            raise ValueError("The number of samples in X and y must match.")

        # Check if the number of neighbors is valid
        if self.n_neighbors <= 0 or self.n_neighbors > X.shape[0]:
            raise ValueError(
                "n_neighbors must be a positive integer less than or equal to the number of samples in X."
            )

    def _one_hot_encode(self, X):
        """Apply one-hot encoding to the categorical columns in the DataFrame."""
        # Find the categorical columns in the DataFrame
        categorical_cols = DataPrep.find_categorical_columns(X)
        # Apply one-hot encoding to the categorical columns
        X = DataPrep.one_hot_encode(X, categorical_cols)
        return X

    def _compute_distances(self, X):
        """Helper method to call the appropriate distance computation method."""
        # Check if the distance metric is valid
        if self.distance_metric not in ["euclidean", "manhattan", "minkowski"]:
            raise ValueError(f"Unsupported distance metric: {self.distance_metric}")

        if self.numba:
            from ._nearest_neighbors_jit_utils import (
                _jit_compute_distances_euclidean,
                _jit_compute_distances_manhattan,
                _jit_compute_distances_minkowski,
            )

            if self.distance_metric == "euclidean":
                return _jit_compute_distances_euclidean(X, self.X_train)
            elif self.distance_metric == "manhattan":
                return _jit_compute_distances_manhattan(X, self.X_train)
            elif self.distance_metric == "minkowski":
                return _jit_compute_distances_minkowski(X, self.X_train, p=3)

        else:
            if self.distance_metric == "euclidean":
                return self._compute_distances_euclidean(X)
            elif self.distance_metric == "manhattan":
                return self._compute_distances_manhattan(X)
            elif self.distance_metric == "minkowski":
                return self._compute_distances_minkowski(X)

    def _compute_distances_euclidean(self, X):
        """Compute the distances between the training data and the input data.

        This method uses the Euclidean distance formula.
        Formula: d(x, y) = sqrt(sum((x_i - y_i)^2))
        """
        X = np.array(X)
        distances = np.sqrt(((self.X_train - X[:, np.newaxis]) ** 2).sum(axis=2))
        return distances

    def _compute_distances_manhattan(self, X):
        """Compute the distances between the training data and the input data.

        This method uses the Manhattan distance formula.
        Formula: d(x, y) = sum(|x_i - y_i|)
        """
        X = np.array(X)
        distances = np.abs(self.X_train - X[:, np.newaxis]).sum(axis=2)
        return distances

    def _compute_distances_minkowski(self, X, p=3):
        """Compute the distances between the training data and the input data.

        This method uses the Minkowski distance formula.
        Formula: d(x, y) = (sum(|x_i - y_i|^p))^(1/p)
        where p is the order of the norm.
        """
        X = np.array(X)
        distances = np.power(np.abs(self.X_train - X[:, np.newaxis]), p).sum(axis=2)
        return np.power(distances, 1 / p)

    @abstractmethod
    def predict(self, X):
        """The @abstractmethod decorator indicates that this method must be implemented by any subclass of KNNBase."""
        pass
