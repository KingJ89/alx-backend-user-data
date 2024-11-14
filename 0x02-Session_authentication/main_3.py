#!/usr/bin/env python3
"""Cookie server using Flask to retrieve session cookie values."""

from flask import Flask, request
from api.v1.auth.auth import Auth

# Initialize Flask app and authentication
app = Flask(__name__)
auth = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def root_path():
    """Root endpoint that displays the session cookie value."""
    cookie_value = auth.session_cookie(request)
    return f"Cookie value: {cookie_value}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
