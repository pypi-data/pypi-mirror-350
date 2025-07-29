# K-Logger

A Python logging utility optimized for Korean developers with automatic Korean timezone (KST) support and customizable formatting.

[![PyPI version](https://badge.fury.io/py/k-logger.svg)](https://badge.fury.io/py/k-logger)
[![Python Support](https://img.shields.io/pypi/pyversions/k-logger.svg)](https://pypi.org/project/k-logger/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[🇰🇷 한국어 버전](README.kr.md)

## Features

- 🕐 **Automatic Korean Timezone (KST)** - All timestamps are automatically converted to Korean time
- 🔤 **Abbreviated Log Levels** - Clean, single-letter log level indicators (D, I, W, E, C)
- 🎨 **Flexible Formatting** - Toggle file information display based on your needs
- ⚡ **Easy Setup** - Works out of the box with sensible defaults
- 🐍 **Pure Python** - No system dependencies required
- 📦 **Lightweight** - Minimal dependencies (only `loguru` and `pytz`)
- 🖱️ **IDE-Friendly** - Clickable file paths in VSCode and other modern IDEs (format: `file.py:line`)

## Installation

```bash
pip install k-logging
```

## Quick Start

```python
from k_logger import get_logger

logger = get_logger()

logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
```

Output:
```
I 05-23 14:30:15 | example.py:5 - Application started
W 05-23 14:30:15 | example.py:6 - This is a warning
E 05-23 14:30:15 | example.py:7 - An error occurred
```

> 💡 **Pro tip**: In VSCode and other modern IDEs, you can click on `example.py:5` to jump directly to that line in your code!

## Usage

### Basic Usage

K-Logger automatically initializes with sensible defaults when you import it:

```python
from k_logger import get_logger

logger = get_logger()
logger.info("Hello, World!")
```

### Custom Configuration

You can customize the logger behavior using `setup_korean_logger()`:

```python
from k_logger import setup_korean_logger

# Show debug messages and include file information
logger = setup_korean_logger(level="DEBUG", show_file_info=True)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Minimal Format

For cleaner output without file information:

```python
from k_logger import setup_korean_logger

# Simple format without file info
logger = setup_korean_logger(level="INFO", show_file_info=False)

logger.info("Clean log output")  # I 05-23 14:30:15 - Clean log output
```

## Log Levels

| Level    | Abbreviation | Description |
|----------|--------------|-------------|
| DEBUG    | D            | Detailed information for debugging |
| INFO     | I            | General informational messages |
| WARNING  | W            | Warning messages |
| ERROR    | E            | Error messages |
| CRITICAL | C            | Critical issues |

## API Reference

### `setup_korean_logger(level="INFO", show_file_info=True)`

Configure and return a logger instance with Korean timezone support.

**Parameters:**
- `level` (str): Logging level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
- `show_file_info` (bool): Whether to include file path and line number in logs

**Returns:**
- `loguru.Logger`: Configured logger instance

### `get_logger()`

Get the current logger instance. If not configured, returns the auto-configured default logger.

**Returns:**
- `loguru.Logger`: Current logger instance

## Examples

### Integration with Existing Projects

```python
# myapp.py
from k_logger import get_logger

logger = get_logger()

def process_data(data):
    logger.debug(f"Processing {len(data)} items")
    try:
        # Process data here
        result = data.upper()
        logger.info("Data processed successfully")
        return result
    except Exception as e:
        logger.error(f"Failed to process data: {e}")
        raise
```

### Multi-module Applications

```python
# config.py
from k_logger import setup_korean_logger

# Configure once at application startup
logger = setup_korean_logger(level="DEBUG", show_file_info=True)

# other_module.py
from k_logger import get_logger

logger = get_logger()  # Gets the same configured instance
logger.info("Using logger in another module")
```

## Requirements

- Python 3.7+
- `loguru` >= 0.6.0
- `pytz` >= 2021.1

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **june-oh** - [GitHub](https://github.com/june-oh)

## Changelog

### v1.0.0 (2025-05-23)
- First stable release
- Korean timezone support
- Abbreviated log levels
- Customizable formatting options
- IDE-friendly clickable file paths

## Acknowledgments

- Built with [loguru](https://github.com/Delgan/loguru) - Python logging made (stupidly) simple
- Timezone support by [pytz](https://github.com/stub42/pytz) - World timezone definitions for Python 