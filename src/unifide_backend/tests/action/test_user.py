from unifide_backend.tests.test_base import TestBase
from unifide_backend.action.user import save_user


class UserTests(TestBase):
    def test_save_user(self):
        print "test_save_user"
        user = save_user("testing@kianwei.com", "password")
        print user
        assert user is not None