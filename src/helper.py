# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project formatter tool.
# It contains miscellaneous helper functions.
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
from geotagx_validator.helper import check_arg_type

def to_json_string(dictionary, compress=False):
    """Converts the specified dictionary into a string in JSON format.

    Args:
        dictionary (dict): A dictionary to convert.
        compress (bool): If set to True, the string will be compressed
            as much as possible.

    Returns:
        basestring: A string in JSON format.

    Raises:
        TypeError: If dictionary argument is not a dict, or compress is not a bool.
    """
    check_arg_type(to_json, "dictionary", dictionary, dict)
    check_arg_type(to_json, "compress", compress, bool)

    from json import dumps
    output = dumps(
        dictionary,
        indent=0 if compress else 4,
        separators=(",", ":" if compress else ": "),
        encoding="UTF-8",
        ensure_ascii=False
    ).encode("UTF-8")
    return output.replace("\n", "") if compress else output


def normalize_string(string, language_code):
    """Normalizes the specified string.

    The normalization process creates a dictionary that contains the specified string mapped to
    the given language code.

    Args:
        string (str): A string to normalize.
        language_code (str): A language code that the string will be associated with.

    Returns:
        dict: The normalized string.

    Raises:
        TypeError: If either the string or language_code argument is not a basestring.
        ValueError: If the specified language code is not valid.
    """
    check_arg_type(normalize_string, "string", string, basestring)
    check_arg_type(normalize_string, "language_code", language_code, basestring)

    from geotagx_validator.helper import is_language_code

    if not is_language_code(language_code):
        raise ValueError("'{}' is not a valid language code.".format(language_code))

    return {language_code: string}


def serialize_configuration_set(configuration_set, path, overwrite=False):
    """Writes each of the specified configurations to their respective JSON files.

    Args:
        configuration_set (dict): A set of configurations.
        path (str): A path to the directory where the configuration files will
            be written.
        overwrite (bool): If set to True, any pre-existing configuration files
            will be overwritten.

    Raises:
        TypeError: If the configuration_set argument is not a dictionary, path is not a
            basestring, or overwrite is not a boolean.
        ValueError: If the specified configuration set is not valid.
        IOError: If the specified path does not lead to a writable directory.
    """
    check_arg_type(serialize_configuration_set, "configuration_set", configuration_set, dict)
    check_arg_type(serialize_configuration_set, "path", path, basestring)
    check_arg_type(serialize_configuration_set, "overwrite", overwrite, bool)

    from geotagx_validator.core import is_configuration_set
    from geotagx_validator.helper import is_directory
    import os

    valid, message = is_configuration_set(configuration_set)
    if not valid:
        raise ValueError(message)
    elif not is_directory(path, check_writable=True):
        raise IOError("The path '{}' is not a writable directory. Please make sure you have the appropriate access permissions.".format(path))

    filename = {
        "project": os.path.join(path, "project.json"),
        "task_presenter": os.path.join(path, "task_presenter.json"),
        "tutorial": os.path.join(path, "tutorial.json"),
    }
    if not overwrite and any(os.path.isfile(f) for f in filename.values()):
        raise IOError("The directory '{}' already contains a project (project.json), task presenter (task_presenter.json) and/or a tutorial (tutorial.json) configuration. To overwrite either, set the '-f' or '--force' flag.".format(path))

    for key, configuration in configuration_set.iteritems():
        with open(filename[key], "w") as file:
            file.write(to_json_string(configuration))
