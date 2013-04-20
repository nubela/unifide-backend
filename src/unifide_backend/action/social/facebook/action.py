#===============================================================================
# utils to interface with facebook graph api
#===============================================================================

from flask.helpers import json
from unifide_backend.local_config import FB_APP_ID
from unifide_backend.action.social.facebook.sdk import GraphAPI
from unifide_backend.action.social.facebook.model import FBUser, FBPage, FBPost, _FBUser, FBComment
from unifide_backend.action.admin.user.action import get_max_brands
from bson.objectid import ObjectId
from threading import Thread
from unifide_backend.action.util import unix_time, key_check
from unifide_backend.action.mapping.action import update_brand_mapping


def save_fb_user(user_id, brand_name, fb_id, access_token, token_expiry):

    def save_obj():
        fbUser_obj = FBUser()
        fbUser_obj.u_id = user_id
        fbUser_obj.fb_id = fb_id
        fbUser_obj.brand_name = brand_name
        fbUser_obj.access_token = access_token
        fbUser_obj.expires = token_expiry
        fbUser_obj._id = FBUser.collection().insert(fbUser_obj.serialize())
        return fbUser_obj

    # dupe check before inserting new fb user record into db
    fbUser_obj = FBUser.collection().find_one({"u_id": user_id, "fb_id": fb_id, "access_token": access_token})
    if fbUser_obj is not None:
        saved_fb_user_obj = FBUser.unserialize(fbUser_obj)
    else:
        saved_fb_user_obj = save_obj()

    return saved_fb_user_obj


def get_fb_user(user_id, brand_name):
    dic = FBUser.collection().find_one({"u_id": user_id, "brand_name": brand_name})
    return FBUser.unserialize(dic) if dic is not None else None


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


def get_fb_page_list(user_id, access_token):
    url = "%s/%s" % (user_id, "accounts")
    return GraphAPI(access_token).request(url)["data"]


def put_fb_page(fb_user_obj, brand_name, page_obj):

    def save_obj():
        fbPage_obj = FBPage()
        fbPage_obj.page_id = page_obj["id"]
        fbPage_obj.name = page_obj["name"]
        fbPage_obj.category = page_obj["category"]
        fbPage_obj._id = FBPage.collection().insert(fbPage_obj.serialize())
        return fbPage_obj

    fb_page_obj = FBPage.collection().find_one({"page_id": page_obj["id"]})
    if fb_page_obj is not None:
        saved_fbPage_obj = FBPage.unserialize(fb_page_obj)
    else:
        saved_fbPage_obj = save_obj()

    update_brand_mapping(fb_user_obj.u_id, brand_name, "facebook", page_obj["id"], page_obj["access_token"]);

    """
    t = Thread(target=load_fb_page_to_db, args=(page_obj["id"], fb_user_obj))
    t.setDaemon(False)
    t.start()
    """

    return saved_fbPage_obj


def del_fb_user(user_id, brand_name):
    del_fb_page(user_id, brand_name)
    FBUser.collection().remove({"u_id": user_id, "brand_name": brand_name})


def del_fb_page(user_id, brand_name):
    update_brand_mapping(user_id, brand_name, "facebook")


def load_fb_page_to_db(page_id, user_id):
    page = get_fb_page(user_id, page_id)
    posts = get_fb_posts(page_id, page.page_access_token)
    save_fb_posts(posts["data"], page_id)

    if subscribe_fb_updates(page) == True:
        print "Facebook Realtime Updates (" + str(page_id) + ") successful."
    else:
        print "Facebook Realtime Updates (" + str(page_id) + ") unsuccessful."


def subscribe_fb_updates(page):
    url = "%s/%s" % (page.page_id, "tabs")
    data = {"app_id": FB_APP_ID}
    return GraphAPI(page.page_access_token).request(url, post_args=data)


def get_fb_page(user_id, page_id):
    pages = FBUser.unserialize(FBUser.collection().find_one({"u_id": user_id})).pages
    for page in pages:
        fbPage = FBPage.unserialize(FBPage.collection().find_one({"page_access_token": page}))
        if fbPage.page_id == page_id:
            return fbPage


def get_fb_posts(page_id, access_token, limit=200, since=None):
    url = "%s/%s" % (page_id, "feed")
    data = {"limit": limit}
    if since is not None:
        data["since"] = since
    return GraphAPI(access_token).request(url, args=data)


