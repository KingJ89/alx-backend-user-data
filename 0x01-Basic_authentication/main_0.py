#!/usr/bin/env python3
"""Main script to test basic Auth class methods."""

from api.v1.auth.auth import Auth

# Initialize Auth instance
auth_instance = Auth()

# Test require_auth method
print(auth_instance.require_auth("/api/v1/status/", ["/api/v1/status/"]))

# Test authorization_header method
print(auth_instance.authorization_header())

# Test current_user method
print(auth_instance.current_user())

