from datetime import datetime
from data.database import read_query, update_query, insert_query
from data.models import Reply


def create_reply(text: str, topic_id: int, user_id: int) -> Reply | None:
    query = "insert into replies (text, topic_id, user_id, creation_date) values (?, ?, ?, ?)"
    params = (text, topic_id, user_id, datetime.now().strftime("%Y-%m-%d %H:%M"))
    reply_id = insert_query(query, params)

    if reply_id:
        return Reply(id=reply_id,
                     text=text,
                     topic_id=topic_id,
                     user_id=user_id,
                     creation_date=params[-1])
    else:
        return None


def vote_on_reply(reply_id: int, user_id: int, vote_type: bool) -> bool:

    query = """select 1 from reply_votes WHERE reply_id = ? AND user_id = ?"""
    params = (reply_id, user_id)
    existing_vote = read_query(query, params)
    
    if existing_vote:
        return False
    
    if vote_type:
        query = "UPDATE replies SET upvotes = upvotes + 1 WHERE reply_id = ?"
    else:
        query = "UPDATE replies SET downvotes = downvotes + 1 WHERE reply_id = ?"
    
    params = (reply_id,)
    rows_affected = update_query(query, params)
    
    return rows_affected > 0


def fav_a_reply(reply_id: int, user_id: int) -> bool:

    query = "SELECT 1 FROM replies WHERE reply_id = ? AND user_id = ?"
    params = (reply_id, user_id)
    reply_exists = read_query(query, params)
    
    if not reply_exists:
        return False
    
    query = "UPDATE replies SET is_favorite = 1 WHERE reply_id = ? AND user_id = ?"
    params = (reply_id, user_id)
    rows_affected = update_query(query, params)
    
    return rows_affected > 0
