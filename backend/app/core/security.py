import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.config import settings

ALGORITHM = "HS256"


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return f"pbkdf2_sha256${_b64url_encode(salt)}${_b64url_encode(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        scheme, salt_b64, digest_b64 = password_hash.split("$", 2)
        if scheme != "pbkdf2_sha256":
            return False
        salt = _b64url_decode(salt_b64)
        expected = _b64url_decode(digest_b64)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def create_access_token(data: dict[str, Any], expires_minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    payload = data.copy()
    payload["exp"] = int(expire.timestamp())
    header = {"typ": "JWT", "alg": ALGORITHM}
    signing_input = f"{_b64url_encode(json.dumps(header, separators=(',', ':')).encode())}.{_b64url_encode(json.dumps(payload, separators=(',', ':')).encode())}"
    signature = hmac.new(settings.secret_key.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url_encode(signature)}"


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
        signing_input = f"{header_b64}.{payload_b64}"
        expected = hmac.new(settings.secret_key.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256).digest()
        actual = _b64url_decode(signature_b64)
        if not hmac.compare_digest(expected, actual):
            return None
        payload = json.loads(_b64url_decode(payload_b64))
        if int(payload.get("exp", 0)) < int(datetime.now(timezone.utc).timestamp()):
            return None
        return payload
    except Exception:
        return None



def _secret_stream(length: int) -> bytes:
    seed = hashlib.sha256(settings.secret_key.encode("utf-8")).digest()
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(hashlib.sha256(seed + str(counter).encode("ascii")).digest())
        counter += 1
    return bytes(out[:length])


def encrypt_secret(value: str | None) -> str | None:
    """Lightweight reversible encryption for development.

    Production should replace this with KMS/Fernet/secret manager.
    """
    if not value:
        return None
    raw = value.encode("utf-8")
    key = _secret_stream(len(raw))
    cipher = bytes(a ^ b for a, b in zip(raw, key))
    return _b64url_encode(cipher)


def decrypt_secret(value: str | None) -> str | None:
    if not value:
        return None
    try:
        cipher = _b64url_decode(value)
        key = _secret_stream(len(cipher))
        raw = bytes(a ^ b for a, b in zip(cipher, key))
        return raw.decode("utf-8")
    except Exception:
        return None


def mask_secret(value: str | None, head: int = 4, tail: int = 4) -> str:
    if not value:
        return "未配置"
    if len(value) <= head + tail:
        return "*" * len(value)
    return f"{value[:head]}{'*' * 8}{value[-tail:]}"
