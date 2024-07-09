"""Application implementation - Ready controller."""

import logging

from fastapi import APIRouter
from ..views import GetUserResponse, ErrorResponse
from ..exceptions import HTTPException, UserNotFound, DynamoTableDoesNotExist
from ..model.dynamo_context_manager import DynamoConnection


router = APIRouter()
logger = logging.getLogger(__name__)

# Check if DynamoDB is up and running
connection = DynamoConnection()


@router.get(
    "/users/{user_id}",
    tags=["get_user"],
    response_model=GetUserResponse,
    summary="Get user by userid.",
    status_code=200,
    responses={
        502: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_user(user_id: int) -> GetUserResponse:
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
    logger.info("Started GET /users/{user_id}")

    if not connection.is_alive:
        logger.error("Connesisone a DynamoDB non riuscita")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(
                code=502, message="Connessione a DynamoDB non riuscita"
            ).model_dump(exclude_none=True),
        )
    try:
        user = connection.get_user(user_id=user_id)
        logger.info(f"Utente {user_id} trovato")
    except UserNotFound as e:
        logger.error(f"Utenta {user_id} non trovato")
        raise HTTPException(
            status_code=404,
            content=ErrorResponse(code=404, message="User not found").model_dump(
                exclude_none=True
            ),
        )
    except DynamoTableDoesNotExist as e:
        logger.error("Tabella non trovata")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(code=502, message="Tabella non trovata").model_dump(
                exclude_none=True
            ),
        )
    except Exception as e:
        logger.error(f"Errore sconosciuto: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(code=500, message="Errore sconosciuto").model_dump(
                exclude_none=True
            ),
        )

    return GetUserResponse(status="ok", detail=user)
