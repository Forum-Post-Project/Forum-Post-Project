from data.database import insert_query, read_query, update_query
from datetime import datetime
from data.models import Topic, Reply
from services import categories_service
from common.responses import Forbidden, BadRequest
from data.models import TopicWithReplies


def create_topic(title: str, category_id: int, user_id: int) -> Topic or None:
    query = "insert into topics (title, category_id, user_id, creation_date) values (?,?,?,?)"
    category = categories_service.get_category_by_id(category_id)
    if category.is_locked:
        return Forbidden(content="Category is locked!")
    params = (title, category_id, user_id, datetime.now().strftime("%Y-%m-%d %H:%M"))
    topic_id = insert_query(query, params)
    if topic_id:
        return Topic(id=topic_id,
                     title=title,
                     category_id=category_id,
                     user_id=user_id,
                     creation_date=params[-1])
    else:
        return None


def get_all_topics(search: str = None, sort_by: str = None, limit: int = 10, offset: int = 0):
    base_query = """select * from topics"""
    params = ()
    if search:
        base_query += f""" where title like ?"""
        params += (f"%{search}%",)

    if sort_by:
        if sort_by.lower() in ["oldest", "newest"]:
            if sort_by.lower() == "oldest":
                base_query += """ order by creation_date asc"""
            else:
                base_query += """ order by creation_date desc"""
        else:
            return BadRequest(content="Sorting topics only using 'oldest' or 'newest'!")

    base_query += f""" limit {limit} offset {offset}"""
    query_result = read_query(base_query, params)
    topics = [Topic.from_query_result(*row) for row in query_result]
    return topics


def get_topic_with_replies(topic_id: int) -> TopicWithReplies or None:
    topic_query = """select title, category_id from topics where topic_id = ?"""
    topic_result = read_query(topic_query, (topic_id,))
    if not topic_result:
        return None

    topic_title, category_id = topic_result[0]

    reply_query = """select * from replies where topic_id = ?"""
    reply_result = read_query(reply_query, (topic_id,))

    replies = [Reply.from_query_result(*reply_data) for reply_data in reply_result]

    return TopicWithReplies(category_id=category_id, title=topic_title, replies=replies)


def get_topic(topic_id: int):
    query = """select * from topics where topic_id = ?"""
    result = read_query(query, (topic_id,))
    if result:
        return result[0]
    else:
        return None


def lock_topic(topic_id: int):
    query = """update topics set is_locked = 1 where topic_id = ?"""
    update_query(query, (topic_id,))
