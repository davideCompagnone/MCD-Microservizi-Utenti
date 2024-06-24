from routers.v1.router import root_api_router as v1_router
from fastapi import FastAPI
from routers.v1.exceptions import http_exception_handler, HTTPException

# Crea un'istanza dell'applicazione FastAPI.
app = FastAPI()

# Import and register the routers
app.include_router(v1_router)
app.add_exception_handler(HTTPException, http_exception_handler)
