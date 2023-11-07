#!/usr/bin/env python3
"""Module for the auth class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """The template Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check for auth path"""
        return False

    def authorization_header(self, request=None) -> str:
        """get the auth header"""
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user"""
        return request
