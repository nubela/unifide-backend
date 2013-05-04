from flask import jsonify, request
from base import org


def put_business_info():
    """
    (PUT: business/info)
    """
    desc = request.form.get("description")
    name = request.form.get("name")
    email = request.form.get("email")
    address = request.form.get("address")

    #update it
    org_info_obj = org.get()
    if name is not None:
        org_info_obj.name = name
    if desc is not None:
        org_info_obj.description = desc
    if email is not None:
        org_info_obj.email = email
    if address is not None:
        org_info_obj.address = address
    org.save(org_info_obj)

    return jsonify({
        "status": "ok"
    })


def get_business_info():
    """
    (GET: business/info)
    """
    org_info_obj = org.get()
    return jsonify(org_info_obj.serialize())


def put_business_reservation():
    pass


def get_business_reservation():
    pass


def del_business_reservation():
    pass


def put_business_item():
    pass


def get_business_item():
    pass


def del_business_item():
    pass


def put_business_media():
    pass


def get_business_media():
    pass


def del_business_media():
    pass


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/business/info/',
                     "put_business_info", put_business_info, methods=['PUT'])

    app.add_url_rule('/business/info/',
                     "get_business_info", get_business_info, methods=['GET'])

    app.add_url_rule('/business/reservation/',
                     "put_business_reservation", put_business_reservation, methods=['PUT'])

    app.add_url_rule('/business/reservation/',
                     "get_business_reservation", get_business_reservation, methods=['GET'])

    app.add_url_rule('/business/reservation/',
                     "del_business_reservation", del_business_reservation, methods=['DELETE'])

    app.add_url_rule('/business/item/',
                     "put_business_item", put_business_item, methods=['PUT'])

    app.add_url_rule('/business/item/',
                     "get_business_item", get_business_item, methods=['GET'])

    app.add_url_rule('/business/item/',
                     "del_business_item", del_business_item, methods=['DELETE'])

    app.add_url_rule('/business/media/',
                     "put_business_media", put_business_media, methods=['PUT'])

    app.add_url_rule('/business/media/',
                     "get_business_media", get_business_media, methods=['GET'])

    app.add_url_rule('/business/media/',
                     "del_business_media", del_business_media, methods=['DELETE'])