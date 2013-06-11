from datetime import datetime
from time import mktime
import feedparser
import galerts
from unifide_backend.action.social.brand_mention.model import Keyword, Mention
from unifide_backend.action.util import readable, generator_to_list
from unifide_backend.local_config import GOOGLE_USERNAME, GOOGLE_PASSWD_ENCODED


def del_keyword(keyword_str, async=False):
    kw_obj = get_keyword_from_str(keyword_str)
    if kw_obj is None: return

    #delete off db
    Keyword.collection().remove({"_id": kw_obj.obj_id()})

    #dleete off google alert account
    alert_obj = _get_alert_from_keyword(keyword_str)
    _gam().delete(alert_obj)


def get_keyword_from_str(kw):
    dic = Keyword.collection().find_one({"keyword": kw})
    return Keyword.unserialize(dic) if dic is not None else None


def get_str_keywords():
    """
    Gets all registered keywords
    """
    alerts = generator_to_list(_gam().alerts)
    return [x.query for x in alerts]


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


def _update():
    """
    Polls the feeds to fetch the latest mentions
    """
    coll = Keyword.collection()
    keyword_obj_lis = [Keyword.unserialize(x) for x in coll.find()]
    for keyword in keyword_obj_lis:
        d = feedparser.parse(keyword.feed_url)
        for entry in d["entries"]:
            if get_mention_by_alert_id(entry["id"]) is None and entry["title"] != "Feeds for Google Alerts":
                _save_mention(keyword.keyword, entry)


def get_mention_by_alert_id(alert_id):
    coll = Mention.collection()
    dic = coll.find_one({
        "alert_id": alert_id
    })
    return Mention.unserialize(dic) if dic is not None else None


def _save_mention(keyword, feed_entry):
    coll = Mention.collection()
    mention_obj = Mention()
    mention_obj.url = feed_entry["link"]
    mention_obj.summary = feed_entry["summary"]
    mention_obj.title = feed_entry["title"]
    mention_obj.alert_id = feed_entry["id"]
    mention_obj.keyword = keyword
    mention_obj.modification_timestamp_utc = datetime.fromtimestamp(mktime(feed_entry["published_parsed"]))
    coll.save(mention_obj.serialize())


class AlertCreationStatus:
    IN_PROGRESS = "in_progress"
    CREATED = "created"
    DELETED = "deleted"