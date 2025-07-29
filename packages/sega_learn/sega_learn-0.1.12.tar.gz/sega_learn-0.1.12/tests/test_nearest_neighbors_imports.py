import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.nearest_neighbors import *
from tests.utils import BaseTest


class TestImportsNearestNeighbors(BaseTest):
    """Tests that the clustering subpackage can be imported correctly.

    Methods:
    - setUpClass: Initializes a new instance of the Index class before each test method is run.
    - test_individual_imports: Tests that each module in the segadb package can be imported individually.
    - test_wildcard_import: Tests that the segadb package can be imported using a wildcard import.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Imports - Nearest Neighbors", end="", flush=True)

    def test_individual_imports(self):  # NOQA D201
        from sega_learn.nearest_neighbors import KNeighborsClassifier as knc
        from sega_learn.nearest_neighbors import KNeighborsRegressor as knr

        assert knc is not None
        assert knr is not None

    def test_wildcard_import(self):  # NOQA D201
        assert KNeighborsClassifier is not None
        assert KNeighborsRegressor is not None

    # NOQA D201
    def test_KNeighborsClassifier(self):  # NOQA D201
        from sega_learn.nearest_neighbors import KNeighborsClassifier

        assert KNeighborsClassifier is not None

    def test_KNeighborsRegressor(self):  # NOQA D201
        from sega_learn.nearest_neighbors import KNeighborsRegressor

        assert KNeighborsRegressor is not None


if __name__ == "__main__":
    unittest.main()
