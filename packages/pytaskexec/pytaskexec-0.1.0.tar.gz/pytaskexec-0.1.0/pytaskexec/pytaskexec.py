"""A lightweight task management system built on Python's concurrent.futures package.

This module provides a simple yet powerful interface for creating and managing
concurrent tasks in Python. It offers both decorator and function-based approaches
to create tasks that can be executed concurrently.

Features:
    - Easy task creation using decorators or function calls
    - Concurrent execution using Python's concurrent.futures
    - Flexible task management and execution control
    - Support for both synchronous and asynchronous task execution

Example:
    >>> @task
    ... def example_task(x):
    ...     return x * 2
    ...
    >>> task1 = example_task(5)
    >>> # Or create task directly
    >>> task2 = wrap_as_task(lambda x: x + 1, 3)

Author: Anandan B S
Version: 0.1.0
"""

import concurrent.futures
import functools
import logging
import os

from .exceptions import TaskRunnerError, TaskNotFoundError, TaskSchedulingError


# Configure default logging
DEFAULT_LOG_LEVEL = logging.INFO
if os.environ.get('PYTASKEXEC_DEBUG', '').lower() in ('true', '1', 'yes'):
    DEFAULT_LOG_LEVEL = logging.DEBUG


def wrap_as_task(target, *args, **kwargs):
    """Wrap a function as a Task object.

    Args:
        target (callable): Function to be wrapped as a task
        *args: Positional arguments for the target function
        **kwargs: Keyword arguments for the target function

    Returns:
        Task: A Task object that can be scheduled with TaskRunner
    """
    return Task(target, args, kwargs)


def taskify(fn):
    """Decorator to convert a function into a Task.

    This decorator transforms a regular function into a Task object that can be
    scheduled with TaskRunner. When the decorated function is called, it returns
    a Task instance instead of executing immediately.

    Args:
        fn (callable): The function to be converted into a Task

    Returns:
        callable: A wrapped function that returns a Task instance

    Example:
        >>> @taskify
        ... def my_function(x):
        ...     return x * 2
        ...
        >>> task = my_function(5)  # Returns a Task object
        >>> runner = TaskRunner()
        >>> runner.schedule(task)  # Schedules the task for execution
    """

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        is_task = kwargs.pop('is_task', True)
        if not is_task:  # added for unit testing.
            fn(*args, **kwargs)
        else:
            return Task(fn, args, kwargs)

    return wrapped


class Task(object):
    """Task."""

    def __init__(self, fn, args=None, kwargs=None):
        """Constructor."""
        self.name = fn.__name__
        self.fn = fn
        if not args:
            args = tuple()
        if not kwargs:
            kwargs = dict()
        self.args = args
        self.kwargs = kwargs


