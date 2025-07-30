#!/usr/bin/env python3
import os
import sys
import argparse
import json
import platform
import subprocess
import shutil
from pathlib2 import Path


def build(args):
    """Build a Positron project into an executable using Nuitka."""
    
    parser = argparse.ArgumentParser(
        prog="positron build",
        description="Build a Positron project into an executable using Nuitka"
    )
    parser.add_argument(
        "--root_path", "-r", 
        help="Root path of the project (default: current directory)", 
        type=str, 
        default=".", 
        required=False
    )
    parser.add_argument(
        "--output", "-o",
        help="Output filename for the executable (default: project name)",
        type=str,
        required=False
    )
    parser.add_argument(
        "--build-type",
        help="Type of build to create",
        type=str,
        choices=["EXE", "EXE-ONEDIR", "DEB", "DMG", "APK"],
        default="EXE-ONEDIR"
    )
    parser.add_argument(
        "--onefile",
        help="Create a single executable file instead of a directory",
        action="store_true"
    )
    parser.add_argument(
        "--windows-console",
        help="Keep console window on Windows (default: disable for GUI apps)",
        action="store_true"
    )
    parser.add_argument(
        "--include-data",
        help="Include additional data files (format: source=destination)",
        action="append",
        default=[]
    )
    parser.add_argument(
        "--python-path",
        help="Specific Python interpreter to use for building",
        type=str,
        required=False
    )
    
    parsed_args = parser.parse_args(args)
    
    # Get project directory
    directory = os.path.abspath(parsed_args.root_path)
    os.chdir(directory)
    
    # Check if this is a Positron project
    config_path = os.path.join(directory, "config.json")
    if not os.path.exists(config_path):
        print("❌ Error: This directory is not a Positron project.")
        print("Please run this command from the root of your Positron project (where config.json is located).")
        print("To create a new Positron project, run: positron create")
        return 1
    
    # Load project configuration
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return 1
    
    project_name = config.get("name", "positron_app")
    main_file = config.get("entry_file", "main/main.py")
    
    # Check if main file exists
    main_file_path = os.path.join(directory, main_file)
    if not os.path.exists(main_file_path):
        print(f"❌ Error: Main file '{main_file}' not found in project directory.")
        print(f"Expected location: {main_file_path}")
        return 1
    
    # Check if Nuitka is available
    print("🔍 Checking for Nuitka...")
    if not _check_nuitka_available():
        print("❌ Nuitka is not installed or not available in PATH.")
        print("\n📦 To install Nuitka, run one of the following commands:")
        print("   pip install nuitka")
        print("   pip install nuitka[all]  # For additional features")
        print("\n💡 If you're using a virtual environment which has Nutika, make sure it's activated.")
        return 1
    
    print("✅ Nuitka found!")
    
    # Determine output filename
    output_name = parsed_args.output or project_name
    if platform.system().lower() == "windows" and not output_name.endswith('.exe'):
        output_name += '.exe'
    
    # Build Nuitka command
    nuitka_cmd = ["python", "-m", "nuitka"]
    
    # Add main file
    nuitka_cmd.append(main_file_path)
    
    # Output options
    nuitka_cmd.extend(["--output-filename", output_name])
    
    # Handle different build types
    build_type = parsed_args.build_type
    print(f"📦 Building with type: {build_type}")
    
    if build_type == "EXE":
        # Single executable file
        nuitka_cmd.append("--onefile")
        if platform.system().lower() == "windows":
            print("📦 Building as single Windows executable...")
        else:
            print("📦 Building as single executable...")
    elif build_type == "EXE-ONEDIR":
        # Directory with executable and dependencies
        print("📂 Building as directory with executable...")
    elif build_type == "DEB":
        if platform.system().lower() != "linux":
            print("⚠️ Warning: Building DEB package on a non-Linux system may not work correctly.")
        print("📦 Building Debian package...")
        nuitka_cmd.extend(["--debian-package"])
    elif build_type == "DMG":
        if platform.system().lower() != "darwin":
            print("⚠️ Warning: Building DMG package on a non-macOS system may not work correctly.")
        print("📦 Building macOS package...")
        nuitka_cmd.extend(["--macos-create-app-bundle"])
    elif build_type == "APK":
        print("⚠️ Building APK packages requires additional setup with Buildozer.")
        print("This functionality is experimental.")
        return 1
    
    # Onefile option (this will override if build_type is something else but --onefile is passed)
    if parsed_args.onefile:
        nuitka_cmd.append("--onefile")
        print("📦 Building as single executable file...")
    
    # Console options for Windows
    if platform.system().lower() == "windows":
        if not parsed_args.windows_console:
            nuitka_cmd.append("--windows-disable-console")
            print("🖥️  Console window will be disabled (GUI mode)")
        else:
            print("🖥️  Console window will be kept")
    
    # Include data files
    for data_spec in parsed_args.include_data:
        if '=' in data_spec:
            source, dest = data_spec.split('=', 1)
            nuitka_cmd.extend(["--include-data-file", f"{source}={dest}"])
        else:
            nuitka_cmd.extend(["--include-data-file", data_spec])
    
    # Add optimization flags
    nuitka_cmd.extend([
        "--enable-plugin=pylint-warnings",
        "--assume-yes-for-downloads",
        "--show-progress"
    ])
      # Detect and include common web frameworks
    if _has_flask_or_fastapi(directory):
        print("🌐 Detected web framework, adding web-related optimizations...")
        nuitka_cmd.extend([
            "--include-package=flask",
            "--include-package=fastapi",
            "--include-package=uvicorn",
            "--include-package=jinja2"
        ])
    
    # Include all project files
    print("📁 Including all project files...")
    nuitka_cmd.extend(["--include-data-dir", f"{directory}={directory}"])
    
    print(f"\n🔨 Building executable for {project_name}...")
    print(f"📄 Main file: {main_file}")
    print(f"📤 Output: {output_name}")
    print(f"🎯 Target: {platform.system()} {platform.machine()}")
    
    # Show the command that will be executed
    print(f"\n🚀 Running Nuitka...")
    print("Command:", " ".join(nuitka_cmd))
    print()
    
    try:
        # Run Nuitka
        result = subprocess.run(nuitka_cmd, check=True, cwd=directory)
        
        print(f"\n✅ Build completed successfully!")
        print(f"📦 Executable created: {output_name}")
        
        # Provide instructions
        if parsed_args.onefile:
            print(f"\n💡 You can now run your application with: ./{output_name}")
        else:
            dist_dir = output_name.replace('.exe', '.dist') if output_name.endswith('.exe') else f"{output_name}.dist"
            print(f"💡 Your application is in the '{dist_dir}' directory")
            print(f"   Run it with: ./{dist_dir}/{output_name}")
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with exit code {e.returncode}")
        print("🔧 Try the following troubleshooting steps:")
        print("   1. Make sure all dependencies are installed")
        print("   2. Check that your main file runs without errors")
        print("   3. Try building with --windows-console to see error messages")
        print("   4. Update Nuitka: pip install --upgrade nuitka")
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


def _check_nuitka_available():
    """Check if Nuitka is available in the current environment."""
    try:
        result = subprocess.run(
            ["python", "-m", "nuitka", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try alternative method
            result = subprocess.run(
                ["nuitka", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


def _has_flask_or_fastapi(directory):
    """Check if the project uses Flask or FastAPI."""
    try:
        # Check requirements files
        req_files = ["requirements.txt", "requirements-dev.txt", "pyproject.toml"]
        for req_file in req_files:
            req_path = os.path.join(directory, req_file)
            if os.path.exists(req_path):
                with open(req_path, 'r') as f:
                    content = f.read().lower()
                    if 'flask' in content or 'fastapi' in content:
                        return True
        
        # Check main file imports
        config_path = os.path.join(directory, "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                main_file = config.get("main", "main_app.py")
                main_path = os.path.join(directory, main_file)
                if os.path.exists(main_path):
                    with open(main_path, 'r') as f:
                        content = f.read().lower()
                        if 'import flask' in content or 'from flask' in content or \
                           'import fastapi' in content or 'from fastapi' in content:
                            return True
        
        return False
    except Exception:
        return False


if __name__ == "__main__":
    sys.exit(build(sys.argv[1:]))
