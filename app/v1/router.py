"""Application configuration - root APIRouter. """

from fastapi import APIRouter
from .controller import (
    ready,
    insert_user,
    delete_user,
    get_users,
    get_user,
    update_user,
)

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(ready.router, tags=["Ready"])
router_v1.include_router(insert_user.router, tags=["Insert new user"])
router_v1.include_router(delete_user.router, tags=["Delete a user"])
router_v1.include_router(get_users.router, tags=["Get all users"])
router_v1.include_router(get_user.router, tags=["Get user details"])
router_v1.include_router(update_user.router, tags=["Update user details"])
