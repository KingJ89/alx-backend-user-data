#!/usr/bin/env python3
"""
Basic Flask app for user authentication.
"""
from flask import Flask, request, abort, jsonify, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    Welcome route.

    Returns:
        JSON response with a welcome message.
    """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """
    Register a new user.

    Args:
        email (str): User's email address.
        password (str): User's password.

    Returns:
        JSON response indicating success or failure.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, description="Email and password are required")

    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'}), 201
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Log in a user.

    Args:
        email (str): User's email address.
        password (str): User's password.

    Returns:
        JSON response with session information or 401 on failure.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401, description="Invalid credentials")

    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Log out a user by invalidating their session.

    Returns:
        Redirect to the home page or 403 if no valid session is found.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403, description="Session not found")

    AUTH.destroy_session(user.id)
    response = jsonify({'message': 'logout successful'})
    response.delete_cookie('session_id')
    return redirect('/', code=302)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def get_profile() -> str:
    """
    Retrieve the profile of the logged-in user.

    Returns:
        JSON response with the user's email or 403 if not logged in.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403, description="No valid session")

    return jsonify({'email': user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def request_password_reset() -> str:
    """
    Request a password reset token for a user.

    Args:
        email (str): User's email address.

    Returns:
        JSON response with the reset token or 403 if the email is invalid.
    """
    email = request.form.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': reset_token}), 200
    except ValueError:
        abort(403, description="Invalid email")


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password() -> str:
    """
    Reset a user's password using a reset token.

    Args:
        email (str): User's email address.
        reset_token (str): Valid password reset token.
        new_password (str): New password for the user.

    Returns:
        JSON response indicating success or 403 on failure.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400, description="Email, reset token, and new password are required")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({'email': email, 'message': 'Password updated'}), 200
    except ValueError:
        abort(403, description="Invalid reset token")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
