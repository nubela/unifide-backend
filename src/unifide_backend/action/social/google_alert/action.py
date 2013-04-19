import galerts
from unifide_backend.action.social.google_alert.model import Keyword
from unifide_backend.action.util import readable, generator_to_list
from unifide_backend.local_config import GOOGLE_USERNAME, GOOGLE_PASSWD_ENCODED


def get_keywords():
    """
    Gets all registered keywords
    """
    pass


def _get_alert_from_keyword(kw):
    filtered = filter(lambda x: x.query == kw, generator_to_list(_gam().alerts))
    if len(filtered) > 0:
        return filtered[0]
    return None


def _gam():
    gam = galerts.GAlertsManager(GOOGLE_USERNAME, readable(GOOGLE_PASSWD_ENCODED))
    return gam


def register(keyword, async=False):
    """
    Registers a keyword for a Google Alert
    """
    #check
    if _get_alert_from_keyword(keyword) is not None:
        return

    #create record as in-progress in db first (for reactivity)
    kw_obj = Keyword()
    kw_obj.keyword = keyword
    kw_obj.status = AlertCreationStatus.IN_PROGRESS
    coll = Keyword.collection()
    kw_obj._id = coll.save(kw_obj.serialize())

    #create it on google alerts
    gam = _gam()
    gam.create(keyword, galerts.TYPE_EVERYTHING, feed=True, freq=galerts.FREQ_AS_IT_HAPPENS, vol=galerts.VOL_ALL)

    #get newly created alerts if it exists, else delete the doc
    alert = _get_alert_from_keyword(keyword)
    if alert is not None:
        kw_obj.status = AlertCreationStatus.CREATED
        kw_obj.feed_url = alert.feedurl
        coll.save(kw_obj.serialize())
    else:
        kw_obj.status = AlertCreationStatus.DELETED
        coll.save(kw_obj.serialize())


def get_mentions(limit=None):
    """
    In no order particularly, fetches the latest list of alerts given registered
    """
    if limit is None:
        limit = 5

    pass


def _update():
    """
    Polls the feeds to fetch the latest mentions
    """
    pass


class AlertCreationStatus:
    IN_PROGRESS = "in_progress"
    CREATED = "created"
    DELETED = "deleted"