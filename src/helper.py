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
