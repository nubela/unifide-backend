#===============================================================================
# utils to interface with facebook graph api
#===============================================================================
from urlparse import parse_qsl
from flask.helpers import json
import requests
from unifide_backend.util.db import __get_collection

FACEBOOK_GRAPH_API_URL = "https://graph.facebook.com"
PERMISSIONS = "manage_pages,publish_stream"
API_CACHE = {}


def get_page_list(user_access_token):
    """
    Get list of pages user is an admin
    """

    #get info
    fb_api = FacebookApi.new(user_access_token)
    fb_user_info = fb_api.get_info()

    #build param with page access token
    param = {
        "access_token": user_access_token
    }

    full_url = "%s/%s/%s" % (FACEBOOK_GRAPH_API_URL, fb_user_info["id"], "accounts")
    r = requests.get(full_url, params=param)
    data = json.loads(r.text)

    #formulate list of page name, id, category
    page_list = []
    for d in data["data"]:
        p = {
            "category": d["category"],
            "name": d["name"],
            "id": d["id"]
        }
        page_list.append(p)

    return page_list, fb_user_info["id"]


def get_user_access_token(code, app_id, app_secret, redirect_uri="http://127.0.0.1/"):
    """
    Authenticates an app with a user's code;
    Exchanges a user's auth code and to an access token
    """

    #build param with app's data
    param = {
        "client_id": app_id,
        "client_secret": app_secret,
        "redirect_uri": redirect_uri,
        "code": code,
    }

    full_url = "%s%s" % (FACEBOOK_GRAPH_API_URL, "/oauth/access_token")
    r = requests.get(full_url, params=param)
    sq = dict(parse_qsl(r.text))
    return sq["access_token"]


def get_page_access_token(page_id, user_access_token):
    """
    Save page access token with page id
    """

    param = {
        "fields": "access_token,name",
        "access_token": user_access_token
    }

    full_url = "%s/%s" % (FACEBOOK_GRAPH_API_URL, page_id)
    r = requests.get(full_url, params=param)
    data = json.loads(r.text)
    return data["access_token"], data["name"]


class FacebookApi:
    access_token = None

    def __init__(self, access_token):
        self.access_token = access_token
        API_CACHE[access_token] = self

    @staticmethod
    def new(access_token):
        return API_CACHE.get(access_token, FacebookApi(access_token))

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