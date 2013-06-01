#===============================================================================
# utils to interface with facebook graph api
#===============================================================================

import datetime
from threading import Thread

from base.util import coerce_bson_id
from unifide_backend.local_config import FB_APP_ID
from unifide_backend.action.social.facebook.sdk import GraphAPI
from unifide_backend.action.social.facebook.model import FBUser, FBPage, FBPost, FBComment, FBEvent
from unifide_backend.action.mapping.action import update_brand_mapping
from unifide_backend.action.mapping.model import BrandMapping, CampaignState
from unifide_backend.action.util import isoformat, replace_newline, strip_tags


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
    url = "%s" % (page_obj["id"])
    page_data = GraphAPI(page_obj["access_token"]).request(url)

    fb_page = FBPage()
    fb_page.page_id = page_data["id"]
    fb_page.name = page_data["name"]
    page_data.pop("id", None)
    page_data.pop("name", None)
    fb_page.fields = page_data

    def save_obj(page):
        return FBPage.collection().save(page.serialize())

    dupe_obj = FBPage.collection().find_one({"page_id": page_obj["id"]})
    if dupe_obj is None:
        fb_page._id = save_obj(fb_page)
    else:
        FBPage.collection().update({"page_id": page_obj["id"]}, fb_page.serialize())
        fb_page = FBPage.unserialize(FBPage.collection().find_one({"page_id": page_obj["id"]}))

    update_brand_mapping(fb_user_obj.u_id, brand_name, "facebook", page_obj["id"], page_obj["access_token"]);

    t = Thread(target=load_fb_page_to_db, args=(page_obj["id"], page_obj["access_token"]))
    t.setDaemon(False)
    t.start()

    return fb_page


def del_fb_user(user_id, brand_name):
    del_fb_page(user_id, brand_name)
    FBUser.collection().remove({"u_id": user_id, "brand_name": brand_name})


def del_fb_page(user_id, brand_name):
    update_brand_mapping(user_id, brand_name, "facebook")


def load_fb_page_to_db(page_id, page_access_token):
    posts = get_fb_posts(page_id, page_access_token)
    for post in posts["data"]:
        save_fb_post(post, page_id)

    result = subscribe_fb_updates(page_id, page_access_token)
    print "Facebook Realtime Updates (" + str(page_id) + ") : " + str(result)


def subscribe_fb_updates(page_id, page_access_token):
    url = "%s/%s" % (page_id, "tabs")
    data = {"app_id": FB_APP_ID}
    return GraphAPI(page_access_token).request(url, post_args=data)


def get_fb_posts(page_id, access_token, limit=200, since=None):
    url = "%s/%s" % (page_id, "feed")
    data = {"limit": limit}
    if since is not None:
        data["since"] = since
    return GraphAPI(access_token).request(url, args=data)


def save_fb_post(post, page_id):
    post_obj = FBPost()
    post_obj.post_id = post["id"]
    post_obj.page_id = page_id
    post_obj.owner = post["from"]
    post_obj.created_time = post["created_time"]
    post_obj.updated_time = post["updated_time"]
    comments_list = post.pop("comments", None)
    post_obj.fields = post

    def save_obj(post):
        return FBPost.collection().save(post.serialize())

    dupe_obj = FBPost.collection().find_one({"post_id": str(post["id"])})

    if dupe_obj is None:
        post_obj._id = save_obj(post_obj)
    else:
        FBPost.collection().update({"post_id": post["id"]}, post_obj.serialize())
        post_obj = FBPost.unserialize(FBPost.collection().find_one({"post_id": post["id"]}))

    if comments_list is not None:
        for comment in comments_list["data"]:
            save_fb_post_comment(comment, post_obj.post_id)

    return post_obj


def save_fb_post_comment(comment, post_id):
    comment_obj = FBComment()
    comment_obj.post_id = post_id
    comment_obj.comment_id = comment["id"]
    comment_obj.owner = comment["from"]
    comment_obj.message = comment["message"]
    comment_obj.created_time = comment["created_time"]
    comment_obj.fields = comment

    dupe_obj = FBComment.collection().find_one({"comment_id": comment["id"]})

    if dupe_obj is None:
        comment_obj._id = FBComment.collection().save(comment_obj.serialize())
    else:
        FBComment.collection().update({"comment_id": comment["id"]}, comment_obj.serialize())
        comment_obj = FBComment.unserialize(FBComment.collection().find_one({"comment_id": comment["id"]}))

    return comment_obj


def save_fb_event(event, page_id):
    event_obj = FBEvent()
    event_obj.event_id = event["id"]
    event_obj.page_id = page_id
    event_obj.owner = event["owner"]
    event_obj.fields = event

    dupe_obj = FBEvent.collection().find_one({"event_id": event["id"]})

    if dupe_obj is None:
        event_obj._id = FBEvent.collection().save(event_obj.serialize())
    else:
        FBEvent.collection().update({"event_id": event["id"]}, event_obj.serialize())
        event_obj = FBEvent.unserialize(FBEvent.collection().find_one({"event_id": event["id"]}))

    return event_obj


