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


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """
    get status method
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Retrieve number of each objects by type
    """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])
    return jsonify(num_objs)
