#!/usr/bin/python3
"""
This module defines a set of route handlers for the City object in the
Flask application.
It includes handlers for GET, POST, PUT, and DELETE methods.

Imports:
    City from models.city: The City class definition.
    Place from models.city: The Place class definition.
    storage from models: The storage engine for the application.
    app_views from api.v1.views: The blueprint for the views of
    the application.
    jsonify, abort, request, make_response from flask: Flask functions for
    handling responses and requests.
"""

from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/cities/<string:city_id>/places", methods=["GET"])
def list_cities(city_id):
    """
    Retrieves all places objects associated with a specific City object from
    the storage.

    Args:
        city_id (str): The id of the City object.

    Returns:
        A JSON list of dictionaries where each dictionary represents a Place
        objects if found, otherwise aborts with a 404 error.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    all = city.places
    return make_response(jsonify(
        [
            obj.to_dict() for obj in all
            ]
        ), 200)


@app_views.route("/places/<string:place_id>", methods=["GET"])
def retrieve_city(place_id):
    """
    Retrieves a specific Place object from the storage.

    Args:
        place_id (str): The id of the Place object to retrieve.

    Returns:
        A JSON dictionary representing the Place object if found, otherwise
        aborts with a 404 error.
    """
    obj = storage.get(City, place_id)
    if not obj:
        abort(404)
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/places/<string:place_id>", methods=["DELETE"])
def delete_city(place_id):
    """
    Deletes a specific Place object from the storage.

    Args:
        place_id (str): The id of the Place object to delete.

    Returns:
        A JSON empty dictionary with a status code 200 if the Place object is
        deleted, otherwise aborts with a 404 error.
    """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<string:city_id>/places", methods=["POST"])
def create_city(city_id):
    """
    Creates a new Place object associated with a specific City object and
    saves it to the storage.

    Args:
        city_id (str): The id of the City object.

    Returns:
        A JSON dictionary representing the new Place object if created,
        otherwise returns a JSON error message with a status code 400.
    """
    from models.user import User

    city = storage.get(Place, city_id)
    if not city:
        abort(404)

    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)

    if not params.get('user_id', None):
        return make_response("Missing user_id", 400)

    user = storage.get(User, params.get('user_id', None))
    if not user:
        abort(404)

    if not params.get('name', None):
        return make_response("Missing name", 400)

    params.update({"city_id": city_id})
    newObj = Place(**params)
    newObj.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=["PUT"])
def update_city(place_id):
    """
    Updates a specific Place object in the storage.

    Args:
        place_id (str): The id of the Place object to update.

    Returns:
        A JSON dictionary representing the updated Place object if updated,
        otherwise returns a JSON error message with a status code 400.
    """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)

    params.pop("id", None)
    params.pop("city_id", None)
    params.pop("created_at", None)
    params.pop("updated_at", None)
    params.pop("user_id", None)

    updated_obj = obj.to_dict()
    updated_obj.update(params)
    new_obj = Place(**updated_obj)

    obj.delete()
    new_obj.save()

    return make_response(jsonify(new_obj.to_dict()), 200)