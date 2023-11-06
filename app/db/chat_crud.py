from ..db import db_client 

table = db_client.client.table("chat")

def get_all_messages(uuid, foreign_uuid):
    '''
        Gets all the messages between two users
    '''

def add_message(uuid, foreign_uuid):
    '''
        User uuid adds a message between a chat with foreign_uuid
    '''
