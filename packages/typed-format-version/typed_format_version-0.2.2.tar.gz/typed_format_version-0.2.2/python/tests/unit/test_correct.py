# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test typed-format-version with a couple of valid data files."""

import dataclasses
import functools
from typing import Any, Dict

import pytest
import typed_format_version

from . import util


@dataclasses.dataclass(frozen=True)
class CorrectCase:
    """A single test case for correctly-formatted data."""

    raw: Dict[str, Any]
    version: typed_format_version.Version
    data: Dict[str, Any]


@dataclasses.dataclass(frozen=True)
class CorrectData:
    """The top-level structure of the correct.toml file."""

    correct: Dict[str, CorrectCase]


@functools.lru_cache
def load_good() -> Dict[str, CorrectCase]:
    """Load the valid test cases."""
    raw = util.toml_load("correct.toml")
    ver, top = typed_format_version.get_version_t_and_load(
        raw,
        CorrectData,
        pop=True,
        failonextra=True,
    )
    assert ver == (1, 0)
    return top.correct


@pytest.mark.parametrize("tcase", load_good().values(), ids=load_good().keys())
def test_good(tcase: CorrectCase) -> None:
    """Make sure that loading the format data succeeds."""
    raw = dict(tcase.raw)
    ver = typed_format_version.get_version(raw, pop=True)
    assert (ver, raw) == (tcase.version, tcase.data)
