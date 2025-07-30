# uvs - Simple Script Registry Tool

## Overview

`uvs` (uv scripts) is a simple command-line tool that manages Python scripts stored in GitHub Gists. It clones Gists locally and creates PATH-accessible wrapper scripts that execute using `uv run`.

## Core Functionality

### Installation
```bash
# Add a script using any Gist URL format
uvs add https://gist.github.com/username/abc123def456
uvs add https://gist.github.com/abc123def456  
uvs add git@gist.github.com:abc123def456.git
uvs add abc123def456  # Just the Gist ID

# Specify a specific file as entrypoint
uvs add abc123def456 --file utils.py

# Remove a script
uvs remove <script-name>

# List installed scripts
uvs list

# Update scripts to latest version
uvs update [script-name]
```

## Architecture

```
~/.uvs/
├── scripts/
│   ├── gist-abc123/         # Cloned Gist repository
│   │   ├── script.py
│   │   └── .git/
│   └── gist-def456/
│       ├── tool.py
│       └── .git/
├── bin/                     # PATH wrapper scripts
│   ├── script              # Points to gist-abc123/script.py
│   └── tool                # Points to gist-def456/tool.py
└── config.json             # Simple configuration
```

## Script Metadata (Optional PEP 723)

Scripts can include PEP 723 metadata for dependencies and naming:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["requests", "click>=8.0"]
# ///

# Optional: Override executable name
# [tool.uvs]
# name = "my-tool"

import click

@click.command()
def main():
    click.echo("Hello from my tool!")

if __name__ == "__main__":
    main()
```

## Wrapper Script Generation

### Unix/Linux/macOS (`~/.uvs/bin/script-name`)
```bash
#!/bin/bash
cd "$HOME/.uvs/scripts/gist-abc123"
exec uv run script.py "$@"
```

### Windows (`~/.uvs/bin/script-name.cmd`)
```cmd
@echo off
cd "%USERPROFILE%\.uvs\scripts\gist-abc123"
uv run script.py %*
```

## URL Format Detection & Authentication

The tool automatically detects authentication method based on URL format:

### HTTPS URLs (Token or No Auth)
```bash
# Input: https://gist.github.com/username/abc123def456
# Uses: git clone https://gist.github.com/abc123def456.git
# Auth: Uses stored token if available, otherwise public access

