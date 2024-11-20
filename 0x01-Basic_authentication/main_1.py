#!/usr/bin/env python3
"""Main script to test require_auth method of Auth class with various paths."""

from api.v1.auth.auth import Auth

# Initialize Auth instance
auth_instance = Auth()

# Test require_auth with various paths and excluded paths
print(auth_instance.require_auth(None, None))
print(auth_instance.require_auth(None, []))
print(auth_instance.require_auth("/api/v1/status/", []))
print(auth_instance.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(auth_instance.require_auth("/api/v1/status", ["/api/v1/status/"]))
print(auth_instance.require_auth("/api/v1/users", ["/api/v1/status/"]))
print(auth_instance.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))
