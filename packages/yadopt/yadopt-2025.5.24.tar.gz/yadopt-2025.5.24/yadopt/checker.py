"""
Check argument vector based on the parsed arguments and options.
"""

# Declare published functions and variables.
__all__ = ["check_user_input"]

# Import custom modules.
from .argvec import ArgVector
from .dtypes import ArgsInfo, OptsInfo
from .errors import YadOptError


def check_user_input(argvec: ArgVector, args: ArgsInfo, opts: OptsInfo) -> bool:
    """
    Check all user input variables are defined in arguments/options section.

    Args:
        argvec  (ArgVector) : User input info.
        docinfo (DocStrInfo): Parse result of arguments/options section.

    Returns:
        (bool): Returns True if all checks are passed.
    """
    # Generate a set of all available argument names.
    available_args: set[str] = {item.name for item in args.items}

    # Generate a set of all available option names.
    available_opts  = {item.name     for item in opts.items}
    available_opts |= {item.name_alt for item in opts.items if item.name_alt is not None}

    # Check all user input is defined in argument sections.
    for name, value in argvec.args.items():
        if name not in available_args:
            raise YadOptError["usage_arg_mismatch"](name, value)

    # Check all user input is defined in option sections.
    for name, value in argvec.opts.items():
        if name not in available_opts:
            raise YadOptError["usage_arg_mismatch"](name, value)

    return True


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
