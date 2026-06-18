
import os
import subprocess
import sys

def build():
    """
    Bundles the application into a standalone executable using PyInstaller.
    """
    print("Starting build process...")
    
    # Define paths
    main_script = "main.py"
    app_name = "WebScraperPro"
    
    # PyInstaller command
    # --noconsole: Don't show a command prompt when running the app
    # --onefile: Bundle everything into a single .exe
    # --add-data: Include necessary assets (format is "source;dest" on Windows)
    # --name: Set the output executable name
    
    params = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        "--name", app_name,
        # Add assets
        "--add-data", f"assets{os.pathsep}assets",
        # Explicitly include sub-packages if needed (usually PyInstaller finds them)
        "--hidden-import", "PyQt6.sip",
    ]
    
    # If an icon exists, add it
    icon_path = os.path.join("assets", "icons", "app.ico")
    if os.path.exists(icon_path):
        params.extend(["--icon", icon_path])
    else:
        print("Note: No icon found at assets/icons/app.ico. Using default executable icon.")

    params.append(main_script)
    
    print(f"Running command: {' '.join(params)}")
    
    try:
        subprocess.check_call(params)
        print("\nBuild successful!")
        print(f"The executable can be found in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("\nError: PyInstaller not found. Please install it with 'pip install pyinstaller'.")
        sys.exit(1)

if __name__ == "__main__":
    build()
