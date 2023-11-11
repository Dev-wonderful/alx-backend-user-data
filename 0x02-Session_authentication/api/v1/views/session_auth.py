#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't find the User
    """
    data = None
    error_msg = None
    data = request.form

    if data.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and data.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            user_email: str = data.get("email")
            user_password: str = data.get("password")
            result: list = User.search({'email': user_email})
            if len(result) == 0:
                return (
                    jsonify({"error": "no user found for this email"}), 404
                )
            user: User = result[0]
            if user.is_valid_password(user_password) is False:
                return (
                    jsonify({"error": "wrong password"}), 401
                )
            # create session ID
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(os.getenv('SESSION_NAME'), session_id)
            return response
        except Exception as e:
            error_msg = "Can't login the user: {}".format(e)
    return jsonify({'error': error_msg}), 400


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Log out a logged in user"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
