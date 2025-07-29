import os
import platform
from .. import load_shared_lib, check_dependencies

# Verify the current operating system is supported
# This module only works on arm macOS platforms
system = platform.system()
machine = platform.machine()
if system != "Darwin" or not ('arm64' in machine or 'aarch64' in machine):
    raise RuntimeError(f"Unsupported platform: {system} {machine}. This module requires macOS on Apple Silicon.")

# Make sure IDA kernel is loaded (idapro python or inside IDA)
check_dependencies("libidalib.dylib")

# Load the shared library
load_shared_lib(os.path.join(os.path.dirname(__file__), "libida_domain.dylib"))

# On macOS, also preload the _ida_domain.so file to avoid search path issues
load_shared_lib(os.path.join(os.path.dirname(__file__), "_ida_domain.so"))

# Import ida_domain SWIG module
from .ida_domain import *

