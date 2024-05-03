#!/usr/bin/python3
"""
This module defines a set of route handlers for the Amenity object in
the Flask application.
It includes handlers for GET, DELETE, and POST methods.

Imports:
    Amenity from models.amenity: The Amenity class definition.
    Place from models.place: The Place class definition.
    storage from models: The storage engine for the application.
    app_views from api.v1.views: The blueprint for the views of
    the application.
    jsonify, abort, make_response from flask: Flask functions for handling
    responses and requests.
    getenv from os: Function to get the value of an environment variable.
"""

from models.amenity import Amenity
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response
from os import getenv


db_type = getenv('HBNB_TYPE_STORAGE', 'file')


@app_views.route("/places/<string:place_id>/amenities", methods=["GET"])
def list_amenities_in_place(place_id):
    """
    Retrieves all Amenity objects associated with a specific Place object
    from the storage.

    Args:
        place_id (str): The id of the Place object.

    Returns:
        A JSON list of dictionaries where each dictionary represents an
        Amenity object if found, otherwise aborts with a 404 error.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all = place.amenities
    return make_response(jsonify(
        [
            obj.to_dict() if db_type != 'file' else obj for obj in all
            ]
        ), 200)


@app_views.route(
    "/places/<string:place_id>/amenities/<string:amenity_id>",
    methods=["DELETE"]
    )
def delete_amenity_of_place(place_id, amenity_id):
    """
    Deletes a specific Amenity object associated with a specific Place object
    from the storage.

    Args:
        place_id (str): The id of the Place object.
        amenity_id (str): The id of the Amenity object to delete.

    Returns:
        A JSON empty dictionary with a status code 200 if the Amenity object
        is deleted, otherwise aborts with a 404 error.
    """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)

    if amenity_obj not in place_obj.amenities:
        abort(404)

    amenity_obj.delete()
    place_obj.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/places/<string:place_id>/amenities/<string:amenity_id>",
    methods=["POST"]
    )
def link_amenity_to_place(place_id, amenity_id):
    """
    Links a new Amenity object to a specific Place object and saves it
    to the storage.

    Args:
        place_id (str): The id of the Place object.
        amenity_id (str): The id of the Amenity object to link.

    Returns:
        A JSON dictionary representing the new Amenity object if linked,
        otherwise aborts with a 404 error.
    """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)

    if amenity_obj in place_obj.amenities:
        return make_response(jsonify(amenity_obj.to_dict()), 200)

    place_obj.amenities.append(amenity_obj)
    place_obj.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)
