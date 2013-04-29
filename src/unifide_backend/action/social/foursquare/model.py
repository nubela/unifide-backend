from base.base_model import Base


class FSQUser(Base):
    def __init__(self, **kwargs):
        self.fsq_id = None
        self.u_id = None
        self.brand_name = None
        self.first_name = None
        self.last_name = None
        self.fields = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FSQUser(**dic)

    @staticmethod
    def coll_name():
        return "fsq_user"


class FSQVenue(Base):
    def __init__(self, **kwargs):
        self.venue_id = None
        self.name = None
        self.fields = None

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FSQVenue(**dic)

    @staticmethod
    def coll_name():
        return "fsq_venue"


class FSQCheckin(Base):
    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FSQCheckin(**dic)

    @staticmethod
    def coll_name():
        return "fsq_checkin"


class FSQTip(Base):
    def __init__(self, **kwargs):
        self.venue_id = None
        self.tip_id = None
        self.text = None
        self.fields = None
        self.createdAt = None

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FSQTip(**dic)

    @staticmethod
    def coll_name():
        return "fsq_tip"


class FSQPageUpdate(Base):
    def __init__(self, **kwargs):
        self.venue_id = None
        self.update_id = None
        self.shout = None
        self.fields = None
        self.createdAt = None

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FSQPageUpdate(**dic)

    @staticmethod
    def coll_name():
        return "fsq_pageupdate"