import foursquare
import datetime
from threading import Thread

from unifide_backend.local_config import FSQ_CLIENT_ID, FSQ_CLIENT_SECRET, FSQ_REDIRECT_URI
from unifide_backend.action.social.foursquare.model import FSQUser, FSQVenue, FSQTip, FSQCheckin, FSQPageUpdate
from unifide_backend.action.util import key_check
from unifide_backend.action.mapping.action import update_brand_mapping, get_brand_mapping
from unifide_backend.action.mapping.model import BrandMapping, CampaignState
from unifide_backend.action.social.foursquare.sdk import FoursquareAPI


def get_api():
    return foursquare.Foursquare(client_id=FSQ_CLIENT_ID, client_secret=FSQ_CLIENT_SECRET, redirect_uri=FSQ_REDIRECT_URI)


def get_auth_url():
    return get_api().oauth.auth_url()


def get_access_token_from_fsq(code):
    return get_api().oauth.get_token(code)


def save_fsq_user(user_id, brand_name, access_token):
    api = get_api()
    api.set_access_token(access_token)
    me = api.users()["user"]

    fsq_user = FSQUser()
    fsq_user.fsq_id = me["id"]
    fsq_user.u_id = user_id
    fsq_user.brand_name = brand_name
    fsq_user.first_name = key_check(me, "firstName")
    fsq_user.last_name = key_check(me, "lastName")
    fsq_user.fields = me

    dupe_obj = FSQUser.collection().find_one({"u_id": user_id, "brand_name": brand_name})
    if dupe_obj is None:
        fsq_user._id = FSQUser.collection().insert(fsq_user.serialize())
    else:
        FSQUser.collection().update({"u_id": user_id, "brand_name": brand_name}, fsq_user.serialize())
        fsq_user = FSQUser.unserialize(FSQUser.collection().find_one({"u_id": user_id, "brand_name": brand_name}))

    update_brand_mapping(user_id, brand_name, "foursquare", fsq_user.fsq_id, access_token)

    return fsq_user


def get_fsq_user(user_id, brand_name):
    dic = FSQUser.collection().find_one({"u_id": user_id, "brand_name": brand_name})
    return FSQUser.unserialize(dic) if dic is not None else None


def get_fsq_venues_managed(user_id, brand_name):
    url = "venues/managed"
    brand_obj = get_brand_mapping(user_id, brand_name)
    api = FoursquareAPI(brand_obj.foursquare["access_token"])
    data = api.request(url)

    return data["response"]["venues"]["items"]



def put_fsq_venue(user_id, brand_name, venue_id):
    url = "%s/%s" % ("venues", venue_id)
    brand_obj = get_brand_mapping(user_id, brand_name)
    api = FoursquareAPI(brand_obj.foursquare["access_token"])
    data = api.request(url)
    v = data["response"]

    venue = FSQVenue()
    venue.venue_id = v["venue"]["id"]
    venue.name = v["venue"]["name"]
    venue.fields = v

    dupe_obj = FSQVenue.collection().find_one({"venue_id": v["venue"]["id"]})
    if dupe_obj is None:
        FSQVenue.collection().insert(venue.serialize())
    else:
        FSQVenue.collection().update({"venue_id": v["venue"]["id"]}, venue.serialize())
        venue = FSQVenue.unserialize(FSQVenue.collection().find_one({"venue_id": v["venue"]["id"]}))

    BrandMapping.collection().update({"uid": user_id, "brand_name": brand_name}, {"$push": {"foursquare.venues": v["venue"]["id"]}})

    t = Thread(target=load_fsq_tips_to_db, args=(v["venue"]["id"], brand_obj.foursquare["access_token"]))
    t.setDaemon(False)
    t.start()

    return venue


def load_fsq_tips_to_db(venue_id, access_token):
    api = get_api()
    api.set_access_token(access_token)
    data = api.venues.tips(venue_id)
    for tip in data["tips"]["items"]:
        put_fsq_tips(venue_id, tip)


def put_fsq_tips(venue_id, t):
    tip = FSQTip()
    tip.venue_id = venue_id
    tip.tip_id = t["id"]
    tip.text = t["text"]
    tip.fields = t
    tip.createdAt = t["createdAt"]

    dupe_obj = FSQTip.collection().find_one({"venue_id": venue_id, "tip_id": t["id"]})
    if dupe_obj is None:
        tip._id = FSQTip.collection().insert(tip.serialize())
    else:
        FSQTip.collection().update({"venue_id": venue_id, "tip_id": t["id"]})
        tip = FSQTip.unserialize(FSQTip.collection().find_one({"venue_id": venue_id, "tip_id": t["id"]}))

    return tip


def del_fsq_venue(user_id, brand_name, venue_id):
    BrandMapping.collection().update({"uid": user_id, "brand_name": brand_name}, {"$pop": {"foursquare.venues": venue_id}})


def del_fsq_user(user_id, brand_name):
    update_brand_mapping(user_id, brand_name, "foursquare")
    FSQUser.collection().remove({"u_id": user_id, "brand_name": brand_name})


def put_fsq_update(shout, venue_id, access_token, state):
    datetime_now = datetime.datetime.utcnow().isoformat('T')
    page_update = FSQPageUpdate()
    page_update.venue_id = venue_id
    page_update.shout = shout
    page_update.createdAt = datetime_now
    print shout, venue_id, access_token

    if state == CampaignState.PUBLISHED:
        url = "%s/%s" % ("pageupdates", "add")
        api = FoursquareAPI(access_token)
        dict = {"pageId": venue_id,
                "venueId": venue_id,
                "shout": shout}
        data = api.request(url, post_args=dict)
        print data

    pass