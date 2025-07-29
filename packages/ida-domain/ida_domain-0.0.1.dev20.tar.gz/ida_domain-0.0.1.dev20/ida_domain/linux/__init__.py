import os
import platform
from .. import load_shared_lib, check_dependencies

# Verify the current operating system is supported
# This module only works on Linux platforms
system = platform.system()
if system != "Linux":
  raise RuntimeError(f"Unsupported platform: {system}")

# Make sure IDA kernel is loaded (idapro python or inside IDA)
check_dependencies("libidalib.so")

# Load the shared library
load_shared_lib(os.path.join(os.path.dirname(__file__), "libida_domain.so"))

# Import ida_domain SWIG module
from .ida_domain import *