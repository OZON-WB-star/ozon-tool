from pydantic import BaseModel, Field


class OzonCredentialTestRequest(BaseModel):
    client_id: str = Field(min_length=2)
    api_key: str = Field(min_length=8)


class OzonCredentialTestResponse(BaseModel):
    ok: bool
    message: str
    warehouse_count: int = 0
    raw_status: int | None = None
