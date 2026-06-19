from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


# 正式开发时使用 PostgreSQL；当前代码仍保留 mock_db，方便逐步迁移。
engine = create_engine(getattr(settings, "database_url", "sqlite:///./dae_erp.db"), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
