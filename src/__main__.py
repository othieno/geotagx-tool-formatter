# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project formatter tool.
#
# Author: Jeremy Othieno (j.othieno@gmail.com)
#
# Copyright (c) 2017 UNITAR/UNOSAT
#
# The MIT License (MIT)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
import argparse
from geotagx_validator.helper import check_arg_type, print_exception

def main():
    """Executes the application.
    """
    import sys
    sys.exit(run(get_argparser().parse_args(sys.argv[1:])))


def run(arguments):
    """Executes the application with the specified command-line arguments.

    Args:
        arguments (argparse.Namespace): A set of command-line arguments.

    Returns:
        int: 0 if validation was successful, 1 otherwise.
    """
    from geotagx_validator.helper import sanitize_paths, deserialize_configuration_set
    from core import format_configuration_set
    from helper import serialize_configuration_set

    exit_code = 0
    try:
        if not arguments.quiet:
            _setup_logging(arguments.verbose)

        for path in sanitize_paths(arguments.paths):
            configuration_set = deserialize_configuration_set(path)
            serialize_configuration_set(
                format_configuration_set(configuration_set),
                path,
                overwrite=True
            )
            print "The project located at '{}' was successfully formatted.".format(path)
    except Exception as e:
        print_exception(e, arguments.verbose)
        exit_code = 1
    finally:
        return exit_code


def get_argparser(subparsers=None):
    """Constructs the application's command-line argument parser. The formatter tool
    is a standalone program but also a part of the GeoTag-X toolkit which means
    that its arguments can be sub-commands to a specific command. For more information,
    check out: https://docs.python.org/2/library/argparse.html#sub-commands

    Args:
        subparsers (argparse._SubParsersAction): If specified, the argument parser is
            created as a parser for a program command, and not the actual program.

    Returns:
        argparse.ArgumentParser: A command-line argument parser instance.

    Raises:
        TypeError: If the subparsers argument is not a NoneType or an argparse._SubParsersAction instance.
    """
    check_arg_type(get_argparser, "subparsers", subparsers, (argparse._SubParsersAction, type(None)))

    parser = None
    parser_arguments = {
        "description": "A tool that formats a GeoTag-X project's configurations.",
        "add_help": False,
    }
    if subparsers is None:
        parser = argparse.ArgumentParser(prog="geotagx-formatter", **parser_arguments)
    elif isinstance(subparsers, argparse._SubParsersAction):
        parser = subparsers.add_parser("format", help="Format your GeoTag-X projects.", **parser_arguments)
        parser.set_defaults(run=run)

    options = parser.add_argument_group("OPTIONS")
    options.add_argument("-h", "--help", action="help", help="Display this help and exit.")
    options.add_argument("-q", "--quiet", action="store_true", help="Suppress all warnings.")
    options.add_argument("-v", "--verbose", action="store_true", help="Detail the actions being performed.")
    options.add_argument("-V", "--version", action="version", help="Display version information and exit.", version=_version())

    parser.add_argument("paths", metavar="PATH", nargs="+")

    return parser


def _version():
    """Returns the tool's version string."""
    from __init__ import __version__
    return "GeoTag-X Project Formatter Tool v%s, Copyright (C) 2017 UNITAR/UNOSAT." % __version__


def _setup_logging(verbose=False):
    """Sets up logging.

    Args:
        verbose (bool): If set to True, the build tool will log most of its operations, even the mundane.
    """
    import logging
    logging_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging_level)


if __name__ == "__main__":
    main()
