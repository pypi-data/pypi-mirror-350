# uvs Implementation Guide

## Project Overview

Create `uvs` (uv scripts) - a CLI tool that manages Python scripts stored in GitHub Gists. The tool clones Gists locally and creates PATH-accessible wrapper scripts that execute using `uv run`.

## Tech Stack Requirements

- **Dependency Management**: `uv` for project management
- **CLI Framework**: `typer` for command-line interface
- **Terminal Output**: `rich` for enhanced printing and formatting
- **HTTP Requests**: `httpx` for any HTTP requests needed
- **Testing**: `pytest` for unit testing
- **External Dependencies**: `git` and `uv` (system requirements)

## Project Structure

```
uvs/
├── pyproject.toml           # uv project configuration
├── src/
│   └── uvs/
│       ├── __init__.py
│       ├── main.py          # Entry point with Typer CLI
│       ├── core.py          # Core functionality
│       ├── git_utils.py     # Git operations
│       ├── config.py        # Configuration management
│       ├── path_manager.py  # PATH and wrapper management
│       └── metadata.py      # Script metadata parsing
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_git_utils.py
│   ├── test_config.py
│   ├── test_path_manager.py
│   └── test_metadata.py
└── README.md
```

## pyproject.toml Configuration

```toml
[project]
name = "uvs"
version = "0.1.0"
description = "Manage Python scripts from GitHub Gists with uv"
requires-python = ">=3.8"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "httpx>=0.25.0",
]

[project.scripts]
uvs = "uvs.main:app"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Core Architecture

### 1. main.py - CLI Entry Point

```python
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
from typing import Optional

app = typer.Typer(help="Manage Python scripts from GitHub Gists")
console = Console()

@app.command()
def add(
    url_or_id: str = typer.Argument(..., help="Gist URL or ID"),
    file: Optional[str] = typer.Option(None, "--file", help="Specific file to use as entrypoint")
):
    """Add a script from a GitHub Gist"""
    # Implementation here

@app.command()
def remove(name: str = typer.Argument(..., help="Script name to remove")):
    """Remove an installed script"""
    # Implementation here

@app.command()
def list():
    """List all installed scripts"""
    # Implementation here

@app.command() 
def update(name: Optional[str] = typer.Argument(None, help="Script name to update, or all if not specified")):
    """Update scripts to latest version"""
    # Implementation here

@app.command()
def config():
    """Manage configuration"""
    # Implementation here

if __name__ == "__main__":
    app()
```

### 2. core.py - Core Business Logic

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
import json
import shutil

@dataclass
class InstalledScript:
    name: str
    gist_id: str
    entry_file: str
    clone_url: str
    auth_method: str
    version: Optional[str] = None

class UVSCore:
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.home() / ".uvs"
        self.scripts_dir = self.base_dir / "scripts"
        self.bin_dir = self.base_dir / "bin"
        self.config_file = self.base_dir / "config.json"
        
        # Ensure directories exist
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        self.bin_dir.mkdir(parents=True, exist_ok=True)
    
    def add_script(self, url_or_id: str, explicit_file: Optional[str] = None) -> InstalledScript:
        """Add a script from a Gist"""
        # Parse URL to get clone URL and auth method
        # Clone the Gist
        # Detect main script file
        # Parse metadata for script name
        # Create wrapper script
        # Update registry
        pass
    
    def remove_script(self, name: str) -> bool:
        """Remove an installed script"""
        # Remove from registry
        # Delete wrapper script
        # Delete cloned directory
        pass
    
    def list_scripts(self) -> List[InstalledScript]:
        """List all installed scripts"""
        pass
    
    def update_script(self, name: str) -> bool:
        """Update a specific script"""
        # git pull in the script directory
        # Regenerate wrapper if needed
        pass
    
    def update_all_scripts(self) -> List[str]:
        """Update all scripts"""
        pass
```

### 3. git_utils.py - Git Operations

