from flask import jsonify, request, render_template
import orders


def get_order():
    """
    (GET: order)
    """
    all_orders = orders.Order.collection().find({})
    all_order_objs = [orders.Order.unserialize(dic) for dic in all_orders]
    order_lis = [x.serialize(json_friendly=True) for x in all_order_objs]
    return jsonify({
        "status": "ok",
        "orders": order_lis,
    })


def post_order_status():
    order_id = request.form.get("order_id")
    status = request.form.get("status")
    priv8_note = request.form.get("private_note")
    pub_note = request.form.get("public_note")
    redirect_url = request.form.get("redirect_to")

    order_obj = orders.get(order_id)
    order_obj.status = status
    order_obj.status_public_notes = pub_note
    order_obj.status_private_notes = priv8_note
    orders.save(order_obj)

    if redirect_url:
        return render_template("redirect.html", **{
            "redirect_url": redirect_url
        })

    return jsonify({"status": "ok"})


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/order/',
                     "get_order", get_order, methods=['GET'])

    app.add_url_rule('/order/status/',
                     "post_order_status", post_order_status, methods=['POST'])