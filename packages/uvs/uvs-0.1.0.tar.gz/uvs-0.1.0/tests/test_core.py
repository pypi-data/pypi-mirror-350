"""Tests for uvs core functionality."""

from datetime import UTC, datetime
from unittest.mock import patch

import pytest

from uvs.core import UVSCore
from uvs.git_utils import parse_gist_url


def test_parse_gist_url_https():
    """Test parsing HTTPS Gist URL."""
    gist_id, clone_url, auth_method = parse_gist_url("https://gist.github.com/user/abc123")
    assert gist_id == "abc123"
    assert clone_url == "https://gist.github.com/abc123.git"
    assert auth_method == "https"


def test_parse_gist_url_ssh():
    """Test parsing SSH Gist URL."""
    gist_id, clone_url, auth_method = parse_gist_url("git@gist.github.com:abc123.git")
    assert gist_id == "abc123"
    assert clone_url == "git@gist.github.com:abc123.git"
    assert auth_method == "ssh"


@pytest.fixture
def temp_uvs_dir(tmp_path):
    """Create a temporary UVS directory for testing."""
    return UVSCore(base_dir=tmp_path)


def test_uvs_core_initialization(temp_uvs_dir):
    """Test UVSCore initialization."""
    assert temp_uvs_dir.scripts_dir.exists()
    assert temp_uvs_dir.bin_dir.exists()
    assert temp_uvs_dir.config_file.exists()
    assert temp_uvs_dir.registry_file.exists()


