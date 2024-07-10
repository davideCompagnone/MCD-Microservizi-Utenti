"""Application implementation - Ready controller."""

import logging

from fastapi import APIRouter
from ..views import GetAllUsersResponse, ErrorResponse
from ..exceptions import HTTPException, EmptyTable, DynamoTableDoesNotExist
from ..model.dynamo_context_manager import DynamoConnection
from typing import List


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/users",
    tags=["get_all_user"],
    response_model=GetAllUsersResponse,
    summary="Get all users",
    status_code=200,
    responses={502: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def get_all_user() -> GetAllUsersResponse:
    """Run basic application health check.

    If the application is up and running then this endpoint will return simple
    response with status ok. Moreover, if it has Redis enabled then connection
    to it will be tested. If Redis ping fails, then this endpoint will return
    502 HTTP error.
    \f

    Returns:
        response (ReadyResponse): ReadyResponse model object instance.

    Raises:
        HTTPException: If applications has enabled Redis and can not connect
            to it. NOTE! This is the custom exception, not to be mistaken with
            FastAPI.HTTPException class.

    """
    logger.info("Started GET /users")

    # Check if DynamoDB is up and running
    connection = DynamoConnection()

    if not connection.is_alive:
        logger.error("Connesisone a DynamoDB non riuscita")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(
                code=502, message="Connessione a DynamoDB non riuscita"
            ).model_dump(exclude_none=True),
        )

    try:
        users: List = connection.get_users()
        logger.info(f"Fetch di tutti gli utenti eseguito.")

    except DynamoTableDoesNotExist:
        logger.error("Tabella non esistente")
        raise HTTPException(
            status_code=404,
            content=ErrorResponse(code=404, message="Tabella non esistente").model_dump(
                exclude_none=True
            ),
        )
    except Exception as e:
        logger.error(f"Errore sconosciuto: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500, message=f"Errore sconosciuto: {e}"
            ).model_dump(exclude_none=True),
        )
    return GetAllUsersResponse(status="ok", users=users)
