#!/usr/bin/python3
"""
This is the initialization file for the Flask application views.

Modules:
--------
flask: This module is used to create a Blueprint for the application views.

Blueprint:
----------
app_views:
    This is a Blueprint instance that represents the application views.
    It is named 'app_views' and has a URL prefix of '/api/v1'.

Imports:
--------
api.v1.views.index:
    This module contains the routes and views for the application.
    All its contents are imported into this module.
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.places import *
