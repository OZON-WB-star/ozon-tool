from pydantic import BaseModel, EmailStr


class UserSummary(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    registered_at: str
    stores_bound: int
    plan: str
    plan_label: str
    last_active: str
    status: str
    role_label: str
    focus: str
    verified: bool
    next_step: str


class CurrentUserOverview(BaseModel):
    name: str
    email: EmailStr
    plan_label: str
    stores_bound: int
    analysis_access: str
    next_step: str
    role_label: str
    verified_label: str
    focus: str
