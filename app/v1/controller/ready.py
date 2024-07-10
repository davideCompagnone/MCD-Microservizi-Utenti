from fastapi import APIRouter
from ..views import ReadyResponse, ErrorResponse
from ..exceptions import HTTPException
from ..model.dynamo_context_manager import DynamoConnection
from ..utils.custom_logger import LogSetupper


router = APIRouter()
logger = LogSetupper(__name__).setup()


@router.get(
    "/ready",
    tags=["Ready"],
    response_model=ReadyResponse,
    summary="Check dello stato dell'API e della connessione a dynamoDB.",
    status_code=200,
    responses={502: {"model": ErrorResponse}},
)
async def readiness_check() -> ReadyResponse:
    """Funzione per verificare che l'interfaccia API sia pronta. Esegue anche un check su DynamoDB.

    Raises:
        HTTPException: 502 se la connessione a Dynamo DB non è riuscita

    Returns:
        ReadyResponse: Risposta alla chiamata
    """
    logger.info("Started GET /ready")

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
        # raise HTTPException(
        #     status_code=502,
        #     content=ErrorResponse(
        #         code=502,
        #         message="Connessione a DynamoDB non riuscita",
        #         details=[{"test": "test"}],
        #     ).model_dump(exclude_none=True),
        # )
    return ReadyResponse(status="ok")
