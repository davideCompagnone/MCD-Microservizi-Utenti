"""Application configuration - root APIRouter. """

from fastapi import APIRouter
from .controller import ready, insert_user, delete_user, get_users

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(ready.router, tags=["ready"])
router_v1.include_router(insert_user.router, tags=["insert_user"])
router_v1.include_router(delete_user.router, tags=["delete_user"])
router_v1.include_router(get_users.router, tags=["get_users"])