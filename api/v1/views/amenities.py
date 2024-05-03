#!/usr/bin/python3
"""
This module defines a set of route handlers for the Amenity object in the
Flask application.
It includes handlers for GET, POST, PUT, and DELETE methods.

Imports:
    Amenity from models.amenity: The Amenity class definition.
    storage from models: The storage engine for the application.
    app_views from api.v1.views: The blueprint for the views of
    the application.
    jsonify, abort, request, make_response from flask: Flask functions for
    handling responses and requests.
"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/amenities", methods=["GET"])
def list_amenities():
    """
    Retrieves all Amenity objects from the storage.

    Returns:
        A JSON list of dictionaries where each dictionary represents
        a Amenity object.
    """
    all = storage.all(Amenity)
    return make_response(jsonify(
        [
            obj.to_dict() for obj in all.values()
        ]
    ), 200)


@app_views.route("/amenities/<string:amenity_id>", methods=["GET"])
def retrieve_amenity(amenity_id):
    """
    Retrieves a specific Amenity object from the storage.

    Args:
        amenity_id (str): The id of the Amenity object to retrieve.

    Returns:
        A JSON dictionary representing the Amenity object if found, otherwise
        aborts with a 404 error.
    """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """
    Deletes a specific Amenity object from the storage.

    Args:
        amenity_id (str): The id of the Amenity object to delete.

    Returns:
        A JSON empty dictionary with a status code 200 if the Amenity object is
        deleted, otherwise aborts with a 404 error.
    """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """
    Creates a new Amenity object and saves it to the storage.

    Returns:
        A JSON dictionary representing the new Amenity object if created,
        otherwise returns a JSON error message with a status code 400.
    """
    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)
    if not params.get('name', None):
        return make_response("Missing name", 400)

    newObj = Amenity(**params)
    newObj.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """
    Updates a specific Amenity object in the storage.

    Args:
        amenity_id (str): The id of the Amenity object to update.

    Returns:
        A JSON dictionary representing the updated Amenity object if updated,
        otherwise returns a JSON error message with a status code 400.
    """
    obj = storage.get(Amenity, amenity_id)
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
    new_obj = Amenity(**updated_obj)

    obj.delete()
    new_obj.save()

    return make_response(jsonify(new_obj.to_dict()), 200)
