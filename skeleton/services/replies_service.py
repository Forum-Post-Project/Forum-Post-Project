from datetime import datetime
from data.database import read_query, update_query, insert_query
from data.models import Reply
from common.responses import BadRequest
from data.models import ReplyWithVotes


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


def get_reply_by_id(reply_id: int) -> Reply or None:
    query = """select * from replies where reply_id = ?"""
    params = (reply_id,)

    data = read_query(query, params)

    if not data:
        return None
    else:
        return Reply.from_query_result(*data[0])


def get_reply_with_votes(reply_id: int) -> ReplyWithVotes | None:
    query = """
        select r.reply_id, r.text, r.topic_id, r.user_id, r.creation_date, 
               ifnull(v.vote_type, 0) as vote_type
        from replies r
        left join votes v on r.reply_id = v.reply_reply_id
        where r.reply_id = ?
    """
    params = (reply_id,)
    result = read_query(query, params)

    if result:
        reply_data = result[0]

        return ReplyWithVotes(
            id=reply_data[0],
            text=reply_data[1],
            topic_id=reply_data[2],
            user_id=reply_data[3],
            creation_date=reply_data[4],
            vote_type=reply_data[5]
        )
    else:
        return None


def upvote_reply(reply_id: int, user_id: int):
    if not has_upvoted(reply_id, user_id):
        vote_reply(reply_id, 1, user_id)
    else:
        return BadRequest(content="User has already upvoted this reply")


def downvote_reply(reply_id: int, user_id: int):
    if not has_downvoted(reply_id, user_id):
        vote_reply(reply_id, -1, user_id)
    else:
        return BadRequest(content="User has already downvoted this reply")


def vote_reply(reply_id: int, vote_type: int, user_id: int) -> None:
    query = """
        insert into votes (user_user_id, reply_reply_id, vote_type)
        values (?, ?, ?)
        on duplicate key update vote_type = values(vote_type)
    """
    params = (user_id, reply_id, vote_type)
    insert_query(query, params)


def has_upvoted(reply_id: int, user_id: int) -> bool:
    query = """select count(*) from votes where user_user_id = ? and reply_reply_id = ? and vote_type = 1"""

    params = (user_id, reply_id)
    result = read_query(query, params)
    return result[0][0] > 0


def has_downvoted(reply_id: int, user_id: int) -> bool:
    query = """select count(*) from votes where user_user_id = ? and reply_reply_id = ? and vote_type = -1"""
    params = (user_id, reply_id)
    result = read_query(query, params)
    return result[0][0] > 0
