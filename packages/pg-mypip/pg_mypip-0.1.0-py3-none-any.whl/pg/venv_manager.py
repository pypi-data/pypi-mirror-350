import os
import subprocess
import sys



def add_venv_to_gitignore(venv_dir):
    gitignore_path = ".gitignore"
    # Read existing .gitignore entries if file exists
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            lines = f.read().splitlines()
    else:
        lines = []
    # Add venv_dir if not already present
    if venv_dir not in lines:
        with open(gitignore_path, "a") as f:
            if lines and lines[-1] != "":
                f.write("\n")
            f.write(f"{venv_dir}\n")
        print(f"📝 Added '{venv_dir}' to .gitignore")
    else:
        print(f"ℹ️ '{venv_dir}' is already in .gitignore")

def create_virtualenv():
    venv_dir = input("Enter the name for your virtual environment (default: my_pip_env): ").strip() or "my_pip_env"
    if not os.path.exists(venv_dir):
        print(f"🔧 Creating virtual environment at '{venv_dir}'...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        print(f"✅ Virtual environment created at {venv_dir}")
    else:
        print(f"ℹ️ Virtual environment already exists at {venv_dir}")

def get_pip_path(venv_dir="my_pip_env"):
    if os.name == "nt":  # Windows
        return os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_dir, "bin", "pip")

def get_python_path(venv_dir="my_pip_env"):
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        return os.path.join(venv_dir, "bin", "python")
