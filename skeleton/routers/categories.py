from fastapi import APIRouter, Header
from services import categories_service, users_service
from common.responses import NotFound, Forbidden, Conflict, BadRequest, Unauthorized
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
                       page_size: int = 10, token: str = Header()):

    user = get_user_or_raise_401(token)

    if not user:
        return Unauthorized(content="Login required for this action!")

    category = categories_service.get_category_by_id(category_id, search=search, sort=sort, page=page,
                                                     page_size=page_size)
    if not category:
        return NotFound(content=f"Category with id:{category_id} does not exist!")

    if user.is_admin:
        return category

    if category.is_private:

        if not categories_service.access_exists(user.id, category_id):
            return Forbidden(content="User does not have access to this category!")

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


@categories_router.put("/{category_id}/private")
def make_category_private(category_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    if not user.is_admin:
        return Forbidden(content="Only admins can change the private status of a category!")

    category = categories_service.get_category_by_id(category_id)

    if not category:
        return NotFound(content=f"Category with id:{category_id} does not exist!")

    if category.is_private:
        return Conflict(content="Category is already private!")

    categories_service.make_category_private(category_id)

    return {"message": f"Category with id:{category_id} is now private!"}


@categories_router.put("/{category_id}/non_private")
def make_category_non_private(category_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    if not user.is_admin:
        return Forbidden(content="Only admins can change the private status of a category!")

    category = categories_service.get_category_by_id(category_id)

    if not category:
        return NotFound(content=f"Category with id:{category_id} does not exist!")

    if not category.is_private:
        return Conflict(content="Category is already non-private!")

    categories_service.make_category_non_private(category_id)

    return {"message": f"Category with id:{category_id} is now non-private!"}


@categories_router.put("/{category_id}/read_access/{user_id}")
def give_user_category_read_access(category_id: int, user_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)
    if not user.is_admin:
        return Forbidden(content="Only admins can grant category read access!")

    category = categories_service.get_category_by_id(category_id)
    if not category:
        return NotFound(content=f"Category with id:{category_id} not found.")

    user_exists = users_service.get_by_id(user_id)
    if not user_exists:
        return NotFound(content=f"User with id:{user_id} not found.")

    access_level = categories_service.access_exists(user_id, category_id)
    if access_level:
        categories_service.revoke_user_category_access(user_id, category_id)

    categories_service.give_user_category_read_access(category_id, user_id, access_level="Read")

    return {"message": f"User with id:{user_id} granted read access to category with id:{category_id}."}


@categories_router.put("/{category_id}/write_access/{user_id}")
def give_user_category_write_access(category_id: int, user_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)
    if not user.is_admin:
        return Forbidden(content="Only admins can grant category read access!")

    category = categories_service.get_category_by_id(category_id)
    if not category:
        return NotFound(content=f"Category with id:{category_id} not found.")

    user_exists = users_service.get_by_id(user_id)
    if not user_exists:
        return NotFound(content=f"User with id:{user_id} not found.")

    access_level = categories_service.access_exists(user_id, category_id)
    if access_level:
        categories_service.revoke_user_category_access(user_id, category_id)

    categories_service.give_user_category_read_access(category_id, user_id, access_level="Write")

    return {"message": f"User with id:{user_id} granted write access to category with id:{category_id}."}


@categories_router.put("/{category_id}/remove_access/{user_id}")
def remove_access(category_id: int, user_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)
    if not user.is_admin:
        return Forbidden(content="Only admins can revoke user access.")

    categories_service.revoke_user_category_access(user_id, category_id)


@categories_router.get("/{category_id}/privileged_users")
def get_privileged_users(category_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    if not user.is_admin:
        return Forbidden(content="Only admins can view privileged users of a category!")

    privileged_users = categories_service.get_privileged_users(category_id)

    return privileged_users


@categories_router.put("/{category_id}/lock")
def lock_category(category_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    if not user.is_admin:
        return Forbidden(content="Only admins can lock categories!")

    category = categories_service.get_category_by_id(category_id)

    if not category:
        return NotFound(content=f"Category with id:{category_id} does not exist!")

    categories_service.lock_category(category_id)

    return {"message": f"Category with id:{category_id} locked successfully and can no longer accept new Topics!"}


