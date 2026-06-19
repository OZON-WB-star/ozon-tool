from fastapi import APIRouter

from app.schemas.selection import SelectionCategory, SelectionKeyword, SelectionProduct
from app.services.mock_db import get_selection_summary, list_items


router = APIRouter()


@router.get("/overview")
def selection_overview() -> dict:
    return get_selection_summary()


@router.get("/categories", response_model=list[SelectionCategory])
def selection_categories() -> list[SelectionCategory]:
    return [SelectionCategory(**item) for item in list_items("selection_categories")]


@router.get("/keywords", response_model=list[SelectionKeyword])
def selection_keywords() -> list[SelectionKeyword]:
    return [SelectionKeyword(**item) for item in list_items("selection_keywords")]


@router.get("/products", response_model=list[SelectionProduct])
def selection_products() -> list[SelectionProduct]:
    return [SelectionProduct(**item) for item in list_items("selection_products")]
