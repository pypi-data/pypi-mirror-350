#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import argparse
from typing import List, Tuple
import shutil


class InstallerError(Exception):
    pass


class DependencyInstaller:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.os_name = platform.system().lower()
        self.is_root = os.geteuid() == 0 if self.os_name != 'windows' else True

    def log(self, message: str) -> None:
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def run_command(self, command: List[str], check: bool = True) -> Tuple[int, str, str]:
        """Execute a command and return its output."""
        try:
            self.log(f"Running command: {' '.join(command)}")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            if check and process.returncode != 0:
                raise InstallerError(f"Command failed: {stderr}")
            return process.returncode, stdout, stderr
        except Exception as e:
            raise InstallerError(f"Failed to execute command: {e}")

    def check_python_version(self) -> None:
        """Verify Python version is compatible."""
        if sys.version_info < (3, 7):
            raise InstallerError("Python 3.7 or higher is required")
        self.log(f"Python version {sys.version_info.major}.{sys.version_info.minor} detected")

    def check_pip(self) -> None:
        """Verify pip is installed and up to date."""
        try:
            import pip
            self.run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            self.log("Pip is installed and up to date")
        except ImportError:
            raise InstallerError("Pip is not installed. Please install pip first.")

    def install_system_dependencies_debian(self) -> None:
        """Install system dependencies for Debian-based systems."""
        if not self.is_root:
            raise InstallerError("Root privileges required. Please run with sudo.")

        commands = [
            ["apt-get", "update"],
            ["apt-get", "install", "-y",
             "ffmpeg",
             "libavcodec-dev",
             "libavformat-dev",
             "libswscale-dev",
             "libavdevice-dev",
             "libavfilter-dev",
             "libavutil-dev",
             "python3-dev",
             "python3-pip"]
        ]

        for cmd in commands:
            self.run_command(cmd)

    def install_system_dependencies_rhel(self) -> None:
        """Install system dependencies for RHEL-based systems."""
        if not self.is_root:
            raise InstallerError("Root privileges required. Please run with sudo.")

        commands = [
            ["yum", "install", "-y", "epel-release"],
            ["yum", "install", "-y",
             "ffmpeg",
             "ffmpeg-devel",
             "python3-devel",
             "python3-pip"]
        ]

        for cmd in commands:
            self.run_command(cmd)

    def install_system_dependencies_macos(self) -> None:
        """Install system dependencies for macOS."""
        if not shutil.which("brew"):
            raise InstallerError("Homebrew is required. Please install it first.")

        commands = [
            ["brew", "update"],
            ["brew", "install", "ffmpeg"],
            ["brew", "install", "python3"]
        ]

        for cmd in commands:
            self.run_command(cmd)

    def install_system_dependencies_windows(self) -> None:
        """Install system dependencies for Windows."""
        if not shutil.which("choco"):
            raise InstallerError(
                "Chocolatey is required for Windows installation. "
                "Please install it first: https://chocolatey.org/install"
            )

        commands = [
            ["choco", "install", "-y", "ffmpeg"],
            ["choco", "install", "-y", "python3"]
        ]

        for cmd in commands:
            self.run_command(cmd)

    def install_python_requirements(self) -> None:
        """Install Python package requirements."""
        requirements = [
            "opencv-python>=4.8.0",
            "av>=10.0.0",
            "numpy>=1.24.0",
            "av-ffmpeg>=6.0.0",
            "python-rtsp>=0.1.4",
            "typing-extensions>=4.5.0",
            "dataclasses>=0.6"
        ]

        with open("requirements.txt", "w") as f:
            f.write("\n".join(requirements))

        self.run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    def install(self) -> None:
        """Main installation method."""
        try:
            self.log("Starting installation...")
            self.check_python_version()
            self.check_pip()

            # Install system dependencies based on OS
            if self.os_name == "linux":
                # Check Linux distribution
                if os.path.exists("/etc/debian_version"):
                    self.install_system_dependencies_debian()
                elif os.path.exists("/etc/redhat-release"):
                    self.install_system_dependencies_rhel()
                else:
                    raise InstallerError("Unsupported Linux distribution")
            elif self.os_name == "darwin":
                self.install_system_dependencies_macos()
            elif self.os_name == "windows":
                self.install_system_dependencies_windows()
            else:
                raise InstallerError(f"Unsupported operating system: {self.os_name}")

            # Install Python requirements
            self.install_python_requirements()

            self.log("Installation completed successfully!")

        except InstallerError as e:
            print(f"Installation failed: {str(e)}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {str(e)}", file=sys.stderr)
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Install RTSP video processing dependencies")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    installer = DependencyInstaller(verbose=args.verbose)
    installer.install()


if __name__ == "__main__":
    main()