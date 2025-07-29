import os
import sys
import unittest
import warnings

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sega_learn.linear_models import LogisticRegression, OrdinaryLeastSquares
from sega_learn.utils.imputation import *
from tests.utils import BaseTest


# Helper Mock Estimators for TestCustomImputer
class MockEstimator:  # noqa: D101
    def __init__(  # noqa: D107
        self,
        constant_prediction=None,
        predict_mean_of_y=False,
        predict_mode_of_y=False,
        dtype=None,
    ):
        self.constant_prediction = constant_prediction
        self.predict_mean_of_y = predict_mean_of_y
        self.predict_mode_of_y = predict_mode_of_y
        self.y_fit_ = None
        self.fitted_ = False
        self.dtype = dtype

    def fit(self, X, y):  # noqa: D102
        self.y_fit_ = np.asarray(y)  # Ensure y is array-like for operations
        self.fitted_ = True
        return self

    def predict(self, X):  # noqa: D102
        if not self.fitted_:
            raise RuntimeError("Estimator not fitted.")
        n_samples = X.shape[0]

        if self.constant_prediction is not None:
            pred = np.full(n_samples, self.constant_prediction)
        elif self.predict_mean_of_y and self.y_fit_ is not None:
            try:
                numeric_y = pd.to_numeric(self.y_fit_)
                mean_val = np.nanmean(numeric_y)
                pred = np.full(n_samples, mean_val if not np.isnan(mean_val) else 0)
            except Exception:
                pred = np.full(n_samples, 0)
        elif self.predict_mode_of_y and self.y_fit_ is not None:
            from collections import Counter

            counts = Counter(self.y_fit_)
            mode_val = counts.most_common(1)[0][0] if counts else "unknown"
            pred = np.full(n_samples, mode_val)
        else:
            pred = np.zeros(n_samples)  # Default fallback

        if self.dtype:
            return pred.astype(self.dtype)
        return pred


class MockRegressor(MockEstimator):  # noqa: D101
    def __init__(self, constant_prediction=0.0, predict_mean_of_y=True):  # noqa: D107
        super().__init__(
            constant_prediction=constant_prediction,
            predict_mean_of_y=predict_mean_of_y,
            dtype=float,
        )


class MockClassifier(MockEstimator):  # noqa: D101
    def __init__(self, constant_prediction="cat_A", predict_mode_of_y=True):  # noqa: D107
        super().__init__(
            constant_prediction=constant_prediction,
            predict_mode_of_y=predict_mode_of_y,
            dtype=object,
        )
        self.classes_ = None  # For compatibility with some checks

    def fit(self, X, y):  # noqa: D102
        super().fit(X, y)
        self.classes_ = np.unique(y)
        return self


def assert_no_float_nan(arr):
    """Asserts that a numpy array does not contain float NaN values, handling object arrays."""
    if arr.dtype == object:
        for x in np.nditer(arr, flags=["refs_ok"]):
            val = x.item()  # Get the actual Python object
            if isinstance(val, float) and np.isnan(val):
                raise AssertionError(f"Found float NaN in object array: {arr}")
    elif np.issubdtype(arr.dtype, np.floating) and np.isnan(arr).any():
        raise AssertionError(f"Found float NaN in numeric array: {arr}")
    # Other types (int, bool, string if not object) are fine


