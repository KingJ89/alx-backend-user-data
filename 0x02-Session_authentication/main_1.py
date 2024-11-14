#!/usr/bin/env python3
"""Main script to test session creation with SessionAuth."""

from api.v1.auth.session_auth import SessionAuth

# Initialize SessionAuth instance
sa = SessionAuth()

# Display the type and initial state of user_id_by_session_id
print(f"{type(sa.user_id_by_session_id)}: {sa.user_id_by_session_id}")

# Test cases for different user_ids
test_user_ids = [None, 89, "abcde", "fghij", "abcde"]

# Loop through each test case and create a session, displaying the result
for user_id in test_user_ids:
    session = sa.create_session(user_id)
    print(f"{user_id} => {session}: {sa.user_id_by_session_id}")
