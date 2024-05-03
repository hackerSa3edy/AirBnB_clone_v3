#!/usr/bin/python3
"""
This is the main file for the Flask application.

Modules:
--------
flask: This module is used to create a Flask application instance.
models: This module contains the storage system for the application.
api.v1.views: This module contains the blueprint for the application views.

Variables:
----------
app: This is a Flask application instance.

Functions:
----------
close_db(excep): This function is called when the application context
tears down.

Main Function:
--------------
The main function runs the Flask application on host '0.0.0.0' and port 5000.
It also enables multithreading.

"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(excep):
    """
    This function is called when the application context tears down.
    It closes the storage system.

    Parameters:
    -----------
    excep: Exception
        The exception that was raised (if any).
    """
    storage.close()


@app.errorhandler(404)
def err404(error):
    """
    This function is a route handler for the 404 error in the application.
    It is triggered when a requested resource is not found on the server.

    Args:
        error (werkzeug.exceptions.HTTPException): The error object passed
        by the Flask application.

    Returns:
        A tuple where the first element is a JSON object with a key "error"
        and a value "Not found",
        and the second element is the HTTP status code 404.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """
    The main function runs the Flask application on host '0.0.0.0' and
    port 5000.
    It also enables multithreading.
    """
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=getenv('HBNB_API_PORT', 5000),
        threaded=True
        )
