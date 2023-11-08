#!/usr/bin/env python3
"""Module for the Basic Authentication"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
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
        except UnicodeDecodeError:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """get current user"""
        if (decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str)):  # noqa: E129
            return None, None
        decoded_header = decoded_base64_authorization_header.replace(
            ':', ' ', 1
        )
        current_user: list = decoded_header.split()
        if len(current_user) != 2:
            return None, None

        return tuple(current_user)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """Get user details from the database"""
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        # find user and validate password
        try:
            users = User.search({'email': user_email})
            if len(users) == 0:
                return None
            user = users[0]
            if user.is_valid_password(user_pwd) is False:
                return None
        except KeyError:
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user"""
        basic_auth_header = self.authorization_header(request)
        if not basic_auth_header:
            return None
        decoded_details = self.decode_base64_authorization_header(
            self.extract_base64_authorization_header(
                basic_auth_header
            )
        )
        if not decoded_details:
            return None
        user_credentials = self.extract_user_credentials(
            decoded_details
        )
        if not user_credentials:
            return None
        current_user = self.user_object_from_credentials(
            *user_credentials
        )
        return current_user
