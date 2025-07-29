# Importing the required libraries
import warnings

import numpy as np


class RegressorTreeUtility:
    """Utility class containing helper functions for building the Regressor Tree.

    Handles variance calculation, leaf value calculation, and finding the best split.
    """

    def __init__(self, X, y, min_samples_split, n_features):
        """Initialize the utility class with references to data and parameters.

        Args:
            X (np.ndarray): Reference to the feature data.
            y (np.ndarray): Reference to the target data.
            min_samples_split (int): Minimum number of samples required to split a node.
            n_features (int): Total number of features in X.
        """
        self._X = X
        self._y = y
        self.min_samples_split = min_samples_split
        self._n_features = n_features

    def calculate_variance(self, indices, sample_weight=None):
        """Calculate weighted variance for the subset defined by indices."""
        n_indices = len(indices)
        if n_indices == 0:
            return 0.0

        y_subset = self._y[indices]
        if sample_weight is None:
            return np.var(y_subset)
        else:
            # Ensure weights correspond to the subset indices
            weights_subset = sample_weight[indices]
            total_weight = np.sum(weights_subset)
            if total_weight <= 0:
                return 0.0  # Avoid division by zero

            weighted_mean = np.average(y_subset, weights=weights_subset)
            weighted_variance = np.average(
                (y_subset - weighted_mean) ** 2, weights=weights_subset
            )
            return weighted_variance

    def calculate_leaf_value(self, indices, sample_weight=None):
        """Calculate the weighted mean value for a leaf node."""
        n_indices = len(indices)
        if n_indices == 0:
            return np.nan

        y_subset = self._y[indices]
        if sample_weight is None:
            return np.mean(y_subset)
        else:
            weights_subset = sample_weight[indices]
            total_weight = np.sum(weights_subset)
            if total_weight <= 0:
                return np.mean(
                    y_subset
                )  # Fallback to unweighted mean if weights sum to 0

            return np.average(y_subset, weights=weights_subset)

    def best_split(self, indices, sample_weight=None):
        """Finds the best split for the data subset defined by indices."""
        n_samples_node = len(indices)
        if n_samples_node < self.min_samples_split:
            return None  # Not enough samples to split

        if sample_weight is None:
            current_sample_weight = np.ones(n_samples_node)
        else:
            # Get weights corresponding to the current node's indices
            current_sample_weight = sample_weight[indices]

        # Calculate variance of the current node using the utility's method
        parent_variance = self.calculate_variance(indices, sample_weight)
        if parent_variance == 0:  # Pure node already
            return None

        best_gain = -np.inf
        best_split_info = None

        # Consider a subset of features
        num_features_total = self._n_features
        if num_features_total <= 0:
            return None
        num_features_to_consider = max(1, int(np.sqrt(num_features_total)))
        if num_features_to_consider > num_features_total:
            num_features_to_consider = num_features_total

        selected_feature_indices = np.random.choice(
            num_features_total, size=num_features_to_consider, replace=False
        )

        # Use data corresponding to current indices (referencing X stored in utility)
        X_node = self._X[indices]
        # y_node is implicitly used via self.calculate_variance

        for feature_idx in selected_feature_indices:
            feature_values = X_node[:, feature_idx]
            potential_split_values = np.unique(
                np.percentile(feature_values, [25, 50, 75])
            )

            for split_val in potential_split_values:
                # Partition INDICES, not data
                # mask applies to the *subset* X_node
                mask_left = feature_values <= split_val
                indices_left = indices[mask_left]
                indices_right = indices[~mask_left]

                n_left, n_right = len(indices_left), len(indices_right)

                # Ensure split creates two non-empty children
                # (Could add min_samples_leaf check here too)
                if n_left == 0 or n_right == 0:
                    continue

                # Calculate gain based on children's variance using the utility's method
                var_left = self.calculate_variance(indices_left, sample_weight)
                var_right = self.calculate_variance(indices_right, sample_weight)

                # # Weighted variance of children
                # child_variance = (
                #     n_left * var_left + n_right * var_right
                # ) / n_samples_node

                # Use total weight for weighting child variances
                total_weight_node = np.sum(current_sample_weight)
                if total_weight_node <= 0:
                    continue  # Should not happen if validated earlier

                weight_left = np.sum(current_sample_weight[mask_left])
                weight_right = np.sum(current_sample_weight[~mask_left])

                if weight_left <= 0 or weight_right <= 0:
                    continue  # Avoid division by zero if weights are zero

                child_variance = (
                    weight_left * var_left + weight_right * var_right
                ) / total_weight_node

                # Information gain (variance reduction)
                info_gain = parent_variance - child_variance

                if info_gain > best_gain:
                    best_gain = info_gain
                    best_split_info = {
                        "feature_idx": feature_idx,
                        "threshold": split_val,
                        "indices_left": indices_left,
                        "indices_right": indices_right,
                        "info_gain": info_gain,
                    }

        # If no split improves variance (info_gain <= 0), best_split_info remains None
        # Or if initial checks failed (e.g., pure node, not enough samples)
        if best_gain <= 0:
            return None

        return best_split_info


