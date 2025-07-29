"""
Initialize yadopt module.
"""

# Import functions.
from .yadopt import parse, wrap, to_dict, to_namedtuple, save, load
from .dtypes import YadOptArgs

# Version information.
__version__ = "2025.05.24"

# Declare published functions and variables.
__all__ = ["parse", "wrap", "to_dict", "to_namedtuple", "save", "load", "YadOptArgs", "__version__"]

# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
