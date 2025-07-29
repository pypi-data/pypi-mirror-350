[![PyPI version](https://badge.fury.io/py/xarray-regressions.svg)](https://badge.fury.io/py/xarray-regressions)
[![Build status](https://github.com/aazuspan/xarray-regressions/actions/workflows/ci.yaml/badge.svg)](https://github.com/aazuspan/xarray-regressions/actions/workflows/ci.yaml)
[![Documentation Status](https://readthedocs.org/projects/xarray-regressions/badge/?version=latest)](https://xarray-regressions.readthedocs.io/en/latest/?badge=latest)

A [pytest-regressions](https://pytest-regressions.readthedocs.io/en/latest/overview.html) plugin for identifying regressions in [Xarray](https://docs.xarray.dev/en/stable/) objects.

## Install

```
pip install xarray-regressions
```

## Usage

If you're unfamiliar with `pytest-regressions`, check out [their documentation](https://pytest-regressions.readthedocs.io/en/latest/overview.html) first. `xarray-regressions` registers a compatible test fixture `xarray_regression` for detecting regressions in the data or metadata of `xr.DataArray` and `xr.Dataset` objects.

```python
from xarray_regressions import XarrayRegressionFixture
import xarray as xr

def make_dataarray() -> xr.DataArray:
    """A dummy method that needs to be tested."""
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


def test_make_dataarray(xarray_regression: XarrayRegressionFixture):
    """Test that the function always returns an identical xr.DataArray."""
    da = make_dataarray()
    xarray_regression.check(
        da,
        check_names=True,
        check_attrs=True,
    )
```

Once the test is initialized and the expected result is stored in a NetCDF file, `test_make_dataarray` will fail if the generated `xr.DataArray` changes in a future run.

`xarray_regression.check` uses [xr.testing.assert_equal](https://docs.xarray.dev/en/stable/generated/xarray.testing.assert_equal.html) to compare equality of values, dimensions, and coordinates. If `atol` or `rtol` are provided, it will use [xr.testing.assert_allclose](https://docs.xarray.dev/en/latest/generated/xarray.testing.assert_allclose.html) instead. Names and attributes are checked separately. Encodings are not currently checked.
