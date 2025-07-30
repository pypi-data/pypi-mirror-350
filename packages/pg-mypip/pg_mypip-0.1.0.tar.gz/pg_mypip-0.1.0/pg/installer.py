import subprocess
from venv_manager import get_pip_path

def update_package_list(package_name):
    with open("requirements.txt", "a") as f:
        f.write(package_name + "\n")

def install_package(package_source):
    pip = get_pip_path()
    try:
        subprocess.check_call([pip, "install", package_source])
        update_package_list(package_source)
        print(f"✅ Installed: {package_source}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install: {package_source}")

def upgrade_package(package_name):
    pip = get_pip_path()
    try:
        subprocess.check_call([pip, "install", "--upgrade", package_name])
        print(f"⬆️  Upgraded: {package_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to upgrade: {package_name}")

def uninstall_package(package_name):
    pip = get_pip_path()
    try:
        subprocess.check_call([pip, "uninstall", "-y", package_name])
        print(f"🗑️  Uninstalled: {package_name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to uninstall: {package_name}")

def list_packages():
    pip = get_pip_path()
    try:
        subprocess.check_call([pip, "list"])
    except subprocess.CalledProcessError:
        print("❌ Failed to list packages")
