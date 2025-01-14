#!/usr/bin/python3
"""
places amenities
"""
import sys
sys.path.append('AirBnB_clone_v3')
from flask import abort, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route(
        '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_places_amenities(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenities.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
        strict_slashes=False
        )
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
        strict_slashes=False
        )
def link_amenity_to_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
