#!/usr/bin/env python3
"""Filtered logger module"""
import re

def filter_datum(fields: list, redaction: str, message: 
                 list, separator: str) -> str:
    """Filter the log info"""
    for field in fields:
        pattern = r'{}=([^;]+)'.format(field)
        replacement = '{}={}'.format(field, redaction)
    return re.sub(pattern, replacement, message)
