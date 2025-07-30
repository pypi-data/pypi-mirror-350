<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Changelog

All notable changes to the typed-format-version project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.2] - 2025-05-26

### DEPRECATED

- This library has been deprecated.
  See [the media-type-version Python library][pypi-media-type-version] or
  [the media-type-version Rust crate][crates-io-media-type-version] for
  the author's replacement.

### Fixes

- Python implementation:
    - test suite:
        - push the unit test suite into `python/tests/unit/` to avoid pytest masking
          packaging errors by adding `python/` to the module search path
- Documentation:
    - add the release date to the 0.2.1 changelog entry
    - fix the formatting of Markdown nested lists
    - bump the `mkdocstrings` version to fix the documentation build

### Additions

- Python implementation:
    - add more docstrings for the benefit of the Python API reference
    - declare Python 3.12 and 3.13 as supported versions
    - push the source files down into the `python/src/` subdirectory
    - test suite:
        - import the `vetox` tool for running Tox in a virtual environment
        - use `pytest` 8.x with no changes
        - use `ruff` 0.11.11:
            - shuffle the `ruff` configuration file layout
            - drop an unused override
            - reformat for trailing commas
- Rust implementation:
    - use `//` comments for the SPDX tags
    - declare MSRV 1.58, use inline format strings
    - override a couple of `Clippy` lints
    - allow `thiserror` 2.x with no changes
- Documentation:
    - add a MkDocs-based documentation tree including a Python API reference
    - add ReadTheDocs build glue
    - add a download page
    - add a deprecation notice in favor of `media-type-version`
- Nix:
    - add a Nix expression and a shell helper for running the Python tests with
      all the Python versions present in nixpkgs/unstable using the `vetox` tool
    - add a Nix expression for building and testing the Rust implementation

### Other changes

- Switch to SPDX copyright and license identifiers
- Drop the years from the copyright notices
- Python implementation:
    - minor refactoring and fixes suggested by Ruff 0.1.8
    - drop support for Python 3.7
    - switch to Ruff for source code formatting
    - introduce a hierarchy of error classes so we can raise more specific errors
    - build metadata:
        - add the "Typing :: Typed" trove classifier
        - break the various lists of dependencies out into separate files
        - switch from `setuptools` to `hatchling`
    - test suite:
        - add tags to the Tox environments for use with the `tox-stages` tool from
          the `test-stages` Python library
        - use `mypy` 1.x with no changes
        - add a Ruff test environment
        - add a reuse test environment to check the SPDX tags
        - convert the `tox.ini` file to the Tox 4.x format
        - do not pass the `python_version` parameter to Mypy, there are other ways to
          check with different Python versions
        - add a `pyupgrade` test environment, not invoked automatically
        - drop the `pep8` and `pylint` test environments, Ruff does that now
- Rust implementation:
    - minor refactoring and fixes suggested by Clippy 1.74
    - use `toml` 0.8.x and `serde_yaml` 0.9.x with no changes
    - switch from `expect-exit` to `anyhow` and `thiserror`
- Documentation:
    - changelog: use the "Keep a Changelog" format:
        - mark the changelog entries' versions up as hyperlinks
        - break the changelog entries into sections
    - move the changelog into the `docs/` directory

## [0.2.1] - 2022-10-10

### Other changes

- Rust implementation:
    - use the thiserror library instead of the quick-error one
    - use the anyhow library to chain errors

## [0.2.0] - 2022-10-02

### Incompatible changes

- the Rust implementation's `get_format_from_value()` and
  `get_version_from_value()` functions dropped the "conversion function"
  argument, relying on the "value" argument to implement the `Deserializer`
  trait for its own contents

### Fixes

- Rust implementation:
    - turn `serde_json` and `serde_yaml` into `dev-dependencies`

### Additions

- Python implementation:
    - declare Python 3.11 as a supported version
    - add a Nix expression for running the Tox tests with different Python
      versions using `nix-shell`
    - add more files to the sdist tarball
- Rust implementation:
    - add `toml` to `dev-dependencies` and run the tests for TOML values, too
    - implement `Eq` for `Version`

### Other changes

- Global changes:
    - convert the test data files from JSON to TOML
- Python implementation:
    - drop the flake8 + hacking Tox test environment
    - add both lower and upper version constraints for the dependencies in
      the Tox test environments
    - drop `types-dataclasses` from the mypy Tox test environment
- Rust implementation:
    - minor refactoring for some Clippy lints
    - silence the `clippy::std_instead_of_core` lint in the `run-clippy` tool 
    - drop some silenced lints from `run-clippy` since we do not violate them
    - use the `tracing` and `tracing-test` crates for the test suite

## [0.1.0] - 2022-07-21

### Started

- First public release

[Unreleased]: https://gitlab.com/ppentchev/typed-format-version/-/compare/release%2F0.2.2...main
[0.2.2]: https://gitlab.com/ppentchev/typed-format-version/-/compare/release%2F0.2.1...release%2F0.2.2
[0.2.1]: https://gitlab.com/ppentchev/typed-format-version/-/compare/release%2F0.2.0...release%2F0.2.1
[0.2.0]: https://gitlab.com/ppentchev/typed-format-version/-/compare/release%2F0.1.0...release%2F0.2.0
[0.1.0]: https://gitlab.com/ppentchev/typed-format-version/-/tags/release%2F0.1.0

[crates-io-media-type-version]: https://crates.io/crates/media-type-version "The media-type-version Rust crate"
[pypi-media-type-version]: https://pypi.org/project/media-type-version "The media-type-version Python library"
