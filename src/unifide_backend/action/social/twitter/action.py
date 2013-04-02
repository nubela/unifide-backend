from unifide_backend.local_config import TW_CONSUMER_KEY, TW_CONSUMER_SECRET, ADD_USER_MAX_TWEET
from unifide_backend.action.social.twitter.model import TWUser, TWTweet, _TWUser
from unifide_backend.action.admin.user.action import get_max_brands
from threading import Thread
import tweepy
from tweepy.cursor import Cursor

def get_api(key, secret):
    """
    Retrieve twitter API object based on user's access token key and secret
    """
    auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
    auth.set_access_token(key, secret)
    return tweepy.API(auth), auth.access_token.key, auth.access_token.secret


def get_avail_slots(user_id):
    """
    Check if unifide account has reached business/brand subscription limit
    """
    max_brand = get_max_brands(user_id)
    twUser = get_tw_users(user_id)

    return max_brand - (twUser.count() if twUser is not None else 0)


def save_tw_user(user_id, key, secret):
    """
    Add twitter account to the unifide user and spawn thread to pull recent tweewts from home timeline
    """
    api, token_key, token_secret = get_api(key, secret)

    def save_obj():
        twUser_obj = TWUser()
        twUser_obj.u_id = user_id
        twUser_obj.tw_id = api.me().id_str
        twUser_obj.username = api.me().screen_name
        twUser_obj.token_key = token_key
        twUser_obj.token_secret = token_secret
        twUser_obj._id = TWUser.collection().insert(twUser_obj.serialize())
        return twUser_obj

    # dupe check before inserting new fb user record into db
    twUser = TWUser.collection().find_one({"u_id": user_id, "tw_id": api.me().screen_name})
    if twUser is not None:
        saved_tw_user_obj = TWUser.unserialize(twUser)
    else:
        saved_tw_user_obj = save_obj()

    t = Thread(target=save_tweets, args=(user_id, saved_tw_user_obj.tw_id))
    t.setDaemon(False)
    t.start()

    return saved_tw_user_obj


def get_tw_user(user_id, tw_id):
    """
    To support unifide accounts with multiple twitter accounts
    """
    dic = TWUser.collection().find_one({"u_id": user_id, "tw_id": tw_id})
    return TWUser.unserialize(dic) if dic is not None else None


def get_tw_users(user_id):
    """
    To support unifide accounts with multiple twitter accounts
    """
    return TWUser.collection().find({"u_id": user_id})


def get_tweets(user_id, tw_id, count=None, since_id=None, max_id=None):
    """
    Incomplete implementation (input optional arguments into api.home_timeline)
    """
    user = get_tw_user(user_id, tw_id)
    auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
    auth.set_access_token(user.token_key, user.token_secret)
    api = tweepy.API(auth)

    return api.home_timeline()


def save_tweets(user_id, tw_id):
    """
    Pull X number of recent tweets from home timeline into database and cache users related to the tweets
    """
    twUser = get_tw_user(user_id, tw_id)
    api = get_api(twUser.token_key, twUser.token_secret)[0]
    user_cache_to_db = {}

    def save_obj(s):
        tweet_obj = TWTweet()
        tweet_obj.id = s.id_str
        tweet_obj.tw_id = str(tw_id)
        tweet_obj.user = s.user.id_str
        tweet_obj.text = s.text
        tweet_obj.coordinates = s.coordinates
        tweet_obj.created_at = s.created_at.strftime("%s")
        tweet_obj.entities = s.entities
        tweet_obj.favorite_count = s.favorite_count
        tweet_obj.retweet_count = s.retweet_count
        tweet_obj._id = TWTweet.collection().insert(tweet_obj.serialize())
        user_cache_to_db[s.user.id] = { "screen_name": s.user.screen_name, "profile_image_url": s.user.profile_image_url }
        return tweet_obj

    # save tweets into database
    for status in Cursor(api.home_timeline, count=200).items(ADD_USER_MAX_TWEET):
        if TWTweet.collection().find_one({"id": status.id}) is None:
            save_obj(status)

    # cache tweet owners into database
    for k,v in user_cache_to_db.iteritems():
        if _TWUser.collection().find_one({"tw_id": str(k)}) is None:
            cache_user = _TWUser()
            cache_user.tw_id = str(k)
            cache_user.screen_name = v["screen_name"]
            cache_user.profile_image_url = v["profile_image_url"]
            _TWUser.collection().insert(cache_user.serialize())
        else:
            _TWUser.collection().update({"tw_id": str(k)}, {"$set": {"screen_name": v["screen_name"], "profile_image_url": v["profile_image_url"]}})


def save_tweet(status, tw_id):

    def save_obj(s):
        tweet_obj = TWTweet()
        tweet_obj.id = s.id_str
        tweet_obj.tw_id = str(tw_id)
        tweet_obj.user = s.user.id_str
        tweet_obj.text = s.text
        tweet_obj.coordinates = s.coordinates
        tweet_obj.created_at = s.created_at.strftime("%s")
        tweet_obj.entities = s.entities
        tweet_obj.favorite_count = s.favorite_count
        tweet_obj.retweet_count = s.retweet_count

        tweeter_obj = _TWUser()
        tweeter_obj.tw_id = s.user.id_str
        tweeter_obj.screen_name = s.user.screen_name
        tweeter_obj.profile_image_url = s.user.profile_image_url

        return tweet_obj, tweeter_obj

    tweet, tweeter = save_obj(status)

    if TWTweet.collection().find_one({"id": tweet.id}) is None:
        TWTweet.collection().insert(tweet.serialize())

    if _TWUser.collection().find_one({"tw_id": tweeter.tw_id}) is None:
        _TWUser.collection().insert(tweeter.serialize())
    else:
        _TWUser.collection().update({"tw_id": tweeter.tw_id}, {"$set": {"screen_name": tweeter.screen_name, "profile_image_url": tweeter.profile_image_url}})

    print "tweet: " + str(tweet)
    print "tweeter: " + str(tweeter)


def activate_stream(user_id, tw_id):
    """
    Activate twitter user stream
    """
    twUser = get_tw_user(user_id, tw_id)
    auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
    auth.set_access_token(twUser.token_key, twUser.token_secret)
    l = StreamListener(api=tweepy.API(auth))
    streamer = tweepy.Stream(auth, l)
    streamer.userstream(async=True)


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        save_tweet(status, self.api.me().id)
        return True

    def on_error(self, status):
        print status