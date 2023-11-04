from ..db import db_client 
from ..schemas.profile_schema import Profile


table = db_client.client.table("matches")

def get_user_liked(uuid):
    '''
        Gets who a user has liked so far
    '''
    return table.select("*").eq("uuid",uuid).execute()

def delete_matches(curr_uuid, foreign_uuid):
    '''
        If a user deletes their account or simply unmatches it will get rid of both rows for both users
    '''
    table.delete().match({'uuid':curr_uuid, 'liked_user':foreign_uuid}).execute()
    table.delete().match({'uuid':foreign_uuid, 'liked_user':curr_uuid}).execute()


def create_user_liked(curr_uuid, foreign_uuid, match:bool):
    '''
        If the other user has liked the main user then it will be a match. Otherwise it will simply be one user liked another
    '''
    if not match:
        table.insert({"uuid": curr_uuid, "liked_user": foreign_uuid,"match":False}).execute()
    else:
        table.update({'match': True}).eq('uuid', curr_uuid).eq('liked_user', foreign_uuid).execute()
        table.upsert({'uuid': curr_uuid, 'liked_user': foreign_uuid, 'match': True}).execute()
        #update for both users since it is guaranteed that if they match they already have a row for each other

