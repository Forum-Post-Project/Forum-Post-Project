from fastapi import APIRouter, Header
from pydantic import BaseModel
from services import categories_service
from common.responses import NotFound, BadRequest, Forbidden
from data.models import Category, CreateCategory
from common.authentication import get_user_or_raise_401

categories_router = APIRouter(prefix="/categories")


@categories_router.get("/")
def get_all_categories():
    categories = categories_service.get_all_categories()

    if not categories:
        return NotFound(content="No categories found!")

    return categories


@categories_router.get("/{category_id}")
def get_category_by_id(category_id: int,
                       search: str = None,
                       sort: str = None,
                       page: int = None,
                       page_size: int = 10):

    category = categories_service.get_category_by_id(category_id, search=search, sort=sort, page=page,
                                                     page_size=page_size)

    if not category:
        return NotFound(content=f"Category with id:{category_id} does not exist!")

    return category


@categories_router.post("/")
def create_category(creating_category: CreateCategory, token: str = Header()):
    user = get_user_or_raise_401(token)

    if not user.is_admin:
        return Forbidden("Only admins can create categories!")
    if not creating_category.name:
        return BadRequest(content="Category name is required in order to create a category!")

    created_category = categories_service.create_category(creating_category.name)

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


@categories_router.put("/{category_id}/lock")
def lock_category(category_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    if not user.is_admin:
        return Forbidden(content="Only admins can lock categories!")

    category = categories_service.get_category_by_id(category_id)

    if not category:
        return NotFound(content=f"Category with id:{category_id} does not exist!")

    categories_service.lock_category(category_id)

    return f"Category with id:{category_id} locked successfully and can no longer accept new Topics!"
