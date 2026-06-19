# V3：Ozon 店铺授权接入

## 本阶段完成目标

V3 的目标是把系统从“账号 + 权限 + 数据库”推进到“可以接入真实 Ozon 店铺”。

已完成：

1. 用户前台填写 Ozon 店铺名称、Client ID、API Key。
2. 后端保存店铺授权信息。
3. API Key 使用开发版可逆加密保存，不再明文直接写入数据库。
4. 提交时可以立即测试 Ozon Seller API。
5. 测试接口使用 `POST https://api-seller.ozon.ru/v1/warehouse/list`。
6. 普通用户只能看到自己绑定的店铺。
7. 管理员后台可以看到所有用户绑定的店铺。
8. 店铺状态分为：
   - `normal`：授权正常
   - `pending`：已保存，未测试
   - `error`：授权失败或 API Key 权限不足

## Ozon API Key 获取位置

进入 Ozon 卖家后台：

```text
设置 / Seller API / API Keys
```

复制：

```text
Client ID
API Key
```

API Key 只在创建时显示一次，必须及时保存。

## 新增接口

### 1. 测试 Ozon API Key

```http
POST /api/ozon/test-credentials
Authorization: Bearer <token>
Content-Type: application/json
```

请求：

```json
{
  "client_id": "你的 Client ID",
  "api_key": "你的 API Key"
}
```

返回：

```json
{
  "ok": true,
  "message": "Ozon API 授权成功，检测到 1 个仓库",
  "warehouse_count": 1,
  "raw_status": 200
}
```

### 2. 创建店铺并测试授权

```http
POST /api/stores/connect
Authorization: Bearer <token>
Content-Type: application/json
```

请求：

```json
{
  "name": "WYFAN-Ozon-RU",
  "site": "Ozon RU",
  "auth": "api",
  "client_id": "你的 Client ID",
  "api_key": "你的 API Key",
  "test_now": true,
  "note": "主店铺"
}
```

### 3. 重新测试店铺授权

```http
POST /api/stores/{store_id}/test
Authorization: Bearer <token>
```

### 4. 查看单个店铺授权状态

```http
GET /api/stores/{store_id}/auth-status
Authorization: Bearer <token>
```

## 重要说明

当前加密方式是开发版，方便本地跑通流程。正式上线前建议改成：

1. HTTPS 全站启用。
2. 数据库使用 PostgreSQL。
3. API Key 使用生产级加密方案，例如云厂商 KMS、Vault 或 Fernet。
4. 增加操作日志，记录谁在什么时候新增、修改、测试了店铺授权。
5. 增加套餐权限，不同套餐开放不同同步频率。

## 下一步 V4 建议

V4 应该开始做 Ozon 商品同步：

1. 从授权成功的店铺读取商品列表。
2. 写入 `products` 表。
3. 前台商品页面展示真实商品。
4. 后台同步任务页面显示同步成功 / 失败记录。
5. 增加手动同步按钮。
