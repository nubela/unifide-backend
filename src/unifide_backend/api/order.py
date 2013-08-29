from flask import request, jsonify, json
from base.util import coerce_bson_id
import orders
from orders.order.support import apply_shipping, apply_coupon, apply_tax, apply_discounts


def put_order():
    """
    (PUT: order)
    """
    items_lis = json.loads(request.form.get("items"))
    admin_notes = request.form.get("admin_notes")
    user_notes = request.form.get("user_notes")
    status = request.form.get("status")
    user_id = request.form.get("user_id")
    admin_id = request.form.get("admin_id")

    #actionables
    apply_shipping_id = request.form.get("shipping_method", None)
    apply_coupon_code = request.form.get("apply_coupon", None)
    apply_debits_credits = request.form.get("apply_debits_credits", False)
    if apply_debits_credits == "false":
        apply_coupon_code = False
    elif apply_debits_credits == "true":
        apply_coupon_code = True

    o = orders.Order()
    o.user_id = user_id
    o.status = status
    o.items = [{"obj_id": coerce_bson_id(x["obj_id"]), "quantity": float(x["quantity"])} for x in items_lis]
    o.request_notes = user_notes
    o.admin_notes = admin_notes
    o.admin_id = admin_id
    if apply_shipping_id is not None and len(apply_shipping_id) > 0:
        apply_shipping(o, apply_shipping_id)
    if apply_coupon_code is not None and len(apply_coupon_code) > 0:
        apply_coupon(o, apply_coupon_code)

    if apply_debits_credits:
        #apply taxes and discounts
        apply_discounts(o)
        apply_tax(o)

    o.save()

    return jsonify({
        "status": "ok",
    })


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/order/',
                     "put_order", put_order, methods=['PUT', 'POST'])
