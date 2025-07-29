import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.trees import *
from tests.utils import BaseTest


class TestImportsLinear(BaseTest):
    """Tests that the linear_models subpackage can be imported correctly.

    Methods:
    - setUpClass: Initializes a new instance of the Index class before each test method is run.
    - test_individual_imports: Tests that each module in the segadb package can be imported individually.
    - test_wildcard_import: Tests that the segadb package can be imported using a wildcard import.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Imports - Trees", end="", flush=True)

    def test_individual_imports(self):
        """Tests that each module in the segadb package can be imported individually."""
        from sega_learn.trees import AdaBoostClassifier as abc
        from sega_learn.trees import AdaBoostRegressor as abr
        from sega_learn.trees import ClassifierTree as ct
        from sega_learn.trees import ClassifierTreeUtility as ctu
        from sega_learn.trees import GradientBoostedClassifier as gbc
        from sega_learn.trees import GradientBoostedRegressor as gbr
        from sega_learn.trees import RandomForestClassifier as rfc
        from sega_learn.trees import RandomForestRegressor as rfr
        from sega_learn.trees import RegressorTree as rt
        from sega_learn.trees import RegressorTreeUtility as rtu

        assert ctu is not None
        assert ct is not None
        assert rtu is not None
        assert rt is not None
        assert rfc is not None
        assert rfr is not None
        assert gbr is not None
        assert gbc is not None
        assert abc is not None
        assert abr is not None

    def test_wildcard_import(self):
        """Tests that the segadb package can be imported using a wildcard import."""
        assert ClassifierTreeUtility is not None
        assert ClassifierTree is not None
        assert RegressorTreeUtility is not None
        assert RegressorTree is not None
        assert RandomForestClassifier is not None
        assert RandomForestRegressor is not None
        assert GradientBoostedRegressor is not None
        assert GradientBoostedClassifier is not None
        assert AdaBoostRegressor is not None
        assert AdaBoostClassifier is not None

    def test_ClassifierTree(self):  # NOQA D201
        from sega_learn.trees import ClassifierTree

        assert ClassifierTree is not None

    def test_ClassifierTreeUtility(self):  # NOQA D201
        from sega_learn.trees import ClassifierTreeUtility

        assert ClassifierTreeUtility is not None

    def test_GradientBoostedClassifier(self):  # NOQA D201
        from sega_learn.trees import GradientBoostedClassifier

        assert GradientBoostedClassifier is not None

    def test_GradientBoostedRegressor(self):  # NOQA D201
        from sega_learn.trees import GradientBoostedRegressor

        assert GradientBoostedRegressor is not None

    def test_RandomForestClassifier(self):  # NOQA D201
        from sega_learn.trees import RandomForestClassifier

        assert RandomForestClassifier is not None

    def test_RandomForestRegressor(self):  # NOQA D201
        from sega_learn.trees import RandomForestRegressor

        assert RandomForestRegressor is not None

    def test_RegressorTree(self):  # NOQA D201
        from sega_learn.trees import RegressorTree

        assert RegressorTree is not None

    def test_RegressorTreeUtility(self):  # NOQA D201
        from sega_learn.trees import RegressorTreeUtility

        assert RegressorTreeUtility is not None

    def test_AdaBoostClassifier(self):  # NOQA D201
        from sega_learn.trees import AdaBoostClassifier

        assert AdaBoostClassifier is not None

    def test_AdaBoostRegressor(self):  # NOQA D201
        from sega_learn.trees import AdaBoostRegressor

        assert AdaBoostRegressor is not None


if __name__ == "__main__":
    unittest.main()
