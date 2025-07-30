import re
import os
import sys
from pathlib import Path


class VersionManager:
    def __init__(self, version_file="VERSION", setup_file="setup.py"):
        self.version_file = Path(version_file)
        self.setup_file = Path(setup_file)
        
    def read_version(self):
        """Read current version from VERSION file"""
        if not self.version_file.exists():
            raise FileNotFoundError(f"Version file {self.version_file} not found")
        return self.version_file.read_text().strip()
    
    def write_version(self, version):
        """Write version to VERSION file"""
        self.version_file.write_text(version + '\n')
        
    def update_setup_py(self, version):
        """Update version in setup.py"""
        if not self.setup_file.exists():
            print(f"Warning: {self.setup_file} not found, skipping setup.py update")
            return
            
        content = self.setup_file.read_text()
        
        # Pattern to match version= line
        pattern = r'version\s*=\s*["\'][^"\']*["\']'
        replacement = f'version="{version}"'
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            self.setup_file.write_text(new_content)
        else:
            print(f"Warning: Could not find version= line in {self.setup_file}")
    
    def parse_version(self, version_str):
        """Parse version string into major.minor.patch"""
        parts = version_str.split('.')
        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {version_str}. Expected major.minor.patch")
        
        try:
            return [int(part) for part in parts]
        except ValueError:
            raise ValueError(f"Invalid version format: {version_str}. All parts must be integers")
    
    def format_version(self, major, minor, patch):
        """Format version components into string"""
        return f"{major}.{minor}.{patch}"
    
    def bump_patch(self):
        """Increment patch version"""
        current = self.read_version()
        major, minor, patch = self.parse_version(current)
        new_version = self.format_version(major, minor, patch + 1)
        self._update_version(new_version)
        return new_version
    
    def bump_minor(self):
        """Increment minor version, reset patch to 0"""
        current = self.read_version()
        major, minor, patch = self.parse_version(current)
        new_version = self.format_version(major, minor + 1, 0)
        self._update_version(new_version)
        return new_version
    
    def bump_major(self):
        """Increment major version, reset minor and patch to 0"""
        current = self.read_version()
        major, minor, patch = self.parse_version(current)
        new_version = self.format_version(major + 1, 0, 0)
        self._update_version(new_version)
        return new_version
    
    def set_version(self, version_str):
        """Set specific version"""
        # Validate format
        self.parse_version(version_str)
        self._update_version(version_str)
        return version_str
    
    def _update_version(self, new_version):
        """Update both VERSION file and setup.py"""
        self.write_version(new_version)
        self.update_setup_py(new_version)

    @staticmethod
    def get_version(version_file="VERSION", default_version="0.1.0"):
        """
        Get version from file, create with default if missing.
        
        Args:
            version_file: Path to version file (default: "VERSION")
            default_version: Default version if file doesn't exist (default: "0.1.0")
            
        Returns:
            Version string
        """
        vm = VersionManager(version_file)
        
        try:
            return vm.read_version()
        except FileNotFoundError:
            # Create VERSION file with default version
            vm.write_version(default_version)
            return default_version



__all__ = ['VersionManager']