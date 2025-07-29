# Importing the required libraries

import joblib
import numpy as np

# Here's a high-level overview:
# Random Subsampling:
#   The algorithm starts by randomly selecting a subset of the data.
#   This helps in reducing the computational complexity and ensures that the algorithm can handle large datasets efficiently.
# Building Isolation Trees:
#   For each subset, the algorithm builds an isolation tree.
#   A binary tree where each node splits the data based on a randomly selected feature and a randomly selected split value between the minimum and maximum values of that feature.
# Isolation Path Length:
#   The path length from the root of the tree to a given observation is recorded.
#   The idea is that anomalies, being few and different, will have shorter paths on average because they are easier to isolate.
# Averaging Path Lengths:
#   The average path length of an observation across all trees is calculated.
#   This average path length is then used to compute an anomaly score.
# Anomaly Score:
#   The anomaly score is derived from the average path length.
#   Observations with shorter average path lengths are considered anomalies.
#   The score is typically normalized to a range between 0 and 1, where a score close to 1 indicates a high likelihood of being an anomaly.


class IsolationUtils:
    """Utility functions for the Isolation Forest algorithm."""

    @staticmethod
    def compute_avg_path_length(size):
        """Computes the average path length of unsuccessful searches in a binary search tree.

        Args:
            size: (int) - The size of the tree.

        Returns:
            average_path_length: (float) - The average path length.
        """
        # If the size is less than or equal to 1, return 0
        # This is because a tree with 0 or 1 nodes has no path to traverse
        if size <= 1:
            return 0
        # Else, calculate the average path length using the formula:
        # 2 * (log(size - 1) + Euler's constant) - (2 * (size - 1) / size)
        return 2 * (np.log(size - 1) + 0.5772156649) - (2 * (size - 1) / size)


class IsolationTree:
    """IsolationTree is a class that implements an isolation tree, which is a fundamental building block of the Isolation Forest algorithm.

    The Isolation Forest is an unsupervised learning method used for anomaly detection.

    Attributes:
        max_depth (int): The maximum depth of the tree. Default is 10.
        tree (dict): The learned isolation tree structure.
        force_true_length (bool): If True, the true path length is used for scoring
            instead of the average path length.

    Methods:
        __init__(max_depth=10, force_true_length=False):
            Initializes the IsolationTree with the specified maximum depth and
            scoring method.
        fit(X, depth=0):
            Fits the isolation tree to the input data by recursively partitioning
            the data based on randomly selected features and split values.
        path_length(X, tree=None, depth=0):
            Computes the path length for a given sample by traversing the tree
            structure. The path length is used to determine how isolated a sample is.
    """

    def __init__(self, max_depth=10, force_true_length=False):
        """Initializes the Isolation Forest with specified parameters.

        Args:
            max_depth: (int), optional - Maximum depth of the tree (default is 10).
            force_true_length: (bool), optional - If True, use the true path length for scoring (default is False).

        Attributes:
            max_depth: (int) - Maximum depth of the tree.
            tree: (object or None) - The tree structure used in the Isolation Forest (default is None).
            force_true_length: (bool) - Indicates whether to use the true path length for scoring.
        """
        self.max_depth = max_depth
        self.tree = None
        self.force_true_length = (
            force_true_length  # If true, use the true path length for scoring
        )

    def fit(self, X, depth=0):
        """Fits the isolation tree to the data.

        Args:
            X: (array-like) - The input features.
            depth: (int) - The current depth of the tree (default: 0).

        Returns:
            dict: The learned isolation tree.
        """
        if len(X) == 0:
            raise ValueError("Input data X cannot be empty.")

        if len(X) <= 1 or depth >= self.max_depth:
            return {"size": len(X)}

        # Randomly select a feature and a split value
        feature = np.random.randint(0, X.shape[1])
        split_val = np.random.uniform(np.min(X[:, feature]), np.max(X[:, feature]))

        # Partition the data
        X_left = X[X[:, feature] <= split_val]
        X_right = X[X[:, feature] > split_val]

        # Recursively build the left and right subtrees
        left_tree = self.fit(X_left, depth + 1)
        right_tree = self.fit(X_right, depth + 1)

        self.tree = {
            "feature": feature,
            "split_val": split_val,
            "left": left_tree,
            "right": right_tree,
        }
        return self.tree

    def path_length(self, X, tree=None, depth=0):
        """Computes the path length for a given sample.

        Args:
            X: (array-like) - The input sample.
            tree: (dict) - The current node of the tree (default: None).
            depth: (int) - The current depth of the tree (default: 0).

        Returns:
            int: The path length.
        """
        if len(X) == 0:
            raise ValueError("Input data X cannot be empty.")

        if tree is None:
            tree = self.tree

        if "size" in tree:
            if self.force_true_length:
                return depth  # Return the true path length
            else:
                return depth + IsolationUtils.compute_avg_path_length(
                    tree["size"]
                )  # Return the average path length for the size

        feature = tree["feature"]
        split_val = tree["split_val"]

        if X[feature] <= split_val:
            return self.path_length(X, tree["left"], depth + 1)
        else:
            return self.path_length(X, tree["right"], depth + 1)


