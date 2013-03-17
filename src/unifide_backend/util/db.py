from unifide_backend.local_config import SQL_URI, DB_NAME
from pymongo import MongoClient


def get_mongo(db=[]):
    """
    This function employs a good ol` gotcha with using mutable objects as a default value for an argument to cache
    the database object.

    If the `db` arg is an empty list, populate it with the object.
    Every other call to this function will skip the if clause and return the cached `db` object.
    Win.
    """
    if db == []:
        connection = MongoClient(SQL_URI)
        mongo_db = connection[DB_NAME]
        db += [mongo_db]
    return db[0]


def __get_collection(collection_name, coll=[]):
    if coll == []:
        mongo_db = get_mongo()
        collection = mongo_db[collection_name]
        coll += [collection]
    return coll[0]