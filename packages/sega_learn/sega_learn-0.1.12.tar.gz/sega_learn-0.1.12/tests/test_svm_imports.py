import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.svm import *
from tests.utils import BaseTest


class TestImportsSVM(BaseTest):
    """Tests that the SVM subpackage can be imported correctly.

    Methods:
    - setUpClass: Initializes a new instance of the Index class before each test method is run.
    - test_individual_imports: Tests that each module in the segadb package can be imported individually.
    - test_wildcard_import: Tests that the segadb package can be imported using a wildcard import.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Imports - SVM", end="", flush=True)

    def test_individual_imports(self):
        """Tests that each module in the segadb package can be imported individually."""
        from sega_learn.svm import BaseSVM as bsvm
        from sega_learn.svm import GeneralizedSVC as gsvc
        from sega_learn.svm import GeneralizedSVR as gsvr
        from sega_learn.svm import LinearSVC as lsvc
        from sega_learn.svm import LinearSVR as lsvr
        from sega_learn.svm import OneClassSVM as osvm

        assert bsvm is not None
        assert lsvc is not None
        assert lsvr is not None
        assert osvm is not None
        assert gsvr is not None
        assert gsvc is not None

    def test_wildcard_import(self):
        """Tests that the segadb package can be imported using a wildcard import."""
        assert BaseSVM is not None
        assert LinearSVC is not None
        assert LinearSVR is not None
        assert OneClassSVM is not None
        assert GeneralizedSVR is not None
        assert GeneralizedSVC is not None

    def test_LinearSVC(self):  # NOQA D201
        from sega_learn.svm import LinearSVC

        assert LinearSVC is not None

    def test_LinearSVR(self):  # NOQA D201
        from sega_learn.svm import LinearSVR

        assert LinearSVR is not None

    def test_OneClassSVM(self):  # NOQA D201
        from sega_learn.svm import OneClassSVM

        assert OneClassSVM is not None

    def test_GeneralizedSVC(self):  # NOQA D201
        from sega_learn.svm import GeneralizedSVC

        assert GeneralizedSVC is not None

    def test_GeneralizedSVR(self):  # NOQA D201
        from sega_learn.svm import GeneralizedSVR

        assert GeneralizedSVR is not None

    def test_BaseSVM(self):  # NOQA D201
        from sega_learn.svm import BaseSVM

        assert BaseSVM is not None


if __name__ == "__main__":
    unittest.main()