```python
import subprocess
import re
from typing import Tuple
from pathlib import Path

def parse_gist_url(url_or_id: str) -> Tuple[str, str, str]:
    """
    Parse Gist URL/ID and return (gist_id, clone_url, auth_method)
    
    Returns:
        - gist_id: The 32-character Gist ID
        - clone_url: Full Git clone URL
        - auth_method: "ssh" or "https"
    """
    # SSH format: git@gist.github.com:abc123.git
    if url_or_id.startswith('git@gist.github.com:'):
        gist_id = url_or_id.split(':')[1].replace('.git', '')
        return gist_id, url_or_id, "ssh"
    
    # HTTPS format: https://gist.github.com/username/abc123
    if url_or_id.startswith('https://gist.github.com/'):
        gist_id = url_or_id.split('/')[-1]
        clone_url = f"https://gist.github.com/{gist_id}.git"
        return gist_id, clone_url, "https"
    
    # Just Gist ID: abc123
    if re.match(r'^[a-f0-9]{32}$', url_or_id):
        # Try SSH first if available, fallback to HTTPS
        if has_ssh_key():
            clone_url = f"git@gist.github.com:{url_or_id}.git"
            return url_or_id, clone_url, "ssh"
        else:
            clone_url = f"https://gist.github.com/{url_or_id}.git"
            return url_or_id, clone_url, "https"
    
    raise ValueError(f"Invalid Gist URL or ID: {url_or_id}")

def has_ssh_key() -> bool:
    """Check if SSH key is available for GitHub"""
    try:
        result = subprocess.run(
            ["ssh", "-T", "git@github.com"],
            capture_output=True,
            text=True,
            timeout=5
        )
        # GitHub SSH test returns exit code 1 but with success message
        return "successfully authenticated" in result.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def clone_gist(clone_url: str, destination: Path) -> bool:
    """Clone a Gist to the specified directory"""
    try:
        result = subprocess.run(
            ["git", "clone", clone_url, str(destination)],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone Gist: {e.stderr}")

def update_gist(gist_dir: Path) -> bool:
    """Update a cloned Gist (git pull)"""
    try:
        result = subprocess.run(
            ["git", "pull"],
            cwd=gist_dir,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
```

### 4. metadata.py - Script Metadata Parsing

```python
import re
import tomllib  # Python 3.11+, use tomli for older versions
from pathlib import Path
from typing import Optional, Dict, Any, List

def detect_main_script(gist_dir: Path, explicit_file: Optional[str] = None) -> str:
    """Find the main Python script in a Gist"""
    py_files = [f.name for f in gist_dir.glob("*.py") 
                if not f.name.startswith('test')]
    
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
    
    # 4. Use first .py file alphabetically
    return sorted(py_files)[0]

def parse_script_metadata(script_path: Path) -> Dict[str, Any]:
    """Parse PEP 723 and uvs metadata from a Python script"""
    content = script_path.read_text(encoding='utf-8')
    
    # Look for PEP 723 script metadata block
    pattern = r'# /// script\n(.*?)\n# ///'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return {}
    
    toml_content = match.group(1)
    # Remove leading "# " from each line
    toml_content = '\n'.join(line[2:] if line.startswith('# ') else line 
                            for line in toml_content.split('\n'))
    
    try:
        metadata = tomllib.loads(toml_content)
        return metadata
    except tomllib.TOMLDecodeError:
        return {}

def get_script_name(script_path: Path, metadata: Dict[str, Any]) -> str:
    """Determine the script name from metadata or filename"""
    # Check for custom name in uvs metadata
    if 'tool' in metadata and 'uvs' in metadata['tool']:
        custom_name = metadata['tool']['uvs'].get('name')
        if custom_name:
            return custom_name
    
    # Use filename without extension
    return script_path.stem

def get_dependencies(metadata: Dict[str, Any]) -> List[str]:
    """Extract dependencies from metadata"""
    return metadata.get('dependencies', [])

def get_python_version(metadata: Dict[str, Any]) -> Optional[str]:
    """Extract Python version requirement"""
    return metadata.get('requires-python')
```

### 5. path_manager.py - PATH and Wrapper Management

