"""CLI for tools."""

from collections.abc import Collection
from pathlib import Path
from re import finditer

from cyclopts import App

from softboiler_github_io_tools import add_changes
from softboiler_github_io_tools.sync import check_compilation, escape
from softboiler_github_io_tools.types import ChangeType

APP = App(help_format="markdown")
"""CLI."""


def main():  # noqa: D103
    APP()


@APP.command
def compile(high: bool = False):  # noqa: A001
    """Compile."""
    log(check_compilation(high))


@APP.command
def add_change(change: ChangeType = "change"):
    """Add change."""
    add_changes.add_change(change)


@APP.command
def get_actions():
    """Get actions used by this repository.

    For additional security, select "Allow <user> and select non-<user>, actions and
    reusable workflows" in the General section of your Actions repository settings, and
    paste the output of this command into the "Allow specified actions and reusable
    workflows" block.

    Parameters
    ----------
    high
        Highest dependencies.
    """
    actions: list[str] = []
    for contents in [
        path.read_text("utf-8") for path in Path(".github/workflows").iterdir()
    ]:
        actions.extend([
            f"{match['action']}@*,"
            for match in finditer(r'uses:\s?"?(?P<action>.+)@', contents)
        ])
    log(sorted(set(actions)))


def log(obj):
    """Send object to `stdout`."""
    match obj:
        case str():
            print(obj)  # noqa: T201
        case Collection():
            for o in obj:
                log(o)
        case Path():
            log(escape(obj))
        case _:
            print(obj)  # noqa: T201


if __name__ == "__main__":
    main()
