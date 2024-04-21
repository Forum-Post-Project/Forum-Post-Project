from fastapi import APIRouter
from pydantic import BaseModel


replies_router = APIRouter(prefix="/replies")


@replies_router.post("/{topic_id}")
def create_new_reply():
    pass


@replies_router.put("/{id}/vote")
def vote_on_reply():
    pass


@replies_router.put("/{id}/favourite")
def fav_a_reply():
    pass