```python
import os
import platform
from pathlib import Path
from typing import Optional

class PathManager:
    def __init__(self, bin_dir: Path):
        self.bin_dir = bin_dir
        self.is_windows = platform.system() == "Windows"
    
    def create_wrapper_script(self, script_name: str, gist_dir: Path, entry_file: str):
        """Create a wrapper script in the bin directory"""
        if self.is_windows:
            self._create_windows_wrapper(script_name, gist_dir, entry_file)
        else:
            self._create_unix_wrapper(script_name, gist_dir, entry_file)
    
    def _create_unix_wrapper(self, script_name: str, gist_dir: Path, entry_file: str):
        """Create Unix/Linux/macOS wrapper script"""
        wrapper_path = self.bin_dir / script_name
        wrapper_content = f"""#!/bin/bash
# Auto-generated wrapper for {script_name}
cd "{gist_dir}"
exec uv run {entry_file} "$@"
"""
        wrapper_path.write_text(wrapper_content)
        wrapper_path.chmod(0o755)  # Make executable
    
    def _create_windows_wrapper(self, script_name: str, gist_dir: Path, entry_file: str):
        """Create Windows wrapper script"""
        wrapper_path = self.bin_dir / f"{script_name}.cmd"
        wrapper_content = f"""@echo off
REM Auto-generated wrapper for {script_name}
cd "{gist_dir}"
uv run {entry_file} %*
"""
        wrapper_path.write_text(wrapper_content)
    
    def remove_wrapper_script(self, script_name: str):
        """Remove wrapper script"""
        if self.is_windows:
            wrapper_path = self.bin_dir / f"{script_name}.cmd"
        else:
            wrapper_path = self.bin_dir / script_name
        
        if wrapper_path.exists():
            wrapper_path.unlink()
    
    def ensure_bin_in_path(self):
        """Ensure the bin directory is in PATH"""
        # This is a complex operation that should modify shell configs
        # Implementation should handle .bashrc, .zshrc, PowerShell profiles, etc.
        # For now, just warn the user if it's not in PATH
        if str(self.bin_dir) not in os.environ.get('PATH', ''):
            return False
        return True
    
    def get_path_instruction(self) -> str:
        """Get instruction for adding bin dir to PATH"""
        if self.is_windows:
            return f"Add {self.bin_dir} to your PATH environment variable"
        else:
            return f"Add this to your shell config: export PATH=\"{self.bin_dir}:$PATH\""
```

### 6. config.py - Configuration Management

```python
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class UVSConfig:
    github_token: Optional[str] = None
    default_auth: str = "auto"  # "auto", "ssh", "https"
    bin_dir: Optional[str] = None
    scripts_dir: Optional[str] = None

class ConfigManager:
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self._config = self._load_config()
    
    def _load_config(self) -> UVSConfig:
        """Load configuration from file"""
        if not self.config_file.exists():
            return UVSConfig()
        
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            return UVSConfig(**data)
        except (json.JSONDecodeError, TypeError):
            return UVSConfig()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(asdict(self._config), f, indent=2)
    
    def get(self, key: str) -> Any:
        """Get configuration value"""
        return getattr(self._config, key, None)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        if hasattr(self._config, key):
            setattr(self._config, key, value)
            self.save_config()
        else:
            raise KeyError(f"Unknown configuration key: {key}")
    
    @property
    def github_token(self) -> Optional[str]:
        return self._config.github_token
    
    @github_token.setter
    def github_token(self, value: Optional[str]):
        self._config.github_token = value
        self.save_config()
```

## Error Handling Strategy

### Custom Exceptions
```python
class UVSError(Exception):
    """Base exception for uvs"""
    pass

class GitError(UVSError):
    """Git operation failed"""
    pass

class GistNotFoundError(UVSError):
    """Gist not found or not accessible"""
    pass

class ScriptNotFoundError(UVSError):
    """Script not found in registry"""
    pass

class InvalidGistError(UVSError):
    """Gist doesn't contain valid Python scripts"""
    pass
```

