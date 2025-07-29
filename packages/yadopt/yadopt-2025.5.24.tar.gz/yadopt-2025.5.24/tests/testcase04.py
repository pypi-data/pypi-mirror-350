"""
Testcase 4: Error checks.
"""

class Testcase04_01:
    """
    Error check - usage and arguments not match

    Usage:
        sample.py <arg_mistake> [-a NAME]

    Arguments:
        arg       Input argument.

    Options:
        -a name   Option with value.
    """
    commands = [
        "sample.py arg -a val",
    ]

    @staticmethod
    def check(index, args, command):
        """
        Checker function for testcases.

        Args:
            index   (int)       : Index of testcases.
            args    (YadOptArgs): Parsed command line arguments.
            command (str)       : Command string (source of `args`).
        """
        if index == 0:
            assert args.__class__.__name__ == "YadOptErrorUsageArgMismatch"
            assert str(args).strip().startswith("Error summary:\n  ")

        else:
            raise ValueError(f"Check function for index={index} not found")


class Testcase04_02:
    """
    Error check - usage parse

    Usage:
        sample.py (-h|--help)

    Options:
        -h, --help   Show help message.
    """
    commands = [
        "sample.py --help",
    ]

    @staticmethod
    def check(index, args, command):
        """
        Checker function for testcases.

        Args:
            index   (int)       : Index of testcases.
            args    (YadOptArgs): Parsed command line arguments.
            command (str)       : Command string (source of `args`).
        """
        if index == 0:
            assert args.__class__.__name__ == "YadOptErrorUsageParse"
            assert str(args).strip().startswith("Error summary:\n  ")

        else:
            raise ValueError(f"Check function for index={index} not found")


class Testcase04_03:
    """
    Error check - invalid constants

    Usage:
        sample.py subcmd <arg> bad_constant_token

    Arguments:
        arg    Input argument.
    """
    commands = [
        "sample.py argument",
    ]

    @staticmethod
    def check(index, args, command):
        """
        Checker function for testcases.

        Args:
            index   (int)       : Index of testcases.
            args    (YadOptArgs): Parsed command line arguments.
            command (str)       : Command string (source of `args`).
        """
        if index == 0:
            assert args.__class__.__name__ == "YadOptErrorInvalidConstant"
            assert str(args).strip().startswith("Error summary:\n  ")

        else:
            raise ValueError(f"Check function for index={index} not found")


class Testcase04_04:
    """
    Error check - user input not match

    Usage:
        sample.py subcmd <arg>

    Arguments:
        arg    Input argument.
    """
    commands = [
        "sample.py cmdsub argument",
    ]

    @staticmethod
    def check(index, args, command):
        """
        Checker function for testcases.
    
        Args:
            index   (int)       : Index of testcases.
            args    (YadOptArgs): Parsed command line arguments.
            command (str)       : Command string (source of `args`).
        """
        if index == 0:
            assert args.__class__.__name__ == "YadOptErrorValidUsageNotFound"
            assert str(args).strip().startswith("Error summary:\n  ")

        else:
            raise ValueError(f"Check function for index={index} not found")


class Testcase04_05:
    """
    Error check - mandatory arguments

    Usage:
        cmd <config_path>
        cmd --help

    Arguments:
        config_path    Path to config

    Other options:
        -h, --help     Show this help message and exit.
    """
    commands = [
        "sample.py",
        "sample.py --help",
    ]

    @staticmethod
    def check(index, args, command):
        """
        Checker function for testcases.

        Args:
            index   (int)       : Index of testcases.
            args    (YadOptArgs): Parsed command line arguments.
            command (str)       : Command string (source of `args`).
        """
        if index == 0:
            assert args.__class__.__name__ == "YadOptErrorValidUsageNotFound"
            assert str(args).strip().startswith("Error summary:\n  ")

        elif index == 1:
            assert isinstance(args, SystemExit)

        else:
            raise ValueError(f"Check function for index={index} not found")


class Testcase04_06:
    """
    Error check - mandatory options

    Usage:
        sample.py --opt VALUE
        sample.py --help

    Options:
        --opt VALUE    Option with value.
        -h, --help     Show this help message and exit.
    """
    commands = [
        "sample.py",
        "sample.py --help",
    ]

    @staticmethod
    def check(index, args, command):
        """
        Checker function for testcases.

        Args:
            index   (int)       : Index of testcases.
            args    (YadOptArgs): Parsed command line arguments.
            command (str)       : Command string (source of `args`).
        """
        if index == 0:
            assert args.__class__.__name__ == "YadOptErrorValidUsageNotFound"
            assert str(args).strip().startswith("Error summary:\n  ")

        elif index == 1:
            assert isinstance(args, SystemExit)

        else:
            raise ValueError(f"Check function for index={index} not found")


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker
