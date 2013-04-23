from base.base_model import Base


class TWUser(Base):
    def __init__(self, **kwargs):
        self.tw_id = None
        self.u_id = None
        self.username = None
        self.brand_name = None
        self.oauth_key = None
        self.oauth_secret = None
        self.added_on = None
        self.created_at = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return TWUser(**dic)

    @staticmethod
    def coll_name():
        return "tw_user"


class TWTweet(Base):
    def __init__(self, **kwargs):
        self.tweet_id = None
        self.tw_id = None
        self.user = None
        self.text = None
        self.fields = None
        self.created_at = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return TWTweet(**dic)

    @staticmethod
    def coll_name():
        return "tw_tweet"