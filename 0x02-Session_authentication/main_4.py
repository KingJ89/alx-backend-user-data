#!/usr/bin/env python3
"""Main script for testing SessionAuth with Flask."""

from flask import Flask, request
from api.v1.auth.session_auth import SessionAuth
from models.user import User

# Create a test user
user_email = "bobsession@hbtn.io"
user_clear_pwd = "fake pwd"

user = User()
user.email = user_email
user.password = user_clear_pwd
user.save()

# Create a session ID for the test user
session_auth = SessionAuth()
session_id = session_auth.create_session(user.id)
print(f"User with ID: {user.id} has a Session ID: {session_id}")

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'], strict_slashes=False)
def root_path():
    """Root endpoint that checks for a valid session and user."""
    request_user = session_auth.current_user(request)
    if request_user is None:
        return "No user found\n"
    return f"User found: {request_user.id}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
