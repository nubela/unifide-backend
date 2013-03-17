from unifide_backend.util.db import __get_collection
from unifide_backend.models import User, FacebookUser


def get_user_from_email(email):
    user = __get_collection("users").find({"email": email})
    if user.count() > 0:
        return user[0]["_id"]
    return None


def save_user(email, passwd):
    user_id = get_user_from_email(email)
    if not user_id:
        user_obj = User()
        user_obj.email = email
        user_obj.passwd_hash = passwd
        #fbuser = FacebookUser()
        #fbuser.fb_id = "something"
        #fbuser.access_token = "another thing"

        user_id = __get_collection("users").insert(user_obj.serialize())
        #fbuser_id = __get_collection("users").update({"_id": user_id}, {"$push": {'fb': fbuser.serialize()}})

    return user_id