def test_registry_operations(temp_uvs_dir):
    """Test registry loading and saving."""
    # Test empty registry
    registry = temp_uvs_dir._load_registry()
    assert registry == {}

    # Test saving and loading registry
    test_data = {
        "test-script": {
            "name": "test-script",
            "gist_id": "abc123def4567890abcdef1234567890",
            "entry_file": "main.py",
            "clone_url": "https://gist.github.com/abc123def4567890abcdef1234567890.git",
            "auth_method": "https",
            "installed_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
    }
    temp_uvs_dir._save_registry(test_data)
    loaded_registry = temp_uvs_dir._load_registry()
    assert loaded_registry == test_data


def test_list_scripts_empty(temp_uvs_dir):
    """Test listing scripts when none are installed."""
    scripts = temp_uvs_dir.list_scripts()
    assert len(scripts) == 0


def test_list_scripts(temp_uvs_dir):
    """Test listing installed scripts."""
    # Add test data to registry
    test_data = {
        "test-script": {
            "name": "test-script",
            "gist_id": "abc123def4567890abcdef1234567890",
            "entry_file": "main.py",
            "clone_url": "https://gist.github.com/abc123def4567890abcdef1234567890.git",
            "auth_method": "https",
            "installed_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
    }
    temp_uvs_dir._save_registry(test_data)

    # Test listing
    scripts = temp_uvs_dir.list_scripts()
    assert len(scripts) == 1
    script = scripts[0]
    assert script.name == "test-script"
    assert script.gist_id == "abc123def4567890abcdef1234567890"
    assert script.entry_file == "main.py"


def test_remove_script_not_installed(temp_uvs_dir):
    """Test removing a non-existent script."""
    with pytest.raises(ValueError, match="Script test-script is not installed"):
        temp_uvs_dir.remove_script("test-script")


def test_update_script_not_installed(temp_uvs_dir):
    """Test updating a non-existent script."""
    with pytest.raises(ValueError, match="Script test-script is not installed"):
        temp_uvs_dir.update_script("test-script")


def test_update_all_scripts_empty(temp_uvs_dir):
    """Test updating all scripts when none are installed."""
    updated = temp_uvs_dir.update_all_scripts()
    assert len(updated) == 0


@patch("uvs.core.clone_gist")
@patch("uvs.core.detect_main_script")
@patch("uvs.core.parse_script_metadata")
@patch("uvs.core.get_script_name")
def test_add_script(mock_get_name, mock_parse_metadata, mock_detect_script, mock_clone, temp_uvs_dir):
    """Test adding a script."""
    # Setup mocks
    mock_detect_script.return_value = "main.py"
    mock_parse_metadata.return_value = {}
    mock_get_name.return_value = "test-script"
    mock_clone.return_value = True

    # Do not pre-create the Gist directory; let add_script handle it
    # Test adding script
    script = temp_uvs_dir.add_script("abc123def4567890abcdef1234567890")
    assert script.name == "test-script"
    assert script.gist_id == "abc123def4567890abcdef1234567890"
    assert script.entry_file == "main.py"

    # Verify registry
    registry = temp_uvs_dir._load_registry()
    assert "test-script" in registry
    assert registry["test-script"]["gist_id"] == "abc123def4567890abcdef1234567890"


@patch("uvs.core.update_gist")
def test_update_script(mock_update, temp_uvs_dir):
    """Test updating a script."""
    # Setup test data
    test_data = {
        "test-script": {
            "name": "test-script",
            "gist_id": "abc123def4567890abcdef1234567890",
            "entry_file": "main.py",
            "clone_url": "https://gist.github.com/abc123def4567890abcdef1234567890.git",
            "auth_method": "https",
            "installed_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
    }
    temp_uvs_dir._save_registry(test_data)

    # Create test Gist directory
    gist_dir = temp_uvs_dir.scripts_dir / "gist-abc123def4567890abcdef1234567890"
    gist_dir.mkdir()

    # Setup mock
    mock_update.return_value = True

    # Test updating
    assert temp_uvs_dir.update_script("test-script")

    # Verify registry was updated
    registry = temp_uvs_dir._load_registry()
    assert registry["test-script"]["updated_at"] != test_data["test-script"]["updated_at"]


@patch("uvs.core.clone_gist")
@patch("uvs.core.detect_main_script")
@patch("uvs.core.parse_script_metadata")
@patch("uvs.core.get_script_name")
def test_add_script_generic_name_error(
    mock_get_name, mock_parse_metadata, mock_detect_script, mock_clone, temp_uvs_dir
):
    """Test error when entrypoint is main.py/script.py and no custom name is provided."""
    for entry_file, script_name in [("main.py", "main"), ("script.py", "script")]:
        mock_detect_script.return_value = entry_file
        mock_parse_metadata.return_value = {}
        mock_get_name.return_value = script_name
        mock_clone.return_value = True
        with pytest.raises(ValueError, match=f"Refusing to install with generic name '{script_name}'"):
            temp_uvs_dir.add_script("abc123def4567890abcdef1234567890")


@patch("uvs.core.clone_gist")
@patch("uvs.core.detect_main_script")
@patch("uvs.core.parse_script_metadata")
@patch("uvs.core.get_script_name")
def test_add_script_with_custom_name_cli(
    mock_get_name, mock_parse_metadata, mock_detect_script, mock_clone, temp_uvs_dir
):
    """Test success when custom name is provided via CLI, even if entrypoint is main.py/script.py."""
    mock_detect_script.return_value = "main.py"
    mock_parse_metadata.return_value = {}
    mock_get_name.return_value = "main"
    mock_clone.return_value = True
    script = temp_uvs_dir.add_script("abc123def4567890abcdef1234567890", name="mycustom")
    assert script.name == "mycustom"
    assert script.entry_file == "main.py"


@patch("uvs.core.detect_main_script")
@patch("uvs.core.parse_script_metadata")
@patch("uvs.core.get_script_name")
def test_copy_script_file(mock_get_name, mock_parse_metadata, mock_detect_script, temp_uvs_dir, tmp_path):
    """Test copying a single script file."""
    # Create a test script file
    test_script = tmp_path / "test.py"
    test_script.write_text("print('test')")

    # Setup mocks
    mock_parse_metadata.return_value = {}
    mock_get_name.return_value = "test-script"

    # Test copying script
    script = temp_uvs_dir.copy_script(test_script)
    assert script.name == "test-script"
    assert script.is_local
    assert script.auth_method == "local"
    assert script.clone_url == str(test_script)

    # Verify registry
    registry = temp_uvs_dir._load_registry()
    assert "test-script" in registry
    assert registry["test-script"]["is_local"]
    assert registry["test-script"]["auth_method"] == "local"


@patch("uvs.core.detect_main_script")
@patch("uvs.core.parse_script_metadata")
@patch("uvs.core.get_script_name")
def test_copy_script_directory(mock_get_name, mock_parse_metadata, mock_detect_script, temp_uvs_dir, tmp_path):
    """Test copying a script directory."""
    # Create a test script directory
    test_dir = tmp_path / "test-dir"
    test_dir.mkdir()
    (test_dir / "main.py").write_text("print('test')")
    (test_dir / "utils.py").write_text("print('utils')")

    # Setup mocks
    mock_detect_script.return_value = "main.py"
    mock_parse_metadata.return_value = {}
    mock_get_name.return_value = "test-script"

    # Test copying directory
    script = temp_uvs_dir.copy_script(test_dir)
    assert script.name == "test-script"
    assert script.is_local
    assert script.auth_method == "local"
    assert script.clone_url == str(test_dir)

    # Verify registry
    registry = temp_uvs_dir._load_registry()
    assert "test-script" in registry
    assert registry["test-script"]["is_local"]
    assert registry["test-script"]["auth_method"] == "local"


def test_copy_script_nonexistent(temp_uvs_dir):
    """Test copying a nonexistent script."""
    with pytest.raises(ValueError, match="Path does not exist"):
        temp_uvs_dir.copy_script("/nonexistent/path")


@patch("uvs.core.detect_main_script")
@patch("uvs.core.parse_script_metadata")
@patch("uvs.core.get_script_name")
def test_copy_script_generic_name_error(mock_get_name, mock_parse_metadata, mock_detect_script, temp_uvs_dir, tmp_path):
    """Test error when copying a script with generic name."""
    # Create a test script file
    test_script = tmp_path / "main.py"
    test_script.write_text("print('test')")

    # Setup mocks
    mock_parse_metadata.return_value = {}
    mock_get_name.return_value = "main"

    # Test copying script with generic name
    with pytest.raises(ValueError, match="Refusing to install with generic name 'main'"):
        temp_uvs_dir.copy_script(test_script)
