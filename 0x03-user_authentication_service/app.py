#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """Index route for the app"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register():
    """Register a new user"""
    data = request.form
    email = data.get("email", None)
    password = data.get("password", None)
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """Logs in and creates a new session for a user"""
    data = request.form
    email = data.get("email", None)
    password = data.get("password", None)
    try:
        assert email is not None
        assert password is not None
    except AssertionError:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(401)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
