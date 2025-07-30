"""Git utilities for uvs."""

import subprocess
from pathlib import Path

GIST_ID_LENGTH = 32
SSH_PARTS_COUNT = 2
HTTPS_PARTS_MIN = 5


def parse_gist_url(url_or_id: str) -> tuple[str, str, str]:
    """Parse a Gist URL or ID into clone URL and auth method"""
    # If it's just an ID, construct HTTPS URL
    if len(url_or_id) == GIST_ID_LENGTH and url_or_id.isalnum():
        return url_or_id, f"https://gist.github.com/{url_or_id}.git", "https"

    # Handle SSH URLs
    if url_or_id.startswith("git@"):
        parts = url_or_id.split(":")
        if len(parts) != SSH_PARTS_COUNT:
            raise ValueError("Invalid SSH URL format")
        gist_id = parts[1].replace(".git", "")
        return gist_id, url_or_id, "ssh"

    # Handle HTTPS URLs
    if url_or_id.startswith("https://"):
        parts = url_or_id.split("/")
        if len(parts) < HTTPS_PARTS_MIN:
            raise ValueError("Invalid HTTPS URL format")
        gist_id = parts[-1].replace(".git", "")
        return gist_id, f"https://gist.github.com/{gist_id}.git", "https"

    raise ValueError("Invalid Gist URL or ID format")


def check_ssh_available() -> bool:
    """Check if SSH is available for authentication"""
    try:
        subprocess.run(["ssh", "-T", "git@gist.github.com"], capture_output=True, check=False)
        return True
    except subprocess.CalledProcessError:
        return False


def clone_gist(clone_url: str, destination: Path) -> bool:
    """Clone a Gist to the specified directory"""
    try:
        subprocess.run(
            ["git", "clone", clone_url, str(destination)],
            capture_output=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone Gist: {e.stderr}") from e


def update_gist(gist_dir: Path) -> bool:
    """Update a cloned Gist (git pull)"""
    try:
        subprocess.run(["git", "pull"], cwd=gist_dir, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to update Gist: {e.stderr}") from e
