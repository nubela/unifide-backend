class User:
    def __init__(self, **kwargs):
        self.id = None
        self.username = None
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.email = None
        self.passwd_hash = None

        #facebook
        self.fb = []

        #account meta
        self.account_status = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)


    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def serialize(self):
        return {k: v for k, v in self.__dict__.iteritems()}

    @staticmethod
    def unserialize(json):
        return User(**json.loads(json))


class FacebookUser:
    def __init__(self, **kwargs):
        self.fb_id = None
        self.access_token = None
        self.pages = []

        for k, v in kwargs.iteritems():
            setattr(self, k, v)


    def serialize(self):
        return {k: v for k, v in self.__dict__.iteritems()}


class FacebookPage:
    def __init__(self, **kwargs):
        self.page_id = None
        self.page_access_token = None
        self.category = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)


    def serialize(self):
        return {k: v for k, v in self.__dict__.iteritems()}