class IsolationForest:
    """IsolationForest is an implementation of the Isolation Forest algorithm for anomaly detection.

    Attributes:
        n_trees (int): The number of isolation trees to build. Default is 100.
        max_samples (int or None): The maximum number of samples to draw for each tree. If None, defaults to the minimum of 256 or the number of samples in the dataset.
        max_depth (int): The maximum depth of each isolation tree. Default is 10.
        n_jobs (int): The number of parallel jobs to run. Set to -1 to use all available cores. Default is 1.
        force_true_length (bool): Whether to force the true path length calculation. Default is False.
        trees (list): A list to store the trained isolation trees.
        classes_ (numpy.ndarray): An array representing the classes (0 for normal, 1 for anomaly).

    Methods:
        __init__(n_trees=100, max_samples=None, max_depth=10, n_jobs=1, force_true_length=False):
            Initializes the IsolationForest with the specified parameters.
        fit(X):
            Fits the isolation forest to the data.
                X (array-like): The input features.
        _fit_tree(X):
            Fits a single isolation tree to a subset of the data.
                X (array-like): The input features.
                IsolationTree: A trained isolation tree.
        anomaly_score(X):
            Computes the anomaly scores for given samples.
                X (array-like): The input samples.
                numpy.ndarray: An array of anomaly scores.
        predict(X, threshold=0.5):
            Predicts whether samples are anomalies.
                X (array-like): The input samples.
                threshold (float): The threshold for classifying anomalies (default: 0.5).
                numpy.ndarray: An array of predictions (1 if the sample is an anomaly, 0 otherwise).
        __sklearn_is_fitted__():
            Checks if the model has been fitted.
                bool: True if the model is fitted, False otherwise.
    """

    def __init__(
        self,
        n_trees=100,
        max_samples=None,
        max_depth=10,
        n_jobs=1,
        force_true_length=False,
    ):
        """Initializes the IsolationForest with the specified parameters.

        Args:
            n_trees: (int), optional - The number of isolation trees to build (default: 100).
            max_samples: (int or None), optional - The maximum number of samples to draw for each tree.
                If None, defaults to the minimum of 256 or the number of samples in the dataset (default: None).
            max_depth: (int), optional - The maximum depth of each isolation tree (default: 10).
            n_jobs: (int), optional - The number of parallel jobs to run.
                Set to -1 to use all available cores (default: 1).
            force_true_length: (bool), optional - Whether to force the true path length calculation (default: False).

        Attributes:
            n_trees: (int) - The number of isolation trees.
            max_samples: (int or None) - The maximum number of samples for each tree.
            max_depth: (int) - The maximum depth of the trees.
            force_true_length: (bool) - Indicates whether to use the true path length for scoring.
            trees: (list) - A list to store the trained isolation trees.
            n_jobs: (int) - The number of parallel jobs to run.
            classes_: (np.ndarray) - An array representing the classes (0 for normal, 1 for anomaly).
        """
        self.n_trees = n_trees
        self.max_samples = max_samples
        self.max_depth = max_depth
        self.force_true_length = force_true_length
        self.trees = []
        self.n_jobs = n_jobs

        if self.n_jobs == 0:
            raise ValueError(
                "n_jobs must be greater than 0. Set to -1 for all available cores."
            )
        if self.n_jobs == -1:
            self.n_jobs = joblib.cpu_count()
        if self.n_jobs > joblib.cpu_count():
            raise ValueError(
                f"n_jobs cannot be greater than the number of available cores: {joblib.cpu_count()}"
            )

        self.classes_ = np.array([0, 1])  # Define the classes attribute

    def fit(self, X, y=None):
        """Fits the isolation forest to the data.

        Args:
            X: (array-like) - The input features.
            y: (array-like) - The target labels (not used in this implementation).
        """
        if self.max_samples is None:
            self.max_samples = min(256, len(X))

        self.trees = joblib.Parallel(n_jobs=self.n_jobs)(
            joblib.delayed(self._fit_tree)(X) for _ in range(self.n_trees)
        )

    def _fit_tree(self, X):
        if len(X) > self.max_samples:
            X_sample = X[np.random.choice(len(X), self.max_samples, replace=False)]
        else:
            X_sample = X

        tree = IsolationTree(
            max_depth=self.max_depth, force_true_length=self.force_true_length
        )
        tree.fit(X_sample)
        return tree

    def anomaly_score(self, X):
        """Computes the anomaly scores for given samples.

        Args:
            X: (array-like) - The input samples.

        Returns:
            array: An array of anomaly scores.
        """
        if X.ndim == 1:
            X = X.reshape(1, -1)
        path_lengths = np.array(
            [[tree.path_length(x) for tree in self.trees] for x in X]
        )
        avg_path_lengths = np.mean(path_lengths, axis=1)
        return 2 ** (
            -avg_path_lengths / IsolationUtils.compute_avg_path_length(self.max_samples)
        )

    def predict(self, X, threshold=0.5):
        """Predicts whether samples are anomalies.

        Args:
            X: (array-like) - The input samples.
            threshold: (float) - The threshold for classifying anomalies (default: 0.5).

        Returns:
            array: An array of predictions (1 if the sample is an anomaly, 0 otherwise).
        """
        if X.ndim == 1:
            X = X.reshape(1, -1)
        scores = np.array([self.anomaly_score(x) for x in X])
        return (scores > threshold).astype(int)

    def __sklearn_is_fitted__(self):
        """Checks if the model has been fitted."""
        return len(self.trees) > 0


# # Example usage
# if __name__ == "__main__":
#     # Generate some sample data
#     X = np.random.randn(1000, 2)

#     # Fit the isolation forest
#     iso_forest = IsolationForest(n_trees=100, max_samples=256, max_depth=10)
#     iso_forest.fit(X)

#     # Predict anomaly scores for new samples
#     new_samples = np.random.randn(10, 2)
#     for sample in new_samples:
#         score = iso_forest.anomaly_score(sample)
#         prediction = iso_forest.predict(sample)
#         print(f"Sample: {sample}, Anomaly Score: {score}, Prediction: {'Anomaly' if prediction == 1 else 'Normal'}")

# # Compare training time for n_jobs
# if __name__ == "__main__":
#     import time

#     # Generate synthetic data for testing
#     X = np.random.randn(1_000_000, 10)

#     def fit_and_time(num_jobs):
#         model = IsolationForest(n_jobs=num_jobs)
#         start_time = time.time()
#         model.fit(X)
#         end_time = time.time()
#         return end_time - start_time

#     for num_jobs in [1, 2, 4, 8, -1]:
#         elapsed_time = fit_and_time(num_jobs)
#         print(f"Training time with n_jobs={num_jobs}: {elapsed_time:.2f} seconds")
