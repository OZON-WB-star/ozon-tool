# 大鹅ERP 后端骨架

这是给大鹅ERP前后台准备的第一版后端骨架，目标是先把接口边界、目录结构和数据流梳理清楚，后面再逐步替换为真实数据库、Redis、任务队列和 Ozon API。

## 当前能力

- 用户注册 / 登录接口骨架
- 当前用户资料接口
- 用户店铺绑定与店铺列表接口
- 选品中心数据接口
- 工具中心数据接口
- 后台用户 / 店铺 / 任务接口
- 健康检查接口

## 推荐后续接入顺序

1. 把 `app/services/mock_db.py` 换成真实数据库访问层
2. 接入 JWT 登录态与密码哈希
3. 接入 Ozon Seller API 授权与同步任务
4. 接入 Celery / RQ / APScheduler 任务队列
5. 把前台页面从静态 `mock-data.js` 切到这里的 API

## 运行方式

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
```

启动后可访问：

- `http://127.0.0.1:8010/health`
- `http://127.0.0.1:8010/docs`

## 目录结构

```text
dae-erp-backend/
  app/
    api/routes/
    core/
    schemas/
    services/
    main.py
  requirements.txt
```
