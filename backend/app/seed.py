from sqlalchemy.orm import Session

from app.core.security import encrypt_secret, hash_password
from app.models import Product, Store, SyncJob, User


def seed_database(db: Session) -> None:
    """Create first admin/user/demo data if database is empty."""
    if db.query(User).count() > 0:
        return

    admin = User(
        name="大鹅ERP管理员",
        email="admin@example.com",
        phone="18000000000",
        password_hash=hash_password("admin123456"),
        role="admin",
        plan="internal",
        status="active",
        verified=True,
        focus="后台管理与用户运营",
        next_step="管理用户与店铺",
        last_active="系统初始化",
    )
    user = User(
        name="测试用户",
        email="demo@example.com",
        phone="18000000001",
        password_hash=hash_password("user123456"),
        role="user",
        plan="free_analysis",
        status="active",
        verified=True,
        focus="Ozon 选品与上品",
        next_step="绑定 Ozon 店铺",
        last_active="系统初始化",
    )
    db.add_all([admin, user])
    db.flush()

    store = Store(
        user_id=user.id,
        platform="ozon",
        name="Ozon 测试店铺",
        site="Ozon RU",
        auth="api",
        status="normal",
        health=89,
        client_id="demo-client-id",
        api_key_encrypted=encrypt_secret("demo-api-key-not-real"),
        note="正式开发测试店铺（示例 Key 不可真实调用）",
    )
    db.add(store)
    db.flush()

    db.add_all([
        Product(store_id=store.id, sku="DE-PET-001", name="宠物去浮毛梳", stock=64, weekly_orders=38, status="normal", price=929),
        Product(store_id=store.id, sku="DE-BAG-017", name="便携化妆收纳包", stock=21, weekly_orders=14, status="low", price=1190),
        Product(store_id=store.id, sku="DE-LIGHT-009", name="露营挂灯", stock=9, weekly_orders=19, status="low", price=1699),
    ])
    db.add_all([
        SyncJob(store_id=store.id, name="商品同步", source="Ozon API", frequency="每 2 小时", job_type="products", status="pending"),
        SyncJob(store_id=store.id, name="订单同步", source="Ozon API", frequency="每 30 分钟", job_type="orders", status="pending"),
    ])
    db.commit()
