import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.trees import *
from sega_learn.trees.randomForestClassifier import _classify_oob
from sega_learn.utils import make_classification
from tests.utils import BaseTest


class TestClassifierTreeUtility(BaseTest):
    """Set up the ClassifierTreeUtility instance for testing."""

    @classmethod
    def setUpClass(cls):
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Classifier Tree Utility", end="", flush=True)

    def setUp(self):
        """Set up the ClassifierTreeUtility instance for testing."""
        self.utility = ClassifierTreeUtility()

    def test_init(self):
        """Tests the initialization of the ClassifierTreeUtility class."""
        self.assertIsInstance(self.utility, ClassifierTreeUtility)
        self.assertEqual(self.utility.min_samples_split, 2)

    def test_entropy(self):
        """Tests the entropy method of the ClassifierTreeUtility class."""
        class_y = [0, 0, 1, 1, 1, 1]
        expected_entropy = (
            0.9182958340544896  # Expected entropy value (calculated manually)
        )
        self.assertAlmostEqual(
            self.utility.entropy(class_y), expected_entropy, places=5
        )

    def test_entropy_with_single_class(self):
        """Tests the entropy method with a single class."""
        class_y = [0, 0, 0, 0, 0, 0]
        expected_entropy = 0.0
        self.assertAlmostEqual(
            self.utility.entropy(class_y), expected_entropy, places=5
        )

    def test_entropy_with_empty_list(self):
        """Tests the entropy method with an empty list."""
        class_y = []
        expected_entropy = 0.0
        self.assertAlmostEqual(
            self.utility.entropy(class_y), expected_entropy, places=5
        )

    def test_entropy_with_single_element(self):
        """Tests the entropy method with a single element."""
        class_y = [1]
        expected_entropy = 0.0
        self.assertAlmostEqual(
            self.utility.entropy(class_y), expected_entropy, places=5
        )

    def test_entropy_with_two_classes(self):
        """Tests the entropy method with two classes."""
        class_y = [0, 1, 0, 1, 0, 1]
        expected_entropy = 1.0
        self.assertAlmostEqual(
            self.utility.entropy(class_y), expected_entropy, places=5
        )

    def test_entropy_with_sample_weights(self):
        """Tests the entropy method with sample weights."""
        class_y = [0, 1, 0, 1, 0, 1]
        sample_weights = [1, 2, 1, 2, 1, 2]
        expected_entropy = 0.9182958340544867  # Calculated manually
        self.assertAlmostEqual(
            self.utility.entropy(class_y, sample_weights), expected_entropy, places=5
        )

    def test_entropy_with_sample_weights_empty(self):
        """Tests the entropy method with empty sample weights."""
        class_y = [0, 1, 0, 1, 0, 1]
        sample_weights = []
        with self.assertRaises(ValueError):
            self.utility.entropy(class_y, sample_weights)

    def test_entropy_with_sample_weights_different_length(self):
        """Tests the entropy method with sample weights of different length."""
        class_y = [0, 1, 0, 1, 0, 1]
        sample_weights = [1, 2]
        with self.assertRaises(ValueError):
            self.utility.entropy(class_y, sample_weights)

    def test_entropy_with_sample_weights_single_class(self):
        """Tests the entropy method with sample weights for a single class."""
        class_y = [0, 0, 0, 0, 0, 0]
        sample_weights = [1, 2, 3, 4, 5, 6]
        expected_entropy = 0.0
        self.assertAlmostEqual(
            self.utility.entropy(class_y, sample_weights), expected_entropy, places=5
        )

    def test_entropy_with_sample_weights_single_element(self):
        """Tests the entropy method with sample weights for a single element."""
        class_y = [1]
        sample_weights = [1]
        expected_entropy = 0.0
        self.assertAlmostEqual(
            self.utility.entropy(class_y, sample_weights), expected_entropy, places=5
        )

    def test_partition_classes(self):
        """Tests the partition_classes method of the ClassifierTreeUtility class."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 1]
        split_attribute = 0
        split_val = 2.5
        X_left, X_right, y_left, y_right, sw_left, sw_right = (
            self.utility.partition_classes(X, y, split_attribute, split_val)
        )
        self.assertEqual(X_left.tolist(), [[2, 3], [1, 2]])
        self.assertEqual(X_right.tolist(), [[3, 4], [5, 6]])
        self.assertEqual(y_left.tolist(), [0, 1])
        self.assertEqual(y_right.tolist(), [0, 1])

    def test_partition_classes_with_sample_weights(self):
        """Tests the partition_classes method with sample weights."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 1]
        sample_weights = [1, 2, 3, 4]
        split_attribute = 0
        split_val = 2.5
        X_left, X_right, y_left, y_right, sw_left, sw_right = (
            self.utility.partition_classes(
                X, y, split_attribute, split_val, sample_weights
            )
        )
        self.assertEqual(sw_left.tolist(), [1, 2])
        self.assertEqual(sw_right.tolist(), [3, 4])

    def test_partition_classes_with_empty_sample_weights(self):
        """Tests the partition_classes method with empty sample weights."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 1]
        sample_weights = []
        split_attribute = 0
        split_val = 2.5
        with self.assertRaises((ValueError, IndexError)):
            self.utility.partition_classes(
                X, y, split_attribute, split_val, sample_weights
            )

    def test_partition_classes_with_different_length_sample_weights(self):
        """Tests the partition_classes method with sample weights of different length."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 1]
        sample_weights = [1, 2]
        split_attribute = 0
        split_val = 2.5
        with self.assertRaises((ValueError, IndexError)):
            self.utility.partition_classes(
                X, y, split_attribute, split_val, sample_weights
            )

    def test_information_gain(self):
        """Tests the information_gain method of the ClassifierTreeUtility class."""
        previous_y = [0, 0, 1, 1, 1, 1]
        current_y = [[0, 0], [1, 1, 1, 1]]
        expected_info_gain = (
            0.9182958340544896  # Expected information gain value (calculated manually)
        )
        self.assertAlmostEqual(
            self.utility.information_gain(previous_y, current_y),
            expected_info_gain,
            places=5,
        )

    def test_information_gain_with_sample_weights(self):
        """Tests the information_gain method with sample weights."""
        previous_y = [0, 0, 1, 1, 1, 1]
        current_y = [[0, 0], [1, 1, 1, 1]]
        sample_weights = [1, 2, 3, 4, 5, 6]
        expected_info_gain = (
            0.5916727785823249  # Expected information gain value (calculated manually)
        )
        self.assertAlmostEqual(
            self.utility.information_gain(previous_y, current_y, sample_weights),
            expected_info_gain,
            places=5,
        )

    def test_information_gain_with_none_sample_weights(self):
        """Tests the information_gain method with None sample weights."""
        previous_y = [0, 0, 1, 1, 1, 1]
        current_y = [[0, 0], [1, 1, 1, 1]]
        expected_info_gain = (
            0.9182958340544896  # Expected information gain value (calculated manually)
        )
        self.assertAlmostEqual(
            self.utility.information_gain(previous_y, current_y),
            expected_info_gain,
            places=5,
        )

    def test_information_gain_with_empty_sample_weights(self):
        """Tests the information_gain method with empty sample weights."""
        previous_y = [0, 0, 1, 1, 1, 1]
        current_y = [[0, 0], [1, 1, 1, 1]]
        sample_weights = []
        with self.assertRaises((ValueError, IndexError)):
            self.utility.information_gain(previous_y, current_y, sample_weights)

    def test_information_gain_with_different_length_sample_weights(self):
        """Tests the information_gain method with sample weights of different length."""
        previous_y = [0, 0, 1, 1, 1, 1]
        current_y = [[0, 0], [1, 1, 1, 1]]
        sample_weights = [1, 2]
        with self.assertRaises((ValueError, IndexError)):
            self.utility.information_gain(previous_y, current_y, sample_weights)

    def test_best_split(self):
        """Tests the best_split method of the ClassifierTreeUtility class."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 0]
        best_split = self.utility.best_split(X, y)

        self.assertIn("split_attribute", best_split)
        self.assertIn("split_val", best_split)
        self.assertIn("X_left", best_split)
        self.assertIn("X_right", best_split)
        self.assertIn("y_left", best_split)
        self.assertIn("y_right", best_split)
        self.assertIn("info_gain", best_split)

        self.assertIsInstance(best_split["split_attribute"], (int, np.integer))
        self.assertIsInstance(
            best_split["split_val"], (int, float, np.integer, np.float64)
        )
        self.assertIsInstance(best_split["X_left"], np.ndarray)
        self.assertIsInstance(best_split["X_right"], np.ndarray)
        self.assertIsInstance(best_split["y_left"], np.ndarray)
        self.assertIsInstance(best_split["y_right"], np.ndarray)
        self.assertIsInstance(best_split["info_gain"], float)

    def test_best_split_with_sample_weights(self):
        """Tests the best_split method with sample weights."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 0]
        sample_weights = [1, 2, 3, 4]
        best_split = self.utility.best_split(X, y, sample_weight=sample_weights)

        self.assertIn("split_attribute", best_split)
        self.assertIn("split_val", best_split)
        self.assertIn("X_left", best_split)
        self.assertIn("X_right", best_split)
        self.assertIn("y_left", best_split)
        self.assertIn("y_right", best_split)
        self.assertIn("info_gain", best_split)

    def test_best_split_with_none_sample_weights(self):
        """Tests the best_split method with None sample weights."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 0]
        best_split = self.utility.best_split(X, y, sample_weight=None)

        self.assertIn("split_attribute", best_split)
        self.assertIn("split_val", best_split)
        self.assertIn("X_left", best_split)
        self.assertIn("X_right", best_split)
        self.assertIn("y_left", best_split)
        self.assertIn("y_right", best_split)
        self.assertIn("info_gain", best_split)

    def test_best_split_with_empty_sample_weights(self):
        """Tests the best_split method with empty sample weights."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 0]
        sample_weights = []
        with self.assertRaises((ValueError, IndexError)):
            self.utility.best_split(X, y, sample_weight=sample_weights)

    def test_best_split_with_different_length_sample_weights(self):
        """Tests the best_split method with sample weights of different length."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 0]
        sample_weights = [1, 2]
        with self.assertRaises((ValueError, IndexError)):
            self.utility.best_split(X, y, sample_weight=sample_weights)

    def test_best_split_with_min_samples_split(self):
        """Tests the best_split method with min_samples_split."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 0]
        min_samples_split = 2
        self.utility.min_samples_split = min_samples_split
        best_split = self.utility.best_split(X, y)

        self.assertIn("split_attribute", best_split)
        self.assertIn("split_val", best_split)
        self.assertIn("X_left", best_split)
        self.assertIn("X_right", best_split)
        self.assertIn("y_left", best_split)
        self.assertIn("y_right", best_split)
        self.assertIn("info_gain", best_split)

    def test_best_split_with_3_min_samples_split(self):
        """Tests the best_split method with min_samples_split set to 3."""
        X = [[2, 3], [1, 2], [3, 4], [5, 6]]
        y = [0, 1, 0, 0]
        min_samples_split = 3
        self.utility.min_samples_split = min_samples_split
        best_split = self.utility.best_split(X, y)

        self.assertIn("split_attribute", best_split)
        self.assertIn("split_val", best_split)
        self.assertIn("X_left", best_split)
        self.assertIn("X_right", best_split)
        self.assertIn("y_left", best_split)
        self.assertIn("y_right", best_split)
        self.assertIn("info_gain", best_split)

    def test_entropy_empty(self):
        """Test entropy with an empty class list."""
        class_y = []
        expected_entropy = 0.0
        self.assertAlmostEqual(
            self.utility.entropy(class_y), expected_entropy, places=5
        )

    def test_entropy_single_element(self):
        """Test entropy with a single element."""
        class_y = [1]
        expected_entropy = 0.0
        self.assertAlmostEqual(
            self.utility.entropy(class_y), expected_entropy, places=5
        )

    def test_partition_classes_empty(self):
        """Test partition_classes with empty inputs."""
        X = []
        y = []
        split_attribute = 0
        split_val = 0.5
        X_left, X_right, y_left, y_right, sw_left, sw_right = (
            self.utility.partition_classes(X, y, split_attribute, split_val)
        )
        self.assertEqual(len(X_left), 0)
        self.assertEqual(len(X_right), 0)
        self.assertEqual(len(y_left), 0)
        self.assertEqual(len(y_right), 0)

    def test_partition_classes_single_element(self):
        """Test partition_classes with a single element."""
        X = [[1, 2]]
        y = [1]
        split_attribute = 0
        split_val = 1.5
        X_left, X_right, y_left, y_right, sw_left, sw_right = (
            self.utility.partition_classes(X, y, split_attribute, split_val)
        )
        self.assertEqual(X_left.tolist(), [[1, 2]])
        self.assertEqual(X_right.tolist(), [])
        self.assertEqual(y_left.tolist(), [1])
        self.assertEqual(y_right.tolist(), [])

    def test_information_gain_empty(self):
        """Test information_gain with empty inputs."""
        previous_y = []
        current_y = [[], []]
        expected_info_gain = 0.0
        self.assertAlmostEqual(
            self.utility.information_gain(previous_y, current_y),
            expected_info_gain,
            places=5,
        )

    def test_information_gain_no_split(self):
        """Test information_gain when no split occurs."""
        previous_y = [1, 1, 1, 1]
        current_y = [[1, 1, 1, 1], []]
        expected_info_gain = 0.0
        self.assertAlmostEqual(
            self.utility.information_gain(previous_y, current_y),
            expected_info_gain,
            places=5,
        )

    def test_best_split_empty(self):
        """Test best_split with empty inputs."""
        X = []
        y = []
        best_split = self.utility.best_split(X, y)
        # Return None if no split found
        self.assertIsNone(best_split)

    def test_best_split_single_element(self):
        """Test best_split with a single element."""
        X = [[1, 2]]
        y = [1]
        best_split = self.utility.best_split(X, y)
        # if if n_samples < 2 or current_total_weight <= 0 then returns leaf node
        self.assertEqual(best_split["label"], 1)


