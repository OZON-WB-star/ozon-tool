from collections.abc import Iterable
from uuid import uuid4


MOCK_DB = {
    "users": [
        {
            "id": "user_wyb",
            "name": "wang yubo",
            "email": "wyb461225@163.com",
            "phone": "18057445016",
            "registered_at": "2026-06-12",
            "stores_bound": 2,
            "plan": "free_analysis",
            "plan_label": "免费分析",
            "last_active": "今天 12:20",
            "status": "active",
            "role_label": "前台用户",
            "focus": "Ozon 选品与上品",
            "verified": True,
            "next_step": "完善店铺授权",
        },
        {
            "id": "user_qiha",
            "name": "QIHA 测试店",
            "email": "469475300@qq.com",
            "phone": "18000000002",
            "registered_at": "2026-06-10",
            "stores_bound": 1,
            "plan": "setup_pending",
            "plan_label": "待完善授权",
            "last_active": "今天 10:45",
            "status": "pending",
            "role_label": "待配置用户",
            "focus": "店铺授权接入",
            "verified": False,
            "next_step": "补全授权参数",
        },
    ],
    "stores": [
        {
            "id": "store_qiha",
            "owner_id": "user_wyb",
            "name": "QIHA-GEILI",
            "site": "Ozon RU",
            "auth": "api",
            "status": "normal",
            "health": 89,
            "synced_at": "今天 11:40",
            "note": "测试主店铺",
        },
        {
            "id": "store_kitchen",
            "owner_id": "user_wyb",
            "name": "Kitchen Nova",
            "site": "Ozon KZ",
            "auth": "cookie",
            "status": "error",
            "health": 48,
            "synced_at": "昨天 19:20",
            "note": "等待重新授权",
        },
        {
            "id": "store_qiha_lab",
            "owner_id": "user_qiha",
            "name": "QIHA Lab",
            "site": "Ozon RU",
            "auth": "api",
            "status": "normal",
            "health": 82,
            "synced_at": "今天 09:15",
            "note": "测试分析店铺",
        },
    ],
    "store_configs": [
        {
            "id": "cfg_qiha_api",
            "store_id": "store_qiha",
            "config_item": "Seller API",
            "channel": "Client ID / API Key",
            "status": "normal",
            "updated_at": "今天 11:42",
            "note": "主店铺 API 可用",
        },
        {
            "id": "cfg_qiha_cookie",
            "store_id": "store_qiha",
            "config_item": "浏览器 Cookie",
            "channel": "插件兼容链路",
            "status": "warn",
            "updated_at": "昨天 20:10",
            "note": "建议逐步迁移到 API",
        },
        {
            "id": "cfg_kitchen_cookie",
            "store_id": "store_kitchen",
            "config_item": "浏览器 Cookie",
            "channel": "旧授权链路",
            "status": "error",
            "updated_at": "昨天 19:20",
            "note": "等待重新授权",
        },
    ],
    "products": [
        {"id": "DE-PET-001", "name": "宠物去浮毛梳", "store_id": "store_qiha", "stock": 64, "weekly_orders": 38, "status": "normal", "price": 929},
        {"id": "DE-BEAUTY-017", "name": "便携化妆收纳包", "store_id": "store_qiha", "stock": 21, "weekly_orders": 14, "status": "low", "price": 1190},
        {"id": "DE-KITCHEN-022", "name": "厨房旋转调味架", "store_id": "store_kitchen", "stock": 108, "weekly_orders": 7, "status": "weak", "price": 1460},
        {"id": "DE-OUTDOOR-009", "name": "露营挂灯", "store_id": "store_qiha", "stock": 9, "weekly_orders": 19, "status": "low", "price": 1699},
    ],
    "draft_products": [
        {"id": "draft_pet_bath", "name": "宠物洗澡按摩刷", "source": "选品中心", "status": "image", "missing": "主图、白底图", "suggested_price": "₽1129", "next_step": "上传图片后发布"},
        {"id": "draft_bag", "name": "旅行收纳压缩包", "source": "采集导入", "status": "attribute", "missing": "材质、规格", "suggested_price": "₽899", "next_step": "补属性并校验类目"},
        {"id": "draft_rack", "name": "厨房油盐收纳架", "source": "人工创建", "status": "ready", "missing": "无", "suggested_price": "₽1369", "next_step": "可直接上架"},
        {"id": "draft_trash", "name": "车载折叠垃圾桶", "source": "选品中心", "status": "pricing", "missing": "价格方案", "suggested_price": "未生成", "next_step": "进入定价工具"},
    ],
    "inventory_alerts": [
        {"id": "inv_lantern", "name": "露营挂灯", "available": 9, "sales_7d": 19, "days": 3, "in_transit": 40, "restock": 120, "status": "urgent"},
        {"id": "inv_beauty", "name": "便携化妆收纳包", "available": 21, "sales_7d": 14, "days": 10, "in_transit": 0, "restock": 80, "status": "warn"},
        {"id": "inv_pet", "name": "宠物去浮毛梳", "available": 64, "sales_7d": 38, "days": 12, "in_transit": 100, "restock": 60, "status": "healthy"},
        {"id": "inv_kitchen", "name": "厨房旋转调味架", "available": 108, "sales_7d": 7, "days": 42, "in_transit": 0, "restock": 0, "status": "hold"},
    ],
    "selection_categories": [
        {
            "id": "cat_pet",
            "name": "宠物清洁",
            "demand": "高",
            "competition": "中",
            "margin": "34%",
            "trend": "上升",
            "note": "适合继续深挖白牌款",
        },
        {
            "id": "cat_home",
            "name": "家居收纳",
            "demand": "高",
            "competition": "高",
            "margin": "26%",
            "trend": "稳定",
            "note": "重点做差异化组合",
        },
        {
            "id": "cat_outdoor",
            "name": "户外露营",
            "demand": "中高",
            "competition": "中",
            "margin": "31%",
            "trend": "季节上升",
            "note": "适合配合活动推品",
        },
    ],
    "selection_keywords": [
        {
            "id": "kw_pet",
            "keyword": "pet grooming brush",
            "category": "宠物清洁",
            "heat": "8.9",
            "difficulty": "中",
            "action": "适合做主推词",
        },
        {
            "id": "kw_storage",
            "keyword": "storage organizer",
            "category": "家居收纳",
            "heat": "8.2",
            "difficulty": "高",
            "action": "适合做长尾组合",
        },
        {
            "id": "kw_lantern",
            "keyword": "camping lantern",
            "category": "户外露营",
            "heat": "7.8",
            "difficulty": "中",
            "action": "适合活动期推广",
        },
    ],
    "selection_products": [
        {
            "id": "pick_pet",
            "name": "宠物去浮毛梳",
            "category": "宠物清洁",
            "score": 92,
            "margin": "36%",
            "risk": "低",
            "source": "市场热词 + 现有动销",
        },
        {
            "id": "pick_storage",
            "name": "桌面分层收纳盒",
            "category": "家居收纳",
            "score": 85,
            "margin": "28%",
            "risk": "中",
            "source": "类目需求稳定",
        },
        {
            "id": "pick_lantern",
            "name": "露营磁吸挂灯",
            "category": "户外露营",
            "score": 88,
            "margin": "33%",
            "risk": "中",
            "source": "季节趋势上升",
        },
    ],
    "analysis_overview": {
        "sales_today": 98600,
        "orders_today": 146,
        "pending_orders": 23,
        "avg_health": 73,
        "free_pages": 3,
    },
    "analysis_products": [
        {
            "id": "ap_pet",
            "name": "宠物去浮毛梳",
            "impressions": 28400,
            "ctr": "6.7%",
            "conversion": "3.9%",
            "sales_7d": 38,
            "risk": "healthy",
            "advice": "可继续加推",
        },
        {
            "id": "ap_lantern",
            "name": "露营挂灯",
            "impressions": 17200,
            "ctr": "5.9%",
            "conversion": "4.8%",
            "sales_7d": 19,
            "risk": "warn",
            "advice": "先补货再扩量",
        },
        {
            "id": "ap_rack",
            "name": "厨房旋转调味架",
            "impressions": 23100,
            "ctr": "4.2%",
            "conversion": "1.3%",
            "sales_7d": 7,
            "risk": "low",
            "advice": "优化主图和价格",
        },
    ],
    "analysis_orders": [
        {
            "id": "ao_pending",
            "dimension": "待发货订单",
            "quantity": 23,
            "ratio": "15.7%",
            "trend": "下午集中",
            "advice": "按爆款优先出货",
        },
        {
            "id": "ao_shipping",
            "dimension": "运输中订单",
            "quantity": 81,
            "ratio": "55.5%",
            "trend": "稳定",
            "advice": "继续跟踪签收率",
        },
        {
            "id": "ao_cancel",
            "dimension": "取消订单",
            "quantity": 7,
            "ratio": "4.8%",
            "trend": "下降",
            "advice": "维持库存准确率",
        },
        {
            "id": "ao_exception",
            "dimension": "异常订单",
            "quantity": 4,
            "ratio": "2.7%",
            "trend": "需处理",
            "advice": "排查物流与库存同步",
        },
    ],
    "tool_rates": [
        {
            "id": "rate_1",
            "cny_cost": "￥18",
            "rub_price": "₽729",
            "margin": "25% - 30%",
            "note": "适合轻小件",
        },
        {
            "id": "rate_2",
            "cny_cost": "￥35",
            "rub_price": "₽1699",
            "margin": "22% - 26%",
            "note": "适合功能型商品",
        },
    ],
    "tool_taxes": [
        {"id": "tax_purchase", "item": "采购成本", "value": "￥18 - ￥48", "note": "商品本体成本"},
        {"id": "tax_fee", "item": "平台佣金", "value": "12% - 18%", "note": "按类目不同调整"},
        {"id": "tax_logistics", "item": "头程物流", "value": "￥4 - ￥12", "note": "随体积重量变化"},
    ],
    "tool_templates": [
        {
            "id": "tpl_title",
            "type": "标题模板",
            "category": "宠物清洁",
            "content": "核心功能 + 适用对象 + 材质卖点 + 场景词",
        },
        {
            "id": "tpl_detail",
            "type": "详情模板",
            "category": "户外露营",
            "content": "痛点开头 + 场景展示 + 参数说明 + 使用方法",
        },
    ],
    "admin_summary": {
        "registered_users": 2,
        "connected_stores": 3,
        "active_sync_jobs": 14,
        "free_analysis_users": 1,
    },
    "admin_services": [
        {
            "id": "svc_selection",
            "name": "选品中心 API",
            "scope": "市场 / 类目 / 关键词 / 候选商品",
            "access": "前台开放",
            "status": "normal",
            "owner": "选品服务",
            "note": "已供前台选品页调用",
        },
        {
            "id": "svc_analysis",
            "name": "分析中心 API",
            "scope": "店铺概览 / 商品分析 / 订单结构",
            "access": "前台免费",
            "status": "normal",
            "owner": "分析服务",
            "note": "当前免费，后续可分层收费",
        },
        {
            "id": "svc_tools",
            "name": "工具服务 API",
            "scope": "汇率 / 税费 / 文案模板",
            "access": "前台开放",
            "status": "warn",
            "owner": "工具服务",
            "note": "后续补交互式计算器",
        },
    ],
    "sync_jobs": [
        {
            "id": "job_selection",
            "name": "选品市场聚合",
            "source": "分析服务",
            "frequency": "每日",
            "status": "normal",
            "last_run": "今天 03:00",
        },
        {
            "id": "job_orders",
            "name": "订单状态同步",
            "source": "Ozon 授权店铺",
            "frequency": "10 分钟",
            "status": "running",
            "last_run": "今天 12:10",
        },
        {
            "id": "job_logistics",
            "name": "物流费用更新",
            "source": "工具服务",
            "frequency": "每日",
            "status": "warn",
            "last_run": "今天 08:00",
        },
    ],
}


