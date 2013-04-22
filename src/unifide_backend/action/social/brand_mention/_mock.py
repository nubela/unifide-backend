"""
Util methods to mock data rows for google alerts
(to test reactivity, etc)
"""
from random import choice
import loremipsum
from base.util import __gen_uuid
from unifide_backend.action.social.brand_mention.action import register
from unifide_backend.action.social.brand_mention.model import Mention


def mock_mentions(times_to_mock=5):
    for _ in range(times_to_mock):
        m = Mention()
        m.alert_id = __gen_uuid()
        m.url = "http://unifide.sg"
        m.title = loremipsum.sentence(max_char=choice(range(20, 30)))
        m.summary = loremipsum.sentence(max_char=choice(range(20, 30)))
        m.keyword = __gen_uuid()
        Mention.collection().save(m.serialize())


def mock_keywords(times_to_mock=3):
    for _ in range(times_to_mock):
        kw = loremipsum.sentence(10)
        print "Registering %s.." % (kw)
        register(kw)
        print "Done"