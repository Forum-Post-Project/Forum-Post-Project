from fastapi import APIRouter
from pydantic import BaseModel
from data.models import Message
from services.messages_service import create_message, get_conversation, get_all_conversations

messages_router = APIRouter(prefix="/messages/users")


@messages_router.post("/{sender_id}/{receiver_id}", response_model=Message)
def create_new_message(sender_id: int, receiver_id: int, message: Message):

    new_message = create_message(message.text, sender_id, receiver_id)
    return new_message


@messages_router.get("/{sender_id}/{receiver_id}", response_model=list[Message])
def get_conversation(sender_id: int, receiver_id: int):

    conversation = get_conversation(sender_id, receiver_id)
    return conversation


@messages_router.get("/{sender_id}/receivers", response_model=list[Message])
def get_all_conversations(sender_id: int):

    conversations = get_all_conversations(sender_id)
    return conversations
