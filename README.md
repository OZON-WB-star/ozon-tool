# OZON + 1688 Web Workbench

这是桌面版 `OZON + 1688` 工具的本地网页版本。

当前版本已经接入：

- 自动定位 `F:\OZON-PY\OZON_1688独立软件_final` 下的最新 OZON 导出表
- 检测 `http://127.0.0.1:9222` 的浏览器调试连接
- 运行 1688 搜图找货
- 停止当前 1688 任务
- 生成 `*_erp_ready.xlsx`
- 下载 1688 结果表和 ERP 上品表

## 默认目录

程序会优先把下面这个目录当成主项目目录：

```text
F:\OZON-PY\OZON_1688独立软件_final
```

新生成的文件默认写入：

```text
F:\OZON-PY\OZON_1688独立软件_final\EXPORT
```

网页运行期文件会写入：

```text
F:\OZON-PY\OZON_1688独立软件_final\WEB_RUNTIME
```

## 启动

```bat
cd /d C:\Users\admin\Documents\Codex\2026-05-18\1688-excel\web_ozon_1688
python launch.py
```

然后打开：

```text
http://127.0.0.1:8000
```

## 依赖

```bat
pip install -r requirements.txt
playwright install chromium
```

## 当前建议流程

1. 先在 OZON 侧完成采集并导出 Excel。
2. 打开网页后点击“刷新最新导出”。
3. 确认 Chrome 或 Edge 已经登录 1688，并且已开启调试端口。
4. 点击“检测 1688 浏览器”。
5. 点击“运行 1688 找品”。
6. 完成后点击“生成 ERP 上品表”。

## 下一步可继续扩展

- 把 OZON 集采控制也做进网页
- 把 ERP 自动上品表单提交做进网页
- 增加人工复核和利润筛选专页
