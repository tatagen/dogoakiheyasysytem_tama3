# Cloudflare Workers Python エントリーポイント
# モジュールレベルで FastAPI を import しない → Cloudflare の検証フェーズを通過できる

_initialized = False
_asgi_app = None


async def _initialize():
    global _initialized, _asgi_app
    if _initialized:
        return

    # Pyodide 環境では micropip で PyPI パッケージをインストール
    try:
        import micropip
        await micropip.install([
            "fastapi",
            "starlette",
            "pydantic",
            "anyio",
            "sniffio",
            "typing_extensions",
        ])
    except ImportError:
        pass  # ローカル開発環境では不要

    # パッケージインストール後に FastAPI アプリを import
    import importlib
    importlib.invalidate_caches()
    import main_app
    _asgi_app = main_app.app
    _initialized = True


async def app(scope, receive, send):
    if scope["type"] in ("http", "websocket") and not _initialized:
        await _initialize()

    if _asgi_app is not None:
        await _asgi_app(scope, receive, send)
    elif scope["type"] == "http":
        await send({
            "type": "http.response.start",
            "status": 503,
            "headers": [[b"content-type", b"text/plain; charset=utf-8"]],
        })
        await send({"type": "http.response.body", "body": "起動中...".encode()})
