import os
import time
from datetime import datetime, timedelta

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Route

import state as st
import auth as au
from templates import LOGIN_HTML, HTML

ALLOWED_HOST_SUFFIXES = tuple(
    x.strip()
    for x in os.getenv("DOGO_ALLOWED_HOSTS", "localhost,127.0.0.1,.workers.dev").split(",")
    if x.strip()
)


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not st.is_state_loaded():
            await st.load_state(request)
            st.mark_state_loaded()

        host = (request.headers.get("host") or "").split(":")[0]
        if host and not any(host == a or host.endswith(a) for a in ALLOWED_HOST_SUFFIXES):
            return JSONResponse({"ok": False, "msg": "invalid host"}, status_code=400)

        request.state.session = au.parse_session_value(request.cookies.get(au.SESSION_COOKIE))

        if request.url.path.startswith("/api/") and request.url.path not in ("/api/login",):
            if not au.is_authenticated(request):
                return JSONResponse({"ok": False, "msg": "authentication required"}, status_code=401)

        if request.method == "POST" and request.url.path.startswith("/api/") and request.url.path not in ("/api/login",):
            session = getattr(request.state, "session", None) or {}
            csrf_header = request.headers.get("x-csrf-token", "")
            if not csrf_header or csrf_header != session.get("csrf"):
                return JSONResponse({"ok": False, "msg": "invalid csrf token"}, status_code=403)

        if request.url.path == "/" and not au.is_authenticated(request):
            return self._with_headers(HTMLResponse(LOGIN_HTML))

        response = await call_next(request)

        if (request.method == "POST"
                and request.url.path.startswith("/api/")
                and request.url.path not in ("/api/login", "/api/logout")
                and response.status_code < 400):
            await st.save_state(request)

        return self._with_headers(response)

    def _with_headers(self, response: Response) -> Response:
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self' 'unsafe-inline'; "
            "script-src 'self' 'unsafe-inline'; img-src 'self' data:; "
            "connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        )
        return response


async def home(request: Request):
    session = getattr(request.state, "session", None)
    if not session:
        return HTMLResponse(LOGIN_HTML)
    return HTMLResponse(HTML.replace("__CSRF_TOKEN__", session["csrf"]))


async def login_api(request: Request):
    ip = au.get_client_ip(request)

    if ip in st.PERMANENT_BANS:
        return JSONResponse({"ok": False, "msg": "このアクセス元は永久にブロックされています。"}, status_code=403)

    attempts = au.prune_login_attempts(ip)
    if len(attempts) >= au.LOGIN_MAX_ATTEMPTS:
        return JSONResponse({"ok": False, "msg": "試行回数が多すぎます。しばらく待ってから再試行してください。"}, status_code=429)

    body = await request.json()
    username = str(body.get("username", ""))
    password = str(body.get("password", ""))
    if username != au.APP_USERNAME or password != au.APP_PASSWORD:
        attempts.append(time.time())
        st.LOGIN_ATTEMPTS[ip] = attempts
        st.TOTAL_FAILURES[ip] = st.TOTAL_FAILURES.get(ip, 0) + 1
        if st.TOTAL_FAILURES[ip] >= au.PERMANENT_BAN_THRESHOLD:
            st.PERMANENT_BANS.add(ip)
            await st.save_state(request)
            return JSONResponse({"ok": False, "msg": "このアクセス元は永久にブロックされています。"}, status_code=403)
        return JSONResponse({"ok": False, "msg": "ユーザー名またはパスワードが違います。"}, status_code=401)

    st.LOGIN_ATTEMPTS[ip] = []
    session_value, _csrf = au.make_session_value(username)
    response = JSONResponse({"ok": True})
    response.set_cookie(
        key=au.SESSION_COOKIE,
        value=session_value,
        httponly=True,
        secure=request.url.scheme == "https",
        samesite="strict",
        max_age=au.SESSION_MAX_AGE,
        path="/",
    )
    return response


async def logout_api(request: Request):
    response = JSONResponse({"ok": True})
    response.delete_cookie(au.SESSION_COOKIE, path="/")
    return response


async def snapshot(request: Request):
    rooms = list(st.ROOMS.values())
    pending = [st.REQUESTS[rid] for rid in st.PENDING if rid in st.REQUESTS]
    heading = [st.REQUESTS[rid] for rid in st.HEADING if rid in st.REQUESTS]
    free_count = sum(1 for r in rooms if r["status"] == "available")
    return JSONResponse({"rooms": rooms, "pending": pending, "heading": heading,
                         "free_count": free_count, "remain": free_count})


