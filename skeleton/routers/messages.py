from fastapi import APIRouter
from pydantic import BaseModel


messages_router = APIRouter(prefix="/messages")


@messages_router.post("/") #Receiver ID in Body. May refactor ID in URL if needed.
def create_new_message():
    pass


@messages_router.get("/receiver/{id}")
def get_conversation():
    pass


@messages_router.get("/receivers")
def get_all_conversations():
    pass
