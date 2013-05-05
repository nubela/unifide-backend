from flask import jsonify
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


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/order/',
                     "get_order", get_order, methods=['GET'])