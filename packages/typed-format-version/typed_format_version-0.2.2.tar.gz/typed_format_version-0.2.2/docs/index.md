<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# typed-format-version: load format.version.{major,minor} from a structured file.

## DEPRECATED in favor of media-type-version

This library is deprecated.
The author is not aware of any other libraries and programs using it, and
he himself has moved on to using a `mediaType` declaration to specify both
the format and its version.
See [the media-type-version Python library][pypi-media-type-version] and
[the media-type-version Rust crate][crates-io-media-type-version] for
more information.

## Overview

\[[Home][ringlet] | [Source][gitlab] | [Python API](api-python.md) | [Rust API][rustdoc-top] | [ReadTheDocs][readthedocs] | [PyPI][pypi] | [crates.io][crates-io]\]

This library tries to parse a format.version "section" in some raw data that
may have been loaded from a configuration file, and determines whether that
section contains valid "major" and "minor" integer values. The caller can
then choose the correct schema to validate the loaded data against, e.g. by
using the `typedload` library with the correct top-level dataclass definition.

The most commonly used function will probably be `get_version()`
([Python][typed_format_version.get_version], [Rust][rustdoc-get-version-from-str]): it takes
a raw data dictionary and returns a `Version`
([Python][typed_format_version.Version], [Rust][rustdoc-Version]) object with a `major` and `minor`
integer attributes, if the data contained a valid "format" dictionary with
a "version" dictionary within it. The Python `get_version()` function can also
remove the top-level "format" member, if a true value is passed for the `pop`
argument.

[rustdoc-top]: https://docs.rs/typed-format-version/latest/typed_format_version/
[rustdoc-get-version-from-str]: https://docs.rs/typed-format-version/latest/typed_format_version/fn.get_version_from_str.html
[rustdoc-Version]: https://docs.rs/typed-format-version/latest/typed_format_version/struct.Version.html

## Python examples

Load some data from a file, make sure it is in the correct format:

``` py
    try:
        raw = json.load(pathlib.Path(cfgfile).open())
        ver = typed_format_version.get_version(raw)
    except (OSError, ValueError) as err:
        sys.exit(f"Invalid data format for {cfgfile}: {err}")
    if ver.as_version_tuple() != (0, 2):
        sys.exit("Only config format 0.2 supported right now")
    cfg = typedload.load(raw, ConfigData)
```

Determine the best version to validate against, allowing more fields to be
added in minor versions that we do not know about yet:

``` py
    SCHEMAS = {
        (0, 1): ConfigTop_0_1,
        (0, 2): ConfigTop_0_2,
        (1, 0): ConfigTop_1_0,
    }
    try:
        raw = json.load(pathlib.Path(cfgfile).open())
        exact_ver = typed_format_version.get_version(raw)
        mver = typed_format_version.determine_version_match(exact_ver, SCHEMAS)
    except (OSError, ValueError) as err:
        sys.exit(f"Invalid data format for {cfgfile}: {err}")
    
    # Either load the data directly...
    cfg = typedload.load(raw, SCHEMAS[mver.version], failonextra=mver.failonextra)
    
    # ...or do something with mver.version, possibly examining ver further and
    # "upgrading" the loaded configuration from earlier versions by e.g.
    # adding default values for fields or reshaping the data.
```

## Rust examples

Load some data from a file, make sure it is in the correct format:

``` rust
    use std::fs;
    
    use anyhow::{bail, Context};
    
    let contents = fs::read_to_string(&infile).with_context(|| format!("Could not read {}", infile.display()))?;
    let fver = typed_format_version::get_version_from_str(&contents, serde_json::from_str)
        .with_contedxt(|| format!("Could not parse format.version from {}", infile.display()))?;
    if (fver.major(), fver.minor()) != (0, 2) {
        bail!("Only config format 0.2 supported right now");
    }
    let cfg: ConfigData = serde_json::from_str(&contents)
        .with_context(|| format!("Could not parse {}", infile.display()))?;
```

Upgrade from an earlier versions of the data format:

``` rust
    let cfg = match fver.major() {
        0 => {
            let cfg_0: ConfigData_0 = serde_json::from_str(&contents)
                .with_context(|| format!("Could not parse {}", infile.display()))?;
            upgrade_from_version_0(cfg_0)
        },
        1 => serde_json::from_str::<ConfigData>(&contents)
            .with_context(|| format!("Could not parse {}", infile.display()))?,
        _ => bail!(format!("Unexpected major format version {}", fver.major()),
    };
```

## Contact

The `typed-format-version` library is developed in
[a GitLab repository][gitlab] and hosted [at Ringlet][ringlet].
It was written by [Peter Pentchev][roam].

[gitlab]: https://gitlab.com/ppentchev/typed-format-version "The typed-format-version GitLab repository"
[ringlet]: https://devel.ringlet.net/devel/typed-format-version/ "The typed-format-version Ringlet homepage"
[readthedocs]: https://typed-format-version.readthedocs.io/ "The typed-format-version ReadTheDocs page"
[pypi]: https://pypi.org/project/typed-format-version/ "The typed-format-version module on PyPI"
[crates-io]: https://crates.io/crates/typed-format-version "The typed-format-version crate on crates.io"
[pypi-media-type-version]: https://pypi.org/project/media-type-version "The media-type-version Python library"
[crates-io-media-type-version]: https://crates.io/crates/media-type-version "The media-type-version Rust crate"
[roam]: mailto:roam@ringlet.net "Peter Pentchev"
