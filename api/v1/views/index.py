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
from flask import jsonify


@app_views.route("/status")
def status():
    """
    This function is linked to the '/status' route.

    Returns:
    --------
    json: A JSON response with the status of the application.
    """
    return jsonify({"status": "OK"})
