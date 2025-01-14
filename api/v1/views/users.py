#!/usr/bin/python3
"""
user
"""
import sys
sys.path.append('/AirBnB_clone_v3')
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    get users
    """

    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/user/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    get user
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    delete user
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        storage.delete(user)
        storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['PUT'], strict_slashes=False)
def create_user():
    """
    create user
    """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    user_data = request.get_json()
    user = User(**user_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    update user
    """
    user = storage.gete(User, user_id)
    if not  user:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    user_data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'update_at']
    for key, values in user_data.items():
        if key not in ignore_keys:
            settar(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
