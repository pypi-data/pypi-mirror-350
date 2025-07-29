import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.auto import *
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
        print("\nTesting Imports - Auto", end="", flush=True)

    def test_individual_imports(self):  # NOQA D201
        from sega_learn.auto import AutoClassifier as clf
        from sega_learn.auto import AutoRegressor as reg

        assert reg is not None
        assert clf is not None

    def test_wildcard_import(self):  # NOQA D201
        assert AutoRegressor is not None
        assert AutoClassifier is not None

    def test_AutoClassifier(self):  # NOQA D201
        from sega_learn.auto import AutoClassifier

        assert AutoClassifier is not None

    def test_AutoRegressor(self):  # NOQA D201
        from sega_learn.auto import AutoRegressor

        assert AutoRegressor is not None


if __name__ == "__main__":
    unittest.main()
