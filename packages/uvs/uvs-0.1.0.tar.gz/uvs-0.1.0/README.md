# uvs - UV Script management

`uvs` (uv scripts) is a simple command-line tool that manages Python scripts stored in GitHub Gists or from local files/directories. It clones Gists or copies local scripts, and creates PATH-accessible wrapper scripts that execute using `uv run`.

## Installation

```bash
uv tool install uvs
```

## Usage

### Adding Scripts from Gists

```bash
# Add a script using any Gist URL format
uvs add https://gist.github.com/username/abc123def456
uvs add https://gist.github.com/abc123def456  
uvs add git@gist.github.com:abc123def456.git
uvs add abc123def456  # Just the Gist ID

# Specify a specific file as entrypoint
uvs add abc123def456 --file utils.py
```

### Adding Local Scripts (File or Directory)

```bash
# Add a single local script
uvs copy /path/to/myscript.py

# Add a directory of scripts (will auto-detect main entrypoint)
uvs copy /path/to/myproject/

# Specify a specific file as entrypoint in a directory
uvs copy /path/to/myproject/ --file main.py

# Optionally override the script name
uvs copy /path/to/myscript.py --name mytool
```

### Managing Scripts

```bash
# Remove a script
uvs remove <script-name>

# List installed scripts (local and Gist scripts are shown separately)
uvs list

# Update scripts to latest version
uvs update [script-name]

# Completely remove all uvs installed scripts
uvs self delete

# Show uvs version
uvs self version

# Ensure uvs bin directory is in your PATH
uvs self ensurepath
```

### Configuration

```bash
# Set GitHub token
uvs config set github_token <token>

# Get current token
uvs config get github_token

# Remove token
uvs config unset github_token
```

## Script Metadata

Scripts may include metadata using a PEP 723-style block that specifies the Python version and any dependencies. Any other metadata may be specified inside a `[tool.uvs]` TOML table. For example:

```python
# /// script
# requires-python = ">=3.8"
# dependencies = ["requests", "click>=8.0"]
# [tool.uvs]
# name = "my-script-name"
# description = "A basic example of a script"
# ///
```

- `dependencies` can be a comma-separated list.
- `requires-python` specifies the minimum Python version.
- `[tool.uvs]` TOML section in comments for advanced options which can be used to specify a custom `name` or any other metadata to be added to the `pyproject.toml` if the script is packaged.

## Packaging Scripts

You can create a minimal Python package from an installed script using:

```bash
uvs package <script-name> --output <output-dir>
```

This will:
- Extract metadata (description, dependencies, requires-python, etc.) from the script.
- Generate a `pyproject.toml` and `README.md`.
- Copy all Python files and create a package structure in `<output-dir>`, along with the wheels.
- If `--output` is not specified then only the wheels will be generated in a folder in the current directory.

## Project Structure

```
~/.uvs/
├── scripts/
│   ├── gist-abc123/        # Cloned Gist repository
│   │   ├── script.py
│   │   └── .git/
│   ├── local-mytool/       # Local script or directory
│   │   └── myscript.py
│   └── gist-def456/
│       ├── tool.py
│       └── .git/
├── bin/                    # PATH wrapper scripts
│   ├── script              # Points to gist-abc123/script.py
│   ├── tool                # Points to gist-def456/tool.py
│   └── mytool              # Points to local-mytool/myscript.py
└── config.json             # Simple configuration
```

## Requirements

- Python 3.11 or higher
- `uv` package manager
- `git` command-line tool
