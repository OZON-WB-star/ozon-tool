from pydantic import BaseModel


class SelectionCategory(BaseModel):
    id: str
    name: str
    demand: str
    competition: str
    margin: str
    trend: str
    note: str


class SelectionKeyword(BaseModel):
    id: str
    keyword: str
    category: str
    heat: str
    difficulty: str
    action: str


class SelectionProduct(BaseModel):
    id: str
    name: str
    category: str
    score: int
    margin: str
    risk: str
    source: str
