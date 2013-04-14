from base.base_model import Base


class CPMenu(Base):
    def __init__(self, **kwargs):
        self.uid = None
        self.order = None
        self.first_lvl = None
        self.second_lvl = []

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return CPMenu(**dic)

    @staticmethod
    def coll_name():
        return "cp_menu"


class CPMenuItem(Base):
    def __init__(self, **kwargs):
        self.name = None
        self.link = None
        self.order = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return CPMenuItem(**dic)