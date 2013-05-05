import datetime

from flask.globals import request
from flask.helpers import json, jsonify

PLATFORM_CAMPAIGN = "web"
PLATFORM_FACEBOOK = "facebook"
PLATFORM_TWITTER = "twitter"
PLATFORM_FOURSQUARE = "foursquare"
PLATFORM_PUSH = "push"
PLATFORM_BLOG = "blog"


def put_campaign_media():
    """
    (PUT: campaign/media)
    """

    #req_vars
    user_id = request.form.get("user_id")
    brand_name = request.form.get("brand_name")
    print user_id

    return jsonify({"status": "ok"})


def put_campaign_data():
    """
    (PUT: campaign/data)
    """
    from campaigns.campaign.model import Campaign, CampaignType
    from campaigns.campaign.action import save
    from unifide_backend.action.mapping.model import CampaignState
    from unifide_backend.action.mapping.action import put_mapping, get_brand_mapping
    from unifide_backend.action.social.facebook.action import put_fb_post, get_fb_user, put_fb_event
    from unifide_backend.action.social.twitter.action import put_tweet, get_tw_user
    from unifide_backend.action.social.foursquare.action import put_fsq_update

    user_id = request.form.get("user_id")
    brand_name = request.form.get("brand_name")
    platforms = request.form.get("platform")
    type = request.form.get("type")
    title = request.form.get("title")
    description = request.form.get("description")
    event_datetime_start = float(request.form.get("datetime_start")) if request.form.get("datetime_start") is not None else None
    event_datetime_end = float(request.form.get("datetime_end")) if request.form.get("datetime_end") is not None else None
    place = request.form.get("place")
    item_list = request.form.get("item_list")
    state = request.form.get("state")
    scheduled_datetime = float(request.form.get("scheduled_datetime")) if state == CampaignState.SCHEDULED else None

    brand_obj = get_brand_mapping(user_id, brand_name)
    platforms = platforms.split(",")

    kvp = {}
    if PLATFORM_CAMPAIGN in platforms:
        c = Campaign()
        c.uid = user_id
        c.title = title
        c.description = description
        c.type = type
        c.item_id_lis = item_list
        #event component
        c.happening_datetime_start = event_datetime_start if event_datetime_start is not None else None
        c.happening_datetime_end = event_datetime_end if event_datetime_end is not None else None
        c._id = save(c)
        kvp["campaign"] = c._id
        print "done campaign"

    if PLATFORM_FACEBOOK in platforms:
        fb_user = get_fb_user(user_id, brand_name)
        if type == CampaignType.PROMOTION:
            post = put_fb_post(brand_obj.facebook, fb_user.fb_id, state, title)
            kvp[PLATFORM_FACEBOOK] = post._id
        elif type == CampaignType.EVENT:
            event = put_fb_event(brand_obj.facebook, fb_user.fb_id, state, title, description, event_datetime_start, event_datetime_end)
            kvp[PLATFORM_FACEBOOK] = event._id
        print "done facebook"

    if PLATFORM_TWITTER in platforms:
        tw_user = get_tw_user(user_id, brand_name)[0]
        tweet = put_tweet(title, tw_user.tw_id, brand_obj.twitter["access_token"]["key"], brand_obj.twitter["access_token"]["secret"], state)
        kvp[PLATFORM_TWITTER] = tweet._id
        print "done twitter"

    if PLATFORM_FOURSQUARE in platforms:
        #todo : error accessing API endpoint for page updates
        #page_update = put_fsq_update(title, brand_obj.foursquare["venues"][0], brand_obj.foursquare["access_token"], state)
        print "done foursquare"

    if PLATFORM_BLOG in platforms:
        #todo : waiting for articles implementation
        pass

    if PLATFORM_PUSH in platforms:
        #todo : waiting for push implementation
        pass

    publish_datetime = datetime.datetime.now() if state == CampaignState.PUBLISHED else datetime.datetime.fromtimestamp(scheduled_datetime)
    put_mapping(user_id, brand_name, kvp, publish_datetime, type, state)

    return jsonify({"status": "ok"})


def update_campaign_data():
    pass


def get_campaign():
    pass


def del_campaign():
    pass


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/campaign/media/',
                     "put_campaign_media", put_campaign_media, methods=['PUT'])

    app.add_url_rule('/campaign/data/',
                     "put_campaign_data", put_campaign_data, methods=['PUT'])

    app.add_url_rule('/campaign/data/update/',
                     "update_campaign_data", update_campaign_data, methods=['PUT'])

    app.add_url_rule('/campaign/',
                     "get_campaign", get_campaign, methods=['GET'])

    app.add_url_rule('/campaign/',
                     "del_campaign", del_campaign, methods=['DELETE'])