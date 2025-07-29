import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.pipelines import *
from tests.utils import BaseTest


class TestImportsPipelines(BaseTest):
    """Tests that the Pipelines subpackage can be imported correctly.

    Methods:
    - setUpClass: Initializes a new instance of the Index class before each test method is run.
    - test_individual_imports: Tests that each module in the segadb package can be imported individually.
    - test_wildcard_import: Tests that the segadb package can be imported using a wildcard import.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Imports - Pipelines", end="", flush=True)

    def test_individual_imports(self):
        """Tests that each module in the segadb package can be imported individually."""
        from sega_learn.pipelines import ForecastingPipeline as fp
        from sega_learn.pipelines import Pipeline as p

        assert fp is not None
        assert p is not None

    def test_wildcard_import(self):
        """Tests that the segadb package can be imported using a wildcard import."""
        assert ForecastingPipeline is not None
        assert Pipeline is not None

    def test_ForecastingPipeline(self):  # NOQA D201
        from sega_learn.pipelines import ForecastingPipeline

        assert ForecastingPipeline is not None

    def test_Pipeline(self):  # NOQA D201
        from sega_learn.pipelines import Pipeline

        assert Pipeline is not None


if __name__ == "__main__":
    unittest.main()
