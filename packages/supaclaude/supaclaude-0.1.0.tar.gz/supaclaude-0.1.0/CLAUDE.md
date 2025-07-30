# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI wrapper for the `claude` bash command that adds enhanced JSON output formatting using the `rich` library.

## Commands

### Development
```bash
# Run the main script directly with uv
uv run main.py [args]

# Install the project (after building)
uv pip install -e .

# Run the installed CLI
supaclaude [args]  # All args are passed to claude command
```

### Testing
```bash
# Test basic functionality with uv
uv run main.py --help

# Test JSON stream formatting
uv run main.py --output-format stream-json [other args]
```

## Architecture

The CLI is a thin wrapper around the `claude` bash command with the following behavior:
- All arguments are passed directly to the underlying `claude` command
- When `--output-format stream-json` is detected, the output is parsed and formatted using `rich.print()` for better readability
- Otherwise, output is passed through unchanged

## Implementation Notes

- The main entry point is `main.py` which should use `subprocess` to call the `claude` command
- Python files use uv script syntax with inline dependencies: `# /// script` blocks at the top
- Dependencies should be declared both in the script header (for `uv run`) and in `pyproject.toml` (for installation)
- Must handle streaming output properly for the JSON formatting case
- Error handling should preserve the exit code from the underlying `claude` command
- The `rich` library needs to be added as a dependency in both locations