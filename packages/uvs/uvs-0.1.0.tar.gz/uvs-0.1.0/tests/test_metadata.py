"""Tests for uvs metadata parsing."""

from pathlib import Path

import pytest

from uvs.metadata import (
    detect_main_script,
    get_dependencies,
    get_python_version,
    get_script_name,
    parse_script_metadata,
)


@pytest.fixture
def temp_gist_dir(tmp_path):
    """Create a temporary Gist directory with test files."""
    gist_dir = tmp_path / "gist-abc123"
    gist_dir.mkdir()

    # Create test files
    (gist_dir / "main.py").write_text("print('main')")
    (gist_dir / "utils.py").write_text("print('utils')")
    (gist_dir / "test_main.py").write_text("print('test')")

    return gist_dir


def test_detect_main_script_default(temp_gist_dir):
    """Test main script detection with default behavior."""
    script = detect_main_script(temp_gist_dir)
    assert script == "main.py"


def test_detect_main_script_explicit(temp_gist_dir):
    """Test main script detection with explicit file."""
    script = detect_main_script(temp_gist_dir, "utils.py")
    assert script == "utils.py"


def test_detect_main_script_no_files(tmp_path):
    """Test main script detection with no Python files."""
    with pytest.raises(ValueError, match="No Python files found in Gist"):
        detect_main_script(tmp_path)


def test_parse_script_metadata(tmp_path):
    """Test script metadata parsing."""
    content = """#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["requests", "click>=8.0"]
# ///

# [tool.uvs]
# name = "my-tool"
"""
    script_path = tmp_path / "test.py"
    script_path.write_text(content)

    try:
        metadata = parse_script_metadata(script_path)
        assert metadata["requires-python"] == ">=3.8"
        assert metadata["dependencies"] == ["requests", "click>=8.0"]
    finally:
        if script_path.exists():
            script_path.unlink()


def test_get_script_name():
    """Test script name resolution."""
    script_path = Path("test.py")
    metadata = {"tool": {"uvs": {"name": "custom-name"}}}

    # Test custom name
    assert get_script_name(script_path, metadata) == "custom-name"

    # Test default name
    assert get_script_name(script_path, {}) == "test"


def test_get_dependencies():
    """Test dependency extraction."""
    metadata = {"dependencies": ["requests", "click>=8.0"]}
    assert get_dependencies(metadata) == ["requests", "click>=8.0"]
    assert get_dependencies({}) == []


def test_get_python_version():
    """Test Python version requirement extraction."""
    metadata = {"requires-python": ">=3.8"}
    assert get_python_version(metadata) == ">=3.8"
    assert get_python_version({}) is None


def test_parse_script_metadata_tool_uvs(tmp_path):
    """Test parsing [tool.uvs] section in comments."""
    content = """#!/usr/bin/env python3
# /// script
# [tool.uvs]
# name = "custom-name"
# version = "1.0.0"
# ///

print("Hello, world!")
"""
    script_path = tmp_path / "test.py"
    script_path.write_text(content)

    try:
        metadata = parse_script_metadata(script_path)
        assert "tool" in metadata
        assert "uvs" in metadata["tool"]
        assert metadata["tool"]["uvs"]["name"] == "custom-name"
        assert metadata["tool"]["uvs"]["version"] == "1.0.0"
    finally:
        if script_path.exists():
            script_path.unlink()


def test_parse_script_metadata_both_sections(tmp_path):
    """Test parsing both PEP 723 and [tool.uvs] sections."""
    content = """#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["requests"]
# [tool.uvs]
# name = "custom-name"
# version = "1.0.0"
# ///

print("Hello, world!")
"""
    script_path = tmp_path / "test.py"
    script_path.write_text(content)

    try:
        metadata = parse_script_metadata(script_path)
        assert "requires-python" in metadata
        assert "dependencies" in metadata
        assert "tool" in metadata
        assert "uvs" in metadata["tool"]
        assert metadata["tool"]["uvs"]["name"] == "custom-name"
        assert metadata["tool"]["uvs"]["version"] == "1.0.0"
    finally:
        if script_path.exists():
            script_path.unlink()
