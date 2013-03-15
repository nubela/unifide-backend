from flask.globals import request
from flask.helpers import json, jsonify


def connect_facebook():
    """
    (PUT: facebook/connect)
    """

    return "works"


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/facebook/connect',
        "connect_facebook", connect_facebook, methods=['PUT'])