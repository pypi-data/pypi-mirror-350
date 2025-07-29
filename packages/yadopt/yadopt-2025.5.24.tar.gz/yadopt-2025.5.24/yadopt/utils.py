"""
Collection of utility functions.
"""

# Import standard libraries.
import pprint
import re
import string
import textwrap

# For type hinting.
from collections.abc import Generator
from typing          import Any


def get_default(description: str) -> tuple[str, str | None]:
    """
    Get default value.

    Args:
        description (str): Description message contains default value.

    Returns:
        (tuple): A tuple of (rest of description, default value string).

    Examples:
        >>> get_default("sample description [default: value]")
        ('sample description', 'value')
    """
    default_pattern: str = r"^(.*)\s+\[default:\s*([^\]]+)\]\s*$"

    # Search default string.
    m: re.Match[str] | None = re.fullmatch(default_pattern, description)

    # Returns entire description and None if no default string found.
    if m is None:
        return (description.strip(), None)

    # Otherwise, returns rest of descriptions and default string.
    return (m.group(1).strip(), m.group(2).strip())


def get_error_marker(line: str, token: str) -> str:
    """
    Args:
        line  (str): Entire line.
        token (str): Target token.

    Returns:
        (str): Error marker string like.

    Examples:
        >>> get_error_marker("this is a pen", "pen")
        '          ^^^'
        >>> get_error_marker("this is a pen", "pencil")
        '             '
    """
    pos: int = line.find(token)

    # Returns whitespace if the token not found in the line.
    if pos < 0:
        return " " * len(line)

    return " " * pos + "^" * len(token) + " " * (len(line) - len(token) - pos)


def get_section_lines(docstr: str, section_name: str) -> Generator[str]:
    """
    Parse docstring and split it to sections.

    Args:
        docstr       (str): Input docstring.
        section_name (str): Target section name.

    Returns:
        (Generator[str]): Lines of specified section.
    """
    def get_indent(text: str) -> str:
        """
        Get indent of the given text.
        """
        match: re.Match | None = re.match(r"^(\s*)", text)
        return match.group(1) if (match is not None) else ""

    # Initialize the section type.
    is_target_section: bool = False

    # Initialize output lines.
    lines: list[str] = []

    for line in docstr.split("\n"):

        # Strip unnecessary whitespaces from right.
        line = line.rstrip()

        # Update the section flag (colon expression).
        if line.endswith(":"):
            is_target_section = line[:-1].lower().endswith(section_name)

        # Update the section flag (bracket expression).
        elif line.startswith("[") and line.endswith("]"):
            is_target_section = line[1:-1].lower().endswith(section_name)

        # Returns the current line if the line is inside the target section.
        elif is_target_section and line.strip() and (line[0] in string.whitespace):
            lines.append(line)

    # Do nothing if the target section is empty.
    if len(lines) == 0:
        return (line for line in lines)

    # Get indent of the target section.
    indent: str = get_indent(lines[0])

    # Process multiple line.
    while lines:

        line = lines.pop(0)

        # Appent lines if the indent does not match.
        while lines and (get_indent(lines[0]) != indent):
            line += " " + lines.pop(0).lstrip()

        yield line


def strtobool(s: str) -> bool | None:
    """
    Convert the given string to bool instance. The function `bool(...)` is not suitable
    for this purpose, because `bool("False")` returns `True`.

    Args:
        s (str): Input string.

    Returns:
        (bool | None): Corresponding boolean value.

    Examples:
        >>> strtobool("True")
        True
        >>> strtobool("False")
        False
    """
    if s.lower() in {"t", "true", "y", "yes", "on", "1"}:
        return True
    if s.lower() in {"f", "false", "n", "no", "off", "0"}:
        return False
    return None


def retokenize(argv: list[str]) -> Generator[str]:
    """
    Tokenize the argument vector.

    Args:
        argv (list[str]): Argument vector to be tokenized.

    Returns:
        (Generator[str]): Re-tokenized tokens.

    Examples:
        >>> list(retokenize(["A=a", "B=b"]))
        ['A', 'a', 'B', 'b']
    """
    for token in argv:
        yield from token.split("=", maxsplit=1)


def repr_dataclass_items(name: str, data: Any) -> str:
    """
    String expression of dataclass that has items.

    Args:
        name (str): Name of the dataclass.
        data (Any): Instance of dataclass.
    """
    # Header of the string expression.
    text: str = f"{name}:\n"

    # Append item info.
    for idx, item in enumerate(data.items):
        text += f" |-({idx:02d}) " + textwrap.indent(pprint.pformat(item), " |      ")[8:] + "\n"

    # Append docstring info.
    text += f" |-(docstr) str of length {len(data.docstr)}"

    return text.strip()


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
