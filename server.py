from __future__ import annotations

import warnings
import cgi
import html
import json
import mimetypes
import os
import sys
import threading
import time
import uuid
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

warnings.filterwarnings("ignore", category=DeprecationWarning, module=r"cgi")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

TRACE_DIR = Path(__file__).resolve().parent / "data"
TRACE_DIR.mkdir(parents=True, exist_ok=True)
TRACE_FILE = TRACE_DIR / "server_import.log"


def _trace(message: str) -> None:
    with TRACE_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")


_trace("server module start")

from openpyxl import load_workbook

_trace("openpyxl import ok")

from finder1688.excel_io import ExcelWorkbookAdapter

_trace("finder1688.excel_io import ok")


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
RESULT_DIR = DATA_DIR / "results"
TMP_DIR = DATA_DIR / "tmp"

HOST = "127.0.0.1"
PORT = 8000

for folder in (UPLOAD_DIR, RESULT_DIR, TMP_DIR):
    folder.mkdir(parents=True, exist_ok=True)


STATE_LOCK = threading.Lock()
STATE: Dict[str, Any] = {
    "current_upload": None,
    "current_result": None,
    "job": None,
    "message": "等待上传 Excel。",
}


INDEX_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OZON + 1688 网页版工作台</title>
  <style>
    :root {
      --bg: #0b1220;
      --panel: rgba(15, 23, 42, 0.78);
      --panel-strong: #111827;
      --line: rgba(148, 163, 184, 0.18);
      --text: #e5eefc;
      --muted: #9fb0cc;
      --accent: #ff9f43;
      --accent-2: #46d3c6;
      --danger: #ff6b6b;
      --success: #67e8a1;
      --shadow: 0 24px 70px rgba(2, 6, 23, 0.45);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(70, 211, 198, 0.18), transparent 35%),
        radial-gradient(circle at top right, rgba(255, 159, 67, 0.18), transparent 28%),
        linear-gradient(160deg, #060b16 0%, #0b1220 52%, #10182a 100%);
      font-family: "Segoe UI Variable", "Microsoft YaHei UI", "PingFang SC", sans-serif;
      min-height: 100vh;
    }
    .shell {
      max-width: 1480px;
      margin: 0 auto;
      padding: 28px 22px 36px;
    }
    .hero {
      display: grid;
      grid-template-columns: 1.8fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
      animation: fadeIn 0.45s ease-out;
    }
    .brand, .status-strip, .card, .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      backdrop-filter: blur(14px);
      border-radius: 22px;
    }
    .brand {
      padding: 24px 26px;
      position: relative;
      overflow: hidden;
    }
    .brand::after {
      content: "";
      position: absolute;
      inset: auto -120px -120px auto;
      width: 260px;
      height: 260px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(255, 159, 67, 0.22), transparent 65%);
      pointer-events: none;
    }
    .eyebrow {
      color: var(--accent-2);
      letter-spacing: 0.12em;
      text-transform: uppercase;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 10px;
    }
    h1 {
      margin: 0;
      font-size: clamp(28px, 4vw, 42px);
      line-height: 1.05;
    }
    .subtitle {
      margin-top: 14px;
      max-width: 760px;
      color: var(--muted);
      line-height: 1.7;
      font-size: 15px;
    }
    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }
    .chip {
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--line);
      color: var(--text);
      font-size: 13px;
    }
    .status-strip {
      padding: 20px 20px 18px;
      display: grid;
      gap: 10px;
    }
    .status-title {
      font-size: 14px;
      color: var(--muted);
    }
    .status-value {
      font-size: 18px;
      font-weight: 700;
      line-height: 1.35;
    }
    .status-meta {
      display: grid;
      gap: 8px;
      font-size: 13px;
      color: var(--muted);
    }
    .grid {
      display: grid;
      grid-template-columns: 1.05fr 1.1fr;
      gap: 16px;
      align-items: start;
    }
    .card {
      padding: 20px;
    }
    .section-title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 16px;
    }
    .section-title h2 {
      margin: 0;
      font-size: 20px;
    }
    .section-title p {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
    }
    .uploader {
      border: 1px dashed rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.04);
      padding: 18px;
      border-radius: 18px;
      display: grid;
      gap: 12px;
    }
    .uploader input[type="file"] {
      width: 100%;
      color: var(--muted);
    }
    .row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .btn {
      appearance: none;
      border: 0;
      border-radius: 14px;
      padding: 12px 16px;
      font-weight: 700;
      cursor: pointer;
      transition: transform 0.15s ease, opacity 0.15s ease, background 0.15s ease;
    }
    .btn:hover { transform: translateY(-1px); }
    .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
    .btn-primary {
      background: linear-gradient(135deg, var(--accent), #ffd166);
      color: #1c1404;
    }
    .btn-secondary {
      background: rgba(255,255,255,0.08);
      color: var(--text);
      border: 1px solid var(--line);
    }
    .btn-danger {
      background: rgba(255, 107, 107, 0.18);
      color: #ffdede;
      border: 1px solid rgba(255, 107, 107, 0.35);
    }
    .stack {
      display: grid;
      gap: 12px;
    }
    .kv {
      display: grid;
      grid-template-columns: 130px 1fr;
      gap: 12px;
      align-items: start;
      font-size: 14px;
      padding: 12px 0;
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .kv:last-child { border-bottom: 0; }
    .kv .k { color: var(--muted); }
    .kv .v { word-break: break-all; }
    .summary-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }
    .metric {
      padding: 16px;
      border-radius: 18px;
      background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.04));
      border: 1px solid var(--line);
    }
    .metric .num {
      display: block;
      font-size: 24px;
      font-weight: 800;
      margin-bottom: 4px;
    }
    .metric .label {
      color: var(--muted);
      font-size: 13px;
    }
    .table-wrap {
      overflow: auto;
      border-radius: 16px;
      border: 1px solid var(--line);
      background: rgba(7, 12, 22, 0.72);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 1000px;
    }
    thead th {
      position: sticky;
      top: 0;
      background: #111827;
      color: #d8e6ff;
      text-align: left;
      font-size: 13px;
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    tbody td {
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      font-size: 13px;
      color: #e6eefc;
      vertical-align: top;
    }
    tbody tr:hover td {
      background: rgba(255,255,255,0.03);
    }
    .muted { color: var(--muted); }
    .ok { color: var(--success); }
    .warn { color: #ffd166; }
    .bad { color: var(--danger); }
    .footer {
      margin-top: 18px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.8;
    }
    a { color: #8bd3ff; text-decoration: none; }
    a:hover { text-decoration: underline; }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @media (max-width: 1100px) {
      .hero, .grid { grid-template-columns: 1fr; }
      .summary-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 720px) {
      .shell { padding: 16px 12px 28px; }
      .summary-grid { grid-template-columns: 1fr; }
      .kv { grid-template-columns: 1fr; gap: 4px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <div class="hero">
      <div class="brand">
        <div class="eyebrow">OZON + 1688 WEB WORKBENCH</div>
        <h1>OZON 选品 + 1688 找货 + ERP 上品<br/>网页版本</h1>
        <div class="subtitle">
          这是你当前桌面版软件的网页化工作台。先把 Excel 导进来，生成可上品表，再逐步接入 1688 检索和 ERP 自动填单。
          目前先做成本地版，适合在你自己的电脑上运行，避免浏览器登录、1688 会话和 ERP 账号分离。
        </div>
        <div class="chips">
          <div class="chip">本地运行</div>
          <div class="chip">Excel 上传</div>
          <div class="chip">ERP 上品表生成</div>
          <div class="chip">结果下载</div>
          <div class="chip">后续可接 1688 自动找品</div>
        </div>
      </div>
      <div class="status-strip">
        <div class="status-title">当前状态</div>
        <div class="status-value" id="jobStatus">正在载入...</div>
        <div class="status-meta">
          <div>当前文件：<span id="currentUpload" class="muted">无</span></div>
          <div>最新结果：<span id="currentResult" class="muted">无</span></div>
          <div>提示：<span id="message" class="muted">无</span></div>
        </div>
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <div class="section-title">
          <div>
            <h2>上传与处理</h2>
            <p>上传 Excel 后，点击生成 ERP 上品表。结果会自动保存到本地。</p>
          </div>
        </div>

        <div class="uploader">
          <input id="fileInput" type="file" accept=".xlsx,.xlsm,.xltx,.xltm" />
          <div class="row">
            <button class="btn btn-primary" id="uploadBtn">上传 Excel</button>
            <button class="btn btn-secondary" id="generateBtn">生成 ERP 上品表</button>
            <button class="btn btn-secondary" id="refreshBtn">刷新状态</button>
            <button class="btn btn-danger" id="clearBtn">清空当前文件</button>
          </div>
          <div class="muted" id="uploadHint">建议上传你当前已经处理好的 `_1688_ready.xlsx` 文件。</div>
        </div>

        <div style="height:14px"></div>

        <div class="summary-grid" id="summaryGrid">
          <div class="metric"><span class="num">-</span><span class="label">工作表数量</span></div>
          <div class="metric"><span class="num">-</span><span class="label">目标行数</span></div>
          <div class="metric"><span class="num">-</span><span class="label">文件大小</span></div>
          <div class="metric"><span class="num">-</span><span class="label">最新状态</span></div>
        </div>

        <div class="footer">
          <div>网页服务地址：<span class="warn">http://127.0.0.1:8000</span></div>
          <div>如果你后面要接真正的 1688 自动找品，我们可以把 Playwright 进程也挂到这个网页后台里，做成一键运行。</div>
        </div>
      </div>

      <div class="card">
        <div class="section-title">
          <div>
            <h2>文件与预览</h2>
            <p>查看当前文件信息、生成结果和前几条商品预览。</p>
          </div>
          <div class="row">
            <a class="btn btn-secondary" id="downloadLink" href="#" target="_blank" style="display:none;text-decoration:none;">下载结果</a>
          </div>
        </div>

        <div class="stack">
          <div class="panel" style="padding:16px;">
            <div class="kv"><div class="k">输入文件</div><div class="v" id="uploadPath">无</div></div>
            <div class="kv"><div class="k">输出文件</div><div class="v" id="resultPath">无</div></div>
            <div class="kv"><div class="k">处理任务</div><div class="v" id="jobInfo">无</div></div>
          </div>

          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style="width:72px;">#</th>
                  <th>商品标题</th>
                  <th>SKU</th>
                  <th>评分</th>
                  <th>OZON 售价</th>
                  <th>1688 匹配</th>
                  <th>备注</th>
                </tr>
              </thead>
              <tbody id="previewBody">
                <tr><td colspan="7" class="muted">暂无数据，请先上传 Excel。</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const stateUrl = "/api/state";
    const uploadBtn = document.getElementById("uploadBtn");
    const generateBtn = document.getElementById("generateBtn");
    const refreshBtn = document.getElementById("refreshBtn");
    const clearBtn = document.getElementById("clearBtn");
    const fileInput = document.getElementById("fileInput");
    const downloadLink = document.getElementById("downloadLink");

    async function refreshState() {
      const res = await fetch(stateUrl, {cache: "no-store"});
      const data = await res.json();
      renderState(data);
      return data;
    }

    function renderState(data) {
      document.getElementById("jobStatus").textContent = data.job ? data.job.status_text : "等待上传 Excel";
      document.getElementById("currentUpload").textContent = data.current_upload || "无";
      document.getElementById("currentResult").textContent = data.current_result || "无";
      document.getElementById("message").textContent = data.message || "无";
      document.getElementById("uploadPath").textContent = data.current_upload_path || "无";
      document.getElementById("resultPath").textContent = data.current_result_path || "无";
      document.getElementById("jobInfo").textContent = data.job ? `${data.job.id} / ${data.job.status_text}` : "无";

      const summary = data.summary || {};
      const metrics = document.querySelectorAll(".metric .num");
      metrics[0].textContent = summary.sheet_count ?? "-";
      metrics[1].textContent = summary.target_rows ?? "-";
      metrics[2].textContent = summary.file_size_text ?? "-";
      metrics[3].textContent = data.job ? data.job.status_text : "待命";

      const body = document.getElementById("previewBody");
      body.innerHTML = "";
      const preview = data.preview || [];
      if (!preview.length) {
        body.innerHTML = '<tr><td colspan="7" class="muted">暂无可预览的目标行。</td></tr>';
      } else {
        preview.forEach((row, index) => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${escapeHtml(row.title || "")}</td>
            <td>${escapeHtml(row.sku || "")}</td>
            <td>${row.score ?? ""}</td>
            <td>${row.ozon_price_cny ?? ""}</td>
            <td>${escapeHtml(row.status || "")}</td>
            <td>${escapeHtml(row.note || "")}</td>
          `;
          body.appendChild(tr);
        });
      }

      if (data.current_result_path) {
        downloadLink.style.display = "inline-flex";
        downloadLink.href = data.download_url || "#";
      } else {
        downloadLink.style.display = "none";
      }
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    async function uploadFile() {
      const file = fileInput.files[0];
      if (!file) {
        alert("请先选择一个 Excel 文件。");
        return;
      }
      const form = new FormData();
      form.append("file", file);
      uploadBtn.disabled = true;
      uploadBtn.textContent = "上传中...";
      try {
        const res = await fetch("/api/upload", { method: "POST", body: form });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "上传失败");
        await refreshState();
        alert("上传成功：" + data.filename);
      } catch (err) {
        alert(err.message);
      } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = "上传 Excel";
      }
    }

    async function generateErp() {
      generateBtn.disabled = true;
      generateBtn.textContent = "处理中...";
      try {
        const res = await fetch("/api/generate-erp", { method: "POST" });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "生成失败");
        alert("已开始生成 ERP 上品表。");
        await refreshState();
      } catch (err) {
        alert(err.message);
      } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = "生成 ERP 上品表";
      }
    }

    async function clearCurrent() {
      const res = await fetch("/api/clear", { method: "POST" });
      const data = await res.json();
      if (!res.ok) {
        alert(data.error || "清空失败");
        return;
      }
      fileInput.value = "";
      await refreshState();
    }

    uploadBtn.addEventListener("click", uploadFile);
    generateBtn.addEventListener("click", generateErp);
    refreshBtn.addEventListener("click", refreshState);
    clearBtn.addEventListener("click", clearCurrent);

    refreshState();
    setInterval(refreshState, 2000);
  </script>
</body>
</html>
"""

INDEX_FILE = Path(__file__).resolve().parent / "index.html"


def _set_state(**kwargs: Any) -> None:
    with STATE_LOCK:
        STATE.update(kwargs)


def _get_state() -> Dict[str, Any]:
    with STATE_LOCK:
        return dict(STATE)


def _safe_filename(name: str) -> str:
    return Path(name).name.replace("\\", "_").replace("/", "_")


def _human_size(num: int) -> str:
    value = float(num)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024.0:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024.0
    return f"{value:.1f} TB"


def _inspect_workbook(path: Path) -> Dict[str, Any]:
    try:
        workbook = load_workbook(path, read_only=True, data_only=True)
    except Exception as exc:
        return {
            "sheet_count": 0,
            "target_rows": 0,
            "file_size_text": _human_size(path.stat().st_size),
            "error": str(exc),
        }

    try:
        adapter = ExcelWorkbookAdapter(path)
        preview_rows = list(adapter.iter_target_rows())[:8]
        target_count = sum(1 for _ in adapter.iter_target_rows())
    except Exception:
        preview_rows = []
        target_count = 0

    return {
        "sheet_count": len(workbook.sheetnames),
        "sheet_names": workbook.sheetnames,
        "target_rows": target_count,
        "preview_rows": [asdict(row) for row in preview_rows],
        "file_size_text": _human_size(path.stat().st_size),
    }


def _current_paths() -> Dict[str, Path | None]:
    state = _get_state()
    upload = Path(state["current_upload_path"]) if state.get("current_upload_path") else None
    result = Path(state["current_result_path"]) if state.get("current_result_path") else None
    return {"upload": upload, "result": result}


def _start_generate_erp() -> Dict[str, Any]:
    paths = _current_paths()
    src = paths["upload"]
    if src is None or not src.exists():
        return {"ok": False, "error": "请先上传 Excel 文件。"}

    with STATE_LOCK:
        job = STATE.get("job")
        if job and job.get("running"):
            return {"ok": False, "error": "已有任务正在执行。"}

        job_id = uuid.uuid4().hex[:10]
        job = {
            "id": job_id,
            "running": True,
            "status_text": "生成中",
            "source": str(src),
            "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "output": "",
            "error": "",
        }
        STATE["job"] = job
        STATE["message"] = "ERP 上品表生成中..."

    def worker() -> None:
        try:
            output_name = f"{src.stem}_erp_ready{src.suffix}"
            output_path = RESULT_DIR / output_name
            adapter = ExcelWorkbookAdapter(src)
            adapter.save(output_path)

            with STATE_LOCK:
                STATE["current_result"] = output_name
                STATE["current_result_path"] = str(output_path)
                STATE["job"] = {
                    **STATE["job"],
                    "running": False,
                    "status_text": "完成",
                    "output": str(output_path),
                    "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                STATE["message"] = "ERP 上品表已生成。"
        except Exception as exc:
            with STATE_LOCK:
                STATE["job"] = {
                    **STATE["job"],
                    "running": False,
                    "status_text": "失败",
                    "error": str(exc),
                    "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                STATE["message"] = f"生成失败：{exc}"

    threading.Thread(target=worker, daemon=True).start()
    return {"ok": True, "job_id": job_id}


class WebHandler(BaseHTTPRequestHandler):
    server_version = "Ozon1688Web/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_html(load_index_html())
            return
        if parsed.path == "/api/state":
            self._send_json(self._build_state_payload())
            return
        if parsed.path.startswith("/download/"):
            self._send_download(parsed.path.removeprefix("/download/"))
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/upload":
            self._handle_upload()
            return
        if parsed.path == "/api/generate-erp":
            payload = _start_generate_erp()
            self._send_json(payload, status=HTTPStatus.OK if payload.get("ok") else HTTPStatus.BAD_REQUEST)
            return
        if parsed.path == "/api/clear":
            self._handle_clear()
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def _handle_upload(self) -> None:
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._send_json({"error": "请使用文件上传表单。"}, status=HTTPStatus.BAD_REQUEST)
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": content_type,
                "CONTENT_LENGTH": self.headers.get("Content-Length", ""),
            },
        )
        file_item = form["file"] if "file" in form else None
        if not file_item or not getattr(file_item, "filename", ""):
            self._send_json({"error": "没有收到上传文件。"}, status=HTTPStatus.BAD_REQUEST)
            return

        raw_name = _safe_filename(file_item.filename)
        if not raw_name.lower().endswith((".xlsx", ".xlsm", ".xltx", ".xltm")):
            self._send_json({"error": "只支持 Excel 文件。"}, status=HTTPStatus.BAD_REQUEST)
            return

        upload_path = UPLOAD_DIR / f"{int(time.time())}_{raw_name}"
        with upload_path.open("wb") as f:
            f.write(file_item.file.read())

        result_path = RESULT_DIR / f"{upload_path.stem}_erp_ready{upload_path.suffix}"
        _set_state(
            current_upload=raw_name,
            current_upload_path=str(upload_path),
            current_result=result_path.name if result_path.exists() else None,
            current_result_path=str(result_path) if result_path.exists() else None,
            message=f"已上传 {raw_name}",
        )

        self._send_json({
            "ok": True,
            "filename": raw_name,
            "saved_as": upload_path.name,
        })

    def _handle_clear(self) -> None:
        _set_state(
            current_upload=None,
            current_upload_path=None,
            current_result=None,
            current_result_path=None,
            job=None,
            message="已清空当前文件。",
        )
        self._send_json({"ok": True})

    def _build_state_payload(self) -> Dict[str, Any]:
        state = _get_state()
        upload_path = Path(state["current_upload_path"]) if state.get("current_upload_path") else None
        result_path = Path(state["current_result_path"]) if state.get("current_result_path") else None
        summary = {}
        preview: List[Dict[str, Any]] = []

        if upload_path and upload_path.exists():
            summary = _inspect_workbook(upload_path)
            preview = summary.get("preview_rows", [])
        elif result_path and result_path.exists():
            summary = _inspect_workbook(result_path)
            preview = summary.get("preview_rows", [])

        job = state.get("job")
        if job:
            job = dict(job)

        payload = {
            "current_upload": state.get("current_upload"),
            "current_upload_path": str(upload_path) if upload_path else "",
            "current_result": state.get("current_result"),
            "current_result_path": str(result_path) if result_path else "",
            "message": state.get("message"),
            "job": job,
            "summary": summary,
            "preview": preview,
            "download_url": f"/download/{Path(state['current_result_path']).name}" if state.get("current_result_path") else "",
        }
        return payload

    def _send_json(self, data: Dict[str, Any], status: int = HTTPStatus.OK) -> None:
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_html(self, text: str, status: int = HTTPStatus.OK) -> None:
        encoded = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_download(self, filename: str) -> None:
        filename = _safe_filename(filename)
        candidate_paths = [RESULT_DIR / filename, UPLOAD_DIR / filename]
        for path in candidate_paths:
            if path.exists() and path.is_file():
                mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
                with path.open("rb") as f:
                    blob = f.read()
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(blob)))
                self.send_header("Content-Disposition", f'attachment; filename="{path.name}"')
                self.end_headers()
                self.wfile.write(blob)
                return
        self.send_error(HTTPStatus.NOT_FOUND, "File not found")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), WebHandler)
    print(f"Web app running at http://{HOST}:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def load_index_html() -> str:
    if INDEX_FILE.exists():
        return INDEX_FILE.read_text(encoding="utf-8")
    return INDEX_HTML


if __name__ == "__main__":
    main()
