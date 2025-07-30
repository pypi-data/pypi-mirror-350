#!/usr/bin/env python
"""
Version bumping utility for django-jqgrid
"""
import re
import sys
import os
from pathlib import Path

def get_current_version():
    """Get current version from setup.py"""
    setup_path = Path(__file__).parent / 'setup.py'
    with open(setup_path, 'r') as f:
        content = f.read()
    
    match = re.search(r"version='([^']+)'", content)
    if match:
        return match.group(1)
    return None

def update_version(old_version, new_version):
    """Update version in all relevant files"""
    files_to_update = [
        'setup.py',
        '__init__.py',
        'pyproject.toml',
    ]
    
    updated_files = []
    
    for filename in files_to_update:
        filepath = Path(__file__).parent / filename
        if not filepath.exists():
            continue
            
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Different patterns for different files
        if filename == 'setup.py':
            new_content = re.sub(
                r"version='[^']+'",
                f"version='{new_version}'",
                content
            )
        elif filename == '__init__.py':
            new_content = re.sub(
                r'__version__\s*=\s*["\'][^"\']+["\']',
                f'__version__ = "{new_version}"',
                content
            )
        elif filename == 'pyproject.toml':
            new_content = re.sub(
                r'version\s*=\s*["\'][^"\']+["\']',
                f'version = "{new_version}"',
                content
            )
        
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            updated_files.append(filename)
    
    return updated_files

def bump_version(version_type='patch'):
    """Bump version based on type (major, minor, patch)"""
    current = get_current_version()
    if not current:
        print("Could not find current version!")
        return None
    
    parts = current.split('.')
    
    # Handle versions like "1.0.01"
    major = int(parts[0])
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'patch':
        patch += 1
    
    # Format with leading zeros if original had them
    if len(parts) > 2 and len(parts[2]) > 1 and parts[2].startswith('0'):
        new_version = f"{major}.{minor}.{patch:02d}"
    else:
        new_version = f"{major}.{minor}.{patch}"
    
    return new_version

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ['major', 'minor', 'patch']:
            # Bump version
            new_version = bump_version(sys.argv[1])
            if new_version:
                current = get_current_version()
                print(f"Bumping version from {current} to {new_version}")
                updated = update_version(current, new_version)
                print(f"Updated files: {', '.join(updated)}")
        else:
            # Set specific version
            new_version = sys.argv[1]
            current = get_current_version()
            print(f"Changing version from {current} to {new_version}")
            updated = update_version(current, new_version)
            print(f"Updated files: {', '.join(updated)}")
    else:
        print(f"Current version: {get_current_version()}")
        print("\nUsage:")
        print("  python bump_version.py           # Show current version")
        print("  python bump_version.py major     # Bump major version (1.0.0 -> 2.0.0)")
        print("  python bump_version.py minor     # Bump minor version (1.0.0 -> 1.1.0)")
        print("  python bump_version.py patch     # Bump patch version (1.0.0 -> 1.0.1)")
        print("  python bump_version.py 1.2.3     # Set specific version")