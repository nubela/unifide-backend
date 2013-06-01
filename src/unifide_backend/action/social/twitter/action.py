import datetime
import tweepy
from threading import Thread
from tweepy.cursor import Cursor
from flask.helpers import json

from base.util import coerce_bson_id
from unifide_backend.local_config import TW_CONSUMER_KEY, TW_CONSUMER_SECRET, ADD_USER_MAX_TWEET, TW_INDIVIDUAL_STREAM
from unifide_backend.action.social.twitter.model import TWUser, TWTweet
from unifide_backend.action.mapping.action import update_brand_mapping
from unifide_backend.action.mapping.model import BrandMapping, CampaignState


def get_api(key, secret):
    """
    Retrieve twitter API object based on user's access token key and secret
    """
    auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
    auth.set_access_token(key, secret)
    return tweepy.API(auth), auth.access_token.key, auth.access_token.secret


def save_tw_user_oauth(user_id, brand_name, key, secret):
    twUser_obj = TWUser()
    twUser_obj.u_id = user_id
    twUser_obj.brand_name = brand_name
    twUser_obj.oauth_key = key
    twUser_obj.oauth_secret = secret

    def save_obj(twUser):
        return TWUser.collection().insert(twUser.serialize())

    dupe_obj = TWUser.collection().find_one({"u_id": user_id, "brand_name": brand_name})

    if dupe_obj is None:
        twUser_obj._id = save_obj(twUser_obj)
    else:
        TWUser.collection().update({"u_id": user_id, "brand_name": brand_name}, {"oauth_key": key, "oauth_secret": secret})


def get_tw_user_oauth(user_id, brand_name):
    dic = TWUser.collection().find_one({"u_id": user_id, "brand_name": brand_name})
    return TWUser.unserialize(dic) if dic is not None else None


def save_tw_user(user_id, brand_name, key, secret):
    """
    Add twitter account to the unifide user and spawn thread to pull recent tweewts from home timeline
    """
    api, token_key, token_secret = get_api(key, secret)
    twUser_obj = TWUser()
    twUser_obj.u_id = user_id
    twUser_obj.tw_id = api.me().id_str
    twUser_obj.brand_name = brand_name
    twUser_obj.username = api.me().screen_name

    TWUser.collection().update({"u_id": user_id, "brand_name": brand_name}, twUser_obj.serialize())
    saved_tw_user_obj = TWUser.unserialize(TWUser.collection().find_one({"u_id": user_id, "brand_name": brand_name}))

    update_brand_mapping(user_id, brand_name, "twitter", api.me().id_str, {"key": key, "secret": secret})

    t = Thread(target=save_tweets, args=(user_id, saved_tw_user_obj.tw_id, brand_name))
    t.setDaemon(False)
    t.start()

    return saved_tw_user_obj


def del_twitter_user(user_id, brand_name):
    update_brand_mapping(user_id, brand_name, "twitter")
    TWUser.collection().remove({"u_id": user_id, "brand_name": brand_name})


def get_tw_user(user_id, brand_name):
    dic = TWUser.collection().find_one({"u_id": str(user_id), "brand_name": brand_name})
    tw_user = TWUser.unserialize(dic) if dic is not None else None
    if tw_user is not None:
        brand_dic = BrandMapping.collection().find_one({"uid": user_id, "brand_name": brand_name})
        brand = BrandMapping.unserialize(brand_dic) if brand_dic is not None else None
    return tw_user, brand.twitter["access_token"]


def save_tweets(user_id, tw_id, brand_name):
    tw_user, access_token = get_tw_user(user_id, brand_name)
    api = get_api(access_token["key"], access_token["secret"])[0]

    for status in Cursor(api.home_timeline, count=200).items(ADD_USER_MAX_TWEET):
        save_tweet(status, tw_id)

    if TW_INDIVIDUAL_STREAM:
        activate_stream(user_id, brand_name)


def save_tweet(status, tw_id):
    status_dict = json.loads(status.json)
    tweet_obj = TWTweet()
    tweet_obj.tweet_id = status.id_str
    tweet_obj.tw_id = tw_id
    tweet_obj.user = status_dict["user"]
    tweet_obj.text = status_dict["text"]
    tweet_obj.fields = status_dict
    tweet_obj.created_at = status.created_at

    if TWTweet.collection().find_one({"tweet_id": tweet_obj.tweet_id, "tw_id": tweet_obj.tw_id}) is None:
        tweet_obj._id = TWTweet.collection().insert(tweet_obj.serialize())
    else:
        TWTweet.collection().update({"tweet_id": tweet_obj.tweet_id, "tw_id": tweet_obj.tw_id}, tweet_obj.serialize())
        tweet_obj = TWTweet.unserialize(TWTweet.collection().find_one({"tweet_id": tweet_obj.tweet_id, "tw_id": tweet_obj.tw_id}))

    return tweet_obj


def put_tweet(text, tw_id, key, secret, state, media_file):
    datetime_now = datetime.datetime.utcnow().isoformat('T')
    tw = TWTweet()
    tw.tw_id = tw_id
    tw.text = text
    tw.created_at = datetime_now

    if state == CampaignState.PUBLISHED:
        api = get_api(key, secret)[0]
        data = api.update_status(text)
        tw = save_tweet(data, tw_id)
    else:
        tw._id = TWTweet.collection().insert(tw.serialize())

    return tw


def del_tweet(id_str, obj_id, key, secret):
    if id_str is not None:
        api = get_api(key, secret)[0]
        data = api.destroy_status(id=long(id_str))
        print data
    TWTweet.collection().update({"_id": coerce_bson_id(obj_id)}, {"$set": {"is_deleted": 1}})


def post_tweet_reply(text, tw_id, in_reply_to, key, secret):
    api = get_api(key, secret)[0]
    data = api.update_status(status=text, in_reply_to_status_id=in_reply_to)
    tw = save_tweet(data, tw_id)
    return tw


def update_profile(key, secret, name=None, url=None, location=None, description=None):
    api = get_api(key, secret)[0]
    data = api.update_profile(name=name, url=url, location=location, description=description)



# live updates
def activate_stream(user_id, brand_name):
    """
    Activate twitter user stream
    """
    twUser, access_token = get_tw_user(user_id, brand_name)
    auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
    auth.set_access_token(access_token["key"], access_token["secret"])
    l = StreamListener(api=tweepy.API(auth))
    streamer = tweepy.Stream(auth, l)
    streamer.userstream(async=True)


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        save_tweet(status, self.api.me().id_str)
        return True

    def on_error(self, status):
        print status


# monkey patch for tweepy to get json

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse


#
#code below is deprecated or not tested with new implementation
#

def get_tweets(user_id, tw_id, count=None, since_id=None, max_id=None):
    """
    Incomplete implementation (input optional arguments into api.home_timeline)
    """
    user = get_tw_user(user_id, tw_id)
    auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
    auth.set_access_token(user.token_key, user.token_secret)
    api = tweepy.API(auth)

    return api.home_timeline()