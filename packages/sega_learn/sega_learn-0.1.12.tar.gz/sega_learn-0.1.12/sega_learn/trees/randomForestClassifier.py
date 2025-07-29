"""This module contains the implementation of a Random Forest Classifier.

The module includes the following classes:
- RandomForest: A class representing a Random Forest model.
- RandomForestWithInfoGain: A class representing a Random Forest model that returns information gain for vis.
- runRandomForest: A class that runs the Random Forest algorithm.
"""

# Importing the required libraries
import multiprocessing
from datetime import datetime

import numpy as np
from joblib import Parallel, delayed

from sega_learn.utils.metrics import Metrics

from .treeClassifier import ClassifierTree


def _fit_tree(X, y, max_depth, min_samples_split, sample_weight=None):
    """Helper function for parallel tree fitting. Fits a single tree on a bootstrapped sample.

    Args:
        X: (array-like) - The input features.
        y: (array-like) - The target labels.
        max_depth: (int) - The maximum depth of the tree.
        min_samples_split: (int) - The minimum samples required to split a node.
        sample_weight: (array-like or None) - The weights for each sample.

    Returns:
        ClassifierTree: A fitted tree object.
    """
    # Create bootstrapped sample
    indices = np.random.choice(len(X), size=len(X), replace=True)
    X_sample = X[indices]
    y_sample = y[indices]

    # Fit tree on bootstrapped sample
    tree = ClassifierTree(max_depth=max_depth, min_samples_split=min_samples_split)
    return tree.fit(X_sample, y_sample, sample_weight)


def _classify_oob(X, trees, bootstraps):
    """Helper function for parallel out-of-bag predictions. Classifies using out-of-bag samples.

    Args:
        X: (array-like) - The input features.
        trees: (list) - The list of fitted trees.
        bootstraps: (list) - The list of bootstrapped indices for each tree.

    Returns:
        list: The list of out-of-bag predictions.
    """
    all_classifications = []

    for i, record in enumerate(X):
        classifications = []
        for _j, (tree, bootstrap) in enumerate(zip(trees, bootstraps)):
            # Check if record is out-of-bag for this tree
            if i not in bootstrap:
                classifications.append(ClassifierTree.classify(tree, record))
        # Determine the majority vote
        if len(classifications) > 0:
            counts = np.bincount(classifications)
            majority_class = np.argmax(counts)
            all_classifications.append(majority_class)
        else:
            all_classifications.append(np.random.choice([0, 1]))

    return all_classifications


