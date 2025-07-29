"""Tasks of format."""

from typing import Any, List

from invoke import Collection, Context, Result, task

from invokelint.path import PYTHON_DIRS
from invokelint import ruff as ruff_commands
from invokelint.run import run_in_order, run_in_pty

ns = Collection()


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def docformatter(context: Context, *, check: bool = False, **kwargs: Any) -> List[Result]:  # noqa: ARG001
    """Runs docformatter.

    This function includes hard coding of line length.
    see:
    - Add pyproject.toml support for config (Issue #10) by weibullguy · Pull Request #77 · PyCQA/docformatter
    https://github.com/PyCQA/docformatter/pull/77
    """
    docformatter_options = " --recursive {}".format("--check" if check else "--in-place")
    return [run_in_pty(context, "docformatter{} {}".format(docformatter_options, " ".join(PYTHON_DIRS)), warn=True)]


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def autoflake(context: Context, *, check: bool = False, **kwargs: Any) -> List[Result]:  # noqa: ARG001
    """Runs autoflake."""
    autoflake_options = " --recursive {}".format("--check" if check else "--in-place")
    return [run_in_pty(context, "autoflake{} {}".format(autoflake_options, " ".join(PYTHON_DIRS)), warn=True)]


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def isort(context: Context, *, check: bool = False, **kwargs: Any) -> List[Result]:  # noqa: ARG001
    """Runs isort."""
    isort_options = " --check-only --diff" if check else ""
    return [run_in_pty(context, "isort{} {}".format(isort_options, " ".join(PYTHON_DIRS)), warn=True)]


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def black(context: Context, *, check: bool = False, **kwargs: Any) -> List[Result]:  # noqa: ARG001
    """Runs Black."""
    black_options = " --check --diff" if check else ""
    return [run_in_pty(context, "black{} {}".format(black_options, " ".join(PYTHON_DIRS)), warn=True)]


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def call_ruff_check(context: Context, *, check: bool = False, **kwargs: Any) -> List[Result]:  # noqa: ARG001
    if check:
        return ruff_commands.chk(context, show_fixes=True)
    result = []
    result.extend(ruff_commands.chk(context, show_fixes=True, warn=True))
    result.extend(ruff_commands.chk(context, fix=True, show_fixes=True))
    return result


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def call_ruff_fmt(context: Context, *, check: bool = False, **kwargs: Any) -> List[Result]:  # noqa: ARG001
    if check:
        return ruff_commands.fmt(context, diff=check)
    result = []
    result.extend(ruff_commands.fmt(context, diff=True, warn=True))
    result.extend(ruff_commands.fmt(context))
    return result


@task(
    help={
        "check": "Checks if source is formatted without applying changes",
        "ruff": "Leave ruff warnings",
        "by_ruff": "Formats code by ruff",
    },
)
def fmt(context: Context, *, check: bool = False, ruff: bool = False, by_ruff: bool = False) -> List[Result]:
    """Formats code by docformatter, isort, autoflake, and Black (option for only check available)."""
    tasks = [docformatter, autoflake]
    if by_ruff:
        tasks.append(call_ruff_fmt)
    else:
        tasks.extend([isort, black])
    if check or not ruff:
        tasks.append(call_ruff_check)
    return run_in_order(tasks, context, check=check)


ns.add_task(fmt, default=True)
