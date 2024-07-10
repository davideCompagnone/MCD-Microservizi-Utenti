from fastapi import APIRouter
from ..views import GetUserResponse, ErrorResponse
from ..exceptions import HTTPException, UserNotFound, DynamoTableDoesNotExist
from ..model.dynamo_context_manager import DynamoConnection
from botocore.exceptions import ClientError
from ..utils.custom_logger import LogSetupper


router = APIRouter()
logger = LogSetupper(__name__).setup()

# Check if DynamoDB is up and running
connection = DynamoConnection()


@router.get(
    "/users/{user_id}",
    tags=["get_user"],
    response_model=GetUserResponse,
    summary="Ottieni i dettagli di un utente dall user_id.",
    status_code=200,
    responses={
        502: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_user(user_id: int) -> GetUserResponse:
    """Funzione per ottenere i dettagli di un utente dato il suo user id

    Args:
        user_id (int): user id dell'utente che si vuole ottenere

    Raises:
        HTTPException: 502 se la connessione a Dynamo DB non è riuscita
        HTTPException: 404 se l'utente non è stato trovato
        HTTPException: 500 per un errore legato al client Dynamo db
        HTTPException: 500 per un errore generico
        HTTPException: 502 se la tabella non esiste

    Returns:
        GetUserResponse: Risposta con i dettagli del singolo utente
    """
    logger.debug(f"Comincio la chiamata /users/{user_id}")

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
        logger.error(f"Utenta non trovato: {e}")
        raise HTTPException(
            status_code=404,
            content=ErrorResponse(code=404, message="User not found").model_dump(
                exclude_none=True
            ),
        )
    except DynamoTableDoesNotExist as e:
        logger.error(f"Tabella non trovata: {e}")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(code=502, message="Tabella non trovata").model_dump(
                exclude_none=True
            ),
        )
    except ClientError as e:
        logger.error(f"Errore client DynamoDB: {e}")
        raise HTTPException(
            status_code=500,
            content=ErrorResponse(
                code=500, message="Errore client DynamoDB"
            ).model_dump(exclude_none=True),
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
