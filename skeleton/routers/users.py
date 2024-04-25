from fastapi import APIRouter
from pydantic import BaseModel
from services import users_service


users_router = APIRouter(prefix="/users")


@users_router.get("/login")
def user_login():
    pass


@users_router.get("/info")
def user_info():
    pass


@users_router.post("/register")
def register_user():
    pass
