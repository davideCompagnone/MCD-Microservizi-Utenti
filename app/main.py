# from v1.router import router_v1
# from fastapi import FastAPI


# app = FastAPI()

# # Import dei router
# app.include_router(router_v1)
from v1.model.dynamo_context_manager import DynamoConnection
from v1.config.db_credentials import DynamoCredentials

credentials = DynamoCredentials()

connection = DynamoConnection(credentials=credentials)
