from fastapi import APIRouter
from pydantic import BaseModel
from services import categories_service
from common.responses import NotFound

categories_router = APIRouter(prefix="/categories")


@categories_router.get("/")
def get_all_categories():
    categories = categories_service.get_all_categories()

    if not categories:
        return NotFound(content="No categories found!")

    return categories


@categories_router.get("/{category_id}")  # todo
def get_category_by_id(category_id: int):
    category = categories_service.get_category_by_id(category_id)

    if not category:
        return NotFound(content=f"Category with id:{category_id} does not exist!")

    return category


@categories_router.post("/")
def create_category(name: str):
    created_category = categories_service.create_category(name)

    return created_category


@categories_router.put("/{id}/private")
def change_private_status():
    pass


@categories_router.put("/{id}/read_access/{user_id}")
def change_read_access():
    pass


@categories_router.put("/{id}/write_access/{user_id}")
def change_write_access():
    pass


@categories_router.put("/{id}/remove_access/{user_id}")
def remove_access():
    pass


@categories_router.get("/{id}/privileges")
def show_privileges():
    pass


@categories_router.put("/{id}/lock")
def lock_category():
    pass
