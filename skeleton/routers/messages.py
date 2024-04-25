from fastapi import APIRouter
from pydantic import BaseModel


messages_router = APIRouter(prefix="/messages/users")


@messages_router.post("/{sender_id}/{receiver_id}") #Receiver ID in Body. May refactor ID in URL if needed.
def create_new_message():
    pass


@messages_router.get("/{sender_id}/{receiver_id}")
def get_conversation():
    pass


@messages_router.get("/{sender_id}/receivers")
def get_all_conversations():
    pass
