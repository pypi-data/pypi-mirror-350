# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test selecting an appropriate version to validate against."""

import dataclasses
import functools
from typing import List, Tuple

import pytest
import typed_format_version

from . import util


@dataclasses.dataclass(frozen=True)
class SelectCase:
    """A single test case of select-version data."""

    version: typed_format_version.Version
    result: typed_format_version.VersionMatch


@dataclasses.dataclass(frozen=True)
class SelectInfo:
    """The information about the select-version test cases."""

    versions: List[typed_format_version.Version]
    cases: List[SelectCase]


@dataclasses.dataclass(frozen=True)
class SelectData:
    """The top-level structure of the select.toml file."""

    select: SelectInfo


@functools.lru_cache
def load_select() -> List[Tuple[List[typed_format_version.Version], SelectCase]]:
    """Load the select-version test cases."""
    raw = util.toml_load("select.toml")
    ver, top = typed_format_version.get_version_t_and_load(
        raw,
        SelectData,
        pop=True,
        failonextra=True,
    )
    assert ver == (1, 0)
    return [(top.select.versions, tcase) for tcase in top.select.cases]


@pytest.mark.parametrize(("versions", "tcase"), load_select())
def test_select(versions: List[typed_format_version.Version], tcase: SelectCase) -> None:
    """Make sure that the correct format version is chosen."""
    assert (
        typed_format_version.determine_version_match(
            tcase.version,
            {(ver.major, ver.minor): None for ver in versions},
        )
        == tcase.result
    )
