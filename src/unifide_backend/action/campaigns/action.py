from unifide_backend.action.campaigns.model import CampaignMapping
from campaigns.campaign.action import get as get_web_campaign


def put_mapping(uid, kvp):
    c_mapping = CampaignMapping()
    c_mapping.uid = uid

    for k,v in kvp.iteritems():
        old_val = getattr(c_mapping, k) if getattr(c_mapping, k) is not None else []
        old_val.append(v)
        setattr(c_mapping, k, old_val)

    c_mapping._id = CampaignMapping.collection().insert(c_mapping.serialize())
    return c_mapping