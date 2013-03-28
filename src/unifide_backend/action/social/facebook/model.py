from base.base_model import Base


class FBUser(Base):
    def __init__(self, **kwargs):
        self.u_id = None
        self.fb_id = None
        self.access_token = None
        self.expires = None
        self.pages = []

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
        self.category = None
        self.page_access_token = None
        self.is_published = None
        self.likes = None
        self.location = None
        self.phone = None
        self.check_ins = None
        self.cover = None
        self.website = None
        self.talking_about_count = None
        self.hours = None

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
        self.name = None
        self.start_time = None
        self.end_time = None
        self.description = None
        self.location = None

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
        self.page_id = None
        self.picture = None
        self.link = None
        self.link_name = None
        self.caption = None
        self.description = None
        self.source = None
        self.source_properties = None
        self.type = None
        self.likes = None
        self.place = None
        self.with_tags = None
        self.comments = []
        self.object_id = None
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
        self.id = None;
        self.user = None
        self.text = None
        self.like_count = None
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