### Rich Error Display
```python
from rich.console import Console
from rich.panel import Panel

console = Console()

def handle_error(error: Exception):
    """Display errors with Rich formatting"""
    if isinstance(error, GitError):
        console.print(Panel(str(error), title="Git Error", style="red"))
    elif isinstance(error, GistNotFoundError):
        console.print(Panel(str(error), title="Gist Not Found", style="yellow"))
    else:
        console.print(Panel(str(error), title="Error", style="red"))
```

## Testing Strategy

### Test Structure
```python
# tests/test_core.py
import pytest
from pathlib import Path
from uvs.core import UVSCore
from uvs.git_utils import parse_gist_url

def test_parse_gist_url_https():
    gist_id, clone_url, auth_method = parse_gist_url("https://gist.github.com/user/abc123")
    assert gist_id == "abc123"
    assert clone_url == "https://gist.github.com/abc123.git"
    assert auth_method == "https"

def test_parse_gist_url_ssh():
    gist_id, clone_url, auth_method = parse_gist_url("git@gist.github.com:abc123.git")
    assert gist_id == "abc123"
    assert clone_url == "git@gist.github.com:abc123.git"
    assert auth_method == "ssh"

# Use pytest fixtures for temporary directories
@pytest.fixture
def temp_uvs_dir(tmp_path):
    return UVSCore(base_dir=tmp_path)
```

## Registry Management

### Scripts Registry Format
Store installed scripts in `~/.uvs/registry.json`:
```json
{
  "scripts": {
    "my-tool": {
      "name": "my-tool",
      "gist_id": "abc123def456",
      "entry_file": "main.py",
      "clone_url": "https://gist.github.com/abc123def456.git",
      "auth_method": "https",
      "version": "1.0.0",
      "installed_at": "2025-05-26T10:00:00Z",
      "updated_at": "2025-05-26T10:00:00Z"
    }
  }
}
```

## Rich UI Components

### Progress Indicators
```python
from rich.progress import Progress, SpinnerColumn, TextColumn

def clone_with_progress(clone_url: str, destination: Path):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Cloning Gist...", total=None)
        # Perform clone operation
        clone_gist(clone_url, destination)
        progress.update(task, completed=True)
```

### Tables for Listing
```python
from rich.table import Table

def display_scripts_table(scripts: List[InstalledScript]):
    table = Table(title="Installed Scripts")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Gist ID", style="yellow")
    table.add_column("Entry File", style="blue")
    
    for script in scripts:
        table.add_row(
            script.name,
            script.version or "unknown",
            script.gist_id,
            script.entry_file
        )
    
    console.print(table)
```

## Implementation Steps

1. **Initialize Project**
   ```bash
   uv init uvs
   cd uvs
   uv add typer rich httpx
   uv add --dev pytest pytest-cov
   ```

2. **Create Basic CLI Structure**
   - Implement `main.py` with Typer commands
   - Add basic argument parsing and help text

3. **Implement Git Operations**
   - URL parsing logic
   - SSH key detection
   - Git clone/pull operations

4. **Add Metadata Parsing**
   - PEP 723 parser
   - Script name resolution
   - Dependency extraction

5. **Implement Core Logic**
   - Script installation workflow
   - Registry management
   - Wrapper script generation

6. **Add PATH Management**
   - Cross-platform wrapper creation
   - PATH detection and warnings

7. **Implement Configuration**
   - Config file management
   - Token storage
   - User preferences

8. **Add Rich UI**
   - Progress indicators
   - Error formatting
   - Tables for listing

9. **Write Tests**
   - Unit tests for all modules
   - Integration tests for workflows
   - Mock Git operations for testing

10. **Documentation**
    - CLI help text
    - README with examples
    - Installation instructions

## Entry Point Configuration

Ensure the CLI is accessible via `uvs` command by configuring the entry point in `pyproject.toml`:

```toml
[project.scripts]
uvs = "uvs.main:app"
```

This implementation guide provides a complete roadmap for building the `uvs` tool with all specified requirements and best practices for CLI tools using the modern Python ecosystem.
