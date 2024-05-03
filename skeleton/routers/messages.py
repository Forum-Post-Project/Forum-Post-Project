from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from services import messages_service
from data.models import Message
from common.authentication import get_user_or_raise_401

messages_router = APIRouter(prefix="/messages/users")


@messages_router.post("/{receiver_id}", response_model=Message)
def create_new_message(receiver_id: int, message: Message, token: str = Header(...)):

    sender_id = get_user_or_raise_401(token).id

    new_message = messages_service.create_message(
        message.text, sender_id, receiver_id)
    if not new_message:
        raise HTTPException(status_code=500, detail="Failed to create message")

    return new_message


@messages_router.get("/{receiver_id}", response_model=list[Message])
def get_conversation(receiver_id: int, token: str = Header(...)):

    sender_id = get_user_or_raise_401(token).id

    conversation = messages_service.get_conversation(sender_id, receiver_id)
    return conversation


@messages_router.get("/receivers", response_model=list[Message])
def get_all_conversations(token: str = Header(...)):

    sender_id = get_user_or_raise_401(token).id

    conversations = messages_service.get_all_conversations(sender_id)
    return conversations
