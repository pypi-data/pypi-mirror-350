# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Create a virtual environment, install Tox, run it."""

from __future__ import annotations

import argparse
import configparser
import dataclasses
import functools
import json
import logging
import pathlib
import shlex
import subprocess
import sys
import tempfile
import typing
import venv


if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final


VERSION: Final = "0.1.0"
"""The vetox library version."""


TOX_MIN_VERSION: Final = "4.1"
"""The minimum version of Tox needed to run our tests."""


@dataclasses.dataclass(frozen=True)
class Config:
    """Runtime configuration for the venv-tox tool."""

    conf: pathlib.Path
    """The path to the `tox.ini` file to use."""

    log: logging.Logger
    """The logger to send diagnostic, informational, warning, and error messages to."""

    tempd: pathlib.Path
    """The temporary directory to operate in."""


# Shamelessly stolen from the logging-std module
@functools.lru_cache
def build_logger() -> logging.Logger:
    """Build a logger object, send info messages to stdout, everything else to stderr."""
    logger: Final = logging.getLogger("logging-std")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    h_out: Final = logging.StreamHandler(sys.stdout)
    h_out.setLevel(logging.INFO)
    h_out.addFilter(lambda rec: rec.levelno == logging.INFO)
    logger.addHandler(h_out)

    h_err: Final = logging.StreamHandler(sys.stderr)
    h_err.setLevel(logging.INFO)
    h_err.addFilter(lambda rec: rec.levelno != logging.INFO)
    logger.addHandler(h_err)

    return logger


def create_and_update_venv(cfg: Config) -> pathlib.Path:
    """Create a virtual environment, update all the packages within."""
    penv: pathlib.Path = cfg.tempd / "venv"
    cfg.log.info("About to create the %(penv)s virtual environment", {"penv": penv})
    if sys.version_info >= (3, 9):
        cfg.log.info("- using venv.create(upgrade_deps) directly")
        venv.create(penv, with_pip=True, upgrade_deps=True)
        return penv

    cfg.log.info("- no venv.create(upgrade_deps)")
    venv.create(penv, with_pip=True)

    cfg.log.info("- obtaining the list of packages in the virtual environment")
    contents: Final = subprocess.check_output(
        [penv / "bin/python3", "-m", "pip", "list", "--format=json"], encoding="UTF-8"
    )
    pkgs: Final = json.loads(contents)
    if (
        not isinstance(pkgs, list)
        or not pkgs
        or not all(isinstance(pkg, dict) and "name" in pkg for pkg in pkgs)
    ):
        sys.exit(f"Unexpected `pip list --format=json` output: {pkgs!r}")

    names: Final = sorted(pkg["name"] for pkg in pkgs)
    cfg.log.info(
        "- upgrading the %(names)s package%(plu)s in the virtual environment",
        {"names": ", ".join(names), "plu": "" if len(names) == 1 else "s"},
    )
    subprocess.check_call([penv / "bin/python3", "-m", "pip", "install", "-U", "--", *names])
    return penv


@functools.lru_cache
def get_tox_min_version(cfg: Config) -> str:
    """Look for a minimum Tox version in the tox.ini file, fall back to TOX_MIN_VERSION."""
    cfgp: Final = configparser.ConfigParser(interpolation=None)
    with cfg.conf.open(encoding="UTF-8") as tox_ini:
        cfgp.read_file(tox_ini)

    return cfgp["tox"].get("min_version", cfgp["tox"].get("minversion", TOX_MIN_VERSION))


def install_tox(cfg: Config, penv: pathlib.Path) -> None:
    """Install Tox into the virtual environment."""
    minver: Final = get_tox_min_version(cfg)
    cfg.log.info("Installing Tox >= %(minver)s", {"minver": minver})
    subprocess.check_call([penv / "bin/python3", "-m", "pip", "install", f"tox >= {minver}"])


