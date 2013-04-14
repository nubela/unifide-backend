from base.scheduling.model import SchedulingBase


class Mapping(SchedulingBase):
    """
        social = facebook, twitter, foursquare
        campaign = web, iOS, android
        blog = blog
    """
    def __init__(self, **kwargs):
        super(Mapping, self).__init__()

        self.uid = None
        self.facebook_list = None
        self.twitter_list = None
        self.foursquare_list = None
        self.campaign_list = None
        self.blog_list = None
        self.is_published = None
        self.is_draft = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return Mapping(**dic)

    @staticmethod
    def coll_name():
        return "mapping"