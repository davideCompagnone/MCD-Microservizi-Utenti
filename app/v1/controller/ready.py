from fastapi import APIRouter
from ..views import ReadyResponse
from ..model.dynamo_context_manager import DynamoCredentials
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
        HTTPException: alza un eccezione 502 se la connessione a Dynamo DB non è riuscita

    Returns:
        ReadyResponse: Risposta alla chiamata
    """
    logger.info("Started GET /ready")
    env_config = DynamoCredentials()

    return ReadyResponse(status="ok", version=env_config.version)
