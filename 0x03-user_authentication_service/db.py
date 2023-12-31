#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to the db"""
        session = self._session
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, *args, **kwargs) -> User:
        """find user by certain attributes"""
        session = self._session
        try:
            # print(kwargs)
            result = session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError
        # print(result)
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, *args, **kwargs) -> None:
        """find user by certain attributes"""
        session = self._session
        try:
            user = self.find_user_by(id=user_id)
            # print(user)
        except NoResultFound:
            raise ValueError

        for attribute, value in kwargs.items():
            if getattr(user, attribute, None) is None:
                raise ValueError
            setattr(user, attribute, value)
            session.commit()
        return None
