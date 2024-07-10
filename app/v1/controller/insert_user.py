from fastapi import APIRouter
from ..views import UserInsertedResponse, ErrorResponse
from ..exceptions import HTTPException, DynamoTableDoesNotExist
from ..model.dynamo_context_manager import DynamoConnection
from ..model.user import User
from botocore.exceptions import ClientError
from ..utils.custom_logger import LogSetupper


router = APIRouter()
connection = DynamoConnection()
logger = LogSetupper(__name__).setup()


@router.post(
    "/users",
    tags=["inser_user"],
    response_model=UserInsertedResponse,
    summary="Inserisci un nuovo utente in tabella",
    status_code=200,
    responses={
        502: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def insert_user(user: User) -> UserInsertedResponse:
    """Funzione per inserire un nuovo utente

    Args:
        user (User): Dettagli dell'utente che si vuole aggiungere

    Raises:
        HTTPException: 502 se la connessione a Dynamo DB non è riuscita
        HTTPException: 502 se la tabella non esiste
        HTTPException: 500 per un errore legato al client Dynamo db
        HTTPException: 500 per un errore generico

    Returns:
        UserInsertedResponse: Risposta alla chiamata post
    """
    logger.info("Comincio l'inserimento di un nuovo utente")

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
        user_id = connection.insert_user(user)
        logger.info(f"Utente inserito con id {user_id}")

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
    except Exception as e:
        logger.error(f"Errore sconosciuto: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500,
                message="Errore sconosciuto",
            ).model_dump(exclude_none=True),
        )

    return UserInsertedResponse(status="ok", user_id=str(user_id))
