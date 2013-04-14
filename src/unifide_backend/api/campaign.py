from flask.globals import request
from flask.helpers import json, jsonify


def put_campaign_media():
    pass


def put_campaign_data():
    from campaigns.campaign.model import Campaign
    from campaigns.campaign.action import save
    from unifide_backend.action.campaigns.action import put_mapping

    user_id = request.form.get("user_id")
    title = request.form.get("title")
    description = request.form.get("description")
    type = request.form.get("type")
    datetime = request.form.get("datetime")
    place = request.form.get("place")

    c = Campaign()
    c.title = title
    c.description = description
    c.type = type
    c._id = save(c)

    kvp = {}
    kvp["web"] = c._id

    put_mapping(user_id, kvp)

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