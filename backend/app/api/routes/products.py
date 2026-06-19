from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Product, Store, User
from app.schemas.products import InventoryAlertRow, ProductDraftRow, ProductOnlineRow, ProductOverview
from app.services.mock_db import list_items

router = APIRouter()


def _visible_store_ids(db: Session, user: User) -> list[int]:
    query = db.query(Store.id)
    if user.role == "user":
        query = query.filter(Store.user_id == user.id)
    return [row[0] for row in query.all()]


@router.get("/overview", response_model=ProductOverview)
def products_overview(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ProductOverview:
    store_ids = _visible_store_ids(db, current_user)
    products = db.query(Product).filter(Product.store_id.in_(store_ids)).all() if store_ids else []
    low_stock = len([p for p in products if p.stock <= 20])
    return ProductOverview(
        online=len(products),
        low_stock=low_stock,
        active=len([p for p in products if p.status == "normal"]),
        optimize=len([p for p in products if p.status != "normal"]),
        drafts=4,
        drafts_images=1,
        drafts_pricing=1,
        ready_to_publish=1,
        alerts=low_stock,
        in_transit=100,
        turnover_days=18,
        restock_plans=2,
    )


@router.get("/online", response_model=list[ProductOnlineRow])
def products_online(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ProductOnlineRow]:
    store_ids = _visible_store_ids(db, current_user)
    products = db.query(Product).filter(Product.store_id.in_(store_ids)).order_by(Product.id.desc()).all() if store_ids else []
    return [ProductOnlineRow(id=str(item.id), name=item.name, store_id=str(item.store_id), stock=item.stock, weekly_orders=item.weekly_orders, status=item.status, price=int(item.price or 0)) for item in products]


@router.get("/drafts", response_model=list[ProductDraftRow])
def products_drafts() -> list[ProductDraftRow]:
    return [ProductDraftRow(**item) for item in list_items("draft_products")]


@router.get("/inventory", response_model=list[InventoryAlertRow])
def products_inventory(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[InventoryAlertRow]:
    store_ids = _visible_store_ids(db, current_user)
    products = db.query(Product).filter(Product.store_id.in_(store_ids)).all() if store_ids else []
    rows = []
    for item in products:
        days = int(item.stock / max(item.weekly_orders / 7, 1)) if item.weekly_orders else 99
        rows.append(InventoryAlertRow(id=str(item.id), name=item.name, available=item.stock, sales_7d=item.weekly_orders, days=days, in_transit=0, restock=max(item.weekly_orders * 3 - item.stock, 0), status="urgent" if days <= 5 else "warn" if days <= 14 else "healthy"))
    return rows
