from fastapi import APIRouter, HTTPException

from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.common import MessageResponse, TokenResponse
from app.services.mock_db import create_user, find_user_by_account


router = APIRouter()


@router.post("/register", response_model=MessageResponse)
def register(payload: RegisterRequest) -> MessageResponse:
    exists = find_user_by_account(payload.email) or find_user_by_account(payload.phone)
    if exists:
        raise HTTPException(status_code=409, detail="账号已存在")

    create_user(
        {
            "name": payload.name,
            "phone": payload.phone,
            "email": payload.email,
            "password": payload.password,
            "focus": payload.focus,
            "next_step": "绑定 Ozon 店铺",
        }
    )
    return MessageResponse(message=f"已创建演示账号 {payload.email}")


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    user = find_user_by_account(payload.account)
    if not user:
        raise HTTPException(status_code=404, detail="账号不存在")

    return TokenResponse(access_token="demo-token", user_id=user["id"])
