from flask.globals import request
from flask.helpers import json, jsonify
from base import users
from base.util import coerce_bson_id


def put_account_user():
    from unifide_backend.action.cp.action import put_new_menu
    from unifide_backend.action.mapping.action import put_new_user_mapping

    #req_vars
    user_id = request.form.get("user_id")

    user_menu_obj = put_new_menu()
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


def new_user(_id, address, email, first_name, last_name, middle_name, password, status, user_groups, username):
    u = users.User()
    if _id is not None:
        u = users.get(_id)
    u.username = username
    u.first_name = first_name
    u.middle_name = middle_name
    u.last_name = last_name
    u.email = email
    u.address = address
    u.groups = user_groups if user_groups is not None else []
    u.account_status = status
    u._id = u.save()

    if len(password) > 0:
        users.set_passwd(u, password)


def put_user():
    """
    (PUT: user)
    """
    _id = coerce_bson_id(request.form.get("_id"))
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    middle_name = request.form.get("middle_name")
    last_name = request.form.get("last_name")
    address = request.form.get("address")
    user_groups = json.loads(request.form.get("user_groups"))
    status = request.form.get("status")

    new_user(_id, address, email, first_name, last_name, middle_name, password, status, user_groups, username)

    return jsonify({
        "status": "ok",
    })


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/user/',
                     "put_user", put_user, methods=['PUT'])

    app.add_url_rule('/account/user/',
                     "put_account_user", put_account_user, methods=['PUT'])

    app.add_url_rule('/account/info/',
                     "put_account_info", put_account_info, methods=['PUT'])
