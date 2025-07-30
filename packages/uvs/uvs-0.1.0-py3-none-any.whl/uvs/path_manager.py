"""PATH and wrapper management for uvs."""

import os
import platform
from pathlib import Path


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
        if str(self.bin_dir) not in os.environ.get("PATH", ""):
            return False
        return True

    def get_path_instruction(self) -> str:
        """Get instruction for adding bin dir to PATH"""
        if self.is_windows:
            return f"Add {self.bin_dir} to your PATH environment variable"
        else:
            return f'Add this to your shell config: export PATH="{self.bin_dir}:$PATH"'
