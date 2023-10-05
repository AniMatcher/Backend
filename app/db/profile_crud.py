from ..db import db_client 
from ..profile_schema import Profile

def post_new_user(profile:Profile):
    return db_client.client.table("users").insert({"uuid": profile.uuid, "username": profile.username, "gender": profile.gender, "sex_pref": profile.sex_pref, "genre": profile.genre, "bio": profile.bio}).execute()
