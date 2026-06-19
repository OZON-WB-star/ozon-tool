from fastapi import APIRouter

from app.schemas.common import MessageResponse
from app.schemas.stores import StoreConfigRow, StoreConnectRequest, StoreRecord
from app.services.mock_db import create_store, list_items


router = APIRouter()


@router.get("", response_model=list[StoreRecord])
def get_stores(owner_id: str | None = None) -> list[StoreRecord]:
    rows = list_items("stores")
    if owner_id:
        rows = [item for item in rows if item["owner_id"] == owner_id]
    return [StoreRecord(**item) for item in rows]


@router.get("/configs", response_model=list[StoreConfigRow])
def get_store_configs(store_id: str | None = None) -> list[StoreConfigRow]:
    rows = list_items("store_configs")
    if store_id:
        rows = [item for item in rows if item["store_id"] == store_id]
    return [StoreConfigRow(**item) for item in rows]


@router.post("/connect", response_model=MessageResponse)
def connect_store(payload: StoreConnectRequest, user_id: str | None = None) -> MessageResponse:
    create_store(
        {
            "owner_id": user_id or "user_wyb",
            "name": payload.name,
            "site": payload.site,
            "auth": payload.auth,
            "note": payload.note or "新接入店铺",
        }
    )
    return MessageResponse(message=f"已接收店铺接入请求 {payload.name}")
