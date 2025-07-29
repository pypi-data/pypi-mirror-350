import numpy as np


class PCA:
    """Principal Component Analysis (PCA) implementation."""

    def __init__(self, n_components):
        """Initializes the PCA model.

        Args:
            n_components: (int) - Number of principal components to keep.
        """
        self.n_components = n_components
        self.components = None
        self.mean_ = None

    def fit(self, X):
        """Fits the PCA model to the data.

        Args:
            X: (np.ndarray) - Input data of shape (n_samples, n_features).

        Raises:
            ValueError: If input data is not a 2D numpy array or if n_components exceeds the number of features.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError("Input data must be a numpy array.")
        if X.ndim != 2:
            raise ValueError("Input data must be a 2D array.")
        if self.n_components > X.shape[1]:
            raise ValueError(
                "Number of components cannot be greater than the number of features."
            )

        # Mean centering
        self.mean_ = np.mean(X, axis=0)
        X = X - self.mean_

        # Covariance matrix
        cov = np.cov(X.T)

        # Eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(cov)

        # Sort eigenvectors by eigenvalues in descending order
        eigenvectors = eigenvectors[:, np.argsort(eigenvalues)[::-1]]

        # Select the top n_components eigenvectors
        self.components_ = eigenvectors[:, : self.n_components]
        self.explained_variance_ratio_ = eigenvalues[: self.n_components] / np.sum(
            eigenvalues
        )

    def transform(self, X):
        """Applies dimensionality reduction on the input data.

        Args:
            X: (np.ndarray) - Input data of shape (n_samples, n_features).

        Returns:
            X_transformed: (np.ndarray) - Data transformed into the principal component space of shape (n_samples, n_components).

        Raises:
            ValueError: If input data is not a 2D numpy array or if its dimensions do not match the fitted data.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError("Input data must be a numpy array.")
        if X.ndim != 2:
            raise ValueError("Input data must be a 2D array.")
        if X.shape[1] != self.mean_.shape[0]:
            raise ValueError(
                "Input data must have the same number of features as the data used to fit the model."
            )

        # Project data to the principal component space
        X = X - self.mean_
        return np.dot(X, self.components_)

    def fit_transform(self, X):
        """Fits the PCA model and applies dimensionality reduction on the input data.

        Args:
            X: (np.ndarray) - Input data of shape (n_samples, n_features).

        Returns:
            X_transformed: (np.ndarray) - Data transformed into the principal component space of shape (n_samples, n_components).
        """
        self.fit(X)
        return self.transform(X)

    def get_explained_variance_ratio(self):
        """Retrieves the explained variance ratio.

        Returns:
            explained_variance_ratio_: (np.ndarray) - Array of explained variance ratios for each principal component.
        """
        return self.explained_variance_ratio_

    def get_components(self):
        """Retrieves the principal components.

        Returns:
            components_: (np.ndarray) - Array of principal components of shape (n_features, n_components).
        """
        return self.components_

    def inverse_transform(self, X_reduced):
        """Reconstructs the original data from the reduced data.

        Args:
            X_reduced: (np.ndarray) - Reduced data of shape (n_samples, n_components).

        Returns:
            X_original: (np.ndarray) - Reconstructed data of shape (n_samples, n_features).

        Raises:
            ValueError: If input data is not a 2D numpy array.
        """
        if not isinstance(X_reduced, np.ndarray):
            raise ValueError("Input data must be a numpy array.")
        if X_reduced.ndim != 2:
            raise ValueError("Input data must be a 2D array.")
        return np.dot(X_reduced, self.components_.T) + self.mean_


class SVD:
    """Singular Value Decomposition (SVD) implementation."""

    def __init__(self, n_components):
        """Initializes the SVD model.

        Args:
            n_components: (int) - Number of singular values and vectors to keep.
        """
        self.n_components = n_components
        self.U = None
        self.S = None
        self.Vt = None

    def fit(self, X):
        """Fits the SVD model to the data.

        Args:
            X: (np.ndarray) - Input data of shape (n_samples, n_features).

        Raises:
            ValueError: If input data is not a 2D numpy array or if n_components exceeds the minimum dimension of the input data.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError("Input data must be a numpy array.")
        if X.ndim != 2:
            raise ValueError("Input data must be a 2D array.")
        if self.n_components > min(X.shape):
            raise ValueError(
                "Number of components cannot be greater than the minimum dimension of the input data."
            )

        U, S, Vt = np.linalg.svd(X, full_matrices=False)
        self.U = U[:, : self.n_components]
        self.S = S[: self.n_components]
        self.Vt = Vt[: self.n_components, :]

    def transform(self, X):
        """Applies the SVD transformation on the input data.

        Args:
            X: (np.ndarray) - Input data of shape (n_samples, n_features).

        Returns:
            X_transformed: (np.ndarray) - Data transformed into the singular value space of shape (n_samples, n_components).

        Raises:
            ValueError: If input data is not a 2D numpy array.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError("Input data must be a numpy array.")
        if X.ndim != 2:
            raise ValueError("Input data must be a 2D array.")

        return np.dot(X, self.Vt.T)

    def fit_transform(self, X):
        """Fits the SVD model and applies the transformation on the input data.

        Args:
            X: (np.ndarray) - Input data of shape (n_samples, n_features).

        Returns:
            X_transformed: (np.ndarray) - Data transformed into the singular value space of shape (n_samples, n_components).
        """
        self.fit(X)
        return self.transform(X)

    def get_singular_values(self):
        """Retrieves the singular values.

        Returns:
            S: (np.ndarray) - Array of singular values of shape (n_components,).
        """
        return self.S

    def get_singular_vectors(self):
        """Retrieves the singular vectors.

        Returns:
            U: (np.ndarray) - Left singular vectors of shape (n_samples, n_components).
            Vt: (np.ndarray) - Right singular vectors of shape (n_components, n_features).
        """
        return self.U, self.Vt
