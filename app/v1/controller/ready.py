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
)
async def readiness_check() -> ReadyResponse:
    """Funzione per verificare che l'interfaccia API sia pronta. Esegue anche un check su DynamoDB.

    Raises:
        HTTPException: 502 se la connessione a Dynamo DB non è riuscita

    Returns:
        ReadyResponse: Risposta alla chiamata
    """
    logger.info("Started GET /ready")
    return ReadyResponse(status="ok")
