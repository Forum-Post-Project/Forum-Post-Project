from data.database import insert_query, read_query
from data.models import Message
from common.responses import CreatedSuccessfully
from datetime import datetime


def create_message(text: str, sender_id: int, receiver_id: int) -> Message or None:
    query = """insert into messages (text, sender_id, receiver_id, creation_date) values (?, ?, ?, ?)"""
    params = (text, sender_id, receiver_id, datetime.now())
    message_id = insert_query(query, params)
    if message_id:
        return Message(id=message_id, text=text, sender_id=sender_id, receiver_id=receiver_id, creation_date=params[-1])
    else:
        return None


def get_conversation(sender_id: int, receiver_id: int) -> list[Message]:
    query = """select message_id, text, sender_id, receiver_id, creation_date 
               from messages 
               where (sender_id = ? and receiver_id = ?) or (sender_id = ? and receiver_id = ?) 
               order by creation_date"""
    params = (sender_id, receiver_id, receiver_id, sender_id)
    data = read_query(query, params)
    return [Message.from_query_result(*row) for row in data]


def get_all_conversations(sender_id: int) -> list[Message]:
    query = """select message_id, text, sender_id, receiver_id, creation_date 
               from messages 
               where sender_id = ? or receiver_id = ? 
               order by creation_date"""
    params = (sender_id, sender_id)
    data = read_query(query, params)
    return [Message.from_query_result(*row) for row in data]
