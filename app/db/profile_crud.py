from ..db import db_client 
from ..profile_schema import Profile, UserAnimes


def post_new_user(profile:Profile):
    return db_client.client.table("users").insert({"uuid": profile.uuid, "username": profile.username, "gender": profile.gender, "sex_pref": profile.sex_pref, "genre": profile.genre, "bio": profile.bio}).execute()


def user_animes(animes: UserAnimes):
    data = [{"uuid": animes.uuid, "aid": anime} for anime in animes.animes]
    return db_client.client.table("user_animes").insert(data).execute()


    