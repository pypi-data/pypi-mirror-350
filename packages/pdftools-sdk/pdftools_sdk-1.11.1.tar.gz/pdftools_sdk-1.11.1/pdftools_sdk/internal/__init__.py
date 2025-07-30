import os
import platform
from ctypes import CDLL, c_void_p
import atexit

# Only load the library if it hasn't been loaded already
_lib = globals().get('_lib', None)

def __load_library():
    # Define the library name
    lib_name = "PdfToolsSdk"

    # Get the current platform
    current_platform = platform.system().lower()
    if current_platform == "linux":
        lib_name = "lib" + lib_name + ".so"
    elif current_platform == "darwin":
        lib_name = "lib" + lib_name + ".dylib"
    elif current_platform == "windows":
        lib_name += ".dll"

    # Get the current architecture
    current_arch = platform.machine()

    # Map the platform and architecture to the corresponding folder
    folder_map = {
        "linux": {
            "x86_64": "linux-x64"
        },
        "darwin": {
            "x86_64": "osx-x64",
            "arm64": "osx-arm64"
        },
        "windows": {
            "AMD64": "win-x64",
            "x86": "win-x86",
            "ARM64": "win-arm64"
        }
    }

    # Get the platform and architecture specific folder
    folder = folder_map.get(current_platform, {}).get(current_arch, "")

    # Get the directory of the current file
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Construct the library path
    lib_path = os.path.join(dir_path, "lib", folder, lib_name)

    # Load the library
    try:
        lib = CDLL(lib_path)
        lib.PdfTools_Initialize.restype = None
        lib.PdfTools_Initialize.argtypes = []
        lib.PdfTools_Initialize()

        print(f"Successfully loaded library from {lib_path}")

        # Register the uninitialization function
        def _unload_library():
            if lib is not None:
                lib.PdfTools_Uninitialize.restype = None
                lib.PdfTools_Uninitialize.argtypes = []
                lib.PdfTools_Uninitialize()
                print("Successfully unloaded library")

        atexit.register(_unload_library)

        return lib
    except OSError as e:
        print(f"Failed to load library from {lib_path}: {e}")
        return None

# Load the library only if it has not been loaded yet
if _lib is None:
    _lib = __load_library()
