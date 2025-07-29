# Importing the required libraries

import numpy as np


class ClassifierTreeUtility:
    """Utility class for computing entropy, partitioning classes, and calculating information gain."""

    def __init__(self, min_samples_split=2):
        """Initialize the utility class."""
        self.min_samples_split = min_samples_split

    def entropy(self, class_y, sample_weight=None):
        """Computes the entropy for a given class.

        Args:
            class_y: (array-like) - The class labels.
            sample_weight: (array-like) - The sample weights (default: None).

        Returns:
            float: The entropy value.
        """
        n_samples = len(class_y)
        if n_samples == 0:
            return 0.0

        if sample_weight is None:
            # If no weights, use standard entropy calculation
            counts = np.bincount(class_y)
            probabilities = counts[counts > 0] / n_samples
            if (
                probabilities.size == 0
            ):  # Should not happen if n_samples > 0 but safety check
                return 0.0
            return -np.sum(
                probabilities * np.log2(probabilities + 1e-15)
            )  # Add epsilon for log2(0)
        else:
            # Ensure weights are numpy array
            sample_weight = np.asarray(sample_weight)
            if sample_weight.shape[0] != n_samples:
                raise ValueError("sample_weight must have the same length as class_y.")

            total_weight = np.sum(sample_weight)
            if total_weight <= 0:
                # If total weight is zero or less, cannot calculate weighted entropy meaningfully.
                # Fallback to unweighted entropy if samples exist.
                if n_samples > 0:
                    return self.entropy(
                        class_y, sample_weight=None
                    )  # Call unweighted version
                else:
                    return 0.0

            # Use weighted counts
            unique_classes, class_indices = np.unique(class_y, return_inverse=True)
            weighted_counts = np.bincount(class_indices, weights=sample_weight)

            # Calculate probabilities based on the *total weight of the current subset*
            probabilities = weighted_counts[weighted_counts > 0] / total_weight
            if probabilities.size == 0:
                return 0.0

            # Calculate weighted entropy
            entropy_val = -np.sum(
                probabilities * np.log2(probabilities + 1e-15)
            )  # Add epsilon
            return entropy_val

    def partition_classes(self, X, y, split_attribute, split_val, sample_weight=None):
        """Partitions the dataset into two subsets based on a given split attribute and value.

        Args:
            X: (array-like) - The input features.
            y: (array-like) - The target labels.
            split_attribute: (int) - The index of the attribute to split on.
            split_val: (float) - The value to split the attribute on.
            sample_weight: (array-like) - The sample weights (default: None).

        Returns:
            X_left:  (array-like) - The subset of input features where the split attribute is less than or equal to the split value.
            X_right: (array-like) - The subset of input features where the split attribute is greater than the split value.
            y_left:  (array-like) - The subset of target labels corresponding to X_left.
            y_right: (array-like) - The subset of target labels corresponding to X_right.
        """
        # Convert X and y to NumPy arrays for faster computation
        X = np.array(X)
        y = np.array(y)

        if X.ndim == 1:  # If X has only one feature
            X = X.reshape(-1, 1)  # Convert to a 2D array with one column

        # Use NumPy boolean indexing for partitioning
        # X_left  contains rows where the split attribute is less than or equal to the split value
        # X_right contains rows where the split attribute is greater than the split value
        # y_left  contains target labels corresponding to X_left
        # y_right contains target labels corresponding to X_right
        mask = X[:, split_attribute] <= split_val
        X_left = X[mask]
        X_right = X[~mask]
        y_left = y[mask]
        y_right = y[~mask]

        # Partition weights
        if sample_weight is not None:
            sample_weight = np.array(
                sample_weight
            )  # Ensure sample_weight is a NumPy array
            sample_weight_left = sample_weight[mask]
            sample_weight_right = sample_weight[~mask]
            return (
                X_left,
                X_right,
                y_left,
                y_right,
                sample_weight_left,
                sample_weight_right,
            )

        else:
            return X_left, X_right, y_left, y_right, None, None

    def information_gain(
        self, previous_y, current_y, sample_weight_prev=None, sample_weight_current=None
    ):
        """Calculates the information gain between the previous and current values of y.

        Args:
            previous_y: (array-like) - The previous values of y.
            current_y: (array-like) - The current values of y.
            sample_weight_prev: (array-like) - The sample weights for the previous y values (default: None).
            sample_weight_current: (array-like) - The sample weights for the current y values (default: None).

        Returns:
            float: The information gain between the previous and current values of y.
        """
        n_samples_prev = len(previous_y)
        if n_samples_prev == 0:
            return 0.0

        # --- Calculate entropy of the parent node ---
        if sample_weight_prev is None:
            sample_weight_prev = np.ones(n_samples_prev)

        total_weight_prev = np.sum(sample_weight_prev)
        # Calculate parent entropy using the correct weights
        entropy_prev = self.entropy(previous_y, sample_weight_prev)

        # --- Calculate weighted average entropy of the children nodes ---
        weighted_entropy_current = 0.0

        if sample_weight_current is None:
            # Create default weights if none provided (should match children sizes)
            sample_weight_current = [
                np.ones(len(subset)) if len(subset) > 0 else np.array([])
                for subset in current_y
            ]
        elif not isinstance(sample_weight_current, list) or len(
            sample_weight_current
        ) != len(current_y):
            raise ValueError(
                "sample_weight_current must be a list of arrays matching current_y structure."
            )

        # Use total weight of parent for weighting factor denominator
        if total_weight_prev <= 0:
            # If parent total weight is zero, gain cannot be calculated meaningfully based on weights
            # Fallback to unweighted calculation if samples exist
            if n_samples_prev > 0:
                weighted_entropy_current = 0.0
                for subset_y in current_y:
                    if len(subset_y) > 0:
                        weighting_factor = len(subset_y) / n_samples_prev
                        weighted_entropy_current += weighting_factor * self.entropy(
                            subset_y
                        )  # Unweighted child entropy
                return (
                    entropy_prev - weighted_entropy_current
                )  # Gain based on unweighted entropy
            else:
                return 0.0  # No gain if parent node was effectively empty

        # Calculate weighted entropy sum of children
        for i, subset_y in enumerate(current_y):
            if len(subset_y) > 0:
                subset_weights = sample_weight_current[i]
                subset_total_weight = np.sum(subset_weights)

                if subset_total_weight > 0:
                    # Weight factor is proportion of total parent weight
                    weighting_factor = subset_total_weight / total_weight_prev
                    # Child entropy uses its own weights
                    child_entropy = self.entropy(subset_y, subset_weights)
                    weighted_entropy_current += weighting_factor * child_entropy
                # If child weight is zero, its contribution to weighted entropy is zero

        info_gain = entropy_prev - weighted_entropy_current
        # Ensure info_gain is not negative due to floating point issues
        return max(0.0, info_gain)

    def best_split(self, X, y, sample_weight=None):
        """Finds the best attribute and value to split the data based on information gain.

        Args:
            X: (array-like) - The input features.
            y: (array-like) - The target variable.
            sample_weight: (array-like) - The sample weights (default: None).

        Returns:
            dict: A dictionary containing the best split attribute, split value, left and right subsets of X and y,
                  and the information gain achieved by the split.
        """
        # ----- Input Validation and Setup -----
        if not isinstance(X, (list, np.ndarray)) or not isinstance(
            y, (list, np.ndarray)
        ):
            raise TypeError("X and y must be lists or NumPy arrays.")

        X = np.asarray(X) if not isinstance(X, np.ndarray) else X
        y = (
            np.asarray(y).astype(int)
            if not isinstance(y, np.ndarray)
            else y.astype(int)
        )  # Ensure y is int

        n_samples = X.shape[0]

        if sample_weight is None:
            sample_weight = np.ones(n_samples)
        else:
            sample_weight = np.asarray(sample_weight, dtype=np.float64)
            if sample_weight.shape[0] != n_samples:
                raise ValueError("sample_weight must have the same length as X and y.")

        current_total_weight = np.sum(sample_weight)

        # ----- Base Cases for Leaf Node -----
        unique_classes, class_indices = np.unique(y, return_inverse=True)

        # Calculate weighted majority class (needed if returning leaf)
        if current_total_weight > 0:
            weighted_counts = np.bincount(class_indices, weights=sample_weight)
            majority_label = unique_classes[np.argmax(weighted_counts)]
        elif n_samples > 0:  # Fallback if weights are zero
            counts = np.bincount(y)
            majority_label = np.argmax(counts)
        else:  # Empty node
            return None  # Cannot determine label or split

        if len(unique_classes) <= 1:  # Pure node
            return {"label": majority_label}
        if n_samples < self.min_samples_split:  # Min samples split condition
            return {"label": majority_label}

        # ----- Find Best Split -----
        best_info_gain = (
            -np.inf
        )  # Use negative infinity to ensure any positive gain is better
        best_split = None

        num_features_total = X.shape[1]
        if num_features_total == 0:  # No features to split on
            return {"label": majority_label}

        # Randomly select a subset of features (sqrt strategy)
        num_features_to_consider = max(1, int(np.sqrt(num_features_total)))
        if num_features_to_consider > num_features_total:
            num_features_to_consider = num_features_total

        selected_attributes = np.random.choice(
            num_features_total, size=num_features_to_consider, replace=False
        )

        for split_attribute in selected_attributes:
            feature_values = X[:, split_attribute]
            potential_split_values = np.unique(
                np.percentile(feature_values, [25, 50, 75])
            )

            for split_val in potential_split_values:
                # Partition using indices for efficiency is better if X is large, but direct partitioning is simpler here
                (X_left, X_right, y_left, y_right, sw_left, sw_right) = (
                    self.partition_classes(
                        X,
                        y,
                        split_attribute,
                        split_val,
                        sample_weight,  # Pass original weights
                    )
                )

                # Skip if split doesn't create two non-empty children
                if len(y_left) == 0 or len(y_right) == 0:
                    continue

                # Calculate information gain using original weights for parent and partitioned weights for children
                info_gain = self.information_gain(
                    y, [y_left, y_right], sample_weight, [sw_left, sw_right]
                )

                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                    # Store the actual partitions resulting from the split
                    best_split = {
                        "split_attribute": split_attribute,
                        "split_val": split_val,
                        "X_left": X_left,  # Store the actual partitioned data
                        "X_right": X_right,
                        "y_left": y_left,
                        "y_right": y_right,
                        "sample_weight_left": sw_left,  # Store partitioned weights
                        "sample_weight_right": sw_right,
                        "info_gain": info_gain,
                    }

        # If no split provided positive gain, return leaf node
        if best_split is None or best_info_gain <= 1e-9:  # Use tolerance
            return {"label": majority_label}

        return best_split


