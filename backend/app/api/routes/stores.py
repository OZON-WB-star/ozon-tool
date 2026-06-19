from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import decrypt_secret, encrypt_secret, mask_secret
from app.db import get_db
from app.deps import get_current_user
from app.models import Store, User
from app.schemas.common import MessageResponse
from app.schemas.stores import StoreAuthStatus, StoreConfigRow, StoreConnectRequest, StoreRecord
from app.services.ozon_client import test_ozon_credentials

router = APIRouter()


def _store_query_for_user(db: Session, user: User):
    query = db.query(Store)
    if user.role == "user":
        query = query.filter(Store.user_id == user.id)
    return query


def _get_visible_store(store_id: int, db: Session, user: User) -> Store:
    store = _store_query_for_user(db, user).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="店铺不存在或无权访问")
    return store


def to_store_record(store: Store) -> StoreRecord:
    api_key = decrypt_secret(store.api_key_encrypted) if store.api_key_encrypted else None
    return StoreRecord(
        id=str(store.id),
        owner_id=str(store.user_id),
        name=store.name,
        site=store.site,
        auth=store.auth,
        status=store.status,
        health=store.health,
        synced_at=store.last_sync_at.strftime("%Y-%m-%d %H:%M") if store.last_sync_at else "暂未同步",
        note=store.note,
        client_id_masked=mask_secret(store.client_id),
        api_key_masked=mask_secret(api_key),
    )


@router.get("", response_model=list[StoreRecord])
def get_stores(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[StoreRecord]:
    return [to_store_record(item) for item in _store_query_for_user(db, current_user).order_by(Store.id.desc()).all()]


@router.get("/configs", response_model=list[StoreConfigRow])
def get_store_configs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[StoreConfigRow]:
    rows = []
    for store in _store_query_for_user(db, current_user).order_by(Store.id.desc()).all():
        rows.append(StoreConfigRow(
            id=f"cfg_{store.id}_api",
            store_id=str(store.id),
            config_item="Seller API",
            channel="Client ID / API Key",
            status="normal" if store.status == "normal" else "warn" if store.status == "pending" else "error",
            updated_at=store.last_sync_at.strftime("%Y-%m-%d %H:%M") if store.last_sync_at else "未完成测试",
            note=store.note,
        ))
    return rows


@router.post("/connect", response_model=MessageResponse)
def connect_store(payload: StoreConnectRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> MessageResponse:
    status = "pending"
    health = 0
    note = payload.note or "新接入店铺，等待测试授权"
    last_sync_at = None

    if payload.auth == "api" and payload.test_now:
        result = test_ozon_credentials(payload.client_id or "", payload.api_key or "")
        if result.ok:
            status = "normal"
            health = 90
            note = result.message
            last_sync_at = datetime.utcnow()
        else:
            status = "error"
            health = 20
            note = result.message

    store = Store(
        user_id=current_user.id,
        platform="ozon",
        name=payload.name,
        site=payload.site,
        auth=payload.auth,
        client_id=payload.client_id,
        api_key_encrypted=encrypt_secret(payload.api_key),
        status=status,
        health=health,
        note=note,
        last_sync_at=last_sync_at,
    )
    db.add(store)
    db.commit()
    if status == "normal":
        return MessageResponse(message=f"已创建店铺 {payload.name}，Ozon API 授权测试成功")
    if status == "error":
        return MessageResponse(message=f"已创建店铺 {payload.name}，但授权测试失败：{note}")
    return MessageResponse(message=f"已创建店铺 {payload.name}，下一步请测试 Ozon API 授权")


@router.post("/{store_id}/test", response_model=MessageResponse)
def test_store_auth(store_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> MessageResponse:
    store = _get_visible_store(store_id, db, current_user)
    api_key = decrypt_secret(store.api_key_encrypted)
    result = test_ozon_credentials(store.client_id or "", api_key or "")
    store.status = "normal" if result.ok else "error"
    store.health = 90 if result.ok else 20
    store.note = result.message
    store.last_sync_at = datetime.utcnow() if result.ok else store.last_sync_at
    db.commit()
    return MessageResponse(message=result.message)


@router.get("/{store_id}/auth-status", response_model=StoreAuthStatus)
def store_auth_status(store_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> StoreAuthStatus:
    store = _get_visible_store(store_id, db, current_user)
    api_key = decrypt_secret(store.api_key_encrypted)
    return StoreAuthStatus(
        id=str(store.id),
        name=store.name,
        status=store.status,
        health=store.health,
        note=store.note,
        client_id_masked=mask_secret(store.client_id),
        api_key_masked=mask_secret(api_key),
        last_sync_at=store.last_sync_at.strftime("%Y-%m-%d %H:%M") if store.last_sync_at else "暂未同步",
    )
