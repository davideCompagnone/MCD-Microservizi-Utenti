from routers.v1.router import root_api_router as v1_router
from routers.v1.utils.custom_logger import LogSetupper
from fastapi import FastAPI

logger = LogSetupper(__name__).setup()


app = FastAPI()

# Import and register the routers
app.include_router(v1_router)
