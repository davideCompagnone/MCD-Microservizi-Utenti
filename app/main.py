from v1.router import router_v1
from v1.exceptions import http_exception_handler, HTTPException
from fastapi import FastAPI
import os

# Setup dell'applicazione in locale
if os.getenv("ENVIRONMENT") == "local":
    from v1.model.dynamo_context_manager import DynamoConnection
    from v1.utils.custom_logger import LogSetupper

    logger = LogSetupper(__name__).setup()
    connection = DynamoConnection()
    if connection.is_alive and not connection.table_exists:
        logger.warning(
            f"Tabella {connection.table_name} non trovata e ambiente di esecuzione local, la creo..."
        )
        try:
            connection.create_users_table()
            logger.info(f"Tabella {connection.table_name} creata con successo")
        except Exception as e:
            logger.error(f"Errore nella creazione della tabella: {e}")
            exit(1)

app = FastAPI()

# Import dei router
app.include_router(router_v1)
app.add_exception_handler(HTTPException, http_exception_handler)
