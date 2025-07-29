import numpy as np
import pandas as pd

from sega_learn.utils import DataPrep


class KMeans:
    """This class implements the K-Means clustering algorithm along with methods for evaluating the optimal number of clusters and visualizing the clustering results.

    Args:
        X: The data matrix (numpy array).
        n_clusters: The number of clusters.
        max_iter: The maximum number of iterations.
        tol: The tolerance to declare convergence.

    Methods:
        - __init__: Initializes the KMeans object with parameters such as the data matrix, number of clusters, maximum iterations, and convergence tolerance.
        - _handle_categorical: Handles categorical columns in the input data by one-hot encoding.
        - _convert_to_ndarray: Converts input data to a NumPy ndarray and handles categorical columns.
        - initialize_centroids: Randomly initializes the centroids for KMeans clustering.
        - assign_clusters: Assigns clusters based on the nearest centroid.
        - update_centroids: Updates centroids based on the current cluster assignments.
        - fit: Fits the KMeans model to the data by iteratively updating centroids and cluster assignments until convergence.
        - predict: Predicts the closest cluster each sample in new_X belongs to.
        - elbow_method: Implements the elbow method to determine the optimal number of clusters.
        - calinski_harabasz_index: Calculates the Calinski-Harabasz Index for evaluating clustering performance.
        - davies_bouldin_index: Calculates the Davies-Bouldin Index for evaluating clustering performance.
        - silhouette_score: Calculates the Silhouette Score for evaluating clustering performance.
        - find_optimal_clusters: Implements methods to find the optimal number of clusters using the elbow method,
                             Calinski-Harabasz Index, Davies-Bouldin Index, and Silhouette Score. It also plots the evaluation
                             metrics to aid in determining the optimal k value.
    """

    def __init__(self, X, n_clusters=3, max_iter=300, tol=1e-4):
        """Initialize the KMeans object.

        Args:
            X: The data matrix (numpy array, pandas DataFrame, or list).
            n_clusters: The number of clusters.
            max_iter: The maximum number of iterations.
            tol: The tolerance to declare convergence.
        """
        # Validate input parameters
        if not isinstance(n_clusters, int) or n_clusters < 1:
            raise ValueError("n_clusters must be a positive integer.")
        if n_clusters > X.shape[0]:
            raise ValueError(
                "n_clusters must be less than or equal to the number of samples."
            )
        if not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("max_iter must be a positive integer.")
        if not isinstance(tol, (int, float)) or tol <= 0:
            raise ValueError("tol must be a positive number.")

        self.X = self._convert_to_ndarray(X).astype(
            float
        )  # Convert input data to ndarray
        self.n_clusters = n_clusters  # Number of clusters
        self.max_iter = max_iter  # Maximum number of iterations
        self.tol = tol  # Tolerance for convergence
        self.centroids = None  # Centroids of the clusters
        self.labels = None  # Cluster assignments for each data point

    def _handle_categorical(self, X):
        """Handle categorical columns by one-hot encoding.

        Args:
            X: The input data with potential categorical columns.

        Returns:
            X_processed: The processed data with categorical columns encoded.
        """
        categorical_cols = DataPrep.find_categorical_columns(X)
        X_processed = DataPrep.one_hot_encode(
            X, categorical_cols
        )  # One-hot encode categorical columns

        return X_processed

    def _convert_to_ndarray(self, X):
        """Convert input data to a NumPy ndarray and handle categorical columns.

        Args:
            X: The input data, which can be a list, DataFrame, or ndarray.

        Returns:
            X_ndarray: The converted and processed input data as a NumPy ndarray.
        """
        import pandas as pd

        if isinstance(X, np.ndarray):  # Check if input is already a NumPy array
            X_ndarray = X.copy()  # Create a copy of the array

        elif isinstance(X, list):  # Check if input is a list
            X_ndarray = np.array(X)  # Convert list to NumPy array

        elif isinstance(X, pd.DataFrame):  # Check if input is a DataFrame
            X_ndarray = X.values  # Convert DataFrame to NumPy array

        else:  # Raise error for unsupported input type
            raise ValueError(
                "Unsupported input type. Input must be a list, NumPy array, or DataFrame."
            )

        X_processed = self._handle_categorical(X_ndarray)  # Handle categorical columns

        return X_processed

    def initialize_centroids(self):
        """Randomly initialize the centroids.

        Returns:
            centroids: The initialized centroids.
        """
        # np.random.seed(1)                                           # Set random seed for reproducibility
        random_indices = np.random.permutation(
            self.X.shape[0]
        )  # Randomly shuffle indices
        centroids = self.X[
            random_indices[: self.n_clusters]
        ]  # Select the first n_clusters points as centroids
        return centroids

    def assign_clusters(self, centroids):
        """Assign clusters based on the nearest centroid.

        Args:
            centroids: The current centroids.

        Returns:
            labels: The cluster assignments for each data point.
        """
        self.X = self.X.astype(float)  # Convert X to float type if necessary
        centroids = centroids.astype(float)  # Ensure centroids are float type

        distances = np.sqrt(
            ((self.X - centroids[:, np.newaxis]) ** 2).sum(axis=2)
        )  # Calculate pairwise distances
        labels = np.argmin(distances, axis=0)  # Assign labels based on minimum distance

        return labels

    def update_centroids(self):
        """Update the centroids based on the current cluster assignments.

        Returns:
            centroids: The updated centroids.
        """
        centroids = np.array(
            [  # Calculate new centroids
                self.X[self.labels == i].mean(axis=0)
                if np.sum(self.labels == i) > 0  # Mean of points in cluster i
                else self.X[
                    np.random.choice(len(self.X))
                ]  # Random point if no points in cluster
                for i in range(self.n_clusters)  # For each cluster
            ]
        )

        return centroids

    def fit(self):
        """Fit the KMeans model to the data."""
        self.centroids = self.initialize_centroids()  # Initialize centroids

        for _ in range(self.max_iter):  # Iterate until convergence or max_iter
            prev_centroids = np.copy(self.centroids)  # Store previous centroids
            self.labels = self.assign_clusters(self.centroids)  # Assign clusters
            self.centroids = self.update_centroids()  # Update centroids

            if np.all(
                np.abs(prev_centroids - self.centroids) < self.tol
            ):  # Check for convergence
                break

    def predict(self, new_X):
        """Predict the closest cluster each sample in new_X belongs to.

        Args:
            new_X: The data matrix to predict (numpy array).

        Returns:
            labels: The predicted cluster labels.
        """
        # Validate input data
        if not isinstance(
            new_X, (np.ndarray, list, pd.DataFrame)
        ):  # Check if input is a valid type
            raise ValueError(
                "Unsupported input type. Input must be a list, NumPy array, or DataFrame."
            )
        if new_X.shape[1] != self.X.shape[1]:  # Check if number of features match
            raise ValueError(
                f"Number of features in new_X ({new_X.shape[1]}) does not match the model ({self.X.shape[1]})."
            )
        if self.labels is None:  # Check if model has been fitted
            raise ValueError("Fit the model before predicting.")

        new_X = self._convert_to_ndarray(new_X).astype(
            float
        )  # Convert input data to ndarray

        distances = np.sqrt(
            ((new_X - self.centroids[:, np.newaxis]) ** 2).sum(axis=2)
        )  # Calculate pairwise distances
        labels = np.argmin(distances, axis=0)  # Assign labels based on minimum distance

        return labels

    def elbow_method(self, max_k=10):
        """Implement the elbow method to determine the optimal number of clusters.

        Args:
            max_k: The maximum number of clusters to test.

        Returns:
            distortions: A list of distortions for each k.
        """
        distortions = []
        for k in range(1, max_k + 1):  # Iterate over each k value
            kmeans = KMeans(self.X, n_clusters=k)  # Initialize KMeans with k clusters
            kmeans.fit()  # Fit the KMeans model

            distortion = (
                sum(
                    np.min(
                        np.sqrt(
                            ((self.X - kmeans.centroids[:, np.newaxis]) ** 2).sum(
                                axis=2
                            )
                        ),
                        axis=0,
                    )
                )
                / self.X.shape[0]
            )  # Calculate distortion
            distortions.append(distortion)  # Append distortion to list

        return distortions

    def calinski_harabasz_index(self, X, labels, centroids):
        """Calculate the Calinski-Harabasz Index for evaluating clustering performance.

        Args:
            X: The data matrix (numpy array).
            labels: The cluster labels for each data point.
            centroids: The centroids of the clusters.

        Returns:
            ch_index: The computed Calinski-Harabasz Index.
        """
        clusters = np.unique(labels)  # Unique cluster labels
        n_clusters = len(clusters)  # Number of clusters
        N = len(X)  # Total number of data points

        if n_clusters <= 1:  # Check if there is only one cluster
            return 0

        mean_total = np.mean(X, axis=0)  # Mean of all data points

        Bk = np.sum(
            [
                len(labels[labels == c])
                * np.linalg.norm(centroids[c] - mean_total) ** 2
                for c in clusters
            ]
        )  # Compute the between-cluster dispersion (B(K))
        Wk = np.sum(
            [
                np.sum(np.linalg.norm(X[labels == c] - centroids[c], axis=1) ** 2)
                for c in clusters
            ]
        )  # Compute the within-cluster dispersion (W(K))

        ch_index = (Bk / Wk) * (
            (N - n_clusters) / (n_clusters - 1)
        )  # Compute the Calinski-Harabasz Index

        return ch_index

    def davies_bouldin_index(self, X, labels, centroids):
        """Calculate the Davies-Bouldin Index for evaluating clustering performance.

        Args:
            X: The data matrix (numpy array).
            labels: The cluster labels for each data point.
            centroids: The centroids of the clusters.

        Returns:
            db_index: The computed Davies-Bouldin Index.
        """
        clusters = np.unique(labels)  # Unique cluster labels
        n_clusters = len(clusters)  # Number of clusters
        cluster_distances = np.zeros(
            (n_clusters, n_clusters)
        )  # Pairwise distances between centroids

        for i in range(n_clusters):  # For each cluster
            for j in range(i + 1, n_clusters):  # For each other cluster
                cluster_distances[i, j] = np.linalg.norm(
                    centroids[i] - centroids[j]
                )  # Calculate distance between centroids
                cluster_distances[j, i] = cluster_distances[i, j]  # Symmetric matrix

        db_indices = []
        for i in range(n_clusters):  # For each cluster
            indices_same_cluster = np.where(labels == clusters[i])[
                0
            ]  # Indices of points in the same cluster
            avg_distance_same = np.mean(
                np.linalg.norm(X[indices_same_cluster] - centroids[i], axis=1)
            )  # Average distance within cluster

            similarity_scores = []
            for j in range(n_clusters):  # For each other cluster
                if j != i:  # Skip the same cluster
                    indices_other_cluster = np.where(labels == clusters[j])[
                        0
                    ]  # Indices of points in the other cluster
                    avg_distance_other = np.mean(
                        np.linalg.norm(X[indices_other_cluster] - centroids[j], axis=1)
                    )  # Average distance to other cluster
                    avg_distance_centroids = cluster_distances[
                        i, j
                    ]  # Average distance between centroids
                    if avg_distance_centroids != 0:  # Handle division by zero
                        similarity = (
                            avg_distance_same + avg_distance_other
                        ) / avg_distance_centroids  # Calculate similarity score
                        similarity_scores.append(similarity)  # Append similarity score

            if similarity_scores:  # Check if the list is not empty
                db_index = np.max(
                    similarity_scores
                )  # Davies-Bouldin Index for the cluster
                db_indices.append(db_index)  # Append DB Index for the cluster

        if db_indices:  # Check if the list is not empty
            return np.mean(db_indices)  # Return the mean Davies-Bouldin Index
        else:
            return 0  # Return 0 if no valid similarity scores found

    def silhouette_score(self, X, labels):
        """Calculate the silhouette score for evaluating clustering performance.

        Args:
            X: The data matrix (numpy array).
            labels: The cluster labels for each data point.

        Returns:
            silhouette_score: The computed silhouette score.
        """
        n = len(X)  # Total number of data points
        clusters = np.unique(labels)  # Unique cluster labels
        silhouette_scores = []  # List to store silhouette scores

        for i in range(n):  # For each data point
            a = np.mean(
                np.linalg.norm(X[labels == labels[i]] - X[i], axis=1)
            )  # Compute a(i) for the same cluster

            valid_clusters = [c for c in clusters if c != labels[i]]  # Other clusters
            if valid_clusters:
                b = np.min(
                    [
                        np.mean(np.linalg.norm(X[labels == c] - X[i], axis=1))
                        for c in valid_clusters
                    ]
                )  # Compute b(i) for other clusters
                silhouette_scores.append(
                    (b - a) / max(a, b)
                )  # Compute silhouette score

        if silhouette_scores:
            return np.mean(
                silhouette_scores
            )  # If silhouette scores are available, return the mean
        else:
            return 0  # Return 0 if no valid silhouette scores found

    def find_optimal_clusters(self, max_k=10, true_k=None, save_dir=None):
        """Find the optimal number of clusters using various evaluation metrics and plot the results.

        Args:
            X: The data matrix (numpy array).
            max_k: The maximum number of clusters to consider.
            true_k: The true number of clusters in the data.
            save_dir: The directory to save the plot (optional).

        Returns:
            ch_optimal_k: The optimal number of clusters based on the Calinski-Harabasz Index.
            db_optimal_k: The optimal number of clusters based on the Davies-Bouldin Index.
            silhouette_optimal_k: The optimal number of clusters based on the Silhouette Score.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError(
                "Matplotlib is required for plotting. Please install matplotlib first."
            ) from None

        X = self.X.astype(float)  # Convert X to float type if necessary
        distortions = self.elbow_method(max_k)  # Calculate distortions for each k

        ch_indices = []  # Initialize lists for calinski_harabasz_index
        db_indices = []  # Initialize lists for davies_bouldin_index
        silhouette_scores = []  # Initialize lists for silhouette_score

        for k in range(1, max_k + 1):  # Iterate over each k value
            kmeans = KMeans(X, n_clusters=k)  # Initialize KMeans with k clusters
            kmeans.fit()  # Fit the KMeans model
            centroids = kmeans.centroids  # Get the centroids
            labels = kmeans.predict(X)  # Predict cluster labels

            ch_indices.append(
                self.calinski_harabasz_index(X, labels, centroids)
            )  # Calculate Calinski-Harabasz Index
            db_indices.append(
                self.davies_bouldin_index(X, labels, centroids)
            )  # Calculate Davies-Bouldin Index
            silhouette_scores.append(
                self.silhouette_score(X, labels)
            )  # Calculate Silhouette Score

        # Convert lists to NumPy arrays
        ch_indices = np.array(ch_indices)
        db_indices = np.array(db_indices)
        silhouette_scores = np.array(silhouette_scores)

        # Normalize the evaluation metrics
        ch_scores = (ch_indices - ch_indices.min()) / (
            ch_indices.max() - ch_indices.min()
        )
        db_scores = (db_indices - db_indices.min()) / (
            db_indices.max() - db_indices.min()
        )
        silhouette_scores = (silhouette_scores - silhouette_scores.min()) / (
            silhouette_scores.max() - silhouette_scores.min()
        )

        # Calculate the differences between consecutive scores
        ch_diffs = np.diff(ch_scores)
        db_diffs = np.diff(db_scores)
        silhouette_diffs = np.diff(silhouette_scores)

        # Calculate the second derivatives
        ch_second_derivatives = np.diff(ch_diffs)
        db_second_derivatives = np.diff(db_diffs)
        silhouette_second_derivatives = np.diff(silhouette_diffs)

        # Find the optimal k value based on the second derivative
        ch_optimal_k = np.argmax(ch_second_derivatives) + 2
        db_optimal_k = np.argmax(db_second_derivatives) + 2
        silhouette_optimal_k = np.argmax(silhouette_second_derivatives) + 2

        plt.figure(figsize=(15, 4))  # Set the figure size

        # Plot the elbow method
        plt.subplot(1, 4, 1)
        plt.plot(range(1, max_k + 1), distortions, "bx-")
        plt.xlabel("Number of clusters (k)")
        plt.ylabel("Distortion")
        plt.title("The Elbow Method showing the Optimal k")
        if true_k:
            plt.axvline(x=true_k, color="black", linestyle="--", label="true_k")

        # If legend is not empty, show the legend
        if true_k:
            plt.legend()

        # Plot Calinski-Harabasz Index
        plt.subplot(1, 4, 2)
        plt.plot(range(1, max_k + 1), ch_scores, "bx-")
        plt.xlabel("Number of clusters (k)")
        plt.ylabel("Calinski-Harabasz Index")
        plt.title("Calinski-Harabasz Index for Optimal k")
        plt.axvline(x=ch_optimal_k, color="red", linestyle="--", label="optimal_k")
        if true_k:
            plt.axvline(x=true_k, color="black", linestyle="--", label="true_k")
        plt.legend()

        # Plot Davies-Bouldin Index
        plt.subplot(1, 4, 3)
        plt.plot(range(1, max_k + 1), db_scores, "bx-")
        plt.xlabel("Number of clusters (k)")
        plt.ylabel("Davies-Bouldin Index")
        plt.title("Davies-Bouldin Index for Optimal k")
        plt.axvline(x=db_optimal_k, color="red", linestyle="--", label="optimal_k")
        if true_k:
            plt.axvline(x=true_k, color="black", linestyle="--", label="true_k")
        plt.legend()

        # Plot Silhouette Score
        plt.subplot(1, 4, 4)
        plt.plot(range(1, max_k + 1), silhouette_scores, "bx-")
        plt.xlabel("Number of clusters (k)")
        plt.ylabel("Silhouette Score")
        plt.title("Silhouette Score for Optimal k")
        plt.axvline(
            x=silhouette_optimal_k, color="red", linestyle="--", label="optimal_k"
        )
        if true_k:
            plt.axvline(x=true_k, color="black", linestyle="--", label="true_k")
        plt.legend()

        plt.tight_layout()

        if save_dir:
            plt.savefig(save_dir, dpi=300)
        else:
            plt.show()

        return (
            ch_optimal_k,
            db_optimal_k,
            silhouette_optimal_k,
        )  # Return the optimal k values


class DBSCAN:
    """This class implements the Density-Based Spatial Clustering of Applications with Noise (DBSCAN) algorithm.

    Args:
        X: The data matrix (numpy array).
        eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        min_samples: The number of samples in a neighborhood for a point to be considered as a core point.

    Methods:
        - __init__: Initializes the DBSCAN object with the input parameters.
        - fit: Fits the DBSCAN model to the data and assigns cluster labels.
        - predict: Predicts the cluster labels for new data points.
        - fit_predict: Fits the DBSCAN model and returns cluster labels.
        - silhouette_score: Calculates the Silhouette Score for evaluating clustering performance.
        - _handle_categorical: Handles categorical columns by one-hot encoding.
        - _convert_to_ndarray: Converts input data to a NumPy ndarray and handles categorical columns.
        - _custom_distance_matrix: Calculates the pairwise distance matrix using a custom distance calculation method.
    """

    def __init__(self, X, eps=0.5, min_samples=5, compile_numba=False):
        """Initialize the DBSCAN object.

        Args:
            X: The data matrix (numpy array).
            eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
            min_samples: The number of samples in a neighborhood for a point to be considered as a core point.
            compile_numba: Whether to compile the distance calculations using Numba for performance.
            If not compiled, the first call to the numba fitting function will take longer, but subsequent calls will be faster.
        """
        # Validate input parameters
        if not isinstance(eps, (int, float)) or eps <= 0:
            raise ValueError("eps must be a positive number.")
        if not isinstance(min_samples, int) or min_samples < 1:
            raise ValueError("min_samples must be a positive integer.")

        self.X = self._convert_to_ndarray(X).astype(
            float
        )  # Convert input data to ndarray
        self.eps = eps  # Maximum distance between samples
        self.min_samples = min_samples  # Minimum number of samples for core
        self.labels = None  # Cluster labels for each data point

        if compile_numba:
            try:
                from ._dbscan_jit_utils import _assign_clusters, _identify_core_points

                _identify_core_points(
                    np.zeros((1, 1)), 1, 1
                )  # Compile the numba functions
                _assign_clusters(
                    np.zeros((1, 1)), np.zeros(1), 1
                )  # Compile the numba functions
            except ImportError:
                raise ImportError(
                    "Numba is required for faster computation. Please install numba first."
                ) from None
            except Exception as e:
                raise RuntimeError(
                    f"An error occurred while importing Numba: {e}"
                ) from None

    def _handle_categorical(self, X):
        """Handle categorical columns by one-hot encoding.

        Args:
            X: The input data with potential categorical columns.

        Returns:
            X_processed: The processed data with categorical columns encoded.
        """
        categorical_cols = DataPrep.find_categorical_columns(X)
        X_processed = DataPrep.one_hot_encode(
            X, categorical_cols
        )  # One-hot encode categorical columns

        return X_processed

    def _convert_to_ndarray(self, X):
        """Convert input data to a NumPy ndarray and handle categorical columns.

        Args:
            X: The input data, which can be a list, DataFrame, or ndarray.

        Returns:
            X_ndarray: The converted and processed input data as a NumPy ndarray.
        """
        if isinstance(X, np.ndarray):  # Check if input is already a NumPy array
            X_ndarray = X.copy()  # Create a copy of the array

        elif isinstance(X, list):  # Check if input is a list
            X_ndarray = np.array(X)  # Convert list to NumPy array

        elif isinstance(X, pd.DataFrame):  # Check if input is a DataFrame
            X_ndarray = X.values  # Convert DataFrame to NumPy array

        else:  # Raise error for unsupported input type
            raise ValueError(
                "Unsupported input type. Input must be a list, NumPy array, or DataFrame."
            )

        X_processed = self._handle_categorical(X_ndarray)  # Handle categorical columns

        return X_processed

    def _custom_distance_matrix(self, X1, X2, metric="euclidean"):
        """Calculate the pairwise distance matrix between two sets of data points using a custom distance calculation method.

        Args:
            X1: The first data matrix (numpy array).
            X2: The second data matrix (numpy array).
            metric: The distance metric to use ('euclidean', 'manhattan', or 'cosine').

        Returns:
            dist_matrix: The pairwise distance matrix between data points in X1 and X2.
        """
        if metric == "euclidean":
            # Euclidean distance calculation: f(x) = sqrt(sum((x1 - x2)^2))
            dist_matrix = np.sqrt(
                np.sum((X1[:, np.newaxis, :] - X2[np.newaxis, :, :]) ** 2, axis=2)
            )
        elif metric == "manhattan":
            # Manhattan distance calculation: f(x) = sum(|x1 - x2|)
            dist_matrix = np.sum(
                np.abs(X1[:, np.newaxis, :] - X2[np.newaxis, :, :]), axis=2
            )
        elif metric == "cosine":
            # Cosine distance calculation: f(x) = 1 - (x1 . x2) / (||x1|| * ||x2||)
            X1_normalized = X1 / np.linalg.norm(X1, axis=1)[:, np.newaxis]
            X2_normalized = X2 / np.linalg.norm(X2, axis=1)[:, np.newaxis]
            dist_matrix = 1 - np.dot(X1_normalized, X2_normalized.T)
        else:
            raise ValueError(f"Unsupported metric: {metric}")

        return dist_matrix

    def fit(self, metric="euclidean", numba=False):
        """Fit the DBSCAN model to the data.

        Algorithm Steps:
        1. Calculate the distance matrix between all points in the dataset.
        2. Identify core points based on the minimum number of neighbors within eps distance.
        3. Assign cluster labels using depth-first search (DFS) starting from core points.

        Args:
            metric: The distance metric to use ('euclidean', 'manhattan', or 'cosine').
            numba: Whether to use numba for faster computation.

        Returns:
            labels: The cluster labels for each data point.
        """
        if numba:
            try:
                from ._dbscan_jit_utils import _assign_clusters, _identify_core_points
            except ImportError:
                raise ImportError(
                    "Numba is required for faster computation. Please install numba first."
                ) from None

        dist_matrix = self._custom_distance_matrix(
            self.X, self.X, metric
        )  # Calculate pairwise distance matrix

        core_points = np.zeros(self.X.shape[0], dtype=bool)  # Initialize core points
        labels = -1 * np.ones(self.X.shape[0], dtype=int)  # Initialize labels
        cluster_id = 0  # Initialize cluster ID

        if numba:
            core_points = _identify_core_points(dist_matrix, self.eps, self.min_samples)
            labels = _assign_clusters(dist_matrix, core_points, self.eps)
        else:
            for i in range(self.X.shape[0]):  # For each data point
                neighbors = np.where(dist_matrix[i] < self.eps)[
                    0
                ]  # Find neighbors within eps distance

                if len(neighbors) >= self.min_samples:
                    core_points[i] = True  # If core point, mark as True

            for i in range(self.X.shape[0]):  # For each data point
                if labels[i] == -1 and core_points[i]:  # If core point and unassigned
                    labels[i] = cluster_id  # Assign cluster ID
                    stack = [i]  # Initialize stack with core point

                    while stack:  # Depth-first search (DFS)
                        point = stack.pop()  # Pop the top element
                        neighbors = np.where(dist_matrix[point] < self.eps)[
                            0
                        ]  # Find neighbors within eps distance

                        if len(neighbors) >= self.min_samples:  # If core point
                            for neighbor in neighbors:  # For each neighbor
                                if labels[neighbor] == -1:  # If unassigned
                                    labels[neighbor] = cluster_id  # Assign cluster ID
                                    stack.append(neighbor)  # Add to stack
                    cluster_id += 1  # Increment cluster ID

        self.labels = labels  # Store cluster labels
        return labels

    def predict(self, new_X):
        """Predict the cluster labels for new data points.

        Note: DBSCAN does not naturally support predicting new data points.

        Args:
            new_X: The data matrix to predict (numpy array).

        Returns:
            labels: The predicted cluster labels (-1 for noise).
        """
        # Validate input parameters
        if not isinstance(
            new_X, (np.ndarray, list, pd.DataFrame)
        ):  # Check if input is a valid type
            raise ValueError(
                "Unsupported input type. Input must be a list, NumPy array, or DataFrame."
            )
        if new_X.shape[1] != self.X.shape[1]:  # Check if number of features match
            raise ValueError(
                f"Number of features in new_X ({new_X.shape[1]}) does not match the model ({self.X.shape[1]})."
            )
        if self.labels is None:  # Check if model has been fitted
            raise ValueError("Fit the model before predicting.")

        new_X = self._convert_to_ndarray(new_X).astype(
            float
        )  # Convert input data to ndarray
        dist_matrix = self._custom_distance_matrix(
            new_X, self.X
        )  # Calculate distance matrix
        labels = -1 * np.ones(
            new_X.shape[0], dtype=int
        )  # Initialize labels for new data points as noise (-1)

        for i in range(new_X.shape[0]):  # For each new data point
            neighbors = np.where(dist_matrix[i] < self.eps)[
                0
            ]  # Find neighbors within eps distance

            if len(neighbors) > 0:  # If neighbors found
                labels[i] = self.labels[
                    neighbors[0]
                ]  # Assign the cluster label of the first neighbor

        return labels

    def fit_predict(self, numba=False):
        """Fit the DBSCAN model to the data and return the cluster labels.

        Returns:
            labels: The cluster labels for the data.
        """
        return self.fit(numba=numba)  # Fits the DBSCAN model and return cluster labels

    def silhouette_score(self):
        """Calculate the silhouette score for evaluating clustering performance.

        Returns:
            silhouette_score: The computed silhouette score.
        """
        if (
            self.labels is None or len(set(self.labels)) <= 1
        ):  # If cluster labels are available and at least two unique clusters
            return -1

        a = np.zeros(len(self.X))  # Initialize a(i) for each data point
        b = np.zeros(len(self.X))  # Initialize b(i) for each data point

        for i in range(len(self.X)):  # For each data point
            same_cluster = (
                self.labels == self.labels[i]
            )  # Indices of points in the same cluster as point i
            other_clusters = (
                self.labels != self.labels[i]
            )  # Indices of points in other clusters

            if np.sum(same_cluster) > 1:  # If more than one point in the same cluster
                a[i] = np.mean(
                    np.linalg.norm(self.X[same_cluster] - self.X[i], axis=1)
                )  # Compute a(i)
            else:
                a[i] = 0  # Set a(i) to 0 if only one point in the same cluster

            # Compute b(i) for each cluster different from point i's cluster
            other_cluster_distances = [
                np.mean(
                    np.linalg.norm(
                        self.X[other_clusters & (self.labels == label)] - self.X[i],
                        axis=1,
                    )
                )
                for label in set(self.labels)
                if label != -1 and label != self.labels[i]
            ]
            if other_cluster_distances:
                b[i] = np.min(other_cluster_distances)
            else:
                b[i] = 0

        silhouette_scores = (b - a) / np.maximum(
            a, b
        )  # Compute silhouette scores for all points
        silhouette_score = np.mean(silhouette_scores)  # Compute mean silhouette score

        return silhouette_score

    def auto_eps(
        self, min=0.1, max=1.1, precision=0.01, return_scores=False, verbose=False
    ):
        """Find the optimal eps value for DBSCAN based on silhouette score.

        Args:
            min: The minimum eps value to start the search.
            max: The maximum eps value to end the search.
            precision: The precision of the search.
            return_scores: Whether to return a dictionary of (eps, score) pairs.
            verbose: Whether to print the silhouette score for each eps value.

        Returns:
            eps: The optimal eps value.
            scores_dict (optional): A dictionary of (eps, score) pairs if return_scores is True.
        """
        # Validate input parameters
        if not isinstance(min, (int, float)) or min <= 0:
            raise ValueError("min must be a positive number.")
        if not isinstance(max, (int, float)) or max <= 0:
            raise ValueError("max must be a positive number.")
        if not isinstance(precision, (int, float)) or precision <= 0:
            raise ValueError("precision must be a positive number.")

        best_eps = 0.1
        best_score = -1
        step = 0.1
        scores_dict = {}

        # Iterate over different eps values with decreasing step size based on precision
        while step >= precision:
            for eps in np.arange(min, max, step):
                self.eps = eps
                self.fit()
                score = self.silhouette_score()
                # try:
                #     score = self.silhouette_score()
                # except:
                #     score = float('-inf')

                scores_dict[eps] = score
                if verbose:
                    print(f"eps: {eps:.3f}, score: {score:.4f}")
                if score > best_score:
                    if verbose:
                        print(f"\tNew best score: {score:.4f}")
                    best_score = score
                    best_eps = eps
            min = best_eps - step
            max = best_eps + step
            step /= 10

        self.eps = best_eps
        if return_scores:
            return best_eps, scores_dict
        return best_eps
