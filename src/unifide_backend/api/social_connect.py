from flask.globals import request
from flask.helpers import json, jsonify
from unifide_backend.local_config import FB_APP_ID, FB_APP_SECRET, FB_REDIRECT_URI


def connect_facebook():
    """
    (PUT: social_connect/facebook)
    """
    from unifide_backend.action.social.facebook.action import FacebookAPI, save_fb_oauth
    from base.users.action import get_user

    print "testing facebook"
    verb = "put"
    noun = "social_connect/facebook"

    #req_vars
    user_id = request.form.get("user_id")
    facebook_code = request.form.get("code")

    #auth check
    #to-do

    fb_user = FacebookAPI.generate(facebook_code, FB_APP_ID, FB_APP_SECRET, FB_REDIRECT_URI)
    user = get_user(user_id)
    page_list = fb_user.get_page_list()
    fb_id = fb_user.get_info()["id"]
    #save user access token to user
    fbUser_id = save_fb_oauth(user, fb_user.access_token, fb_id)

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
    from unifide_backend.action.social.facebook.action import FacebookAPI, get_user_token, save_fb_page
    from base.users.action import get_user

    verb = "put"
    noun = "social_connect/facebook/page"

    #req_vars
    user_id = request.form.get("user_id")
    fb_page_id = request.form.get("page_id")

    #auth check
    #to-do

    fb_user = FacebookAPI.new(get_user_token(user_id))
    page_token, page_name = fb_user.get_page_access_token(fb_page_id)
    user = get_user(user_id)
    fbPage_id = save_fb_page(user, fb_page_id, fb_user.access_token, page_token, page_name)

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

    app.add_url_rule('/social_connect/facebook/',
        "connect_facebook", connect_facebook, methods=['GET'])

    app.add_url_rule('/social_connect/facebook/page/',
        "put_facebook_page", put_facebook_page, methods=['PUT'])

    app.add_url_rule('/social_connect/twitter/',
        "connect_twitter", connect_twitter, methods=['PUT'])

    app.add_url_rule('/social_connect/foursquare/',
        "connect_foursquare", connect_foursquare, methods=['PUT'])

    app.add_url_rule('/social_connect/google_alerts/',
        "google_alerts", google_alerts, methods=['PUT'])