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
        from geotagx_validator.task_presenter import is_task_presenter_language
        from geotagx_validator.question import is_question

        valid, message = is_task_presenter_language(language)
        if not valid:
            raise ValueError(message)

        valid, message = is_question(question, language["available"])
        if not valid:
            raise ValueError(message)

    formatters = {
        "title": lambda x: format_question_title(x, False),
        "hint": lambda x: format_question_help(x, False),
        "help": lambda x: format_question_help(x, False),
        "input": lambda x: format_question_input(x, False),
    }
    for key, value in question.iteritems():
        formatter = formatters.get(key)
        if formatter:
            question[key] = formatter(value)

    return question


def format_question_title(question_title, validate=True):
    raise NotImplementedError


def format_question_help(question_help, validate=True):
    raise NotImplementedError


def format_question_input(question_input, validate=True):
    raise NotImplementedError
