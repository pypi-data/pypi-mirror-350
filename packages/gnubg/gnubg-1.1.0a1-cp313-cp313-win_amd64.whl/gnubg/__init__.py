"""""" # start delvewheel patch
def _delvewheel_patch_1_10_1():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'gnubg.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_10_1()
del _delvewheel_patch_1_10_1
# end delvewheel patch

import os
from pathlib import Path

if os.name == "nt" and hasattr(os, "add_dll_directory"):
    pkgdir = Path(__file__).parent
    if pkgdir.is_dir():
        os.add_dll_directory(str(pkgdir))

# Import your compiled extension module
from .gnubg import *

# Optional: Expose a namespace
__all__ = [name for name in globals().keys() if not name.startswith("_")]
