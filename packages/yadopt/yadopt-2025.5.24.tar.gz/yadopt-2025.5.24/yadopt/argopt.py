"""
Docstring parser.
"""

# Declare published functions and variables.
__all__ = ["parse_docstr_args", "parse_docstr_opts"]

# Import standard libraries.
import re

# Import custom modules.
from .dtypes   import ArgEntry, ArgsInfo, OptEntry, OptsInfo
from .errors   import YadOptError
from .hints    import DTYPE_HINTS
from .matchers import match_arg, match_opt
from .utils    import get_default, get_section_lines


def parse_docstr_args(docstr: str) -> ArgsInfo:
    """
    Parse docstring and returns arguments info.

    Args:
        docstr (str): Docstring to be parsed.

    Returns:
        (ArgsInfo): Arguments information of docstring.
    """
    # Get arguments information.
    items: list[ArgEntry] = []
    for item in map(parse_line, get_section_lines(docstr, "arguments")):
        if isinstance(item, ArgEntry):
            items.append(item)

    # Get arguments sections of docstring.
    docstr_args: str = "Arguments:\n" + "\n".join(get_section_lines(docstr, "arguments"))

    return ArgsInfo(items, docstr_args)


def parse_docstr_opts(docstr: str) -> OptsInfo:
    """
    Parse docstring and returns options info.

    Args:
        docstr (str): Docstring to be parsed.

    Returns:
        (OptsInfo): Options information of docstring.
    """
    # Get options information.
    items: list[OptEntry] = []
    for item in map(parse_line, get_section_lines(docstr, "options")):
        if isinstance(item, OptEntry):
            items.append(item)

    # Get options sections of docstring.
    docstr_opts: str = "Options:\n" + "\n".join(get_section_lines(docstr, "options"))

    return OptsInfo(items, docstr_opts)


def parse_line(line: str) -> ArgEntry | OptEntry | None:
    """
    Parse an entry of argument and option sections.

    Args:
        line (str): Input line.

    Returns:
        (ArgEntry | OptEntry | None): Parsed result.

    Examples:
        >>> parse_line("  -o   msg")
        OptEntry(name='o', name_alt=None, has_value=False, dtype_str='bool', desc='msg', default='False')
        >>> parse_line("  --opt   msg")
        OptEntry(name='opt', name_alt=None, has_value=False, dtype_str='bool', desc='msg', default='False')
        >>> parse_line("  -o, --opt   msg")
        OptEntry(name='opt', name_alt='o', has_value=False, dtype_str='bool', desc='msg', default='False')
        >>> parse_line("  -o, --opt INT   msg")
        OptEntry(name='opt', name_alt='o', has_value=True, dtype_str='int', desc='msg', default=None)
        >>> parse_line("  arg1 msg")
        ArgEntry(name='arg1', dtype_str='unknown', desc='msg', default=None)
        >>> parse_line("  arg1  (INT) msg  [default: 10]")
        ArgEntry(name='arg1', dtype_str='int', desc='msg', default='10')
    """
    # Try to parse as argument line.
    (outputs, description, _) = match_arg(line)

    if len(outputs) > 0:

        # Get matched argument name.
        name = outputs[0]

        # The name should not be None.
        if not isinstance(name, str):
            raise YadOptError["internal_error"]()

        # Get data type.
        (dtype_str, description) = get_dtype_str(name, description)

        # Get default value.
        (description, default) = get_default(description)

        return ArgEntry(name, dtype_str, description, default)

    # Try to parse as option line.
    (outputs, description, has_value) = match_opt(line)

    if len(outputs) > 0:

        # Unpack matched results.
        name, name_alt, value = outputs

        # The name should be a string.
        if not isinstance(name, str):
            raise YadOptError["internal_error"]()

        # Get data type.
        (dtype_str, description) = get_dtype_str(value, description)

        # Get default value.
        (description, default) = get_default(description)

        # If the option has no value (i.e. has_value is False),
        # then the data type and defualt value should be bool and False, respectively.
        if has_value is False:
            (dtype_str, default) = ("bool", "False")

        return OptEntry(name, name_alt, has_value, dtype_str, description, default)

    return None


def get_dtype_str(var_name: str | None, description: str) -> tuple[str, str]:
    """
    Returns appropriate data type.

    Args:
        var_name (str): Variable name.

    Returns:
        (tuple): A tuple of appropriate Python data type and the rest of description.

    Examples:
        >>> get_dtype_str("x_int", "Integer value.")
        ('int', 'Integer value.')
        >>> get_dtype_str("x", "(INT) Integer value.")
        ('int', 'Integer value.')
    """
    # Try to get type from the description.
    if (m := re.match(r"^\s*\((\w+)\)\s*", description)) is not None:

        # Get matched data type name and description.
        dtype_str = m.group(1).strip().lower()
        description = description[len(m.group(0)):]

        # If the matched data type name is valid, then return them.
        if dtype_str in DTYPE_HINTS:
            return (dtype_str, description)

    # Returns unknown type if variable name is None.
    if var_name is None:
        return ("unknown", description)

    # Try to get type from the variable name.
    for key in DTYPE_HINTS:
        if var_name.lower().endswith(key):
            return (key, description)

    return ("unknown", description)


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
