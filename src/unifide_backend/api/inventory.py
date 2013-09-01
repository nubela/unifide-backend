from flask import request, jsonify
from base.util import coerce_bson_id
from ecommerce import inventory


def put_inventory_container():
    """
    (PUT: inventory/container)
    """
    container_id = coerce_bson_id(request.form.get("container_id"))
    inventory.add_to_inventory(container_id)
    return jsonify({"status": "ok"})


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/inventory/container/',
                     "put_inventory_container", put_inventory_container, methods=['PUT'])