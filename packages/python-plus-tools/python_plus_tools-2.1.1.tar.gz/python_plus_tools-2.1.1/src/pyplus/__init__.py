'''
The python Plus - Pyplus
================
the python's plus library.\n
'''

from .core import *
from .tools import *
from . import tools, science
if get_config("library", {"autoCreateLocalConfig": True}).get("pyscience", True):
    from advancedlib import _all as advancedlib
elif get_config("import", {"advancedlib" : True}).get("advancedlib", True):
    from advancedlib import _no_math

__version__ = get_version("main")