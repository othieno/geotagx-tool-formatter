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
from collections import OrderedDict

def format_task_presenter_configuration(configuration, validate_configuration=False):
    """Formats the specified task presenter configuration.

    Args:
        configuration (dict): A task presenter configuration to format.
        validate_configuration (bool): If set to True, the specified configuration
            will be validated before it's processed.

    Returns:
        dict: The formatted task presenter configuration.

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
        "questionnaire": lambda q, v: format_task_presenter_questionnaire(q, configuration["language"], v),
    }
    for key in configuration:
        formatter = formatters.get(key)
        if formatter:
            configuration[key] = formatter(configuration[key], False)

    return configuration


def format_task_presenter_language(language, validate_language=True):
    """Formats the specified task presenter language configuration.

    Args:
        language (dict): A language configuration to format.
        validate_language (bool): If set to True, the specified configuration
            will be validated before it's processed.

    Returns:
        dict: The formatted language configuration.

    Raises:
        TypeError: If the language argument is not a dictionary, or
            validate_language is not a boolean.
        ValueError: If the specified configuration is not a valid language
            configuration.
    """
    check_arg_type(format_task_presenter_language, "language", language, dict)
    check_arg_type(format_task_presenter_language, "validate_language", validate_language, bool)

    if validate_language:
        valid, message = validator.is_task_presenter_language(language)
        if not valid:
            raise ValueError(message)

    # Add any missing fields to the configuration.
    for key, value in format_task_presenter_language.DEFAULT_CONFIGURATION.iteritems():
        language.setdefault(key, value)

    return language


format_task_presenter_language.DEFAULT_CONFIGURATION = OrderedDict({
    "default": "en",
    "available": ["en"],
})
"""The default task presenter language configuration."""


def format_task_presenter_subject(subject, validate_subject=True):
    """Formats the specified task presenter subject configuration.

    Args:
        subject (dict): A subject configuration to format.
        validate_subject (bool): If set to True, the specified configuration
            will be validated before it's processed.

    Returns:
        dict: The formatted subject configuration.

    Raises:
        TypeError: If the subject argument is not a dictionary, or
            validate_subject is not a boolean.
        ValueError: If the specified configuration is not a valid subject
            configuration.
    """
    check_arg_type(format_task_presenter_subject, "subject", subject, dict)
    check_arg_type(format_task_presenter_subject, "validate_subject", validate_subject, bool)

    if validate_subject:
        valid, message = validator.is_task_presenter_subject(subject)
        if not valid:
            raise ValueError(message)

    # Add any missing fields to the configuration.
    for key, value in format_task_presenter_subject.DEFAULT_CONFIGURATION.iteritems():
        subject.setdefault(key, value)

    return subject


format_task_presenter_subject.DEFAULT_CONFIGURATION = OrderedDict({
    "type": "image",
})
"""The default task presenter subject configuration."""


def format_task_presenter_questionnaire(questionnaire, language, validate_configurations=True):
    """Formats the specified task presenter questionnaire configuration.

    Args:
        questionnaire (dict): A questionnaire configuration to format.
        language (dict): A language configuration used to help format the
            questionnaire configuration.
        validate_configurations (bool): If set to True, the specified questionnaire
            and language configurations will be validated before they are processed.

    Returns:
        dict: The formatted questionnaire configuration.

    Raises:
        TypeError: If either the questionnaire or language argument is not a
            dictionary, or validate_configurations is not a boolean.
        ValueError: If either the questionnaire or language configuration is invalid.
    """
    check_arg_type(format_task_presenter_questionnaire, "questionnaire", questionnaire, dict)
    check_arg_type(format_task_presenter_questionnaire, "language", language, dict)
    check_arg_type(format_task_presenter_questionnaire, "validate_configurations", validate_configurations, bool)

    if validate_configurations:
        valid, message = validator.is_task_presenter_language(language)
        if not valid:
            raise ValueError(message)

        valid, message = validator.is_task_presenter_questionnaire(questionnaire, language["available"])
        if not valid:
            raise ValueError(message)

    from question import format_question

    questions = questionnaire["questions"]
    for i, question in enumerate(questions):
        questions[i] = format_question(question, language, False)

    return questionnaire