def list_items(key: str) -> list[dict]:
    return list(MOCK_DB.get(key, []))


def get_first(key: str) -> dict | None:
    items: Iterable[dict] = MOCK_DB.get(key, [])
    return next(iter(items), None)


def find_user_by_account(account: str) -> dict | None:
    for user in MOCK_DB["users"]:
        if user["email"] == account or user["phone"] == account:
            return user
    return None


def find_user_by_id(user_id: str | None) -> dict | None:
    if not user_id:
        return None
    for user in MOCK_DB["users"]:
        if user["id"] == user_id:
            return user
    return None


def create_user(payload: dict) -> dict:
    user_id = payload.get("id") or f"user_{uuid4().hex[:8]}"
    user = {
        "id": user_id,
        "name": payload["name"],
        "email": payload["email"],
        "phone": payload["phone"],
        "registered_at": payload.get("registered_at", "2026-06-19"),
        "stores_bound": payload.get("stores_bound", 0),
        "plan": payload.get("plan", "free_analysis"),
        "plan_label": payload.get("plan_label", "免费分析"),
        "last_active": payload.get("last_active", "刚刚注册"),
        "status": payload.get("status", "active"),
        "role_label": payload.get("role_label", "前台用户"),
        "focus": payload.get("focus", "Ozon 选品"),
        "verified": payload.get("verified", False),
        "next_step": payload.get("next_step", "绑定 Ozon 店铺"),
        "password": payload.get("password", ""),
    }
    MOCK_DB["users"].insert(0, user)
    return user


