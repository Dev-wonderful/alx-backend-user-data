#!/usr/bin/env python3
"""Filtered logger module"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message:
                 str, separator: str) -> str:
    """Filter the log info

    Args:
        fields (list): A list of strings representing all fields to obfuscate
        redaction (str): A string representing by what the field will
                         be obfuscated
        message (str): A string representing the log line
        separator (str): A string representing by which character is
                         separating all fields in the log line

    Returns:
        str: The log message obfuscated
    """
    for field in fields:
        pattern: str = r'{}=([^{}]+)'.format(field, separator)
        replacement: str = '{}={}'.format(field, redaction)
        message = re.sub(pattern, replacement, message)
    return message
