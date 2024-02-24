#!/usr/bin/python3
"""
index file
"""
from flask import jsonify
from city import City
from place import Place
from review import Review
from user import User
from state import State
from api.v1.views import app_views
from models import storage



@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    get stats method
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
