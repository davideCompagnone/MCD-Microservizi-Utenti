from fastapi import APIRouter
from ..views import GetAllUsersResponse, ErrorResponse
from ..exceptions import HTTPException, DynamoTableDoesNotExist
from ..model.dynamo_context_manager import DynamoConnection
from typing import List
from ..utils.custom_logger import LogSetupper
from botocore.exceptions import ClientError

router = APIRouter()
logger = LogSetupper(__name__).setup()


@router.get(
    "/users",
    tags=["get_all_user"],
    response_model=GetAllUsersResponse,
    summary="Esegue il retrieve di tutti gli utenti.",
    status_code=200,
    responses={502: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def get_all_user() -> GetAllUsersResponse:
    """Esegue il retrieve di tutti gli utenti

    Raises:
        HTTPException: 502 se la connessione a Dynamo DB non è riuscita
        HTTPException: 502 se la tabella non esiste
        HTTPException: 500 per un errore legato al client Dynamo db

    Returns:
        GetAllUsersResponse: Elenco di tutti gli utenti presenti nella tabella
    """

    logger.info("Comincio retrieve di tutti lgi utenti")

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
            content=ErrorResponse(
                code=500, message=f"Errore sconosciuto: {e}"
            ).model_dump(exclude_none=True),
        )
    return GetAllUsersResponse(status="ok", users=users)
