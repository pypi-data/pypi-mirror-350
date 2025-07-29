from __future__ import annotations

from typing import Any, Callable, TypeVar

from pathlib import Path
import os
import pytest
from pytest_regressions.common import perform_regression_check
import xarray as xr
from xarray.core.utils import dict_equiv
from xarray.core.formatting import diff_attrs_repr

XarrayType = TypeVar("XarrayType", bound=xr.DataArray | xr.Dataset)


def assert_attrs_equal(a: XarrayType, b: XarrayType) -> None:
    assert dict_equiv(a.attrs, b.attrs), diff_attrs_repr(a.attrs, b.attrs, "identical")


def assert_names_equal(a: xr.DataArray, b: xr.DataArray) -> None:
    assert a.name == b.name, f"DataArray names are different. L: {a.name}, R: {b.name}"


class XarrayRegressionFixture:
    def __init__(
        self,
        datadir: Path,
        original_datadir: Path,
        request: pytest.FixtureRequest,
    ) -> None:
        self.request = request
        self.datadir = datadir
        self.original_datadir = original_datadir
        self.force_regen = False
        self.with_test_class_names = False

    def _get_load_fn(self, obj):
        if isinstance(obj, xr.DataArray):
            return xr.open_dataarray
        elif isinstance(obj, xr.Dataset):
            return xr.open_dataset
        else:
            msg = (
                f"Object of type `{obj.__class__.__name__}` has no default loading "
                "function. The object may be unsupported or require explicitly passing "
                "your own `load_fn`."
            )
            raise ValueError(msg)

    def check(
        self,
        obj: XarrayType,
        *,
        basename: str | None = None,
        fullpath: os.PathLike[str] | None = None,
        rtol: float | None = None,
        atol: float | None = None,
        check_attrs: bool = True,
        check_names: bool = True,
        load_fn: Callable[[Path], XarrayType] | None = None,
        load_kwargs: dict[str, Any] | None = None,
        dump_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """
        Check an xarray object against a previously recorded one, or generate a new file.
        """
        ___tracebackhide__ = True  # noqa: F841

        if load_fn is None:
            load_fn = self._get_load_fn(obj)
        load_kwargs = load_kwargs or {}
        dump_kwargs = dump_kwargs or {}
        atol = atol or 0.0
        rtol = rtol or 0.0

        def check_fn(obtained_filename: Path, expected_filename: Path) -> None:
            obtained_data = load_fn(obtained_filename, **load_kwargs)
            expected_data = load_fn(expected_filename, **load_kwargs)
            if check_names and isinstance(obj, xr.DataArray):
                assert_names_equal(obtained_data, expected_data)
            if rtol or atol:
                xr.testing.assert_allclose(
                    obtained_data, expected_data, rtol=rtol, atol=atol
                )
            else:
                xr.testing.assert_equal(obtained_data, expected_data)
            if check_attrs:
                assert_attrs_equal(obtained_data, expected_data)

        def dump_fn(filename: Path) -> None:
            obj.to_netcdf(filename, **dump_kwargs)

        perform_regression_check(
            datadir=self.datadir,
            original_datadir=self.original_datadir,
            request=self.request,
            check_fn=check_fn,
            dump_fn=dump_fn,
            extension=".nc",
            basename=basename,
            fullpath=fullpath,
            force_regen=self.force_regen,
            with_test_class_names=self.with_test_class_names,
        )
