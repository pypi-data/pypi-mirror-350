import numpy as np

from .base import KNeighborsBase


class KNeighborsClassifier(KNeighborsBase):
    """K-Nearest Neighbors classifier.

    This class implements the k-nearest neighbors algorithm for classification.
    """

    def predict(self, X):
        """Predict the class labels for the provided data.

        Args:
            X: array-like, shape (n_samples, n_features) - The input data for which to predict the class labels.

        Returns:
            predictions: array, shape (n_samples,) - The predicted class labels for the input data.
        """
        # Apply one-hot encoding if specified
        if self.one_hot_encode:
            X = self._one_hot_encode(X)

        # Check if the model has been fitted
        if self.X_train is None or self.y_train is None:
            raise ValueError(
                "The model has not been fitted yet. Please call the fit method before predict."
            )

        # Set the floating point precision for the input data
        X, _ = self._data_precision(X)

        # Compute the distances between all training samples and the input data
        distances = self._compute_distances(X)

        if self.numba:
            from ._nearest_neighbors_jit_utils import _numba_predict_classifier

            predictions = _numba_predict_classifier(
                distances, self.y_train, self.n_neighbors
            )
        else:
            # Find the indices of the k nearest neighbors, sort them, and select the top k
            nearest_neighbors = np.argsort(distances, axis=1)[:, : self.n_neighbors]
            top_k_y = self.y_train[nearest_neighbors]

            # For each sample, find the most common class label among the k nearest neighbors
            predictions = np.array(
                [np.bincount(labels.astype(int)).argmax() for labels in top_k_y]
            )

        return predictions
