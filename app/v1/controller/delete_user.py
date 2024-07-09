"""Application implementation - Ready controller."""

import logging

from fastapi import APIRouter
from ..views import UserDeletedResponse, ErrorResponse
from ..exceptions import HTTPException, UserNotFound, DynamoTableDoesNotExist
from ..model.dynamo_context_manager import DynamoConnection
from ..model.user import User
from botocore.exceptions import ClientError
from typing import Dict


router = APIRouter()
connection = DynamoConnection()
logger = logging.getLogger(__name__)


@router.delete(
    "/users/{user_id}",
    tags=["delete_user"],
    response_model=UserDeletedResponse,
    summary="Delete an user by userid.",
    status_code=200,
    responses={
        404: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_user(user_id: int) -> UserDeletedResponse:
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
    logger.info(f"Started delete /users")

    # Check if DynamoDB is up and running

    if not connection.is_alive:
        logger.error("Connesisone a DynamoDB non riuscita")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(
                code=502, message="Connessione a DynamoDB non riuscita"
            ).model_dump(exclude_none=True),
        )

    try:
        connection.delete_user(user_id)
        logger.info(f"Utente eliminato con id {user_id}")
    except DynamoTableDoesNotExist as e:
        logger.error(f"Tabella non trovata: {e}")
        raise HTTPException(
            status_code=404,
            content=ErrorResponse(
                code=404, message=f"Tabella non trovata: {e}"
            ).model_dump(exclude_none=True),
        )
    except UserNotFound as e:
        logger.error(f"Utente con ID {user_id} non trovato: {e}")
        raise HTTPException(
            status_code=404,
            content=ErrorResponse(
                code=404, message=f"Utente con ID {user_id} non trovato"
            ).model_dump(exclude_none=True),
        )
    except ClientError as e:
        logger.error(f"Errore durante l'eliminazione dell'utente: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500,
                message="Errore durante l'eliminazione dell'utente",
            ).model_dump(exclude_none=True),
        )
    return UserDeletedResponse(status="ok", user_id=str(user_id))