class TaskRunner(concurrent.futures.ThreadPoolExecutor):
    """Task runner with exception handling and logging.

    Handles task scheduling, execution, cancellation, and result retrieval
    with proper exception handling and logging.
    """

    def __init__(self, name='task_runner', max_workers=10):
        """Initialize task runner.

        Args:
            name (str): Name of the task runner, used for logging
            max_workers (int): Maximum number of worker threads

        Raises:
            ValueError: If max_workers is less than 1
        """
        if max_workers < 1:
            raise ValueError("max_workers must be greater than 0")

        self.name = name
        try:
            super(TaskRunner, self).__init__(
                max_workers=max_workers, thread_name_prefix=name)
            self.logger = logging.getLogger(name)
            self.logger.setLevel(DEFAULT_LOG_LEVEL)
            self._id = 1
            self.future_to_taskid = dict()
            self.logger.info(
                f'Task runner {name} initialized with {max_workers} workers')
        except Exception as e:
            self.logger.error(f'Failed to initialize TaskRunner: {str(e)}')
            raise TaskRunnerError(
                f'TaskRunner initialization failed: {str(e)}')

    def schedule(self, task):
        """Schedule any task.

        Args:
            task (Task): Task object to be scheduled

        Returns:
            int: Task ID for the scheduled task

        Raises:
            TaskSchedulingError: If task scheduling fails
            ValueError: If task is None or invalid
        """
        if not task or not hasattr(task, 'fn'):
            raise ValueError("Invalid task object")

        try:
            self._id += 1
            self.future_to_taskid[self._id] = super(
                TaskRunner, self).submit(task.fn, *task.args, **task.kwargs)
            self.logger.debug(f'Scheduled task {task.name} with ID {self._id}')
            return self._id
        except Exception as e:
            self.logger.error(f'Failed to schedule task {task.name}: {str(e)}')
            raise TaskSchedulingError(f'Failed to schedule task: {str(e)}')

    def block(self, timeout=None, return_when=concurrent.futures.ALL_COMPLETED, taskids=None):
        """Block until tasks are completed.

        Args:
            timeout (float, optional): Maximum time to wait
            return_when (str): Future completion condition
            taskids (list, optional): Specific task IDs to wait for

        Raises:
            TaskNotFoundError: If any specified task ID is not found
            ValueError: If timeout is negative
        """
        if timeout is not None and timeout < 0:
            raise ValueError("timeout cannot be negative")

        try:
            if taskids:
                try:
                    fs = [self.future_to_taskid[taskid] for taskid in taskids]
                except KeyError as e:
                    raise TaskNotFoundError(f'Task ID not found: {e}')
                self.logger.debug(f'Waiting for specific tasks: {taskids}')
            else:
                fs = list(self.future_to_taskid.values())
                self.logger.debug('Waiting for all pending tasks')

            concurrent.futures.wait(
                fs, timeout=timeout, return_when=return_when)
            self.logger.info('Task wait completed')
        except Exception as e:
            if not isinstance(e, TaskNotFoundError):
                self.logger.error(f'Error while waiting for tasks: {str(e)}')
                raise TaskRunnerError(f'Block operation failed: {str(e)}')

    def get_result(self, taskid, timeout=5):
        """Get the result of any taskid.

        Args:
            taskid (int): Task ID to get result for
            timeout (float): Maximum time to wait for result

        Returns:
            Any: Result of the task execution

        Raises:
            TaskNotFoundError: If task ID is not found
            concurrent.futures.TimeoutError: If result retrieval times out
            ValueError: If timeout is negative
            Exception: Any exception raised by the task itself
        """
        if timeout is not None and timeout < 0:
            raise ValueError("timeout cannot be negative")

        self.logger.debug(f'Getting result for task {taskid}')
        try:
            if taskid not in self.future_to_taskid:
                raise TaskNotFoundError(f'Task ID not found: {taskid}')

            result = self.future_to_taskid[taskid].result(timeout=timeout)
            self.logger.debug(f'Task {taskid} completed successfully')
            return result
        except concurrent.futures.TimeoutError:
            self.logger.warning(
                f'Task {taskid} result retrieval timed out after {timeout} seconds')
            raise
        except Exception as e:
            if isinstance(e, TaskNotFoundError):
                raise
            self.logger.error(
                f'Error getting result for task {taskid}: {str(e)}')
            raise

    def cancel_task(self, tid):
        """Cancel any tasks.

        Args:
            tid (int): Task ID to cancel

        Returns:
            bool: True if task was cancelled successfully

        Raises:
            TaskNotFoundError: If task ID is not found
        """
        self.logger.info(f'Attempting to cancel task {tid}')
        try:
            if tid not in self.future_to_taskid:
                raise TaskNotFoundError(f'Task ID not found: {tid}')

            result = self.future_to_taskid[tid].cancel()
            if result:
                self.logger.info(f'Task {tid} cancelled successfully')
            else:
                self.logger.warning(
                    f'Failed to cancel task {tid} (may be running or completed)')
            return result
        except Exception as e:
            if isinstance(e, TaskNotFoundError):
                raise
            self.logger.error(f'Error cancelling task {tid}: {str(e)}')
            raise TaskRunnerError(f'Cancel operation failed: {str(e)}')

    def get_pending_ids(self):
        """Get IDs of pending tasks.

        Returns:
            list: List of task IDs that are still pending

        Raises:
            TaskRunnerError: If there's an error checking task status
        """
        self.logger.debug('Checking for pending tasks')
        try:
            futures = list(self.future_to_taskid.values())
            if not futures:
                return []
            pending_ids = []
            for tid, fs in self.future_to_taskid.items():
                if not fs.done():
                    pending_ids.append(tid)
            self.logger.debug(f'Found {len(pending_ids)} pending tasks')
            return pending_ids

        except Exception as e:
            self.logger.error(f'Error getting pending task IDs: {str(e)}')
            raise TaskRunnerError(f'Failed to get pending task IDs: {str(e)}')

    def cancel_pending(self):
        """Cancel all pending tasks."""
        self.logger.info('Canceling all pending tasks')
        for tid in self.get_pending_ids():
            self.cancel_task(tid)
