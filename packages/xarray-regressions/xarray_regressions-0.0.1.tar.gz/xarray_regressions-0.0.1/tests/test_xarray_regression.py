import xarray as xr
import numpy as np

import pytest

from xarray_regressions import XarrayRegressionFixture

# TODO
# Solve the problem where --force-regen regenerates using the expected failures
# Test with some real world data that has spatial reference, fill value, etc
# Come up with a solution to test encoding
# Ideally raise better warnings that refer to what changed, rather than left versus right sides


@pytest.fixture
def dataarray() -> xr.DataArray:
    return xr.DataArray(
        np.full((2, 4, 3), 1),
        dims=["variable", "y", "x"],
        coords={
            "variable": ["var1", "var2"],
            "y": [1, 2, 3, 4],
            "x": [1, 2, 3],
        },
        name="sample_data",
        attrs={"foo": "bar"},
    )


@pytest.fixture
def dataset(dataarray) -> xr.Dataset:
    return xr.Dataset(
        {
            "var1": dataarray,
            "var2": dataarray,
        },
        coords={
            "y": [1, 2, 3, 4],
            "x": [1, 2, 3],
        },
        attrs={"foo": "bar"},
    )


def test_dataarray_regression(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataarray)


def test_dataarray_regression_with_tolerance(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    dataarray = dataarray.astype(np.float32).drop_attrs()
    xarray_regression.check(dataarray)
    rtol = 1e-5
    atol = 1e-3
    with pytest.raises(AssertionError, match="DataArray objects are not close"):
        xarray_regression.check(dataarray * (1 + rtol * 10), rtol=rtol)
    with pytest.raises(AssertionError, match="DataArray objects are not close"):
        xarray_regression.check(dataarray + atol * 10, atol=atol)

    xarray_regression.check(dataarray * (1 + rtol), rtol=rtol * 1.1)
    xarray_regression.check(dataarray + atol, atol=atol * 1.1)


def test_dataarray_regression_ignore_attrs(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataarray)
    dataarray = dataarray.assign_attrs(foo="asdf")
    xarray_regression.check(dataarray, check_attrs=False)
    dataarray = dataarray.assign_attrs(bar="baz")
    xarray_regression.check(dataarray, check_attrs=False)


def test_dataarray_regression_ignore_names(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataarray)
    dataarray = dataarray.rename("other_name")
    xarray_regression.check(dataarray, check_names=False)
    dataarray = dataarray.rename("other_name2")
    xarray_regression.check(dataarray, check_names=False)


def test_dataarray_regression_fails_with_mismatched_data(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataarray)
    with pytest.raises(AssertionError, match="DataArray objects are not equal"):
        dataarray *= 2
        xarray_regression.check(dataarray)
    with pytest.raises(AssertionError, match="DataArray objects are not equal"):
        dataarray = dataarray.astype(np.float32)
        xarray_regression.check(dataarray)


def test_dataarray_regression_fails_with_mismatched_attrs(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataarray)
    with pytest.raises(AssertionError, match="Differing attributes"):
        dataarray = dataarray.assign_attrs(foo="asdf")
        xarray_regression.check(dataarray)
    with pytest.raises(AssertionError, match=".*Attributes only on the left object"):
        dataarray = dataarray.assign_attrs(bar="baz")
        xarray_regression.check(dataarray)


def test_dataarray_regression_fails_with_mismatched_names(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataarray)
    with pytest.raises(AssertionError, match="DataArray names are different"):
        dataarray = dataarray.rename("other_name")
        xarray_regression.check(dataarray)


def test_dataarray_regression_fails_with_mismatched_dims(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataarray)
    with pytest.raises(AssertionError, match="Differing dimensions"):
        dataarray = dataarray.rename({"x": "x2"})
        xarray_regression.check(dataarray)


def test_dataarray_regression_fails_with_mismatched_coords(
    dataarray: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataarray)
    with pytest.raises(AssertionError, match="Differing coordinates"):
        dataarray = dataarray.assign_coords(x=[3, 2, 1])
        xarray_regression.check(dataarray)


def test_dataset_regression(
    dataset: xr.Dataset, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataset)


def test_dataset_regression_with_tolerance(
    dataset: xr.DataArray, xarray_regression: XarrayRegressionFixture
):
    dataset = dataset.astype(np.float32).drop_attrs()
    xarray_regression.check(dataset)
    rtol = 1e-5
    atol = 1e-3
    with pytest.raises(AssertionError, match="Dataset objects are not close"):
        xarray_regression.check(dataset * (1 + rtol * 10), rtol=rtol)
    with pytest.raises(AssertionError, match="Dataset objects are not close"):
        xarray_regression.check(dataset + atol * 10, atol=atol)

    xarray_regression.check(dataset * (1 + rtol), rtol=rtol * 1.1)
    xarray_regression.check(dataset + atol, atol=atol * 1.1)


def test_dataset_regression_ignore_attrs(
    dataset: xr.Dataset, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataset)
    dataset = dataset.assign_attrs(foo="asdf")
    xarray_regression.check(dataset, check_attrs=False)
    dataset = dataset.assign_attrs(bar="baz")
    xarray_regression.check(dataset, check_attrs=False)
    dataset["var1"] = dataset["var1"].assign_attrs(bar="baz")
    xarray_regression.check(dataset, check_attrs=False)


def test_dataset_regression_fails_with_mismatched_attrs(
    dataset: xr.Dataset, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataset)
    with pytest.raises(AssertionError, match="Differing attributes"):
        dataset = dataset.assign_attrs(foo="asdf")
        xarray_regression.check(dataset)
    with pytest.raises(AssertionError, match="Attributes only on the left object"):
        dataset = dataset.assign_attrs(bar="baz")
        xarray_regression.check(dataset)
    with pytest.raises(AssertionError, match="Attributes only on the left object"):
        dataset["var1"] = dataset["var1"].assign_attrs(bar="baz")
        xarray_regression.check(dataset)


def test_dataset_regression_fails_with_mismatched_variable_names(
    dataset: xr.Dataset, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataset)
    with pytest.raises(AssertionError, match="Data variables only on the left object"):
        dataset = dataset.rename({"var1": "other_name"})
        xarray_regression.check(dataset)


def test_dataset_regression_fails_with_mismatched_dims(
    dataset: xr.Dataset, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataset)
    with pytest.raises(AssertionError, match="Differing dimensions"):
        dataset = dataset.rename({"x": "x2"})
        xarray_regression.check(dataset)


def test_dataset_regression_fails_with_mismatched_coords(
    dataset: xr.Dataset, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataset)
    with pytest.raises(AssertionError, match="Differing coordinates"):
        dataset = dataset.assign_coords(x=[3, 2, 1])
        xarray_regression.check(dataset)


def test_dataset_regression_fails_with_mismatched_data(
    dataset: xr.Dataset, xarray_regression: XarrayRegressionFixture
):
    xarray_regression.check(dataset)
    with pytest.raises(AssertionError, match="Differing data"):
        dataset["var1"] *= 2
        xarray_regression.check(dataset)
    with pytest.raises(AssertionError, match="Differing data"):
        dataset["var1"] = dataset["var1"].astype(np.float32)
        xarray_regression.check(dataset)


def test_xarray_regression_fails_with_unsupported_type(
    xarray_regression: XarrayRegressionFixture,
):
    with pytest.raises(ValueError, match="`ndarray` has no default loading function"):
        xarray_regression.check(np.ndarray([1, 2, 3]))
