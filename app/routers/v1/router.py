"""Application configuration - root APIRouter. """

from fastapi import APIRouter
from .controller import ready, health

root_api_router = APIRouter(prefix="/v1")

root_api_router.include_router(ready.router, tags=["ready"])
root_api_router.include_router(health.router, tags=["health"])
