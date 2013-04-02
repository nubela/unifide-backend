from flask.helpers import json, jsonify
import urllib
from unifide_backend.tests.test_base import TestBase
from unifide_backend.action.social.facebook.model import FBPage
from unifide_backend.local_config import FB_APP_ID, FB_APP_SECRET, FB_REDIRECT_URI, FB_PERMS, \
    TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_REDIRECT_URI
import tweepy


class SocialConnectTests(TestBase):
    def _test_connect_facebook(self):
        print "test_connect_facebook"
        from unifide_backend.action.social.facebook.sdk import get_access_token_from_code
        from unifide_backend.action.social.facebook.action import get_fb_id, save_fb_user
        from unifide_backend.action.admin.user.action import get_user

        user_id = "xaa8LzkwtCCgb6BeP"
        facebook_code = "AQDGTtp1SjVpa1TeKcTfvikm909c56L9ObIWDmLayRYPSJ_qGFN8SPfEZRRTe6V0-XwKh45Vcd6BZAkFxXWsUGlBKNGkyZ1ToKGZztByuZgDYMnoUg-4nv2_nMrE60QmoHBYs4OpW6RjTWAUBUgdwv2vGuxzR1EPHIbpvT2zklVPXfnQbIotY6ulMLAhO-6iyzhVS7UWWA9QJzms6JymFv7T#_=_"

        user = get_user(user_id)
        result = get_access_token_from_code(facebook_code, FB_REDIRECT_URI, FB_APP_ID, FB_APP_SECRET)
        access_token, token_expiry = result["access_token"], result["expires"]
        fb_id = get_fb_id(access_token)
        fb_user = save_fb_user(user.get_id(), fb_id, access_token, token_expiry)

        assert fb_user.get_id()
        print fb_user.get_id()


    def _test_get_facebook_pages(self):
        print "test_get_facebook_pages"
        from unifide_backend.action.social.facebook.action import get_fb_user, get_fb_page_list

        user_id = "xaa8LzkwtCCgb6BeP"

        fbUser = get_fb_user(user_id)
        page_list = get_fb_page_list(fbUser.fb_id, fbUser.access_token)

        assert page_list is not None
        print json.dumps({"status": "ok", "page_list": page_list})


    def _test_put_facebook_page(self):
        print "test_put_facebook_page"
        from unifide_backend.action.social.facebook.action import get_avail_slots, get_fb_user, get_fb_page_list, save_fb_page

        user_id = "xaa8LzkwtCCgb6BeP"
        fb_page_id = "493620310673753"

        fbUser = get_fb_user(user_id)

        if fbUser is not None and get_avail_slots(user_id) == 0:
            assert False

        page_list = get_fb_page_list(fbUser.fb_id, fbUser.access_token)

        for page in page_list:
            if page["id"] == fb_page_id:
                fbPage_obj = save_fb_page(fbUser.u_id, fbUser.fb_id, page["name"],
                                          page["id"], page["category"], page["access_token"])
                break

        assert fbPage_obj is not None


    def _test_get_posts(self):
        print "test_get_posts"
        from unifide_backend.action.social.facebook.action import get_fb_page, get_fb_posts

        user_id = "xaa8LzkwtCCgb6BeP"
        page_id = "493620310673753"

        print get_fb_posts(page_id, get_fb_page(user_id, page_id).page_access_token)


    def _test_save_posts(self):
        print "test_save_posts"
        from unifide_backend.action.social.facebook.action import get_fb_posts, get_fb_page, save_fb_posts

        user_id = "xaa8LzkwtCCgb6BeP"
        page_id = "493620310673753"

        posts = get_fb_posts(page_id, get_fb_page(user_id, page_id).page_access_token)
        print posts["data"]
        save_fb_posts(posts["data"], page_id)


    def _test_auth_twitter(self):
        print "test_auth_twitter"

        auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_REDIRECT_URI)

        try:
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError:
            print 'Error! Failed to get request token.'

        assert redirect_url is not None
        print "url: " + str(redirect_url)
        print "token key: " + str(auth.request_token.key)
        print "token secret: " + str(auth.request_token.secret)


    def _test_connect_twitter(self):
        print "test_connect_twitter"
        from unifide_backend.action.social.twitter.action import save_tw_user

        user_id = "xaa8LzkwtCCgb6BeP"
        verifier = "dCEqbii65ERrisHvv0tkqvFlbQMPFEYaKzdDhQKSQbE"
        token = "MhWHfcvBRAKsYLvcV8SOoZYeA1YI425U4AxBrxDAE"
        token_secret = "YqlmXejvSuvTLVGclBxNpiEQWDUJE1fAI4L6UH3eT74"

        auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
        auth.set_request_token(token, token_secret)

        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print 'Error! Failed to get access token.'
            assert False

        tw_user = save_tw_user(user_id, auth.access_token.key, auth.access_token.secret)
        if tw_user is None:
            assert False

        print "access token key: " + str(auth.access_token.key)
        print "access token secret: " + str(auth.access_token.secret)


    def _test_get_tweets(self):
        print "test_get_tweets"
        from unifide_backend.action.social.twitter.action import get_tweets

        user_id = "xaa8LzkwtCCgb6BeP"
        tw_id = "1130701424"

        for status in get_tweets(user_id, tw_id):
            print status.text
            print status.user.name
            print

    def _test_save_tweets(self):
        # get and save tweets
        # set up streaming API to receive tweets
        print "test_save_tweets"
        from unifide_backend.action.social.twitter.action import save_tweets

        user_id = "xaa8LzkwtCCgb6BeP"
        tw_id = "1130701424"

        save_tweets(user_id, tw_id)

    def _test_rate_limit_status(self):
        print "test_rate_limit_status"
        from unifide_backend.action.social.twitter.action import get_tw_user, get_api

        user_id = "xaa8LzkwtCCgb6BeP"
        tw_id = "1130701424"

        twUser = get_tw_user(user_id, tw_id)
        api = get_api(twUser.token_key, twUser.token_secret)[0]

        result = api.rate_limit_status(resources="statuses")["resources"]["statuses"]
        for k, v in result.iteritems():
            print k, v


    def test_activate_stream(self):
        print "test_activate_stream"
        from unifide_backend.action.social.twitter.action import activate_stream

        user_id = "xaa8LzkwtCCgb6BeP"
        tw_id = "1130701424"

        activate_stream(user_id, tw_id)


