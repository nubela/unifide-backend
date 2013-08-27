from datetime import datetime
from time import mktime
from flask import request, jsonify
from base import items
from base.util import coerce_bson_id
from ecommerce import coupons
from ecommerce.coupons import Coupon


def new_coupon(admin_id, amount, applicable_on, begins_on, container_id, coupon_type, description, ends_on, item_id,
               lifetime_type, min_spending, name, user_applicable, user_groups, user_id, valid_times, coupon_code):
    c = Coupon()
    c.coupon_scope = coupons.CouponScope.ALL_ITEMS
    if applicable_on == "item":
        c.coupon_scope = coupons.CouponScope.ITEM_ONLY
        c.obj_id = coerce_bson_id(item_id)
        c.coll_name = items.Item.coll_name()
    elif applicable_on == "container":
        c.coupon_scope = coupons.CouponScope.CONTAINER_WIDE
        c.obj_id = coerce_bson_id(container_id)
        c.coll_name = items.Container.coll_name()
    if coupon_type == "percentage":
        c.coupon_percentage_off = amount
    elif coupon_type == "absolute":
        c.coupon_value = amount
    c.valid_times = valid_times
    c.order_minimum_spending = min_spending
    c.coupon_lifetime_type = coupons.CouponLifetime.FOREVER
    if lifetime_type == "duration":
        c.coupon_lifetime_type = coupons.CouponLifetime.LIMITED
        c.begins_utc_datetime = datetime.fromtimestamp(
            mktime(datetime.utctimetuple(datetime.strptime(begins_on, "%d/%m/%Y"))))
        c.expire_utc_datetime = c.begins_utc_datetime = datetime.fromtimestamp(
            mktime(datetime.utctimetuple(datetime.strptime(ends_on, "%d/%m/%Y"))))
    c.user_scope = coupons.CouponUserScope.ALL
    if user_applicable == "group":
        c.user_scope = coupons.CouponUserScope.GROUP
        c.user_group = user_groups
    elif user_applicable == "user_specific":
        c.user_id = coerce_bson_id(user_id)
        c.user_scope = coupons.CouponUserScope.SPECIFIC
    c.name = name
    c.description = description
    c.status = coupons.CouponStatus.AVAILABLE
    c.admin_id = admin_id
    c.coupon_code = coupon_code
    c.save()


def put_coupon():
    """
    (PUT: coupon)
    """
    name = request.form.get("name")
    description = request.form.get("description")
    applicable_on = request.form.get("applicable_on")
    item_id = request.form.get("item_id")
    container_id = request.form.get("container_id")
    coupon_type = request.form.get("coupon_type")
    amount = request.form.get("amount")
    min_spending = request.form.get("min_spending")
    lifetime_type = request.form.get("lifetime_type")
    begins_on = request.form.get("begins_on")
    ends_on = request.form.get("ends_on")
    user_applicable = request.form.get("user_applicable")
    user_groups = request.form.get("user_groups")
    user_id = request.form.get("usr_id")
    valid_times = request.form.get("valid_times")
    admin_id = request.form.get("admin_id")
    coupon_code = request.form.get("coupon_code")

    new_coupon(admin_id, amount, applicable_on, begins_on, container_id, coupon_type, description, ends_on, item_id,
               lifetime_type, min_spending, name, user_applicable, user_groups, user_id, valid_times, coupon_code)

    return jsonify({
        "status": "ok",
    })


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/coupon/',
                     "put_coupon", put_coupon, methods=['PUT'])