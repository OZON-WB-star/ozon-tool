from pydantic import BaseModel


class StoreRecord(BaseModel):
    id: str
    owner_id: str
    name: str
    site: str
    auth: str
    status: str
    health: int
    synced_at: str
    note: str


class StoreConfigRow(BaseModel):
    id: str
    store_id: str
    config_item: str
    channel: str
    status: str
    updated_at: str
    note: str


class StoreConnectRequest(BaseModel):
    name: str
    site: str
    auth: str
    client_id: str | None = None
    api_key: str | None = None
    owner_email: str
    note: str | None = None