class RegressorTree:
    """A class representing a decision tree for regression.

    Args:
        max_depth: (int) - The maximum depth of the decision tree.
        min_samples_split: (int) - The minimum number of samples required to split a node.
        n_features: (int) - The number of features in the dataset.
        X: (array-like) - The input features.
        y: (array-like) - The target labels.

    Methods:
        fit(X, y, verbose=False): Fits the decision tree to the training data.
        predict(X): Predicts the target values for the input features.
        _traverse_tree(x, node): Traverses the decision tree for a single sample x.
        _leran_recursive(indices, depth): Recursive helper function for learning.
    """

    def __init__(self, max_depth=5, min_samples_split=2):
        """Initialize the decision tree.

        Args:
            max_depth (int): The maximum depth of the decision tree.
            min_samples_split (int): The minimum number of samples required to split a node.
        """
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split  # Minimum samples required to split
        self.tree = {}
        self._X = None  # Store reference to original X
        self._y = None  # Store reference to original y
        self._n_features = None

    def fit(self, X, y, sample_weight=None, verbose=False):
        """Fit the decision tree to the training data.

        Args:
            X: (array-like) - The input features.
            y: (array-like) - The target labels.
            sample_weight: (array-like) - The sample weights (default: None).
            verbose: (bool) - If True, print detailed logs during fitting.

        Returns:
            dict: The learned decision tree.
        """
        self.verbose = verbose

        # Convert only once and store references
        self._X = np.asarray(X)
        self._y = np.asarray(y)
        self._n_features = self._X.shape[1]

        # Handle sample_weight
        if sample_weight is not None and sample_weight is not False:
            sample_weight = np.asarray(sample_weight)
            if sample_weight.shape[0] != self._X.shape[0]:
                raise ValueError("sample_weight must have the same length as X.")
        else:
            # Use equal weights if none provided
            sample_weight = np.ones(self._X.shape[0])

        # validate input data
        if self._X.shape[0] != self._y.shape[0]:
            raise ValueError("X and y must have the same number of samples.")
        elif self._X.shape[0] == 0 or self._y.shape[0] == 0:
            raise ValueError("X and y must not be empty.")

        # Initialize the utility class here, passing data references and params
        self.utility = RegressorTreeUtility(
            self._X, self._y, self.min_samples_split, self._n_features
        )

        initial_indices = np.arange(self._X.shape[0])
        self.tree = self._learn_recursive(
            initial_indices, depth=0, sample_weight=sample_weight
        )

        if verbose:
            print(f"Fitted tree with {len(X)} samples and max depth {self.max_depth}\n")

        return self.tree

    def predict(self, X):
        """Predict the target value for a record or batch of records using the decision tree.

        Args:
            X: (array-like) - The input features.

        Returns:
            np.ndarray: The predicted target values.
        """
        if not isinstance(X, ((list, np.ndarray))):
            raise TypeError("X must be a list or NumPy array.")
        # If not fitted, raise error (if tree is empty {})
        if self.tree == {}:
            raise RuntimeError("The model has not been fitted yet.")

        X = np.asarray(X)
        if X.ndim == 1:  # Handle single record
            X = X.reshape(1, -1)

        predictions = [self._traverse_tree(x, self.tree) for x in X]
        return np.array(predictions)

    def _traverse_tree(self, x, node):
        """Traverse the tree for a single sample x.

        Args:
            x (array-like): The input features.
            node (dict): The current node in the decision tree.
        """
        # Check if it's a leaf node
        if "value" in node:
            return node["value"]

        # Check if node is valid (basic check)
        if "feature_idx" not in node or "threshold" not in node:
            # This might happen if the tree is malformed or empty
            # return NaN, assuming values are floats
            warnings.warn("Malformed node encountered during prediction.", stacklevel=2)
            return np.nan  # Or handle appropriately

        # Decide which branch to follow
        if x[node["feature_idx"]] <= node["threshold"]:
            # Potential issue: If left node is empty or malformed
            if isinstance(node.get("left"), dict):
                return self._traverse_tree(x, node["left"])
            else:
                # Handle cases where subtree might not be a dict (e.g., None if pruning happened badly)
                warnings.warn("Left node missing/malformed.", stacklevel=2)
                return np.nan  # Or a default value based on parent? Hard to say without more context.
        else:
            if isinstance(node.get("right"), dict):
                return self._traverse_tree(x, node["right"])
            else:
                warnings.warn("Right node missing/malformed.", stacklevel=2)
                return np.nan

    def _learn_recursive(self, indices, depth, sample_weight):
        """Recursive helper function for learning.

        Args:
            indices (array-like): The indices of the current node.
            depth (int): The current depth of the decision tree.
            sample_weight (array-like): The sample weights for the current node.
        """
        # Check termination conditions
        # 1. Max depth reached
        # 2. Node is pure (variance is 0) - checked implicitly by best_split gain > 0
        # 3. Not enough samples to split - checked by best_split returning None
        # 4. No split improves variance - checked by best_split gain > 0

        # Calculate leaf value first (will be used if termination condition met)
        leaf_value = self.utility.calculate_leaf_value(indices, sample_weight)

        # Base cases
        if depth >= self.max_depth:
            if self.verbose:
                print(
                    f"\tDepth limit reached at depth {depth}. Leaf value: {leaf_value}"
                )
            return {"value": leaf_value}

        if len(indices) < self.min_samples_split:
            if self.verbose:
                print(
                    f"\tMin samples limit reached ({len(indices)} < {self.min_samples_split}). Leaf value: {leaf_value}"
                )
            return {"value": leaf_value}

        # Find the best split for the current indices, considering sample weights
        split_info = self.utility.best_split(indices, sample_weight)

        # If no good split found (includes pure nodes, min_samples, no gain)
        if split_info is None:
            if self.verbose:
                print(
                    f"\tNo good split found at depth {depth}. Leaf value: {leaf_value}"
                )
            return {"value": leaf_value}

        if self.verbose:
            print(
                f"\tSplit at depth {depth}: Feature {split_info['feature_idx']} <= {split_info['threshold']:.2f}, Gain: {split_info['info_gain']:.4f}"
            )

        # Recursively build left and right subtrees
        left_subtree = self._learn_recursive(
            split_info["indices_left"], depth + 1, sample_weight
        )
        right_subtree = self._learn_recursive(
            split_info["indices_right"], depth + 1, sample_weight
        )

        # Return internal node structure
        return {
            "feature_idx": split_info["feature_idx"],
            "threshold": split_info["threshold"],
            "left": left_subtree,
            "right": right_subtree,
            "n_samples": len(indices),
            "info_gain": split_info["info_gain"],
        }
