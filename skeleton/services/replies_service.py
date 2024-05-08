from data.database import read_query, update_query
from data.models import Reply


def vote_on_reply(reply_id: int, user_id: int, vote_type: bool) -> bool:

    query = "SELECT 1 FROM reply_votes WHERE reply_id = ? AND user_id = ?"
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
