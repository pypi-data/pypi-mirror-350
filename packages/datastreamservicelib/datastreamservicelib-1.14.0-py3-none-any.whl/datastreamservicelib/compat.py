"""Compatibility stuff for old python versions"""

from typing import TypeVar, cast, TYPE_CHECKING
import asyncio
import platform
import logging

LOGGER = logging.getLogger(__name__)
T = TypeVar("T")  # pylint: disable=C0103
if TYPE_CHECKING:
    from typing import Any  # pylint: disable=C0412


class NamedTask(asyncio.Task):  # type: ignore
    """wrapper for mypy checking in older python versions"""

    def get_name(self) -> str:
        """dummy"""
        raise NotImplementedError()

    def set_name(self, __value: object) -> None:
        """dummy"""
        raise NotImplementedError()


def cast_task(task: "asyncio.Task[T]") -> "NamedTask[T]":  # type: ignore
    """Cast task to NamedTask"""
    return cast("NamedTask[Any]", task)  # type: ignore


def asyncio_eventloop_check_policy() -> None:
    """Check platform and override eventloop if needed"""
    if platform.system() == "Windows":
        py_versions = platform.python_version_tuple()
        if int(py_versions[0]) == 3 and int(py_versions[1]) >= 8:
            LOGGER.info("Windows and py38 detected, setting eventloop to Selector")
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore
            asyncio.set_event_loop(asyncio.SelectorEventLoop())


def asyncio_eventloop_get() -> asyncio.AbstractEventLoop:
    """Check platform and return instance of usable eventloop"""
    if platform.system() == "Windows":
        py_versions = platform.python_version_tuple()
        if int(py_versions[0]) == 3 and int(py_versions[1]) >= 8:
            return asyncio.SelectorEventLoop()
    return asyncio.get_event_loop()
