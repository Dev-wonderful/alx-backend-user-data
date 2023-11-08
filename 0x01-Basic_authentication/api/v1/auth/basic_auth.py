#!/usr/bin/env python3
"""Module for the Basic Authentication"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """decode the base64 encoding"""
        if (base64_authorization_header is None or
            not isinstance(base64_authorization_header, str)):  # noqa: E129
            return None
        try:
            base_byte = base64.b64decode(base64_authorization_header)
            utf8_str = base_byte.decode('utf-8')
            return utf8_str
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """get current user"""
        if (decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str)):  # noqa: E129
            return None, None
        current_user: list = decoded_base64_authorization_header.split(':')
        if len(current_user) != 2:
            return None, None

        return tuple(current_user)
