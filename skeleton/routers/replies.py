from fastapi import APIRouter, Header, HTTPException
from data.models import Reply, CreateReply
from services import replies_service
from common.authentication import get_user_or_raise_401
from services import topics_services, categories_service
from common.responses import NotFound, Forbidden

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


@replies_router.put("/{id}/vote")
def vote_on_reply(id: int, vote_type: bool, token: str = Header()):
    if not token:
        raise HTTPException(
            status_code=401, detail="Authentication token is required")

    success = replies_service.vote_on_reply(id, token, vote_type)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to vote on reply")
    return {"message": "Vote recorded successfully"}


@replies_router.put("/{id}/favourite")
def fav_a_reply(id: int, token: str = Header()):
    if not token:
        raise HTTPException(
            status_code=401, detail="Authentication token is required")

    success = replies_service.fav_a_reply(id, token)
    if not success:
        raise HTTPException(
            status_code=400, detail="Failed to mark reply as favorite")
    return {"message": "Reply marked as favorite successfully"}
