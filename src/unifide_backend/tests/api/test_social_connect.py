from flask.helpers import json, jsonify
import urllib
from unifide_backend.tests.test_base import TestBase
from unifide_backend.action.social.facebook.model import FBPage
from unifide_backend.local_config import FB_APP_ID, FB_APP_SECRET, FB_REDIRECT_URI, FB_PERMS


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

        """
        u_id = "xaa8LzkwtCCgb6BeP"
        code = "value"
        data = {"user_id": u_id,
                "code": code
        }

        resp = self.client.put("/", data=data)
        print resp.data
        resp_dict = json.loads(resp.data)

        assert resp_dict["status"] == "ok"
        assert FBPage.collection().find({"u_id": u_id}).count() > 0
        """


    def _test_get_facebook_pages(self):
        print "test_get_facebook_pages"
        from unifide_backend.action.social.facebook.action import get_fb_users, get_fb_page_list

        user_id = "xaa8LzkwtCCgb6BeP"

        fbUsers = get_fb_users(user_id)
        page_list = []

        for k,v in get_fb_page_list(fbUsers).iteritems():
            page_list.append(v)

        assert page_list.count > 0
        print json.dumps({"status": "ok", "page_list": page_list})

        """
        data = {"user_id": ""}
        resp = self.client.get("/social_connect/facebook/page/?" + urllib.urlencode(data))
        resp_dict = json.loads(resp.data)
        print resp_dict["page_list"]
        assert resp_dict["status"] == "ok"
        """


    def test_put_facebook_page(self):
        print "test_put_facebook_page"
        from unifide_backend.action.social.facebook.action import get_avail_slots, get_fb_users, get_fb_page_list, save_fb_page

        user_id = "xaa8LzkwtCCgb6BeP"
        fb_page_id = "493620310673753"

        fbUsers = get_fb_users(user_id)

        if fbUsers is not None and get_avail_slots(user_id) == 0:
            assert False

        page_list = get_fb_page_list(fbUsers)

        print page_list
        for id,pages in page_list.iteritems():
            for page in pages:
                print page["id"]
                if page["id"] == fb_page_id:
                    fbPage_obj = save_fb_page(user_id, id, page["name"], page["id"], page["category"], page["access_token"])
                    break
            if fbPage_obj:
                break

        assert fbPage_obj is not None