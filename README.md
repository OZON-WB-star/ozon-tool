# 大鹅ERP 正式开发版

这个版本不是单纯的 GitHub Pages 静态演示，而是按正式软件开发方式拆分：

- `user-frontend/`：用户前台，给注册用户/客户使用。
- `admin-frontend/`：管理后台，给你自己和内部运营人员使用。
- `backend/`：FastAPI 后端接口，负责登录、权限、店铺、商品、订单、选品、数据同步等。
- `docs/`：产品规划、权限设计、数据库设计、接口规划、部署说明。

## 一、前台和后台的区别

### 用户前台
用户前台是客户登录后看到的系统，重点是让客户自己使用工具：注册登录、绑定 Ozon 店铺、商品管理、订单查看、库存预警、选品分析、关键词分析、定价测算、文案模板、数据看板。

### 管理后台
管理后台是你自己用的，不给普通用户看，重点是管理客户和系统：用户管理、店铺授权管理、用户套餐/权限管理、数据同步任务管理、API 服务状态、异常任务处理、后台运营配置。

## 二、本地启动

### 1. 启动后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8010
```

后端健康检查：`http://127.0.0.1:8010/health`

API 文档：`http://127.0.0.1:8010/docs`

### 2. 打开用户前台

```text
user-frontend/index.html
```

### 3. 打开管理后台

```text
admin-frontend/index.html
```

## 三、线上部署建议

正式开发不建议只放 GitHub Pages。推荐：

- 前台：Vercel / Netlify / Cloudflare Pages
- 后台：Vercel / Netlify / Cloudflare Pages，或者单独二级域名 `admin.xxx.com`
- 后端：Render / Railway / Fly.io / 阿里云 / 腾讯云 / 服务器
- 数据库：PostgreSQL
- 缓存和任务：Redis + 定时任务

## 四、正式开发优先级

第一阶段先做 MVP：用户注册登录、前后台权限分离、用户绑定店铺、商品列表同步、订单列表同步、库存预警、定价工具、后台用户管理、后台店铺管理、后台同步任务管理。

详细规划见 `docs/`。
