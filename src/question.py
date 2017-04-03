# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project formatter tool.
# It contains formatters for various components of a question configuration.
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
from geotagx_validator.task_presenter import is_task_presenter_language
from geotagx_validator.question import *
from geotagx_validator.helper import is_normalized_string
from helper import normalize_string

def format_question(question, language, validate_configurations=True):
    """Formats the specified question configuration.

    Args:
        question (dict): A question configuration to format.
        language (dict): A language configuration used to help format the
            question configuration.
        validate_configurations (bool): If set to True, the specified question and
            language configurations will be validated before they are processed.

    Returns:
        dict: The formatted question configuration.

    Raises:
        TypeError: If either the question or language argument is not a
            dictionary, or validate_configurations is not a boolean.
        ValueError: If either the question or language configuration is invalid.
    """
    check_arg_type(format_question, "question", question, dict)
    check_arg_type(format_question, "language", language, dict)
    check_arg_type(format_question, "validate_configurations", validate_configurations, bool)

    if validate_configurations:
        valid, message = is_task_presenter_language(language)
        if not valid:
            raise ValueError(message)

        valid, message = is_question(question, language["available"])
        if not valid:
            raise ValueError(message)

    formatters = {
        "title": format_question_title,
        "hint": format_question_help,
        "help": format_question_help,
        "input": format_question_input,
    }
    for key, value in question.iteritems():
        formatter = formatters.get(key)
        if formatter:
            question[key] = formatter(value, language, False)

    return question


def format_question_title(question_title, language, validate_configurations=True):
    """Formats the specified question title.

    This function will convert the question title into a normalized string. If the
    title is already normalized, no action is performed and the original title is
    returned.

    Args:
        question_title (basestring|dict): A question title configuration to format.
        language (dict): A language configuration used to help format the title.
        validate_configurations (bool): If set to True, the specified question title
            and language configurations will be validated before they are processed.

    Returns:
        dict: The formatted question title.

    Raises:
        TypeError: If either the question_title or language argument is not a
            dictionary, or validate_configurations is not a boolean.
        ValueError: If either the question_title or language configuration is invalid.
    """
    check_arg_type(format_question_title, "question_title", question_title, (basestring, dict))
    check_arg_type(format_question_title, "language", language, dict)
    check_arg_type(format_question_title, "validate_configurations", validate_configurations, bool)

    if validate_configurations:
        valid, message = is_task_presenter_language(language)
        if not valid:
            raise ValueError(message)

        valid, message = is_question_title(question_title)
        if not valid:
            raise ValueError(message)

    return question_title if is_normalized_string(question_title) else normalize_string(question_title, language["default"])


def format_question_help(question_help, language, validate_configurations=True):
    """Formats the specified question help.

    This function will convert the question help into a normalized string. If the
    help is already normalized, no action is performed and the original help is
    returned.

    Args:
        question_help (basestring|dict): A question help configuration to format.
        language (dict): A language configuration used to help format the help.
        validate_configurations (bool): If set to True, the specified question help
            and language configurations will be validated before they are processed.

    Returns:
        dict: The formatted question help.

    Raises:
        TypeError: If either the question_help or language argument is not a
            dictionary, or validate_configurations is not a boolean.
        ValueError: If either the question_help or language configuration is invalid.
    """
    check_arg_type(format_question_help, "question_help", question_help, (basestring, dict))
    check_arg_type(format_question_help, "language", language, dict)
    check_arg_type(format_question_help, "validate_configurations", validate_configurations, bool)

    if validate_configurations:
        valid, message = is_task_presenter_language(language)
        if not valid:
            raise ValueError(message)

        valid, message = is_question_help(question_help)
        if not valid:
            raise ValueError(message)

    return question_help if is_normalized_string(question_help) else normalize_string(question_help, language["default"])


