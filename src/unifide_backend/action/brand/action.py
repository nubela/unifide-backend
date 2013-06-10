from unifide_backend.action.brand.model import BrandConfig


def save(config_obj):
    id = BrandConfig.collection().save(config_obj.serialize())
    return id


def convert_campaign_channels(cc_obj):
    campaign_channel_obj = BrandConfig()
    campaign_channel_obj.name = "campaign_channel"
    campaign_channel_obj.value = cc_obj
    return campaign_channel_obj


class CampaignChannels:
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    FOURSQUARE = "4sq"
    BLOG = "blog"
    WEB_MOBILE = "web_and_mobile"
    PUSH_NOTIFICATION = "push_notification"