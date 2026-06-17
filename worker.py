from js import Response, Headers

_app = None
_ready = False


async def _ensure_app():
    global _app, _ready
    if _ready:
        return
    import micropip
    await micropip.install([
        "fastapi",
        "starlette",
        "pydantic",
        "anyio",
        "sniffio",
        "typing_extensions",
    ])
    import importlib
    importlib.invalidate_caches()
    import main_app
    _app = main_app.app
    _ready = True


async def on_fetch(request, env):
    await _ensure_app()
    return await _run_asgi(request, env)


async def _run_asgi(js_req, env):
    from urllib.parse import urlparse

    url_str = str(js_req.url)
    parsed = urlparse(url_str)
    method = str(js_req.method).upper()

    # Collect request headers as ASGI byte pairs
    raw_headers = []
    try:
        for pair in js_req.headers.entries():
            raw_headers.append((str(pair[0]).lower().encode(), str(pair[1]).encode()))
    except Exception:
        pass

    # Read request body (skip for GET / HEAD)
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
    return Response.new(bytes(resp_body), status=status_code[0], headers=headers_obj)
