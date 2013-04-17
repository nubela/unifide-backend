from flask.helpers import json, jsonify
import urllib
from unifide_backend.tests.test_base import TestBase
from campaigns.campaign.model import Campaign
from campaigns.campaign.action import save
from unifide_backend.action.mapping.action import put_mapping, get_mapping, get_brand_mapping
from unifide_backend.action.social.facebook.action import put_fb_post
from unifide_backend.api.campaign import PLATFORM_CAMPAIGN, PLATFORM_FACEBOOK
import datetime

class CampaignTests(TestBase):
    def _test_put_campaign_data2(self):
        user_id = "xaa8LzkwtCCgb6BeP"
        title = "test_title"
        description = "test_description"
        type = "promotional"

        c = Campaign()
        c.uid = user_id
        c.title = title
        c.description = description
        c.type = type
        c._id = save(c)

        kvp = {}
        kvp["campaign_list"] = c._id

        mapping_obj = put_mapping(user_id, kvp, datetime.datetime.now())

        assert mapping_obj is not None

    def test_put_campaign_data(self):
        user_id = "xaa8LzkwtCCgb6BeP"
        brand_id = "516bb6f3c64ed2c1ad73842a"
        platforms = ["campaign", "facebook"]
        title = "test_title"
        description = "test_description"
        type = "promotional"
        is_published = True
        is_draft = False
        item_list = []

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

        publish_datetime = datetime.datetime.now() if is_published is True else None
        put_mapping(user_id, kvp, publish_datetime, is_published, is_draft)