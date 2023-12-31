#!/usr/bin/env python3
"""Module for the auth class"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """The template Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check for auth path"""
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        path = path if path[-1] == '/' else path + '/'
        # handle wild card pattern matching urls
        wild_card = excluded_paths[0] if '*' in excluded_paths[0] else None
        if path in excluded_paths:
            return False
        elif wild_card:
            return False if path >= wild_card[:-1] else True
        return True

    def authorization_header(self, request=None) -> str:
        """get the auth request header"""
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        # print(request.cookies.get(os.getenv('SESSION_NAME')))
        return request.cookies.get(os.getenv('SESSION_NAME'))
