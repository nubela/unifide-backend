#===============================================================================
# utils to interface with facebook graph api
#===============================================================================
from flask.helpers import json
import requests
import urllib
import hashlib
from base.db import get_mongo
from base.users.default_config import USERS_COLLECTION_NAME
from unifide_backend.action.social.facebook.model import FacebookUser, FacebookPage


FACEBOOK_PAGE = "https://www.facebook.com"
FACEBOOK_GRAPH_API_URL = "https://graph.facebook.com"
PERMISSIONS = "manage_pages,publish_stream"
API_CACHE = {}


def get_user_token(user_id):
    """
    Currently only supports 1 facebook account so first user access token [0]
    """
    user = __get_collection().find({"_id": user_id})
    if user.count() > 0:
        if user[0]["fb"]:
            return user[0]["fb"][0]["access_token"]
    return None


def save_fb_oauth(user_obj, user_access_token, fb_id):
    """
    Currently only supports 1 facebook account per user
    """
    fbUser_id = __get_collection().find({"_id": user_obj["_id"], "fb.access_token": user_access_token})
    if user_obj is not None and fbUser_id.count() == 0:
        fbUser = FacebookUser()
        fbUser.fb_id = fb_id
        fbUser.access_token = user_access_token
        fbUser_id = __get_collection().update({"_id": user_obj["_id"]}, {"$push": {"fb": fbUser.serialize()}})

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
        fbPage_id = __get_collection().update({"_id": user_obj["_id"], "fb.access_token": user_access_token}, {"$push": {"fb.$.pages": fbPage.serialize()}})

    return fbPage_id


#===============================================================================
# base requirement = user access token to perform most of the API functions
#===============================================================================
class FacebookAPI:
    access_token = None

    def __init__(self, access_token):
        self.access_token = access_token
        API_CACHE[access_token] = self

    @staticmethod
    def new(access_token):
        return API_CACHE.get(access_token, FacebookAPI(access_token))

    @staticmethod
    def auth_url(app_id, redirect_url, randNum=""):
        url = "%s%s" % (FACEBOOK_PAGE, "/dialog/oauth?")
        kvps = {'client_id': app_id,
                'redirect_uri': redirect_url,
                'scope': PERMISSIONS,
                'state': hashlib.sha256(randNum)}

        return url + urllib.urlencode(kvps)

    @staticmethod
    def generate(code, app_id, app_secret, redirect_url):
        url = "%s%s" % (FACEBOOK_GRAPH_API_URL, "/oauth/access_token")
        r = requests.get(url, params={
            "client_id": app_id,
            "client_secret": app_secret,
            "redirect_uri": redirect_url,
            "code": code,
            })

        user_access_token = json.loads(r.text)
        return FacebookAPI(user_access_token["access_token"])

    def get_info(self, rehash=False):
        if not rehash and hasattr(self, "info"):
            return self.info

        url = "%s%s" % (FACEBOOK_GRAPH_API_URL, "/me")
        r = requests.get(url, params={
            "access_token": self.access_token,
            })

        self.info_raw = r.text
        self.info = json.loads(self.info_raw)
        return self.info

    def get_friends(self, rehash=False):
        if not rehash and hasattr(self, "friends"):
            return self.friends

        url = "%s%s" % (FACEBOOK_GRAPH_API_URL, "/me/friends")
        r = requests.get(url, params={
            "access_token": self.access_token,
            "offset": 0,
            "format": "json",
            "limit": 50000,
            })

        self.friends_raw = r.text
        self.friends = json.loads(self.friends_raw)

        return self.friends

    #===============================================================================
    # formulate list of page name, id, category
    # page_list = []
    # for d in data["data"]:
    #    p = {
    #        "category": d["category"],
    #        "name": d["name"],
    #        "id": d["id"]
    #    }
    #    page_list.append(p)
    #===============================================================================
    def get_page_list(self, fb_id=None, rehash=False):
        if not rehash and hasattr(self, "page_list"):
            return self.page_list

        if fb_id is None:
            fb_id = self.get_info()["id"]

        url = "%s/%s/%s" % (FACEBOOK_GRAPH_API_URL, fb_id, "accounts")
        r = requests.get(url, params={
            "access_token": self.access_token
            })

        self.page_list_raw = r.text
        self.page_list = json.loads(self.page_list_raw)

        return self.page_list

    def get_page_access_token(self, page_id):
        if hasattr(self, "page_list"):
            for page in self.page_list["data"]:
                if page["id"] == page_id:
                    return page["access_token"], page["name"]

        url = "%s/%s" % (FACEBOOK_GRAPH_API_URL, page_id)
        r = requests.get(url, params={
            "fields": "access_token,name",
            "access_token": self.access_token
            })

        self.page_access_token = json.loads(r.text)

        return self.page_access_token["access_token"], self.page_access_token["name"]


def __get_collection(coll=[]):
    if coll == []:
        mongo_db = get_mongo()
        collection = mongo_db[USERS_COLLECTION_NAME]
        coll += [collection]
    return coll[0]