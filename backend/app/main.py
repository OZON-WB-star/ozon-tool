from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, analysis, auth, products, selection, stores, tools, users
from app.core.config import settings


app = FastAPI(
    title="Dae ERP API",
    version="0.1.0",
    description="大鹅ERP 前后台统一 API 骨架",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(stores.router, prefix="/api/stores", tags=["stores"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(selection.router, prefix="/api/selection", tags=["selection"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
