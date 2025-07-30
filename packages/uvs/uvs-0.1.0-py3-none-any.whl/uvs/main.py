"""Main CLI entry point for uvs."""

import os
import platform
import re
import shutil
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import tomli_w
import typer
from rich.console import Console
from rich.table import Table

from .config import ConfigManager
from .core import UVSCore
from .metadata import parse_script_metadata

app = typer.Typer(help="Manage Python scripts from GitHub Gists")
console = Console()

# Create self subcommand group
self_app = typer.Typer(help="Manage uvs itself")
app.add_typer(self_app, name="self")


def get_core() -> UVSCore:
    """Get UVSCore instance"""
    return UVSCore()


def get_config() -> ConfigManager:
    """Get ConfigManager instance"""
    return ConfigManager(Path.home() / ".uvs" / "config.json")


@app.command()
def add(
    url_or_id: str = typer.Argument(..., help="Gist URL or ID"),
    file: str | None = typer.Option(None, "--file", help="Specific file to use as entrypoint"),
    name: str | None = typer.Option(None, "--name", help="Override script name"),
):
    """Add a script from a Gist"""
    try:
        core = get_core()
        script = core.add_script(url_or_id, file, name)
        console.print(f"[green]Successfully installed script: {script.name}[/green]")

        # Check if bin directory is in PATH
        if not core.path_manager.ensure_bin_in_path():
            console.print("[yellow]Warning: Script installed but bin directory not in PATH[/yellow]")
            console.print(f"Please run: {core.path_manager.get_path_instruction()}")
    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1) from e


@app.command()
def remove(name: str = typer.Argument(..., help="Script name to remove")):
    """Remove an installed script"""
    try:
        core = get_core()
        if core.remove_script(name):
            console.print(f"[green]Successfully removed script: {name}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1) from e


@app.command()
def copy(
    path: str = typer.Argument(..., help="Path to local script or directory"),
    file: str | None = typer.Option(None, "--file", help="Specific file to use as entrypoint"),
    name: str | None = typer.Option(None, "--name", help="Override script name"),
):
    """Add a script from a local path"""
    try:
        core = get_core()
        script = core.copy_script(path, file, name)
        console.print(f"[green]Successfully installed local script: {script.name}[/green]")

        # Check if bin directory is in PATH
        if not core.path_manager.ensure_bin_in_path():
            console.print("[yellow]Warning: Script installed but bin directory not in PATH[/yellow]")
            console.print(f"Please run: {core.path_manager.get_path_instruction()}")
    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1) from e


@app.command()
def list():
    """List all installed scripts"""
    try:
        core = get_core()
        scripts = core.list_scripts()

        if not scripts:
            console.print("[yellow]No scripts installed[/yellow]")
            return

        # Split scripts into local and gist
        local_scripts = [s for s in scripts if s.is_local]
        gist_scripts = [s for s in scripts if not s.is_local]

        # Display Gist scripts
        if gist_scripts:
            table = Table(title="Gist Scripts")
            table.add_column("Name", style="cyan")
            table.add_column("Gist ID", style="yellow")
            table.add_column("Entry File", style="blue")
            table.add_column("Updated", style="green")

            for script in gist_scripts:
                table.add_row(
                    script.name,
                    script.gist_id,
                    script.entry_file,
                    script.updated_at or "unknown",
                )
            console.print(table)

        # Display local scripts
        if local_scripts:
            table = Table(title="Local Scripts")
            table.add_column("Name", style="cyan")
            table.add_column("Source Path", style="yellow")
            table.add_column("Entry File", style="blue")
            table.add_column("Updated", style="green")

            for script in local_scripts:
                table.add_row(
                    script.name,
                    script.clone_url,  # Original path
                    script.entry_file,
                    script.updated_at or "unknown",
                )
            console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1) from e


@app.command()
def update(
    name: str | None = typer.Argument(None, help="Script name to update, or all if not specified"),
):
    """Update scripts to latest version"""
    try:
        core = get_core()
        if name:
            if core.update_script(name):
                console.print(f"[green]Successfully updated script: {name}[/green]")
            else:
                console.print(f"[yellow]No updates available for script: {name}[/yellow]")
        else:
            updated = core.update_all_scripts()
            if updated:
                console.print(f"[green]Successfully updated scripts: {', '.join(updated)}[/green]")
            else:
                console.print("[yellow]No updates available[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1) from e


@app.command()
def config(
    action: str = typer.Argument(..., help="Action to perform (get/set/unset)"),
    key: str | None = typer.Argument(None, help="Configuration key"),
    value: str | None = typer.Argument(None, help="Configuration value"),
):
    """Manage configuration"""
    try:
        config = get_config()

        if action == "get":
            if not key:
                raise ValueError("Key is required for get action")
            value = config.get(key)
            if value is None:
                console.print(f"[yellow]No value set for {key}[/yellow]")
            else:
                console.print(f"{key} = {value}")

        elif action == "set":
            if not key or not value:
                raise ValueError("Key and value are required for set action")
            config.set(key, value)
            console.print(f"[green]Set {key} = {value}[/green]")

        elif action == "unset":
            if not key:
                raise ValueError("Key is required for unset action")
            config.set(key, None)
            console.print(f"[green]Unset {key}[/green]")

        else:
            raise ValueError(f"Unknown action: {action}")

    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1) from e


