#===============================================================================
# utils to interface with facebook graph api
#===============================================================================

from unifide_backend.action.social.facebook.sdk import GraphAPI
from unifide_backend.action.social.facebook.model import FBUser, FBPage
from unifide_backend.action.admin.user.action import get_max_brands

def get_avail_slots(user_id):
    max_brand = get_max_brands(user_id)
    fbUsers = get_fb_users(user_id)
    for user in fbUsers:
        if user.u_id == user_id:
            max_brand -= len(user.pages)

    return max_brand


def save_fb_user(user_id, fb_id, access_token, token_expiry):

    def save_obj():
        fbUser_obj = FBUser()
        fbUser_obj.u_id = user_id
        fbUser_obj.fb_id = fb_id
        fbUser_obj.access_token = access_token
        fbUser_obj.expires = token_expiry
        fbUser_obj._id = FBUser.collection().insert(fbUser_obj.serialize())
        return fbUser_obj

    # dupe check before inserting new fb user record into db
    fbUser_obj = FBUser.collection().find({"u_id": user_id, "fb_id": fb_id, "access_token": access_token})
    if fbUser_obj.count() > 0:
        saved_fb_user_obj = FBUser.unserialize(fbUser_obj[0])
    else:
        saved_fb_user_obj = save_obj()

    return saved_fb_user_obj


def get_fb_users(user_id):
    fbUsers = []
    dic = FBUser.collection().find({"u_id": user_id})
    if dic:
        for d in dic:
            fbUsers.append(FBUser.unserialize(d))
    return fbUsers


def get_fb_id(access_token):
    url = "%s" % ("me")
    # retrieve fb id from local db cache
    coll = FBUser.collection()
    dic = coll.find_one({"access_token": str(access_token)})
    fb_id = FBUser.unserialize(dic).fb_id if dic is not None else None
    # retrieve from fb graph api if not found in local db
    if fb_id is None:
        fb_id = GraphAPI(access_token).request(url)["id"]

    return fb_id


def get_fb_page_list(fbUsers):
    page_list = {}
    for user in fbUsers:
        page = None
        url = "%s/%s" % (user.fb_id, "accounts")
        try:
            page = GraphAPI(user.access_token).request(url)["data"]
        except:
            pass
        if page:
            page_list[user.fb_id] = page

    return page_list


def save_fb_page(u_id, fb_id, page_name, page_id, page_category, page_token):

    def save_obj():
        fbPage_obj = FBPage()
        fbPage_obj.page_id = page_id
        fbPage_obj.name = page_name
        fbPage_obj.category = page_category
        fbPage_obj.page_access_token = page_token
        fbPage_obj._id = FBPage.collection().insert(fbPage_obj.serialize())
        return fbPage_obj

    fbPage_obj = FBPage.collection().find({"page_id": page_id, "page_access_token": page_token})
    if fbPage_obj.count() > 0:
        saved_fbPage_obj = FBPage.unserialize(fbPage_obj[0])
    else:
        saved_fbPage_obj = save_obj()

    if FBUser.collection().find({"u_id": u_id, "fb_id": fb_id, "pages": saved_fbPage_obj.get_id()}).count() == 0:
        FBUser.collection().update({"u_id": u_id, "fb_id": fb_id},
                                   {"$push":
                                        {"pages": saved_fbPage_obj.get_id()}
                                   })

    return saved_fbPage_obj