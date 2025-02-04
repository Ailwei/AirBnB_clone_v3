#!/usr/bin/python3
"""
places reviews
"""
import sys
sys.path.append('/AirBnB_clone_v3')
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """
    get place reviews
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route(
        '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_place_review(review_id):
    """
    get place review
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_review(review_id):
    """
    delete review
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    create review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    update review
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
