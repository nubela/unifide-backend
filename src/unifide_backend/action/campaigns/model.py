from base.base_model import Base


class CampaignMapping(Base):
    def __init__(self, **kwargs):
        self.uid = None
        self.facebook = None
        self.twitter = None
        self.foursquare = None
        self.web = None
        self.blog = None
        self.ios = None
        self.android = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return CampaignMapping(**dic)

    @staticmethod
    def coll_name():
        return "campaign_mapping"