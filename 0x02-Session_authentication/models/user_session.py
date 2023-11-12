#!/usr/bin/env python3
"""The module for the user session database model"""
from models.base import Base


class UserSession(Base):
    """The UserSession model class"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a user session instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
