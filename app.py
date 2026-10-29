"""A dependency-free Four Seasons website using only Python's standard library."""

from __future__ import annotations

import html
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

SEASON_ORDER = ("spring", "summer", "autumn", "winter")

SEASONS = {
    "spring": {
        "slug": "spring",
        "number": "01",
        "name": "Spring",
        "location": "Kunming, Yunnan",
        "short_location": "Kunming",
        "image": "images/spring-kunming.jpg",
        "image_alt": "Pink cherry blossoms framing a traditional building in Kunming",
        "quote": "The earth laughs in flowers.",
        "author": "Ralph Waldo Emerson",
        "accent": "#d76e8d",
        "wash": "#f6e6eb",
    },
    "summer": {
        "slug": "summer",
        "number": "02",
        "name": "Summer",
        "location": "Hainan",
        "short_location": "Hainan",
        "image": "images/summer-hainan.webp",
        "image_alt": "Tall palm trees and a bright blue sky beside the coast in Hainan",
        "quote": "Deep summer is when laziness finds respectability.",
        "author": "Sam Keen",
        "accent": "#138eb9",
        "wash": "#dff3f7",
    },
    "autumn": {
        "slug": "autumn",
        "number": "03",
        "name": "Autumn",
        "location": "Jiuzhaigou, Sichuan",
        "short_location": "Jiuzhaigou",
        "image": "images/autumn-jiuzhaigou.png",
        "image_alt": "Golden autumn trees reflected in a clear turquoise lake in Jiuzhaigou",
        "quote": "Autumn is a second spring when every leaf is a flower.",
        "author": "Albert Camus",
        "accent": "#c86b2c",
        "wash": "#f7e9d7",
    },
    "winter": {
        "slug": "winter",
        "number": "04",
        "name": "Winter",
        "location": "Tibet",
        "short_location": "Tibet",
        "image": "images/winter-tibet.png",
        "image_alt": "Golden morning light on a snow-covered mountain reflected in still water",
        "quote": "If winter comes, can spring be far behind?",
        "author": "Percy Bysshe Shelley",
        "accent": "#578aab",
        "wash": "#e3edf2",
    },
}


def escape(value: object) -> str:
    """Escape text before inserting it into an HTML template."""
    return html.escape(str(value), quote=True)


def render_template(template_name: str, values: dict[str, object]) -> str:
    """Load an HTML file and replace {{PLACEHOLDERS}} with supplied values."""
    template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    return template


def mini_navigation() -> str:
    links = []
    for slug in SEASON_ORDER:
        season = SEASONS[slug]
        links.append(
            f'<a href="/season/{season["slug"]}">'
            f'<span>{escape(season["number"])}</span>{escape(season["name"])}</a>'
        )
    return "\n".join(links)


def season_cards() -> str:
    cards = []
    for slug in SEASON_ORDER:
        season = SEASONS[slug]
        loading = "eager" if season["number"] in ("01", "02") else "lazy"
        cards.append(
            f"""
            <a class="season-card"
               href="/season/{season['slug']}"
               style="--accent: {season['accent']}; --wash: {season['wash']};"
               data-season-card
               data-page-transition
               aria-label="Explore {escape(season['name'])} in {escape(season['location'])}">
              <span class="card-image-wrap">
                <img src="/static/{escape(season['image'])}"
                     alt="{escape(season['image_alt'])}"
                     loading="{loading}">
              </span>
              <span class="card-wash" aria-hidden="true"></span>
              <span class="card-number">{escape(season['number'])}</span>
              <span class="card-copy">
                <span class="card-location">{escape(season['location'])}</span>
                <span class="card-title">{escape(season['name'])}</span>
              </span>
              <span class="card-arrow" aria-hidden="true">↗</span>
            </a>
            """
        )
    return "\n".join(cards)


def home_page() -> str:
    return render_template(
        "index.html",
        {
            "MINI_NAV": mini_navigation(),
            "SEASON_CARDS": season_cards(),
        },
    )