class ClassifierTree:
    """A class representing a decision tree.

    Args:
        max_depth: (int) - The maximum depth of the decision tree.

    Methods:
        learn(X, y, par_node={}, depth=0): Builds the decision tree based on the given training data.
        classify(record): Classifies a record using the decision tree.
    """

    def __init__(self, max_depth=5, min_samples_split=2):
        """Initializes the ClassifierTree with a maximum depth."""
        self.tree = {}  # Initialize the tree as an empty dictionary
        self.max_depth = max_depth  # Set the maximum depth of the tree
        self.min_samples_split = min_samples_split  # Minimum samples required to split
        self.info_gain = []  # Initialize the information gain list
        self.utility = ClassifierTreeUtility(min_samples_split=min_samples_split)

    def fit(self, X, y, sample_weight=None):
        """Fits the decision tree to the training data.

        Args:
            X: (array-like) - The input features.
            y: (array-like) - The target labels.
            sample_weight: (array-like) - The sample weights (default: None).
        """
        # Ensure y is integer type for bincount
        y = np.asarray(y).astype(int)
        self.tree = self.learn(X, y, sample_weight=sample_weight)
        return self.tree

    def learn(self, X, y, par_node=None, depth=0, sample_weight=None):
        """Builds the decision tree based on the given training data.

        Args:
            X: (array-like) - The input features.
            y: (array-like) - The target labels.
            par_node: (dict) - The parent node of the current subtree (default: {}).
            depth: (int) - The current depth of the subtree (default: 0).
            sample_weight: (array-like) - The sample weights (default: None).

        Returns:
            dict: The learned decision tree.
        """
        # --- Input Conversion and Validation ---
        if not isinstance(X, (list, np.ndarray)) or not isinstance(
            y, (list, np.ndarray)
        ):
            raise TypeError("X and y must be lists or NumPy arrays.")

        X = np.asarray(X)
        y = np.asarray(y).astype(int)  # Ensure y is int

        n_samples = X.shape[0]

        if sample_weight is None:
            sample_weight = np.ones(n_samples)
        else:
            sample_weight = np.asarray(sample_weight, dtype=np.float64)
            if sample_weight.shape[0] != n_samples:
                raise ValueError("sample_weight length mismatch.")

        # Check for empty node
        if n_samples == 0:
            return {}  # Represent an empty node/branch

        # --- Calculate Majority Label (needed for leaf nodes) ---
        current_total_weight = np.sum(sample_weight)
        unique_classes, class_indices = np.unique(y, return_inverse=True)

        if current_total_weight > 0:
            weighted_counts = np.bincount(class_indices, weights=sample_weight)
            majority_label = unique_classes[np.argmax(weighted_counts)]
        elif n_samples > 0:  # Fallback if all weights are zero
            counts = np.bincount(y)
            majority_label = np.argmax(counts)
        else:
            # Should not happen if n_samples == 0 check above works
            return {}

        # --- Base Cases (Termination Conditions) ---
        # 1. Pure node (only one class left)
        if len(unique_classes) <= 1:
            return {
                "label": majority_label
            }  # Use majority label (which is the only label)

        # 2. Max depth reached
        if depth >= self.max_depth:
            return {"label": majority_label}

        # 3. Minimum samples for split not met
        if n_samples < self.min_samples_split:  # Use the parameter here
            return {"label": majority_label}

        # --- Find Best Split ---
        # Pass current sample weights to best_split
        best_split = self.utility.best_split(X, y, sample_weight)

        # 4. No beneficial split found (includes pure nodes implicitly, or min_samples_split check inside best_split)
        if (
            best_split is None
            or "label" in best_split
            or best_split["info_gain"] <= 1e-9
        ):
            return {"label": majority_label}

        # --- Recursive Step ---
        # Build subtrees using the partitioned data and weights from best_split
        left_tree = self.learn(
            best_split["X_left"],
            best_split["y_left"],
            depth=depth + 1,
            sample_weight=best_split["sample_weight_left"],
        )
        right_tree = self.learn(
            best_split["X_right"],
            best_split["y_right"],
            depth=depth + 1,
            sample_weight=best_split["sample_weight_right"],
        )

        # Return internal node structure
        return {
            "split_attribute": best_split["split_attribute"],
            "split_val": best_split["split_val"],
            "left": left_tree,
            "right": right_tree,
            # Optionally store info gain or node stats if needed
            # "info_gain": best_split["info_gain"],
            # "n_samples": n_samples
        }

    @staticmethod
    def classify(tree, record):
        """Classifies a given record using the decision tree.

        Args:
            tree: (dict) - The decision tree.
            record: (dict) - A dictionary representing the record to be classified.

        Returns:
            The label assigned to the record based on the decision tree.
        """
        # If tree is empty return None
        if tree is None or tree == {}:
            return None

        if "label" in tree:
            return tree["label"]

        if record[tree["split_attribute"]] <= tree["split_val"]:
            return ClassifierTree.classify(tree["left"], record)
        else:
            return ClassifierTree.classify(tree["right"], record)

    def predict(self, X):
        """Predicts the labels for a given set of records using the decision tree.

        Args:
            X: (array-like) - The input features.

        Returns:
            list: A list of predicted labels for each record.
        """
        if self.tree is None or self.tree == {}:
            return None

        predictions = []

        for record in X:
            prediction = ClassifierTree.classify(self.tree, record)
            predictions.append(prediction)

        return predictions

    def predict_proba(self, X):
        """Predicts the probabilities for a given set of records using the decision tree.

        Args:
            X: (array-like) - The input features.

        Returns:
            list: A list of dictionaries where each dictionary represents the probability distribution
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

        if self.tree is None or self.tree == {}:
            return None

        probabilities = []

        for record in X:
            prob = traverse_tree(self.tree, record)
            probabilities.append(prob)

        return probabilities
