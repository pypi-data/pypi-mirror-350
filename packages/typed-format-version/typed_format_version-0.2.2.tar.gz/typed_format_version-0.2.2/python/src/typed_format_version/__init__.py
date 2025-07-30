# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""typed-format-version: load format.version.{major,minor} from a structured file.

This module tries to parse a format.version "section" in some raw data that
may have been loaded from a configuration file, and determines whether that
section contains valid "major" and "minor" integer values. The caller can
then choose the correct schema to validate the loaded data against, e.g. by
using the `typedload` library with the correct top-level dataclass definition.

The most commonly used function will probably be `get_version()`: it takes
a raw data dictionary and returns a `Version` object with a `major` and `minor`
integer attributes, if the data contained a valid "format" dictionary with
a "version" dictionary within it. Optionally the `get_version()` function can
remove the top-level "format" member, if a true value is passed for the `pop`
argument.
"""

import dataclasses
from typing import Any, Dict, NamedTuple, Tuple, Type, TypeVar

import typedload


class VersionTuple(NamedTuple):
    """The format version number as a tuple for easier comparison and matching."""

    major: int
    """The major version number."""

    minor: int
    """The minor version number."""


@dataclasses.dataclass(frozen=True)
class Version:
    """The format version number."""

    major: int
    """The major version number."""

    minor: int
    """The minor version number."""

    def as_version_tuple(self) -> VersionTuple:
        """Convert to a tuple for easier comparison and matching."""
        return VersionTuple(major=self.major, minor=self.minor)


@dataclasses.dataclass(frozen=True)
class Format:
    """The format specification."""

    version: Version
    """The format version."""


@dataclasses.dataclass(frozen=True)
class VersionMatch:
    """Matched version number and exactness."""

    version: Version
    """The matched version number."""

    failonextra: bool
    """True if the match was exact, false if the minor version number was higher."""


VERSION = "0.2.2"
"""The `typed_format_version` library's version."""

_T = TypeVar("_T")


@dataclasses.dataclass
class LoadError(ValueError):
    """An error that occurred while looking for the format.version tuple."""


@dataclasses.dataclass
class FormatExtractError(LoadError):
    """Could not extract the "format" element from the raw data."""

    err: Exception
    """The error that occurred."""

    def __str__(self) -> str:
        """Return a human-readable description of the error."""
        return f"Could not extract the 'format' element from the raw data: {self.err}"


@dataclasses.dataclass
class FormatParseError(LoadError):
    """Could not parse the "format" element from the raw data."""

    err: Exception
    """The error that occurred."""

    def __str__(self) -> str:
        """Return a human-readable description of the error."""
        return f"Could not parse the 'format' element from the raw data: {self.err}"


@dataclasses.dataclass
class VersionMatchError(LoadError):
    """Could not find a match for the format version in the supplied table."""

    version: Version
    """The version that we looked for."""

    err: Exception
    """The error that occurred."""

    def __str__(self) -> str:
        """Return a human-readable description of the error."""
        return f"Could not find a match for the {self.version} version: {self.err}"


def get_format(data: Dict[str, Any], *, pop: bool = False) -> Format:
    """Get the known attributes of the format member (only the version)."""
    try:
        raw = data.pop("format") if pop else data["format"]
    except (AttributeError, KeyError, TypeError) as err:
        raise FormatExtractError(err) from err

    try:
        return typedload.load(raw, Format, failonextra=False)
    except typedload.exceptions.TypedloadException as err:
        raise FormatParseError(err) from err


def get_version(data: Dict[str, Any], *, pop: bool = False) -> Version:
    """Get the major and minor format.version attributes."""
    return get_format(data, pop=pop).version


def get_version_t(data: Dict[str, Any], *, pop: bool = False) -> VersionTuple:
    """Get the major and minor format.version attributes."""
    return get_version(data, pop=pop).as_version_tuple()


def get_format_and_load(
    data: Dict[str, Any],
    dtype: Type[_T],
    *,
    pop: bool = False,
    **kwargs: Any,  # noqa: ANN401
) -> Tuple[Format, _T]:
    """Get the format attributes, load and validate the data itself."""
    fmt = get_format(data, pop=pop)
    return fmt, typedload.load(data, dtype, **kwargs)


def get_version_and_load(
    data: Dict[str, Any],
    dtype: Type[_T],
    *,
    pop: bool = False,
    **kwargs: Any,  # noqa: ANN401
) -> Tuple[Version, _T]:
    """Get the version attributes, load and validate the data itself."""
    fmt, res = get_format_and_load(data, dtype, pop=pop, **kwargs)
    return fmt.version, res


def get_version_t_and_load(
    data: Dict[str, Any],
    dtype: Type[_T],
    *,
    pop: bool = False,
    **kwargs: Any,  # noqa: ANN401
) -> Tuple[VersionTuple, _T]:
    """Get the version attributes, load and validate the data itself."""
    ver, res = get_version_and_load(data, dtype, pop=pop, **kwargs)
    return ver.as_version_tuple(), res


def determine_version_match(version: Version, schemas: Dict[Tuple[int, int], Any]) -> VersionMatch:
    """Figure out which schema to load and whether to allow extra fields.

    If there is an exact major.minor version match, return the specified
    version and set the `failonextra` field to true, so that the data
    matches the specification exactly.

    If there is no exact match, but there are versions with the same major
    number and a minor number that is lower than the specified one, then
    return the highest one among them (still lower than the specified one) and
    set the `failonextra` field to false, so as to allow extra fields ostensibly
    defined in a later format version.
    """
    major, minor = version.as_version_tuple()
    if (major, minor) in schemas:
        return VersionMatch(version=version, failonextra=True)

    try:
        highest_lower_minor = max(
            v_minor for (v_major, v_minor) in schemas if v_major == major and v_minor < minor
        )
    except ValueError as err:
        raise VersionMatchError(version, err) from err
    return VersionMatch(
        version=Version(
            major=major,
            minor=highest_lower_minor,
        ),
        failonextra=False,
    )
