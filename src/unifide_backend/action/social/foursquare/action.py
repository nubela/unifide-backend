import foursquare
from unifide_backend.local_config import FSQ_CLIENT_ID, FSQ_CLIENT_SECRET, FSQ_REDIRECT_URI
from unifide_backend.action.social.foursquare.model import FSQUser, FSQVenue, FSQTip, FSQCheckin
from unifide_backend.action.util import key_check


def get_api():
    return foursquare.Foursquare(client_id=FSQ_CLIENT_ID, client_secret=FSQ_CLIENT_SECRET, redirect_uri=FSQ_REDIRECT_URI)


def get_auth_url():
    return get_api().oauth.auth_url()


def get_access_token_from_fsq(code):
    return get_api().oauth.get_token(code)


def save_fsq_user(user_id, access_token):
    client = get_api()
    client.set_access_token(access_token)
    me = client.users()["user"]
    print me

    def save_obj():
        fsq_user = FSQUser()
        fsq_user.fsq_id = me["id"]
        fsq_user.u_id = user_id
        fsq_user.first_name = key_check(me, "firstName")
        fsq_user.last_name = key_check(me, "lastName")
        fsq_user.access_token = access_token
        fsq_user._id = FSQUser.collection().insert(fsq_user.serialize())
        return fsq_user

    user_check = FSQUser.collection().find_one({"u_id": user_id,"fsq_id": me["id"]})
    if user_check is not None:
        fsq_user_obj = FSQUser.unserialize(user_check)
    else:
        fsq_user_obj = save_obj()

    return fsq_user_obj


def get_fsq_user(user_id):
    dic = FSQUser.collection().find_one({"u_id": user_id})
    return FSQUser.unserialize(dic) if dic is not None else None