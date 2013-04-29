from base.scheduling.model import SchedulingBase
from base.base_model import Base


class Mapping(SchedulingBase):
    """
        campaign = web, iOS, android
    """
    def __init__(self, **kwargs):
        super(Mapping, self).__init__()

        self.uid = None
        self.brand_name = None
        self.facebook = None
        self.twitter = None
        self.foursquare = None
        self.campaign = None
        self.blog = None
        self.state = None

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


class BrandMapping(Base):
    def __init__(self, **kwargs):
        super(BrandMapping, self).__init__()

        self.uid = None
        self.brand_name = None
        self.facebook = None
        self.twitter = None
        self.foursquare = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return BrandMapping(**dic)

    @staticmethod
    def coll_name():
        return "brand_mapping"


class CampaignState:
    DRAFT="draft"
    PUBLISHED="published"
    SCHEDULED="scheduled"