"""CLI for tools."""

import json
import tomllib
from collections.abc import Collection
from datetime import UTC, datetime
from json import dumps
from pathlib import Path
from re import finditer
from shlex import split
from subprocess import run
from sys import executable

from cyclopts import App

from softboiler_github_io_tools.sync import (
    COMPS,
    DEV,
    LOCK,
    NODEPS,
    PYPROJECT,
    PYRIGHTCONFIG,
    PYTEST,
    SYNC,
    VERSION,
    get_comp_path,
)

APP = App()
"""CLI."""


def main():
    """Invoke the CLI."""
    APP()


def log(obj):
    """Send an object to `stdout` and return it."""
    match obj:
        case Collection():
            if len(obj):
                print(*obj, sep="\n")  # noqa: T201
        case _:
            print(obj)  # noqa: T201
    return obj


@APP.command()
def get_actions() -> list[str]:
    """Get actions used by this repository.

    For additional security, select "Allow <user> and select non-<user>, actions and
    reusable workflows" in the General section of your Actions repository settings, and
    paste the output of this command into the "Allow specified actions and reusable
    workflows" block.

    Args:
        high: Highest dependencies.
    """
    actions: list[str] = []
    for contents in [
        path.read_text("utf-8") for path in Path(".github/workflows").iterdir()
    ]:
        actions.extend([
            f"{match['action']}@*,"
            for match in finditer(r'uses:\s?"?(?P<action>.+)@', contents)
        ])
    return log(sorted(set(actions)))


@APP.command()
def get_comp(high: bool = False) -> Path:
    """Compile dependencies for a system.

    Args:
        high: Highest dependencies.
    """
    if LOCK.exists():
        comp = get_comp_path(high)
        if existing_comp := json.loads(LOCK.read_text("utf-8")).get(comp.stem):
            comp.write_text(encoding="utf-8", data=existing_comp)
            return comp
    return compile(high)


@APP.command()
def compile(high: bool = False) -> Path:  # noqa: A001
    """Recompile dependencies for a system.

    Args:
        high: Highest dependencies.
    """
    sep = " "
    result = run(
        args=split(
            sep.join([
                f"{Path(executable).as_posix()} -m uv",
                f"pip compile --python-version {VERSION}",
                f"--resolution {'highest' if high else 'lowest-direct'}",
                f"--exclude-newer {datetime.now(UTC).isoformat().replace('+00:00', 'Z')}",
                "--all-extras",
                sep.join([p.as_posix() for p in [PYPROJECT, DEV, SYNC]]),
            ])
        ),
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr)
    deps = result.stdout
    comp = get_comp_path(high)
    comp.write_text(
        encoding="utf-8",
        data=(
            "\n".join([
                *[line.strip() for line in deps.splitlines()],
                *[line.strip() for line in NODEPS.read_text("utf-8").splitlines()],
            ])
            + "\n"
        ),
    )
    return log(comp)


@APP.command()
def lock() -> Path:
    """Lock all local dependency compilations."""
    LOCK.write_text(
        encoding="utf-8",
        data=json.dumps(
            indent=2,
            sort_keys=True,
            obj={
                **(json.loads(LOCK.read_text("utf-8")) if LOCK.exists() else {}),
                **{
                    comp.stem.removeprefix("requirements_"): comp.read_text("utf-8")
                    for comp in COMPS.iterdir()
                },
            },
        )
        + "\n",
    )
    return log(LOCK)


@APP.command()
def sync_local_dev_configs():
    """Synchronize local dev configs to shadow `pyproject.toml`, with some changes.

    Duplicate pyright and pytest configuration from `pyproject.toml` to
    `pyrightconfig.json` and `pytest.ini`, respectively. These files shadow the
    configuration in `pyproject.toml`, which drives CI or if shadow configs are not
    present. Shadow configs are in `.gitignore` to facilitate local-only shadowing.

    Concurrent test runs are disabled in the local pytest configuration which slows down
    the usual local, granular test workflow.
    """
    config = tomllib.loads(PYPROJECT.read_text("utf-8"))
    # Write pyrightconfig.json
    pyright = config["tool"]["pyright"]
    data = dumps(pyright, indent=2)
    PYRIGHTCONFIG.write_text(encoding="utf-8", data=f"{data}\n")
    # Write pytest.ini
    pytest = config["tool"]["pytest"]["ini_options"]
    PYTEST.write_text(
        encoding="utf-8",
        data="\n".join(["[pytest]", *[f"{k} = {v}" for k, v in pytest.items()], ""]),
    )


if __name__ == "__main__":
    main()
