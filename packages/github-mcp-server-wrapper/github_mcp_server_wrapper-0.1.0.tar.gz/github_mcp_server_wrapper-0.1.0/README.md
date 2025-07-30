# github-mcp-server-wrapper

A Python wrapper that allows you to install and run the official GitHub `github-mcp-server` Go binary using `uvx`.

ex: `uvx github-mcp-server stdio`

## How it works

This wrapper:
1. Downloads the appropriate `github-mcp-server` binary for your platform from GitHub releases
2. Caches it in `~/.cache/uvx-go-binaries/`
3. Runs the binary with any arguments you provide

## Setup

### Option 1: Install from PyPI

```bash
uvx github-mcp-server
```

### Option 2: Install from local directory

1. Create a directory for your package:
```bash
mkdir github-mcp-server-wrapper
cd github-mcp-server-wrapper
```

2. Create the package structure:
```
github-mcp-server-wrapper/
├── pyproject.toml
├── README.md
└── github_mcp_server_wrapper.py
```

3. Copy the provided files into the directory

4. Install and run using uvx:
```bash
# Run directly from the directory
uvx --from . github-mcp-server

# Or install globally
uv pip install .
```

### Option 3: Install from GitHub (your repository)

Once you push this to your GitHub repository:

```bash
uvx --from git+https://github.com/yourusername/github-mcp-server-wrapper github-mcp-server
```

## Usage

Once installed, you can run the Go binary through uvx:

```bash
# Run with no arguments
uvx github-mcp-server

# Pass arguments to the Go binary
uvx github-mcp-server --help
uvx github-mcp-server --config config.json
```

## Publishing to PyPI

To make this available for everyone via `uvx github-mcp-server`:

1. Create an account on [PyPI](https://pypi.org)

2. Build the package:
```bash
pip install build
python -m build
```

3. Upload to PyPI:
```bash
pip install twine
twine upload dist/*
```

After publishing, anyone can run:
```bash
uvx github-mcp-server
```

## Requirements

- Python 3.8+
- `uv` and `uvx` installed
- Internet connection (for downloading the Go binary)

## How it handles different platforms

The wrapper automatically detects your OS and architecture and downloads the appropriate binary:
- macOS (darwin): amd64, arm64
- Linux: amd64, arm64, arm
- Windows: amd64, arm64

## License

MIT License