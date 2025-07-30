"""Core functionality for uvs."""

import json
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .git_utils import clone_gist, parse_gist_url, update_gist
from .metadata import detect_main_script, get_script_name, parse_script_metadata
from .path_manager import PathManager


@dataclass
class InstalledScript:
    name: str
    gist_id: str
    entry_file: str
    clone_url: str
    auth_method: str
    version: str | None = None
    installed_at: str | None = None
    updated_at: str | None = None
    is_local: bool = False  # Track if script is from local path


class UVSCore:
    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or Path.home() / ".uvs"
        self.scripts_dir = self.base_dir / "scripts"
        self.bin_dir = self.base_dir / "bin"
        self.config_file = self.base_dir / "config.json"
        self.registry_file = self.base_dir / "registry.json"

        # Ensure directories exist
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        self.bin_dir.mkdir(parents=True, exist_ok=True)

        # Initialize empty config file if it doesn't exist
        if not self.config_file.exists():
            with open(self.config_file, "w") as f:
                json.dump({}, f)
        # Initialize empty registry file if it doesn't exist
        if not self.registry_file.exists():
            with open(self.registry_file, "w") as f:
                json.dump({}, f)

        # Initialize path manager
        self.path_manager = PathManager(self.bin_dir)

    def _load_registry(self) -> dict[str, dict[str, Any]]:
        """Load the scripts registry"""
        if not self.registry_file.exists():
            return {}

        try:
            with open(self.registry_file) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_registry(self, registry: dict[str, dict[str, Any]]):
        """Save the scripts registry"""
        with open(self.registry_file, "w") as f:
            json.dump(registry, f, indent=2)

    def add_script(
        self,
        url_or_id: str,
        explicit_file: str | None = None,
        name: str | None = None,
    ) -> InstalledScript:
        """Add a script from a Gist"""
        # Parse URL to get clone URL and auth method
        gist_id, clone_url, auth_method = parse_gist_url(url_or_id)

        # Create Gist directory
        gist_dir = self.scripts_dir / f"gist-{gist_id}"
        if gist_dir.exists():
            raise ValueError(f"Gist {gist_id} is already installed")

        # Clone the Gist
        clone_gist(clone_url, gist_dir)

        # Detect main script file
        entry_file = detect_main_script(gist_dir, explicit_file)
        script_path = gist_dir / entry_file

        # Parse metadata for script name
        metadata = parse_script_metadata(script_path)
        # Determine script name: CLI > metadata > filename
        if name:
            script_name = name
            custom_name_used = True
        else:
            script_name = get_script_name(script_path, metadata)
            # Check if custom name is present in metadata
            custom_name_used = "tool" in metadata and "uvs" in metadata["tool"] and metadata["tool"]["uvs"].get("name")
        # ENFORCE: If entry_file is main.py or script.py and name is main or script and no custom name, error
        if entry_file in {"main.py", "script.py"} and script_name in {"main", "script"} and not custom_name_used:
            raise ValueError(
                f"Refusing to install with generic name '{script_name}'. "
                f"Please specify a custom name in [tool.uvs] or with --name."
            )

        # Create wrapper script
        self.path_manager.create_wrapper_script(script_name, gist_dir, entry_file)

        # Create script record
        now = datetime.now(UTC).isoformat()
        script = InstalledScript(
            name=script_name,
            gist_id=gist_id,
            entry_file=entry_file,
            clone_url=clone_url,
            auth_method=auth_method,
            installed_at=now,
            updated_at=now,
        )

        # Update registry
        registry = self._load_registry()
        registry[script_name] = {
            "name": script.name,
            "gist_id": script.gist_id,
            "entry_file": script.entry_file,
            "clone_url": script.clone_url,
            "auth_method": script.auth_method,
            "installed_at": script.installed_at,
            "updated_at": script.updated_at,
        }
        self._save_registry(registry)

        return script

    def remove_script(self, name: str) -> bool:
        """Remove an installed script"""
        registry = self._load_registry()

        if name not in registry:
            raise ValueError(f"Script {name} is not installed")

        script_info = registry[name]

        # Handle both local and gist scripts
        if script_info.get("is_local", False):
            script_dir = self.scripts_dir / f"local-{name}"
        else:
            script_dir = self.scripts_dir / f"gist-{script_info['gist_id']}"

        # Remove wrapper script
        self.path_manager.remove_wrapper_script(name)

        # Remove script directory
        if script_dir.exists():
            shutil.rmtree(script_dir)

        # Update registry
        del registry[name]
        self._save_registry(registry)

        return True

    def list_scripts(self) -> list[InstalledScript]:
        """List all installed scripts"""
        registry = self._load_registry()
        return [
            InstalledScript(
                name=info["name"],
                gist_id=info["gist_id"],
                entry_file=info["entry_file"],
                clone_url=info["clone_url"],
                auth_method=info["auth_method"],
                installed_at=info.get("installed_at"),
                updated_at=info.get("updated_at"),
                is_local=info.get("is_local", False),  # Load is_local flag, default to False for backward compatibility
            )
            for info in registry.values()
        ]

    def update_script(self, name: str) -> bool:
        """Update a specific script"""
        registry = self._load_registry()

        if name not in registry:
            raise ValueError(f"Script {name} is not installed")

        script_info = registry[name]
        gist_dir = self.scripts_dir / f"gist-{script_info['gist_id']}"

        if not gist_dir.exists():
            raise ValueError(f"Gist directory for {name} not found")

        # Update Gist
        if not update_gist(gist_dir):
            return False

        # Update registry
        now = datetime.now(UTC).isoformat()
        script_info["updated_at"] = now
        self._save_registry(registry)

        return True

    def update_all_scripts(self) -> list[str]:
        """Update all scripts"""
        registry = self._load_registry()
        updated = []
        failed = []

        for name in registry:
            try:
                if self.update_script(name):
                    updated.append(name)
                else:
                    failed.append(name)
            except Exception:
                failed.append(name)

        return updated

    def copy_script(
        self,
        script_path: Path,
        explicit_file: str | None = None,
        name: str | None = None,
    ) -> InstalledScript:
        """Add a script from a local path"""
        script_path = Path(script_path)
        if not script_path.exists():
            raise ValueError(f"Path does not exist: {script_path}")

        # Store original path before any modifications
        original_path = script_path.absolute()  # Convert to absolute path

        # If path is a directory, use detect_main_script logic
        if script_path.is_dir():
            entry_file = detect_main_script(script_path, explicit_file)
            script_path = script_path / entry_file
        else:
            entry_file = script_path.name

        # Parse metadata for script name
        metadata = parse_script_metadata(script_path)
        # Determine script name: CLI > metadata > filename
        if name:
            script_name = name
            custom_name_used = True
        else:
            script_name = get_script_name(script_path, metadata)
            # Check if custom name is present in metadata
            custom_name_used = "tool" in metadata and "uvs" in metadata["tool"] and metadata["tool"]["uvs"].get("name")

        # ENFORCE: If entry_file is main.py or script.py and name is main or script and no custom name, error
        if entry_file in {"main.py", "script.py"} and script_name in {"main", "script"} and not custom_name_used:
            raise ValueError(
                f"Refusing to install with generic name '{script_name}'. "
                f"Please specify a custom name in [tool.uvs] or with --name."
            )

        # Create a unique directory for the script
        script_dir = self.scripts_dir / f"local-{script_name}"
        if script_dir.exists():
            raise ValueError(f"Script {script_name} is already installed")

        # Copy the script or directory
        if original_path.is_dir():
            shutil.copytree(original_path, script_dir)
        else:
            script_dir.mkdir(parents=True)
            shutil.copy2(script_path, script_dir / entry_file)

        # Create wrapper script
        self.path_manager.create_wrapper_script(script_name, script_dir, entry_file)

        # Create script record
        now = datetime.now(UTC).isoformat()
        script = InstalledScript(
            name=script_name,
            gist_id=f"local-{script_name}",  # Use local- prefix for local scripts
            entry_file=entry_file,
            clone_url=str(original_path.absolute()),  # Ensure we store absolute path
            auth_method="local",
            installed_at=now,
            updated_at=now,
            is_local=True,  # Mark as local script
        )

        # Update registry
        registry = self._load_registry()
        registry[script_name] = {
            "name": script.name,
            "gist_id": script.gist_id,
            "entry_file": script.entry_file,
            "clone_url": script.clone_url,
            "auth_method": script.auth_method,
            "installed_at": script.installed_at,
            "updated_at": script.updated_at,
            "is_local": script.is_local,  # Store is_local flag
        }
        self._save_registry(registry)

        return script
