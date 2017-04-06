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
from geotagx_validator.helper import check_arg_type

def format_configuration_set(configuration_set, validate_configuration_set=True):
    """Formats the specified set of project configurations.

    Args:
        configurations (dict): A dictionary containing a set of configurations to format.
        validate_configuration_set (bool): If set to True, the configurations will be
            validated before they are processed.

    Returns:
        dict: A formatted set of project configurations.

    Raises:
        TypeError: If the configuration_set argument is not a dictionary.
        ValueError: If the specified configuration set is invalid.
    """
    check_arg_type(format_configuration_set, "configuration_set", configuration_set, dict)
    check_arg_type(format_configuration_set, "validate_configuration_set", validate_configuration_set, bool)

    from project import format_project_configuration
    from task_presenter import format_task_presenter_configuration
    from tutorial import format_tutorial_configuration
    from geotagx_validator.core import is_configuration_set

    if validate_configuration_set:
        valid, message = is_configuration_set(configuration_set)
        if not valid:
            raise ValueError(message)

    formatters = {
        "project": format_project_configuration,
        "task_presenter": format_task_presenter_configuration,
        "tutorial": lambda c, v: format_tutorial_configuration(c, configuration_set["task_presenter"], v, False),
    }
    for key, configuration in configuration_set.iteritems():
        formatter = formatters.get(key, None)
        if formatter:
            configuration = formatter(configuration, False)

    return configuration_set