@self_app.command(name="ensurepath")
def self_ensure_path():
    """Ensure the uvs bin directory is in your PATH permanently."""
    core = get_core()
    bin_dir = str(core.bin_dir)
    shell = os.environ.get("SHELL", "")
    home = str(Path.home())
    export_line = f'export PATH="{bin_dir}:$PATH"'
    shell_config = None
    shell_name = shell.split("/")[-1]

    if platform.system() == "Windows":
        msg = (
            f"[yellow]Automatic PATH modification is not supported on Windows.\n"
            f"{core.path_manager.get_path_instruction()}[/yellow]"
        )
        console.print(msg)
        return

    # Determine shell config file
    if shell_name == "zsh":
        shell_config = os.path.join(home, ".zshrc")
    elif shell_name == "bash":
        shell_config = os.path.join(home, ".bashrc")
    elif shell_name == "fish":
        shell_config = os.path.join(home, ".config/fish/config.fish")
        export_line = f"set -gx PATH {bin_dir} $PATH"
    else:
        # Default to .profile
        shell_config = os.path.join(home, ".profile")

    # Check if already present
    if shell_config and os.path.exists(shell_config):
        with open(shell_config) as f:
            contents = f.read()
        if export_line in contents:
            console.print(f"[green]uvs bin directory is already in your PATH via {shell_config}[/green]")
            return

    # Append export line
    if shell_config:
        with open(shell_config, "a") as f:
            f.write(f"\n# Added by uvs\n{export_line}\n")
        console.print(f"[green]Added uvs bin directory to PATH in {shell_config}[/green]")
        console.print(f"[yellow]Please restart your shell or run:[/yellow] [bold]{export_line}[/bold]")
    else:
        msg = (
            "[red]Could not determine your shell config file. "
            f"Please add the following to your shell config manually:[/red]\n"
            f"[bold]{export_line}[/bold]"
        )
        console.print(msg)


@self_app.command(name="version")
def self_version():
    """Show the version of uvs."""
    try:
        ver = version("uvs")
        console.print(f"[green]uvs version {ver}[/green]")
    except PackageNotFoundError:
        console.print("[yellow]uvs version dev[/yellow]")


@self_app.command(name="delete")
def self_delete():
    """Remove uvs and all installed scripts from your system."""
    try:
        core = get_core()
        bin_dir = str(core.bin_dir)
        base_dir = str(core.base_dir)
        shell = os.environ.get("SHELL", "")
        home = str(Path.home())
        export_line = f'export PATH="{bin_dir}:$PATH"'
        shell_config = None
        shell_name = shell.split("/")[-1]

        # Confirm deletion
        console.print("[red]Warning: This will remove all installed scripts and uvs configuration.[/red]")
        if not typer.confirm("Are you sure you want to continue?"):
            return

        # Remove from PATH
        if platform.system() != "Windows":
            if shell_name == "zsh":
                shell_config = os.path.join(home, ".zshrc")
            elif shell_name == "bash":
                shell_config = os.path.join(home, ".bashrc")
            elif shell_name == "fish":
                shell_config = os.path.join(home, ".config/fish/config.fish")
                export_line = f"set -gx PATH {bin_dir} $PATH"
            else:
                shell_config = os.path.join(home, ".profile")

            if shell_config and os.path.exists(shell_config):
                with open(shell_config) as f:
                    contents = f.read()
                if export_line in contents:
                    new_contents = contents.replace(f"\n# Added by uvs\n{export_line}\n", "")
                    with open(shell_config, "w") as f:
                        f.write(new_contents)
                    console.print(f"[green]Removed uvs bin directory from PATH in {shell_config}[/green]")

        # Remove uvs directory
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
            console.print(f"[green]Removed uvs directory: {base_dir}[/green]")
        else:
            console.print(f"[yellow]uvs directory not found: {base_dir}[/yellow]")

        console.print("[green]uvs has been completely removed from your system.[/green]")
        console.print("[yellow]You may need to restart your shell for PATH changes to take effect.[/yellow]")

    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1) from e


