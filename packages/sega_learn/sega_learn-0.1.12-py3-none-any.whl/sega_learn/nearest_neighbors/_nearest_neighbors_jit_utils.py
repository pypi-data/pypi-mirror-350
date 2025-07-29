import numpy as np
from numba import njit, prange

# The following lines are used to compile the numba functions into shared library
# from numba.pycc import CC
# cc = CC('compiled_dbscan_jit_utils')
# cc.verbose = True


@njit(parallel=True, fastmath=True)
def _jit_compute_distances_euclidean(X, X_train):
    n_samples, n_features = X.shape
    n_train_samples = X_train.shape[0]
    distances = np.empty((n_samples, n_train_samples), dtype=np.float64)
    for i in prange(n_samples):
        for j in range(n_train_samples):
            diff = X[i] - X_train[j]
            distances[i, j] = np.sqrt(np.sum(diff**2))
    return distances


@njit(parallel=True, fastmath=True)
def _jit_compute_distances_manhattan(X, X_train):
    n_samples, n_features = X.shape
    n_train_samples = X_train.shape[0]
    distances = np.empty((n_samples, n_train_samples), dtype=np.float64)
    for i in prange(n_samples):
        for j in range(n_train_samples):
            diff = X[i] - X_train[j]
            distances[i, j] = np.sum(np.abs(diff))
    return distances


@njit(parallel=True, fastmath=True)
def _jit_compute_distances_minkowski(X, X_train, p):
    n_samples, n_features = X.shape
    n_train_samples = X_train.shape[0]
    distances = np.empty((n_samples, n_train_samples), dtype=np.float64)
    for i in prange(n_samples):
        for j in range(n_train_samples):
            diff = X[i] - X_train[j]
            distances[i, j] = np.power(np.sum(np.abs(diff) ** p), 1 / p)
    return distances


@njit(parallel=True, fastmath=True)
def _numba_predict_regressor(distances, y_train, n_neighbors):
    """Numba-optimized helper function for KNN regression predictions.

    Args:
        distances (np.ndarray): 2D array of shape (n_samples, n_train_samples), precomputed distances.
        y_train (np.ndarray): 1D array of shape (n_train_samples,), training labels.
        n_neighbors (int): Number of nearest neighbors to consider.

    Returns:
        np.ndarray: 1D array of shape (n_samples,), predicted values.
    """
    n_samples = distances.shape[0]
    predictions = np.empty(n_samples, dtype=np.float64)

    for i in prange(n_samples):
        # Get the indices of the k nearest neighbors
        nearest_indices = np.argsort(distances[i])[:n_neighbors]
        # Compute the mean of the k nearest neighbors
        predictions[i] = np.mean(y_train[nearest_indices])

    return predictions


@njit(parallel=True, fastmath=True)
def _numba_predict_classifier(distances, y_train, n_neighbors):
    """Numba-optimized helper function for KNN classification predictions.

    Args:
        distances (np.ndarray): 2D array of shape (n_samples, n_train_samples), precomputed distances.
        y_train (np.ndarray): 1D array of shape (n_train_samples,), training labels.
        n_neighbors (int): Number of nearest neighbors to consider.

    Returns:
        predictions (np.ndarray): 1D array of shape (n_samples,), predicted class labels.
    """
    n_samples = distances.shape[0]
    predictions = np.empty(n_samples, dtype=np.int32)

    for i in prange(n_samples):
        # Get the indices of the k nearest neighbors
        nearest_indices = np.argsort(distances[i])[:n_neighbors]
        # Get the labels of the k nearest neighbors
        nearest_labels = y_train[nearest_indices].astype(np.int32)  # Cast to integer
        # Find the most common label (mode) among the k nearest neighbors
        label_counts = np.bincount(nearest_labels)
        predictions[i] = np.argmax(label_counts)

    return predictions


# if __name__ == "__main__":
#     cc.compile()
