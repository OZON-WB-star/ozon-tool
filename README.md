# 大鹅ERP 正式开发版 V3

这是面向正式开发的跨境电商 ERP / SaaS 项目骨架。

## V3 已完成

- 用户前台和管理后台分离
- FastAPI 后端
- SQLite 本地开发数据库
- 用户注册 / 登录
- JWT 登录状态
- 普通用户与管理员权限隔离
- Ozon 店铺授权接入
- Ozon Client ID / API Key 保存
- Ozon API 授权测试
- 后台查看所有用户店铺授权状态

## 目录结构

```text
dae-erp-formal-dev/
├─ user-frontend/       用户前台
├─ admin-frontend/      管理后台
├─ backend/             FastAPI 后端
├─ docs/                产品、接口、数据库、部署文档
├─ docker-compose.yml   PostgreSQL + Redis 开发环境
└─ .env.example         环境变量示例
```

## 启动后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
```

接口文档：

```text
http://127.0.0.1:8010/docs
```

## 默认测试账号

用户前台：

```text
账号：demo@example.com
密码：user123456
```

管理后台：

```text
账号：admin@example.com
密码：admin123456
```

## 打开前端

用户前台：

```text
user-frontend/login.html
```

管理后台：

```text
admin-frontend/login.html
```

## V3 使用流程

1. 启动后端。
2. 打开 `user-frontend/login.html`。
3. 登录普通用户账号。
4. 进入 `connect-store.html`。
5. 填写 Ozon Client ID 和 API Key。
6. 勾选“提交时立即测试 Ozon API 授权”。
7. 提交后查看店铺状态。
8. 管理员登录后台，在 `admin-frontend/stores.html` 查看所有店铺授权状态。

## 注意

如果你从 V2 升级到 V3，本地已有 `backend/dae_erp.db`，可能缺少新增字段。开发阶段最简单的处理方式是删除旧数据库文件后重新启动后端：

```text
backend/dae_erp.db
```

正式上线后不能这样处理，需要使用 Alembic 做数据库迁移。

## 下一步

建议做 V4：Ozon 商品同步。
