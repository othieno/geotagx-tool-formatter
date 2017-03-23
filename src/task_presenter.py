# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project formatter tool.
# It contains formatters for various components of a task presenter configuration.
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
import geotagx_validator.task_presenter as validator

def format_task_presenter_configuration(configuration, validate_configuration=False):
    """Formats the specified task presenter configuration.

    Args:
        configuration (dict): A task presenter configuration to format.
        validate_configuration (bool): If set to True, the specified configuration
            will be validated before it's processed.

    Raises:
        TypeError: If the configuration argument is not a dictionary, or
            validate_configuration is not a boolean.
        ValueError: If the specified configuration is not a valid task presenter
            configuration.
    """
    check_arg_type(format_task_presenter_configuration, "configuration", configuration, dict)
    check_arg_type(format_task_presenter_configuration, "validate_configuration", validate_configuration, bool)

    if validate_configuration:
        valid, message = validator.is_task_presenter_configuration(configuration)
        if not valid:
            raise ValueError(message)

    formatters = {
        "language": format_task_presenter_language,
        "subject": format_task_presenter_subject,
        "questionnaire": format_task_presenter_questionnaire,
    }
    for key in configuration:
        formatter = formatters.get(key)
        if formatter:
            configuration[key] = formatter(configuration[key], False)

    return configuration


def format_task_presenter_language(language, validate_language=True):
    raise NotImplementedError


def format_task_presenter_subject(subject, validate_subject=True):
    raise NotImplementedError


def format_task_presenter_questionnaire(questionnaire, validate_questionnaire=True):
    raise NotImplementedError
