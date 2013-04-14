from flask.globals import request
from flask.helpers import json, jsonify
from unifide_backend.local_config import FB_APP_ID, FB_APP_SECRET, FB_REDIRECT_URI, FB_PERMS, FB_REALTIME_TOKEN, \
    TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_REDIRECT_URI
import tweepy


def auth_facebook():
    """
    (GET: social_connect/facebook/auth)
    """
    from unifide_backend.action.social.facebook.sdk import auth_url

    verb = "get"
    noun = "social_connect/facebook/auth"

    #auth check
    #to-do

    return jsonify({"status": "ok",
                    "auth_url": auth_url(FB_APP_ID, FB_REDIRECT_URI, FB_PERMS)})


def connect_facebook():
    """
    (PUT: social_connect/facebook)
    """
    from unifide_backend.action.social.facebook.sdk import get_access_token_from_code
    from unifide_backend.action.social.facebook.action import get_fb_id, save_fb_user
    from unifide_backend.action.admin.user.action import get_user

    verb = "put"
    noun = "social_connect/facebook"

    #req_vars
    user_id = request.form.get("user_id")
    facebook_code = request.form.get("code")

    #auth check
    #to-do

    user = get_user(user_id)
    result = get_access_token_from_code(facebook_code, FB_REDIRECT_URI, FB_APP_ID, FB_APP_SECRET)
    access_token, token_expiry = result["access_token"], result["expires"]
    fb_id = get_fb_id(access_token)
    fb_user = save_fb_user(user.get_id(), fb_id, access_token, token_expiry)

    if fb_user is None:
        return jsonify({"status": "error",
                        "error": "Fail to save user access token"})

    return jsonify({"status": "ok"})


def get_facebook_updates():
    """
    (GET: social_connect/facebook/updates)
    """
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    verify_token = request.args.get("hub.verify_token")

    if verify_token != FB_REALTIME_TOKEN or mode != "subscribe":
        return jsonify({"status": "error",
                        "error": "Invalid verification token."})

    return challenge


def put_facebook_updates():
    """
    (POST: social_connect/facebook/updates)
    """
    from unifide_backend.action.social.facebook.action import page_realtime_update

    data = json.loads(request.data)
    object = data["object"]
    entry = data["entry"]

    if object == "page":
        page_realtime_update(entry)

    return jsonify({"status": "ok"})


def get_facebook_pages():
    """
    (GET: social_connect/facebook/page)
    """
    from unifide_backend.action.social.facebook.action import get_fb_user, get_fb_page_list

    verb = "get"
    noun = "social_connect/facebook/page"

    #req_vars
    user_id = request.args.get("user_id")

    #auth check
    #to-do

    fbUser = get_fb_user(user_id)

    return jsonify({"status": "ok",
                    "page_list": get_fb_page_list(fbUser.fb_id, fbUser.access_token)})


def put_facebook_page():
    """
    (PUT: social_connect/facebook/page)
    """
    from unifide_backend.action.social.facebook.action import get_avail_slots, get_fb_user, get_fb_page_list, save_fb_page

    verb = "put"
    noun = "social_connect/facebook/page"

    #req_vars
    user_id = request.form.get("user_id")
    fb_page_id = request.form.get("page_id")

    #auth check
    #to-do

    fbUser = get_fb_user(user_id)

    if fbUser is not None and get_avail_slots(user_id) == 0:
        return jsonify({"status": "error",
                        "error": "Exceeded business subscription limit."})

    page_list = get_fb_page_list(fbUser.fb_id, fbUser.access_token)
    for page in page_list:
        if page["id"] == fb_page_id:
            fbPage_obj = save_fb_page(fbUser.u_id, fbUser.fb_id, page["name"],
                                      page["id"], page["category"], page["access_token"])
            break

    if fbPage_obj is None:
        return jsonify(({"status": "error",
                         "error": "Fail to save page access token"}))

    return jsonify({"status": "ok"})


def auth_twitter():
    """
    (GET: social_connect/twitter/auth)
    """

    verb = "get"
    noun = "social_connect/twitter/auth"

    #auth check
    #to-do

    auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_REDIRECT_URI)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'
        return jsonify({"status": "error",
                        "error": "Failed to get request token."})

    return jsonify({"status": "ok",
                    "auth_url": redirect_url,
                    "request_token": {"oauth_token": auth.request_token.key,
                                      "oauth_token_secret": auth.request_token.secret}})


