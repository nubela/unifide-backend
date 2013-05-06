from unifide_backend.action.mapping.model import Mapping, BrandMapping
from base.scheduling.decorator import schedulable
from base.util import coerce_bson_id
from unifide_backend.action.admin.user.action import get_max_brands


@schedulable
def save(mapping_obj):
    col = Mapping.collection()
    id = col.insert(mapping_obj.serialize())
    return id


def put_mapping(uid, brand_name, kvp, publish_datetime, type, state):
    mapping_obj = Mapping()
    mapping_obj.uid = uid
    mapping_obj.brand_name = brand_name
    mapping_obj.state = state
    mapping_obj.type = type
    mapping_obj.publish_datetime = publish_datetime

    for k,v in kvp.iteritems():
        setattr(mapping_obj, k, v)

    mapping_obj._id = save(mapping_obj)
    return mapping_obj


def get_mapping(mapping_obj_id):
    collection = Mapping.collection()
    if mapping_obj_id is None:
        return None
    dic = collection.find_one({"_id": coerce_bson_id(mapping_obj_id)})
    return Mapping.unserialize(dic) if dic is not None else None


def del_mapping(mapping_obj_id):
    collection = Mapping.collection()
    if mapping_obj_id is None:
        return None
    dic = collection.update({"_id": coerce_bson_id(mapping_obj_id)}, {"$set": {"is_deleted": 1} })


def get_brand_mapping(user_id, brand_name):
    collection = BrandMapping.collection()
    if user_id is None or brand_name is None:
        return None
    dic = collection.find_one({"uid": user_id, "brand_name": brand_name})
    return BrandMapping.unserialize(dic) if dic is not None else None


def get_brand_platform_id(user_id, brand_id, platform):
    dic = BrandMapping.collection().find_one({"uid": user_id, "_id": coerce_bson_id(brand_id)})
    brand = BrandMapping.unserialize(dic) if dic is not None else None
    return getattr(brand, platform)


def get_brand_available_slots(user_id, platform):
    avail_max_brands = get_max_brands(user_id)
    dic_list = BrandMapping.collection().find({"uid": user_id})
    for d in dic_list:
        brand = BrandMapping.unserialize(d)
        avail_max_brands = (avail_max_brands-1) if getattr(brand, platform) is not None else avail_max_brands

    return avail_max_brands


def update_brand_mapping(user_id, brand_name, platform, platform_id=None, access_token=None):
    if platform_id is None and access_token is None:
        BrandMapping.collection().update({"uid": user_id, "brand_name": brand_name}, {"$set": {platform: None}})
    else:
        BrandMapping.collection().update({"uid": user_id, "brand_name": brand_name}, {"$set": {platform: {"id": platform_id, "access_token": access_token}}})


def put_new_user_mapping(user_id):
    brand_mapping_obj = BrandMapping()
    brand_mapping_obj.uid = user_id
    brand_mapping_obj.brand_name = "default"
    brand_mapping_obj.is_selected = 1
    brand_mapping_obj._id = BrandMapping.collection().insert(brand_mapping_obj.serialize())
    return brand_mapping_obj
