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


@categories_router.put("/{id}/read_access") #User ID given in Body. Can be reworked in URL if needed.
def change_read_access():
    pass


@categories_router.put("/{id}/write_access") #User ID given in Body. Can be reworked in URL if needed.
def change_write_access():
    pass


@categories_router.put("/{id}/access_revocation") #User ID given in Body. Can be reworked in URL if needed.
def revoke_access():
    pass


@categories_router.get("/{id}/privileges")
def show_privileges():
    pass


@categories_router.put("/{id}/lock")
def lock_category():
    pass
