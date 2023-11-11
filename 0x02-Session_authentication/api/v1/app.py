#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from typing import Union
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# print(os.environ)
auth: Union[str, Auth, BasicAuth, SessionAuth] = None
auth_config = {
    'auth': Auth(),
    'basic_auth': BasicAuth(),
    'session_auth': SessionAuth()
}
auth_type = os.getenv('AUTH_TYPE')
if auth_type in auth_config.keys():
    auth = auth_config.get(auth_type)


@app.before_request
def run_before_every_request():
    """Check auth before every request"""
    if auth is None:
        return
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    if auth.require_auth(request.path, excluded_paths) is False:
        return
    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:  # noqa: E501
        # print("here")
        abort(401)
    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
