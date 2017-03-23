# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project formatter tool.
# It contains formatters for various components of a project configuration.
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
import geotagx_validator.project as validator

def format_project_configuration(configuration, validate_configuration=True):
    """Formats the specified project configuration.

    Args:
        configuration (dict): A project configuration to format.

    Raises:
        TypeError: If the configuration argument is not a dictionary, or
            validate_configuration is not a boolean.
        ValueError: If the specified configuration is not a valid project configuration.
    """
    check_arg_type(format_project_configuration, "configuration", configuration, dict)
    check_arg_type(format_project_configuration, "validate_configuration", validate_configuration, bool)

    if validate_configuration:
        valid, message = validator.is_project_configuration(configuration)
        if not valid:
            raise ValueError(message)

    formatters = {
        "name": format_project_name,
        "description": format_project_description,
        "repository": format_project_repository,
    }
    for key in configuration:
        formatter = formatters.get(key)
        if formatter:
            configuration[key] = formatter(configuration[key], False)

    return configuration


def format_project_name(name, validate_name=True):
    raise NotImplementedError


def format_project_description(description, validate_description=True):
    raise NotImplementedError


def format_project_repository(repository, validate_repository=True):
    raise NotImplementedError
