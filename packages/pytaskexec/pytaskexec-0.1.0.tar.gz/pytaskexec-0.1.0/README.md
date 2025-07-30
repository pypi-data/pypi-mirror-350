# pytaskexec

A lightweight task execution system for concurrent operations in Python. This package provides a simple yet powerful interface for creating and managing concurrent tasks using Python's ThreadPoolExecutor.

## Features

- Easy task creation using decorators or function wrappers
- Concurrent execution using thread pools
- Flexible task management with scheduling and cancellation
- Comprehensive exception handling
- Configurable logging
- Type hints support

## Installation

```bash
pip install pytaskexec
```

## Quick Start

```python
from pytaskexec import TaskRunner, taskify
import time

# Create a task using the decorator
@taskify
def process_data(item, delay=1):
    time.sleep(delay)  # Simulate work
    return f"Processed {item}"

# Create a TaskRunner
with TaskRunner(max_workers=3) as runner:
    # Schedule multiple tasks
    task_ids = [
        runner.schedule(process_data(f"item_{i}"))
        for i in range(5)
    ]

    # Get results as they complete
    for tid in task_ids:
        result = runner.get_result(tid)
        print(result)
```

## Advanced Usage

### Creating Tasks

There are two ways to create tasks:

1. Using the `@taskify` decorator:
```python
@taskify
def my_task(x, y):
    return x + y

task = my_task(1, 2)  # Creates a Task object
```

2. Using the `wrap_as_task` function:
```python
from pytaskexec import wrap_as_task

def my_function(x, y):
    return x + y

task = wrap_as_task(my_function, 1, 2)  # Creates a Task object
```

### Task Management

```python
with TaskRunner(name="my_runner", max_workers=5) as runner:
    # Schedule tasks
    tid1 = runner.schedule(my_task(1, 2))
    tid2 = runner.schedule(my_task(3, 4))

    # Wait for specific tasks
    runner.block(taskids=[tid1, tid2])

    # Get results with timeout
    try:
        result = runner.get_result(tid1, timeout=5)
    except concurrent.futures.TimeoutError:
        runner.cancel_task(tid1)

    # Cancel all pending tasks
    runner.cancel_pending()
```

### Debug Logging

Set the environment variable `PYTASKEXEC_DEBUG` to enable debug logging:

```bash
export PYTASKEXEC_DEBUG=1  # Linux/Mac
set PYTASKEXEC_DEBUG=1      # Windows
```

## Development

### Setting up the Development Environment

1. Clone the repository:
```bash
git clone https://github.com/anandan-bs/pytaskexec.git
cd pytaskexec
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.
