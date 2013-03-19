from base.base_model import Base

class FacebookUser(Base):
    def __init__(self, **kwargs):
        self.fb_id = None
        self.access_token = None
        self.pages = []

        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class FacebookPage(Base):
    def __init__(self, **kwargs):
        self.page_id = None
        self.name = None
        self.page_access_token = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)