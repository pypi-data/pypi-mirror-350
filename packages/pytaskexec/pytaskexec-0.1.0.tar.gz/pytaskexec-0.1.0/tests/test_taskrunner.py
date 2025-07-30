"""Tests for TaskRunner functionality."""
import unittest
import concurrent.futures
import time
from pytaskexec import TaskRunner, wrap_as_task, taskify


@taskify
def sample_task(sec, raise_error=False):
    """Sample task for testing."""
    if raise_error:
        raise NotImplementedError("sample_task is not supported")
    time.sleep(sec)
    return sec


class TestTaskRunner(unittest.TestCase):
    """Tests for TaskRunner implementation.

    Tests cover task scheduling, cancellation, error handling,
    timeout behavior, and task management functionality.
    """

    def test_scheduling(self):
        """Test scheduling."""
        with TaskRunner() as runner:
            tid = runner.schedule(sample_task(1))
            self.assertEqual(runner.get_result(tid), 1)

    def test_cancel_running_task(self):
        """Test cancel running task."""
        with TaskRunner() as runner:
            tid = runner.schedule(sample_task(2))
            self.assertEqual(runner.cancel_task(tid), False)

    def test_cancel_not_run_task(self):
        """Test cancel not run task."""
        with TaskRunner(max_workers=2) as runner:
            runner.schedule(sample_task(2))
            runner.schedule(sample_task(2))
            tid = runner.schedule(sample_task(2))
            self.assertEqual(runner.cancel_task(tid), True)

    def test_exception(self):
        """Test exception."""
        with TaskRunner() as runner:
            tid = runner.schedule(sample_task(2, raise_error=True))
            with self.assertRaises(NotImplementedError):
                runner.get_result(tid)

    def test_timeout(self):
        """Test timeout."""
        with TaskRunner() as runner:
            tid = runner.schedule(sample_task(5))
            with self.assertRaises(concurrent.futures.TimeoutError):
                runner.get_result(tid, timeout=1)

    def test_block_timeout(self):
        """Test block with timeout."""
        with TaskRunner() as runner:
            tid1 = runner.schedule(sample_task(3))
            tid2 = runner.schedule(sample_task(3))
            # Should timeout before tasks complete
            runner.block(timeout=1)
            self.assertIn(tid1, runner.get_pending_ids())
            self.assertIn(tid2, runner.get_pending_ids())

    def test_block_specific_tasks(self):
        """Test blocking on specific task IDs."""
        with TaskRunner() as runner:
            tid1 = runner.schedule(sample_task(1))
            tid2 = runner.schedule(sample_task(5))
            # Block only for tid1
            runner.block(taskids=[tid1])
            # tid1 should be done, tid2 should still be running
            self.assertNotIn(tid1, runner.get_pending_ids())
            self.assertIn(tid2, runner.get_pending_ids())

    def test_cancel_pending(self):
        """Test cancelling all pending tasks."""
        with TaskRunner(max_workers=1) as runner:
            # Schedule more tasks than workers
            # This will start immediately
            tid1 = runner.schedule(sample_task(3))
            tid2 = runner.schedule(sample_task(1))  # This will be pending
            tid3 = runner.schedule(sample_task(1))  # This will be pending

            # Cancel all pending tasks
            runner.cancel_pending()
            pending_ids = runner.get_pending_ids()

            # First task should still be running
            self.assertIn(tid1, pending_ids)
            # Other tasks should be cancelled
            self.assertNotIn(tid2, pending_ids)
            self.assertNotIn(tid3, pending_ids)

    def test_wrap_as_task(self):
        """Test wrap_as_task function."""
        def test_fn(x, y=1):
            return x + y

        # Test with positional args
        task1 = wrap_as_task(test_fn, 2)
        with TaskRunner() as runner:
            tid = runner.schedule(task1)
            self.assertEqual(runner.get_result(tid), 3)

        # Test with keyword args
        task2 = wrap_as_task(test_fn, 2, y=2)
        with TaskRunner() as runner:
            tid = runner.schedule(task2)
            self.assertEqual(runner.get_result(tid), 4)
