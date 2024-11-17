#!/usr/bin/env python3
""" script basic script Import and Instantiate BasicAuth, extract_base64_authorization_header and Check if the input is a string.
Verify that the string starts with "Basic ".
Extract and return the base64-encoded portion if the above conditions are met.
Return None for invalid inputs.
"""

from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_base64_authorization_header(None))
print(a.extract_base64_authorization_header(89))
print(a.extract_base64_authorization_header("Holberton School"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
print(a.extract_base64_authorization_header("Basic1234"))
print(a.extract_base64_authorization_header("Basic Holberton"))