def format_question_input(question_input, language, validate_configurations=True):
    """Formats the specified question input configuration.

    Args:
        question_input (dict): A question input configuration to format.
        language (dict): A language configuration used to help format the
            question input configuration.
        validate_configurations (bool): If set to True, the specified configurations
            will be validated before they are processed.

    Returns:
        dict: The formatted question input configuration.

    Raises:
        TypeError: If either the question_input or language argument is not a
            dictionary, or validate_configurations is not a boolean.
        ValueError: If either the question_input or language configuration is invalid.
    """
    check_arg_type(format_question_input, "question_input", question_input, dict)
    check_arg_type(format_question_input, "language", language, dict)
    check_arg_type(format_question_input, "validate_configurations", validate_configurations, bool)

    if validate_configurations:
        valid, message = is_task_presenter_language(language)
        if not valid:
            raise ValueError(message)

        valid, message = is_question_input(question_input, language["default"])
        if not valid:
            raise ValueError(message)

    input_type = question_input["type"]
    default_configuration = format_question_input.DEFAULT_CONFIGURATIONS.get(input_type, {})
    formatter = {
        "dropdown-list": __format_dropdown_list_input,
        "multiple-option": __format_multiple_option_input,
        "text": __format_text_input,
        "number": __format_number_input,
        "datetime": __format_datetime_input,
        "url": __format_url_input,
        "geotagging": __format_geotagging_input,
    }.get(input_type, None)

    for key, value in default_configuration.iteritems():
        question_input.setdefault(key, value)

    return formatter(question_input, language) if formatter else question_input


format_question_input.DEFAULT_CONFIGURATIONS = {
    "dropdown-list": {
        "options": None,
        "prompt": None,
        "size": 1,
    },
    "multiple-option": {
        "options": None,
        "enable-multiple-choices": False,
        "enable-other-option": True,
        "enable-illustrations": False,
        "size": 8,
    },
    "text": {
        "enable-long-text": False,
        "min-length": 0,
        "max-length": 128,
        "placeholder": None,
    },
    "number": {
        "min-value": None,
        "max-value": None,
        "placeholder": None,
    },
    "datetime": {
        "date-format": "yyyy/MM/dd",
        "time-format": "HH:mm:ss",
        "from": None,
        "to": None,
        "disable-date": False,
        "disable-time": False,
    },
    "url": {
        "max-length": 256,
        "placeholder": None,
    },
    "geotagging": {
        "location": None,
    },
}
"""The set of default configuration values for each question input."""


def __format_dropdown_list_input(dropdown_list_input, language):
    """Formats the specified dropdown-list input.

    Args:
        dropdown_list_input (dict): A dropdown-list input configuration to format.
        language (dict): A language configuration used to help format the input configuration.

    Returns:
        dict: A formatted dropdown-list input configuration.
    """
    raise NotImplementedError

    return dropdown_list_input


def __format_multiple_option_input(multiple_option_input, language):
    """Formats the specified multiple-option input.

    Args:
        multiple_option_input (dict): A multiple-option input configuration to format.
        language (dict): A language configuration used to help format the input configuration.

    Returns:
        dict: A formatted multiple-option input configuration.
    """
    raise NotImplementedError

    return multiple_option_input


def __format_text_input(text_input, language):
    """Formats the specified text input.

    Args:
        text_input (dict): A text input configuration to format.
        language (dict): A language configuration used to help format the input configuration.

    Returns:
        dict: A formatted text input configuration.
    """
    raise NotImplementedError

    return text_input


def __format_number_input(number_input, language):
    """Formats the specified number input.

    Args:
        number_input (dict): A number input configuration to format.
        language (dict): A language configuration used to help format the input configuration.

    Returns:
        dict: A formatted number input configuration.
    """
    raise NotImplementedError

    return number_input


def __format_datetime_input(datetime_input, language):
    """Formats the specified datetime input.

    Args:
        datetime_input (dict): A datetime input configuration to format.
        language (dict): A language configuration used to help format the input configuration.

    Returns:
        dict: A formatted datetime input configuration.
    """
    raise NotImplementedError

    return datetime_input


def __format_url_input(url_input, language):
    """Formats the specified URL input.

    Args:
        url_input (dict): A URL input configuration to format.
        language (dict): A language configuration used to help format the input configuration.

    Returns:
        dict: A formatted URL input configuration.
    """
    raise NotImplementedError

    return url_input


def __format_geotagging_input(geotagging_input, language):
    """Formats the specified geotagging input.

    Args:
        geotagging_input (dict): A geotagging input configuration to format.
        language (dict): A language configuration used to help format the input configuration.

    Returns:
        dict: A formatted geotagging input configuration.
    """
    raise NotImplementedError

    return geotagging_input
