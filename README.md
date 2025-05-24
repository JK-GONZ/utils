# Utils content

* dir_manager.py
* logger_manager.py

---

</br>
</br>

# DirManager

A Python utility class for creating and managing directory structures programmatically.

## Overview

The `DirManager` class provides a simple way to:

- Parse text-based directory tree structures
- Create directory hierarchies from structured definitions
- Generate tree-like visualizations of directory structures

## Features

- Text-based directory structure parsing
- Support for nested directory hierarchies
- Tree-like structure visualization
- Flexible path handling with both string and Path objects
- Clean handling of tree characters and indentation

## Usage Example

```python
from dir_manager import DirManager

# Create a new DirManager instance
dm = DirManager()

# Define your directory structure using a tree-like format
structure = """
project_root
    src
        models
        controllers
        views
    tests
        unit
        integration
    docs
"""

# Parse the structure
dm.parse_structure(structure)

# Preview the structure before creating
print(dm.preview_structure())

# Create the directories
dm.create_directories("/path/to/your/project")
```

## Directory Structure Format

The class accepts directory structures in a tree-like format with indentation. Both standard tree characters and simple indentation are supported:

```
project_root
    ├── src
    │   ├── models
    │   ├── controllers
    │   └── views
    └── tests
        ├── unit
        └── integration
```

or simple indentation:

```
project_root
    src
        models
        controllers
        views
    tests
        unit
        integration
```

## Methods

- `parse_structure(structure_str)`: Parses a string representation of a directory structure
- `create_directories(path=None)`: Creates the defined directory structure at the specified path
- `preview_structure()`: Generates a tree-like visualization of the directory structure
- `set_base_path(path)`: Sets a new base path for directory creation

---
</br>
</br>

# LoggerManager

A Python utility class that simplifies the creation and management of logging configurations, supporting both file and console outputs with advanced features.

## Overview

The [LoggerManager]() class provides a convenient way to:

* Configure logging with both file and console outputs
* Set up rotating file handlers with size limits
* Control log levels and formatting
* Filter logs based on output targets

## Features

* Dual output support (file and console)
* Rotating file handler with configurable size limits
* Custom log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
* Automatic log directory creation
* Customizable log formatting
* Filtering system for output targets

## Pending Features

* [ ] Ability to specify different format patterns for file and console outputs
* [ ] Custom format configuration through constructor parameters
* [ ] Format modification after logger initialization

## Current Log Format

Default format for both file and console:

```bash
YYYY-MM-DD HH:MM:SS - LEVEL - LOGGER_NAME - MESSAGE
```

## Usage Example

```python
from logger_manager import LoggerManager
# Create a logger with both console and file output
logger = LoggerManager(
	name='my_app',
	level='DEBUG',
	log_to_console=True,
	log_to_file=True,
	filename='my_app_log',
	log_dir='logs/app',
	max_file_size=5,  # MB
	backup_count=**3
)

# Using the logger
logger.info("Application started")
logger.debug("Processing data...")
logger.warning("Resource usage high")
logger.error("An error occurred")
logger.critical("System failure")
```




## Configuration Options

* [name](): Logger identifier
* [level](): Minimum severity level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
* [log_to_file](): Enable/disable file logging
* [log_to_console](): Enable/disable console logging
* [log_dir](): Directory for log files
* [filename](): Name of the log file
* [max_file_size](): Maximum size in MB before rotation
* [backup_count](): Number of backup files to keep

## File Rotation

The logger automatically rotates files when they reach the specified size limit ([max_file_size]()). Old log files are kept according to the [backup_count]() parameter, with names like:

* myapp.log
* myapp.log.1
* myapp.log.2
* myapp.log.3

This helps manage disk space while maintaining a history of log records.
