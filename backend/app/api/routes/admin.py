from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_admin
from app.models import Store, SyncJob, User
from app.schemas.admin import AdminJobRow, AdminServiceRow
from app.schemas.stores import StoreRecord
from app.schemas.users import UserSummary
from app.services.mock_db import list_items
from app.api.routes.stores import to_store_record
from app.api.routes.users import to_summary

router = APIRouter()


@router.get("/summary")
def admin_summary(_: User = Depends(get_current_admin), db: Session = Depends(get_db)) -> dict:
    return {
        "registered_users": db.query(User).count(),
        "connected_stores": db.query(Store).count(),
        "active_sync_jobs": db.query(SyncJob).count(),
        "free_analysis_users": db.query(User).filter(User.plan == "free_analysis").count(),
    }


@router.get("/users", response_model=list[UserSummary])
def admin_users(_: User = Depends(get_current_admin), db: Session = Depends(get_db)) -> list[UserSummary]:
    return [to_summary(user, db.query(Store).filter(Store.user_id == user.id).count()) for user in db.query(User).order_by(User.id.desc()).all()]


@router.get("/stores", response_model=list[StoreRecord])
def admin_stores(_: User = Depends(get_current_admin), db: Session = Depends(get_db)) -> list[StoreRecord]:
    return [to_store_record(item) for item in db.query(Store).order_by(Store.id.desc()).all()]


@router.get("/services", response_model=list[AdminServiceRow])
def admin_services(_: User = Depends(get_current_admin)) -> list[AdminServiceRow]:
    return [AdminServiceRow(**item) for item in list_items("admin_services")]


@router.get("/jobs", response_model=list[AdminJobRow])
def admin_jobs(_: User = Depends(get_current_admin), db: Session = Depends(get_db)) -> list[AdminJobRow]:
    jobs = db.query(SyncJob).order_by(SyncJob.id.desc()).all()
    if not jobs:
        return [AdminJobRow(**item) for item in list_items("sync_jobs")]
    return [AdminJobRow(id=str(job.id), name=job.name, source=job.source, frequency=job.frequency, status=job.status, last_run=job.finished_at.strftime("%Y-%m-%d %H:%M") if job.finished_at else "未运行") for job in jobs]
