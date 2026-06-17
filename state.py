from datetime import datetime, timedelta, timezone
from typing import Dict, List
import json
import uuid

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Asia/Tokyo")
except Exception:
    TZ = timezone(timedelta(hours=9))

ROOMS: Dict[int, dict] = {
    1: {"id": 1, "name": "一号室", "capacity": 4, "status": "available", "eta_at": None, "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    2: {"id": 2, "name": "二号室", "capacity": 4, "status": "available", "eta_at": None, "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    3: {"id": 3, "name": "三号室", "capacity": 4, "status": "available", "eta_at": None, "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    4: {"id": 4, "name": "五号室", "capacity": 2, "status": "available", "eta_at": None, "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    5: {"id": 5, "name": "六号室", "capacity": 4, "status": "available", "eta_at": None, "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    6: {"id": 6, "name": "七号室", "capacity": 6, "status": "available", "eta_at": None, "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    7: {"id": 7, "name": "八号室", "capacity": 4, "status": "available", "eta_at": None, "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
    8: {"id": 8, "name": "十号室", "capacity": 4, "status": "available", "eta_at": None, "currentRequestId": None, "currentSeq": None, "currentHeadcount": None},
}

REQUESTS: Dict[str, dict] = {}
PENDING: List[str] = []
HEADING: List[str] = []
HISTORY: List[dict] = []
CANCELED: List[dict] = []
SEQ_COUNTER = 1

LOGIN_ATTEMPTS: Dict[str, List[float]] = {}
PERMANENT_BANS: set = set()
TOTAL_FAILURES: Dict[str, int] = {}

_STATE_LOADED = False


def is_state_loaded() -> bool:
    return _STATE_LOADED


def mark_state_loaded():
    global _STATE_LOADED
    _STATE_LOADED = True


def now_str() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def ceil_to_5min(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    else:
        dt = dt.astimezone(TZ)
    minute = ((dt.minute + 4) // 5) * 5
    if minute >= 60:
        dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        dt = dt.replace(minute=minute, second=0, microsecond=0)
    return dt


def build_request(headcount: int) -> dict:
    global SEQ_COUNTER
    rid = str(uuid.uuid4())
    seq = SEQ_COUNTER
    req = {
        "id": rid,
        "seq": seq,
        "seq_label": f"{seq}",
        "seq_part": None,
        "seq_parts": None,
        "headcount": headcount,
        "calling": False,
        "updated_at": now_str(),
        "room_id": None,
    }
    REQUESTS[rid] = req
    SEQ_COUNTER += 1
    return req


def move_request(rid: str, src: List[str], dst: List[str]):
    if rid in src:
        src.remove(rid)
    if rid not in dst:
        dst.append(rid)


def _state_data() -> dict:
    return {
        "rooms": {str(k): v for k, v in ROOMS.items()},
        "requests": REQUESTS,
        "pending": PENDING,
        "heading": HEADING,
        "history": HISTORY,
        "canceled": CANCELED,
        "seq_counter": SEQ_COUNTER,
        "permanent_bans": list(PERMANENT_BANS),
        "total_failures": TOTAL_FAILURES,
    }


def _apply_state(d: dict):
    global SEQ_COUNTER
    ROOMS.clear()
    ROOMS.update({int(k): v for k, v in d["rooms"].items()})
    REQUESTS.clear()
    REQUESTS.update(d["requests"])
    PENDING[:] = d["pending"]
    HEADING[:] = d["heading"]
    HISTORY[:] = d["history"]
    CANCELED[:] = d["canceled"]
    SEQ_COUNTER = d["seq_counter"]
    PERMANENT_BANS.clear()
    PERMANENT_BANS.update(d.get("permanent_bans", []))
    TOTAL_FAILURES.clear()
    TOTAL_FAILURES.update(d.get("total_failures", {}))


def _get_kv(request):
    env = request.scope.get("cloudflare.workers.env") or request.scope.get("env")
    if env is None:
        return None
    return getattr(env, "STATE_KV", None)


async def save_state(request):
    kv = _get_kv(request)
    if kv is None:
        return
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    try:
        data = json.dumps({"saved_date": today, "data": _state_data()}, ensure_ascii=False)
        await kv.put("state", data)
    except Exception:
        pass


async def load_state(request):
    kv = _get_kv(request)
    if kv is None:
        return
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    try:
        raw = await kv.get("state")
        if not raw:
            return
        saved = json.loads(raw)
        if saved.get("saved_date") != today:
            return
        _apply_state(saved["data"])
    except Exception:
        pass
