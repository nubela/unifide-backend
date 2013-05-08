from unifide_backend.action.cp.model import CPMenu, CPMenuItem
from unifide_backend.action.admin.user.model import User
from unifide_backend.action.mapping.model import Mapping, BrandMapping
from unifide_backend.action.social.facebook.model import FBUser
from unifide_backend.action.social.twitter.model import TWUser
from unifide_backend.action.social.foursquare.model import FSQUser


BASE_MENU = [
            {"order": 0,
             "name": "OVERVIEW",
             "sub-menu":
                  [
                      {"name": "View All", "link": "/", "order": "0"},
                      {"name": "divider", "link": "", "order": "1"},
                      {"name": "Facebook", "link": "/facebook/page/activity", "order": "2"},
                      {"name": "Twitter", "link": "/twitter/activity", "order": "3"},
                      {"name": "Foursquare", "link": "/foursquare/venue/activity", "order": "4"},
                      {"name": "Brand Mention", "link": "/brand-mention", "order": "5"},
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
                      {"name": "Orders", "link": "/order", "order": "2"},
                      {"name": "divider", "link": "", "order": "3"},
                      {"name": "Items", "link": "/items", "order": "4"}
                  ]}
            ]


def init_cp_menu():
    dic_list = User.collection().find() if User.collection().find() is not None else []

    for dic in dic_list:
        user = User.unserialize(dic)

        if CPMenu.collection().find_one({"uid": user._id}) is None:
            for item in BASE_MENU:
                menu = CPMenu()
                menu.uid = user._id
                menu.order = item["order"]
                menu.first_lvl = item["name"]

                for val in item["sub-menu"]:
                    sub_menu = CPMenuItem()
                    sub_menu.name = val["name"]
                    sub_menu.link = val["link"]
                    sub_menu.order = val["order"]
                    menu.second_lvl.append(sub_menu.serialize())

                menu._id = CPMenu.collection().insert(menu.serialize())


def put_new_user_menu(user_id):
    for item in BASE_MENU:
        menu = CPMenu()
        menu.uid = user_id
        menu.order = item["order"]
        menu.first_lvl = item["name"]

        for val in item["sub-menu"]:
            sub_menu = CPMenuItem()
            sub_menu.name = val["name"]
            sub_menu.link = val["link"]
            sub_menu.order = val["order"]
            menu.second_lvl.append(sub_menu.serialize())

        menu._id = CPMenu.collection().insert(menu.serialize())

    return menu


def update_info(user_id, old_brand, new_brand, email):
    if new_brand is not None:
        Mapping.collection().update({"uid": user_id, "brand_name": old_brand}, {"$set": {"brand_name": new_brand}})
        BrandMapping.collection().update({"uid": user_id, "brand_name": old_brand}, {"$set": {"brand_name": new_brand}})
        FBUser.collection().update({"u_id": user_id, "brand_name": old_brand}, {"$set": {"brand_name": new_brand}})
        TWUser.collection().update({"u_id": user_id, "brand_name": old_brand}, {"$set": {"brand_name": new_brand}})
        FSQUser.collection().update({"u_id": user_id, "brand_name": old_brand}, {"$set": {"brand_name": new_brand}})
    if email is not None:
        User.collection().update({"_id": user_id}, {"$set": {"emails.0.address": email}})