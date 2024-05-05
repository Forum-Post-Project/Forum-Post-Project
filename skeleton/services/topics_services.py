from data.database import insert_query, read_query
from datetime import date
from data.models import Topic, Reply
from pydantic import BaseModel


class TopicWithReplies(BaseModel):
    title: str
    replies: list[Reply | None]


def create_topic(title: str, category_id: int, user_id) -> Topic or None:
    query = "insert into topics (title, category_id, user_id, creation_date) values (?,?,?,?)"
    params = (title, category_id, user_id, date.today())
    topic_id = insert_query(query, params)
    if topic_id:
        return Topic(topic_id=topic_id,
                     title=title,
                     category_id=category_id,
                     user_id=user_id,
                     creation_date=params[-1])
    else:
        return None


def get_all_topics(search: str = None, sort_by: str = None, limit: int = 10, offset: int = 0):
    base_query = "SELECT * FROM topics"
    if search:
        base_query += f" WHERE title LIKE '%{search}%'"
    if sort_by:
        base_query += f" ORDER BY {sort_by}"

    base_query += f" LIMIT {limit} OFFSET {offset}"
    query_result = read_query(base_query)
    topics = [Topic.from_query_result(*row) for row in query_result]
    return topics


def get_topic_with_replies(topic_id: int):
    topic_query = "SELECT title FROM topics WHERE topic_id = ?"
    topic_result = read_query(topic_query, (topic_id,))
    if not topic_result:
        return None
    topic_title = topic_result[0][0]

    reply_query = "SELECT * FROM replies WHERE topic_id = ?"
    reply_result = read_query(reply_query, (topic_id,))
    replies = [Reply.from_query_result(*reply_data) for reply_data in reply_result]
    topic = TopicWithReplies(title=topic_title, replies=replies)
    return topic