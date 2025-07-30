# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test typed-format-version with a couple of invalid data files."""

import dataclasses
import functools
from typing import Any, Dict

import pytest
import typed_format_version

from . import util


@dataclasses.dataclass(frozen=True)
class WrongData:
    """The top-level structure of the wrong.toml file."""

    wrong: Dict[str, Any]


@functools.lru_cache
def load_bad() -> Dict[str, Dict[str, Any]]:
    """Load the wrong test cases."""
    raw = util.toml_load("wrong.toml")
    ver, top = typed_format_version.get_version_t_and_load(
        raw,
        WrongData,
        pop=True,
        failonextra=True,
    )
    assert ver == (1, 0)
    return top.wrong


@pytest.mark.parametrize("data", load_bad().values(), ids=load_bad().keys())
def test_bad(data: Dict[str, Any]) -> None:
    """Make sure that loading the format data fails."""
    with pytest.raises(typed_format_version.LoadError) as err:
        typed_format_version.get_format(data)
    assert isinstance(err.value, ValueError)