def create_store(payload: dict) -> dict:
    store_id = payload.get("id") or f"store_{uuid4().hex[:8]}"
    store = {
        "id": store_id,
        "owner_id": payload.get("owner_id", "user_wyb"),
        "name": payload["name"],
        "site": payload["site"],
        "auth": payload["auth"],
        "status": payload.get("status", "normal"),
        "health": payload.get("health", 88),
        "synced_at": payload.get("synced_at", "刚刚接入"),
        "note": payload.get("note", "新接入店铺"),
    }
    MOCK_DB["stores"].insert(0, store)

    owner = find_user_by_id(store["owner_id"])
    if owner:
        owner["stores_bound"] = owner.get("stores_bound", 0) + 1
        owner["next_step"] = "查看店铺授权状态"

    return store


def get_admin_summary() -> dict:
    users = MOCK_DB["users"]
    stores = MOCK_DB["stores"]
    return {
        "registered_users": len(users),
        "connected_stores": len(stores),
        "active_sync_jobs": MOCK_DB["admin_summary"]["active_sync_jobs"],
        "free_analysis_users": len([item for item in users if item.get("plan") == "free_analysis"]),
    }


def get_selection_summary() -> dict:
    categories = MOCK_DB["selection_categories"]
    keywords = MOCK_DB["selection_keywords"]
    products = MOCK_DB["selection_products"]
    return {
        "hot_categories": len(categories),
        "tracked_keywords": len(keywords),
        "candidate_products": len(products),
        "opportunities": max(len(products) * 3, len(categories)),
    }


