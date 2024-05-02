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

from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
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


if __name__ == '__main__':
    """
    The main function runs the Flask application on host '0.0.0.0' and
    port 5000.
    It also enables multithreading.
    """
    app.run(host='0.0.0.0', port=5000, threaded=True)
