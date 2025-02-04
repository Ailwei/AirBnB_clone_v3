#!/usr/bin/python3
"""
cities
"""
import sys
sys.path.append('/AirBnB_clone_v3')
from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    get cities by state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    get cities
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/city_id', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    delete city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(stae_id):
    """
    create city
    """
    state = storage.get(State, city_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    city_data = request.get_json()
    city_data['state_id'] = state_id
    city = City(**city_data)
    city.save()
    return jsonify(City.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    update city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    city_data = request.get_json()
    ignore_keys = ['id', 'state_id', 'creeated_at', 'updated_at']
    for keys, values in city_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
