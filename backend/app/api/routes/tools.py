from fastapi import APIRouter

from app.schemas.tools import ToolRate, ToolTax, ToolTemplate
from app.services.mock_db import list_items


router = APIRouter()


@router.get("/rates", response_model=list[ToolRate])
def get_rates() -> list[ToolRate]:
    rows = []
    for item in list_items("tool_rates"):
        rows.append(
            ToolRate(
                id=item["id"],
                cny_cost=item["cny_cost"],
                rub_price=item["rub_price"],
                margin=item["margin"],
                note=item["note"],
            )
        )
    return rows


@router.get("/taxes", response_model=list[ToolTax])
def get_taxes() -> list[ToolTax]:
    return [ToolTax(**item) for item in list_items("tool_taxes")]


@router.get("/templates", response_model=list[ToolTemplate])
def get_templates() -> list[ToolTemplate]:
    return [ToolTemplate(**item) for item in list_items("tool_templates")]