class TestStatisticalImputer(BaseTest):
    """Unit test for the StatisticalImputer class in the imputation module."""

    @classmethod
    def setUpClass(cls):  # noqa: D102
        print("\nTesting StatisticalImputer", end="", flush=True)

    def setUp(self):  # noqa: D102
        self.numeric_data_nan = np.array(
            [[1, np.nan, 3], [4, 5, np.nan], [np.nan, 8, 9], [10, 11, 12]], dtype=float
        )
        self.expected_mean_numeric = np.array(
            [
                [1, (5 + 8 + 11) / 3, 3],
                [4, 5, (3 + 9 + 12) / 3],
                [(1 + 4 + 10) / 3, 8, 9],
                [10, 11, 12],
            ],
            dtype=float,
        )
        self.expected_median_numeric = np.array(
            [[1, 8, 3], [4, 5, 9], [4, 8, 9], [10, 11, 12]], dtype=float
        )
        self.expected_mode_numeric = np.array(
            [[1, 5, 3], [4, 5, 3], [1, 8, 9], [10, 11, 12]], dtype=float
        )  # Smallest mode for ties

        self.categorical_data_nan = np.array(
            [["a", "x", np.nan], [np.nan, "y", "p"], ["c", "x", "q"], ["a", "z", "p"]],
            dtype=object,
        )
        self.expected_mode_categorical = np.array(
            [["a", "x", "p"], ["a", "y", "p"], ["c", "x", "q"], ["a", "z", "p"]],
            dtype=object,
        )

        self.mixed_data_nan = np.array(
            [[1, "x", np.nan], [np.nan, 5, "p"], [3, "x", 10.0], ["1", "z", np.nan]],
            dtype=object,
        )
        # Col0 ('1' becomes 1): mean (1+1+3)/3=5/3. median 1. mode 1.
        # Col1 (cat): mode 'x'.
        # Col2 (numeric 'p' becomes nan): mean 10.0. median 10.0. mode 10.0.
        self.expected_mode_mixed = np.array(
            [[1, "x", 10.0], [1.0, 5, "p"], [3, "x", 10.0], ["1", "z", 10.0]],
            dtype=object,
        )

        self.all_nan_col_data = np.array([[1, np.nan], [2, np.nan]], dtype=float)
        # For mean/median, NaN col becomes 0. For mode, NaN col becomes "missing" (if object) or 0 (if numeric).
        # If input is float, output after filling NaN col for mode will be float.

        self.numeric_data_custom_missing = np.array(
            [[1, -999, 3], [4, 5, -999]], dtype=float
        )
        self.expected_mean_custom_missing = np.array(
            [[1, 5, 3], [4, 5, 3]], dtype=float
        )

        self.df_numeric_nan = pd.DataFrame(
            self.numeric_data_nan, columns=["A", "B", "C"]
        )

    def test_transform_before_fit(self):
        """Test transform before fit."""
        imputer = StatisticalImputer(warn=False)
        with self.assertRaises(RuntimeError):
            imputer.transform(self.numeric_data_nan)

    def test_invalid_strategy(self):
        """Test invalid strategy."""
        with self.assertRaises(ValueError):
            StatisticalImputer(strategy="unknown")

    def test_mean_imputation_numeric(self):
        """Test mean imputation for numeric data."""
        imputer = StatisticalImputer(strategy="mean", warn=False)
        transformed = imputer.fit_transform(self.numeric_data_nan.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_almost_equal(transformed, self.expected_mean_numeric)

    def test_median_imputation_numeric(self):
        """Test median imputation for numeric data."""
        imputer = StatisticalImputer(strategy="median", warn=False)
        transformed = imputer.fit_transform(self.numeric_data_nan.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_almost_equal(transformed, self.expected_median_numeric)

    def test_mode_imputation_numeric(self):
        """Test mode imputation for numeric data."""
        imputer = StatisticalImputer(strategy="mode", warn=False)
        transformed = imputer.fit_transform(self.numeric_data_nan.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_equal(transformed, self.expected_mode_numeric)

    def test_mode_imputation_categorical(self):
        """Test mode imputation for categorical data."""
        imputer = StatisticalImputer(strategy="mode", warn=False)
        transformed = imputer.fit_transform(self.categorical_data_nan.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_equal(transformed, self.expected_mode_categorical)

    def test_imputation_with_custom_missing_value(self):
        """Test imputation with custom missing value."""
        imputer = StatisticalImputer(strategy="mean", missing_values=-999, warn=False)
        transformed = imputer.fit_transform(self.numeric_data_custom_missing.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_almost_equal(
            transformed, self.expected_mean_custom_missing
        )

    def test_imputation_all_nan_column_mean(self):
        """Test imputation for all-NaN column, mean strategy."""
        imputer_mean = StatisticalImputer(strategy="mean", warn=False)
        # Expected: [ [1,0], [2,0] ] because all-NaN numeric col defaults to 0 for mean/median
        transformed_mean = imputer_mean.fit_transform(self.all_nan_col_data.copy())
        assert_no_float_nan(transformed_mean)
        np.testing.assert_array_almost_equal(
            transformed_mean, np.array([[1, 0], [2, 0]], dtype=float)
        )

    def test_imputation_all_nan_column_mode(self):
        """Test imputation for all-NaN column, mode strategy."""
        imputer_mode = StatisticalImputer(strategy="mode", warn=False)
        # Expected: [ [1,0], [2,0] ] because it's a float column, NaN stat becomes 0 in transform
        transformed_mode = imputer_mode.fit_transform(self.all_nan_col_data.copy())
        assert_no_float_nan(transformed_mode)
        np.testing.assert_array_almost_equal(
            transformed_mode, np.array([[1, 0], [2, 0]], dtype=float)
        )

    def test_dataframe_input(self):
        """Test imputation for dataframe input."""
        imputer = StatisticalImputer(strategy="mean", warn=False)
        with self.assertRaises(TypeError):
            imputer.fit_transform(self.df_numeric_nan.copy())

    def test_fit_transform_equivalence(self):
        """Test fit-transform equivalence."""
        imputer1 = StatisticalImputer(strategy="median", warn=False)
        imputer2 = StatisticalImputer(strategy="median", warn=False)

        data = self.numeric_data_nan.copy()

        transformed_fit_then_transform = imputer1.fit(data).transform(data)
        transformed_fit_transform = imputer2.fit_transform(data)

        np.testing.assert_array_almost_equal(
            transformed_fit_then_transform, transformed_fit_transform
        )


class TestDirectionalImputer(BaseTest):
    """Unit test for the DirectionalImputer class in the imputation module."""

    @classmethod
    def setUpClass(cls):  # noqa: D102
        print("\nTesting DirectionalImputer", end="", flush=True)

    def setUp(self):  # noqa: D102
        self.data_1d_nan = np.array([1, np.nan, np.nan, 4, np.nan, 6], dtype=float)
        self.expected_1d_fwd = np.array([1, 1, 1, 4, 4, 6], dtype=float)
        self.expected_1d_bwd = np.array([1, 4, 4, 4, 6, 6], dtype=float)

        self.data_2d_nan = np.array(
            [[1, np.nan, 3], [np.nan, 5, np.nan], [7, np.nan, 9]], dtype=float
        )
        self.expected_2d_fwd = np.array(
            [[1, np.nan, 3], [1, 5, 3], [7, 5, 9]], dtype=float
        )  # Leading NaN in col 1 remains if no prior val
        self.expected_2d_bwd = np.array(
            [[1, 5, 3], [7, 5, 9], [7, np.nan, 9]], dtype=float
        )  # Trailing NaN in col 1 remains

        self.data_mixed_object = np.array(
            [[1, "a", np.nan], [np.nan, None, "c"], [3, "d", np.nan]], dtype=object
        )
        self.expected_mixed_fwd = np.array(
            [[1, "a", np.nan], [1, None, "c"], [3, "d", "c"]], dtype=object
        )
        self.expected_mixed_bwd = np.array(
            [[1, "a", "c"], [3, "d", "c"], [3, "d", np.nan]], dtype=object
        )

        self.data_leading_nan_col = np.array([[np.nan, 1], [np.nan, 2]], dtype=float)
        self.expected_leading_fwd = np.array(
            [[np.nan, 1], [np.nan, 2]], dtype=float
        )  # FWD keeps leading NaNs
        self.expected_leading_bwd = np.array(
            [[np.nan, 1], [np.nan, 2]], dtype=float
        )  # BWD fills from below, but here there's nothing above to make it non-NaN for fwd

    def test_transform_before_fit(self):
        """Test transform before fit."""
        imputer = DirectionalImputer()
        with self.assertRaises(RuntimeError):
            imputer.transform(self.data_1d_nan)

    def test_invalid_direction(self):
        """Test invalid direction."""
        with self.assertRaises(ValueError):
            DirectionalImputer(direction="sideways")

    def test_forward_fill_1d(self):
        """Test forward fill for 1D array."""
        imputer = DirectionalImputer(direction="forward")
        transformed = imputer.fit_transform(self.data_1d_nan.copy())
        assert_no_float_nan(transformed)  # NaNs should be filled if possible
        np.testing.assert_array_equal(transformed, self.expected_1d_fwd)

    def test_backward_fill_1d(self):
        """Test backward fill for 1D array."""
        imputer = DirectionalImputer(direction="backward")
        transformed = imputer.fit_transform(self.data_1d_nan.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_equal(transformed, self.expected_1d_bwd)

    def test_forward_fill_2d(self):
        """Test forward fill for 2D array."""
        imputer = DirectionalImputer(direction="forward")
        transformed = imputer.fit_transform(self.data_2d_nan.copy())
        # Check for remaining NaNs where ffill couldn't fill (leading NaNs)
        self.assertTrue(np.isnan(transformed[0, 1]))
        transformed_no_nan_check = transformed.copy()
        transformed_no_nan_check[
            np.isnan(transformed_no_nan_check)
        ] = -999  # temp replace for general check
        self.expected_2d_fwd_no_nan_check = self.expected_2d_fwd.copy()
        self.expected_2d_fwd_no_nan_check[
            np.isnan(self.expected_2d_fwd_no_nan_check)
        ] = -999
        np.testing.assert_array_equal(
            transformed_no_nan_check, self.expected_2d_fwd_no_nan_check
        )

    def test_backward_fill_2d(self):
        """Test backward fill for 2D array."""
        imputer = DirectionalImputer(direction="backward")
        transformed = imputer.fit_transform(self.data_2d_nan.copy())
        self.assertTrue(np.isnan(transformed[2, 1]))  # Trailing NaN
        transformed_no_nan_check = transformed.copy()
        transformed_no_nan_check[np.isnan(transformed_no_nan_check)] = -999
        self.expected_2d_bwd_no_nan_check = self.expected_2d_bwd.copy()
        self.expected_2d_bwd_no_nan_check[
            np.isnan(self.expected_2d_bwd_no_nan_check)
        ] = -999
        np.testing.assert_array_equal(
            transformed_no_nan_check, self.expected_2d_bwd_no_nan_check
        )

    def test_forward_fill_mixed_object(self):
        """Test forward fill for mixed object array."""
        imputer = DirectionalImputer(direction="forward")
        transformed = imputer.fit_transform(self.data_mixed_object.copy())
        # Check remaining NaNs (np.nan or None)
        self.assertTrue(
            pd.isna(transformed[0, 2])
        )  # Original NaN was not preceded by non-NaN
        self.assertTrue(
            pd.isna(transformed[1, 1])
        )  # Original None was not preceded by non-None in its column

        # For comparison, replace NaNs/Nones with a placeholder string
        expected_comp = np.where(
            pd.isna(self.expected_mixed_fwd), "__NAN__", self.expected_mixed_fwd
        )
        transformed_comp = np.where(pd.isna(transformed), "__NAN__", transformed)
        np.testing.assert_array_equal(transformed_comp, expected_comp)

    def test_backward_fill_mixed_object(self):
        """Test backward fill for mixed object array."""
        imputer = DirectionalImputer(direction="backward")
        transformed = imputer.fit_transform(self.data_mixed_object.copy())
        self.assertTrue(
            pd.isna(transformed[2, 2])
        )  # Original NaN was not succeeded by non-NaN

    def test_leading_nan_column_no_change(self):
        """Test filling leading NaN column with no change."""
        imputer_fwd = DirectionalImputer(direction="forward")
        transformed_fwd = imputer_fwd.fit_transform(self.data_leading_nan_col.copy())
        np.testing.assert_array_equal(transformed_fwd, self.expected_leading_fwd)

        imputer_bwd = DirectionalImputer(direction="backward")
        transformed_bwd = imputer_bwd.fit_transform(self.data_leading_nan_col.copy())
        # Backward fill on a column that is entirely NaN (or starts with NaNs and has nothing below)
        # will also leave NaNs if nothing to fill from.
        # For column 0 of self.data_leading_nan_col, it's all NaN. So it remains NaN.
        expected_bwd = np.array(
            [[np.nan, 1], [np.nan, 2]], dtype=float
        )  # Correct expectation
        np.testing.assert_array_equal(transformed_bwd, expected_bwd)

    def test_fit_transform_equivalence(self):
        """Test fit-transform equivalence."""
        imputer1 = DirectionalImputer(direction="forward")
        imputer2 = DirectionalImputer(direction="forward")
        data = self.data_2d_nan.copy()
        transformed_fit_then_transform = imputer1.fit(data).transform(data)
        transformed_fit_transform = imputer2.fit_transform(data)
        np.testing.assert_array_equal(
            transformed_fit_then_transform, transformed_fit_transform
        )


class TestInterpolationImputer(BaseTest):
    """Unit test for the InterpolationImputer class in the imputation module."""

    @classmethod
    def setUpClass(cls):  # noqa: D102
        print("\nTesting InterpolationImputer", end="", flush=True)

    def setUp(self):  # noqa: D102
        self.data_1d_linear = np.array([1, np.nan, 3, np.nan, np.nan, 6], dtype=float)
        self.expected_1d_linear = np.array([1, 2, 3, 4, 5, 6], dtype=float)

        self.data_2d_linear = np.array(
            [[1, 10], [np.nan, np.nan], [3, 30]], dtype=float
        )
        self.expected_2d_linear = np.array([[1, 10], [2, 20], [3, 30]], dtype=float)

        self.data_1d_poly_deg2 = np.array(
            [0, np.nan, 8, np.nan, 32], dtype=float
        )  # y = 2*x_idx^2
        self.expected_1d_poly_deg2 = np.array([0, 2, 8, 18, 32], dtype=float)

        self.data_not_enough_points = np.array([1, np.nan, np.nan], dtype=float)
        self.data_all_nan_col = np.array([[1, np.nan], [2, np.nan]], dtype=float)
        self.non_numeric_data = np.array([["a", np.nan], ["b", "c"]], dtype=object)

    def test_transform_before_fit(self):
        """Test transform before fit."""
        imputer = InterpolationImputer(warn=False)
        with self.assertRaises(RuntimeError):
            imputer.transform(self.data_1d_linear)

    def test_invalid_method(self):
        """Test invalid method."""
        with self.assertRaises(ValueError):
            InterpolationImputer(method="cubic", warn=False)

    def test_invalid_degree(self):
        """Test invalid degree."""
        with self.assertRaises(ValueError):
            InterpolationImputer(method="polynomial", degree=-1, warn=False)
        with self.assertRaises(ValueError):
            InterpolationImputer(method="polynomial", degree=1.5, warn=False)

    def test_linear_interpolation_1d(self):
        """Test linear interpolation for 1D array."""
        imputer = InterpolationImputer(method="linear", warn=False)
        transformed = imputer.fit_transform(self.data_1d_linear.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_almost_equal(transformed, self.expected_1d_linear)

    def test_linear_interpolation_2d(self):
        """Test linear interpolation for 2D array."""
        imputer = InterpolationImputer(method="linear", warn=False)
        transformed = imputer.fit_transform(self.data_2d_linear.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_almost_equal(transformed, self.expected_2d_linear)

    def test_polynomial_interpolation_1d_deg2(self):
        """Test polynomial interpolation for 1D array, degree 2."""
        imputer = InterpolationImputer(method="polynomial", degree=2, warn=False)
        transformed = imputer.fit_transform(self.data_1d_poly_deg2.copy())
        assert_no_float_nan(transformed)
        np.testing.assert_array_almost_equal(transformed, self.expected_1d_poly_deg2)

    def test_interpolation_not_enough_points(self):
        """Test interpolation with not enough points."""
        imputer_linear = InterpolationImputer(method="linear", warn=False)
        # Suppress warnings for this test as it's expected
        with warnings.catch_warnings(record=True) as _w:
            warnings.simplefilter("always")
            transformed = imputer_linear.fit_transform(
                self.data_not_enough_points.copy()
            )
        # Expect NaNs to remain where interpolation couldn't happen
        self.assertTrue(np.isnan(transformed[1]))
        self.assertTrue(np.isnan(transformed[2]))

        imputer_poly = InterpolationImputer(method="polynomial", degree=1, warn=False)
        with warnings.catch_warnings(record=True) as _w:
            warnings.simplefilter("always")
            transformed_poly = imputer_poly.fit_transform(
                self.data_not_enough_points.copy()
            )
        self.assertTrue(np.isnan(transformed_poly[1]))
        self.assertTrue(np.isnan(transformed_poly[2]))

    def test_interpolation_all_nan_column(self):
        """Test interpolation with all NaN column."""
        imputer = InterpolationImputer(method="linear", warn=False)
        with warnings.catch_warnings(record=True) as _w:
            warnings.simplefilter("always")
            transformed = imputer.fit_transform(self.data_all_nan_col.copy())
        # Expect NaNs to remain in the all-NaN column
        self.assertTrue(np.isnan(transformed[:, 1]).all())
        self.assertFalse(np.isnan(transformed[:, 0]).any())  # First col should be fine

    def test_non_numeric_input(self):
        """Test non-numeric input."""
        imputer = InterpolationImputer(method="linear", warn=False)
        with self.assertRaises(
            TypeError
        ):  # "InterpolationImputer requires numeric input data."
            imputer.fit_transform(self.non_numeric_data.copy())

    def test_fit_transform_equivalence(self):
        """Test fit-transform equivalence."""
        imputer1 = InterpolationImputer(method="linear", warn=False)
        imputer2 = InterpolationImputer(method="linear", warn=False)
        data = self.data_2d_linear.copy()
        transformed_fit_then_transform = imputer1.fit(data).transform(data)
        transformed_fit_transform = imputer2.fit_transform(data)
        np.testing.assert_array_almost_equal(
            transformed_fit_then_transform, transformed_fit_transform
        )


class TestKNNImputer(BaseTest):
    """Unit test for the KNNImputer class in the imputation module."""

    @classmethod
    def setUpClass(cls):  # noqa: D102
        print("\nTesting KNNImputer", end="", flush=True)

    def setUp(self):  # noqa: D102
        # Data for KNN needs to be simple enough to trace or check properties
        self.numeric_data = np.array(
            [
                [1, 2, np.nan],
                [1.1, 2.1, 5.0],
                [7, 8, 9],
                [7.1, 8.1, np.nan],
                [np.nan, 14, 15],
            ],
            dtype=float,
        )
        self.categorical_data = np.array(
            [
                ["a", "x", np.nan],
                ["a", "y", "p"],
                ["b", "x", "q"],
                ["b", "y", np.nan],
                [np.nan, "z", "p"],
            ],
            dtype=object,
        )
        self.mixed_data = np.array(
            [
                [1, "x", np.nan],
                [1, "y", 3.0],
                ["cat", "x", 5.0],
                [4, np.nan, np.nan],
                [np.nan, "z", 7.0],
            ],
            dtype=object,
        )

        self.df_mixed = pd.DataFrame(self.mixed_data, columns=["F1", "F2", "F3"])

        self.all_missing_col_data = np.array([[1, np.nan], [2, np.nan]], dtype=float)
        self.not_enough_training_samples = np.array(
            [[1, 2, np.nan], [2, 3, np.nan], [3, 4, 5]], dtype=float
        )

    def test_transform_before_fit(self):
        """Test transform before fit."""
        imputer = KNNImputer(warn=False)
        with self.assertRaises(RuntimeError):
            imputer.transform(self.numeric_data)

    def test_invalid_n_neighbors(self):
        """Test invalid n_neighbors."""
        with self.assertRaises(ValueError):
            KNNImputer(n_neighbors=0, warn=False)

    def test_invalid_distance_metric(self):
        """Test invalid distance_metric."""
        with self.assertRaises(ValueError):
            KNNImputer(distance_metric="cosine", warn=False)

    def test_numeric_imputation(self):
        """Test numeric imputation."""
        # Using small k to make it somewhat predictable, but exact values are complex
        imputer = KNNImputer(n_neighbors=1, warn=False)
        transformed = imputer.fit_transform(self.numeric_data.copy())
        assert_no_float_nan(transformed)  # Main check: no NaNs left
        self.assertEqual(transformed.shape, self.numeric_data.shape)
        # Check dtypes, should be numeric
        self.assertTrue(np.issubdtype(transformed.dtype, np.number))

    def test_categorical_imputation(self):
        """Test categorical imputation."""
        imputer = KNNImputer(n_neighbors=1, warn=False)
        transformed = imputer.fit_transform(self.categorical_data.copy())
        assert_no_float_nan(transformed)
        self.assertEqual(transformed.shape, self.categorical_data.shape)
        # Check dtypes, could be object
        self.assertEqual(transformed.dtype, object)

    def test_mixed_data_imputation(self):
        """Test mixed data imputation."""
        imputer = KNNImputer(n_neighbors=1, warn=False)
        transformed = imputer.fit_transform(self.mixed_data.copy())
        assert_no_float_nan(transformed)
        self.assertEqual(transformed.shape, self.mixed_data.shape)
        self.assertEqual(transformed.dtype, object)  # Likely object due to mix

    def test_dataframe_input(self):
        """Test dataframe input."""
        with self.assertRaises(TypeError):
            imputer = KNNImputer(n_neighbors=1, warn=False)
            imputer.fit_transform(self.df_mixed.copy())

    def test_all_missing_column_uses_initial_fill(self):
        """Test all-NaN column uses initial fill."""
        # KNNImputer relies on StatisticalImputer for initial fill.
        # If a column is all NaN initially, stat imputer fills (e.g. 0 or 'missing').
        # KNN step for that column would have no training data, so it should keep initial fill.
        imputer = KNNImputer(n_neighbors=1, warn=False)
        with warnings.catch_warnings(
            record=True
        ) as _w:  # Catch "Not enough samples" warning
            warnings.simplefilter("always")
            transformed = imputer.fit_transform(self.all_missing_col_data.copy())

        assert_no_float_nan(transformed)
        # Expected is based on initial StatImputer fill for all-NaN numeric col (mean -> 0)
        expected = np.array([[1, 0], [2, 0]], dtype=float)
        np.testing.assert_array_almost_equal(transformed, expected)

    def test_not_enough_training_samples_for_knn(self):
        """Test not enough training samples for KNN."""
        # Column 2 has only one non-NaN value. If k > 1, KNN cannot be trained.
        # Uses initial fill for that column.
        imputer = KNNImputer(
            n_neighbors=2, warn=False
        )  # n_neighbors > non-NaN count (1) for col 2

        # Suppress warning about "Not enough samples"
        with warnings.catch_warnings(record=True) as _w:
            warnings.simplefilter("always")
            transformed = imputer.fit_transform(self.not_enough_training_samples.copy())

        assert_no_float_nan(transformed)
        self.assertEqual(transformed.shape, self.not_enough_training_samples.shape)
        # The values in the third column for NaN rows should be the mean of that column (5)
        # Initial mean for col 2 is 5.0.
        # So NaNs in col 2 should be 5.0.
        self.assertAlmostEqual(transformed[0, 2], 5.0)
        self.assertAlmostEqual(transformed[1, 2], 5.0)
        self.assertAlmostEqual(transformed[2, 2], 5.0)  # Original value

    def test_fit_transform_equivalence(self):
        """Test fit-transform equivalence."""
        imputer1 = KNNImputer(n_neighbors=1, warn=False)
        imputer2 = KNNImputer(n_neighbors=1, warn=False)
        data = self.numeric_data.copy()  # Use a simpler numeric case

        transformed_fit_then_transform = imputer1.fit(data).transform(data)
        transformed_fit_transform = imputer2.fit_transform(data)

        # KNN can be sensitive, so allow for small differences if float
        if transformed_fit_then_transform.dtype.kind == "f":
            np.testing.assert_array_almost_equal(
                transformed_fit_then_transform, transformed_fit_transform, decimal=5
            )
        else:
            np.testing.assert_array_equal(
                transformed_fit_then_transform, transformed_fit_transform
            )


class TestCustomImputer(BaseTest):
    """Unit test for the CustomImputer class in the imputation module."""

    @classmethod
    def setUpClass(cls):  # noqa: D102
        print("\nTesting CustomImputer", end="", flush=True)

    def setUp(self):  # noqa: D102
        self.numeric_data = np.array(
            [[1, 2, np.nan], [1.1, 2.1, 5.0], [7, 8, 9], [np.nan, 14, 15]], dtype=float
        )
        self.categorical_data = np.array(
            [["a", "x", np.nan], ["a", "y", "p"], ["b", "x", "q"], [np.nan, "z", "p"]],
            dtype=object,
        )
        self.mixed_data = np.array(
            [
                [1.0, "x", np.nan],
                [np.nan, "y", 3.0],
                [2.0, "x", 5.0],
                [4.0, np.nan, np.nan],
            ],
            dtype=object,
        )
        self.df_mixed = pd.DataFrame(self.mixed_data, columns=["F1", "F2", "F3"])

        # Mock regressors/classifiers
        self.mock_regressor = MockRegressor(constant_prediction=99.0)
        self.mock_classifier = MockClassifier(constant_prediction="0")

        # Actual estimators from sega_learn for more realistic tests
        self.actual_regressor = OrdinaryLeastSquares()
        self.actual_classifier = LogisticRegression(learning_rate=0.01, max_iter=10)

    def test_transform_before_fit(self):
        """Test transform before fit."""
        imputer = CustomImputer(regressor=self.mock_regressor)
        with self.assertRaises(RuntimeError):
            imputer.transform(self.numeric_data)

    def test_no_estimator_provided(self):
        """Test no estimator provided."""
        with self.assertRaises(ValueError):
            CustomImputer(warn=False)

    def test_invalid_estimator_type(self):
        """Test invalid estimator type."""
        with self.assertRaises(TypeError):
            CustomImputer(regressor="not_an_estimator", warn=False)
        with self.assertRaises(TypeError):
            CustomImputer(classifier=lambda x: x, warn=False)  # Missing fit/predict

    def test_numeric_imputation_with_mock_regressor(self):
        """Test numeric imputation with mock regressor."""
        imputer = CustomImputer(regressor=self.mock_regressor, warn=False)
        transformed = imputer.fit_transform(self.numeric_data.copy())
        assert_no_float_nan(transformed)
        self.assertEqual(transformed.shape, self.numeric_data.shape)
        # Check if mock regressor's constant prediction was used
        # NaN at (0,2) should be 99.0. NaN at (3,0) should be 99.0
        self.assertAlmostEqual(transformed[0, 2], 99.0)
        self.assertAlmostEqual(transformed[3, 0], 99.0)
        # Original values should remain
        self.assertAlmostEqual(transformed[0, 0], 1.0)
        self.assertAlmostEqual(transformed[1, 2], 5.0)

    def test_categorical_imputation_with_mock_classifier(self):
        """Test categorical imputation with mock classifier."""
        imputer = CustomImputer(classifier=self.mock_classifier, warn=True)
        transformed = imputer.fit_transform(self.categorical_data.copy())
        assert_no_float_nan(transformed)
        self.assertEqual(transformed.shape, self.categorical_data.shape)

    def test_mixed_data_imputation_with_mocks(self):
        """Test mixed data imputation with mock regressor and classifier."""
        imputer = CustomImputer(
            regressor=self.mock_regressor, classifier=self.mock_classifier, warn=False
        )
        transformed = imputer.fit_transform(self.mixed_data.copy())
        assert_no_float_nan(transformed)
        self.assertEqual(transformed.shape, self.mixed_data.shape)

    def test_mixed_data_with_actual_estimators(self):
        """Test mixed data imputation with actual regressor and classifier."""
        # This test is more of an integration test for CustomImputer with sega_learn estimators
        imputer = CustomImputer(
            regressor=self.actual_regressor,
            classifier=self.actual_classifier,
            one_hot_encode_features=True,
            warn=False,
        )
        # Need a dataset where actual estimators can converge reasonably
        # Using a slightly modified mixed_data for predictability if possible
        data = np.array(
            [
                [1.0, "A", 10.0],
                [2.0, "B", np.nan],  # Regressor for F3
                [np.nan, "A", 30.0],  # Regressor for F1
                [4.0, np.nan, 40.0],  # Classifier for F2
                [5.0, "B", 50.0],
            ],
            dtype=object,
        )

        with (
            warnings.catch_warnings()
        ):  # Suppress potential convergence warnings from LogisticRegression
            warnings.simplefilter("ignore")
            transformed = imputer.fit_transform(data.copy())

        assert_no_float_nan(transformed)
        self.assertEqual(transformed.shape, data.shape)

    def test_no_one_hot_encode_features(self):
        """Test no one-hot encoding."""
        # If one_hot_encode_features=False, estimator must handle mixed types.
        # Mock estimators here don't care about feature types.
        imputer = CustomImputer(
            regressor=self.mock_regressor, one_hot_encode_features=False, warn=False
        )
        transformed = imputer.fit_transform(
            self.mixed_data.copy()
        )  # mixed_data has strings and numbers
        assert_no_float_nan(transformed)
        # Check if numeric NaNs were filled by mock regressor
        self.assertAlmostEqual(transformed[1, 0], 99.0)  # F1 is numeric
        self.assertAlmostEqual(transformed[0, 2], 99.0)  # F3 is numeric
        self.assertAlmostEqual(transformed[3, 2], 99.0)  # F3 is numeric
        # Categorical NaN in F2 should remain or be filled by initial mode if no classifier
        # Current mock_regressor is only one provided.
        # Initial mode for F2 ('x', 'y', 'x', nan) -> 'x'
        self.assertEqual(transformed[3, 1], "x")

    def test_fit_transform_equivalence(self):
        """Test fit-transform equivalence."""
        imputer1 = CustomImputer(
            regressor=self.mock_regressor, classifier=self.mock_classifier, warn=False
        )
        imputer2 = CustomImputer(
            regressor=self.mock_regressor, classifier=self.mock_classifier, warn=False
        )
        data = self.mixed_data.copy()

        transformed_fit_then_transform = imputer1.fit(data).transform(data)
        transformed_fit_transform = imputer2.fit_transform(data)

        # Compare element-wise due to mixed types
        self.assertEqual(
            transformed_fit_then_transform.shape, transformed_fit_transform.shape
        )
        for r in range(transformed_fit_then_transform.shape[0]):
            for c in range(transformed_fit_then_transform.shape[1]):
                val1, val2 = (
                    transformed_fit_then_transform[r, c],
                    transformed_fit_transform[r, c],
                )
                if isinstance(val1, float) and isinstance(val2, float):
                    self.assertAlmostEqual(val1, val2, msg=f"Mismatch at ({r},{c})")
                else:
                    self.assertEqual(val1, val2, msg=f"Mismatch at ({r},{c})")


if __name__ == "__main__":
    unittest.main()
