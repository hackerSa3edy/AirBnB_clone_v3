#!/usr/bin/python3
"""
This module defines a set of route handlers for the User object in the
Flask application.
It includes handlers for GET, POST, PUT, and DELETE methods.

Imports:
    User from models.user: The User class definition.
    storage from models: The storage engine for the application.
    app_views from api.v1.views: The blueprint for the views of the
    application.
    jsonify, abort, request, make_response from flask: Flask functions for
    handling responses and requests.
"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/users", methods=["GET"])
def list_users():
    """
    Retrieves all User objects from the storage.

    Returns:
        A JSON list of dictionaries where each dictionary represents
        a User object.
    """
    all = storage.all(User)
    return make_response(jsonify(
        [
            obj.to_dict() for obj in all.values()
        ]
    ), 200)


@app_views.route("/users/<string:user_id>", methods=["GET"])
def retrieve_user(user_id):
    """
    Retrieves a specific User object from the storage.

    Args:
        user_id (str): The id of the User object to retrieve.

    Returns:
        A JSON dictionary representing the User object if found, otherwise
        aborts with a 404 error.
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Deletes a specific User object from the storage.

    Args:
        user_id (str): The id of the User object to delete.

    Returns:
        A JSON empty dictionary with a status code 200 if the User object is
        deleted, otherwise aborts with a 404 error.
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)

    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"])
def create_user():
    """
    Creates a new User object and saves it to the storage.

    Returns:
        A JSON dictionary representing the new User object if created,
        otherwise returns a JSON error message with a status code 400.
    """
    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)
    if not params.get('email', None):
        return make_response("Missing email", 400)
    if not params.get('password', None):
        return make_response("Missing password", 400)

    newObj = User(**params)
    newObj.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Updates a specific User object in the storage.

    Args:
        user_id (str): The id of the User object to update.

    Returns:
        A JSON dictionary representing the updated User object if updated,
        otherwise returns a JSON error message with a status code 400.
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)

    params.pop("id", None)
    params.pop("created_at", None)
    params.pop("updated_at", None)
    params.pop("email", None)

    updated_obj = obj.to_dict()
    updated_obj.update(params)
    new_obj = User(**updated_obj)

    obj.delete()
    new_obj.save()

    return make_response(jsonify(new_obj.to_dict()), 200)
