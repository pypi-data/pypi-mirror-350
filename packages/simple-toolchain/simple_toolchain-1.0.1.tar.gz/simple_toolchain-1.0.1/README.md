# Simple Toolchain (tc)

A simple command line utility to manage your Python scripts and single-file web apps with automatic dependency isolation.

## Installation

```bash
pip install -e .
```

## Requirements

- **uv** (recommended): For automatic dependency isolation when running Python scripts
  - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - If `uv` is not available, scripts will fall back to system Python

## Usage

### Add a script or web app
```bash
tc add script.py my_script
tc add webapp.html my_webapp
```

### Run a stored item
```bash
tc run my_script
tc run my_webapp
```

### List all stored items
```bash
tc list
```

### Remove a stored item
```bash
tc remove my_script
```

## How it works

- Files are copied to `~/.toolchain/` directory
- Python scripts are stored in `~/.toolchain/scripts/`
- HTML files are stored in `~/.toolchain/webapps/`
- Metadata is tracked in `~/.toolchain/metadata.json`
- Running scripts uses `uv run` for automatic dependency isolation (or falls back to system Python)
- Running web apps opens them in your default browser

## Dependency Management

When using `uv run` (recommended), each script runs in its own isolated environment:
- Dependencies are automatically installed from script imports
- No need to manually install packages on your system
- Each script gets a clean, isolated Python environment
- Add dependencies to your scripts using standard Python imports or `# /// script` metadata blocks

## Supported file types

- `.py` - Python scripts
- `.html` - Single-file web applications