"""
Module to expose more detailed version info for the installed `quantsapp`
"""

import sys

version: str = '0.0.1b1'
# version = '0.0.0.dev1+githash.fedcba987'
# version = '0.0.0.a1'  # Alpha
# version = '0.0.0.b1'  # Beta
# version = '0.0.0.rc1'  # Release candidate
__version__: str = version
VERSION: str = version
full_version: str = version

# git_revision = "7be8c1f9133516fe20fd076f9bdfe23d9f537874"
release = 'dev' not in version and '+' not in version
short_version = version.split("+")[0]

__date__ = '2025-05-20T19:01:25.072281+05:30'  # ISO 8601 format

__status__ = 'Development'  #  "Prototype", "Development", or "Production"

minimum_python_version = '3.12'



def __ensure_min_python_version(required_version: str) -> None:
    """Checks if the current Python version meets or exceeds the required version"""
    try:
        required_major, required_minor, *required_patch = map(int, required_version.split('.'))
    except ValueError:
        raise ValueError("Invalid required version format. Please use 'major.minor[.patch]'.")

    current_major = sys.version_info.major
    current_minor = sys.version_info.minor
    current_patch = sys.version_info.micro

    is_valid_py_version = False
    if current_major > required_major:
        is_valid_py_version = True
    elif current_major == required_major:
        if current_minor > required_minor:
            is_valid_py_version = True
        elif current_minor == required_minor:
            if not required_patch:  # No patch level specified in required version
                is_valid_py_version = True
            elif current_patch >= required_patch[0]:
                is_valid_py_version = True

    if not is_valid_py_version:
        print(f"Error: Python version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is too old")
        print(f"Please upgrade to Python version {minimum_python_version} or higher to run this program")
        sys.exit(1)


__ensure_min_python_version(minimum_python_version)