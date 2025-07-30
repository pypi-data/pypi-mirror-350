# fibos/utils.py
import os
import platform
from ctypes import CDLL
import shutil
import subprocess
import sys

def verify_gcc():
    gcc_path = shutil.which("gcc")
    
    if not gcc_path:
        raise ImportError("GCC not found in PATH. This may mean that GCC is not installed or that the PATH is not configured correctly.")
    
def _load_library(name):
    package_dir = os.path.abspath(os.path.dirname(__file__))
    if platform.system() == 'Windows':
        verify_gcc()
        lib_name = f'{name}.dll'
    elif platform.system() == 'Darwin':
        lib_name = f'{name}.dylib'
    else:
        lib_name = f'{name}.so'
    lib_path = os.path.join(package_dir, lib_name)
    if not os.path.exists(lib_path):
        raise ImportError(f"Library not found: {lib_path}")
    return CDLL(lib_path)