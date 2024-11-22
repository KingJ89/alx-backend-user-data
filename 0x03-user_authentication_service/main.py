#!/usr/bin/env python3
"""
End-to-end integration tests for the authentication system.
"""
import requests

BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """
    Test user registration.
    """
    response = requests.post(
        f'{BASE_URL}/users',
        json={'email': email, 'password': password})
    assert response.status_code == 201, "User registration failed"


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with incorrect password.
    """
    response = requests.post(
        f'{BASE_URL}/sessions',
        json={'email': email, 'password': password})
    assert response.status_code == 401, "Login with incorrect password should fail"


def log_in(email: str, password: str) -> str:
    """
    Test login with correct credentials.

    Returns:
        str: The session ID for the logged-in user.
    """
    response = requests.post(
        f'{BASE_URL}/sessions',
        json={'email': email, 'password': password})
    assert response.status_code == 200, "Login failed with correct credentials"
    data = response.json()
    assert 'session_id' in data, "Session ID missing in login response"
    return data['session_id']


def profile_unlogged() -> None:
    """
    Test accessing profile without being logged in.
    """
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403, "Profile access should fail for unlogged users"


def profile_logged(session_id: str) -> None:
    """
    Test accessing profile while logged in.

    Args:
        session_id (str): The session ID of the logged-in user.
    """
    headers = {'Cookie': f'session_id={session_id}'}
    response = requests.get(f'{BASE_URL}/profile', headers=headers)
    assert response.status_code == 200, "Profile access failed for logged-in user"
    data = response.json()
    assert 'email' in data, "Email missing in profile response"


def log_out(session_id: str) -> None:
    """
    Test logging out.

    Args:
        session_id (str): The session ID of the user to log out.
    """
    headers = {'Cookie': f'session_id={session_id}'}
    response = requests.delete(f'{BASE_URL}/sessions', headers=headers)
    assert response.status_code == 204, "Logout failed"


def reset_password_token(email: str) -> str:
    """
    Test requesting a password reset token.

    Args:
        email (str): The user's email address.

    Returns:
        str: The reset password token.
    """
    response = requests.post(
        f'{BASE_URL}/reset_password', data={'email': email})
    assert response.status_code == 200, "Password reset token request failed"
    data = response.json()
    assert 'reset_token' in data, "Reset token missing in response"
    return data['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test updating the user's password.

    Args:
        email (str): The user's email address.
        reset_token (str): The reset password token.
        new_password (str): The new password.
    """
    response = requests.put(
        f'{BASE_URL}/reset_password',
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password
        })
    assert response.status_code == 200, "Password update failed"
    data = response.json()
    assert data.get('message') == 'Password updated', "Password update message missing or incorrect"


if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
