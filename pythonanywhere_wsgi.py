"""WSGI entry point for deploying the website on PythonAnywhere."""

from __future__ import annotations

import json
import mimetypes
from urllib.parse import unquote

from app import (
    STATIC_DIR,
    home_page,
    not_found_page,
    season_api_data,
    season_page,
)


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = unquote(environ.get("PATH_INFO", "/"))

    if method not in ("GET", "HEAD"):
        body = not_found_page().encode("utf-8")
        headers = [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Allow", "GET, HEAD"),
        ]
        start_response("405 Method Not Allowed", headers)
        return [body]

    status = "200 OK"
    content_type = "text/html; charset=utf-8"

    if path == "/":
        body = home_page().encode("utf-8")
    elif path.startswith("/season/"):
        page = season_page(path.removeprefix("/season/").strip("/"))
        if page is None:
            status = "404 Not Found"
            body = not_found_page().encode("utf-8")
        else:
            body = page.encode("utf-8")
    elif path == "/api/seasons":
        body = json.dumps(
            season_api_data(),
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8")
        content_type = "application/json; charset=utf-8"
    elif path == "/health":
        body = b'{"status": "ok"}'
        content_type = "application/json"
    elif path.startswith("/static/"):
        requested = (STATIC_DIR / path.removeprefix("/static/")).resolve()
        static_root = STATIC_DIR.resolve()

        if not requested.is_relative_to(static_root) or not requested.is_file():
            status = "404 Not Found"
            body = not_found_page().encode("utf-8")
        else:
            body = requested.read_bytes()
            content_type = (
                mimetypes.guess_type(requested.name)[0]
                or "application/octet-stream"
            )
    else:
        status = "404 Not Found"
        body = not_found_page().encode("utf-8")

    headers = [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
        ("X-Content-Type-Options", "nosniff"),
    ]
    start_response(status, headers)
    return [body] if method != "HEAD" else [b""]
