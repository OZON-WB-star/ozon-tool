from pydantic import BaseModel


class ProductOnlineRow(BaseModel):
    id: str
    name: str
    store_id: str
    stock: int
    weekly_orders: int
    status: str
    price: int


class ProductDraftRow(BaseModel):
    id: str
    name: str
    source: str
    status: str
    missing: str
    suggested_price: str
    next_step: str


class InventoryAlertRow(BaseModel):
    id: str
    name: str
    available: int
    sales_7d: int
    days: int
    in_transit: int
    restock: int
    status: str


class ProductOverview(BaseModel):
    online: int
    low_stock: int
    active: int
    optimize: int
    drafts: int
    drafts_images: int
    drafts_pricing: int
    ready_to_publish: int
    alerts: int
    in_transit: int
    turnover_days: int
    restock_plans: int
