import numpy as np

from sega_learn.nearest_neighbors import KNeighborsClassifier


class _Utils:
    """Utility class for data augmentation techniques.

    This class provides methods to check if classes are balanced and to separate samples by class.
    """

    @staticmethod
    def check_class_balance(y):
        """Checks the balance of classes in the given array.

        Args:
            y: (array-like) - Array of class labels.

        Returns:
            tuple: (int, np.ndarray) - A tuple containing the number of unique classes and an array of counts for each class.
        """
        unique, counts = np.unique(y, return_counts=True)
        return len(unique), counts

    @staticmethod
    def separate_samples(X, y):
        """Separates samples based on their class labels.

        Args:
            X: (np.ndarray) - The input data samples.
            y: (np.ndarray) - The class labels corresponding to the input data samples.

        Returns:
            dict: (dict) - A dictionary where the keys are unique class labels and the values are arrays of samples belonging to each class.
        """
        unique_classes = np.unique(y)
        separated_samples = {cls: X[y == cls] for cls in unique_classes}
        return separated_samples

    @staticmethod
    def get_class_distribution(y):
        """Gets the distribution of classes in the given array.

        Args:
            y: (array-like) - Array of class labels.

        Returns:
            dict: (dict) - A dictionary where the keys are unique class labels and the values are their respective counts.
        """
        unique, counts = np.unique(y, return_counts=True)
        return dict(zip(unique, counts))

    @staticmethod
    def get_minority_majority_classes(y):
        """Gets the minority and majority classes from the given array.

        Args:
            y: (array-like) - Array of class labels.

        Returns:
            tuple: (int, int) - A tuple containing the minority class and the majority class.
        """
        unique, counts = np.unique(y, return_counts=True)
        minority_class = unique[np.argmin(counts)]
        majority_class = unique[np.argmax(counts)]
        return minority_class, majority_class

    @staticmethod
    def validate_Xy(X, y):
        """Validates the input data and labels.

        Args:
            X: (array-like) - Feature matrix.
            y: (array-like) - Target vector.

        Raises:
            ValueError: If the shapes of X and y do not match or if they are not numpy arrays.
        """
        if len(X) != len(y):
            raise ValueError("The number of samples in X and y must be the same.")
        if not isinstance(X, np.ndarray):
            raise ValueError("X should be a numpy array.")
        if not isinstance(y, np.ndarray):
            raise ValueError("y should be a numpy array.")


class SMOTE:
    """Synthetic Minority Over-sampling Technique (SMOTE) for balancing class distribution.

    SMOTE generates synthetic samples for the minority class by interpolating between existing samples.
    This helps to create a more balanced dataset, which can improve the performance of machine learning models.

    Algorithm Steps:
        - Step 1: Identify the minority class and its samples.
        - Step 2: For each sample in the minority class, find its k nearest neighbors (using Euclidean distance.)
        - Step 3: Randomly select one or more of these neighbors.
        - Step 4: Create synthetic samples by interpolating between the original sample and the selected neighbors.
    """

    def __init__(self, random_state=None, k_neighbors=5):
        """Initializes the SMOTE with an optional random state and number of neighbors."""
        self.random_state = random_state
        self.k_neighbors = k_neighbors

    def fit_resample(self, X, y, force_equal=False):
        """Resamples the dataset to balance the class distribution by generating synthetic samples.

        Args:
            X: (array-like) - Feature matrix.
            y: (array-like) - Target vector.
            force_equal: (bool), optional - If True, resample until classes are equal (default is False).

        Returns:
            tuple: (np.ndarray, np.ndarray) - Resampled feature matrix and target vector.
        """
        np.random.seed(self.random_state)

        # Validate input data
        _Utils.validate_Xy(X, y)

        # Identify minority class
        minority_class, majority_class = _Utils.get_minority_majority_classes(y)

        # Check if classes are already balanced
        balance = _Utils.check_class_balance(y)
        if balance[1][0] == balance[1][1]:
            return X, y

        # Separate minority and majority class samples
        separated_samples = _Utils.separate_samples(X, y)
        X_minority = separated_samples[minority_class]
        X_majority = separated_samples[majority_class]
        y_minority = np.full(len(X_minority), minority_class)

        # Instantiate the KNNClassifier
        nn = KNeighborsClassifier(n_neighbors=self.k_neighbors + 1, one_hot_encode=True)
        nn.fit(X_minority, y_minority)
        nns = nn.get_distance_indices(X_minority)

        # Generate synthetic samples
        synthetic_samples = []
        target_samples = (
            len(X_majority) - len(X_minority) if force_equal else len(X_minority)
        )
        while len(synthetic_samples) < target_samples:
            for i in range(len(X_minority)):
                # Randomly select one of the k nearest neighbors
                nn_index = np.random.choice(nns[i])

                # Create synthetic sample by interpolating between the original sample and the selected neighbor
                diff = X_minority[nn_index] - X_minority[i]
                synthetic_sample = X_minority[i] + np.random.rand() * diff
                synthetic_samples.append(synthetic_sample)

                if len(synthetic_samples) >= target_samples:
                    break

        # Combine original and synthetic samples
        X_resampled = np.vstack([X, np.array(synthetic_samples)])
        y_resampled = np.hstack([y, np.full(len(synthetic_samples), minority_class)])

        return X_resampled, y_resampled


