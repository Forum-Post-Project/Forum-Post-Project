from fastapi import APIRouter
from pydantic import BaseModel


users_router = APIRouter(prefix="/users")


@users_router.get("/login")
def user_login():
    pass


@users_router.post("/registration")
def register_user():
    pass
