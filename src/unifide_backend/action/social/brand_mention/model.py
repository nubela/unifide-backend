from base.base_model import Base


class Keyword(Base):
    def __init__(self, **kwargs):
        super(Keyword, self).__init__()

        self.keyword = None
        self.feed_url = None
        self.status = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Keyword(**dic)

    @staticmethod
    def coll_name():
        return "keyword"


class Mention(Base):
    def __init__(self, **kwargs):
        super(Mention, self).__init__()

        self.alert_id = None
        self.url = None
        self.title = None
        self.summary = None
        self.keyword = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Mention(**dic)

    @staticmethod
    def coll_name():
        return "mention"