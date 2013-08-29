from flask import request, jsonify
from ecommerce import taxes


def new_tax(admin_id, description, make_active, name, perc):
    t = taxes.TaxRule()
    t.name = name
    t.description = description
    t.tax_perc = perc
    t.status = taxes.TaxStatus.DISABLED
    if make_active:
        t.status = taxes.TaxStatus.ENABLED
    t.admin_id = admin_id
    return t.save()


def put_tax():
    """
    (PUT: tax)
    """
    name = request.form.get("name")
    description = request.form.get("description")
    perc = request.form.get("perc")
    admin_id = request.form.get("admin_id")
    make_active = request.form.get("make_active", False)
    if make_active == "false":
        make_active = False
    new_tax(admin_id, description, make_active, name, perc)

    return jsonify({"status": "ok"})


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/tax/',
                     "put_tax", put_tax, methods=['PUT'])