def save_fb_posts(posts, page_id):
    def save_obj(post):
        comments = []
        users = []
        _fbUser_obj = _FBUser()
        _fbUser_obj.id = post["from"]["id"]
        _fbUser_obj.name = post["from"]["name"]
        users.append(_fbUser_obj)

        fbPost_obj = FBPost()
        fbPost_obj.page_id = page_id
        fbPost_obj.post_id = post["id"]
        fbPost_obj.from_id = post["from"]["id"]
        fbPost_obj.message = key_check(post, "message")
        fbPost_obj.story = key_check(post, "story")
        fbPost_obj.created_time = unix_time(post["created_time"])
        fbPost_obj.updated_time = unix_time(post["updated_time"])
        fbPost_obj.type = post["type"]

        if post["comments"]["count"] > 0:
            for c in post["comments"]["data"]:
                fbComment_obj = FBComment()
                fbComment_obj.post_id = post["id"]
                fbComment_obj.id = c["id"]
                fbComment_obj.user = c["from"]["id"]
                fbComment_obj.text = c["message"]
                fbComment_obj.created_time = unix_time(c["created_time"])
                comments.append(fbComment_obj)

                fbCommentUser_obj = _FBUser()
                fbCommentUser_obj.id = c["from"]["id"]
                fbCommentUser_obj.name = c["from"]["name"]
                # re-look logic for caching comment user's name into database
                if any(u.id != fbCommentUser_obj.id for u in users):
                    users.append(fbCommentUser_obj)

        return fbPost_obj, comments, users

    posts_list, comments_list, users_list = [], [], []
    for post in posts:
        post_obj, comments_obj, users_obj = save_obj(post)
        posts_list.append(post_obj)
        comments_list.extend(comments_obj)
        users_list.extend(users_obj)

    for post in posts_list:
        if FBPost.collection().find_one({"post_id": post.post_id}) is None:
            FBPost.collection().insert(post.serialize())

    for comment in comments_list:
        if FBComment.collection().find_one({"id": comment.id}) is None:
            FBComment.collection().insert(comment.serialize())

    for user in users_list:
        if _FBUser.collection().find_one({"id": user.id}) is None:
            _FBUser.collection().insert(user.serialize())
        else:
            # detected fb user has changed name, so update fb name in database
            _user = _FBUser.unserialize(_FBUser.collection().find_one({"id": user.id}))
            if user.id == _user.id and user.name != _user.name:
                _FBUser.collection().update({"id": user.id}, {"$set": {"name": user.name}})



def get_fb_events():
    pass


def page_realtime_update(entry):
    for e in entry:
        if FBPage.collection().find_one({"page_id": e["id"]}) is None:
            continue
        for change in e["changes"]:
            if change["field"] == "feed" and change["value"]["item"] == "comment" and change["value"]["verb"] == "add":
                add_comment(change, e["id"])


def add_comment(change_obj, page_id):
    value = change_obj["value"]

    def save_obj(value_obj):
        comment_obj = FBComment()
        comment_obj.post_id = str(page_id) + "_" + str(value_obj["parent_id"])
        comment_obj.id = str(page_id) + "_" + str(value_obj["comment_id"])
        comment_obj.user = str(value_obj["sender_id"])
        comment_obj.created_time = value_obj["created_time"]
        comment_obj._id = FBComment.collection().insert(comment_obj.serialize())
        return comment_obj

    if FBComment.collection().find_one({"id": str(page_id) + "_" + str(value["comment_id"])}) is None:
        comment = save_obj(value)
    else:
        comment = FBComment.unserialize(FBComment.collection().find_one({"id": str(page_id) + "_" + str(value["comment_id"])}))

    # get updated comment info from facebook to update missing message and like_count
    updated_comment = get_comment_from_fb(comment, page_id)
    FBComment.collection().update({"id": comment.id}, {"$set": {"text": updated_comment["message"], "like_count": updated_comment["like_count"]}})

    # check if comment user data exists in fb user cache
    if _FBUser.collection().find_one({"id": updated_comment["from"]["id"]}) is None:
        _FBUser.collection().insert({"id": updated_comment["from"]["id"], "name": updated_comment["from"]["name"]})
    else:
        _FBUser.collection().update({"id": updated_comment["from"]["id"]}, {"$set": {"name": updated_comment["from"]["name"]}})

    # update timestamp for post
    if comment is not None and updated_comment is not None:
        FBPost.collection().update({"post_id": comment.post_id}, {"$set": {"updated_time": value["created_time"]}})


def get_comment_from_fb(comment_obj, page_id):
    url = "%s" % (comment_obj.id)
    page = FBPage.unserialize(FBPage.collection().find_one({"page_id": page_id}))
    return GraphAPI(page.page_access_token).request(url)


def put_fb_post(page, message, attachment={}, is_published=True):

    p = FBPost()
    p.message = message
    print page

    def publish():
        api = GraphAPI(page["access_token"])
        return api.put_wall_post(message, profile_id=page["page_id"])["id"]

    def save(post):
        return FBPost.collection().insert(post.serialize())

    if is_published:
        p.post_id = publish()
        if p.post_id is not None:
            p._id = save(p)
        else:
            return None
    else:
        p._id = save(p)

    return p
