from flask import request, jsonify
from ecommerce import cashbacks


def new_cashback(admin_id, description, make_active, min_spending, name, perc):
    c = cashbacks.CashbackRule()
    c.description = description
    c.status = cashbacks.CashbackStatus.ENABLED
    c.cashback_percentage = float(perc)
    c.total_minimum_spending = float(min_spending)
    c.name = name
    c.admin_id = admin_id
    if not make_active:
        c.status = cashbacks.CashbackStatus.DISABLED
    c.save()


def put_cashback():
    """
    (PUT = cashback)
    """
    name = request.form.get("name")
    description = request.form.get("description")
    perc = request.form.get("perc")
    min_spending = request.form.get("min_spending")
    admin_id = request.form.get("admin_id")
    make_active = request.form.get("make_active", False)
    new_cashback(admin_id, description, make_active, min_spending, name, perc)

    return jsonify({"status": "ok"})


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/cashback/',
                     "put_cashback", put_cashback, methods=['PUT'])