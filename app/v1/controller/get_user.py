"""Application implementation - Ready controller."""

import logging

from fastapi import APIRouter
from ..views import ReadyResponse, ErrorResponse
from ..exceptions import HTTPException
from ..model.dynamo_context_manager import DynamoConnection
from ..config.db_credentials import DynamoCredentials


router = APIRouter()
logger = logging.getLogger(__name__)

# Check if DynamoDB is up and running
connection = DynamoConnection()


@router.get(
    "/ready",
    tags=["ready"],
    response_model=ReadyResponse,
    summary="Simple health check.",
    status_code=200,
    responses={502: {"model": ErrorResponse}},
)
async def readiness_check() -> ReadyResponse:
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
    logger.info("Started GET /ready")

    if not connection.is_alive:
        logger.error("Connesisone a DynamoDB non riuscita")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(
                code=502, message="Connessione a DynamoDB non riuscita"
            ).model_dump(exclude_none=True),
        )
        # raise HTTPException(
        #     status_code=502,
        #     content=ErrorResponse(
        #         code=502,
        #         message="Connessione a DynamoDB non riuscita",
        #         details=[{"test": "test"}],
        #     ).model_dump(exclude_none=True),
        # )
    return ReadyResponse(status="ok")
