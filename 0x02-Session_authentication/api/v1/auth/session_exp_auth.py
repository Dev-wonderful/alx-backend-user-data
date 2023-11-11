#!/usr/bin/env python3
"""Module for the Session Authentication Expiration"""
from api.v1.auth.session_auth import SessionAuth
from uuid import uuid4
from models.user import User
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Auth Expiration implementation class"""

    def __init__(self) -> None:
        """initialize an instance"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id (overloaded)"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user_id based on a session ID"""
        session: dict = super().user_id_for_session_id(session_id)
        if session is None:
            return None
        if self.session_duration <= 0:
            return session['user_id']
        created_at = session.get('created_at')
        if created_at is not None:
            if created_at >= (datetime.now() - timedelta(seconds=self.session_duration)):  # noqa: E501
                return session.get('user_id')
        return None
