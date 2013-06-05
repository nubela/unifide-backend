import datetime
import traceback
import Image
import re

from StringIO import StringIO
from flask import redirect
from flask.globals import request
from flask.helpers import json, jsonify
from base.util import coerce_bson_id

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
    from base.media.action import store_locally, url_for
    from base.media.model import Media
    from base.items.model import Item
    from unifide_backend.action.util import url_generator
    from cfg import DOMAIN_PATH

    user_id = request.form.get("user_id")
    brand_name = request.form.get("brand_name")
    platforms = request.form.getlist("platforms")
    type = request.form.get("type")
    title = request.form.get("title")
    description = request.form.get("description")
    event_datetime_start = float(request.form.get("datetime_start")) if request.form.get("datetime_start") is not None else None
    event_datetime_end = float(request.form.get("datetime_end")) if request.form.get("datetime_end") is not None else None
    item_file_id = request.form.get("media_file_url", None)
    state = request.form.get("state")
    scheduled_datetime = float(request.form.get("scheduled_datetime")) if state == CampaignState.SCHEDULED else None
    redirect_url = request.form.get("redirect_to", None)

    brand_obj = get_brand_mapping(user_id, brand_name)

    parsed_title = title
    parsed_description = description
    image_io = None
    file_path = None
    media_obj = None

    # load media object from item ID
    if item_file_id:
        dic = Item.collection().find_one({"_id": coerce_bson_id(item_file_id)})
        item_obj = Item.unserialize(dic) if dic is not None else None
        if item_obj:
            media_obj = Media.unserialize(Media.collection().find_one({"_id": item_obj.media_id}))

    # load user uploaded image
    files = ["media_file"]
    for f in files:
        media_file = request.files.get(f)
        if media_file.filename != "":
            if request.files.get("media_file").mimetype in ["image/png", "image/gif", "image/jpeg", "image/jpg"]:
                file_path = store_locally(media_file.filename, media_file)

    # open file stream to user uploaded image
    if file_path:
        image = Image.open(file_path)
        image_io = StringIO()
        image.save(image_io, 'jpeg', quality=95)
        image_io.seek(0)
    # open file stream to item image
    if media_obj:
        image = Image.open(url_for(media_obj))
        image_io = StringIO()
        image.save(image_io, 'jpeg', quality=95)
        image_io.seek(0)

    kvp = {}
    if PLATFORM_CAMPAIGN in platforms or PLATFORM_BLOG in platforms:
        c = Campaign()
        c.uid = user_id
        c.title = title
        c.description = description
        c.type = type
        if item_file_id is not None:
            c.item_id_lis.append(item_file_id)
        #event component
        c.happening_datetime_start = event_datetime_start if event_datetime_start is not None else None
        c.happening_datetime_end = event_datetime_end if event_datetime_end is not None else None
        c._id = save(c)

    if PLATFORM_CAMPAIGN in platforms:
        kvp["campaign"] = c._id
        print "done campaign"

    if PLATFORM_BLOG in platforms:
        kvp["blog"] = c._id
        print "done blog"

    # add a link to web/blog campaign for social network campaigns
    if PLATFORM_CAMPAIGN in platforms or PLATFORM_BLOG in platforms:
        parsed_title += "\n" + url_generator(DOMAIN_PATH, title)
        parsed_description += "\n\n" + url_generator(DOMAIN_PATH, title)

    if PLATFORM_FACEBOOK in platforms:
        fb_user = get_fb_user(user_id, brand_name)
        if type == CampaignType.PROMOTION:
            post = put_fb_post(brand_obj.facebook, fb_user.fb_id, state, parsed_title, image_io)
            kvp[PLATFORM_FACEBOOK] = post._id
        elif type == CampaignType.EVENT:
            event = put_fb_event(brand_obj.facebook, fb_user.fb_id, state, title, parsed_description, event_datetime_start, event_datetime_end, image_io)
            kvp[PLATFORM_FACEBOOK] = event._id
        print "done facebook"

    if PLATFORM_TWITTER in platforms:
        tw_user = get_tw_user(user_id, brand_name)[0]
        tweet = put_tweet(parsed_title, tw_user.tw_id, brand_obj.twitter["access_token"]["key"], brand_obj.twitter["access_token"]["secret"], state, url_for(media_obj) if media_obj is not None else file_path)
        kvp[PLATFORM_TWITTER] = tweet._id
        print "done twitter"

    if PLATFORM_FOURSQUARE in platforms:
        page_update = put_fsq_update(parsed_title, brand_obj.foursquare["venues"][0], brand_obj.foursquare["access_token"], state)
        kvp[PLATFORM_FOURSQUARE] = page_update._id
        print "done foursquare"

    if PLATFORM_PUSH in platforms:
        kvp[PLATFORM_PUSH] = 1
        #todo : waiting for push implementation
        pass

    publish_datetime = datetime.datetime.now() if state == CampaignState.PUBLISHED else datetime.datetime.fromtimestamp(scheduled_datetime)
    put_mapping(user_id, brand_name, kvp, publish_datetime, type, state)

    if redirect_url is not None:
        return redirect(redirect_url)

    return jsonify({"status": "ok"})


