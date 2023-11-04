#!/usr/bin/env python3
"""Filtered logger module"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message:
                 str, separator: str) -> str:
    """Filter the log info"""
    for field in fields:
        pattern: str = r'{}=([^;]+)'.format(field)
        replacement: str = '{}={}'.format(field, redaction)
    return re.sub(pattern, replacement, message)
