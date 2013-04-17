from flask.globals import request
from flask.helpers import json, jsonify

PLATFORM_CAMPAIGN = "campaign"
PLATFORM_FACEBOOK = "facebook"
PLATFORM_TWITTER = "twitter"
PLATFORM_FOURSQUARE = "foursquare"
PLATFORM_PUSH = "push"

def put_campaign_media():
    pass


def put_campaign_data():
    from campaigns.campaign.model import Campaign
    from campaigns.campaign.action import save
    from unifide_backend.action.mapping.action import put_mapping, get_brand_mapping
    from unifide_backend.action.social.facebook.action import put_fb_post

    user_id = request.form.get("user_id")
    brand_id = request.form.get("brand_id")
    platforms = request.form.get("platforms")
    title = request.form.get("title")
    description = request.form.get("description")
    type = request.form.get("type")
    datetime = request.form.get("datetime")
    place = request.form.get("place")
    is_published = request.form.get("is_published")
    is_draft = request.form.get("is_draft")
    item_list = request.form.get("item_list")

    kvp = {}
    if PLATFORM_CAMPAIGN in platforms:
        c = Campaign()
        c.uid = user_id
        c.title = title
        c.description = description
        c.type = type
        c._id = save(c)
        c.item_id_lis = item_list

        kvp["campaign_list"] = c._id

    if PLATFORM_FACEBOOK in platforms:
        fb_post = put_fb_post(get_brand_mapping(user_id, brand_id).facebook, title)
        kvp["facebook_list"] = fb_post._id

    if PLATFORM_TWITTER in platforms:
        tw_tweet = ""
        kvp["twitter_list"] = tw_tweet._id

    if PLATFORM_FOURSQUARE in platforms:
        fsq_tip = ""
        kvp["foursquare_list"] = fsq_tip._id

    if PLATFORM_PUSH in platforms:
        # todo: push notification
        pass

    publish_datetime = datetime.datetime.now() if is_published is True else None
    put_mapping(user_id, kvp, publish_datetime, is_published, is_draft)

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