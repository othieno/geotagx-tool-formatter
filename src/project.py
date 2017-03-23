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
        validate_configuration (bool): If set to True, the specified configuration
            will be validated before it's processed.

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
    """Formats the specified project name.

    Formatting a project name will simply remove any leading and trailing whitespace.

    Args:
        name (str): A project name to format.
        validate_name (bool): If set to True, the specified project name will be
            validated before it's processed.

    Returns:
        basestring: The formatted project name.

    Raises:
        TypeError: If the name argument is not a basestring instance, or
            validate_name is not a boolean.
        ValueError: If the specified name is not valid.
    """
    check_arg_type(format_project_name, "name", name, basestring)
    check_arg_type(format_project_name, "validate_name", validate_name, bool)

    if validate_name:
        valid, message = validator.is_project_name(name)
        if not valid:
            raise ValueError(message)

    return name.strip()


def format_project_description(description, validate_description=True):
    """Formats the specified project description.

    Formatting a project description will simply remove any leading and trailing
    whitespace.

    Args:
        description (str): A project description to format.
        validate_description (bool): If set to True, the specified project
            description will be validated before it's processed.

    Returns:
        basestring: The formatted project description.

    Raises:
        TypeError: If the description argument is not a basestring instance, or
            validate_description is not a boolean.
        ValueError: If the specified description is not valid.
    """
    check_arg_type(format_project_description, "description", description, basestring)
    check_arg_type(format_project_description, "validate_description", validate_description, bool)

    if validate_description:
        valid, message = validator.is_project_description(description)
        if not valid:
            raise ValueError(message)

    return description.strip()


def format_project_repository(repository, validate_repository=True):
    """Formats the specified project repository.

    Formatting a project repository will simply remove any leading and trailing
    whitespace.

    Args:
        repository (str): A project repository to format.
        validate_repository (bool): If set to True, the specified project
            repository will be validated before it's processed.

    Returns:
        basestring: The formatted project repository.

    Raises:
        TypeError: If the repository argument is not a basestring instance, or
            validate_repository is not a boolean.
        ValueError: If the specified repository is not valid.
    """
    check_arg_type(format_project_repository, "repository", repository, basestring)
    check_arg_type(format_project_repository, "validate_repository", validate_repository, bool)

    if validate_repository:
        valid, message = validator.is_project_repository(repository)
        if not valid:
            raise ValueError(message)

    return repository.strip()
