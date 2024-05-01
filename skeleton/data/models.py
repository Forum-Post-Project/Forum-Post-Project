from pydantic import BaseModel, constr
from datetime import date


class Category(BaseModel):
    id: int
    name: str = constr(pattern="^\w{1,50}$")


class Topic(BaseModel):
    id: int
    title: str = constr(pattern="^\w{1,100}$")
    category_id: int
    user_id: int
    creation_date: date

    @classmethod
    def from_query_result(cls, topic_id, title, category_id, user_id, creation_date):
        return cls(
            id=topic_id,
            title=title,
            category_id=category_id,
            user_id=user_id,
            creation_date=creation_date
        )


class Reply(BaseModel):
    id: int
    text: str
    topic_id: int
    user_id: int
    creation_date: date

    @classmethod
    def from_query_result(cls, reply_id, text, topic_id, user_id, creation_date):
        return cls(
            id=reply_id,
            text=text,
            topic_id=topic_id,
            user_id=user_id,
            creation_date=creation_date
        )


class Vote(BaseModel):
    id: int
    reply_id: int
    user_id: int
    vote_type: bool | None


class Message(BaseModel):
    id: int
    text: str
    sender_id: int
    receiver_id: int
    creation_date: date

    @classmethod
    def from_query_result(cls, message_id, text, sender_id, receiver_id, creation_date):
        return cls(
            id=message_id,
            text=text,
            sender_id=sender_id,
            receiver_id=receiver_id,
            creation_date=creation_date
        )


class User(BaseModel):
    id: int
    username: str = constr(pattern="^\w{5,20}$")
    password: str = constr(pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    name: str = constr(pattern="^\w{2,25}$")
    is_admin: bool = False

    @classmethod
    def from_query_result(cls, user_id, username, password, email, name, is_admin=False):
        return cls(
            id=user_id,
            username=username,
            password=password,
            email=email,
            name=name,
            is_admin=is_admin
        )


class LoginInformation(BaseModel):
    username: str
    password: str
    email: str = None or None
    name: str = None or None
