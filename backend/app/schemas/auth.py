from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str
    focus: str
    invite_code: str | None = None


class LoginRequest(BaseModel):
    account: str
    password: str
