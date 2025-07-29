from __future__ import print_function
from __future__ import absolute_import
import traceback

from .inheritance import *

try:
    from .CopyCatDS import CopyCatDS, CopyCatDSClass, CopyCatServer
except:
    print("Unable to import fandango.interface.CopyCatDS")
    print(traceback.format_exc())
