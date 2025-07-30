'''
This is a moudle for python unit calculation
Use this moudle,plese write: 
`Unit()` or other class in this moudle.
If you want to create new unit class,please use: 
'''

import operator
from advancedlib import operator as operators

from pathlib import Path
from os import getenv

from . import units
from . import pyscience

from toml import load 

try:
    o1 = open(Path(getenv("appdata"),"xystudio", "pyplus", "config.toml"))
    o2 = open(Path(".xystudio", "pyplus", "config.toml").absolute())

    config = (load(o1) | load(o2))

    o1.close()
    o2.close()
except FileNotFoundError:
    config = {}

if config.get("import", {"pyscience" : True}).get("pyscience", True):
    from . import pyscience
    from . import pyscience as science
elif config.get("import", {"math" : False}).get("math", False):
    from advancedlib import math

del load, getenv, Path

__all__ = [
    "units", "pyscience", "science", "operators", "operator"
]
