from flask import request, jsonify
from ecommerce import shipping


def new_shipping_method(admin_id, base_flat_fee, description, from_place, max_weight, min_weight, name,
                        price_per_weight, to):
    s = shipping.ShippingRule()
    s.name = name
    s.description = description
    s.price_per_unit_vol_weight = price_per_weight
    s.flat_price = base_flat_fee
    s.min_unit_vol_weight = min_weight
    s.max_unit_vol_weight = max_weight
    s.from_location = from_place if len(from_place) > 0 else None
    s.to_location = to if len(to) > 0 else None
    s.status = shipping.ShippingStatus.ENABLED
    s.admin_id = admin_id
    s.save()


def put_shipping_method():
    """
    (PUT: tax)
    """
    base_flat_fee = request.form.get("base_flat_fee")
    description = request.form.get("description")
    from_place = request.form.get("from", None)
    max_weight = request.form.get("max_weight")
    min_weight = request.form.get("min_weight")
    name = request.form.get("name")
    price_per_weight = request.form.get("price_per_weight")
    to = request.form.get("to")
    admin_id = request.form.get("admin_id")

    new_shipping_method(admin_id, base_flat_fee, description, from_place, max_weight, min_weight, name,
                        price_per_weight, to)

    return jsonify({"status": "ok"})


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/shipping/',
                     "put_shipping_method", put_shipping_method, methods=['PUT'])