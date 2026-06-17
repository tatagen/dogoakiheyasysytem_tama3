from js import Response, Headers

_app = None
_ready = False
_init_error = None


async def _ensure_app():
    global _app, _ready, _init_error
    if _ready:
        return
    try:
        import importlib
        importlib.invalidate_caches()
        import main_app
        _app = main_app.app
    except Exception:
        import traceback
        _init_error = traceback.format_exc()
    _ready = True


def _err_response(msg: str, status: int = 500):
    h = Headers.new([["content-type", "text/plain; charset=utf-8"]])
    return Response.new(msg, status=status, headers=h)


async def on_fetch(request, env):
    await _ensure_app()

    if _init_error:
        return _err_response(f"[init error]\n{_init_error}")

    if _app is None:
        return _err_response("app failed to load")

    try:
        return await _run_asgi(request, env)
    except Exception:
        import traceback
        return _err_response(f"[runtime error]\n{traceback.format_exc()}")


async def _run_asgi(js_req, env):
    from urllib.parse import urlparse

    url_str = str(js_req.url)
    parsed = urlparse(url_str)
    method = str(js_req.method).upper()

    raw_headers = []
    try:
        for pair in js_req.headers.entries():
            raw_headers.append((str(pair[0]).lower().encode(), str(pair[1]).encode()))
    except Exception:
        pass

    body = b""
    if method not in ("GET", "HEAD"):
        try:
            buf = await js_req.arrayBuffer()
            body = bytes(buf)
        except Exception:
            pass

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "path": parsed.path or "/",
        "query_string": (parsed.query or "").encode(),
        "root_path": "",
        "scheme": parsed.scheme,
        "server": (parsed.hostname or "localhost", parsed.port or (443 if parsed.scheme == "https" else 80)),
        "headers": raw_headers,
        "cloudflare.workers.env": env,
        "env": env,
    }

    body_consumed = [False]

    async def receive():
        if not body_consumed[0]:
            body_consumed[0] = True
            return {"type": "http.request", "body": body, "more_body": False}
        return {"type": "http.disconnect"}

    status_code = [200]
    resp_header_pairs = []
    resp_body = bytearray()

    async def send(message):
        if message["type"] == "http.response.start":
            status_code[0] = message["status"]
            for k, v in message.get("headers", []):
                resp_header_pairs.append((k.decode("latin-1"), v.decode("latin-1")))
        elif message["type"] == "http.response.body":
            chunk = message.get("body", b"")
            if chunk:
                resp_body.extend(chunk)

    await _app(scope, receive, send)

    headers_obj = Headers.new(resp_header_pairs)
    # Pass decoded string — Pyodide converts raw bytes to repr "b'...'" otherwise
    body_str = resp_body.decode("utf-8", errors="replace")
    return Response.new(body_str, status=status_code[0], headers=headers_obj)
