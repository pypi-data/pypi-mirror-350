# TuMee CodeGuard

A powerful file change detection tool that identifies, tracks, and validates code modifications with a focus on respecting designated "guarded" regions across multiple programming languages.

**Package Name:** `tumee-codeguard`  
**Command:** `codeguard`

## Installation

### Prerequisites

- Python 3.10 or higher
- Git (for version control integration)

### Setup

#### On macOS/Linux

```bash
# Make the install script executable
chmod +x install.sh

# Run the installation script
./install.sh
```

#### On Windows

```cmd
# Run the installation script
install.bat
```

## Usage

### Running CodeGuard

#### On macOS/Linux

```bash
# Run CodeGuard
./run_codeguard.sh [command] [options]

# For example, to get help
./run_codeguard.sh --help

# To get effective permissions for a file
./run_codeguard.sh acl /path/to/file
```

#### On Windows

```cmd
# Run CodeGuard
run_codeguard.bat [command] [options]

# For example, to get help
run_codeguard.bat --help

# To get effective permissions for a file
run_codeguard.bat acl C:\path\to\file
```

## Commands

- `acl` - Get effective permissions for a file or directory
- `batch-acl` - Get permissions for multiple paths in a batch
- `aiattributes` - Manage directory-level guard annotations via .ai-attributes files
- `list-guarded-directories` - List directories with guard annotations
- `verify` - Compare two files directly
- `verify-disk` - Compare modified file against current version on disk
- `verify-git` - Compare against last checked-in version in git
- `verify-revision` - Compare against specific revision
- `scan` - Batch operations on directories
- `install-hook` - Install git pre-commit hook
- `serve` - Start MCP server

## Examples

### Managing Directory-Level Guard Annotations

```bash
# Create or update an .ai-attributes file
./run_codeguard.sh aiattributes create --directory ./src --rule "*.py:AI-RO" --description "*.py:Python files are AI read-only"

# List rules from .ai-attributes files
./run_codeguard.sh aiattributes list --directory ./src --recursive

# Validate .ai-attributes files
./run_codeguard.sh aiattributes validate --directory ./src --recursive
```

### Getting Access Control Information

```bash
# Get effective permissions for a file
./run_codeguard.sh acl ./src/main.py --verbose

# Get permissions for multiple paths in a batch
./run_codeguard.sh batch-acl ./src/main.py ./src/utils.py ./src/config.py

# List directories with guard annotations
./run_codeguard.sh list-guarded-directories --directory ./src
```

### Code Validation

```bash
# Compare two files directly
./run_codeguard.sh verify --original ./original.py --modified ./modified.py

# Compare against the last checked-in version in git
./run_codeguard.sh verify-git --file ./src/main.py

# Compare against a specific revision
./run_codeguard.sh verify-revision --file ./src/main.py --from-revision HEAD~3
```

## Guard Annotation System

CodeGuard supports a standardized guard notation that works across programming languages:

```
@GUARD:WHO-PERMISSION
```

Where:
- `@GUARD`: The prefix that identifies this as a guard directive
- `WHO`: Indicates who the rule applies to (`AI` for AI systems, `HU` for human developers, `ALL` for both)
- `PERMISSION`: Specifies the permission level (`RO` for read-only, `ED` for editable with reason, `FX` for fixed/unchangeable)

### Examples

```python
# @GUARD:AI-RO This is an AI read-only section
def sensitive_function():
    pass

# @GUARD:HU-ED Humans can edit this section with good reason
def editable_function():
    pass

"""
@GUARD:ALL-FX
This section is fixed for everyone
"""
```

## Directory-Level Guard System

CodeGuard supports directory-level guard annotations through `.ai-attributes` files:

```
# All files in this directory are AI read-only
* @GUARD:AI-RO

# All Python files in this directory and subdirectories are fixed
**/*.py @GUARD:ALL-FX

# Test files in the tests directory can be edited
tests/* @GUARD:ALL-ED
```
