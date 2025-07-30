#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
import json
import fcntl
import tempfile
from pathlib import Path

class ToolChain:
    def __init__(self):
        self.home_dir = Path.home()
        self.tc_dir = self.home_dir / '.toolchain'
        self.scripts_dir = self.tc_dir / 'scripts'
        self.webapps_dir = self.tc_dir / 'webapps'
        self.metadata_file = self.tc_dir / 'metadata.json'
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create toolchain directories if they don't exist"""
        self.tc_dir.mkdir(exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
        self.webapps_dir.mkdir(exist_ok=True)
        
        if not self.metadata_file.exists():
            self._save_metadata({})
    
    def _load_metadata(self):
        """Load metadata about stored items"""
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except PermissionError:
            print(f"Error: Permission denied reading metadata file '{self.metadata_file}'")
            print("Please check file permissions and try again.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Metadata file '{self.metadata_file}' is corrupted (invalid JSON)")
            print(f"JSON error: {e}")
            print("Consider backing up and removing the file to reset toolchain.")
            sys.exit(1)
    
    def _save_metadata(self, metadata):
        """Save metadata about stored items with atomic write and file locking"""
        try:
            # Use atomic write with temporary file to prevent corruption
            temp_file = self.metadata_file.parent / f"{self.metadata_file.name}.tmp"
            with open(temp_file, 'w') as f:
                # Lock the file to prevent concurrent access
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                json.dump(metadata, f, indent=2)
                f.write('\n')  # Add trailing newline
                f.flush()
                os.fsync(f.fileno())  # Ensure data is written to disk
            
            # Atomically replace the original file
            temp_file.replace(self.metadata_file)
        except PermissionError:
            print(f"Error: Permission denied writing to metadata file '{self.metadata_file}'")
            print("Please check directory permissions and try again.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Failed to save metadata: {e}")
            # Clean up temp file if it exists
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except:
                    pass
            sys.exit(1)
    
    def add(self, file_path, name):
        """Add a script or web app to the toolchain"""
        source_path = Path(file_path)
        
        if not source_path.exists():
            print(f"Error: File '{file_path}' does not exist")
            return False
        
        # Load metadata with file locking to prevent race conditions
        try:
            with open(self.metadata_file, 'r') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared lock for reading
                content = f.read().strip()
                metadata = json.loads(content) if content else {}
        except FileNotFoundError:
            metadata = {}
        except PermissionError:
            print(f"Error: Permission denied reading metadata file '{self.metadata_file}'")
            print("Please check file permissions and try again.")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Metadata file '{self.metadata_file}' is corrupted (invalid JSON)")
            print(f"JSON error: {e}")
            print("Consider backing up and removing the file to reset toolchain.")
            return False
        
        if name in metadata:
            print(f"Error: Name '{name}' already exists. Use 'tc remove {name}' first.")
            return False
        
        # Determine file type and destination
        if source_path.suffix == '.py':
            dest_dir = self.scripts_dir
            item_type = 'script'
        elif source_path.suffix == '.html':
            dest_dir = self.webapps_dir
            item_type = 'webapp'
        else:
            print(f"Error: Unsupported file type '{source_path.suffix}'. Only .py and .html files are supported.")
            return False
        
        # Copy file to toolchain directory
        dest_path = dest_dir / f"{name}{source_path.suffix}"
        try:
            shutil.copy2(source_path, dest_path)
        except Exception as e:
            print(f"Error copying file: {e}")
            return False
        
        # Update metadata
        metadata[name] = {
            'type': item_type,
            'file': str(dest_path),
            'original_path': str(source_path)
        }
        self._save_metadata(metadata)
        
        print(f"Added {item_type} '{name}' successfully")
        return True
    
    def run(self, name, args=None):
        """Run a stored script or web app"""
        metadata = self._load_metadata()
        
        if name not in metadata:
            print(f"Error: '{name}' not found. Use 'tc list' to see available items.")
            return False
        
        item = metadata[name]
        file_path = Path(item['file'])
        
        if not file_path.exists():
            print(f"Error: File for '{name}' no longer exists")
            return False
        
        try:
            if item['type'] == 'script':
                # Check if uv is available
                if shutil.which('uv'):
                    cmd = ['uv', 'run', str(file_path)]
                else:
                    print("Warning: 'uv' not found, falling back to system Python")
                    cmd = [sys.executable, str(file_path)]
                
                if args:
                    cmd.extend(args)
                subprocess.run(cmd)
            elif item['type'] == 'webapp':
                import webbrowser
                webbrowser.open(f"file://{file_path.absolute()}")
            return True
        except Exception as e:
            print(f"Error running '{name}': {e}")
            return False
    
    def remove(self, name):
        """Remove a stored script or web app"""
        metadata = self._load_metadata()
        
        if name not in metadata:
            print(f"Error: '{name}' not found")
            return False
        
        item = metadata[name]
        file_path = Path(item['file'])
        
        # Remove file if it exists
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                print(f"Warning: Could not delete file: {e}")
        
        # Remove from metadata
        del metadata[name]
        self._save_metadata(metadata)
        
        print(f"Removed '{name}' successfully")
        return True
    
    def list_items(self):
        """List all stored scripts and web apps"""
        metadata = self._load_metadata()
        
        if not metadata:
            print("No items in toolchain")
            return
        
        print("Toolchain items:")
        for name, item in metadata.items():
            print(f"  {name} ({item['type']})")

def main():
    parser = argparse.ArgumentParser(description='Toolchain - Manage your scripts and web apps')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a script or web app')
    add_parser.add_argument('file', help='Path to the file to add')
    add_parser.add_argument('name', help='Name to give the item')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run a stored script or web app')
    run_parser.add_argument('name', help='Name of the item to run')
    run_parser.add_argument('args', nargs='*', help='Optional arguments to pass to the script')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a stored script or web app')
    remove_parser.add_argument('name', help='Name of the item to remove')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all stored items')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    tc = ToolChain()
    
    if args.command == 'add':
        tc.add(args.file, args.name)
    elif args.command == 'run':
        tc.run(args.name, args.args)
    elif args.command == 'remove':
        tc.remove(args.name)
    elif args.command == 'list':
        tc.list_items()

if __name__ == '__main__':
    main()