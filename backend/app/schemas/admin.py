from pydantic import BaseModel


class AdminServiceRow(BaseModel):
    id: str
    name: str
    scope: str
    access: str
    status: str
    owner: str
    note: str


class AdminJobRow(BaseModel):
    id: str
    name: str
    source: str
    frequency: str
    status: str
    last_run: str
