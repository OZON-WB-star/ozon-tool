from fastapi import APIRouter

from app.schemas.analysis import AnalysisOrderRow, AnalysisOverview, AnalysisProductRow
from app.services.mock_db import get_analysis_overview, list_items


router = APIRouter()


@router.get("/overview", response_model=AnalysisOverview)
def analysis_overview() -> AnalysisOverview:
    return AnalysisOverview(**get_analysis_overview())


@router.get("/products", response_model=list[AnalysisProductRow])
def analysis_products() -> list[AnalysisProductRow]:
    return [AnalysisProductRow(**item) for item in list_items("analysis_products")]


@router.get("/orders", response_model=list[AnalysisOrderRow])
def analysis_orders() -> list[AnalysisOrderRow]:
    return [AnalysisOrderRow(**item) for item in list_items("analysis_orders")]
