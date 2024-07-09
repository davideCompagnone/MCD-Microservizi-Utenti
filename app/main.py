from v1.router import router_v1
from v1.exceptions import http_exception_handler, HTTPException
from fastapi import FastAPI

app = FastAPI()

# Import dei router
app.include_router(router_v1)
app.add_exception_handler(HTTPException, http_exception_handler)


# async def on_startup() -> None:
#     """Define FastAPI startup event handler.

#     Resources:
#         1. https://fastapi.tiangolo.com/advanced/events/#startup-event

#     """
#     log.debug("Execute FastAPI startup event handler.")
#     if settings.USE_REDIS:
#         await RedisClient.open_redis_client()

#     AiohttpClient.get_aiohttp_client()


# async def on_shutdown() -> None:
#     """Define FastAPI shutdown event handler.

#     Resources:
#         1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event

#     """
#     log.debug("Execute FastAPI shutdown event handler.")
#     # Gracefully close utilities.
#     if settings.USE_REDIS:
#         await RedisClient.close_redis_client()

#     await AiohttpClient.close_aiohttp_client()


# def get_application() -> FastAPI:
#     """Initialize FastAPI application.

#     Returns:
#        FastAPI: Application object instance.

#     """
#     log.debug("Initialize FastAPI application node.")
#     app = FastAPI(
#         title=settings.PROJECT_NAME,
#         debug=settings.DEBUG,
#         version=settings.VERSION,
#         docs_url=settings.DOCS_URL,
#         on_startup=[on_startup],
#         on_shutdown=[on_shutdown],
#     )
#     log.debug("Add application routes.")
#     app.include_router(root_api_router)
#     log.debug("Register global exception handler for custom HTTPException.")
#     app.add_exception_handler(HTTPException, http_exception_handler)

#     return app
