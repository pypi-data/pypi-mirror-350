"""
Collections of data types and classes.
"""

# Declare published functions and variables.
__all__ = ["ArgEntry", "ArgsInfo", "OptEntry", "OptsInfo", "UsageOpt", "UsageEntry", "ArgVector", "YadOptArgs"]

# Import standard libraries.
import dataclasses

# For type hinting.
from typing import Any

# Import custom modules.
from .utils import repr_dataclass_items


############################################################
# Data types for parsing docstring
############################################################

@dataclasses.dataclass
class ArgEntry:
    """
    Parsed result of argument definition in docstring.
    """
    name     : str         # Option name.
    dtype_str: str         # Data type string.
    desc     : str         # Description of this option.
    default  : str | None  # Default value (string).


@dataclasses.dataclass
class ArgsInfo:
    """
    Arguments information of docstring.
    """
    items : list[ArgEntry]  # Arguments information.
    docstr: str             # Arguments section of docstring.

    def __str__(self) -> str:
        return repr_dataclass_items("ArgsInfo", self)


@dataclasses.dataclass
class OptEntry:
    """
    Parsed result of option definition in docstring.
    """
    name     : str         # Option name.
    name_alt : str | None  # Alternative option name.
    has_value: bool        # Number of arguments.
    dtype_str: str         # Data type string.
    desc     : str         # Description of this option.
    default  : str | None  # Default value (string).


@dataclasses.dataclass
class OptsInfo:
    """
    Options information of docstring.
    """
    items : list[OptEntry]  # Options information.
    docstr: str             # Options section of docstring.

    def __str__(self) -> str:
        return repr_dataclass_items("OptsInfo", self)


@dataclasses.dataclass
class UsageOpt:
    """
    Parsed result of usage definition in docstring.
    """
    name     : str   # Option name.
    has_value: bool  # True if this option has a value.
    required : bool  # True if this option is mandatory.


@dataclasses.dataclass
class UsageEntry:
    """
    Parsed result of usage definition in docstring.
    """
    pres: list[str]       # Preceding tokens.
    args: list[str]       # Argument tokens.
    opts: list[UsageOpt]  # Option tokens.


############################################################
# Data types for parsing argument vector
############################################################

@dataclasses.dataclass
class ArgVector:
    """
    Information of user input.
    """
    pres: dict[str, bool]
    args: dict[str, Any]
    opts: dict[str, str|None]

    def __str__(self):
        text  = "ArgVector:\n"
        text += " |- pres = " + str(self.pres) + "\n"
        text += " |- args = " + str(self.args) + "\n"
        text += " |- opts = " + str(self.opts) + "\n"
        return text.strip()


############################################################
# A class to store parsed results
############################################################

class YadOptArgs:
    """
    Command line arguments parsed by YadOpt.
    """
    def __normal_dict__(self) -> dict:
        """
        Returns "normal" dictionary that contains keys not starting with the underscore.
        """
        return {key:value for key, value in self.__dict__.items() if not key.startswith("_")}

    def __repr__(self) -> str:
        """
        Representation of this class.
        """
        contents: str = ", ".join(f"{key}={val}" for key, val in self.__normal_dict__().items())
        return f"{self.__class__.__name__}({contents})"

    def __str__(self) -> str:
        """
        String expression of this class.
        """
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        """
        Returns True if equivarent.
        """
        if isinstance(other, self.__class__):
            return self.__normal_dict__() == other.__normal_dict__()

        raise NotImplementedError()


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