def get_analysis_overview() -> dict:
    overview = dict(MOCK_DB["analysis_overview"])
    overview["orders_today"] = sum(item["quantity"] for item in MOCK_DB["analysis_orders"] if item["id"] in {"ao_pending", "ao_shipping"})
    overview["pending_orders"] = next(
        (item["quantity"] for item in MOCK_DB["analysis_orders"] if item["id"] == "ao_pending"),
        overview["pending_orders"],
    )
    overview["avg_health"] = round(sum(item["health"] for item in MOCK_DB["stores"]) / len(MOCK_DB["stores"]))
    return overview


def get_products_overview() -> dict:
    products = MOCK_DB["products"]
    drafts = MOCK_DB["draft_products"]
    alerts = MOCK_DB["inventory_alerts"]
    return {
        "online": len(products),
        "low_stock": len([item for item in products if item["status"] == "low"]),
        "active": len([item for item in products if item["weekly_orders"] >= 15]),
        "optimize": len([item for item in products if item["status"] in {"weak", "low"}]),
        "drafts": len(drafts),
        "drafts_images": len([item for item in drafts if item["status"] == "image"]),
        "drafts_pricing": len([item for item in drafts if item["status"] == "pricing"]),
        "ready_to_publish": len([item for item in drafts if item["status"] == "ready"]),
        "alerts": len([item for item in alerts if item["status"] in {"urgent", "warn"}]),
        "in_transit": sum(1 for item in alerts if item["in_transit"] > 0),
        "turnover_days": round(sum(item["days"] for item in alerts) / len(alerts)),
        "restock_plans": len([item for item in alerts if item["restock"] > 0]),
    }
