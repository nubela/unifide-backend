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


class Alert(Base):
    def __init__(self, **kwargs):
        super(Alert, self).__init__()

        self.url = None
        self.title = None
        self.keyword = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Alert(**dic)

    @staticmethod
    def coll_name():
        return "alert"