import pytest
from pathlib import Path

from .fixture import XarrayRegressionFixture


@pytest.fixture
def xarray_regression(
    datadir: Path, original_datadir: Path, request: pytest.FixtureRequest
) -> XarrayRegressionFixture:
    return XarrayRegressionFixture(
        datadir=datadir,
        original_datadir=original_datadir,
        request=request,
    )
