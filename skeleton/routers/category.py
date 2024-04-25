from fastapi import APIRouter
from pydantic import BaseModel


categories_router = APIRouter(prefix="/category")


@categories_router.get("/")
def get_all_categories():
    pass


@categories_router.get("/{id}")
def get_category_by_id():
    pass


@categories_router.post("/")
def create_category():
    pass


@categories_router.put("/{id}/private")
def change_private_status():
    pass


@categories_router.put("/{id}/read_access/{user_id}")
def change_read_access():
    pass


@categories_router.put("/{id}/write_access/{user_id}")
def change_write_access():
    pass


@categories_router.put("/{id}/access_removal/{user_id}")
def revoke_access():
    pass


@categories_router.get("/{id}/privileges")
def show_privileges():
    pass


@categories_router.put("/{id}/lock")
def lock_category():
    pass
