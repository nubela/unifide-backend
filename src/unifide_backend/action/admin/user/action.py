from unifide_backend.action.admin.user.model import User, UserOptions


def get_user(user_id):
    coll = User.collection()
    dic = coll.find_one({"_id": user_id})
    user_obj = User.unserialize(dic) if dic is not None else None
    return user_obj


def get_user_options(user_id):
    coll = UserOptions.collection()
    dic = coll.find_one({"u_id": str(user_id)})
    user_options_obj = UserOptions.unserialize(dic) if dic is not None else None
    return user_options_obj


def get_max_brands(user_id):
    return get_user_options(user_id).brands