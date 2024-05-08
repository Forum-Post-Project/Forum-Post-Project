from fastapi import APIRouter, Header, HTTPException
from data.models import Reply
from services import replies_service

replies_router = APIRouter(prefix="/replies")


@replies_router.post("/{topic_id}", response_model=Reply)
def create_new_reply(topic_id: int, token: str = Header(), reply: Reply):
    if not token:
        raise HTTPException(
            status_code=401, detail="Authentication token is required")

    new_reply = replies_service.create_new_reply(topic_id, token, reply)
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
