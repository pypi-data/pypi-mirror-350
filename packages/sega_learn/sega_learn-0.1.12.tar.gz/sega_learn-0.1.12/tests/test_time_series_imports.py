import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.time_series import *
from tests.utils import BaseTest


class TestImportsTimeSeries(BaseTest):
    """Tests that the time_series subpackage can be imported correctly.

    Methods:
    - setUpClass: Initializes a new instance of the Index class before each test method is run.
    - test_individual_imports: Tests that each module in the segadb package can be imported individually.
    - test_wildcard_import: Tests that the segadb package can be imported using a wildcard import.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Imports - Time Series", end="", flush=True)

    def test_individual_imports(self):
        """Tests that each module in the segadb package can be imported individually."""
        from sega_learn.time_series import ARIMA as arima
        from sega_learn.time_series import SARIMA as sarima
        from sega_learn.time_series import SARIMAX as sarimax
        from sega_learn.time_series import AdditiveDecomposition as add
        from sega_learn.time_series import DoubleExponentialSmoothing as des
        from sega_learn.time_series import ExponentialMovingAverage as ema
        from sega_learn.time_series import MultiplicativeDecomposition as mul
        from sega_learn.time_series import SimpleExponentialSmoothing as exps
        from sega_learn.time_series import SimpleMovingAverage as sm
        from sega_learn.time_series import TripleExponentialSmoothing as tes
        from sega_learn.time_series import WeightedMovingAverage as wm

        assert arima is not None
        assert sarima is not None
        assert sarimax is not None
        assert exps is not None
        assert des is not None
        assert tes is not None
        assert sm is not None
        assert wm is not None
        assert add is not None
        assert mul is not None
        assert ema is not None

    def test_wildcard_import(self):
        """Tests that the segadb package can be imported using a wildcard import."""
        assert ARIMA is not None
        assert SARIMA is not None
        assert SARIMAX is not None
        assert DoubleExponentialSmoothing is not None
        assert SimpleExponentialSmoothing is not None
        assert TripleExponentialSmoothing is not None
        assert SimpleMovingAverage is not None
        assert WeightedMovingAverage is not None

    def test_ARIMA(self):  # NOQA D201
        from sega_learn.time_series import ARIMA

        assert ARIMA is not None

    def test_SARIMA(self):  # NOQA D201
        from sega_learn.time_series import SARIMA

        assert SARIMA is not None

    def test_SARIMAX(self):  # NOQA D201
        from sega_learn.time_series import SARIMAX

        assert SARIMAX is not None

    def test_SimpleExponentialSmoothing(self):  # NOQA D201
        from sega_learn.time_series import SimpleExponentialSmoothing

        assert SimpleExponentialSmoothing is not None

    def test_DoubleExponentialSmoothing(self):  # NOQA D201
        from sega_learn.time_series import DoubleExponentialSmoothing

        assert DoubleExponentialSmoothing is not None

    def test_TripleExponentialSmoothing(self):  # NOQA D201ss
        from sega_learn.time_series import TripleExponentialSmoothing

        assert TripleExponentialSmoothing is not None

    def test_SimpleMovingAverage(self):  # NOQA D201
        from sega_learn.time_series import SimpleMovingAverage

        assert SimpleMovingAverage is not None

    def test_WeightedMovingAverage(self):  # NOQA D201
        from sega_learn.time_series import WeightedMovingAverage

        assert WeightedMovingAverage is not None

    def test_ExponentialMovingAverage(self):  # NOQA D201
        from sega_learn.time_series import ExponentialMovingAverage

        assert ExponentialMovingAverage is not None

    def test_AdditiveDecomposition(self):  # NOQA D201
        from sega_learn.time_series import AdditiveDecomposition

        assert AdditiveDecomposition is not None

    def test_MultiplicativeDecomposition(self):  # NOQA D201
        from sega_learn.time_series import MultiplicativeDecomposition

        assert MultiplicativeDecomposition is not None


if __name__ == "__main__":
    unittest.main()