async def create_request(request: Request):
    body = await request.json()
    headcount = int(body.get("headcount", 1))
    status = body.get("status", "pending")
    seq_label = body.get("seq_label")
    req = st.build_request(headcount)
    if seq_label is not None:
        req["seq_label"] = str(seq_label).strip()
    if status == "pending":
        st.PENDING.append(req["id"])
    else:
        st.HEADING.append(req["id"])
    return JSONResponse({"ok": True})


async def update_seq_label(request: Request):
    body = await request.json()
    rid = body["requestId"]
    new_label = str(body.get("seq_label", "")).strip()
    if not new_label:
        return JSONResponse({"ok": False, "msg": "seq_label is required"})
    req = st.REQUESTS.get(rid)
    if not req:
        return JSONResponse({"ok": False, "msg": "request not found"})
    req["seq_label"] = new_label
    req["updated_at"] = st.now_str()
    return JSONResponse({"ok": True})


async def set_calling(request: Request):
    body = await request.json()
    rid = body["requestId"]
    calling = bool(body["calling"])
    if rid in st.REQUESTS:
        st.REQUESTS[rid]["calling"] = calling
        st.REQUESTS[rid]["updated_at"] = st.now_str()
    return JSONResponse({"ok": True})


async def cancel_request(request: Request):
    body = await request.json()
    rid = body["requestId"]
    req = st.REQUESTS.get(rid)
    if not req:
        return JSONResponse({"ok": False, "msg": "not found"})
    if rid in st.PENDING:
        st.PENDING.remove(rid)
    if rid in st.HEADING:
        st.HEADING.remove(rid)
    st.REQUESTS.pop(rid, None)
    room_name = "-"
    if req.get("room_id") and req["room_id"] in st.ROOMS:
        room_name = st.ROOMS[req["room_id"]]["name"]
    st.CANCELED.insert(0, {"id": rid, "seq": req["seq"], "headcount": req["headcount"],
                           "room_name": room_name, "updated_at": st.now_str()})
    return JSONResponse({"ok": True})


async def pending_to_heading(request: Request):
    body = await request.json()
    st.move_request(body["requestId"], st.PENDING, st.HEADING)
    return JSONResponse({"ok": True})


async def heading_to_pending_api(request: Request):
    body = await request.json()
    st.move_request(body["requestId"], st.HEADING, st.PENDING)
    return JSONResponse({"ok": True})


async def update_headcount(request: Request):
    body = await request.json()
    rid = body["requestId"]
    new_headcount = int(body.get("headcount", 1))
    if new_headcount < 1:
        return JSONResponse({"ok": False, "msg": "headcount must be >= 1"})
    req = st.REQUESTS.get(rid)
    if not req:
        return JSONResponse({"ok": False, "msg": "request not found"})
    req["headcount"] = new_headcount
    req["updated_at"] = st.now_str()
    room_id = req.get("room_id")
    if room_id and room_id in st.ROOMS:
        st.ROOMS[room_id]["currentHeadcount"] = new_headcount
    return JSONResponse({"ok": True})


async def assign_room(request: Request):
    body = await request.json()
    room_id = int(body["roomId"])
    request_id = body["requestId"]
    room = st.ROOMS.get(room_id)
    req = st.REQUESTS.get(request_id)
    if not room or not req:
        return JSONResponse({"ok": False, "msg": "not found"})
    if room["status"] != "available":
        return JSONResponse({"ok": False, "msg": "room not available"})
    room["status"] = "occupied"
    room["currentRequestId"] = request_id
    room["currentSeq"] = req.get("seq_label") or str(req["seq"])
    room["currentHeadcount"] = req["headcount"]
    base = st.ceil_to_5min(datetime.now(st.TZ))
    room["eta_at"] = (base + timedelta(minutes=90)).isoformat()
    req["room_id"] = room_id
    req["updated_at"] = st.now_str()
    if request_id in st.HEADING:
        st.HEADING.remove(request_id)
    return JSONResponse({"ok": True})


async def requeue_to_heading_api(request: Request):
    body = await request.json()
    request_id = body["requestId"]
    for room in st.ROOMS.values():
        if room["currentRequestId"] == request_id:
            room["currentRequestId"] = None
            room["currentSeq"] = None
            room["currentHeadcount"] = None
            room["status"] = "available"
            room["eta_at"] = None
    st.move_request(request_id, st.PENDING, st.HEADING)
    if request_id not in st.HEADING:
        st.HEADING.append(request_id)
    return JSONResponse({"ok": True})


async def checkout(request: Request):
    body = await request.json()
    request_id = body["requestId"]
    req = st.REQUESTS.get(request_id)
    if not req:
        return JSONResponse({"ok": False, "msg": "not found"})
    for room in st.ROOMS.values():
        if room["currentRequestId"] == request_id:
            room["currentRequestId"] = None
            room["currentSeq"] = None
            room["currentHeadcount"] = None
            room["status"] = "cleaning"
            base = st.ceil_to_5min(datetime.now(st.TZ))
            room["eta_at"] = (base + timedelta(minutes=15)).isoformat()
            st.HISTORY.insert(0, {"id": request_id, "seq": req["seq"], "headcount": req["headcount"],
                                  "room_name": room["name"], "updated_at": st.now_str()})
            break
    return JSONResponse({"ok": True})


