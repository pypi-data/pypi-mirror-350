#!/usr/bin/env python3
"""
Python wrapper for github-mcp-server Go binary.
This allows installation and execution via uvx.
"""

import os
import sys
import platform
import subprocess
import tempfile
import zipfile
import tarfile
from pathlib import Path
from urllib.request import urlopen
import json


class GithubMCPServerWrapper:
    """Wrapper to download and run the github-mcp-server Go binary."""
    
    REPO = "github/github-mcp-server"
    BINARY_NAME = "github-mcp-server"
    
    def __init__(self):
        self.cache_dir = Path.home() / ".cache" / "uvx-go-binaries" / self.BINARY_NAME
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.binary_path = self.cache_dir / self.BINARY_NAME
        if platform.system() == "Windows":
            self.binary_path = self.binary_path.with_suffix(".exe")
    
    def get_latest_release(self):
        """Fetch the latest release information from GitHub API."""
        api_url = f"https://api.github.com/repos/{self.REPO}/releases/latest"
        with urlopen(api_url) as response:
            return json.loads(response.read())
    
    def get_platform_asset_url(self, release_data):
        """Get the download URL for the current platform."""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Map common architectures
        arch_map = {
            "x86_64": "amd64",
            "aarch64": "arm64",
            "armv7l": "arm",
        }
        arch = arch_map.get(machine, machine)
        
        # Map OS names
        os_map = {
            "darwin": "darwin",
            "linux": "linux",
            "windows": "windows",
        }
        os_name = os_map.get(system, system)
        
        # Find matching asset
        for asset in release_data["assets"]:
            name = asset["name"].lower()
            if os_name in name and arch in name:
                return asset["browser_download_url"]
        
        raise RuntimeError(f"No release found for {system} {machine}")
    
    def download_and_extract(self, url):
        """Download and extract the binary from the release archive."""
        print(f"Downloading {self.BINARY_NAME} from {url}...")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Download the archive
            archive_name = url.split("/")[-1]
            archive_path = tmppath / archive_name
            
            with urlopen(url) as response:
                archive_path.write_bytes(response.read())
            
            # Extract based on file type
            if archive_name.endswith(".zip"):
                with zipfile.ZipFile(archive_path) as zf:
                    zf.extractall(tmppath)
            elif archive_name.endswith((".tar.gz", ".tgz")):
                with tarfile.open(archive_path, "r:gz") as tf:
                    tf.extractall(tmppath)
            elif archive_name.endswith(".tar"):
                with tarfile.open(archive_path, "r") as tf:
                    tf.extractall(tmppath)
            else:
                # Assume it's the binary itself
                archive_path.rename(self.binary_path)
                self.binary_path.chmod(0o755)
                return
            
            # Find the binary in extracted files
            for root, dirs, files in os.walk(tmppath):
                for file in files:
                    if file.startswith(self.BINARY_NAME):
                        src = Path(root) / file
                        src.rename(self.binary_path)
                        self.binary_path.chmod(0o755)
                        return
            
            raise RuntimeError(f"Binary {self.BINARY_NAME} not found in archive")
    
    def ensure_binary(self):
        """Ensure the Go binary is downloaded and available."""
        if self.binary_path.exists():
            return
        
        try:
            print(f"Installing {self.BINARY_NAME}...")
            release_data = self.get_latest_release()
            url = self.get_platform_asset_url(release_data)
            self.download_and_extract(url)
            print(f"Successfully installed {self.BINARY_NAME} to {self.binary_path}")
        except Exception as e:
            print(f"Error installing {self.BINARY_NAME}: {e}", file=sys.stderr)
            sys.exit(1)
    
    def run(self, args):
        """Run the Go binary with given arguments."""
        self.ensure_binary()
        
        try:
            # Run the binary with all passed arguments
            result = subprocess.run(
                [str(self.binary_path)] + args,
                check=False
            )
            sys.exit(result.returncode)
        except Exception as e:
            print(f"Error running {self.BINARY_NAME}: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Entry point for the wrapper."""
    wrapper = GithubMCPServerWrapper()
    wrapper.run(sys.argv[1:])


if __name__ == "__main__":
    main()