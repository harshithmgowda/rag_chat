"""
Phase 1: Environment Sanity Check Script
This script verifies that your Python virtual environment is working properly!
"""
import sys
import os

# Ensure Windows terminal outputs UTF-8 characters cleanly
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    print("=" * 50)
    print("🚀 PYTHON ENVIRONMENT CHECK SUCCESSFUL!")
    print("=" * 50)
    print(f"🐍 Python Version   : {sys.version.split()[0]}")
    print(f"📍 Python Location  : {sys.executable}")
    print(f"📂 Working Directory: {os.getcwd()}")
    
    # Check if we are running inside a virtual environment
    is_venv = sys.prefix != sys.base_prefix
    if is_venv:
        print("✅ Status            : Running INSIDE a Virtual Environment (Isolated & Safe)")
    else:
        print("⚠️ Status            : Running in Global Python (Consider activating venv)")
    print("=" * 50)

if __name__ == "__main__":
    main()
