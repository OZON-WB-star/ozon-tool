from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_admin, get_current_user
from app.models import Store, User
from app.schemas.users import CurrentUserOverview, UserSummary

router = APIRouter()


def role_label(role: str) -> str:
    return {"admin": "后台管理员", "staff": "内部员工", "user": "前台用户"}.get(role, role)


def plan_label(plan: str) -> str:
    return {"free_analysis": "免费分析", "internal": "内部账号", "pro": "专业版"}.get(plan, plan)


def to_summary(user: User, stores_bound: int = 0) -> UserSummary:
    return UserSummary(
        id=str(user.id),
        name=user.name,
        email=user.email,
        phone=user.phone or "",
        registered_at=user.created_at.strftime("%Y-%m-%d") if user.created_at else "",
        stores_bound=stores_bound,
        plan=user.plan,
        plan_label=plan_label(user.plan),
        last_active=user.last_active,
        status=user.status,
        role_label=role_label(user.role),
        focus=user.focus,
        verified=user.verified,
        next_step=user.next_step,
    )


@router.get("/me", response_model=CurrentUserOverview)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> CurrentUserOverview:
    stores_bound = db.query(Store).filter(Store.user_id == current_user.id).count()
    return CurrentUserOverview(
        name=current_user.name,
        email=current_user.email,
        plan_label=plan_label(current_user.plan),
        stores_bound=stores_bound,
        analysis_access="已开通",
        next_step=current_user.next_step,
        role_label=role_label(current_user.role),
        verified_label="已验证" if current_user.verified else "待验证",
        focus=current_user.focus,
    )


@router.get("", response_model=list[UserSummary])
def list_users(_: User = Depends(get_current_admin), db: Session = Depends(get_db)) -> list[UserSummary]:
    users = db.query(User).order_by(User.id.desc()).all()
    result = []
    for user in users:
        stores_bound = db.query(Store).filter(Store.user_id == user.id).count()
        result.append(to_summary(user, stores_bound))
    return result
