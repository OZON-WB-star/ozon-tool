from fastapi import APIRouter

from app.schemas.admin import AdminJobRow, AdminServiceRow
from app.schemas.stores import StoreRecord
from app.schemas.users import UserSummary
from app.services.mock_db import get_admin_summary, list_items


router = APIRouter()


@router.get("/summary")
def admin_summary() -> dict:
    return get_admin_summary()


@router.get("/users", response_model=list[UserSummary])
def admin_users() -> list[UserSummary]:
    return [UserSummary(**item) for item in list_items("users")]


@router.get("/stores", response_model=list[StoreRecord])
def admin_stores() -> list[StoreRecord]:
    return [StoreRecord(**item) for item in list_items("stores")]


@router.get("/services", response_model=list[AdminServiceRow])
def admin_services() -> list[AdminServiceRow]:
    return [AdminServiceRow(**item) for item in list_items("admin_services")]


@router.get("/jobs", response_model=list[AdminJobRow])
def admin_jobs() -> list[AdminJobRow]:
    return [AdminJobRow(**item) for item in list_items("sync_jobs")]
