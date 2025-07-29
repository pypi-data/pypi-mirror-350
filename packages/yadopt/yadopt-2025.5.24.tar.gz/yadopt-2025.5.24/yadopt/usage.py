"""
Usage line parser.
"""

# Declare published functins and variables.
__all__ = ["UsageInfo", "parse_docstr_usage"]

# Import standard libraries.
import copy
import pprint
import re
import textwrap

# For type hinting.
from collections.abc import Generator

# Import custom modules.
from .dtypes import OptsInfo, UsageOpt, UsageEntry
from .errors import YadOptError
from .utils  import get_section_lines


class UsageInfo:
    """
    Usage information of docstring.
    """
    def __init__(self, docstr: str) -> None:
        """
        Read docstring, parse usage section and store the result to myself.

        Args:
            docstr (str): Docstring to be parsed.
        """
        # Add usage information.
        self.items: list[UsageEntry] = [parse_usage_line(line) for line in get_section_lines(docstr, "usage")]

        # Add docstring information.
        self.docstr: str = "Usage:\n" + "\n".join(get_section_lines(docstr, "usage"))

    def __str__(self) -> str:
        """
        String expression of UsageInfo.
        """
        # Header of the string expression.
        text = "UsageInfo:\n"

        # Append item info.
        for idx, item in enumerate(self.items):
            text += f" |-({idx:02d}) " + textwrap.indent(pprint.pformat(item), " |      ")[8:] + "\n"

        # Append docstring info.
        text += f" |-(docstr) str of length {len(self.docstr)}"

        return text.strip()

    def expand_options(self, opts: OptsInfo) -> None:
        """
        Expand [OPTIONS] token in the usage.
        """
        for usage_entry in self.items:
            if "OPTIONS" in {opt.name for opt in usage_entry.opts}:
                usage_entry.opts = [UsageOpt(opt.name, opt.has_value, False) for opt in opts.items]


def parse_docstr_usage(docstr: str) -> UsageInfo:
    """
    Parse docstring and return usage info.

    Args:
        (UsageInfo): Parsed usage information.
    """
    return UsageInfo(docstr)


def parse_usage_line(line: str) -> UsageEntry:
    """
    Parse usage line.

    Args:
        line (str): Input usage string.

    Returns:
        (UsageEntry): Parsed result of one usage.

    Examples:
        >>> parse_usage_line("sample.py <a1> <a2> [--o1]")
        UsageEntry(pres=['sample.py'], args=['a1', 'a2'], opts=[UsageOpt(name='o1', has_value=False, required=False)])
        >>> parse_usage_line("sample.py pre <a1> [--o1 INT]")
        UsageEntry(pres=['sample.py', 'pre'], args=['a1'], opts=[UsageOpt(name='o1', has_value=True, required=False)])
        >>> parse_usage_line("sample.py pre <a1> --o1")
        UsageEntry(pres=['sample.py', 'pre'], args=['a1'], opts=[UsageOpt(name='o1', has_value=False, required=True)])
    """
    def is_arg(token):
        return token.startswith("<") and token.endswith(">")

    def is_opt(token):
        return token.strip("[]").startswith("-") or (token == "[OPTIONS]")

    # Initialize output variable.
    usage: UsageEntry = UsageEntry(pres=[], args=[], opts=[])

    # Tokenize usage string.
    tokens: list[str] = list(tokenize(line))

    # Extract preceding tokens until arguments or options appears.
    while tokens and (not is_arg(tokens[0])) and (not is_opt(tokens[0])):
        usage.pres.append(tokens.pop(0))

    # Process arguments and options.
    while tokens:

        # Get the first token.
        token: str = tokens.pop(0)

        # Case 1: Argument token.
        if token.startswith("<") and token.endswith(">"):
            usage.args.append(token.strip("<>"))

        # Case 2: Mandatory option token.
        elif token.startswith("-"):

            # Get the option name.
            opt_key: str = token.lstrip("-")

            # Case 2.1: Option with value.
            if tokens and all(not tokens[0].startswith(s) for s in ["<", "[", "-"]):

                # Get the option value (but not used now).
                _ = tokens.pop(0)

                # Add option entry.
                usage.opts.append(UsageOpt(name=opt_key, has_value=True, required=True))

            # Case 2.2: Option without value.
            else:
                usage.opts.append(UsageOpt(name=opt_key, has_value=False, required=True))

        # Case 3: Non-mandatory option token.
        elif (token.startswith("[-") and token.endswith("]")) or (token == "[OPTIONS]"):

            # Split option name and value (i.e. split by " " or "=").
            subtokens: list[str] = re.split("[ =]", token.strip("[]").lstrip("-"), maxsplit=1)

            # Add option entry.
            usage.opts.append(UsageOpt(name=subtokens[0], has_value=len(subtokens)>1, required=False))

        else:
            raise YadOptError["invalid_constant"](token, line)

    return usage


def tokenize(usage_line: str) -> Generator[str]:
    """
    Tokenize usage line. This function is focusing on the tokenization of usage pattern.
    If you prefer simple tokenization, use `shlex.split` function.

    Args:
        usage_line (str) : Usage string.
        strip      (bool): Strip whitespace from returned tokens if true.

    Returns:
        (Generator[str]): Tokens in the usage line.

    Examples:
        >>> list(tokenize("sample.py <arg1> [--opt1]"))
        ['sample.py', '<arg1>', '[--opt1]']
        >>> list(tokenize("sample.py --opt1 --opt2 val2"))
        ['sample.py', '--opt1', '--opt2', 'val2']
        >>> list(tokenize("sample.py subcmd <arg1> <arg2> [--opt1] [--opt2 val2]"))
        ['sample.py', 'subcmd', '<arg1>', '<arg2>', '[--opt1]', '[--opt2 val2]']
    """
    token_patterns: list[str] = [r"\s+",                     # Whitespace
                                 r"[\w\.-]+",                # Preceding token
                                 r"<\w+>",                   # Argument token
                                 r"<\w+\.\.\.>",             # Argument token
                                 r"\[[\w\.-]+\]",            # Optional token
                                 r"\[[\w\.-]+ [\w\.-]+\]",   # Optional token with value (space)
                                 r"\[[\w\.-]+=[\w\.-]+\]"]   # Optional token with value (equal)

    # Copy the input usage string for safety.
    usage_line = copy.deepcopy(usage_line)

    while usage_line:

        # Find matched patterns.
        for pattern in token_patterns:
            if (m := re.match(pattern, usage_line)) is not None:
                break

        # Raise an error if no pattern matched.
        if m is None:
            raise YadOptError["usage_parse"](usage_line)

        # Get matched substring.
        token: str = m.group(0)

        # Returns token as generator.
        if token.strip():
            yield token.strip()

        # Remove the returned token.
        usage_line = usage_line[len(token):]


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
