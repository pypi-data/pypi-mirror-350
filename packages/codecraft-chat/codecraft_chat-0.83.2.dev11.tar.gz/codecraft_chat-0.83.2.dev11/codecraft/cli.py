#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entry point script for CodeCraft with proper UTF-8 handling.
This script is referenced in setup.py/pyproject.toml to create the
console script entry point that's callable from anywhere.
"""

import os
import sys
import subprocess


def main_direct_utf8():
    """
    Direct UTF-8 entry point that calls Python with -X utf8 flag.
    This is available as 'codecraft-utf8' after pip install.
    """
    # Set environment variables
    os.environ["PYTHONUTF8"] = "1"
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["PYTHONLEGACYWINDOWSSTDIO"] = "1"
    
    try:
        # On Windows, set console code page to UTF-8
        if sys.platform == "win32":
            # Set console code page to UTF-8 (65001)
            subprocess.run(["chcp", "65001"], shell=True, check=False)
            
        # Get the absolute path to the current Python executable
        python_exe = sys.executable
        
        # The simplest and most reliable approach - just use the module directly
        args = [python_exe, "-X", "utf8", "-m", "codecraft"] + sys.argv[1:]
        
        # Run the command with all arguments
        result = subprocess.run(args)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error: Unable to handle Unicode properly: {e}")
        print("\nPlease try: python -X utf8 -m codecraft [your arguments]")
        sys.exit(1)


def main():
    """
    Launch CodeCraft with UTF-8 encoding properly set.
    This function serves as the entry point when installed via pip.
    """
    # Set UTF-8 mode
    os.environ["PYTHONUTF8"] = "1"
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["PYTHONLEGACYWINDOWSSTDIO"] = "1"

    # If running on Windows, we need to use a direct approach
    if sys.platform == "win32":
        try:
            # Set console code page to UTF-8 (65001)
            subprocess.run(["chcp", "65001"], shell=True, check=False)
            
            # Get the absolute path to the current Python executable
            python_exe = sys.executable
            
            # The most reliable approach is to just use the module directly
            args = [python_exe, "-X", "utf8", "-m", "codecraft"] + sys.argv[1:]
            
            # Run the command with all arguments
            result = subprocess.run(args)
            sys.exit(result.returncode)
        except Exception as e:
            print(f"Error: Unable to handle Unicode properly: {e}")
            print("\nPlease try one of these options instead:")
            print("1. Run with: python -X utf8 -m codecraft [your arguments]")
            print("2. Set environment variable first: $env:PYTHONUTF8=\"1\"")
            print("3. Use the globally available command: codecraft-utf8 [your arguments]")
            sys.exit(1)
    else:
        # For non-Windows platforms, just import and run the main function
        from codecraft.main import main_with_utf8
        sys.exit(main_with_utf8())


if __name__ == "__main__":
    main() 