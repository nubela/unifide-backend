from flask.globals import request
from flask.helpers import json, jsonify


def put_account_user():
    from unifide_backend.action.cp.action import put_new_user_menu
    from unifide_backend.action.mapping.action import put_new_user_mapping

    #req_vars
    user_id = request.form.get("user_id")

    user_menu_obj = put_new_user_menu(user_id)
    if user_menu_obj is None:
        return jsonify({"status": "error",
                        "error": "Failed to add user menu"})

    user_brand_mapping_obj = put_new_user_mapping(user_id)
    if user_brand_mapping_obj is None:
        return jsonify({"status": "error",
                        "error": "Failed to add user brand mapping"})

    return jsonify({"status": "ok"})


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

    app.add_url_rule('/account/user/',
                     "put_account_user", put_account_user, methods=['PUT'])

    app.add_url_rule('/account/password/',
                     "put_account_passwd", put_account_passwd, methods=['PUT'])

    app.add_url_rule('/account/info/',
                     "put_account_info", put_account_info, methods=['PUT'])

    app.add_url_rule('/account/info/',
                     "get_account_info", get_account_info, methods=['GET'])
