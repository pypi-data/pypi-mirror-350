import os
import sys
import ctypes
import platform
from pathlib import Path

# Cross-platform helper to load a shared library with global symbols
def load_shared_lib(lib_path):
  try:
    ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
  except Exception as e:
    print(f"[ERROR] Failed to load {lib_path}: {e}", file=sys.stderr)
    raise

# Check if IDA Python is already loaded
# Either we are running inside IDA or the idapro package was previously imported,
# which means IDA kernel is already available for ida_domain
def check_dependencies(idapro_lib_filename):
  try:
    import ida_diskio
    need_idapro = False
  except ImportError:
    need_idapro = True

  if need_idapro:
    try:
      import idapro
    except ImportError as e:
      # In case idapro package is not installed, try to locate the idalib module using $IDADIR
      ida_dir = os.environ.get("IDADIR", None)
      if ida_dir is None:
        print("[ERROR] Failed to import the 'idapro' Python module.\n"
          "Please ensure that 'idapro' Python module is properly installed. You can do this by following\n"
          "the instructions provided with your IDA installation.\n"
          "Alternatively, you can set the 'IDADIR' environment variable to point to your active IDA install directory.",
          file=sys.stderr)
        # Nothing to do, raise the error
        raise(e)
      # Add the $IDADIR/idalib/python folder to the sys path and try again
      sys.path.append(str(Path(ida_dir) / "idalib" / "python"))
      import idapro
  else:
    # Make sure idalib dll is also loaded, ida_domain is linked against it
    idapro_lib_path = os.path.join(ida_diskio.idadir(None), idapro_lib_filename)
    load_shared_lib(idapro_lib_path)

# Load the platform specific module
system = platform.system()
if system == "Linux":
  from .linux import *
elif system == "Darwin":
  from .macos import *
elif system == "Windows":
  from .windows import *
else:
  raise RuntimeError(f"Unsupported platform: {system}")