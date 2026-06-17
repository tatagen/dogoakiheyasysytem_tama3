import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import List

from state import LOGIN_ATTEMPTS, PERMANENT_BANS, TOTAL_FAILURES

SESSION_COOKIE = "dogo_session"
SESSION_MAX_AGE = 60 * 60 * 17 + 60 * 30
LOGIN_WINDOW_SECONDS = 30 * 60
LOGIN_MAX_ATTEMPTS = 5
PERMANENT_BAN_THRESHOLD = 40

APP_USERNAME = os.getenv("DOGO_APP_USERNAME", "staff")
APP_PASSWORD = os.getenv("DOGO_APP_PASSWORD", "ChangeMe123!")
SESSION_SECRET = os.getenv("DOGO_SESSION_SECRET", "change-this-session-secret")


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def make_session_value(username: str) -> tuple:
    csrf_token = secrets.token_urlsafe(24)
    payload = {"u": username, "csrf": csrf_token, "iat": int(time.time())}
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_b64 = _b64url_encode(payload_bytes)
    sig = hmac.new(SESSION_SECRET.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{sig}", csrf_token


def parse_session_value(raw_value):
    if not raw_value or "." not in raw_value:
        return None
    payload_b64, sig = raw_value.rsplit(".", 1)
    expected = hmac.new(SESSION_SECRET.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return None
    try:
        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
    except Exception:
        return None
    if int(payload.get("iat", 0)) + SESSION_MAX_AGE < int(time.time()):
        return None
    return payload


def get_client_ip(request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def prune_login_attempts(ip: str) -> List[float]:
    now = time.time()
    recent = [ts for ts in LOGIN_ATTEMPTS.get(ip, []) if now - ts <= LOGIN_WINDOW_SECONDS]
    LOGIN_ATTEMPTS[ip] = recent
    return recent


def is_authenticated(request) -> bool:
    return bool(getattr(request.state, "session", None))
