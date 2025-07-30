import os
import sys
import json
import platform
import subprocess
from pathlib2 import Path
import argparse
def start(argv):
    parser=argparse.ArgumentParser()
    parser.add_argument("--no-venv", action="store_true", help="Run without venv, even if a compatible venv is present.")
    args=parser.parse_args(argv)
    if not os.path.exists("config.json"):
        print("This folder does not contain a PyPositron project. Please navigate to the project root, where config.json is located.")
        print("You can create a new project with PyPositron create.")
        sys.exit(1)
    with open(os.path.abspath("config.json"), "r") as f:
        config = json.load(f)
    # switch CWD to project root so all relative paths (entry_file, venvs) resolve correctly
    os.chdir(os.path.dirname(os.path.abspath("config.json")))
    if not os.path.exists(config["entry_file"]):
        print(f"The entry file {config['entry_file']} does not exist. Please create it or change the entry file path in config.json.")
        sys.exit(1)
    if not args.no_venv:
        if platform.system().lower().strip() == "windows":
            ps1_path = Path(__file__).parent / "python_executor.ps1"
            absolute = ps1_path.resolve()
            if config["has_venv"]:
                if os.path.exists(config.get("winvenv_executable","")) and config.get("winvenv_executable","") != "":
                    cmd = ["powershell","-NoProfile","-ExecutionPolicy", "Bypass","-Command", f"& '{absolute}' \'{config["entry_file"]}\' \'{os.getcwd()}\' \'{config["winvenv_executable"]}\'"]
                    result = subprocess.run(cmd,check=True)
                    if result.returncode != 0:
                        print("Error:", result.stderr, file=sys.stderr)
                        sys.exit(result.returncode)
                    sys.exit(0)
                else:
                    print("\x1b[0;93;49m[WARN]Running without venv, as this project does not contain a windows venv, but has a linux venv.\x1b[0m")
            if os.path.exists(config["python_executable"]):
                cmd = ["powershell","-NoProfile","-ExecutionPolicy", "Bypass","-Command", f"& '{absolute}' \'{config["entry_file"]}\' \'{os.getcwd()}\' \'{config["python_executable"]}\'"]
                
            else:
                cmd = ["powershell","-NoProfile","-ExecutionPolicy", "Bypass","-Command", f"& '{absolute}' \'{config["entry_file"]}\' \'{os.getcwd()}\' \'python3\'"]
            result = subprocess.run(cmd,check=True)
            if result.returncode != 0:
                print("Error:", result.stderr, file=sys.stderr)
                sys.exit(result.returncode)
            sys.exit(0)
        else:
            if config["has_venv"]:
                if os.path.exists(config.get("linuxvenv","")) and config.get("linuxvenv","") != "":
                    os.system("bash -c \'source \""+config["linuxvenv"]+"/bin/activate\" && python3 \""+os.path.abspath(config["entry_file"])+"\"\'")
                    exit(0)
                else:
                    print("\x1b[0;93;49m[WARN]Running without venv, as this project does not contain a linux venv, but has a Windows venv.\x1b[0m")
            os.system("python3 \""+os.path.abspath(config["entry_file"])+"\"")
            exit(0)
    else:
        if platform.system().lower().strip() == "windows":
            ps1_path = Path(__file__).parent / "python_executor.ps1"
            absolute = ps1_path.resolve()
            if os.path.exists(config["python_executable"]):
                cmd = ["powershell","-NoProfile","-ExecutionPolicy", "Bypass","-Command", f"& '{absolute}' \'{config["entry_file"]}\' \'{os.getcwd()}\' \'{config["python_executable"]}\'"]
                
            else:
                cmd = ["powershell","-NoProfile","-ExecutionPolicy", "Bypass","-Command", f"& '{absolute}' \'{config["entry_file"]}\' \'{os.getcwd()}\' \'python3\'"]
            result = subprocess.run(cmd,check=True)
            if result.returncode != 0:
                print("Error:", result.stderr, file=sys.stderr)
                sys.exit(result.returncode)
            sys.exit(0)
        else:
            os.system("python3 \""+os.path.abspath(config["entry_file"])+"\"")
            exit(0)
