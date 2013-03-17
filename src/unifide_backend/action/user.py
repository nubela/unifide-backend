from unifide_backend.util.db import __get_collection
from unifide_backend.models import User, FacebookUser, FacebookPage


def get_user_from_email(email):
    user = __get_collection("users").find({"email": email})
    if user.count() > 0:
        return user[0]["_id"]
    return None


def save_test_user(email, passwd):
    user_id = get_user_from_email(email)
    if not user_id:
        user_obj = User()
        user_obj.email = email
        user_obj.passwd_hash = passwd
        user_id = __get_collection("users").insert(user_obj.serialize())

    return user_id


def del_test_user(user_id):
    __get_collection("users").remove({"_id": user_id})


def get_user(user_id):
    user = __get_collection("users").find({"_id": user_id})
    if user.count() > 0:
        return user[0]
    return None


def get_user_access_token(user_id):
    """
    Currently only supports 1 facebook account so first user access token [0]
    """
    user = __get_collection("users").find({"_id": user_id})
    if user.count() > 0:
        if user[0]["fb"]:
            return user[0]["fb"][0]["access_token"]
    return None


def save_fb_oauth(user_obj, user_access_token, fb_id):
    """
    Currently only supports 1 facebook account per user
    """
    fbUser_id = __get_collection("users").find({"_id": user_obj["_id"], "fb.access_token": user_access_token})
    if user_obj is not None and fbUser_id.count() == 0:
        fbUser = FacebookUser()
        fbUser.fb_id = fb_id
        fbUser.access_token = user_access_token
        fbUser_id = __get_collection("users").update({"_id": user_obj["_id"]}, {"$push": {"fb": fbUser.serialize()}})

    return fbUser_id


def save_fb_page(user_obj, page_id, user_access_token, page_access_token, page_name):
    """
    Currently only supports 1 facebook account(w multiple pages) per user
    """
    fbPage_id = None
    if user_obj is not None:
        fbPage = FacebookPage()
        fbPage.page_id = page_id
        fbPage.page_access_token = page_access_token
        fbPage.name = page_name
        fbPage_id = __get_collection("users").update({"_id": user_obj["_id"], "fb.access_token": user_access_token}, {"$push": {"fb.$.pages": fbPage.serialize()}})

    return fbPage_id