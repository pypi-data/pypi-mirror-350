"""Exceptions for pytaskexec package."""


class TaskRunnerError(Exception):
    """Base exception for TaskRunner errors."""
    pass


class TaskNotFoundError(TaskRunnerError):
    """Raised when a task ID is not found."""
    pass


class TaskSchedulingError(TaskRunnerError):
    """Raised when there's an error scheduling a task."""
    pass
