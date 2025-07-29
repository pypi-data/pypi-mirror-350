import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.clustering import *
from tests.utils import BaseTest


class TestImportsClustering(BaseTest):
    """Tests that the clustering subpackage can be imported correctly.

    Methods:
    - setUpClass: Initializes a new instance of the Index class before each test method is run.
    - test_individual_imports: Tests that each module in the segadb package can be imported individually.
    - test_wildcard_import: Tests that the segadb package can be imported using a wildcard import.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Imports - Clustering", end="", flush=True)

    def test_individual_imports(self):  # NOQA D201
        from sega_learn.clustering import DBSCAN as dbs
        from sega_learn.clustering import KMeans as kms

        assert dbs is not None
        assert kms is not None

    def test_wildcard_import(self):  # NOQA D201
        assert DBSCAN is not None
        assert KMeans is not None

    def test_DBSCAN(self):  # NOQA D201
        from sega_learn.clustering import DBSCAN

        assert DBSCAN is not None

    def test_KMeans(self):  # NOQA D201
        from sega_learn.clustering import KMeans

        assert KMeans is not None


if __name__ == "__main__":
    unittest.main()
