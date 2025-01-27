#!/usr/bin/env python3
"""
Route module for the API
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv

# Initialize Flask application
api_app = Flask(__name__)
api_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
api_app.register_blueprint(app_views)
CORS(api_app, resources={r"/api/v1/*": {"origins": "*"}})

authentication = None
auth_type = getenv("AUTH_TYPE")

# Set up authentication type
if auth_type == "auth":
    from api.v1.auth.auth import Auth
    authentication = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    authentication = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    authentication = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    authentication = SessionExpAuth()
elif auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    authentication = SessionDBAuth()


@api_app.errorhandler(404)
def handle_not_found(error) -> str:
    """404 Not Found handler"""
    return jsonify({"error": "Not found"}), 404


@api_app.errorhandler(401)
def handle_unauthorized(error) -> str:
    """401 Unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401


@api_app.errorhandler(403)
def handle_forbidden(error) -> str:
    """403 Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403


@api_app.before_request
def validate_request() -> str:
    """Before Request Handler for validating incoming requests"""
    if authentication is None:
        return

    public_endpoints = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]

    if not authentication.require_auth(request.path, public_endpoints):
        return

    if authentication.authorization_header(request) is None \
            and authentication.session_cookie(request) is None:
        abort(401)

    user = authentication.current_user(request)
    if user is None:
        abort(403)

    request.current_user = user


if __name__ == "__main__":
    api_host = getenv("API_HOST", "0.0.0.0")
    api_port = getenv("API_PORT", "5000")
    api_app.run(host=api_host, port=api_port)

