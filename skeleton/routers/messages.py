from fastapi import APIRouter, Header
from common.responses import InternalServerError
from services import messages_service
from data.models import CreateMessage
from common.authentication import get_user_or_raise_401
from common.responses import Conflict, NotFound

messages_router = APIRouter(prefix="/messages/users")


@messages_router.post("/{receiver_id}")
def create_new_message(receiver_id: int, creating_message: CreateMessage, token: str = Header()):

    sender = get_user_or_raise_401(token)

    if sender.id == receiver_id:
        return Conflict(content="Sender and receiver cannot be the same user")

    new_message = messages_service.create_message(creating_message.text, sender.id, receiver_id)

    if not new_message:
        return InternalServerError(content="Failed to create message")

    return new_message


@messages_router.get("/{receiver_id}")
def get_conversation(receiver_id: int, token: str = Header()):

    sender = get_user_or_raise_401(token)

    if sender.id == receiver_id:
        return Conflict(content="Sender and receiver cannot be the same user")

    conversation = messages_service.get_conversation(sender.id, receiver_id)

    if not conversation:
        return NotFound(content=f"There is no conversation going on with user with id:{receiver_id}!")

    return conversation


@messages_router.get("/receivers")
def get_all_conversations(token: str = Header()):

    sender = get_user_or_raise_401(token)

    conversations = messages_service.get_all_conversations(sender.id)

    return conversations
