from flask.globals import request
from flask.helpers import json, jsonify
from unifide_backend.local_config import FB_APP_ID, FB_APP_SECRET


def connect_facebook():
    """
    (PUT: social_connect/facebook)
    """
    from unifide_backend.action.social.facebook import get_user_access_token, get_page_list
    from unifide_backend.action.user import get_user, save_fb_oauth

    verb = "put"
    noun = "social_connect/facebook"

    #req_vars
    user_id = request.form.get("user_id")
    facebook_code = request.form.get("code")

    #auth check
    #to-do

    user_access_token = get_user_access_token(facebook_code, FB_APP_ID, FB_APP_SECRET)
    user = get_user(user_id)
    page_list, fb_id = get_page_list(user_access_token)
    #save user access token to user
    fbUser_id = save_fb_oauth(user, user_access_token, fb_id)

    if page_list is None:
        return jsonify({"status": "error",
                        "error": "Fail to get list of fb pages"})

    if fbUser_id is None:
        return jsonify({"status": "error",
                        "error": "Fail to save user access token"})

    return jsonify({"status": "ok",
                    "pages": page_list})


def put_facebook_page():
    """
    (PUT: social_connect/facebook/page)
    """
    from unifide_backend.action.social.facebook import get_page_access_token
    from unifide_backend.action.user import get_user, get_user_access_token, save_fb_page

    verb = "put"
    noun = "social_connect/facebook/page"

    #req_vars
    user_id = request.form.get("user_id")
    fb_page_id = request.form.get("page_id")

    #auth check
    #to-do

    user_access_token = get_user_access_token(user_id)
    page_access_token, page_name = get_page_access_token(fb_page_id, user_access_token)
    user = get_user(user_id)
    fbPage_id = save_fb_page(user, fb_page_id, user_access_token, page_access_token, page_name)

    if fbPage_id is None:
        return jsonify(({"status": "error",
                         "error": "Fail to save page access token"}))

    return jsonify({"status": "ok"})


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