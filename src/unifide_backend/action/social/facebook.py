from urlparse import parse_qsl
import requests

FACEBOOK_GRAPH_API_URL = "https://graph.facebook.com"
PERMISSIONS = "manage_pages,publish_stream"


def get_page_list(user_access_token, profile_id):
    """
    Get list of pages user is admin
    """

    return ""


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