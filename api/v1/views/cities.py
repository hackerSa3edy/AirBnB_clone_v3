#!/usr/bin/python3
"""
This module defines a set of route handlers for the City object in the
Flask application.
It includes handlers for GET, POST, PUT, and DELETE methods.

Imports:
    City from models.city: The City class definition.
    State from models.state: The State class definition.
    storage from models: The storage engine for the application.
    app_views from api.v1.views: The blueprint for the views of
    the application.
    jsonify, abort, request, make_response from flask: Flask functions for
    handling responses and requests.
"""

from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/states/<string:state_id>/cities", methods=["GET"])
def list_cities(state_id):
    """
    Retrieves all City objects associated with a specific State object from
    the storage.

    Args:
        state_id (str): The id of the State object.

    Returns:
        A JSON list of dictionaries where each dictionary represents a City
        object if found, otherwise aborts with a 404 error.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    all = state.cities
    return make_response(jsonify(
        [
            obj.to_dict() for obj in all
            ]
        ), 200)


@app_views.route("/cities/<string:city_id>", methods=["GET"])
def retrieve_city(city_id):
    """
    Retrieves a specific City object from the storage.

    Args:
        city_id (str): The id of the City object to retrieve.

    Returns:
        A JSON dictionary representing the City object if found, otherwise
        aborts with a 404 error.
    """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/cities/<string:city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    Deletes a specific City object from the storage.

    Args:
        city_id (str): The id of the City object to delete.

    Returns:
        A JSON empty dictionary with a status code 200 if the City object is
        deleted, otherwise aborts with a 404 error.
    """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<string:state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Creates a new City object associated with a specific State object and
    saves it to the storage.

    Args:
        state_id (str): The id of the State object.

    Returns:
        A JSON dictionary representing the new City object if created,
        otherwise returns a JSON error message with a status code 400.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)
    if not params.get('name', None):
        return make_response("Missing name", 400)

    params.update({"state_id": state_id})
    newObj = City(**params)
    newObj.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Updates a specific City object in the storage.

    Args:
        city_id (str): The id of the City object to update.

    Returns:
        A JSON dictionary representing the updated City object if updated,
        otherwise returns a JSON error message with a status code 400.
    """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)

    params.pop("id", None)
    params.pop("state_id", None)
    params.pop("created_at", None)
    params.pop("updated_at", None)

    updated_obj = obj.to_dict()
    updated_obj.update(params)
    new_obj = City(**updated_obj)

    obj.delete()
    new_obj.save()

    return make_response(jsonify(new_obj.to_dict()), 200)
