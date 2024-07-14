from fastapi import APIRouter
from ..views import UserDeletedResponse, ErrorResponse
from ..exceptions import HTTPException, UserNotFound, DynamoTableDoesNotExist
from ..model.dynamo_context_manager import DynamoConnection
from botocore.exceptions import ClientError
from ..utils.custom_logger import LogSetupper


router = APIRouter()
connection = DynamoConnection()
logger = LogSetupper(__name__).setup()


@router.delete(
    "/users/{user_id}",
    tags=["Delete a user"],
    response_model=UserDeletedResponse,
    summary="Cancella un utente dato il suo user id.",
    status_code=200,
    responses={
        404: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def delete_user(user_id: str) -> UserDeletedResponse:
    """Funzione per eliminare un utente dato il suo user id

    Args:
        user_id (str): Id dell'utente da eliminare

    Raises:
        HTTPException: 502 se la connessione a Dynamo DB non è riuscita
        HTTPException: 502 se la tabella non esiste
        HTTPException: 404 se l'utente non è stato trovato
        HTTPException: 500 per un errore legato al client Dynamo db
        HTTPException: 500 per un errore generico

    Returns:
        UserDeletedResponse: Risposta alla chiamata
    """
    logger.debug(f"Comincio cancellazione del'utente {user_id}")

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
            status_code=502,
            content=ErrorResponse(code=502, message=f"Tabella non trovata").model_dump(
                exclude_none=True
            ),
        )
    except UserNotFound as e:
        logger.error(f"Utente non trovato: {e}")
        raise HTTPException(
            status_code=404,
            content=ErrorResponse(
                code=404, message=f"Utente con ID {user_id} non trovato"
            ).model_dump(exclude_none=True),
        )
    except ClientError as e:
        logger.error(f"Errore client DynamoDB: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500,
                message="Errore client DynamoDB",
            ).model_dump(exclude_none=True),
        )
    except Exception as e:
        logger.error(f"Errore sconosciuto: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500,
                message="Errore sconosciuto",
            ).model_dump(exclude_none=True),
        )
    return UserDeletedResponse(status="ok", user_id=user_id)
