from flask.globals import request
from flask.helpers import json, jsonify


def put_account_passwd():
    pass


def put_account_info():
    pass


def get_account_info():
    pass


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/account/password/',
                     "put_account_passwd", put_account_passwd, methods=['PUT'])

    app.add_url_rule('/account/info/',
                     "put_account_info", put_account_info, methods=['PUT'])

    app.add_url_rule('/account/info/',
                     "get_account_info", get_account_info, methods=['GET'])
