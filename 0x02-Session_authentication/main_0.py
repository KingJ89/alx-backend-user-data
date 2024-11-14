#!/usr/bin/env python3
"""Main script to test Basic Authentication setup."""

import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

# Define user test credentials
user_email = "bob@hbtn.io"
user_clear_pwd = "H0lbertonSchool98!"

# Create a new user instance
user = User()
user.email = user_email
user.password = user_clear_pwd
user.save()

# Display the new user ID
print(f"New user: {user.id}")

# Prepare and display the Base64 encoding for Basic Authentication
basic_credentials = f"{user_email}:{user_clear_pwd}"
encoded_credentials = base64.b64encode(basic_credentials.encode('utf-8')).decode('utf-8')
print(f"Basic Base64: {encoded_credentials}")

