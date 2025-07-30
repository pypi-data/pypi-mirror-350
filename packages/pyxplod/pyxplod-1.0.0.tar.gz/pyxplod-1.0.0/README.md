# pyxplod

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**pyxplod** is a Python refactoring tool that "explodes" Python files by extracting each class and function definition into separate files, automatically replacing them with imports. This helps break down large Python modules into smaller, more manageable pieces while maintaining functionality.

## Features

- 🔍 **Intelligent code extraction**: Uses Python's AST to accurately identify and extract classes and functions
- 📁 **Structure preservation**: Maintains your project's directory structure in the output
- 🔗 **Automatic imports**: Replaces extracted code with proper relative imports
- ⚡ **Smart import optimization**: Only includes imports actually used in each extracted file (v0.3.0+)
- 🛡️ **Safe operation**: Non-destructive - creates new files without modifying originals
- 📊 **Progress tracking**: Visual progress bars and detailed logging with `rich` and `loguru`
- 🎯 **Smart naming**: Converts class/function names to snake_case for consistent file naming
- 🗂️ **Dual methods**: Choose between flat file structure or package-based organization
- ⚡ **Fast processing**: Efficiently handles large codebases with error recovery

## Installation

### From PyPI (when published)

```bash
pip install pyxplod
```

Or using `uv`:

```bash
uv pip install pyxplod
```

### From Source (Current)

```bash
# Clone the repository
git clone https://github.com/twardoch/pyxplod.git
cd pyxplod

# Install in development mode
uv pip install -e .
```

## Usage

### Basic Usage (Files Method)

```bash
pyxplod --input /path/to/source --output /path/to/output
```

### Using Dirs Method

```bash
pyxplod --input /path/to/source --output /path/to/output --method dirs
```

### With Verbose Logging

```bash
pyxplod --input /path/to/source --output /path/to/output --verbose
```

## Methods

pyxplod supports two different explosion methods:

### Files Method (Default)

The `files` method creates separate files in the same directory structure, with each extracted class/function having a filename prefix based on the original file.

### Dirs Method

The `dirs` method creates a directory (package) for each Python file, with extracted classes and functions as separate modules within that package. An `__init__.py` file contains imports and any remaining module-level code.

## How It Works

Given a Python file like this:

```python
# src/utils.py
import os
from typing import List

class FileHandler:
    def __init__(self):
        self.files = []
    
    def add_file(self, path: str):
        self.files.append(path)

def process_data(data: List[str]) -> str:
    return "\n".join(data)

CONSTANT = "some_value"
```

pyxplod will create different structures based on the method used:

### Files Method Output (Default)

```
output/
└── src/
    ├── utils.py                    # Modified main file
    ├── utils_file_handler.py       # Extracted class
    └── utils_process_data.py       # Extracted function
```

### Dirs Method Output

```
output/
└── src/
    └── utils/
        ├── __init__.py             # Module interface with imports
        ├── file_handler.py         # Extracted class
        └── process_data.py         # Extracted function
```

## Example Contents

### Files Method Output

**output/src/utils.py:**
```python
from typing import List
from .utils_file_handler import FileHandler
from .utils_process_data import process_data

CONSTANT = "some_value"
```

**output/src/utils_file_handler.py:**
```python
class FileHandler:
    def __init__(self):
        self.files = []
    
    def add_file(self, path: str):
        self.files.append(path)
```

**output/src/utils_process_data.py:**
```python
from typing import List

def process_data(data: List[str]) -> str:
    return "\n".join(data)
```

### Dirs Method Output

**output/src/utils/__init__.py:**
```python
from typing import List
from .file_handler import FileHandler
from .process_data import process_data

CONSTANT = "some_value"
```

**output/src/utils/file_handler.py:**
```python
class FileHandler:
    def __init__(self):
        self.files = []
    
    def add_file(self, path: str):
        self.files.append(path)
```

**output/src/utils/process_data.py:**
```python
from typing import List

def process_data(data: List[str]) -> str:
    return "\n".join(data)
```

