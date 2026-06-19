# 部署说明

## 推荐域名结构

- 用户前台：`https://app.yourdomain.com`
- 管理后台：`https://admin.yourdomain.com`
- 后端接口：`https://api.yourdomain.com`

## GitHub Pages 是否适合正式项目？

GitHub Pages 可以放静态前端，但不能运行后端。正式项目需要前台页面、后台页面、后端 API、PostgreSQL 数据库分开部署。

## 上线前必须处理

密码加密、API Key 加密、HTTPS、CORS 白名单、管理后台权限校验、数据备份、日志记录。
