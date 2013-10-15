from unifide_backend.action.brand.action import CampaignChannels
from base.items.mock import Generate, ItemAttr, ContainerAttr


BRAND_NAME = "DADA"

CAMPAIGN_CHANNELS = [
    CampaignChannels.FACEBOOK,
    CampaignChannels.TWITTER,
    CampaignChannels.FOURSQUARE,
    CampaignChannels.WEB_MOBILE,
    CampaignChannels.PUSH_NOTIFICATION,
]

USER_GROUPS = {
    "admin": "Admin group",
    "normal": "Normal users",
}

BRAND_MENU = [
    {"order": 0,
     "name": "OVERVIEW",
     "sub-menu":
         [
             {"name": "View All", "link": "/", "order": "0"},
             {"name": "divider", "link": "", "order": "1"},
             {"name": "Facebook", "link": "/facebook/page/activity", "order": "2"},
             {"name": "Twitter", "link": "/twitter/activity", "order": "3"},
             {"name": "Foursquare", "link": "/foursquare/venue/activity", "order": "4"},
             {"name": "divider", "link": "", "order": "6"},
             {"name": "Web / Mobile", "link": "/web/campaign/activity", "order": "7"}
         ]},
    {"order": 1,
     "name": "CAMPAIGN",
     "sub-menu":
         [
             {"name": "New Promotion", "link": "/campaign/promo/new", "order": "0"},
             {"name": "New Event", "link": "/campaign/event/new", "order": "1"},
             {"name": "divider", "link": "", "order": "2"},
             {"name": "Manage", "link": "/campaign", "order": "3"}
         ]},
    {"order": 2,
     "name": "MODULES",
     "sub-menu":
         [
             {"name": "Business Info", "link": "/bizinfo", "order": "0"},
             {"name": "Comments", "link": "/comments", "order": "1"},
             {"name": "divider", "link": "", "order": "3"},
             {"name": "Items", "link": "/items", "order": "4"}
         ]},
    {"order": 3,
     "name": "ECOMMERCE",
     "sub-menu":
         [
             {"name": "Manage Orders", "link": "/order", "order": "0"},
             {"name": "Monitor Inventory", "link": "/inventory", "order": "1"},
             {"name": "divider", "link": "", "order": "2"},
             {"name": "Discounts", "link": "/discount", "order": "3"},
             {"name": "Coupons", "link": "/coupon", "order": "4"},
             {"name": "Cashbacks", "link": "/cashback", "order": "5"},
             {"name": "Shipping", "link": "/shipping", "order": "6"},
             {"name": "Taxes", "link": "/taxes", "order": "7"},
         ]},
]

MODEL = {
    "Clothings": {
        "containers": Generate.ITEMS_CONTAINERS,
        "items": [
            {
                "name": "test",
                "meta": "true",
                ItemAttr.INSTRUCTIONS: "This is the meta container item."},
            {
                "custom": Generate.ITEMS_ONLY,
                "custom_attr": {"brochure_number": range(1, 100)},
            }],
        ContainerAttr.DESCRIPTION: "This container manages your items to sell in your eCommerce store",
    },
}