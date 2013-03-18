from flask.globals import request
from flask.helpers import json, jsonify


def get_overview_facebook():
    pass


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/overview/facebook/',
                     "get_overview_facebook", get_overview_facebook, methods=['GET'])