@app.command()
def package(  # noqa: PLR0912, PLR0915
    name: str = typer.Argument(..., help="Script name to package"),
    output_dir: str | None = typer.Option(None, "--output", "-o", help="Output directory for package files"),
    keep_project: bool = typer.Option(False, "--keep-project", help="Keep the generated project folder structure"),
):
    """Create a Python package from an installed script."""
    try:
        core = get_core()
        scripts = core.list_scripts()
        script = next((s for s in scripts if s.name == name), None)

        if not script:
            raise ValueError(f"Script '{name}' not found")

        script_name_normalized = re.sub(r"[-_.]+", "_", script.name).lower()

        # Get script directory and entry file
        if script.is_local:
            script_dir = core.scripts_dir / f"local-{script.name}"
        else:
            script_dir = core.scripts_dir / f"gist-{script.gist_id}"

        entry_file = script_dir / script.entry_file
        if not entry_file.exists():
            raise ValueError(f"Script file not found: {entry_file}")

        # Parse metadata
        metadata = parse_script_metadata(entry_file)

        # Create output directory
        if output_dir:
            output_path = Path(output_dir)
        elif keep_project:
            output_path = Path.cwd() / f"{script.name}-package"
        else:
            output_path = Path("/tmp") / f"{script.name}-package"

        # Create the output directory and its parents
        output_path.mkdir(parents=True, exist_ok=True)

        # Create pyproject.toml
        pyproject = {
            "build-system": {
                "requires": ["hatchling", "hatch"],
                "build-backend": "hatchling.build",
            },
            "project": {
                "name": script.name,
                "version": "0.0.0-dev",  # Default version
            },
            "tool": {
                "hatch": {
                    "build": {
                        "packages": ["src"],
                    },
                },
            },
        }

        # Add dependencies if specified
        if metadata.get("dependencies"):
            pyproject["project"]["dependencies"] = metadata["dependencies"]

        # Add requires-python if specified
        if metadata.get("requires-python"):
            pyproject["project"]["requires-python"] = metadata["requires-python"]

        # Add other metadata from [tool.uvs] section
        if "tool" in metadata and "uvs" in metadata["tool"]:
            for key, value in metadata["tool"]["uvs"].items():
                if key not in ["dependencies", "requires-python"]:
                    pyproject["project"][key] = value

        # Write pyproject.toml
        with open(output_path / "pyproject.toml", "wb") as f:
            tomli_w.dump(pyproject, f)

        # Use original script name for directory, but underscores for import
        src_dir = output_path / "src" / script_name_normalized
        src_dir.mkdir(parents=True, exist_ok=True)

        # Copy all Python files from the script directory
        for py_file in script_dir.glob("**/*.py"):
            # Calculate relative path from script_dir
            rel_path = py_file.relative_to(script_dir)
            # Replace hyphens with underscores in the file name for import safety
            safe_rel_path = rel_path.with_name(rel_path.name.replace("-", "_"))
            target_path = src_dir / safe_rel_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(py_file, target_path)

            # Create __init__.py in each directory if it doesn't exist
            init_file = target_path.parent / "__init__.py"
            if not init_file.exists():
                init_file.touch()

        # Ensure root __init__.py exists
        root_init = src_dir / "__init__.py"
        if not root_init.exists():
            root_init.touch()

        # Create entry point script
        entry_point = output_path / "src" / f"{script_name_normalized}_cli.py"
        entry_file_stem = Path(script.entry_file).stem
        entry_file_stem_safe = entry_file_stem.replace("-", "_")
        entry_point.write_text(f'''"""Command-line entry point for {script_name_normalized}."""

from {script_name_normalized}.{entry_file_stem_safe} import main

if __name__ == "__main__":
    main()
''')

        # Add entry point to pyproject.toml
        pyproject["project"]["scripts"] = {script.name: f"{script_name_normalized}_cli:main"}

        # Update pyproject.toml with entry point
        with open(output_path / "pyproject.toml", "wb") as f:
            tomli_w.dump(pyproject, f)

        # Create minimal README
        readme_content = f"""# {script.name}

A Python script packaged using uvs.

## Installation

```bash
uv tool install .
```

## Usage

```bash
{script.name}
```
"""
        with open(output_path / "README.md", "w") as f:
            f.write(readme_content)

        console.print(f"[green]Created package in: {output_path}[/green]")
        console.print("\nTo build and install the package:")
        console.print(f"cd {output_path}")
        console.print("uv tool install .")

        # Automatically build the package
        import subprocess

        try:
            subprocess.run(["uv", "pip", "install", "hatch"], cwd=output_path, check=True)
            subprocess.run(["uv", "run", "hatch", "build"], cwd=output_path, check=True)
            dist_dir = output_path / "dist"
            if not output_dir:
                # If no output directory was specified, copy the dist folder to the current directory
                if not keep_project:
                    current_dist_dir = Path.cwd() / f"{script.name}-dist"
                    if current_dist_dir.exists():
                        shutil.rmtree(current_dist_dir)
                    shutil.copytree(dist_dir, current_dist_dir)
                    console.print(f"[green]Package built successfully in: {current_dist_dir}[/green]")
                else:
                    console.print(f"[green]Package built successfully in: {dist_dir}[/green]")
                # Clean up the temporary directory only if --keep-project is not set
                if not keep_project:
                    shutil.rmtree(output_path)
            else:
                console.print(f"[green]Package built successfully in: {dist_dir}[/green]")
                # Do NOT delete the output_path if the user specified --output
                pass
        except Exception as build_exc:
            console.print(f"[red]Package build failed: {build_exc}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
