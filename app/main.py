from v1.router import router_v1
from v1.exceptions import http_exception_handler, HTTPException
from fastapi import FastAPI

app = FastAPI()

# Import dei router
app.include_router(router_v1)
app.add_exception_handler(HTTPException, http_exception_handler)
