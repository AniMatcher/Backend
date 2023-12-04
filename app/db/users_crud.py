from ..db import db_client 
from ..schemas.profile_schema import Profile, UserAnimes

table = db_client.client.table("users")

def get_user_by_uuid(uuid: str):
    return table.select("*").eq("uuid", uuid).execute()

def get_user_by_email(email: str):
    return table.select("*").eq("email", email).execute()

def post_new_user(profile:Profile):
    return table.insert({"uuid": profile.uuid, "username": profile.username, "gender": profile.gender, "sex_pref": profile.sex_pref, "genre": profile.genre, "bio": profile.bio, "image_profile": profile.image}).execute()

def post_blog(text: str, uuid):
    try:
        return table.update({'note' : text}).eq('uuid', uuid).execute()
    except:
        return 

def get_blog(uuid):
    return table.select("note").eq('uuid', uuid).execute()


def get_all_desired_user(gender:str, uuid, prev_liked:list, num):
    '''
        Gets all the users that are the desired gender and makes sure the user is not included. This function only supports choosing one gender.
        num: chooses how many desired users to get
        prev_like: previous people the user liked are not added to the list of possible desired individuals
    '''
    return table.select("*").eq("gender", gender).neq("uuid", uuid).not_.in_('uuid', prev_liked).limit(num).execute()

def put_edit_user(profile: Profile):
    update_data = {
        "uuid": profile.uuid,
        "username": profile.username,
        "gender": profile.gender,
        "sex_pref": profile.sex_pref,
        "genre": profile.genre,
        "bio": profile.bio,
        "image_profile": profile.image
    }
    return table.update(update_data).eq("uuid", profile.uuid).execute()

