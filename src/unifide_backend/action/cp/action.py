from brand_cfg import BRAND_MENU
from unifide_backend.action.cp.model import CPMenu, CPMenuItem
from unifide_backend.action.admin.user.model import User
from unifide_backend.action.mapping.model import Mapping, BrandMapping
from unifide_backend.action.social.facebook.model import FBUser
from unifide_backend.action.social.twitter.model import TWUser
from unifide_backend.action.social.foursquare.model import FSQUser


def clear_menu():
    CPMenu.collection().remove()


def put_new_menu():
    for item in BRAND_MENU:
        menu = CPMenu()
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