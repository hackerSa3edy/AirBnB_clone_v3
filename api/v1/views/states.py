#!/usr/bin/python3
"""
This module defines a set of route handlers for the State object in the
Flask application.
It includes handlers for GET, POST, PUT, and DELETE methods.

Imports:
    State from models.state: The State class definition.
    storage from models: The storage engine for the application.
    app_views from api.v1.views: The blueprint for the views of
    the application.
    jsonify, abort, request, make_response from flask: Flask functions for
    handling responses and requests.
"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/states", methods=["GET"])
def list_states():
    """
    Retrieves all State objects from the storage.

    Returns:
        A JSON list of dictionaries where each dictionary represents
        a State object.
    """
    all = storage.all(State)
    return make_response(jsonify(
        [
            obj.to_dict() for obj in all.values()
        ]
    ), 200)


@app_views.route("/states/<string:state_id>", methods=["GET"])
def retrieve_state(state_id):
    """
    Retrieves a specific State object from the storage.

    Args:
        state_id (str): The id of the State object to retrieve.

    Returns:
        A JSON dictionary representing the State object if found, otherwise
        aborts with a 404 error.
    """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Deletes a specific State object from the storage.

    Args:
        state_id (str): The id of the State object to delete.

    Returns:
        A JSON empty dictionary with a status code 200 if the State object is
        deleted, otherwise aborts with a 404 error.
    """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)

    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"])
def create_state():
    """
    Creates a new State object and saves it to the storage.

    Returns:
        A JSON dictionary representing the new State object if created,
        otherwise returns a JSON error message with a status code 400.
    """
    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)
    if not params.get('name', None):
        return make_response("Missing name", 400)

    newObj = State(**params)
    newObj.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """
    Updates a specific State object in the storage.

    Args:
        state_id (str): The id of the State object to update.

    Returns:
        A JSON dictionary representing the updated State object if updated,
        otherwise returns a JSON error message with a status code 400.
    """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)

    params.pop("id", None)
    params.pop("created_at", None)
    params.pop("updated_at", None)

    updated_obj = obj.to_dict()
    updated_obj.update(params)
    new_obj = State(**updated_obj)

    obj.delete()
    new_obj.save()

    return make_response(jsonify(new_obj.to_dict()), 200)