# Input: https://gist.github.com/abc123def456  
# Uses: git clone https://gist.github.com/abc123def456.git
# Auth: Uses stored token if available, otherwise public access
```

### SSH URLs (SSH Key Auth)
```bash
# Input: git@gist.github.com:abc123def456.git
# Uses: git clone git@gist.github.com:abc123def456.git
# Auth: Uses SSH key authentication
```

### Gist ID Only (Smart Default)
```bash
# Input: abc123def456
# Uses: SSH if key available, otherwise HTTPS
# Tries: git@gist.github.com:abc123def456.git
# Falls back to: https://gist.github.com/abc123def456.git
```

## Configuration

Simple JSON configuration at `~/.uvs/config.json`:

```json
{
  "github_token": "optional-token",
  "default_auth": "ssh",
  "bin_dir": "~/.uvs/bin",
  "scripts_dir": "~/.uvs/scripts"
}
```

## CLI Commands

### `uvs add <gist-id> [options]`
- Clones the Gist to `~/.uvs/scripts/gist-<id>/`
- Parses metadata to determine script name
- Creates wrapper script in `~/.uvs/bin/`
- Options:
  - `--token <token>`: Use GitHub token
  - `--ssh`: Use SSH authentication
  - `--name <name>`: Override script name

### `uvs remove <script-name>`
- Removes wrapper script from `~/.uvs/bin/`
- Removes cloned Gist directory
- Confirms before deletion

### `uvs list`
- Shows installed scripts with versions and sources
- Format: `script-name (v1.0.0) - gist-abc123`

### `uvs update [script-name]`
- Runs `git pull` in Gist directories
- Updates wrapper scripts if metadata changed
- If no script specified, updates all

### `uvs config`
- `uvs config set github_token <token>`
- `uvs config get github_token`
- `uvs config unset github_token`

## Script Name Resolution

1. Check for `[tool.uvs] name = "custom-name"` in the main script
2. Use main script filename without extension (e.g., `main.py` → `main`)
3. Use Gist ID as fallback

### Main Script Selection Priority
1. **`--file` argument** - explicitly specified file (must exist and not be a test file)
2. **`main.py`** - if present
3. **`script.py`** - if present  
4. **First `.py` file** alphabetically (excluding `test*.py` files)
5. **Error** if no Python files found

## PATH Management

- Automatically adds `~/.uvs/bin` to PATH during first installation
- Modifies shell configuration files (`.bashrc`, `.zshrc`, etc.)
- Cross-platform support (Windows PowerShell profile)

## Error Handling

- Graceful failure for network issues
- Clear error messages for authentication problems
- Validation of Gist contents (must contain Python files, excluding test files)
- Conflict resolution for duplicate script names

## Implementation Notes

### Core Dependencies
- `git` (system requirement)
- `uv` (system requirement) 
- Python standard library only (no external dependencies)

### URL Parsing Logic
```python
def parse_gist_url(url_or_id):
    """Parse various Gist URL formats and return clone URL + auth method"""
    
    # SSH format: git@gist.github.com:abc123.git
    if url_or_id.startswith('git@gist.github.com:'):
        gist_id = url_or_id.split(':')[1].replace('.git', '')
        return f"git@gist.github.com:{gist_id}.git", "ssh"
    
    # HTTPS format: https://gist.github.com/username/abc123
    if url_or_id.startswith('https://gist.github.com/'):
        gist_id = url_or_id.split('/')[-1]
        return f"https://gist.github.com/{gist_id}.git", "https"
    
    # Just Gist ID: abc123
    if len(url_or_id) == 32:  # GitHub Gist IDs are 32 chars
        # Try SSH first if key available, fallback to HTTPS
        if has_ssh_key():
            return f"git@gist.github.com:{url_or_id}.git", "ssh"
        else:
            return f"https://gist.github.com/{url_or_id}.git", "https"
    
    raise ValueError(f"Invalid Gist URL or ID: {url_or_id}")
```

### File Structure Detection
```python
def detect_main_script(gist_dir, explicit_file=None):
    """Find the main Python script in a Gist"""
    py_files = [f for f in os.listdir(gist_dir) 
                if f.endswith('.py') and not f.startswith('test')]
    
    if not py_files:
        raise ValueError("No Python files found in Gist")
    
    # 1. Use explicitly specified file if provided
    if explicit_file:
        if explicit_file not in py_files:
            raise ValueError(f"Specified file '{explicit_file}' not found or is a test file")
        return explicit_file
    
    # 2. Check for main.py
    if 'main.py' in py_files:
        return 'main.py'
    
    # 3. Check for script.py  
    if 'script.py' in py_files:
        return 'script.py'
    
    # 4. Use first .py file alphabetically (excluding test files)
    return sorted(py_files)[0]
```

### Wrapper Template
```python
UNIX_WRAPPER = """#!/bin/bash
cd "{script_dir}"
exec uv run {script_file} "$@"
"""

WINDOWS_WRAPPER = """@echo off
cd "{script_dir}"
uv run {script_file} %*
"""
```

## Example Workflow

```bash
# Install uvs
pip install uvs

# Add scripts using any URL format
uvs add https://gist.github.com/username/a1b2c3d4e5f6
uvs add git@gist.github.com:x9y8z7w6v5u4.git  
uvs add a1b2c3d4e5f6  # Just the ID - auto-detects auth

# Add script with specific entrypoint
uvs add abc123def456 --file data_processor.py

# Run the script (now in PATH)
my-script --help
data-processor --input data.csv

# Update all scripts
uvs update

# Remove a script
uvs remove my-script
```

## Security Considerations

- Scripts run with user permissions
- No automatic execution during installation
- Git authentication handled by Git itself
- Clear separation between tool and script execution

## Future Enhancements (Optional)

- `uvs publish <script.py>` - Create and upload to new Gist
- `uvs search <query>` - Search public Gists (if GitHub API allows)
- `uvs info <script-name>` - Show script details and dependencies
- Shell completion for installed scripts

This simplified approach focuses on the core value proposition: easy distribution and execution of Python scripts via GitHub Gists with minimal complexity.
