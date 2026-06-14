# xuanping + 1688 Web Workbench

本项目是  选品 + 1688 找货 + ERP 上品的本地网页版本。

## 当前功能

- 上传 Excel
- 预览目标商品
- 生成 `*_erp_ready.xlsx`
- 下载结果文件

## 目录结构

```text
web_ozon_1688/
  index.html
  launch.py
  requirements.txt
  run_web.bat
  server.py
  .gitignore
```

## 启动

```bat
cd /d C:\Users\admin\Documents\Codex\2026-05-18\1688-excel\web_ozon_1688
python launch.py
```

然后打开：

`http://127.0.0.1:8000`

## 依赖

```bat
pip install -r requirements.txt
```

## 说明

- 这是本地网页服务，适合直接上传到 GitHub 作为源码仓库。
- 后续可以继续接入 1688 自动找品和 ERP 自动填单。
