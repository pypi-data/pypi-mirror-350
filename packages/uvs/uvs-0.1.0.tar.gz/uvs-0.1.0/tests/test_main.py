"""Tests for the main CLI module."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from typer.testing import CliRunner

from uvs.main import app

runner = CliRunner()


@dataclass
class MockScript:
    """Mock script for testing."""

    name: str
    gist_id: str | None
    entry_file: str
    is_local: bool = False
    updated_at: str | None = None
    clone_url: str | None = None


class MockCore:
    """Mock core for testing."""

    def __init__(self, scripts: list[MockScript], scripts_dir: Path, bin_dir: Path):
        self.scripts = scripts
        self.scripts_dir = scripts_dir
        self.bin_dir = bin_dir

    def list_scripts(self) -> list[MockScript]:
        """List all scripts."""
        return self.scripts

    def add_script(self, url_or_id: str, file: str | None = None, name: str | None = None) -> MockScript:
        """Add a script."""
        return self.scripts[0]

    def remove_script(self, name: str) -> bool:
        """Remove a script."""
        return True

    def update_script(self, name: str) -> bool:
        """Update a script."""
        return True

    def update_all_scripts(self) -> list[str]:
        """Update all scripts."""
        return [s.name for s in self.scripts]

    def copy_script(self, path: str, file: str | None = None, name: str | None = None) -> MockScript:
        """Copy a script."""
        return self.scripts[0]


def test_package_command(tmp_path, monkeypatch):
    """Test the package command."""
    # Mock the core and script data
    mock_scripts = [
        MockScript(
            name="test-script",
            gist_id="123",
            entry_file="main.py",
            is_local=False,
        )
    ]
    mock_core = MockCore(mock_scripts, tmp_path, tmp_path)
    monkeypatch.setattr("uvs.main.get_core", lambda: mock_core)

    # Create a mock script directory with multiple Python files
    script_dir = tmp_path / "gist-123"
    script_dir.mkdir()

    # Create main.py with relative imports
    main_file = script_dir / "main.py"
    main_file.write_text(
        '''"""Test script.

# /// script
# requires-python = ">=3.9"
# dependencies = ["requests>=2.0.0", "click>=8.0.0"]
# [tool.uvs]
# description = "Test script description"
# ///
"""
from .utils import helper_function
from .submodule import sub_function

def main():
    print(helper_function())
    print(sub_function())
"""
'''
    )

    # Create utils.py
    utils_file = script_dir / "utils.py"
    utils_file.write_text(
        '''"""Utility functions."""

def helper_function():
    return "Helper function called"
'''
    )

    # Create submodule directory with __init__.py and module.py
    submodule_dir = script_dir / "submodule"
    submodule_dir.mkdir()
    init_file = submodule_dir / "__init__.py"
    init_file.write_text('"""Submodule package."""\n')

    module_file = submodule_dir / "module.py"
    module_file.write_text(
        '''"""Submodule functions."""

def sub_function():
    return "Submodule function called"
'''
    )

    # Run the package command
    result = runner.invoke(app, ["package", "test-script", "--output", str(tmp_path / "package")])
    if result.exit_code != 0:
        print("\nSTDOUT:\n", result.stdout)
        print("\nSTDERR:\n", result.stderr)
    assert result.exit_code == 0

    # Check that the package files were created
    package_dir = tmp_path / "package"
    assert package_dir.exists()
    assert (package_dir / "pyproject.toml").exists()
    assert (package_dir / "README.md").exists()

    # Check that all Python files were copied with correct structure
    src_dir = package_dir / "src" / "test_script"
    assert (src_dir / "__init__.py").exists()
    assert (src_dir / "main.py").exists()
    assert (src_dir / "utils.py").exists()
    assert (src_dir / "submodule" / "__init__.py").exists()
    assert (src_dir / "submodule" / "module.py").exists()

    # Check entry point script
    entry_point = package_dir / "src" / "test_script_cli.py"
    assert entry_point.exists()
    assert "from test_script.main import main" in entry_point.read_text()

    # Check pyproject.toml contents

    with open(package_dir / "pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)

    assert pyproject["project"]["name"] == "test-script"
    assert pyproject["project"]["description"] == "Test script description"
    assert pyproject["project"]["requires-python"] == ">=3.9"
    assert "requests>=2.0.0" in pyproject["project"]["dependencies"]
    assert "click>=8.0.0" in pyproject["project"]["dependencies"]

    # Check entry point configuration
    assert "scripts" in pyproject["project"]
    assert pyproject["project"]["scripts"]["test-script"] == "test_script_cli:main"


def test_package_command_with_relative_imports(tmp_path, monkeypatch):
    """Test packaging a script with relative imports."""
    # Mock the core and script data
    mock_scripts = [
        MockScript(
            name="test-script",
            gist_id="123",
            entry_file="main.py",
            is_local=False,
        )
    ]
    mock_core = MockCore(mock_scripts, tmp_path, tmp_path)
    monkeypatch.setattr("uvs.main.get_core", lambda: mock_core)

    # Create a mock script directory with multiple Python files
    script_dir = tmp_path / "gist-123"
    script_dir.mkdir()

    # Create main.py with relative imports
    main_file = script_dir / "main.py"
    main_file.write_text(
        '''"""Test script.

# /// script
# requires-python = ">=3.9"
# dependencies = ["requests>=2.0.0", "click>=8.0.0"]
# [tool.uvs]
# description = "Test script description"
# ///
"""
from .utils import helper_function
from .submodule import sub_function

