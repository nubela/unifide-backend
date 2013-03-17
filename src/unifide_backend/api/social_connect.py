from flask.globals import request
from flask.helpers import json, jsonify
from unifide_backend.local_config import FB_APP_ID, FB_APP_SECRET


def connect_facebook():
    """
    (PUT: social_connect/facebook)
    """
    from unifide_backend.action.social.facebook import get_user_access_token, get_page_list

    verb = "put"
    noun = "social_connect/facebook"

    #req_vars
    user_id = request.form.get("user_id")
    facebook_code = request.form.get("code")

    #auth check
    #to-do

    user_access_token = get_user_access_token(facebook_code, FB_APP_ID, FB_APP_SECRET)
    page_list = get_page_list(user_access_token)

    return jsonify({"status": "ok",
                    "pages": page_list})


def put_facebook_page():
    """
    (PUT: social_connect/facebook/page)
    """
    from unifide_backend.action.social.facebook import save_page_access_token

    verb = "put"
    noun = "social_connect/facebook/page"

    #req_vars
    user_id = request.form.get("user_id")
    fb_page_id = request.form.get("page_id")

    #auth check
    #to-do

    page_access_token = save_page_access_token(fb_page_id)


    return ""


def connect_twitter():
    """
    (PUT: social_connect/twitter)
    """

    return "twitter"


def connect_foursquare():
    """
    (PUT: social_connect/foursquare)
    """

    return "foursquare"

def google_alerts():
    """
    (PUT: social_connect/google_alerts)
    """

    return "google alerts"

def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/social_connect/facebook',
        "connect_facebook", connect_facebook, methods=['PUT'])

    app.add_url_rule('/social_connect/facebook/page',
        "put_facebook_page", put_facebook_page, methods=['PUT'])

    app.add_url_rule('/social_connect/twitter',
        "connect_twitter", connect_twitter, methods=['PUT'])

    app.add_url_rule('/social_connect/foursquare',
        "connect_foursquare", connect_foursquare, methods=['PUT'])

    app.add_url_rule('/social_connect/google_alerts',
        "google_alerts", google_alerts, methods=['PUT'])