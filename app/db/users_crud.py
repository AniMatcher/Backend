from ..db import db_client 
from ..profile_schema import Profile, UserAnimes

table = db_client.client.table("users")

def get_user_by_uuid(uuid: str):
    return table.select("*").eq("uuid", uuid).execute()

def get_user_by_email(email: str):
    return table.select("*").eq("email", email).execute()

def post_new_user(profile:Profile):
    return table.insert({"uuid": profile.uuid, "username": profile.username, "gender": profile.gender, "sex_pref": profile.sex_pref, "genre": profile.genre, "bio": profile.bio}).execute()


