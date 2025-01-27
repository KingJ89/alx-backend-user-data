#!/usr/bin/env python3
"""
Module for User views
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users() -> str:
    """GET /api/v1/users
    Returns:
      - List of all User objects in JSON format
    """
    users_list = [usr.to_json() for usr in User.all()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str = None) -> str:
    """GET /api/v1/users/<user_id>
    Args:
      - user_id: ID of the User
    Returns:
      - User object in JSON format
      - 404 if the User ID does not exist
    """
    if not user_id:
        abort(404)

    if user_id == "me" and not request.current_user:
        abort(404)

    if user_id == "me" and request.current_user:
        return jsonify(request.current_user.to_json())

    user_obj = User.get(user_id)
    if not user_obj:
        abort(404)

    return jsonify(user_obj.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def remove_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/<user_id>
    Args:
      - user_id: ID of the User
    Returns:
      - Empty JSON if the User has been successfully deleted
      - 404 if the User ID does not exist
    """
    if not user_id:
        abort(404)

    user_obj = User.get(user_id)
    if not user_obj:
        abort(404)

    user_obj.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user() -> str:
    """POST /api/v1/users
    JSON body:
      - email
      - password
      - first_name (optional)
      - last_name (optional)
    Returns:
      - Created User object in JSON format
      - 400 if the User cannot be created
    """
    json_data = None
    error_message = None

    try:
        json_data = request.get_json()
    except Exception:
        pass

    if not json_data:
        error_message = "Wrong format"
    elif not json_data.get("email"):
        error_message = "email missing"
    elif not json_data.get("password"):
        error_message = "password missing"

    if error_message:
        return jsonify({'error': error_message}), 400

    try:
        new_user = User(
            email=json_data.get("email"),
            password=json_data.get("password"),
            first_name=json_data.get("first_name"),
            last_name=json_data.get("last_name")
        )
        new_user.save()
        return jsonify(new_user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def modify_user(user_id: str = None) -> str:
    """PUT /api/v1/users/<user_id>
    Args:
      - user_id: ID of the User
    JSON body:
      - first_name (optional)
      - last_name (optional)
    Returns:
      - Updated User object in JSON format
      - 404 if the User ID does not exist
      - 400 if the User cannot be updated
    """
    if not user_id:
        abort(404)

    user_obj = User.get(user_id)
    if not user_obj:
        abort(404)

    try:
        json_data = request.get_json()
    except Exception:
        return jsonify({'error': "Wrong format"}), 400

    if not json_data:
        return jsonify({'error': "Wrong format"}), 400

    if "first_name" in json_data:
        user_obj.first_name = json_data["first_name"]

    if "last_name" in json_data:
        user_obj.last_name = json_data["last_name"]

    user_obj.save()
    return jsonify(user_obj.to_json()), 200

