from fastapi import APIRouter, Header
from data.models import Topic, Reply
from common.authentication import get_user_or_raise_401
from common.responses import NotFound, BadRequest, Forbidden
from services import topics_services, categories_service
from typing import List, Optional
from data.models import CreateTopic, ChooseBestReply


topics_router = APIRouter(prefix="/topics")


@topics_router.get("/")
def get_all_topics(search: Optional[str] = None, sort_by: Optional[str] = None,
                   limit: int = 10, offset: int = 0, token: str = Header()):

    user = get_user_or_raise_401(token)

    topics = topics_services.get_all_topics(search, sort_by, limit, offset, user.id)

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
            return Forbidden(content=f"Cannot view topic with id:{topic_id}! "
                                     f"User does not have access to category with id:{category_id}"
                                     f" to which the topic belongs to!")

        return topic

    return topic


@topics_router.post("/")
def create_new_topic(creating_topic: CreateTopic, token: str = Header()):
    if not creating_topic.title:
        return BadRequest(content="Topic title is required in order to create a topic!")
    if not creating_topic.category_id:
        return BadRequest(content="Topic can not exist without a category!")

    user = get_user_or_raise_401(token)

    category = categories_service.get_category_by_id(creating_topic.category_id)

    if not category:
        return NotFound(content=f"Category with id:{creating_topic.category_id} not found!")

    if category.is_locked:
        return Forbidden(f"Category with id:{creating_topic.category_id} is locked and does not accept new topics")

    if category.is_private:
        if not categories_service.access_exists(user.id, creating_topic.category_id):
            return Forbidden(f"Category with id:{creating_topic.category_id} is private! User does not have access to "
                             f"it!")
        if not categories_service.check_write_access(user.id, creating_topic.category_id):
            return Forbidden(f"User with id:{user.id} does not have 'Write' access "
                             f"to category with id: {creating_topic.category_id}")

    new_topic = topics_services.create_topic(creating_topic.title, creating_topic.category_id, user.id)

    if user.is_admin:
        return new_topic

    return new_topic


@topics_router.put("/{topic_id}/choose_best_reply")
def choose_best_reply(topic_id: int, choose_reply: ChooseBestReply, token: str = Header()):
    user = get_user_or_raise_401(token)

    topic = topics_services.get_topic_with_replies(topic_id)

    if not topic:
        return NotFound(content=f"Topic with id:{topic_id} not found!")

    category = categories_service.get_category_by_id(topic.category_id)

    if not category:
        return NotFound(content=f"The category to which the topic belongs not found!")

    if category.is_locked:
        return Forbidden(f"You cannot choose a best reply to a topic because it's category with id:{category.category_id}"
                         f" is locked!")

    if category.is_private:
        if not categories_service.get_category_by_id(category.category_id, user.id):
            return Forbidden(f"User does not have access to category with id:{category.category_id} because it is private!")

        if not categories_service.check_write_access(user.id, category.category_id):
            return Forbidden(f"User with id:{user.id} does not have 'Write' access "
                             f"to category with id: {category.category_id}")

        if topic.user_id != user.id:
            return Forbidden(content="Only the topic author can choose the best reply!")

    if not topics_services.check_reply_belongs_to_topic(choose_reply.reply_id, topic_id):
        return BadRequest(content=f"Reply with id {choose_reply.reply_id} does not belong to the topic!")

    if topic.best_reply:
        return Forbidden(content=f"Topic with id:{topic_id} already has a best reply with id:{choose_reply.reply_id}!")

    topics_services.update_best_reply(topic_id, choose_reply.reply_id)

    return {"message": f"Reply with {choose_reply.reply_id} chosen successfully for best reply for topic with id:{topic_id}!"}


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
