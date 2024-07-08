from routers.v1.router import root_api_router as v1_router
from utils.custom_logger import LogSetupper
from fastapi import FastAPI

logger = LogSetupper(__name__).setup()


app = FastAPI()

# Import dei router
app.include_router(v1_router)
