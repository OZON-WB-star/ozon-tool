from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db import get_db
from app.models import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.common import MessageResponse, TokenResponse

router = APIRouter()


@router.post("/register", response_model=MessageResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> MessageResponse:
    exists = db.query(User).filter(or_(User.email == payload.email, User.phone == payload.phone)).first()
    if exists:
        raise HTTPException(status_code=409, detail="账号已存在，请直接登录")

    user = User(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="user",
        plan="free_analysis",
        status="active",
        verified=False,
        focus=payload.focus,
        next_step="绑定 Ozon 店铺",
        last_active="刚注册",
    )
    db.add(user)
    db.commit()
    return MessageResponse(message="注册成功，请登录")


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(or_(User.email == payload.account, User.phone == payload.account)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="账号或密码错误")
    if user.status != "active":
        raise HTTPException(status_code=403, detail="账号已停用")

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=token, user_id=str(user.id), role=user.role)