> **Note**: pyxplod v0.3.0+ automatically optimizes imports - only the imports actually used in each file are included, reducing file sizes by 30-50%.

## Advanced Options

### Command Line Arguments

```bash
pyxplod --help
```

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--input` | Source directory to process | Required | `--input ./src` |
| `--output` | Output directory for exploded files | Required | `--output ./output` |
| `--method` | Processing method: `files` or `dirs` | `files` | `--method dirs` |
| `--verbose` | Enable detailed logging | `False` | `--verbose` |

### Processing Methods Comparison

| Aspect | Files Method | Dirs Method |
|--------|--------------|-------------|
| **Structure** | Flat files with prefixes | Package directories |
| **File naming** | `utils_my_class.py` | `my_class.py` |
| **Organization** | Same directory | Subdirectories with `__init__.py` |
| **Best for** | Simple modules, quick extraction | Complex modules, clean organization |
| **Import style** | `from .utils_my_class import MyClass` | `from .utils.my_class import MyClass` |

## Use Cases

- **Refactoring large modules**: Break down monolithic Python files (500+ lines) into smaller, focused modules
- **Code organization**: Improve project structure by separating concerns and creating logical boundaries
- **Testing**: Make it easier to test individual components in isolation with focused test files
- **Code review**: Simplify code reviews by creating smaller, single-purpose files that are easier to understand
- **Legacy code**: Gradually modernize legacy codebases by extracting reusable components
- **Microservices preparation**: Extract functionality before splitting monoliths into microservices
- **Educational purposes**: Help understand code structure by separating concerns visually

## Features in Detail

### Smart Import Handling
- Preserves all module-level imports in extracted files
- Generates relative imports for the extracted components
- Maintains import order and structure

### Error Handling
- Gracefully handles syntax errors in source files
- Skips files that cannot be parsed
- Provides detailed error messages for troubleshooting

### File Naming
- Converts CamelCase to snake_case automatically
- Handles naming conflicts with automatic deduplication
- Preserves meaningful names while ensuring filesystem compatibility

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/twardoch/pyxplod.git
cd pyxplod

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev,test]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyxplod

# Run specific test
pytest tests/test_pyxplod.py::TestProcessing::test_process_simple_file
```

### Code Quality

```bash
# Auto-format, lint and test (recommended)
fd -e py -x autoflake {}; fd -e py -x pyupgrade --py311-plus {}; fd -e py -x ruff check --output-format=github --fix --unsafe-fixes {}; fd -e py -x ruff format --respect-gitignore --target-version py311 {}; python -m pytest;

# Individual commands
ruff check src/ tests/       # Linting
ruff format src/ tests/      # Formatting  
mypy src/                    # Type checking
```

## Requirements

- Python 3.10 or higher
- Dependencies:
  - `fire` - CLI interface
  - `loguru` - Enhanced logging
  - `rich` - Progress bars and formatting
  - Standard library: `ast`, `pathlib`, `os`

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Limitations & Known Issues

- **Comments**: Comments between class/function definitions may be lost during processing
- **Formatting**: Code formatting may change due to AST parsing and regeneration
- **Nested definitions**: Only top-level classes and functions are extracted (nested classes/functions remain in original files)
- **Decorators**: Some complex decorator chains may need manual review after extraction
- **Large files**: Very large files (>1000 lines) may require more memory and processing time

See [TODO.md](TODO.md) for a complete list of planned improvements.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Set up development environment:
   ```bash
   uv pip install -e ".[dev,test]"
   ```
4. Make your changes and add tests
5. Run the test suite:
   ```bash
   python -m pytest --cov=pyxplod
   ```
6. Ensure code quality:
   ```bash
   fd -e py -x ruff check --fix {}; fd -e py -x ruff format {}
   ```
7. Commit your changes (`git commit -m 'Add some amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Code Guidelines

- Follow PEP 8 style guidelines
- Add type hints using simple syntax (`list`, `dict`, `str | None`)
- Write clear docstrings for all functions and classes
- Add tests for new features and bug fixes
- Keep functions focused and single-purpose

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Author

Created by Adam Twardoch