def update_campaign_data():
    """
    (PUT: /campaign/date/update)
    """
    from campaigns.campaign.model import Campaign
    from unifide_backend.action.mapping.action import get_brand_mapping, get_mapping
    from unifide_backend.action.social.facebook.model import FBEvent
    from unifide_backend.action.social.facebook.action import update_fb_event

    user_id = request.form.get("user_id")
    brand_name = request.form.get("brand_name")
    campaign_id = request.form.get('campaign_id')
    title = request.form.get('title')
    description = request.form.get('description')
    event_datetime_start = float(request.form.get("datetime_start")) if request.form.get("datetime_start") is not None else None
    event_datetime_end = float(request.form.get("datetime_end")) if request.form.get("datetime_end") is not None else None
    place = request.form.get("place")
    item_list = request.form.get("item_list")
    print title, description
    print campaign_id
    brand_obj = get_brand_mapping(user_id, brand_name)
    mapping_obj = get_mapping(campaign_id)
    print brand_obj
    print mapping_obj

    if mapping_obj.campaign is not None:
        Campaign.collection().update({"_id": mapping_obj.campaign},
                                     {"$set" : { "title": title,
                                                 "description": description,
                                                 "item_id_lis": item_list,
                                                 "happening_datetime_start": event_datetime_start,
                                                 "happening_datetime_end": event_datetime_end}
                                     })
    if mapping_obj.blog is not None:
        Campaign.collection().update({"_id": mapping_obj.blog},
                                     {"$set" : { "title": title,
                                                 "description": description,
                                                 "item_id_lis": item_list,
                                                 "happening_datetime_start": event_datetime_start,
                                                 "happening_datetime_end": event_datetime_end}
                                     })
    if mapping_obj.facebook is not None and mapping_obj.type == "event":
        event = FBEvent.collection().find_one({"_id": coerce_bson_id(mapping_obj.facebook)})
        update_fb_event(event["event_id"], brand_obj.facebook, mapping_obj.state, title, description, event_datetime_start, event_datetime_end)

    return jsonify({"status": "ok"})


def get_item_url():
    """
    (GET: /campaign/item/url)
    """
    from base.media.action import url_for
    from base.media.model import Media
    from base.items.model import Item

    obj_id = request.args.get("obj_id")
    item_obj = Item.unserialize(Item.collection().find_one({"_id": coerce_bson_id(obj_id)}))
    media_obj = Media.unserialize(Media.collection().find_one({"_id": item_obj.media_id}))

    if media_obj is None:
        return jsonify({"status": "error",
                        "error": "No item found"})
    item_url = url_for(media_obj)

    return jsonify({"status": "ok",
                    "url": item_url})


def del_campaign():
    """
    (DELETE: /campaign)
    """
    from campaigns.campaign.model import Campaign
    from unifide_backend.action.social.facebook.model import FBPost, FBEvent
    from unifide_backend.action.social.twitter.model import TWTweet
    from unifide_backend.action.social.foursquare.model import FSQPageUpdate
    from unifide_backend.action.mapping.action import del_mapping, get_brand_mapping, get_mapping
    from unifide_backend.action.social.facebook.action import del_fb_post, del_fb_event
    from unifide_backend.action.social.twitter.action import del_tweet
    from unifide_backend.action.social.foursquare.action import del_fsq_update

    user_id = request.args.get("user_id")
    brand_name = request.args.get("brand_name")
    campaigns = request.args.get("campaign_list")

    brand_obj = get_brand_mapping(user_id, brand_name)

    campaign_list = campaigns.split(',')
    for c in campaign_list:
        mapping_obj = get_mapping(c)

        # delete facebook post / event
        if mapping_obj.facebook is not None:
            id = mapping_obj.facebook
            post = FBPost.collection().find_one({"_id": coerce_bson_id(id)})
            try:
                if post is not None:
                    del_fb_post(post["post_id"], id, brand_obj.facebook["access_token"])
                event = FBEvent.collection().find_one({"_id": coerce_bson_id(id)})
                if event is not None:
                    del_fb_event(event["event_id"], id, brand_obj.facebook["access_token"])
            except Exception, err:
                print traceback.format_exc()
                print id

        # delete twitter status
        if mapping_obj.twitter is not None:
            id = mapping_obj.twitter
            tweet = TWTweet.collection().find_one({"_id": coerce_bson_id(id)})
            try:
                del_tweet(tweet["fields"]["id_str"] if tweet["fields"] is not None else None, id, brand_obj.twitter["access_token"]["key"], brand_obj.twitter["access_token"]["secret"])
            except Exception, err:
                print traceback.format_exc()
                print id

        # delete foursquare page update
        if mapping_obj.foursquare is not None:
            id = mapping_obj.foursquare
            page_update = FSQPageUpdate.collection().find_one({"_id": coerce_bson_id(id)})
            try:
                del_fsq_update(page_update["update_id"] if page_update["update_id"] is not None else None, id, brand_obj.foursquare["access_token"])
            except Exception, err:
                print traceback.format_exc()
                print id

        # delete campaign
        if mapping_obj.campaign is not None:
            id = mapping_obj.campaign
            Campaign.collection().update({"_id": coerce_bson_id(id)}, {"$set": {"is_deleted": 1}})

        # delete blog
        if mapping_obj.blog is not None:
            id = mapping_obj.blog
            Campaign.collection().update({"_id": coerce_bson_id(id)}, {"$set": {"is_deleted": 1}})

        #delete mapping
        del_mapping(c)

    return jsonify({"status": "ok"})


def _register_api(app):
    """
    interface method so the app can register the API (routing) calls.
    """

    app.add_url_rule('/campaign/media/',
                     "put_campaign_media", put_campaign_media, methods=['PUT'])

    app.add_url_rule('/campaign/data/',
                     "put_campaign_data", put_campaign_data, methods=['POST'])

    app.add_url_rule('/campaign/data/update/',
                     "update_campaign_data", update_campaign_data, methods=['PUT'])

    app.add_url_rule('/campaign/item/url/',
                     "get_item_url", get_item_url, methods=['GET'])

    app.add_url_rule('/campaign/',
                     "del_campaign", del_campaign, methods=['DELETE'])