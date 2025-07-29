import contextlib
import glob
import importlib.util
import io
import os
import sys
import unittest

from tests.utils import BaseTest, strip_file_path, suppress_print

# Change the working directory to the parent directory to allow importing the segadb package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestExampleExceptions(BaseTest):
    """Test cases to check for exceptions in example files."""

    def test_main(self, example_file):
        """Main test function to check for exceptions in example files."""
        if "classifier.py" in example_file:
            from examples.auto.classifier import run_example

            print(
                f"\nTesting example file: {strip_file_path(example_file)}",
                end="",
                flush=True,
            )
            with suppress_print():
                run_example(verbose=False, test=True)

        if "regressor.py" in example_file:
            from examples.auto.regressor import run_example

            print(
                f"\nTesting example file: {strip_file_path(example_file)}",
                end="",
                flush=True,
            )
            with suppress_print():
                run_example(verbose=False, test=True)


class TestExamplesAuto(BaseTest):
    """Test cases for the example files. Holds dynamically generated test cases for each example file."""

    pass


def load_tests(loader, tests, pattern):
    """Dynamically load test cases for each example file.

    Args:
        loader: The test loader instance.
        tests: The test cases to load.
        pattern: The pattern to match test files.
    """
    # Find all example files in the examples directory. (Files starting with 'example_')
    example_files = glob.glob(
        os.path.join(os.path.dirname(__file__), "..\\examples\\auto\\*.py")
    )

    # Raise an error if no example files are found.
    if not example_files:
        raise FileNotFoundError("No example files found.")

    # Dynamically generate test cases for each example file.
    for example_file in example_files:
        test_name = f"test_{os.path.basename(example_file)}"

        def test_func(self, example_file=example_file):
            """Tests the functionality of a given example file by importing it as a module and executing it."""
            print(
                f"\nTesting example file: {strip_file_path(example_file)}",
                end="",
                flush=True,
            )

            # Import the example file as a module and execute it.
            spec = importlib.util.spec_from_file_location("module.name", example_file)
            example_module = importlib.util.module_from_spec(spec)

            # Redirect stdout to suppress output from the example file.
            with contextlib.redirect_stdout(io.StringIO()):
                spec.loader.exec_module(example_module)

        setattr(
            TestExamplesAuto,
            test_name,
            lambda self, example_file=example_file: TestExampleExceptions().test_main(
                example_file
            ),
        )

    # Load the dynamically generated test cases.
    return loader.loadTestsFromTestCase(TestExamplesAuto)


if __name__ == "__main__":
    unittest.main()
