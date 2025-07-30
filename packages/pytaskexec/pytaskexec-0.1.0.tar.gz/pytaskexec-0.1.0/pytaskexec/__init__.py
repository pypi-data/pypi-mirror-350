"""
pytaskexec - A Python task execution package.

This package provides a simple yet powerful interface for creating and managing
concurrent tasks in Python.
"""

from .pytaskexec import TaskRunner, taskify, wrap_as_task
from .exceptions import TaskRunnerError, TaskNotFoundError, TaskSchedulingError

__version__ = "0.1.0"

__all__ = [
    'TaskRunner',
    'taskify',
    'wrap_as_task',
    'TaskRunnerError',
    'TaskNotFoundError',
    'TaskSchedulingError',
]