class RandomOverSampler:
    """Randomly over-sample the minority class by duplicating examples.

    This technique helps to balance the class distribution by randomly duplicating samples from the minority class.
    It is a simple yet effective method to address class imbalance in datasets.

    Algorithm Steps:
        - Step 1: Identify the minority class and its samples.
        - Step 2: Calculate the number of samples needed to balance the class distribution.
        - Step 3: Randomly select samples from the minority class with replacement.
        - Step 4: Duplicate the selected samples to create a balanced dataset.
    """

    def __init__(self, random_state=None):
        """Initializes the RandomOverSampler with an optional random state."""
        self.random_state = random_state

    def fit_resample(self, X, y):
        """Resamples the dataset to balance the class distribution by duplicating minority class samples.

        Args:
            X: (array-like) - Feature matrix.
            y: (array-like) - Target vector.

        Returns:
            tuple: (np.ndarray, np.ndarray) - Resampled feature matrix and target vector.
        """
        np.random.seed(self.random_state)

        # Validate input data
        _Utils.validate_Xy(X, y)

        # Identify minority class
        minority_class, majority_class = _Utils.get_minority_majority_classes(y)

        # Check if classes are already balanced
        balance = _Utils.check_class_balance(y)
        if balance[1][0] == balance[1][1]:
            return X, y

        # Separate minority and majority class samples
        separated_samples = _Utils.separate_samples(X, y)
        X_minority = separated_samples[minority_class]
        X_majority = separated_samples[majority_class]

        # Calculate number of samples to generate
        n_samples_to_generate = len(X_majority) - len(X_minority)

        # Randomly duplicate minority class samples
        indices = np.random.choice(
            len(X_minority), size=n_samples_to_generate, replace=True
        )
        synthetic_samples = X_minority[indices]

        # Combine original and synthetic samples
        X_resampled = np.vstack([X, synthetic_samples])
        y_resampled = np.hstack([y, np.full(len(synthetic_samples), minority_class)])

        return X_resampled, y_resampled


class RandomUnderSampler:
    """Randomly under-sample the majority class by removing examples.

    This technique helps to balance the class distribution by randomly removing samples from the majority class.
    It is a simple yet effective method to address class imbalance in datasets.

    Algorithm Steps:
        - Step 1: Identify the majority class and its samples.
        - Step 2: Calculate the number of samples to remove to balance the class distribution.
        - Step 3: Randomly select samples from the majority class without replacement.
        - Step 4: Remove the selected samples to create a balanced dataset.
    """

    def __init__(self, random_state=None):
        """Initializes the RandomUnderSampler with an optional random state."""
        self.random_state = random_state

    def fit_resample(self, X, y):
        """Resamples the dataset to balance the class distribution by removing majority class samples.

        Args:
            X: (array-like) - Feature matrix.
            y: (array-like) - Target vector.

        Returns:
            tuple: (np.ndarray, np.ndarray) - Resampled feature matrix and target vector.
        """
        np.random.seed(self.random_state)

        # Validate input data
        _Utils.validate_Xy(X, y)

        # Identify majority class
        minority_class, majority_class = _Utils.get_minority_majority_classes(y)

        # Check if classes are already balanced
        balance = _Utils.check_class_balance(y)
        if balance[1][0] == balance[1][1]:
            return X, y

        # Separate majority and minority class samples
        X_majority = X[y == majority_class]
        X_minority = X[y == minority_class]

        # Calculate number of samples to remove
        n_samples_to_remove = len(X_majority) - len(X_minority)

        # Randomly select majority class samples to remove
        indices = np.random.choice(
            len(X_majority), size=n_samples_to_remove, replace=False
        )
        X_majority_resampled = np.delete(X_majority, indices, axis=0)

        # Combine remaining majority samples with minority samples
        X_resampled = np.vstack([X_majority_resampled, X_minority])
        y_resampled = np.hstack(
            [
                np.full(len(X_majority_resampled), majority_class),
                np.full(len(X_minority), minority_class),
            ]
        )

        return X_resampled, y_resampled


class Augmenter:
    """General class for data augmentation techniques.

    This class allows for the application of multiple augmentation techniques in sequence.
    """

    def __init__(self, techniques, verbose=False):
        """Initializes the Augmenter with a list of techniques and verbosity option."""
        if not isinstance(techniques, list):
            raise ValueError("techniques should be a list of augmentation techniques.")
        for technique in techniques:
            if not hasattr(technique, "fit_resample"):
                raise ValueError("Each technique should have a fit_resample method.")

        self.techniques = techniques
        self.verbose = verbose

    def augment(self, X, y):
        """Applies multiple augmentation techniques in sequence.

        Args:
            X: (np.ndarray) - Feature matrix.
            y: (np.ndarray) - Target vector.

        Returns:
            tuple: (np.ndarray, np.ndarray) - Augmented feature matrix and target vector.
        """
        if self.verbose:
            print("Starting data augmentation...")

        for technique in self.techniques:
            # If classes are not balanced, apply the augmentation technique
            balance = _Utils.check_class_balance(y)
            if balance[1][0] == balance[1][1]:
                if self.verbose:
                    print(
                        f"   !!!!Classes are already balanced. Skipping {technique.__class__.__name__}"
                    )
                continue

            if self.verbose:
                print(f"   ...Applying {technique.__class__.__name__}")
            X, y = technique.fit_resample(X, y)

        if self.verbose:
            print("Data augmentation completed.")
        return X, y
