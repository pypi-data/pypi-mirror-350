"""Script metadata parsing for uvs."""

import re
import tomllib  # Python 3.11+, use tomli for older versions
from pathlib import Path
from typing import Any


def detect_main_script(gist_dir: Path, explicit_file: str | None = None) -> str:
    """Find the main Python script in a Gist"""
    py_files = [f.name for f in gist_dir.glob("*.py") if not f.name.startswith("test")]

    if not py_files:
        raise ValueError("No Python files found in Gist")

    # 1. Use explicitly specified file if provided
    if explicit_file:
        if explicit_file not in py_files:
            raise ValueError(f"Specified file '{explicit_file}' not found or is a test file")
        return explicit_file

    # 2. Check for main.py
    if "main.py" in py_files:
        return "main.py"

    # 3. Check for script.py
    if "script.py" in py_files:
        return "script.py"

    # 4. Use first .py file alphabetically
    return sorted(py_files)[0]


def parse_script_metadata(script_path: Path) -> dict[str, Any]:
    """Parse metadata from a PEP 723-style block inside a Python script."""
    content = script_path.read_text(encoding="utf-8")
    metadata = {}

    # Look for PEP 723 script metadata block
    pattern = r"# /// script\n(.*?)\n# ///"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        toml_content = match.group(1)
        # Remove leading "# " from each line
        toml_content = "\n".join(line[2:] if line.startswith("# ") else line for line in toml_content.split("\n"))

        try:
            # Parse the TOML content
            parsed = tomllib.loads(toml_content)

            # Extract top-level keys (dependencies and requires-python)
            if "dependencies" in parsed:
                metadata["dependencies"] = parsed["dependencies"]
            if "requires-python" in parsed:
                metadata["requires-python"] = parsed["requires-python"]

            # Extract [tool.uvs] section if present
            if "tool" in parsed and "uvs" in parsed["tool"]:
                metadata["tool"] = {"uvs": parsed["tool"]["uvs"]}

        except tomllib.TOMLDecodeError:
            pass

    return metadata


def get_script_name(script_path: Path, metadata: dict[str, Any]) -> str:
    """Determine the script name from metadata or filename"""
    # Check for custom name in uvs metadata
    if "tool" in metadata and "uvs" in metadata["tool"]:
        custom_name = metadata["tool"]["uvs"].get("name")
        if custom_name:
            return custom_name

    # Use filename without extension
    return script_path.stem


def get_dependencies(metadata: dict[str, Any]) -> list[str]:
    """Extract dependencies from metadata"""
    return metadata.get("dependencies", [])


def get_python_version(metadata: dict[str, Any]) -> str | None:
    """Extract Python version requirement"""
    return metadata.get("requires-python")
