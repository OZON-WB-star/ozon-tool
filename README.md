# 大鹅ERP - GitHub Pages 静态部署版

这个目录已经把原来的 `frontend/` 内容提到仓库根目录，适合直接上传到 GitHub Pages、Netlify、Vercel 静态站点。

## 为什么你原来上传后打不开

1. 原包的首页在 `frontend/index.html`，GitHub Pages 默认读取仓库根目录的 `index.html`。
2. `frontend/assets/config.js` 指向 `http://127.0.0.1:8010`，这是你自己电脑本地后端地址，线上访问不到。
3. 部分 HTML 中文是乱码，本版已做编码修复。
4. GitHub Pages 只能部署静态网页，不能运行 `backend/` 里的 FastAPI Python 后端。

## GitHub Pages 使用方法

把本目录内所有文件上传到 GitHub 仓库根目录，不要再套一层 `frontend` 文件夹。

然后进入：

Settings → Pages → Build and deployment → Source 选择 `Deploy from a branch` → Branch 选择 `main` 和 `/root` → Save。

等待 1-3 分钟后访问 GitHub Pages 给你的地址。

## 当前模式

当前为静态演示模式：

```js
window.DAE_STATIC_DEMO_MODE = true;
window.DAE_API_BASE_URL = "";
```

也就是说，页面会使用 `assets/mock-data.js` 里的演示数据，不会连接后端。

如果以后你把 FastAPI 后端部署到服务器，例如 `https://api.your-domain.com`，再把 `assets/config.js` 改成：

```js
window.DAE_STATIC_DEMO_MODE = false;
window.DAE_API_BASE_URL = "https://api.your-domain.com";
```
