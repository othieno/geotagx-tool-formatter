# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project formatter tool.
# It contains formatters for various components of a tutorial configuration.
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
from geotagx_validator.tutorial import *

def format_tutorial_configuration(
    configuration,
    task_presenter_configuration,
    validate_configuration=True,
    validate_task_presenter_configuration=True
):
    """Formats the specified tutorial configuration.

    Args:
        configuration (dict): A tutorial configuration to format.
        task_presenter_configuration (dict): A task presenter configuration to help format the
            tutorial configuration.
        validate_configuration (bool): If set to True, the specified tutorial
            configuration will be validated before it is processed.
        validate_task_presenter_configuration (bool): If set to True, the specified
            task presenter configuration will be validated before it is used to format the
            tutorial configuration.

    Returns:
        dict: The formatted tutorial configuration.

    Raises:
        TypeError: If either the specified configurations is not a dictionary, or the
            validate_configuration and validate_task_presenter_configuration arguments
            are not booleans.
        ValueError: If either of the specified configurations is invalid.
    """
    check_arg_type(format_tutorial_configuration, "configuration", configuration, dict)
    check_arg_type(format_tutorial_configuration, "task_presenter_configuration", task_presenter_configuration, dict)
    check_arg_type(format_tutorial_configuration, "validate_configuration", validate_configuration, bool)
    check_arg_type(format_tutorial_configuration, "validate_task_presenter_configuration", validate_task_presenter_configuration, bool)

    def format_tutorial_subjects(tutorial_subjects, language):
        check_arg_type(format_tutorial_subjects, "tutorial_subjects", tutorial_subjects, list)
        for i, subject in enumerate(tutorial_subjects):
            tutorial_subjects[i] = format_tutorial_subject(subject, language, False)

        return tutorial_subjects

    if validate_configuration:
        valid, message = is_tutorial_configuration(configuration, task_presenter_configuration, validate_task_presenter_configuration=validate_task_presenter_configuration)
        if not valid:
            raise ValueError(message)

    formatters = {
        "default-message": lambda x, y: format_tutorial_default_message(x, y, False),
        "subjects": format_tutorial_subjects,
    }
    for key in configuration:
        formatter = formatters.get(key)
        if formatter:
            configuration[key] = formatter(configuration[key], task_presenter_configuration["language"])

    return configuration


def format_tutorial_default_message(default_message, language, validate_configurations=True):
    raise NotImplementedError


def format_tutorial_subject(tutorial_subject, language, validate_configurations=True):
    raise NotImplementedError


def format_tutorial_subject_assertion(tutorial_subject_assertion, language, validate_configurations=True):
    raise NotImplementedError