def connect_twitter():
    """
    (PUT: social_connect/twitter)
    """
    from unifide_backend.action.social.twitter.action import save_tw_user

    verb = "put"
    noun = "social_connect/twitter"

    #auth check
    #to-do

    user_id = request.form.get("user_id")
    verifier = request.form.get("oauth_verifier")
    token = request.form.get("oauth_token")
    token_secret = request.form.get("oauth_token_secret")

    auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
    auth.set_request_token(token, token_secret)

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'
        return jsonify({"status": "error",
                        "error": "Failed to get access token"})

    tw_user = save_tw_user(user_id, auth.access_token.key, auth.access_token.secret)
    if tw_user is None:
        return jsonify({"status": "error",
                        "error": "Failed to save twitter user"})

    return jsonify({"status": "ok"})


def auth_foursquare():
    """
    (GET: social_connect/foursquare)
    """
    from unifide_backend.action.social.foursquare.action import get_auth_url

    verb = "get"
    noun = "social_connect/foursquare"

    #auth check
    #to-do

    return jsonify({"status": "ok",
                    "auth_url": get_auth_url()})


def connect_foursquare():
    """
    (PUT: social_connect/foursquare)
    """
    from unifide_backend.action.social.foursquare.action import get_access_token_from_fsq, save_fsq_user

    verb = "put"
    noun = "social_connect/foursquare"

    #req_vars
    user_id = request.form.get("user_id")
    code = request.form.get("code")

    #auth check
    #to-do

    try:
        fsq_user_obj = save_fsq_user(user_id, get_access_token_from_fsq(code))
    except:
        return jsonify({"status": "error",
                        "error": "Failed to save foursquare user."})

    return jsonify({"status": "ok"})


def get_foursquare_venue():
    """
    (GET: social_connect/foursquare/venue)
    """

    verb = "get"
    noun = "social_connect/foursquare/venue"

    #req_vars
    user_id = request.form.get("user_id")



    return json({"status": "ok",
                 "venues": ""})


def put_foursquare_venue():
    """
    (PUT: social_connect/foursquare/venue)
    """

    verb = "put"
    noun = "social_connect/foursquare/venue"

    #req_vars
    user_id = request.form.get("user_id")
    venue_id = request.form.get("venue_id")

    return jsonify({"status": "ok"})


def google_alerts():
    """
    (PUT: social_connect/google_alerts)
    """

    return "google alerts"


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/social_connect/facebook/auth/',
        "auth_facebook", auth_facebook, methods=['GET'])

    app.add_url_rule('/social_connect/facebook/',
        "connect_facebook", connect_facebook, methods=['PUT'])

    app.add_url_rule('/social_connect/facebook/updates/',
        "get_facebook_updates", get_facebook_updates, methods=['GET'])

    app.add_url_rule('/social_connect/facebook/updates/',
        "put_facebook_updates", put_facebook_updates, methods=['POST'])

    app.add_url_rule('/social_connect/facebook/page/',
        "get_facebook_pages", get_facebook_pages, methods=['GET'])

    app.add_url_rule('/social_connect/facebook/page/',
        "put_facebook_page", put_facebook_page, methods=['PUT'])

    app.add_url_rule('/social_connect/twitter/auth/',
        "auth_twitter", auth_twitter, methods=['GET'])

    app.add_url_rule('/social_connect/twitter/',
        "connect_twitter", connect_twitter, methods=['PUT'])

    app.add_url_rule('/social_connect/foursquare/',
        "auth_foursquare", auth_foursquare, methods=['GET'])

    app.add_url_rule('/social_connect/foursquare/',
        "connect_foursquare", connect_foursquare, methods=['PUT'])

    app.add_url_rule('/social_connect/foursquare/venue/',
        "put_foursquare_venue", put_foursquare_venue, methods=['PUT'])

    app.add_url_rule('/social_connect/google_alerts/',
        "google_alerts", google_alerts, methods=['PUT'])