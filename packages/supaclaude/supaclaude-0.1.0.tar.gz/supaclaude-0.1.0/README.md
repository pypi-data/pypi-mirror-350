# supaclaude

Enhanced CLI wrapper for Claude with beautiful JSON formatting using Rich.

![PyPI version](https://badge.fury.io/py/supaclaude.svg)
![Python Support](https://img.shields.io/pypi/pyversions/supaclaude.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- Beautiful JSON formatting with Rich panels
- Drop-in replacement for the `claude` CLI
- Zero configuration required
- Automatic detection of `--output-format stream-json`
- Preserves all original Claude CLI functionality

## Installation

```bash
pip install supaclaude
```

## Usage

Simply use `supaclaude` as a drop-in replacement for the `claude` command:

```bash
# Regular usage - passes through as normal
supaclaude "What is the weather today?"

# JSON stream formatting - automatically formats with Rich
supaclaude -p "Create a Python hello world" --output-format stream-json --verbose

# All claude flags and options work as expected
supaclaude --help
supaclaude --version
```

### JSON Formatting

When using `--output-format stream-json`, supaclaude automatically:
- Parses each JSON object in the stream
- Formats it with syntax highlighting
- Wraps it in a beautiful panel with rounded borders
- Uses cyan borders for valid JSON and yellow for non-JSON output

## Requirements

- Python 3.8+
- `claude` CLI installed and available in PATH
- Rich library (automatically installed)

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/supaclaude.git
cd supaclaude

# Install with uv
uv pip install -e .

# Run tests
uv run supaclaude --help
```

## Building and Publishing

```bash
# Build the package
uv build

# Upload to PyPI
uv publish
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built on top of Anthropic's Claude CLI
- Beautiful formatting powered by [Rich](https://github.com/Textualize/rich)