from base.base_model import Base


class User(Base):
    def __init__(self, **kwargs):
        self.username = None
        self.emails = []
        self.createdAt = None
        self.profile = None
        self.services = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
            return self.id()

    @staticmethod
    def unserialize(dic):
        return User(**dic)

    @staticmethod
    def coll_name():
        return "users"


class UserOptions(Base):
    def __init__(self, **kwargs):
        self.u_id = None
        self.brands = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return UserOptions(**dic)

    @staticmethod
    def coll_name():
        return "user_options"