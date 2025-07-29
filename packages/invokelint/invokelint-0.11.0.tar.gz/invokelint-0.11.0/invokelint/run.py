"""Functions to run tasks."""

import platform
from typing import Any, Callable, cast, List, TYPE_CHECKING

from invoke import Context, Result, UnexpectedExit

if TYPE_CHECKING:
    from typing import Protocol

    class TaskFunction(Protocol):
        def __call__(self, context: Context, **kwargs: Any) -> List[Result]:  # pragma: no cover
            # fakeself gets swallowed by the class method binding logic
            # so this will match functions that have bar and the free arguments.
            ...


def run_in_pty(context: Context, command: str, **kwargs: Any) -> Result:
    return cast("Result", context.run(command, pty=platform.system() != "Windows", **kwargs))


def run_in_order(list_task: "List[TaskFunction]", context: Context, *args: Any, **kwargs: Any) -> List[Result]:
    """Runs tasks in order, stop subsequent tasks when task fail."""
    list_result = []
    for each_task in list_task:
        list_result.extend(each_task(context, *args, **kwargs))
    return list_result


def run_all(list_task: List[Callable[[Context], List[Result]]], context: Context) -> List[Result]:
    """Runs all commands even if failure."""
    list_unexpected_exit = []
    list_result = []
    for each_task in list_task:
        try:
            list_result.extend(each_task(context))
        except UnexpectedExit as error:
            list_unexpected_exit.append(error)
    if list_unexpected_exit:
        raise list_unexpected_exit[0]
    return list_result