async def save_eta_api(request: Request):
    body = await request.json()
    room_id = int(body["roomId"])
    hhmm = body["hhmm"]
    room = st.ROOMS.get(room_id)
    if not room:
        return JSONResponse({"ok": False, "msg": "room not found"})
    hour, minute = map(int, hhmm.split(":"))
    now = datetime.now(st.TZ)
    eta = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if eta < now:
        eta = eta + timedelta(days=1)
    room["eta_at"] = eta.isoformat()
    return JSONResponse({"ok": True})


async def clean_done_api(request: Request):
    body = await request.json()
    room_id = int(body["roomId"])
    room = st.ROOMS.get(room_id)
    if not room:
        return JSONResponse({"ok": False, "msg": "room not found"})
    room["status"] = "available"
    room["eta_at"] = None
    return JSONResponse({"ok": True})


async def get_history(request: Request):
    return JSONResponse(st.HISTORY[:50])


async def get_canceled_history(request: Request):
    return JSONResponse(st.CANCELED[:50])


async def get_rooms(request: Request):
    return JSONResponse(list(st.ROOMS.values()))


async def disable_room(request: Request):
    body = await request.json()
    room_id = int(body["roomId"])
    disabled = bool(body["disabled"])
    room = st.ROOMS.get(room_id)
    if not room:
        return JSONResponse({"ok": False, "msg": "room not found"})
    if disabled:
        room["status"] = "disabled"
        room["currentRequestId"] = None
        room["currentSeq"] = None
        room["currentHeadcount"] = None
        room["eta_at"] = None
    else:
        room["status"] = "available"
    return JSONResponse({"ok": True})


async def restore_from_history(request: Request):
    body = await request.json()
    original_id = body["requestId"]
    hist = next((h for h in st.HISTORY if h["id"] == original_id), None)
    if not hist:
        return JSONResponse({"ok": False, "msg": "not found"})
    req = st.build_request(hist["headcount"])
    req["seq"] = hist["seq"]
    req["seq_label"] = f"{req['seq']}"
    st.HEADING.append(req["id"])
    return JSONResponse({"ok": True})


async def cancel_restore(request: Request):
    body = await request.json()
    original_id = body["requestId"]
    target = body.get("target", "heading")
    hist = next((h for h in st.CANCELED if h["id"] == original_id), None)
    if not hist:
        return JSONResponse({"ok": False, "msg": "not found"})
    req = st.build_request(hist["headcount"])
    req["seq"] = hist["seq"]
    if target == "pending":
        st.PENDING.append(req["id"])
    else:
        st.HEADING.append(req["id"])
    return JSONResponse({"ok": True})


app = Starlette(
    routes=[
        Route("/", home, methods=["GET"]),
        Route("/api/login", login_api, methods=["POST"]),
        Route("/api/logout", logout_api, methods=["POST"]),
        Route("/api/snapshot", snapshot, methods=["GET"]),
        Route("/api/requests", create_request, methods=["POST"]),
        Route("/api/requests/update_seq_label", update_seq_label, methods=["POST"]),
        Route("/api/requests/calling", set_calling, methods=["POST"]),
        Route("/api/requests/cancel", cancel_request, methods=["POST"]),
        Route("/api/requests/heading", pending_to_heading, methods=["POST"]),
        Route("/api/requests/heading_to_pending", heading_to_pending_api, methods=["POST"]),
        Route("/api/requests/update_headcount", update_headcount, methods=["POST"]),
        Route("/api/requests/restore", restore_from_history, methods=["POST"]),
        Route("/api/assign", assign_room, methods=["POST"]),
        Route("/api/requeue_to_heading", requeue_to_heading_api, methods=["POST"]),
        Route("/api/checkout", checkout, methods=["POST"]),
        Route("/api/rooms/eta", save_eta_api, methods=["POST"]),
        Route("/api/rooms/clean_done", clean_done_api, methods=["POST"]),
        Route("/api/history", get_history, methods=["GET"]),
        Route("/api/canceled_history", get_canceled_history, methods=["GET"]),
        Route("/api/rooms", get_rooms, methods=["GET"]),
        Route("/api/rooms/disable", disable_room, methods=["POST"]),
        Route("/api/cancel_restore", cancel_restore, methods=["POST"]),
    ],
    middleware=[
        Middleware(SecurityMiddleware),
    ],
)
