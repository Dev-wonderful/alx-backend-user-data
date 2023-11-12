#!/usr/bin/env python3
"""Module for the Session Authentication Expiration database storage"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from uuid import uuid4
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session Auth Expiration database storage implementation class"""

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id (overloaded)"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        new_user_session = UserSession(user_id=user_id, session_id=session_id)
        new_user_session.save()
        # self.user_id_by_session_id[session_id] = new_user_session
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user_id based on a session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        UserSession.load_from_file()
        try:
            result = UserSession.search({'session_id': session_id})
        except KeyError:
            return None
        if len(result) == 0:
            return None
        session: UserSession = result[0]
        if self.session_duration <= 0:
            return session.user_id
        created_at = session.created_at
        if created_at is not None:
            if created_at >= (datetime.now() - timedelta(seconds=self.session_duration)):  # noqa: E501
                return session.user_id
        return None

    def destroy_session(self, request=None):
        """Delete the user session/logout (overloaded)"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        UserSession.load_from_file()
        result = UserSession.search({'session_id': session_id})
        if len(result) == 0:
            return False
        session: UserSession = result[0]
        session.remove()
        return True
