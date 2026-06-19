# API 初版规划

## 用户认证

- `POST /api/auth/register` 用户注册
- `POST /api/auth/login` 用户登录
- `GET /api/users/me` 当前用户信息

## 用户前台接口

- `GET /api/stores` 我的店铺
- `POST /api/stores/connect` 绑定店铺
- `GET /api/products/online` 在线商品
- `GET /api/products/drafts` 商品草稿
- `GET /api/products/inventory` 库存预警
- `GET /api/analysis/overview` 数据总览
- `GET /api/analysis/products` 商品分析
- `GET /api/analysis/orders` 订单分析
- `GET /api/tools/rates` 定价测算记录
- `GET /api/tools/templates` 文案模板

## 管理后台接口

- `GET /api/admin/summary` 后台总览
- `GET /api/admin/users` 所有用户
- `GET /api/admin/stores` 所有店铺
- `GET /api/admin/services` 服务状态
- `GET /api/admin/jobs` 同步任务
- `PATCH /api/admin/users/{id}/plan` 修改套餐
- `PATCH /api/admin/users/{id}/status` 启用/停用用户

## Ozon 服务封装

建议单独封装：`services/ozon_client.py`、`services/product_sync.py`、`services/order_sync.py`、`services/inventory_sync.py`。不要在路由文件里直接写 Ozon API 逻辑。
