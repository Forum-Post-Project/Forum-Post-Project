from fastapi import APIRouter
from pydantic import BaseModel


replies_router = APIRouter(prefix="/replies")


@replies_router.post("/") #Topic ID in Body. May refactor ID in URL if needed.
def create_new_reply():
    pass


@replies_router.put("/{id}/vote") #Topic ID in Body. May refactor ID in URL if needed.
def vote_on_reply():
    pass


@replies_router.put("/{id}/favourite") #Topic ID in Body. May refactor ID in URL if needed.
def fav_a_reply():
    pass
