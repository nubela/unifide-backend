from flask.helpers import json, jsonify
import urllib
from unifide_backend.tests.test_base import TestBase
from campaigns.campaign.model import Campaign
from campaigns.campaign.action import save
from unifide_backend.action.campaigns.action import put_mapping


class CampaignTests(TestBase):
    def test_put_campaign_data(self):
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
        kvp["web"] = c._id

        c_obj = put_mapping(user_id, kvp)
        assert c_obj is not None