def main():
    print(helper_function())
    print(sub_function())
"""
'''
    )

    # Create utils.py
    utils_file = script_dir / "utils.py"
    utils_file.write_text(
        '''"""Utility functions."""

def helper_function():
    return "Helper function called"
'''
    )

    # Create submodule directory with __init__.py and module.py
    submodule_dir = script_dir / "submodule"
    submodule_dir.mkdir()
    init_file = submodule_dir / "__init__.py"
    init_file.write_text('"""Submodule package."""\n')

    module_file = submodule_dir / "module.py"
    module_file.write_text(
        '''"""Submodule functions."""

def sub_function():
    return "Submodule function called"
'''
    )

    # Run the package command
    result = runner.invoke(app, ["package", "test-script", "--output", str(tmp_path / "package")])
    if result.exit_code != 0:
        print("\nSTDOUT:\n", result.stdout)
        print("\nSTDERR:\n", result.stderr)
    assert result.exit_code == 0

    # Check that the package files were created
    package_dir = tmp_path / "package"
    assert package_dir.exists()
    assert (package_dir / "pyproject.toml").exists()
    assert (package_dir / "README.md").exists()

    # Check that all Python files were copied with correct structure
    src_dir = package_dir / "src" / "test_script"
    assert (src_dir / "__init__.py").exists()
    assert (src_dir / "main.py").exists()
    assert (src_dir / "utils.py").exists()
    assert (src_dir / "submodule" / "__init__.py").exists()
    assert (src_dir / "submodule" / "module.py").exists()

    # Check entry point script
    entry_point = package_dir / "src" / "test_script_cli.py"
    assert entry_point.exists()
    assert "from test_script.main import main" in entry_point.read_text()

    # Check pyproject.toml contents
    with open(package_dir / "pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)

    assert pyproject["project"]["name"] == "test-script"
    assert pyproject["project"]["description"] == "Test script description"
    assert pyproject["project"]["requires-python"] == ">=3.9"
    assert "requests>=2.0.0" in pyproject["project"]["dependencies"]
    assert "click>=8.0.0" in pyproject["project"]["dependencies"]

    # Check entry point configuration
    assert "scripts" in pyproject["project"]
    assert pyproject["project"]["scripts"]["test-script"] == "test_script_cli:main"


def test_package_command_with_local_script(tmp_path, monkeypatch):
    """Test packaging a local script."""
    mock_scripts = [
        MockScript(
            name="local-script",
            gist_id=None,
            entry_file="main.py",
            is_local=True,
        )
    ]
    mock_core = MockCore(mock_scripts, tmp_path, tmp_path)
    monkeypatch.setattr("uvs.main.get_core", lambda: mock_core)

    # Create a mock local script directory
    script_dir = tmp_path / "local-local-script"
    script_dir.mkdir()

    # Create main.py with metadata
    main_file = script_dir / "main.py"
    main_file.write_text(
        '''"""Local script.

