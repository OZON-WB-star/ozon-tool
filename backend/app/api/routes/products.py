from fastapi import APIRouter

from app.schemas.products import InventoryAlertRow, ProductDraftRow, ProductOnlineRow, ProductOverview
from app.services.mock_db import get_products_overview, list_items


router = APIRouter()


@router.get("/overview", response_model=ProductOverview)
def products_overview() -> ProductOverview:
    return ProductOverview(**get_products_overview())


@router.get("/online", response_model=list[ProductOnlineRow])
def products_online() -> list[ProductOnlineRow]:
    return [ProductOnlineRow(**item) for item in list_items("products")]


@router.get("/drafts", response_model=list[ProductDraftRow])
def products_drafts() -> list[ProductDraftRow]:
    return [ProductDraftRow(**item) for item in list_items("draft_products")]


@router.get("/inventory", response_model=list[InventoryAlertRow])
def products_inventory() -> list[InventoryAlertRow]:
    return [InventoryAlertRow(**item) for item in list_items("inventory_alerts")]