class TestClassifierTree(BaseTest):
    """Set up the ClassifierTree instance for testing."""

    @classmethod
    def setUpClass(cls):
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Classifier Tree", end="", flush=True)

    def setUp(self):
        """Set up the ClassifierTree instance for testing."""
        self.tree = ClassifierTree(max_depth=5)
        self.X, self.y = make_classification(n_samples=100, n_features=5, n_classes=2)

    def test_init(self):
        """Tests the initialization of the ClassifierTree class."""
        self.assertEqual(self.tree.max_depth, 5)
        self.assertEqual(self.tree.min_samples_split, 2)
        self.assertDictEqual(self.tree.tree, {})
        self.assertIsInstance(self.tree.utility, ClassifierTreeUtility)

    def test_learn(self):
        """Tests the learn method of the ClassifierTree class."""
        self.tree.learn(self.X, self.y)
        self.assertIsInstance(self.tree.tree, dict)

    def test_learn_with_sample_weights(self):
        """Tests the learn method with sample weights."""
        sample_weights = np.random.rand(len(self.X))
        self.tree.learn(self.X, self.y, sample_weight=sample_weights)
        self.assertIsInstance(self.tree.tree, dict)

    def test_learn_with_none_sample_weights(self):
        """Tests the learn method with None sample weights."""
        self.tree.learn(self.X, self.y, sample_weight=None)
        self.assertIsInstance(self.tree.tree, dict)

    def test_learn_with_empty_sample_weights(self):
        """Tests the learn method with empty sample weights."""
        sample_weights = []
        with self.assertRaises((ValueError, IndexError)):
            self.tree.learn(self.X, self.y, sample_weight=sample_weights)

    def test_learn_with_different_length_sample_weights(self):
        """Tests the learn method with sample weights of different length."""
        sample_weights = np.random.rand(len(self.X) - 1)
        with self.assertRaises((ValueError, IndexError)):
            self.tree.learn(self.X, self.y, sample_weight=sample_weights)

    def test_learn_min_samples_split(self):
        """Tests the learn method with min_samples_split."""
        self.tree.min_samples_split = 3
        self.tree.learn(self.X, self.y)
        self.assertIsInstance(self.tree.tree, dict)

    def test_learn_min_samples_split_not_enough_samples(self):
        """Tests the learn method with min_samples_split not enough samples."""
        self.tree.min_samples_split = 10
        self.tree.learn(self.X, self.y)
        self.assertIsInstance(self.tree.tree, dict)

    def test_learn_single_value(self):
        """Tests the learn method with a single value."""
        X = [[1, 2], [1, 2], [1, 2]]
        y = [0, 0, 0]
        self.tree.learn(X, y)
        self.assertEqual(self.tree.tree, {})

    def test_learn_bad_type(self):
        """Tests the learn method with a bad type."""
        X = "not a list"
        y = "not a list"
        with self.assertRaises(TypeError):
            self.tree.learn(X, y)

    def test_learn_empty_dataset(self):
        """Test learning with an empty dataset."""
        X = []
        y = []
        tree = self.tree.learn(X, y)
        self.assertEqual(tree, {})

    def test_learn_single_data_point(self):
        """Test learning with a single data point."""
        X = [[1, 2, 3]]
        y = [1]
        tree = self.tree.learn(X, y)
        self.assertEqual(tree, {"label": 1})

    def test_learn_pure_labels(self):
        """Test learning when all labels are the same."""
        X = [[1, 2], [3, 4], [5, 6]]
        y = [1, 1, 1]
        tree = self.tree.learn(X, y)
        self.assertEqual(tree, {"label": 1})

    def test_learn_max_depth(self):
        """Test learning when the maximum depth is reached."""
        X = [[1, 2], [3, 4], [5, 6], [7, 8]]
        y = [0, 1, 0, 1]
        self.tree.max_depth = 1
        tree = self.tree.learn(X, y)
        self.assertIn("split_attribute", tree)
        self.assertIn("split_val", tree)

    def test_classify_empty_tree(self):
        """Test classification with an empty tree."""
        record = [1, 2, 3]
        result = self.tree.classify({}, record)
        self.assertIsNone(result)

    def test_classify_single_node_tree(self):
        """Test classification with a single-node tree."""
        tree = {"label": 1}
        record = [1, 2, 3]
        result = self.tree.classify(tree, record)
        self.assertEqual(result, 1)

    def test_classify_with_split(self):
        """Test classification with a tree containing a split."""
        tree = {
            "split_attribute": 0,
            "split_val": 2.5,
            "left": {"label": 0},
            "right": {"label": 1},
        }
        record_left = [2, 3]
        record_right = [3, 4]
        result_left = self.tree.classify(tree, record_left)
        result_right = self.tree.classify(tree, record_right)
        self.assertEqual(result_left, 0)
        self.assertEqual(result_right, 1)


