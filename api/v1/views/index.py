#!/usr/bin/python3
"""
This is the main file for the Flask application.

Modules:
--------
api.v1.views: This module contains the blueprint for the application views.
flask: This is the main Flask module.

Routes:
-------
/status: This route returns the status of the application.

Functions:
----------
status(): This function returns a JSON response with the status of
the application.
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """
    This function is linked to the '/status' route.

    Returns:
    --------
    json: A JSON response with the status of the application.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def count():
    """
    This function is a route handler for the "/stats" endpoint.
    It counts the number of instances for each object type in the storage.

    The object types are: Amenity, City, Place, Review, State, and User.

    Returns:
        A JSON object where the keys are the names of the object types and
        the values are the counts of instances for each type.
    """
    objN = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }

    obj_counts = {
        key: storage.count(value) for key, value in objN.items()
        }
    return jsonify(obj_counts)
