#!/usr/bin/env python3
"""
Main 3 - Testing BasicAuth's decode_base64_authorization_header method.
"""

from api.v1.auth.basic_auth import BasicAuth

def main():
    """ Test cases for decode_base64_authorization_header method. """
    basic_auth = BasicAuth()
    
    test_cases = [
        None,
        89,
        "Holberton School",
        "SG9sYmVydG9u",
        "SG9sYmVydG9uIFNjaG9vbA==",
        basic_auth.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")
    ]
    
    for i, test_case in enumerate(test_cases, start=1):
        result = basic_auth.decode_base64_authorization_header(test_case)
        print(f"Test Case {i}: {test_case} -> {result}")

if __name__ == "__main__":
    main()
