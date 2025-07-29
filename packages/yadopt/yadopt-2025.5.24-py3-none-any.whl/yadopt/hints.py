"""
Assign types based on type hinting string.
"""

# Declare published functins and variables.
__all__ = ["auto_type", "type_hint"]

# Import standard libraries.
import ast
import pathlib

# For type hinting.
from collections.abc import Callable

# Import custom modules.
from .argvec import ArgVector
from .dtypes import ArgsInfo, OptsInfo
from .utils  import strtobool

# Define a map from data type string to data type.
DTYPE_HINTS: dict[str, Callable] = {
    # Booleans.
    "bool": strtobool, "boolean": strtobool,
    # Integers.
    "int": int, "integer": int,
    # Floating numbers.
    "flt": float, "float": float,
    # Strings.
    "str": str, "string": str,
    # Path.
    "path": pathlib.Path
}


def auto_type(value: str) -> int | float | str | pathlib.Path:
    """
    Automatically determine the data type.
    """
    try:
        return ast.literal_eval(value)
    except ValueError:
        return str(value)


def fill_default_values(argvec: ArgVector, opts: OptsInfo) -> ArgVector:
    """
    Fill default values.

    Args:
        argvec (ArgVector): Parsed user input.
        opts   (OptsInfo) : Options information of docstring.

    Returns:
        (ArgVector): Parsed user input.
    """
    for opt_entry in opts.items:
        if opt_entry.name not in argvec.opts:
            argvec.opts[opt_entry.name] = opt_entry.default

    return argvec


def type_hint(argvec: ArgVector, args: ArgsInfo, opts: OptsInfo, type_fn: Callable, fill_default: bool) -> None:
    """
    Apply type hints.

    Args:
        argvec       (ArgVector): Parsed user input.
        args         (ArgsInfo) : Arguments information of docstring.
        opts         (OptsInfo) : Options information of docstring.
        type_fn      (Callable) : A function that assign types to values.
        fill_default (bool)     : Fill default values if True.
    """
    def set_typed_value(val_dict: dict, args_or_opts: ArgsInfo | OptsInfo, type_fn: Callable) -> None:
        """
        Get typed value.
        """
        for entry in args_or_opts.items:

            # Do nothing if the entry is not in the value dictionary.
            if entry.name not in val_dict:
                continue

            # If the value is None, not necessary to assign type.
            if val_dict[entry.name] is None:
                continue

            # Get type function.
            fn = DTYPE_HINTS.get(entry.dtype_str, auto_type) if (type_fn is auto_type) else type_fn

            # If the target value is list of string, then apply the type function
            # to the list contents.
            if isinstance(val_dict[entry.name], list):
                val_dict[entry.name] = [fn(v) for v in val_dict[entry.name]]

            # Else, normaly apply type function to the value.
            else:
                val_dict[entry.name] = fn(val_dict[entry.name])

    # Fill deafult values to the user input.
    if fill_default:
        fill_default_values(argvec, opts)

    # Assign type to the values.
    set_typed_value(argvec.args, args, type_fn)
    set_typed_value(argvec.opts, opts, type_fn)


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
