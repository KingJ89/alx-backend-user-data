#!/usr/bin/env python3
"""Main script to test session handling with SessionAuth."""

from api.v1.auth.session_auth import SessionAuth

# Initialize SessionAuth instance
session_auth = SessionAuth()

# Test creating sessions for different user IDs
user_id_1 = "abcde"
session_id_1 = session_auth.create_session(user_id_1)
print(f"{user_id_1} => {session_id_1}: {session_auth.user_id_by_session_id}")

user_id_2 = "fghij"
session_id_2 = session_auth.create_session(user_id_2)
print(f"{user_id_2} => {session_id_2}: {session_auth.user_id_by_session_id}")

print("---")

# Test retrieving user IDs with various session IDs
test_session_id = None
retrieved_user_id = session_auth.user_id_for_session_id(test_session_id)
print(f"{test_session_id} => {retrieved_user_id}")

test_session_id = 89
retrieved_user_id = session_auth.user_id_for_session_id(test_session_id)
print(f"{test_session_id} => {retrieved_user_id}")

test_session_id = "doesntexist"
retrieved_user_id = session_auth.user_id_for_session_id(test_session_id)
print(f"{test_session_id} => {retrieved_user_id}")

print("---")

# Test retrieving user IDs for valid session IDs
test_session_id = session_id_1
retrieved_user_id = session_auth.user_id_for_session_id(test_session_id)
print(f"{test_session_id} => {retrieved_user_id}")

test_session_id = session_id_2
retrieved_user_id = session_auth.user_id_for_session_id(test_session_id)
print(f"{test_session_id} => {retrieved_user_id}")

print("---")

# Create another session for user_id_1 and test retrieval
new_session_id_1 = session_auth.create_session(user_id_1)
print(f"{user_id_1} => {new_session_id_1}: {session_auth.user_id_by_session_id}")

retrieved_user_id = session_auth.user_id_for_session_id(new_session_id_1)
print(f"{new_session_id_1} => {retrieved_user_id}")

retrieved_user_id = session_auth.user_id_for_session_id(session_id_1)
print(f"{session_id_1} => {retrieved_user_id}")
