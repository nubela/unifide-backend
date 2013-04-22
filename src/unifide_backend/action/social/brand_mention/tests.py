import unittest
from unifide_backend.action.social.brand_mention.action import register, _get_alert_from_keyword


class GAlertTests(unittest.TestCase):

    def test_register(self):
        register("nubela2", async=False)
        assert _get_alert_from_keyword("nubela2") is not None