def season_page(slug: str) -> str | None:
    selected = SEASONS.get(slug)
    if selected is None:
        return None

    position = SEASON_ORDER.index(slug)
    previous = SEASONS[SEASON_ORDER[(position - 1) % len(SEASON_ORDER)]]
    following = SEASONS[SEASON_ORDER[(position + 1) % len(SEASON_ORDER)]]

    return render_template(
        "season.html",
        {
            "PAGE_TITLE": escape(
                f"{selected['name']} in {selected['short_location']} | "
                "Four Seasons Across China"
            ),
            "DESCRIPTION": escape(
                f"{selected['quote']} Explore {selected['name']} in "
                f"{selected['location']}."
            ),
            "SLUG": selected["slug"],
            "NAME": escape(selected["name"]),
            "LOCATION": escape(selected["location"]),
            "SHORT_LOCATION": escape(selected["short_location"]),
            "IMAGE": escape(selected["image"]),
            "IMAGE_ALT": escape(selected["image_alt"]),
            "QUOTE": escape(selected["quote"]),
            "AUTHOR": escape(selected["author"]),
            "NUMBER": escape(selected["number"]),
            "ACCENT": escape(selected["accent"]),
            "WASH": escape(selected["wash"]),
            "PREVIOUS_SLUG": previous["slug"],
            "PREVIOUS_NAME": escape(previous["name"]),
            "NEXT_SLUG": following["slug"],
            "NEXT_NAME": escape(following["name"]),
        },
    )


def not_found_page() -> str:
    return render_template("404.html", {})


def season_api_data() -> dict[str, object]:
    public_fields = ("slug", "number", "name", "location", "quote", "author")
    seasons = [
        {field: SEASONS[slug][field] for field in public_fields}
        for slug in SEASON_ORDER
    ]
    return {"seasons": seasons}


class SiteHandler(BaseHTTPRequestHandler):
    server_version = "FourSeasonsPython/1.0"

    def do_GET(self) -> None:
        self.handle_request(send_body=True)

    def do_HEAD(self) -> None:
        self.handle_request(send_body=False)

    def handle_request(self, send_body: bool) -> None:
        path = unquote(urlparse(self.path).path)

        if path == "/":
            self.send_page(home_page(), send_body)
        elif path.startswith("/season/"):
            page = season_page(path.removeprefix("/season/").strip("/"))
            if page is None:
                self.send_page(not_found_page(), send_body, status=404)
            else:
                self.send_page(page, send_body)
        elif path == "/api/seasons":
            payload = json.dumps(
                season_api_data(),
                ensure_ascii=False,
                indent=2,
            ).encode("utf-8")
            self.send_bytes(payload, "application/json; charset=utf-8", send_body)
        elif path == "/health":
            self.send_bytes(b'{"status": "ok"}', "application/json", send_body)
        elif path.startswith("/static/"):
            self.send_static_file(path.removeprefix("/static/"), send_body)
        else:
            self.send_page(not_found_page(), send_body, status=404)

    def send_page(self, content: str, send_body: bool, status: int = 200) -> None:
        self.send_bytes(content.encode("utf-8"), "text/html; charset=utf-8", send_body, status)

    def send_bytes(
        self,
        content: bytes,
        content_type: str,
        send_body: bool,
        status: int = 200,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if send_body:
            self.wfile.write(content)

    def send_static_file(self, relative_path: str, send_body: bool) -> None:
        requested = (STATIC_DIR / relative_path).resolve()

        if not requested.is_relative_to(STATIC_DIR.resolve()) or not requested.is_file():
            self.send_page(not_found_page(), send_body, status=404)
            return

        content_type = mimetypes.guess_type(requested.name)[0] or "application/octet-stream"
        content = requested.read_bytes()
        self.send_bytes(content, content_type, send_body)

    def log_message(self, format_string: str, *args: object) -> None:
        print(f"{self.address_string()} - {format_string % args}")


def run_server() -> None:
    port = int(os.environ.get("PORT", "5000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), SiteHandler)
    print(f"Four Seasons is running at http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
