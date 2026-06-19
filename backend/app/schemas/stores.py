from pydantic import BaseModel, Field


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
    client_id_masked: str | None = None
    api_key_masked: str | None = None


class StoreConfigRow(BaseModel):
    id: str
    store_id: str
    config_item: str
    channel: str
    status: str
    updated_at: str
    note: str


class StoreConnectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    site: str = "Ozon RU"
    auth: str = "api"
    client_id: str | None = None
    api_key: str | None = None
    owner_email: str | None = None
    note: str | None = None
    test_now: bool = True


class StoreAuthStatus(BaseModel):
    id: str
    name: str
    status: str
    health: int
    note: str
    client_id_masked: str
    api_key_masked: str
    last_sync_at: str
