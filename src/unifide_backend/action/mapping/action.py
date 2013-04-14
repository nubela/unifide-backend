from unifide_backend.action.mapping.model import Mapping
from base.scheduling.decorator import schedulable
from base.util import coerce_bson_id


@schedulable
def save(mapping_obj):
    col = Mapping.collection()
    id = col.insert(mapping_obj.serialize())
    return id


def put_mapping(uid, kvp, publish_datetime, is_published=False, is_draft=False):
    mapping_obj = Mapping()
    mapping_obj.uid = uid
    mapping_obj.publish_datetime = publish_datetime
    mapping_obj.is_published = is_published
    mapping_obj.is_draft = is_draft

    for k,v in kvp.iteritems():
        old_val = getattr(mapping_obj, k) if getattr(mapping_obj, k) is not None else []
        old_val.append(v)
        setattr(mapping_obj, k, old_val)

    mapping_obj._id = save(mapping_obj)
    return mapping_obj


def get_mapping(mapping_obj_id):
    collection = Mapping.collection()
    if mapping_obj_id is None:
        return None
    dic = collection.find_one({"_id": coerce_bson_id(mapping_obj_id)})
    return Mapping.unserialize(dic) if dic is not None else None