#!/usr/bin/env python3
"""Module for the Basic Authentication"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """The basic auth class implementation"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header
            for a Basic Authentication
        """
        if (authorization_header is None or
            not isinstance(authorization_header, str)):  # noqa: E129
            return None
        auth_header: list = authorization_header.split()
        if len(auth_header) != 2:
            return None
        type, encoding = auth_header
        if type != 'Basic':
            return None
        return encoding
