from base.base_model import Base


class BrandConfig(Base):
    def __init__(self, **kwargs):
        super(BrandConfig, self).__init__()

        self.name = None
        self.value = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def get_id(self):
        return self.id()

    @staticmethod
    def unserialize(dic):
        return BrandConfig(**dic)

    @staticmethod
    def coll_name():
        return "brand_config"