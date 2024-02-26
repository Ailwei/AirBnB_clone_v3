#!/usr/bin/python3
"""
places
"""
import sys
sys.path.append('/AiBnB_clone_v3')
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_cityid(city_id):
    """
    get the places by city_id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jasonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_places(place_id):
    """
    retrieve places
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    delete places
    """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    stoarage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    create place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')

        user_id = request.json['user_id']
        user_id = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in request.jason:
        abort(400, 'Missing name')
    place_data = request.get_json()
    place_data['city_id'] = city_id
    place = Place(**place_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    update place
    """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    place_data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in place_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    if not request.json:
        abort(400, 'Not a JSON')

    states_ids = request.json.get('states', [])
    cities_ids = request.json.get('cities', [])
    amenities_ids = request.json.get('amenities', [])

    if not states_ids and not cities_ids and not amenities_ids:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places = []
    if states_ids:
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)

    if cities_ids:
        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    if amenities_ids:
        places = [place for place in places
                  if all(amenity_id in [
                          amenity.id for amenity in place.amenities
                          ]
                         for amenity_id in amenities_ids)]

    return jsonify([place.to_dict() for place in places])
