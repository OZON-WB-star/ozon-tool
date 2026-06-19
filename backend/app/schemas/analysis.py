from pydantic import BaseModel


class AnalysisOverview(BaseModel):
    sales_today: int
    orders_today: int
    pending_orders: int
    avg_health: int
    free_pages: int


class AnalysisProductRow(BaseModel):
    id: str
    name: str
    impressions: int
    ctr: str
    conversion: str
    sales_7d: int
    risk: str
    advice: str


class AnalysisOrderRow(BaseModel):
    id: str
    dimension: str
    quantity: int
    ratio: str
    trend: str
    advice: str
