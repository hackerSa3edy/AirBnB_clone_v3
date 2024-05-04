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
from models.state import State
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify, abort, request, make_response


@app_views.route("/cities/<string:city_id>/places", methods=["GET"])
def list_places(city_id):
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
def retrieve_place(place_id):
    """
    Retrieves a specific Place object from the storage.

    Args:
        place_id (str): The id of the Place object to retrieve.

    Returns:
        A JSON dictionary representing the Place object if found, otherwise
        aborts with a 404 error.
    """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/places/<string:place_id>", methods=["DELETE"])
def delete_place(place_id):
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
def create_place(city_id):
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

    city = storage.get(City, city_id)
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
def update_place(place_id):
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


@app_views.route('/places_search', methods=["POST"])
def search_places():
    """
    Searches for Place objects that match the criteria specified in the
    request body.

    The request body should be a JSON object that may contain the keys
    "states", "cities", and "amenities".
    The value for each key should be a list of ids representing State,
    City, and Amenity objects respectively.

    If the request body is empty, all Place objects are returned.

    If the request body is not a JSON, returns a JSON error message with
    a status code 400.

    Args:
        None

    Returns:
        A JSON list of dictionaries where each dictionary represents a Place
        object that matches the search criteria.
    """
    req_body = request.get_json(silent=True, cache=False)
    if req_body is None:
        return make_response("Not a JSON", 400)

    all_places = []
    if len(req_body) != 0:
        states = req_body.get("states", [])
        cities = req_body.get("cities", [])
        amenities = req_body.get("amenities", [])

        if len(states) != 0 and type(states) is list:
            for state_id in states:
                state_obj = storage.get(State, state_id)
                if state_obj:
                    for city in state_obj.cities:
                        all_places.extend(city.places)
        if len(cities) != 0 and type(cities) is list:
            for city_id in cities:
                city_obj = storage.get(City, city_id)
                if city_obj:
                    all_places.extend(city_obj.places)

        all_places = set(all_places)
        all_places = list(all_places)

        if len(states) == 0 and len(cities) == 0:
            all_places.extend(storage.all(Place).values())

        if len(amenities) != 0 and type(amenities) is list:
            amenities = [
                storage.get(Amenity, amenity_id) for amenity_id in amenities if storage.get(
                    Amenity,
                    amenity_id
                    )
                ]
            filtered_places = []
            storage_t = getenv('HBNB_TYPE_STORAGE')
            for place in all_places:
                if storage_t == 'db':
                    place_amenities = place.amenities
                else:
                    place_amenities = place.amenity_ids

                for amenity in place_amenities:
                    if amenity in amenities:
                        filtered_places.append(place)
                        break
            del all_places
            all_places = filtered_places
    else:
        all_places.extend(storage.all(Place).values())

    return make_response(jsonify(
        [
            obj.to_dict() if type(obj) is not dict else obj
            for obj in all_places
            ]
    ), 200)
