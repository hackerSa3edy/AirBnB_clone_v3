#!/usr/bin/python3
"""
This module defines a set of route handlers for the Review object in the
Flask application.
It includes handlers for GET, POST, PUT, and DELETE methods.

Imports:
    Review from models.review: The Review class definition.
    Place from models.place: The Place class definition.
    User from models.user: The User class definition.
    storage from models: The storage engine for the application.
    app_views from api.v1.views: The blueprint for the views of the
    application.
    jsonify, abort, request, make_response from flask: Flask functions for
    handling responses and requests.
"""

from models.review import Review
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/places/<string:place_id>/reviews", methods=["GET"])
def list_reviews(place_id):
    """
    Retrieves all Review objects associated with a specific Place object
    from the storage.

    Args:
        place_id (str): The id of the Place object.

    Returns:
        A JSON list of dictionaries where each dictionary represents a Review
        object if found, otherwise aborts with a 404 error.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all = place.reviews
    return make_response(jsonify(
        [
            obj.to_dict() for obj in all
            ]
        ), 200)


@app_views.route("/reviews/<string:review_id>", methods=["GET"])
def retrieve_review(review_id):
    """
    Retrieves a specific Review object from the storage.

    Args:
        review_id (str): The id of the Review object to retrieve.

    Returns:
        A JSON dictionary representing the Review object if found, otherwise
        aborts with a 404 error.
    """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Deletes a specific Review object from the storage.

    Args:
        review_id (str): The id of the Review object to delete.

    Returns:
        A JSON empty dictionary with a status code 200 if the Review object
        is deleted, otherwise aborts with a 404 error.
    """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """
    Creates a new Review object associated with a specific Place object and
    saves it to the storage.

    Args:
        place_id (str): The id of the Place object.

    Returns:
        A JSON dictionary representing the new Review object if created,
        otherwise returns a JSON error message with a status code 400.
    """
    from models.user import User

    review = storage.get(Place, place_id)
    if not review:
        abort(404)

    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)

    if not params.get('user_id', None):
        return make_response("Missing user_id", 400)

    user = storage.get(User, params.get('user_id', None))
    if not user:
        abort(404)

    if not params.get('text', None):
        return make_response("Missing text", 400)

    params.update({"place_id": place_id})
    newObj = Review(**params)
    newObj.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>", methods=["PUT"])
def update_review(review_id):
    """
    Updates a specific Review object in the storage.

    Args:
        review_id (str): The id of the Review object to update.

    Returns:
        A JSON dictionary representing the updated Review object if updated,
        otherwise returns a JSON error message with a status code 400.
    """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    params = request.get_json(silent=True, cache=False)
    if not params:
        return make_response("Not a JSON", 400)

    params.pop("id", None)
    params.pop("created_at", None)
    params.pop("updated_at", None)
    params.pop("user_id", None)
    params.pop("place_id", None)

    updated_obj = obj.to_dict()
    updated_obj.update(params)
    new_obj = Review(**updated_obj)

    obj.delete()
    new_obj.save()

    return make_response(jsonify(new_obj.to_dict()), 200)
