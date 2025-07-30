#!/usr/bin/env python3
"""
Command-line interface for wl_version_manager
"""

import sys
import argparse
from .version_manager import VersionManager


def main():
    parser = argparse.ArgumentParser(description="Manage package versions")
    parser.add_argument("--version-file", default="VERSION", 
                       help="Version file path (default: VERSION)")
    parser.add_argument("--setup-file", default="setup.py",
                       help="Setup file path (default: setup.py)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Current version command
    subparsers.add_parser("current", help="Show current version")
    
    # Bump commands
    subparsers.add_parser("patch", help="Bump patch version")
    subparsers.add_parser("minor", help="Bump minor version")
    subparsers.add_parser("major", help="Bump major version")
    
    # Set version command
    set_parser = subparsers.add_parser("set", help="Set specific version")
    set_parser.add_argument("version", help="Version to set (e.g., 1.2.3)")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize VERSION file")
    init_parser.add_argument("--initial-version", default="0.1.0",
                           help="Initial version (default: 0.1.0)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    vm = VersionManager(args.version_file, args.setup_file)
    
    try:
        if args.command == "init":
            vm.write_version(args.initial_version)
            vm.update_setup_py(args.initial_version)
            print(f"Initialized version to {args.initial_version}")
        
        elif args.command == "current":
            print(vm.read_version())
        
        elif args.command == "patch":
            new_version = vm.bump_patch()
            print(f"Bumped to {new_version}")
        
        elif args.command == "minor":
            new_version = vm.bump_minor()
            print(f"Bumped to {new_version}")
        
        elif args.command == "major":
            new_version = vm.bump_major()
            print(f"Bumped to {new_version}")
        
        elif args.command == "set":
            new_version = vm.set_version(args.version)
            print(f"Set version to {new_version}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())