def page_realtime_update(entry):
    print entry
    for e in entry:
        if FBPage.collection().find_one({"page_id": e["id"]}) is None:
            continue
        for change in e["changes"]:
            if change["field"] == "feed" and change["value"]["item"] == "comment" and change["value"]["verb"] == "add":
                comment_dict = get_comment_from_fb(change["value"]["comment_id"], e["id"])
                post_id = "%s_%s" % (e["id"], change["value"]["parent_id"])
                save_fb_post_comment(comment_dict, post_id)
                update_post_time(post_id, comment_dict["created_time"])
            elif change["field"] == "feed" and change["value"]["item"] == "post" and change["value"]["verb"] == "add":
                post_dict = get_post_from_fb(change["value"]["post_id"], e["id"])
                save_fb_post(post_dict, e["id"])


def get_comment_from_fb(comment_id, page_id):
    url = "%s_%s" % (page_id, comment_id)
    return GraphAPI().request(url)


def get_post_from_fb(post_id, page_id):
    url = "%s_%s" % (page_id, post_id)
    access_token = (BrandMapping.unserialize(BrandMapping.collection().find_one({"facebook.id": page_id}))).facebook[
        "access_token"]
    print url
    return GraphAPI(access_token).request(url)


def update_post_time(post_id, updated_time):
    print "post_id: " + str(post_id)
    print "updated_time: " + str(updated_time)
    FBPost.collection().update({"post_id": post_id}, {"$set": {"updated_time": updated_time}})


def put_fb_post(page, fb_id, state, message, media_file=None):
    datetime_now = datetime.datetime.utcnow().isoformat('T')
    post = FBPost()
    post.page_id = page["id"]
    post.owner = {"id": fb_id}
    post.fields = {"message": message}
    post.created_time = datetime_now
    post.updated_time = datetime_now

    if state == CampaignState.PUBLISHED:
        api = GraphAPI(page["access_token"])
        if media_file is None:
            post.post_id = api.put_wall_post(message, profile_id=page["id"])["id"]
        else:
            data = api.put_photo(media_file, message=message)
            post.post_id = data["id"]
        url = "%s" % post.post_id
        post_data = api.request(url)
        post = save_fb_post(post_data, page["id"])
    else:
        post._id = FBPost.collection().insert(post.serialize())

    return post


def put_fb_event(page, fb_id, state, title, description, start_time, end_time, media_file=None):
    datetime_now = datetime.datetime.utcnow().isoformat('T')
    event = FBEvent()
    event.page_id = page["id"]
    event.owner = {"id": fb_id}
    event.fields = {"name": title, "description": description}
    event.created_time = datetime_now
    event.updated_time = datetime_now

    if start_time is not None:
        event.fields["start_time"] = isoformat(start_time)
    if end_time is not None:
        event.fields["end_time"] = isoformat(end_time)

    if state == CampaignState.PUBLISHED:
        api = GraphAPI(page["access_token"])
        url = "%s/%s" % (page["id"], "events")

        # todo : note the start and end UTC time formats, currently hard-coded +0000
        dict = {
            "name": title,
            "start_time": isoformat(start_time) + "Z",
            "description": strip_tags(replace_newline(description))
        }

        if end_time is not None:
            dict["end_time"] = isoformat(end_time) + "Z"

        if media_file:
            dict["source"] = media_file
            dict["access_token"] = page["access_token"]
            event.event_id = api.put_event(dict)["id"]
        else:
            event.event_id = api.request(url, post_args=dict)["id"]

        event_data = api.request(event.event_id)
        print "event data"
        print event_data
        event = save_fb_event(event_data, page["id"])
    else:
        event._id = FBEvent.collection().insert(event.serialize())

    return event


def update_fb_event(event_id, page, state, title, description, start_time, end_time):
    datetime_now = datetime.datetime.utcnow().isoformat('T')
    event = FBEvent.collection().find_one({"event_id": event_id})
    event["fields"]["name"] = title
    event["fields"]["description"] = description
    event["updated_time"] = datetime_now

    if start_time is not None:
        event["fields"]["start_time"] = isoformat(start_time)
    if end_time is not None:
        event["fields"]["end_time"] = isoformat(end_time)

    if state == CampaignState.PUBLISHED:
        api = GraphAPI(page["access_token"])
        url = event_id

        dict = {
            "name": title,
            "start_time": isoformat(start_time) + "Z",
            "description": strip_tags(replace_newline(description))
        }

        if end_time is not None:
            dict["end_time"] = isoformat(end_time) + "Z"

        api.request(url, post_args=dict)
        event_data = api.request(event_id)
        event = save_fb_event(event_data, page["id"])
    else:
        FBEvent.collection().update({"event_id": event_id}, {"$set": {event}})
        event = FBEvent.unserialize(FBEvent.collection().find_one({"event_id": event_id}))

    return event


def del_fb_post(post_id, obj_id, access_token):
    if post_id is not None:
        data = GraphAPI(access_token).delete_object(post_id)
        print data
    FBPost.collection().update({"_id": coerce_bson_id(obj_id)}, {"$set": {"is_deleted": 1}})


def del_fb_event(event_id, obj_id, access_token):
    if event_id is not None:
        data = GraphAPI(access_token).delete_object(event_id)
        print data
    FBEvent.collection().update({"_id": coerce_bson_id(obj_id)}, {"$set": {"is_deleted": 1}})


def update_page_attr(page_id, access_token, profile_photo=None, cover_photo=None, about=None, description=None,
                     website=None, phone=None, hours=None):
    url = page_id
    api = GraphAPI(access_token)
    dict = {}
    if about is not None:
        dict["about"] = about
    if description is not None:
        dict["description"] = description
    if website is not None:
        dict["website"] = website
    if phone is not None:
        dict["phone"] = phone
    if hours is not None:
        pass

    data = api.request(url, post_args=dict)
