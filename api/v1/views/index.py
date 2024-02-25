#!/usr/bin/python3
"""
index file
"""
import sys
sys.path.append('/AirBnB_clone_v3')
from flask import jsonify
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'])
def get_status():
    """
    get stats method
    """
    status = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify({"status": "ok"})
