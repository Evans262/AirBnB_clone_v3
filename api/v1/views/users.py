#!/usr/bin/python3
"""State objects"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.users import users


@app_views.route('/api/v1/users', methods=['GET'],
                 strict_slashes=False)
def ret_users():
    """ Retrieves users """
    list_user = []
    for users in storage.all(users).values():
        list_users.append(users.to_dict())
    return jsonify(list_users)


@app_views.route('/api/v1/users/<users_id>', methods=['GET'],
                 strict_slashes=False)
def ret_users(users_id):
    """ Retrieves an users """
    single_users = storage.get(users, users_id)
    if single_users is None:
        abort(404)
    return jsonify(single_users.to_dict())


@app_views.route("/api/v1/users/<users_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(users_id):
    """Delete a users object"""
    users_del = storage.get(users, users_id)
    if users_del:
        storage.delete(users_del)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/api/v1/users/<users_id>', methods=['PUT'],
                 strict_slashes=False)
def update_users(users_id):
    """ Task 7 :Updates a State object:"""
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    users_up = storage.get(users, state_id)
    if users_up is None:
        abort(404)
    for key, val in content.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(users_up, key, val)
    storage.save()
    return jsonify(users_up.to_dict()), 200


@app_views.route('/api/v1/users/', methods=['POST'],
                 strict_slashes=False)
def post_users():
    """create a new users"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_users = users(**request.get_json())
    new_users.save()
    return make_response(jsonify(new_users.to_dict()), 201)
