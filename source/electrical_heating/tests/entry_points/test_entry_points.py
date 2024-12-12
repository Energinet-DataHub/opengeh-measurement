﻿import pytest

from electrical_heating_job import entry_points as module


@pytest.mark.parametrize(
    "entry_point_name",
    [
        "execute",
    ],
)
def test__entry_point_exists(
    installed_package: None,
    entry_point_name: str,
) -> None:
    from source.test_common import assert_entry_point_exists

    assert_entry_point_exists(entry_point_name, module)
