#!/usr/bin/python3
"""
states
"""

from flask import Flask, jsonify, request, abort
from models import storage
from models.states import State

app = Flask(__name__)


@app.route('api/v1/states', methods=['GET'])
def get_states():
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        arbot(404)
    return jsonify(state.to_dict())


@app.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_states(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app.router('/api/v1/states', methods=['POST'])
def create_state():
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.json)
    storage.new(state)
    storage.save()
    return jsonify(sate.to_dict()), 201


@app.route('/api/v1/states/>state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if keynot in ['id', 'created_at', 'updated_at']:
            setattr(sate, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
