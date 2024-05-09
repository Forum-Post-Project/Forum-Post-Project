from fastapi import APIRouter, Header
from data.models import Topic, Reply
from common.authentication import get_user_or_raise_401
from common.responses import NotFound, BadRequest, Forbidden
from services import topics_services, categories_service
from typing import List, Optional
from data.models import CreateTopic


topics_router = APIRouter(prefix="/topics")


@topics_router.get("/")
def get_all_topics(search: Optional[str] = None, sort_by: Optional[str] = None,
                   limit: int = 10, offset: int = 0):
    topics = topics_services.get_all_topics(search, sort_by, limit, offset)
    return topics


@topics_router.get("/{topic_id}")
def get_topic_by_id(topic_id: int, token: str = Header()):
    topic = topics_services.get_topic_with_replies(topic_id)

    if not topic:
        return NotFound(content=f"Topic with id:{topic_id} does not exist!")

    category_id = topic.category_id
    category = categories_service.get_category_by_id(category_id)

    if not category:
        return NotFound(content=f"Category for topic with id:{topic_id} does not exist!")

    user = get_user_or_raise_401(token)

    if user.is_admin:
        return topic

    if category.is_private:
        if not categories_service.access_exists(user.id, category_id):
            return Forbidden(content=f"Cannot view topics! User does not have access to category with id:{category_id}")

        return topic

    return topic


@topics_router.post("/")
def create_new_topic(creating_topic: CreateTopic, token: str = Header()):
    if not creating_topic.title:
        return BadRequest(content="Topic title is required in order to create a topic!")
    if not creating_topic.category_id:
        return BadRequest(content="Topic can not exist without a category!")
    user = get_user_or_raise_401(token)
    new_topic = topics_services.create_topic(creating_topic.title, creating_topic.category_id, user.id)
    return new_topic


@topics_router.put("/{topic_id}/lock")
def lock_topic(topic_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)
    if not user.is_admin:
        return Forbidden(content="Only admins can lock topics")
    topic = topics_services.get_topic(topic_id)
    if not topic:
        return NotFound(content="Topic not found")

    topics_services.lock_topic(topic_id)
    return {"message": f"Topic with id:{topic_id} locked successfully"}
