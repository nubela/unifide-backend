import re
from flask import jsonify, request, redirect
from base import org

def put_business_info():
    """
    (PUT: business/info)
    """
    from unifide_backend.action.mapping.action import get_brand_mapping
    from unifide_backend.action.social.facebook.action import update_page_attr as facebook
    from unifide_backend.action.social.twitter.action import update_profile as twitter
    from unifide_backend.action.social.foursquare.action import update_venue as foursquare

    user_id = request.form.get("user_id")
    brand_name = request.form.get("brand_name")
    desc = request.form.get("description")
    info = request.form.get("info")
    name = request.form.get("name")
    email = request.form.get("email")
    website = request.form.get("website")
    phone = request.form.get("phone")
    address = request.form.get("address")
    redirect_url = request.form.get("redirect_to")

    brand_obj = get_brand_mapping(user_id, brand_name)

    #update it
    org_info_obj = org.get()
    if name is not None:
        org_info_obj.name = name
    if desc is not None:
        org_info_obj.description = desc
    if info is not None:
        org_info_obj.info = info
    if email is not None:
        org_info_obj.email = email
    if website is not None:
        org_info_obj.website = website
    if phone is not None:
        org_info_obj.phone = phone
    if address is not None:
        org_info_obj.address = address
    org.save(org_info_obj)

    #todo: handle errors for each API error
    #update social
    if brand_obj.facebook is not None:
        facebook(brand_obj.facebook["id"], brand_obj.facebook["access_token"],
                 about=org_info_obj.info,
                 description=org_info_obj.description,
                 website=org_info_obj.website,
                 phone=org_info_obj.phone)
    if brand_obj.twitter is not None:
        twitter(brand_obj.twitter["access_token"]["key"], brand_obj.twitter["access_token"]["secret"],
                                    org_info_obj.name, org_info_obj.website, org_info_obj.address, org_info_obj.info)
    if brand_obj.foursquare is not None:
        foursquare(brand_obj.foursquare["venues"][0], brand_obj.foursquare["access_token"],
                                    org_info_obj.name, org_info_obj.address, org_info_obj.phone, org_info_obj.description)

    if redirect_url is not None:
        return redirect(redirect_url, code=303)

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
                     "put_business_info", put_business_info, methods=['PUT', 'POST'])

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