class TestRandomForestClassifier(BaseTest):
    """Set up the RandomForestClassifier instance for testing."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the Index class before each test method is run."""
        print("\nTesting Random Forest Classifier", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the RandomForestClassifier instance for testing."""
        X, y = make_classification(n_samples=100, n_features=5, n_classes=2)
        self.rf = RandomForestClassifier(
            X=X, y=y, max_depth=10, n_estimators=10, random_seed=0, n_jobs=1
        )

    def test_init(self):
        """Tests the initialization of the RandomForestClassifier class."""
        self.assertEqual(self.rf.max_depth, 10)
        self.assertEqual(self.rf.n_estimators, 10)
        self.assertIsInstance(self.rf.trees, list)

    def test_fitting(self):
        """Tests the fitting method of the RandomForestClassifier class."""
        self.rf.fit()
        for tree in self.rf.trees:
            self.assertIsInstance(tree, dict)

    def test_fitting_single_value(self):
        """Tests the fitting method with a single value."""
        _X = [[1, 2, 3]]
        self.rf.fit()
        for tree in self.rf.trees:
            self.assertIn("split_attribute", tree)

    def test_voting(self):
        """Tests the voting method of the RandomForestClassifier class."""
        self.rf.fit()
        predictions = self.rf.predict(self.rf.X)
        self.assertEqual(len(predictions), len(self.rf.X))
        self.assertIsInstance(predictions, list)

    def test_voting_single_value(self):
        """Tests the voting method with a single value."""
        X = [[1, 2, 3, 4, 5]]
        self.rf.fit()
        predictions = self.rf.predict(X)
        self.assertEqual(len(predictions), 1)
        self.assertIsInstance(predictions, list)

    def test_fit(self):
        """Tests the fit method of the RandomForestClassifier class."""
        self.rf.fit(verbose=False)
        self.assertGreaterEqual(self.rf.accuracy, 0.0)
        self.assertLessEqual(self.rf.accuracy, 1.0)

    def test_fit_single_data_point(self):
        """Test fitting the RandomForestClassifier with a single data point."""
        X_single = np.random.rand(1, 5)  # Single sample, 5 features
        y_single = np.array([1])  # Single label
        self.rf.fit(X_single, y_single)
        self.assertEqual(len(self.rf.trees), 10)  # Ensure 10 trees are trained

    def test_fit_empty_dataset(self):
        """Test fitting the RandomForestClassifier with an empty dataset."""
        X_empty = np.empty((0, 5))  # No samples, 5 features
        y_empty = np.empty((0,))
        with self.assertRaises(ValueError):
            self.rf.fit(X_empty, y_empty)

    def test_fit_no_features(self):
        """Test fitting the RandomForestClassifier with no features."""
        X = np.empty((10, 0))  # 10 samples, 0 features
        y = np.random.randint(0, 2, size=10)
        with self.assertRaises(ValueError):
            self.rf.fit(X, y)

    def test_fit_no_samples(self):
        """Test fitting the RandomForestClassifier with no samples."""
        X = np.empty((0, 5))  # 0 samples, 5 features
        y = np.empty((0,))
        with self.assertRaises(ValueError):
            self.rf.fit(X, y)

    def test_fit_single_class(self):
        """Test fitting the RandomForestClassifier with a single class."""
        X = np.random.rand(10, 5)  # 10 samples, 5 features
        y = np.zeros(10)  # Single class
        self.rf.fit(X, y)
        for tree in self.rf.trees:
            self.assertEqual(tree["label"], 0)

    def test_fit_sample_weights(self):
        """Test fitting the RandomForestClassifier with sample weights."""
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, size=10)
        sample_weights = np.random.rand(10)
        self.rf.fit(X, y, sample_weight=sample_weights)
        self.assertEqual(len(self.rf.trees), 10)
        for tree in self.rf.trees:
            self.assertIsInstance(tree, dict)

    def test_fit_sample_weights_empty(self):
        """Test fitting the RandomForestClassifier with empty sample weights."""
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, size=10)
        sample_weights = []
        with self.assertRaises((ValueError, IndexError)):
            self.rf.fit(X, y, sample_weight=sample_weights)

    def test_fit_sample_weights_different_length(self):
        """Test fitting the RandomForestClassifier with sample weights of different length."""
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, size=10)
        sample_weights = np.random.rand(5)
        with self.assertRaises((ValueError, IndexError)):
            self.rf.fit(X, y, sample_weight=sample_weights)

    def test_fit_sample_weights_none(self):
        """Test fitting the RandomForestClassifier with None sample weights."""
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, size=10)
        self.rf.fit(X, y, sample_weight=None)
        self.assertEqual(len(self.rf.trees), 10)

    def test_predict_single_sample(self):
        """Test predicting with a single sample."""
        X = [[1, 2, 3, 4, 5]]
        self.rf.fit()
        predictions = self.rf.predict(X)
        self.assertEqual(len(predictions), 1)
        self.assertIsInstance(predictions, list)

    def test_oob_predictions(self):
        """Test out-of-bag predictions."""
        X = np.random.rand(100, 5)
        y = np.random.randint(0, 2, size=100)
        self.rf.fit(X, y)
        oob_predictions = _classify_oob(X, self.rf.trees, self.rf.bootstraps)
        self.assertEqual(len(oob_predictions), len(X))
        self.assertIsInstance(oob_predictions, list)

    def test_predict_proba(self):
        """Test predicting probabilities."""
        X = np.random.rand(10, 5)
        self.rf.fit()
        proba = self.rf.predict_proba(X)
        self.assertEqual(proba.shape, (10, 2))


class TesGradientBoostedClassifier(BaseTest):
    """Set up the GradientBoostedClassifier instance for testing."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        """Initializes a new instance of the GradientBoostedClassifier class before each test method is run."""
        print("\nTesting Gradient Boosted Classifier", end="", flush=True)

    def setUp(self):  # NOQA D201
        """Set up the GradientBoostedClassifier instance for testing."""
        X, y = make_classification(n_samples=100, n_features=5, n_classes=2)
        self.rf = GradientBoostedClassifier(
            X=X, y=y, max_depth=5, n_estimators=10, min_samples_split=2, random_seed=0
        )

    def test_init(self):
        """Tests the initialization of the GradientBoostedClassifier class."""
        self.assertEqual(self.rf.max_depth, 5)
        self.assertEqual(self.rf.n_estimators, 10)
        self.assertEqual(self.rf.min_samples_split, 2)
        self.assertIsInstance(self.rf.trees_, list)
        self.assertIsInstance(self.rf.X, np.ndarray)
        self.assertIsInstance(self.rf.y, np.ndarray)

    def test_init_bad_n_estimators(self):
        """Tests the initialization of the GradientBoostedClassifier class with a bad number of estimators."""
        with self.assertRaises(ValueError):
            GradientBoostedClassifier(X=self.rf.X, y=self.rf.y, n_estimators=-1)

    def test_init_bad_learning_rate(self):
        """Tests the initialization of the GradientBoostedClassifier class with a bad learning rate."""
        with self.assertRaises(ValueError):
            GradientBoostedClassifier(X=self.rf.X, y=self.rf.y, learning_rate=-0.1)

    def test_init_bad_max_depth(self):
        """Tests the initialization of the GradientBoostedClassifier class with a bad maximum depth."""
        with self.assertRaises(ValueError):
            GradientBoostedClassifier(X=self.rf.X, y=self.rf.y, max_depth=0)

    def test_init_bad_min_samples_split(self):
        """Tests the initialization of the GradientBoostedClassifier class with a bad minimum samples split."""
        with self.assertRaises(ValueError):
            GradientBoostedClassifier(X=self.rf.X, y=self.rf.y, min_samples_split=0)

    def test_fit(self):
        """Tests the fit method of the GradientBoostedClassifier class."""
        self.rf.fit()
        self.assertEqual(len(self.rf.trees_), 10)
        self.assertIsInstance(self.rf.trees_[0], RegressorTree)

    def test_fit_single_data_point(self):
        """Test fitting the GradientBoostedClassifier with a single data point."""
        X_single = np.random.rand(1, 5)  # Single sample, 5 features
        y_single = np.array([1])  # Single label
        self.rf.fit(X_single, y_single)
        self.assertEqual(len(self.rf.trees_[0]), 10)

    def test_fit_empty_dataset(self):
        """Test fitting the GradientBoostedClassifier with an empty dataset."""
        X_empty = np.empty((0, 5))  # No samples, 5 features
        y_empty = np.empty((0,))
        with self.assertRaises(ValueError):
            self.rf.fit(X_empty, y_empty)

    def test_fit_no_features(self):
        """Test fitting the GradientBoostedClassifier with no features."""
        X = np.empty((10, 0))  # 10 samples, 0 features
        y = np.random.randint(0, 2, size=10)
        self.rf.fit(X, y)

    def test_fit_no_samples(self):
        """Test fitting the GradientBoostedClassifier with no samples."""
        X = np.empty((0, 5))  # 0 samples, 5 features
        y = np.empty((0,))
        with self.assertRaises(ValueError):
            self.rf.fit(X, y)

    def test_fit_single_class(self):
        """Test fitting the GradientBoostedClassifier with a single class."""
        X = np.random.rand(10, 5)  # 10 samples, 5 features
        y = np.zeros(10)  # Single class
        self.rf.fit(X, y)
        self.assertEqual(len(self.rf.trees_[0]), 10)

    def test_fit_no_X(self):
        """Test fitting the GradientBoostedClassifier without X."""
        y = np.random.randint(0, 2, size=10)
        with self.assertRaises(ValueError):
            self.rf.fit(X=None, y=y)

    def test_fit_no_y(self):
        """Test fitting the GradientBoostedClassifier without y."""
        X = np.random.rand(10, 5)
        with self.assertRaises(ValueError):
            self.rf.fit(X=X, y=None)

    def test_fit_invalid_X(self):
        """Test fitting the GradientBoostedClassifier with invalid X."""
        X = "not a numpy array"
        y = np.random.randint(0, 2, size=10)
        with self.assertRaises(ValueError):
            self.rf.fit(X=X, y=y)

    def test_fit_invalid_y(self):
        """Test fitting the GradientBoostedClassifier with invalid y."""
        X = np.random.rand(10, 5)
        y = "not a numpy array"
        with self.assertRaises(ValueError):
            self.rf.fit(X=X, y=y)

    def test_fit_invalid_shape(self):
        """Test fitting the GradientBoostedClassifier with mismatched X and y shapes."""
        X = np.random.rand(10, 5)
        y = np.random.rand(5)
        with self.assertRaises(ValueError):
            self.rf.fit(X=X, y=y)

    def test_fit_invalid_shape_X(self):
        """Test fitting the GradientBoostedClassifier with invalid shape for X, not 2D."""
        X = np.random.rand(10, 5, 1)
        y = np.random.randint(0, 2, size=10)
        with self.assertRaises(ValueError):
            self.rf.fit(X=X, y=y)

    def test_fit_invalid_shape_y(self):
        """Test fitting the GradientBoostedClassifier with invalid shape for y."""
        X = np.random.rand(10, 5)
        y = np.random.rand(10, 1)
        with self.assertRaises(ValueError):
            self.rf.fit(X=X, y=y)

    def test_fit_sample_weights(self):
        """Test fitting the GradientBoostedClassifier with sample weights."""
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, size=10)
        sample_weights = np.random.rand(10)
        self.rf.fit(X, y, sample_weight=sample_weights)
        self.assertEqual(len(self.rf.trees_), 10)

    def test_fit_sample_weights_empty(self):
        """Test fitting the GradientBoostedClassifier with empty sample weights."""
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, size=10)
        sample_weights = []
        with self.assertRaises((ValueError, IndexError)):
            self.rf.fit(X, y, sample_weight=sample_weights)

    def test_fit_sample_weights_different_length(self):
        """Test fitting the GradientBoostedClassifier with sample weights of different length."""
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, size=10)
        sample_weights = np.random.rand(5)
        with self.assertRaises((ValueError, IndexError)):
            self.rf.fit(X, y, sample_weight=sample_weights)

    def test_fit_sample_weights_none(self):
        """Test fitting the GradientBoostedClassifier with None sample weights."""
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, size=10)
        self.rf.fit(X, y, sample_weight=None)
        self.assertEqual(len(self.rf.trees_), 10)

    def test_predict(self):
        """Test predicting with the GradientBoostedClassifier."""
        self.rf.fit()
        X_test = np.random.rand(10, 5)
        predictions = self.rf.predict(X_test)
        self.assertEqual(len(predictions), 10)
        self.assertTrue(all(pred in self.rf.classes_ for pred in predictions))

    def test_predict_proba(self):
        """Test predicting probabilities with the GradientBoostedClassifier."""
        self.rf.fit()
        X_test = np.random.rand(10, 5)
        probabilities = self.rf.predict_proba(X_test)
        self.assertEqual(probabilities.shape, (10, 2))
        self.assertTrue(np.allclose(probabilities.sum(axis=1), 1))

    def test_decision_function(self):
        """Test the decision function of the GradientBoostedClassifier."""
        self.rf.fit()
        X_test = np.random.rand(10, 5)
        decision_scores = self.rf.decision_function(X_test)
        self.assertEqual(len(decision_scores), 10)

    def test_get_stats(self):
        """Test the get_stats method of the GradientBoostedClassifier."""
        self.rf.fit()
        X_test, y_test = make_classification(n_samples=20, n_features=5, n_classes=2)
        stats = self.rf.get_stats(y_test, X=X_test)
        self.assertIn("Accuracy", stats)
        self.assertIn("Precision", stats)
        self.assertIn("Recall", stats)
        self.assertIn("F1 Score", stats)
        self.assertIn("Log Loss", stats)


if __name__ == "__main__":
    unittest.main()
