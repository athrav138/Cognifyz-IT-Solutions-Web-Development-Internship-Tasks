"""
utils/paths.py

Provides utility functions for path resolution, ensuring the application
works correctly both in a development environment and when bundled
as a standalone executable (e.g., with PyInstaller).
"""

import os
import sys

def get_base_dir():
    """
    Returns the absolute path to the directory containing the application.
    If running as a bundled executable, this returns the directory where the
    executable is located. Otherwise, it returns the project root.
    """
    if getattr(sys, 'frozen', False):
        # Running as a bundled executable
        return os.path.dirname(sys.executable)
    else:
        # Running in a normal Python environment
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    For --onefile, resources are unpacked to sys._MEIPASS.
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)