def get_tox_cmdline(
    cfg: Config, penv: pathlib.Path, *, parallel: bool = True, args: list[str]
) -> list[pathlib.Path | str]:
    """Get the Tox command with arguments."""
    cfg.log.info(
        "Running Tox%(parallel)s with %(args)s",
        {
            "parallel": " in parallel" if parallel else "",
            "args": ("additional arguments: " + shlex.join(args))
            if args
            else "no additional arguments",
        },
    )
    return [
        penv / "bin/python3",
        "-m",
        "tox",
        "-c",
        cfg.conf,
        "run-parallel" if parallel else "run",
        *args,
    ]


def run_tox(cfg: Config, penv: pathlib.Path, *, parallel: bool = True, args: list[str]) -> None:
    """Run Tox from the virtual environment."""
    subprocess.check_call(get_tox_cmdline(cfg, penv, parallel=parallel, args=args))


def run(cfg_no_tempd: Config, *, parallel: bool, args: list[str]) -> None:
    """Create the virtual environment, install Tox, run it."""
    with tempfile.TemporaryDirectory() as tempd_obj:
        cfg: Final = dataclasses.replace(cfg_no_tempd, tempd=pathlib.Path(tempd_obj))
        penv: Final = create_and_update_venv(cfg)
        install_tox(cfg, penv)
        run_tox(cfg, penv, parallel=parallel, args=args)


def cmd_run(cfg_no_tempd: Config, args: list[str]) -> None:
    """Run the Tox tests sequentially."""
    run(cfg_no_tempd, parallel=False, args=args)


def cmd_run_parallel(cfg_no_tempd: Config, args: list[str]) -> None:
    """Run the Tox tests in parallel."""
    run(cfg_no_tempd, parallel=True, args=args)


def cmd_features(_cfg_no_tempd: Config, _args: list[str]) -> None:
    """Display the list of features supported by the program."""
    print(f"Features: vetox={VERSION} tox=0.1 tox-parallel=0.1")


def cmd_version(_cfg_no_tempd: Config, _args: list[str]) -> None:
    """Display the vetox version."""
    print(f"vetox {VERSION}")


def parse_args() -> tuple[Config, Callable[[Config, list[str]], None], list[str]]:
    """Parse the command-line arguments."""
    parser: Final = argparse.ArgumentParser(prog="vetox")
    parser.add_argument(
        "-c",
        "--conf",
        type=pathlib.Path,
        default=pathlib.Path.cwd() / "tox.ini",
        help="The path to the tox.ini file",
    )

    subp: Final = parser.add_subparsers()
    p_run: Final = subp.add_parser("run", help="Run tests sequentially")
    p_run.add_argument("args", type=str, nargs="*", help="Additional arguments to pass to Tox")
    p_run.set_defaults(func=cmd_run)

    p_run_p: Final = subp.add_parser("run-parallel", help="Run tests in parallel")
    p_run_p.add_argument("args", type=str, nargs="*", help="Additional arguments to pass to Tox")
    p_run_p.set_defaults(func=cmd_run_parallel)

    p_features: Final = subp.add_parser("features", help="Display the supported program features")
    p_features.set_defaults(func=cmd_features)

    p_version: Final = subp.add_parser("version", help="Display the vetox version")
    p_version.set_defaults(func=cmd_version)

    args: Final = parser.parse_args()

    func: Final[Callable[[Config, list[str]], None] | None] = getattr(args, "func", None)
    if func is None:
        sys.exit("No subcommand specified; use `--help` for a list")

    return (
        Config(conf=args.conf, log=build_logger(), tempd=pathlib.Path("/nonexistent")),
        func,
        getattr(args, "args", []),
    )


def main() -> None:
    """Parse command-line arguments, create a virtual environment, run Tox."""
    cfg_no_tempd, func, args = parse_args()
    func(cfg_no_tempd, args)


if __name__ == "__main__":
    main()
