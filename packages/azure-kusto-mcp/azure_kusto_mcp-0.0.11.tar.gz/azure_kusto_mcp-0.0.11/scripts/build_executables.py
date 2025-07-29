import os
import platform
import shutil
import sys
from pathlib import Path
from typing import List, Literal

OSClassifierType = Literal[
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: POSIX :: Linux",
]


def get_executable_name() -> str:
    system = platform.system().lower()
    if system == "windows":
        return "kusto-mcp.exe"
    elif system == "darwin":
        return "kusto-mcp-macos"
    else:
        return "kusto-mcp-linux"


def detect_supported_platforms(bin_dir: Path) -> List[OSClassifierType]:
    """
    Detect supported platforms by scanning the executables in the bin directory.
    Returns a list of platform classifiers.
    """
    platforms: List[OSClassifierType] = []
    for file in os.listdir(bin_dir):
        if file.endswith(".exe"):
            platforms.append("Operating System :: Microsoft :: Windows")
        elif file.endswith("-macos"):
            platforms.append("Operating System :: MacOS")
        elif file.endswith("-linux"):
            platforms.append("Operating System :: POSIX :: Linux")

    if not platforms:
        raise RuntimeError("No platform-specific executables found. Canceling build.")
    return sorted(list(set(platforms)))  # Remove duplicates and sort


def build_executable() -> None:
    # Ensure PyInstaller is installed
    try:
        import PyInstaller.__main__
    except ImportError:
        print("Installing PyInstaller...")
        os.system(f"{sys.executable} -m pip install pyinstaller")
        import PyInstaller.__main__

    executable_name = get_executable_name()

    # Create bin directory if it doesn't exist
    bin_dir = Path("kusto_mcp/bin")
    bin_dir.mkdir(exist_ok=True, parents=True)

    # Build executable
    venv_path = os.environ.get("VIRTUAL_ENV", ".venv")
    site_packages = os.path.join(venv_path, "Lib", "site-packages")
    kusto_data_path = os.path.join(site_packages, "azure", "kusto", "data")

    print(f"Looking for JSON files in: {kusto_data_path}")
    if not os.path.exists(kusto_data_path):
        raise FileNotFoundError(f"Could not find path: {kusto_data_path}")
    json_files = [f for f in os.listdir(kusto_data_path) if f.endswith(".json")]
    print(f"Found JSON files: {json_files}")

    PyInstaller.__main__.run(
        [
            "kusto_mcp/server.py",
            "--onefile",
            "--name",
            executable_name,
            "--distpath",
            str(bin_dir),
            "--clean",
            "--add-data",
            f"{kusto_data_path}/*.json{os.pathsep}azure/kusto/data",
        ]
    )

    # Clean up build artifacts
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists(f"{executable_name}.spec"):
        os.remove(f"{executable_name}.spec")

    # Update platform metadata after successful build
    platforms = detect_supported_platforms(bin_dir)

    # Show available executables
    print("\nAvailable executables:")
    for file in sorted(os.listdir(bin_dir)):
        print(f"  {file}")

    # Show detected platform support
    print("\nDetected platform support:")
    platform_map = {
        "Operating System :: Microsoft :: Windows": ("Windows", "kusto-mcp.exe"),
        "Operating System :: MacOS": ("macOS", "kusto-mcp-macos"),
        "Operating System :: POSIX :: Linux": ("Linux", "kusto-mcp-linux"),
    }

    for plat in sorted(platforms):
        os_name, executable = platform_map[plat]
        print(f"✓ {os_name} (found {executable})")


if __name__ == "__main__":
    build_executable()
