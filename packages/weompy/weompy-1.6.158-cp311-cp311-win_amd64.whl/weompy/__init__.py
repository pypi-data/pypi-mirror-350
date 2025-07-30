import os
import sys
import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .weompy import *

pleoraDirectory = f"{os.environ['ProgramFiles']}\\Common Files\\Pleora\\eBUS SDK"
if os.path.exists(pleoraDirectory):
    os.add_dll_directory(pleoraDirectory)

packageDirectory = os.path.dirname(__file__)
sys.path.append(packageDirectory)

sys.modules[__name__] = importlib.import_module(f"weompy.weompy", package=__name__)
