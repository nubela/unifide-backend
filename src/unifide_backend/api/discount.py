from datetime import datetime
from time import mktime
from flask import request, jsonify
from base import items
from base.util import coerce_bson_id
from ecommerce import discounts


def _new_discount(admin_id, amount, applicable_on, begins_on, container_id, description, discount_type, duration,
                  ends_on, item_id, min_order, name):
    #create discount obj
    discount_obj = discounts.Discount()
    discount_obj.name = name
    discount_obj.description = description
    discount_obj.status = discounts.DiscountStatus.ENABLED
    discount_obj.admin_id = admin_id
    discount_obj.discount_scope = discounts.DiscountScope.ALL_ITEMS
    if applicable_on == "item":
        discount_obj.discount_scope = discounts.DiscountScope.ITEM_ONLY
        discount_obj.obj_id = coerce_bson_id(item_id)
        discount_obj.coll_name = items.Item.coll_name()
    elif applicable_on == "container":
        discount_obj.discount_scope = discounts.DiscountScope.CONTAINER_WIDE
        discount_obj.obj_id = coerce_bson_id(container_id)
        discount_obj.coll_name = items.Container.coll_name()
    if discount_type == "percentage":
        discount_obj.discount_percentage = float(amount)
    elif discount_type == "absolute":
        discount_obj.absolute_discounted_price = float(amount)
    discount_obj.order_minimum_spending = float(min_order)
    discount_obj.discount_lifetime_type = discounts.DiscountLifetime.FOREVER
    if duration == "duration":
        discount_obj.discount_lifetime_type = discounts.DiscountLifetime.LIMITED
        discount_obj.begins_utc_datetime = datetime.fromtimestamp(
            mktime(datetime.utctimetuple(datetime.strptime(begins_on, "%d/%m/%Y"))))
        discount_obj.expire_utc_datetime = datetime.fromtimestamp(
            mktime(datetime.utctimetuple(datetime.strptime(ends_on, "%d/%m/%Y"))))
    discount_obj._id = discount_obj.save()
    return discount_obj


def put_discount():
    """
    (PUT: discount)
    """
    name = request.form.get("name")
    description = request.form.get("description")
    applicable_on = request.form.get("applicable_on")
    item_id = request.form.get("item_id")
    container_id = request.form.get("container_id")
    discount_type = request.form.get("discount_type")
    amount = request.form.get("amount")
    min_order = request.form.get("min_order")
    duration = request.form.get("duration")
    begins_on = request.form.get("begins_on")
    ends_on = request.form.get("ends_on")
    admin_id = request.form.get("admin_id")

    _new_discount(admin_id, amount, applicable_on, begins_on, container_id, description, discount_type,
                                 duration, ends_on, item_id, min_order, name)

    return jsonify({
        "status": "ok",
    })


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/discount/',
                     "put_discount", put_discount, methods=['PUT'])