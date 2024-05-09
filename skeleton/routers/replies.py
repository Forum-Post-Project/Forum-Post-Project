from fastapi import APIRouter, Header, HTTPException
from data.models import Reply, CreateReply
from services import replies_service
from common.authentication import get_user_or_raise_401
from services import topics_services, categories_service
from common.responses import NotFound, Forbidden, Conflict

replies_router = APIRouter(prefix="/replies")


@replies_router.post("/{topic_id}")
def create_reply(topic_id: int, creating_reply: CreateReply, token: str = Header()):

    user = get_user_or_raise_401(token)

    topic = topics_services.get_topic_with_replies(topic_id)

    if not topic:
        return NotFound(content=f"Topic with id:{topic_id} cannot be found!")

    category = categories_service.get_category_by_id(topic.category_id)

    if not category:
        return NotFound(content=f"Category with id:{topic.category_id} cannot be found!")

    if category.is_private:
        if not categories_service.access_exists(user.id, category.category_id):
            return Forbidden(content=f"Topic with id:{topic_id} belongs to a private category! User does not have access to it!")

        if topic.is_locked:
            return Forbidden(content=f"Topic with id{topic_id} is locked and cannot accept replies!")

    new_reply = replies_service.create_reply(creating_reply.text, topic_id, user.id)

    return new_reply


@replies_router.post("/{reply_id}/upvote")
def upvote_reply(reply_id: int, token: str = Header()):

    user = get_user_or_raise_401(token)

    reply = replies_service.get_reply_by_id(reply_id)

    if not reply:
        return NotFound(content=f"Reply with id:{reply_id} not found!")

    topic = topics_services.get_topic_with_replies(reply.topic_id)

    if not topic:
        return NotFound(content=f"Topic with id:{reply.topic_id} not found!")

    if topic.is_locked:
        return Forbidden(content=f"Topic with id{reply.topic_id} is locked! User cannot upvote replies from it!")

    category = categories_service.get_category_by_id(topic.category_id)

    if not category:
        return NotFound(content=f"Category with id:{topic.category_id} not found!")

    if category.is_locked:
        return Forbidden(content=f"Category with id:{topic.category_id} is locked! User cannot access it!")

    if category.is_private:
        if not categories_service.access_exists(user.id, category.category_id):
            return Forbidden(content=f"User has no access to private category with id:{category.category_id}!")

    if replies_service.has_upvoted(reply_id, user.id):
        return Conflict(content="User has already upvoted this reply!")

    replies_service.upvote_reply(reply_id, user.id)
    return {"message": f"Reply with id:{reply_id} upvoted successfully!"}


@replies_router.post("/{reply_id}/downvote")
def downvote_reply(reply_id: int, token: str = Header()):

    user = get_user_or_raise_401(token)

    reply = replies_service.get_reply_by_id(reply_id)

    if not reply:
        return NotFound(content=f"Reply with id:{reply_id} not found!")

    topic = topics_services.get_topic_with_replies(reply.topic_id)

    if not topic:
        return NotFound(content=f"Topic with id:{reply.topic_id} not found!")

    if topic.is_locked:
        return Forbidden(content=f"Topic with id{reply.topic_id} is locked! User cannot downvote replies from it!")

    category = categories_service.get_category_by_id(topic.category_id)

    if not category:
        return NotFound(content=f"Category with id:{topic.category_id} not found!")

    if category.is_locked:
        return Forbidden(content=f"Category with id:{topic.category_id} is locked! User cannot access it!")

    if category.is_private:
        if not categories_service.access_exists(user.id, category.category_id):
            return Forbidden(content=f"User has no access to private category with id:{category.category_id}!")

    if replies_service.has_downvoted(reply_id, user.id):
        return Conflict(content="User has already downvoted this reply!")

    replies_service.downvote_reply(reply_id, user.id)
    return {"message": f"Reply with id:{reply_id} downvoted successfully!"}