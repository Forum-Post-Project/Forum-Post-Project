from fastapi import APIRouter
from pydantic import BaseModel


topics_router = APIRouter(prefix="/topics")


@topics_router.get("/")
def get_all_topics():
    pass


@topics_router.get("/{id}")
def get_topic_by_id():
    pass


@topics_router.post("/")
def create_new_topic():
    pass


@topics_router.put("/{id}/lock")
def lock_topic():
    pass
