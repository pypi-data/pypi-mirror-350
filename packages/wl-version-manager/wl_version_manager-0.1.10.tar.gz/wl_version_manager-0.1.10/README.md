# WL Version Manager

A simple Python package for managing semantic versions in Python projects.

## Features

- Automatic version bumping (patch, minor, major)
- Updates both VERSION file and setup.py
- Command-line interface
- Python API for programmatic use
- Follows semantic versioning (major.minor.patch)

## Installation

```bash
pip install wl_wl_version_manager
```

## Usage

### Command Line

```bash
# Initialize version file
wl_version_manager init

# Show current version
wl_version_manager current

# Bump versions
wl_version_manager patch   # 1.0.0 -> 1.0.1
wl_version_manager minor   # 1.0.1 -> 1.1.0
wl_version_manager major   # 1.1.0 -> 2.0.0

# Set specific version
wl_version_manager set 1.2.3
```

### Python API

```python
from wl_version_manager import VersionManager

vm = VersionManager()

# Read current version
current = vm.read_version()

# Bump versions
new_version = vm.bump_patch()
new_version = vm.bump_minor()
new_version = vm.bump_major()

# Set specific version
vm.set_version("2.1.0")
```

### Integration with Makefile

```makefile
build:
	wl_version_manager patch
	python setup.py sdist
```

## File Structure

The tool expects:
- `VERSION` file containing current version
- `setup.py` with version= line to update

## Options

```bash
wl_version_manager --version-file custom_version.txt --setup-file custom_setup.py current
```

## License

BSD 3-Clause License