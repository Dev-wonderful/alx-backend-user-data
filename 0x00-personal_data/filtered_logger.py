#!/usr/bin/env python3
"""Filtered logger module"""
import re

def filter_datum(fields: list, redaction: str, message: 
                 list, separator: str) -> str:
    """Filter the log info"""
    print(message)
    for field in fields:
        pattern = r'{}=(\S+)'.format(field)
        print(pattern)
        replacement = '{}={}'.format(field, redaction)
        message = re.sub(pattern, replacement, message)
        print(field)
        print(message)
    return message
