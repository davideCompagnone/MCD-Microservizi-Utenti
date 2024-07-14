from fastapi import APIRouter
from ..views import UserUpdatedResponse, ErrorResponse
from ..exceptions import HTTPException, UserNotFound, DynamoTableDoesNotExist
from ..model.dynamo_context_manager import DynamoConnection
from ..model.user import User
from ..utils.custom_logger import LogSetupper
from botocore.exceptions import ClientError


router = APIRouter()
connection = DynamoConnection()
logger = LogSetupper(__name__).setup()


@router.put(
    "/users/{user_id}",
    tags=["Update user details"],
    response_model=UserUpdatedResponse,
    summary="Aggiorna un utente dato un user_id.",
    status_code=200,
    responses={
        404: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_user(user_id: str, user: User) -> UserUpdatedResponse:
    """Funzione per aggiornare un utente

    Args:
        user_id (str): user id dell'utente coinvolto dall'aggiornamento
        user (User): Dettagli dell'utente da aggiornare

    Raises:
        HTTPException: 502 se la connessione a Dynamo DB non è riuscita \f
        HTTPException: 404 se l'utente non è stato trovato \f
        HTTPException: 500 per un errore legato al client Dynamo db \f
        HTTPException: 500 per un errore generico \f
        HTTPException: 502 se la tabella non esiste

    Returns:
        UserUpdatedResponse: Risposta con id dell'utente aggiornato
    """
    logger.info(f"Cominziato l'update PUT /users/{user_id}")

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
        user_id = connection.update_user(user_id=user_id, user_data=user)
        logger.info(f"Utente {user_id} aggiornato")

    except ClientError as e:
        logger.error(f"Errore client DynamoDB: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500, message="Errore client DynamoDB"
            ).model_dump(exclude_none=True),
        )
    except DynamoTableDoesNotExist as e:
        logger.error(f"Tabella non trovata: {e}")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(code=502, message="Tabella non trovata").model_dump(
                exclude_none=True
            ),
        )
    except UserNotFound as e:
        logger.error(f"Utente non trovato: {e}")
        raise HTTPException(
            status_code=404,
            content=ErrorResponse(code=404, message="Utente non trovato").model_dump(
                exclude_none=True
            ),
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

    return UserUpdatedResponse(status="ok", user_id=str(user_id))
