from base.base_model import Base


class FBUser(Base):
    def __init__(self, **kwargs):
        self.u_id = None
        self.fb_id = None
        self.brand_name = None
        self.access_token = None
        self.expires = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FBUser(**dic)

    @staticmethod
    def coll_name():
        return "fb_user"


class FBPage(Base):
    def __init__(self, **kwargs):
        self.page_id = None
        self.name = None
        self.fields = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FBPage(**dic)

    @staticmethod
    def coll_name():
        return "fb_page"


class FBGroup(Base):
    def __init__(self, **kwargs):

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FBGroup(**dic)

    @staticmethod
    def coll_name():
        return "fb_group"

class FBEvent(Base):
    def __init__(self, **kwargs):
        self.event_id = None
        self.page_id = None
        self.owner = None
        self.fields = None
        self.created_time = None
        self.updated_time = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FBEvent(**dic)

    @staticmethod
    def coll_name():
        return "fb_event"


class FBPost(Base):
    def __init__(self, **kwargs):
        self.post_id = None
        self.page_id = None
        self.owner = None
        self.fields = None
        self.created_time = None
        self.updated_time = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FBPost(**dic)

    @staticmethod
    def coll_name():
        return "fb_post"


class FBComment(Base):
    def __init__(self, **kwargs):
        self.post_id = None
        self.comment_id = None;
        self.owner = None
        self.message = None
        self.like_count = None
        self.fields = None
        self.created_time = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FBComment(**dic)

    @staticmethod
    def coll_name():
        return "fb_comment"


class _FBUser(Base):
    def __init__(self, **kwargs):
        self.id = None
        self.name = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return _FBUser(**dic)

    @staticmethod
    def coll_name():
        return "_fb_user"