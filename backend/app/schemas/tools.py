from pydantic import BaseModel


class ToolRate(BaseModel):
    id: str
    cny_cost: str
    rub_price: str
    margin: str
    note: str


class ToolTax(BaseModel):
    id: str
    item: str
    value: str
    note: str


class ToolTemplate(BaseModel):
    id: str
    type: str
    category: str
    content: str
