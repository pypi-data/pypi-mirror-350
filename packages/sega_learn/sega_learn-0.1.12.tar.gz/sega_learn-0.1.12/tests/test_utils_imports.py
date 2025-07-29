import os
import sys
import unittest

# Change the working directory to the parent directory to allow importing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sega_learn.utils import *
from tests.utils import BaseTest


class TestImportsUtils(BaseTest):
    """Tests that the Utils subpackage can be imported correctly.

    Methods:
    - setUpClass: Initializes a new instance of the Index class before each test method is run.
    - test_individual_imports: Tests that each module in the segadb package can be imported individually.
    - test_wildcard_import: Tests that the segadb package can be imported using a wildcard import.
    """

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Imports - Utils", end="", flush=True)

    def test_individual_imports(self):
        """Tests that each module in the segadb package can be imported individually."""
        from sega_learn.utils import PCA as pca
        from sega_learn.utils import SMOTE as smote
        from sega_learn.utils import SVD as svd
        from sega_learn.utils import AnimationBase as anb
        from sega_learn.utils import Augmenter as augmenter
        from sega_learn.utils import ClassificationAnimation as canb
        from sega_learn.utils import CustomImputer as cimp
        from sega_learn.utils import DataPrep as dp
        from sega_learn.utils import DirectionalImputer as dimp
        from sega_learn.utils import Encoder as enc
        from sega_learn.utils import ForcastingAnimation as fanb
        from sega_learn.utils import ForecastRegressor as fr
        from sega_learn.utils import GridSearchCV as gscv
        from sega_learn.utils import InterpolationImputer as impp
        from sega_learn.utils import KNNImputer as knnimp
        from sega_learn.utils import Metrics as metrics
        from sega_learn.utils import ModelSelectionUtility as msu
        from sega_learn.utils import PolynomialTransform as plt
        from sega_learn.utils import RandomOverSampler as ros
        from sega_learn.utils import RandomSearchCV as rscv
        from sega_learn.utils import RandomUnderSampler as rus
        from sega_learn.utils import RegressionAnimation as ranb
        from sega_learn.utils import Scaler as scaler
        from sega_learn.utils import StatisticalImputer as simp
        from sega_learn.utils import VotingClassifier as vc
        from sega_learn.utils import VotingRegressor as vr
        from sega_learn.utils import check_is_fitted as cif
        from sega_learn.utils import check_X_y as cxy
        from sega_learn.utils import make_blobs as mkblobs
        from sega_learn.utils import make_classification as mkcls
        from sega_learn.utils import make_regression as mkreg
        from sega_learn.utils import make_time_series as mkts
        from sega_learn.utils import normalize as norm
        from sega_learn.utils import one_hot_encode as ohe
        from sega_learn.utils import train_test_split as tts

        assert plt is not None
        assert dp is not None
        assert vr is not None
        assert vc is not None
        assert msu is not None
        assert gscv is not None
        assert rscv is not None
        assert metrics is not None
        assert ros is not None
        assert rus is not None
        assert smote is not None
        assert augmenter is not None
        assert pca is not None
        assert svd is not None
        assert mkreg is not None
        assert mkcls is not None
        assert mkblobs is not None
        assert mkts is not None
        assert tts is not None
        assert ohe is not None
        assert norm is not None
        assert scaler is not None
        assert enc is not None
        assert fr is not None
        assert anb is not None
        assert ranb is not None
        assert fanb is not None
        assert canb is not None
        assert cif is not None
        assert cxy is not None
        assert simp is not None
        assert dimp is not None
        assert impp is not None
        assert knnimp is not None
        assert cimp is not None

    def test_wildcard_import(self):
        """Tests that the segadb package can be imported using a wildcard import."""
        assert PolynomialTransform is not None
        assert DataPrep is not None
        assert VotingRegressor is not None
        assert ModelSelectionUtility is not None
        assert GridSearchCV is not None
        assert RandomSearchCV is not None
        assert Metrics is not None
        assert RandomOverSampler is not None
        assert RandomUnderSampler is not None
        assert SMOTE is not None
        assert Augmenter is not None
        assert PCA is not None
        assert SVD is not None
        assert make_regression is not None
        assert make_classification is not None
        assert make_blobs is not None
        assert make_time_series is not None
        assert train_test_split is not None
        assert one_hot_encode is not None
        assert normalize is not None
        assert Scaler is not None
        assert Encoder is not None
        assert AnimationBase is not None
        assert RegressionAnimation is not None
        assert ForcastingAnimation is not None
        assert ClassificationAnimation is not None

    def test_AnimationBase(self):  # NOQA D201
        from sega_learn.utils import AnimationBase

        assert AnimationBase is not None

    def test_RegressionAnimation(self):  # NOQA D201
        from sega_learn.utils import RegressionAnimation

        assert RegressionAnimation is not None

    def test_ForcastingAnimation(self):  # NOQA D201
        from sega_learn.utils import ForcastingAnimation

        assert ForcastingAnimation is not None

    def test_ClassificationAnimation(self):  # NOQA D201
        from sega_learn.utils import ClassificationAnimation

        assert ClassificationAnimation is not None

    def test_PCA(self):  # NOQA D201
        from sega_learn.utils import PCA

        assert PCA is not None

    def test_SMOTE(self):  # NOQA D201
        from sega_learn.utils import SMOTE

        assert SMOTE is not None

    def test_SVD(self):  # NOQA D201
        from sega_learn.utils import SVD

        assert SVD is not None

    def test_Augmenter(self):  # NOQA D201
        from sega_learn.utils import Augmenter

        assert Augmenter is not None

    def test_DataPrep(self):  # NOQA D201
        from sega_learn.utils import DataPrep

        assert DataPrep is not None

    def test_GridSearchCV(self):  # NOQA D201
        from sega_learn.utils import GridSearchCV

        assert GridSearchCV is not None

    def test_Metrics(self):  # NOQA D201
        from sega_learn.utils import Metrics

        assert Metrics is not None

    def test_ModelSelectionUtility(self):  # NOQA D201
        from sega_learn.utils import ModelSelectionUtility

        assert ModelSelectionUtility is not None

    def test_PolynomialTransform(self):  # NOQA D201
        from sega_learn.utils import PolynomialTransform

        assert PolynomialTransform is not None

    def test_RandomOverSampler(self):  # NOQA D201
        from sega_learn.utils import RandomOverSampler

        assert RandomOverSampler is not None

    def test_RandomSearchCV(self):  # NOQA D201
        from sega_learn.utils import RandomSearchCV

        assert RandomSearchCV is not None

    def test_RandomUnderSampler(self):  # NOQA D201
        from sega_learn.utils import RandomUnderSampler

        assert RandomUnderSampler is not None

    def test_Scaler(self):  # NOQA D201
        from sega_learn.utils import Scaler

        assert Scaler is not None

    def test_Encoder(self):  # NOQA D201
        from sega_learn.utils import Encoder

        assert Encoder is not None

    def test_VotingRegressor(self):  # NOQA D201
        from sega_learn.utils import VotingRegressor

        assert VotingRegressor is not None

    def test_ForecastRegressor(self):  # NOQA D201
        from sega_learn.utils import ForecastRegressor

        assert ForecastRegressor is not None

    def test_make_blobs(self):  # NOQA D201
        from sega_learn.utils import make_blobs

        assert make_blobs is not None

    def test_make_classification(self):  # NOQA D201
        from sega_learn.utils import make_classification

        assert make_classification is not None

    def test_make_regression(self):  # NOQA D201
        from sega_learn.utils import make_regression

        assert make_regression is not None

    def test_make_time_series(self):  # NOQA D201
        from sega_learn.utils import make_time_series

        assert make_time_series is not None

    def test_normalize(self):  # NOQA D201
        from sega_learn.utils import normalize

        assert normalize is not None

    def test_one_hot_encode(self):  # NOQA D201
        from sega_learn.utils import one_hot_encode

        assert one_hot_encode is not None

    def test_train_test_split(self):  # NOQA D201
        from sega_learn.utils import train_test_split

        assert train_test_split is not None

    def test_check_is_fitted(self):  # NOQA D201
        from sega_learn.utils import check_is_fitted

        assert check_is_fitted is not None

    def test_check_X_y(self):  # NOQA D201
        from sega_learn.utils import check_X_y

        assert check_X_y is not None

    def test_StatisticalImputer(self):  # NOQA D201
        from sega_learn.utils import StatisticalImputer

        assert StatisticalImputer is not None

    def test_DirectionalImputer(self):  # NOQA D201
        from sega_learn.utils import DirectionalImputer

        assert DirectionalImputer is not None

    def test_InterpolationImputer(self):  # NOQA D201
        from sega_learn.utils import InterpolationImputer

        assert InterpolationImputer is not None

    def test_KNNImputer(self):  # NOQA D201
        from sega_learn.utils import KNNImputer

        assert KNNImputer is not None

    def test_CustomImputer(self):  # NOQA D201
        from sega_learn.utils import CustomImputer

        assert CustomImputer is not None


if __name__ == "__main__":
    unittest.main()
