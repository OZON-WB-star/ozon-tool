import json
from dataclasses import dataclass
from urllib import error, request

OZON_API_BASE = "https://api-seller.ozon.ru"


@dataclass
class OzonTestResult:
    ok: bool
    message: str
    warehouse_count: int = 0
    raw_status: int | None = None


def _post_json(path: str, client_id: str, api_key: str, payload: dict | None = None, timeout: int = 12) -> tuple[int, dict]:
    body = json.dumps(payload or {}).encode("utf-8")
    req = request.Request(
        f"{OZON_API_BASE}{path}",
        data=body,
        method="POST",
        headers={
            "Client-Id": client_id,
            "Api-Key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "dae-erp-dev/0.3",
        },
    )
    with request.urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode("utf-8")
        return resp.status, json.loads(data) if data else {}


def test_ozon_credentials(client_id: str, api_key: str) -> OzonTestResult:
    """Validate Seller API credentials with a low-risk read endpoint.

    /v1/warehouse/list does not require request parameters; Ozon identifies
    the company by Client-Id and Api-Key.
    """
    if not client_id or not api_key:
        return OzonTestResult(False, "请填写 Client ID 和 API Key")
    try:
        status, payload = _post_json("/v1/warehouse/list", client_id, api_key, {})
        warehouses = payload.get("result") or []
        return OzonTestResult(True, f"Ozon API 授权成功，检测到 {len(warehouses)} 个仓库", len(warehouses), status)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")[:300]
        if exc.code in {401, 403}:
            return OzonTestResult(False, "授权失败：Client ID 或 API Key 不正确，或 API Key 权限不足", 0, exc.code)
        return OzonTestResult(False, f"Ozon API 返回错误 {exc.code}：{detail or '无详细信息'}", 0, exc.code)
    except Exception as exc:
        return OzonTestResult(False, f"无法连接 Ozon API：{exc}", 0, None)
