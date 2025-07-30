#!/usr/bin/env python3
import sys
from pg.venv_manager import create_virtualenv
from pg.installer import install_package

def cli():
    create_virtualenv()

    if len(sys.argv) < 2:
        print("Usage: my_pip install <package>")
        return

    if sys.argv[1] == "install":
        if len(sys.argv) < 3:
            print("⚠️ Please specify a package name or URL.")
            return
        install_package(sys.argv[2])
    else:
        print(f"❌ Unknown command: {sys.argv[1]}")



