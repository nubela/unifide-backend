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


def put_account_info():
    """
    (PUT: account/info)
    """
    from unifide_backend.action.cp.action import update_info

    user_id = request.form.get("user_id")
    brand_name = request.form.get("brand_name")
    new_brand_name = request.form.get("new_brand_name")
    email = request.form.get("email")

    update_info(user_id, brand_name, new_brand_name, email)
    print "done"
    return jsonify({"status": "ok"})


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/account/user/',
                     "put_account_user", put_account_user, methods=['PUT'])


    app.add_url_rule('/account/info/',
                     "put_account_info", put_account_info, methods=['PUT'])
