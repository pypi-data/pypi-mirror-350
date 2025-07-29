"""Paths."""

from collections import OrderedDict
import os
from pathlib import Path
from typing import List

import click
from invoke import Collection, Context, task

from invokelint.path.filter_duplication import filter_duplication
from invokelint.path.setuptools import Setuptools

# The following list of directories that setuptools exclude from dist should be added into targets for lint and format.
PACKAGES_TO_LINT = [
    "example",
    "examples",
    "scripts",
    "tools",
    "util",
    "utils",
    "python",
    # ---- Task runners / Build tools ----
    "site_scons",  # SCons
]
MODULES_TO_LINT = [
    "setup",
    "conftest",
    "test",
    "tests",
    "example",
    "examples",
    # ---- Task runners ----
    "toxfile",
    "noxfile",
    "pavement",
    "dodo",
    "tasks",
    "fabfile",
    # ---- Other tools ----
    "conanfile",  # Connan: C/C++ build tool
    "manage",  # Django
]
TEST_PACKAGES = [
    "test",
    "tests",
    "unit_test",
    "unit_tests",
]


def remove_duplicate(list_str: List[str]) -> List[str]:
    """see:

    - Answer: python - Removing duplicates in lists - Stack Overflow
      https://stackoverflow.com/a/7961390/12721873
    """
    return list(OrderedDict.fromkeys(list_str))


setuptools = Setuptools()
PRODUCTION_PACKAGES = filter_duplication([package.replace(".", os.sep) for package in setuptools.packages])
SETUPTOOLS_PYTHON_MODULES = setuptools.find_py_modules(MODULES_TO_LINT)
EXISTING_PACKAGES = [package for package in PACKAGES_TO_LINT if Path(package).is_dir()]
EXISTING_MODULES = [f"{module}.py" for module in SETUPTOOLS_PYTHON_MODULES if Path(f"{module}.py").is_file()]
EXISTING_TEST_PACKAGES = [package for package in TEST_PACKAGES if Path(package).is_dir()]
PYTHON_DIRS = remove_duplicate([*PRODUCTION_PACKAGES, *EXISTING_MODULES, *EXISTING_PACKAGES, *EXISTING_TEST_PACKAGES])
PYTHON_DIRS_EXCLUDING_TEST = remove_duplicate([*PRODUCTION_PACKAGES, *EXISTING_MODULES, *EXISTING_PACKAGES])
ns = Collection()


@task
def debug(_context: Context) -> None:
    """Builds source and wheel packages into dist/ directory."""
    click.echo(f"Setuptools detected packages: {setuptools.packages}")
    click.echo(f"Root packages: {PRODUCTION_PACKAGES}")
    click.echo(f"Setuptools detected Python modules: {SETUPTOOLS_PYTHON_MODULES}")
    click.echo(f"Existing test packages: {EXISTING_TEST_PACKAGES}")
    click.echo(f"Python file or directories to lint: {PYTHON_DIRS}")
    click.echo(f"Python file or directories to lint excluding test packages: {PYTHON_DIRS_EXCLUDING_TEST}")


ns.add_task(debug, default=True)
