from unifide_backend.tests.test_base import TestBase
from unifide_backend.action.user import save_test_user, del_test_user, save_fb_oauth, get_user, save_fb_page, get_user_access_token
from unifide_backend.action.social.facebook import get_page_list, get_page_access_token
from flask.helpers import jsonify

TEST_USER_TOKEN = "AAAEyCP2iuwwBAFQEZCV2XcJ1HQkMHZBd8EzQh4tB05POfL47bRVRDQWwqHq1i8iqQgSYatQAqy2PHxNOVQJCqxSZByFM1t4mW5eWaLU4wZDZD"
TEST_PAGE_ID = "493620310673753"

class UserTests(TestBase):
    def test_save_user_with_fb_oauth(self):
        user_id = save_test_user("testing@kianwei.com", "password")
        page_list, fb_id = get_page_list(TEST_USER_TOKEN)
        user = get_user(user_id)
        fbUser_id = save_fb_oauth(user, TEST_USER_TOKEN, fb_id)
        #del_test_user(user)

        assert fbUser_id is not None


    def test_save_fb_page(self):
        user_id = save_test_user("testing@kianwei.com", "password")
        user_access_token = get_user_access_token(user_id)
        page_access_token, page_name = get_page_access_token(TEST_PAGE_ID, user_access_token)
        user = get_user(user_id)
        fbPage_id = save_fb_page(user, TEST_PAGE_ID, user_access_token, page_access_token, page_name)

        assert fbPage_id is not None