class RandomForestClassifier:
    """RandomForestClassifier is a custom implementation of a Random Forest classifier.

    Attributes:
        n_estimators (int): The number of trees in the forest.
        max_depth (int): The maximum depth of each tree.
        n_jobs (int): The number of jobs to run in parallel. Defaults to -1 (use all available processors).
        random_state (int or None): The seed for random number generation. Defaults to None.
        trees (list): A list of trained decision trees.
        bootstraps (list): A list of bootstrapped indices for out-of-bag (OOB) scoring.
        X (numpy.ndarray or None): The feature matrix used for training.
        y (numpy.ndarray or None): The target labels used for training.
        accuracy (float): The accuracy of the model after fitting.
        precision (float): The precision of the model after fitting.
        recall (float): The recall of the model after fitting.
        f1_score (float): The F1 score of the model after fitting.
        log_loss (float or None): The log loss of the model after fitting (only for binary classification).

    Methods:
        __init__(n_estimators=100, max_depth=10, n_jobs=-1, random_seed=None, X=None, y=None):
            Initializes the RandomForestClassifier object with the specified parameters.
        fit(X=None, y=None, verbose=False):
            Fits the random forest model to the provided data using parallel processing.
        calculate_metrics(y_true, y_pred):
            Calculates evaluation metrics (accuracy, precision, recall, F1 score, and log loss) for classification.
        predict(X):
            Predicts class labels for the provided data using the trained random forest.
        get_stats(verbose=False):
            Returns the evaluation metrics (accuracy, precision, recall, F1 score, and log loss) as a dictionary.
    """

    def __init__(
        self,
        n_estimators=100,
        max_depth=10,
        min_samples_split=2,
        n_jobs=-1,
        random_seed=None,
        X=None,
        y=None,
    ):
        """Initializes the RandomForest object."""
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_jobs = n_jobs if n_jobs > 0 else max(1, multiprocessing.cpu_count())
        self.random_state = random_seed
        self.trees = []
        self.bootstraps = []

        if isinstance(X, tuple):
            self.X = np.array([X])
        else:
            self.X = X
        self.y = y

    def get_params(self):
        """Get the parameters of the RandomForestClassifier."""
        return {
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "n_jobs": self.n_jobs,
            "random_seed": self.random_state,
        }

    def fit(self, X=None, y=None, sample_weight=None, verbose=False):
        """Fit the random forest with parallel processing."""
        if X is None and self.X is None:
            raise ValueError(
                "X must be provided either during initialization or fitting."
            )
        if y is None and self.y is None:
            raise ValueError(
                "y must be provided either during initialization or fitting."
            )

        start_time = datetime.now()

        # Set random seed
        if self.random_state is not None:
            np.random.seed(self.random_state)

        # Convert inputs to numpy arrays, use provided data if available
        X = np.asarray(X if X is not None else self.X)
        y = np.asarray(y if y is not None else self.y)

        # If X or y are empty, raise an error
        if X.size == 0 or y.size == 0:
            raise ValueError("X and y must not be empty.")

        # Sample weight handling
        if sample_weight is None:
            sample_weight = np.ones(len(y), dtype=np.float64)
        else:
            sample_weight = np.asarray(sample_weight, dtype=np.float64)
            if sample_weight.shape[0] != len(y):
                raise ValueError("sample_weight length mismatch.")

        if verbose:
            print("Fitting trees in parallel...")

        # Fit trees in parallel
        self.trees = Parallel(n_jobs=self.n_jobs)(
            delayed(_fit_tree)(
                X, y, self.max_depth, self.min_samples_split, sample_weight
            )
            for _ in range(self.n_estimators)
        )

        # Generate bootstrapped indices for OOB scoring
        self.bootstraps = [
            np.random.choice(len(X), size=len(X), replace=True)
            for _ in range(self.n_estimators)
        ]

        # Compute OOB predictions
        if verbose:
            print("Computing OOB predictions...")

        y_pred = _classify_oob(X, self.trees, self.bootstraps)

        # Calculate evaluation metrics
        self.calculate_metrics(y, y_pred)

        if verbose:
            print(f"Execution time: {datetime.now() - start_time}")
            print(f"Accuracy:  {self.accuracy:.4f}")
            print(f"Precision: {self.precision:.4f}")
            print(f"Recall:    {self.recall:.4f}")
            print(f"F1 Score:  {self.f1_score:.4f}")
            print(f"Log Loss:  {self.log_loss:.4f}")

        return self

    def calculate_metrics(self, y_true, y_pred):
        """Calculate evaluation metrics for classification."""
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        self.accuracy = Metrics.accuracy(y_true, y_pred)
        self.precision = Metrics.precision(y_true, y_pred)
        self.recall = Metrics.recall(y_true, y_pred)
        self.f1_score = Metrics.f1_score(y_true, y_pred)
        if len(np.unique(y_true)) == 2:
            self.log_loss = Metrics.log_loss(y_true, y_pred)

    def predict(self, X):
        """Predict class labels for the provided data."""
        X = np.asarray(X)

        # Validate input dimensions
        if self.X is not None and X.shape[1] != self.X.shape[1]:
            raise ValueError(
                f"Input data must have {self.X.shape[1]} features, but got {X.shape[1]}."
            )

        predictions = []
        for record in X:
            classifications = []
            for tree in self.trees:
                classifications.append(ClassifierTree.classify(tree, record))
            # Determine the majority vote
            counts = np.bincount(classifications)
            majority_class = np.argmax(counts)
            predictions.append(majority_class)

        return predictions

    def predict_proba(self, X):
        """Predict class probabilities for the provided data.

        Args:
            X (array-like): The input features.

        Returns:
            np.ndarray: A 2D array where each row represents the probability distribution
                        over the classes for a record.
        """

        def traverse_tree(tree, record):
            """Helper function to traverse the tree and collect class probabilities."""
            if "label" in tree:
                # If it's a leaf node, return the probability as 1 for the majority class
                return {tree["label"]: 1.0}

            # Traverse left or right subtree based on the split condition
            if record[tree["split_attribute"]] <= tree["split_val"]:
                return traverse_tree(tree["left"], record)
            else:
                return traverse_tree(tree["right"], record)

        X = np.asarray(X)

        # Validate input dimensions
        if self.X is not None and X.shape[1] != self.X.shape[1]:
            raise ValueError(
                f"Input data must have {self.X.shape[1]} features, but got {X.shape[1]}."
            )

        # Initialize an array to store the sum of probabilities for each class
        n_classes = len(np.unique(self.y))
        probabilities = np.zeros((X.shape[0], n_classes))

        # Aggregate probabilities from all trees
        for tree in self.trees:
            for _i, record in enumerate(X):
                # Traverse the tree to get class probabilities for the record
                tree_probs = traverse_tree(tree, record)

                # Convert probabilities to a numpy array
                tree_probs = np.array(
                    [tree_probs.get(cls, 0) for cls in range(n_classes)]
                )

                # Normalize the probabilities to sum to 1
                tree_probs /= np.sum(tree_probs)

            # Sum probabilities for each class
            for i in range(X.shape[0]):
                probabilities[i] += tree_probs

        # Normalize probabilities to ensure they sum to 1 for each record
        probabilities /= len(self.trees)

        return probabilities

    def get_stats(self, verbose=False):
        """Return the evaluation metrics."""
        stats = {
            "Accuracy": self.accuracy,
            "Precision": self.precision,
            "Recall": self.recall,
            "F1 Score": self.f1_score,
            "Log Loss": self.log_loss if len(np.unique(self.y)) == 2 else None,
        }

        if verbose:
            for metric, value in stats.items():
                print(f"{metric}: {value:.4f}")

        return stats
