from fastapi import APIRouter

from app.schemas.users import CurrentUserOverview, UserSummary
from app.services.mock_db import find_user_by_id, get_first, list_items


router = APIRouter()


@router.get("/me", response_model=CurrentUserOverview)
def get_current_user(user_id: str | None = None) -> CurrentUserOverview:
    user = find_user_by_id(user_id) or get_first("users")
    assert user is not None
    return CurrentUserOverview(
        name=user["name"],
        email=user["email"],
        plan_label=user.get("plan_label", "免费分析"),
        stores_bound=user["stores_bound"],
        analysis_access="已开通",
        next_step=user["next_step"],
        role_label=user["role_label"],
        verified_label="已验证" if user["verified"] else "待验证",
        focus=user["focus"],
    )


@router.get("", response_model=list[UserSummary])
def get_users() -> list[UserSummary]:
    return [UserSummary(**item) for item in list_items("users")]
