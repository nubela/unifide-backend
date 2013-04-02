from base.base_model import Base


class TWUser(Base):
    def __init__(self, **kwargs):
        self.tw_id = None
        self.u_id = None
        self.username = None
        self.token_key = None
        self.token_secret = None
        self.followers_count = None
        self.friends_count = None
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
        self.id = None
        self.tw_id = None
        self.user = None
        self.text = None
        self.coordinates = None
        self.created_at = None
        self.entities = None
        self.favorite_count = None
        self.retweet_count = None

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


class TWMedia(Base):
    def __init__(self, **kwargs):
        self.id = None
        self.media_url = None
        self.media_url_https = None
        self.url = None
        self.display_url = None
        self.expanded_url = None
        self.size = None
        self.type = None
        self.indices = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()


class TWUrl(Base):
    def __init__(self, **kwargs):
        self.url = None
        self.display_url = None
        self.expanded_url = None
        self.indices = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()


class TWUserMention(Base):
    def __init__(self, **kwargs):
        self.id = None
        self.screen_name = None
        self.name = None
        self.indices = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()


class TWHashTag(Base):
    def __init__(self, **kwargs):
        self.text = None
        self.indices = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()


class _TWUser(Base):
    def __init__(self, **kwargs):
        self.tw_id = None
        self.screen_name = None
        self.profile_image_url = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return _TWUser(**dic)

    @staticmethod
    def coll_name():
        return "_tw_user"