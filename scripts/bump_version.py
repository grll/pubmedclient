#!/usr/bin/env python
import re
import sys
import subprocess
from pathlib import Path


def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e}")
        sys.exit(1)


def bump_version(version_type):
    init_file = Path("src/pubmedclient/__init__.py")

    # Read current version
    content = init_file.read_text()
    current_version = re.search(r'__version__ = ["\']([^"\']+)["\']', content).group(1)
    major, minor, patch = map(int, current_version.split("."))

    # Update version based on argument
    if version_type == "major":
        new_version = f"{major + 1}.0.0"
    elif version_type == "minor":
        new_version = f"{major}.{minor + 1}.0"
    elif version_type == "patch":
        new_version = f"{major}.{minor}.{patch + 1}"
    else:
        print("Invalid version type. Use 'major', 'minor', or 'patch'")
        sys.exit(1)

    # Update __init__.py
    new_content = re.sub(
        r'__version__ = ["\']([^"\']+)["\']', f'__version__ = "{new_version}"', content
    )
    init_file.write_text(new_content)

    # Git operations
    run_command("git add src/pubmedclient/__init__.py")
    run_command(f'git commit -m "release {new_version}: version bump commit"')
    run_command("git push")
    run_command(f"git tag v{new_version}")
    run_command("git push --tags")

    # Create GitHub release using gh CLI
    run_command(
        f'gh release create v{new_version} --title "Release {new_version}" --generate-notes'
    )

    print(f"Version bumped from {current_version} to {new_version}")
    print(f"Git operations completed and GitHub release v{new_version} created")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: bump_version.py <major|minor|patch>")
        sys.exit(1)

    bump_version(sys.argv[1])
