from base.base_model import Base


class FSQUser(Base):
    def __init__(self, **kwargs):
        self.fsq_id = None
        self.u_id = None
        self.first_name = None
        self.last_name = None
        self.access_token = None

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
    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return FSQTip(**dic)

    @staticmethod
    def coll_name():
        return "fsq_tip"