# 数据库初版设计

正式开发建议使用 PostgreSQL。

## users 用户表

| 字段 | 说明 |
|---|---|
| id | 用户ID |
| name | 用户名称 |
| email | 邮箱 |
| phone | 手机号 |
| password_hash | 密码加密值 |
| role | user / admin_staff / super_admin |
| plan | 套餐 |
| status | active / disabled / pending |
| created_at | 创建时间 |
| updated_at | 更新时间 |

## stores 店铺表

| 字段 | 说明 |
|---|---|
| id | 店铺ID |
| user_id | 所属用户 |
| platform | 平台，例如 ozon |
| name | 店铺名称 |
| client_id | Ozon Client ID |
| api_key_encrypted | 加密后的 API Key |
| status | normal / error / pending |
| last_sync_at | 最近同步时间 |

## products 商品表

| 字段 | 说明 |
|---|---|
| id | 内部商品ID |
| store_id | 店铺ID |
| platform_product_id | 平台商品ID |
| sku | SKU |
| name | 商品名称 |
| price | 售价 |
| stock | 库存 |
| status | 状态 |
| updated_at | 更新时间 |

## orders 订单表

| 字段 | 说明 |
|---|---|
| id | 内部订单ID |
| store_id | 店铺ID |
| platform_order_id | 平台订单号 |
| order_status | 订单状态 |
| amount | 金额 |
| currency | 币种 |
| ordered_at | 下单时间 |

## sync_jobs 同步任务表

| 字段 | 说明 |
|---|---|
| id | 任务ID |
| store_id | 店铺ID |
| job_type | products / orders / stocks |
| status | pending / running / success / failed |
| started_at | 开始时间 |
| finished_at | 结束时间 |
| error_message | 错误信息 |
