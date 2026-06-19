from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.models import User
from app.schemas.ozon import OzonCredentialTestRequest, OzonCredentialTestResponse
from app.services.ozon_client import test_ozon_credentials

router = APIRouter()


@router.post("/test-credentials", response_model=OzonCredentialTestResponse)
def test_credentials(payload: OzonCredentialTestRequest, _: User = Depends(get_current_user)) -> OzonCredentialTestResponse:
    result = test_ozon_credentials(payload.client_id, payload.api_key)
    return OzonCredentialTestResponse(
        ok=result.ok,
        message=result.message,
        warehouse_count=result.warehouse_count,
        raw_status=result.raw_status,
    )
