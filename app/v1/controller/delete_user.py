"""Application implementation - Ready controller."""

import logging

from fastapi import APIRouter
from ..views import UserDeletedResponse, ErrorResponse
from ..exceptions import HTTPException
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
async def insert_user(user_id: str) -> UserDeletedResponse:
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

    try:
        user_id = connection.insert_user(user)
        logger.info(f"Utente inserito con id {user_id}")

    except ClientError as e:
        logger.error(f"Errore durante l'inserimento dell'utente: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500,
                message="Errore durante l'inserimento dell'utente",
            ).model_dump(exclude_none=True),
        )
    except Exception as e:
        logger.error(f"Errore sconosciuto: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500,
                message="Internal server error",
            ).model_dump(exclude_none=True),
        )

    return UserInsertedResponse(status="ok", user_id=user_id)


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        response = table.get_item(Key={"user_id": user_id})
        if "Item" not in response:
            raise HTTPException(status_code=404, detail="User not found")

        table.delete_item(Key={"user_id": user_id})
        return {"detail": "User deleted successfully"}
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting user: {e.response['Error']['Message']}",
        )