# /// script
# requires-python = ">=3.8"
# dependencies = ["typer>=0.9.0"]
# [tool.uvs]
# description = "Local script description"
# ///
"""
def main():
    print("Local script")
"""
'''
    )

    # Run the package command
    result = runner.invoke(app, ["package", "local-script", "--output", str(tmp_path / "package")])
    if result.exit_code != 0:
        print("\nSTDOUT:\n", result.stdout)
        print("\nSTDERR:\n", result.stderr)
    assert result.exit_code == 0

    # Verify package structure
    package_dir = tmp_path / "package"
    assert (package_dir / "src" / "local_script" / "main.py").exists()

    # Check pyproject.toml
    with open(package_dir / "pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)

    assert pyproject["project"]["name"] == "local-script"
    assert pyproject["project"]["description"] == "Local script description"
    assert "typer>=0.9.0" in pyproject["project"]["dependencies"]


def test_package_command_with_nested_imports(tmp_path, monkeypatch):
    """Test packaging a script with deeply nested imports."""
    mock_scripts = [
        MockScript(
            name="nested-script",
            gist_id="456",
            entry_file="main.py",
            is_local=False,
        )
    ]
    mock_core = MockCore(mock_scripts, tmp_path, tmp_path)
    monkeypatch.setattr("uvs.main.get_core", lambda: mock_core)

    # Create a mock script with nested structure
    script_dir = tmp_path / "gist-456"
    script_dir.mkdir()

    # Create main.py
    main_file = script_dir / "main.py"
    main_file.write_text(
        '''"""Nested script.

# /// script
# requires-python = ">=3.8"
# dependencies = []
# [tool.uvs]
# description = "Nested script description"
# ///
"""
from .core import core_function
from .utils.helpers import helper_function
from .utils.submodule.deep import deep_function

def main():
    print(core_function())
    print(helper_function())
    print(deep_function())
"""
'''
    )

    # Create core.py
    core_file = script_dir / "core.py"
    core_file.write_text('def core_function(): return "Core function"')

    # Create nested structure
    utils_dir = script_dir / "utils"
    utils_dir.mkdir()
    utils_init = utils_dir / "__init__.py"
    utils_init.touch()

    helpers_file = utils_dir / "helpers.py"
    helpers_file.write_text('def helper_function(): return "Helper function"')

    submodule_dir = utils_dir / "submodule"
    submodule_dir.mkdir()
    submodule_init = submodule_dir / "__init__.py"
    submodule_init.touch()

    deep_dir = submodule_dir / "deep"
    deep_dir.mkdir()
    deep_init = deep_dir / "__init__.py"
    deep_init.touch()

    deep_file = deep_dir / "deep.py"
    deep_file.write_text('def deep_function(): return "Deep function"')

    # Run the package command
    result = runner.invoke(app, ["package", "nested-script", "--output", str(tmp_path / "package")])
    if result.exit_code != 0:
        print("\nSTDOUT:\n", result.stdout)
        print("\nSTDERR:\n", result.stderr)
    assert result.exit_code == 0

    # Verify package structure
    package_dir = tmp_path / "package"
    src_dir = package_dir / "src" / "nested_script"

    # Check all files were copied with correct structure
    assert (src_dir / "main.py").exists()
    assert (src_dir / "core.py").exists()
    assert (src_dir / "utils" / "__init__.py").exists()
    assert (src_dir / "utils" / "helpers.py").exists()
    assert (src_dir / "utils" / "submodule" / "__init__.py").exists()
    assert (src_dir / "utils" / "submodule" / "deep" / "__init__.py").exists()
    assert (src_dir / "utils" / "submodule" / "deep" / "deep.py").exists()


def test_package_command_error_cases(tmp_path, monkeypatch):
    """Test package command error cases."""
    mock_core = MockCore([], tmp_path, tmp_path)
    monkeypatch.setattr("uvs.main.get_core", lambda: mock_core)

    # Test non-existent script
    result = runner.invoke(app, ["package", "non-existent"])
    assert result.exit_code == 1
    assert "Script 'non-existent' not found" in result.stdout

    # Test with invalid output directory
    mock_scripts = [
        MockScript(
            name="test-script",
            gist_id="123",
            entry_file="main.py",
            is_local=False,
        )
    ]
    mock_core = MockCore(mock_scripts, tmp_path, tmp_path)
    monkeypatch.setattr("uvs.main.get_core", lambda: mock_core)

    # Create script directory but no main.py
    script_dir = tmp_path / "gist-123"
    script_dir.mkdir()

    result = runner.invoke(app, ["package", "test-script"])
    assert result.exit_code == 1
    assert "Script file not found" in result.stdout
