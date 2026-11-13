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
        "intro": (
            "Known as the City of Eternal Spring, Kunming fills with cherry "
            "blossoms and camellias when the weather turns mild."
        ),
        "best_time": "March to May",
        "activities": [
            {
                "title": "Cherry Blossom Walk at Yuantong Temple",
                "description": "Wander beneath the pink blossoms and listen to the temple bells before the crowds arrive.",
            },
            {
                "title": "Boating on Green Lake",
                "description": "Rent a small boat, drift past the willows, and watch the spring flowers reflected in the water.",
            },
            {
                "title": "Camellia Picnic",
                "description": "Spread a blanket among Kunming's camellias and share fruit and tea in the mild afternoon sun.",
            },
            {
                "title": "Stone Forest Day Trip",
                "description": "Walk between the limestone rock formations that rise from the ground like a forest of stone.",
            },
            {
                "title": "Birdwatching at Dianchi Lake",
                "description": "Follow the lakeside paths and watch the birds that gather on the wide water.",
            },
            {
                "title": "Visit the Dounan Flower Market",
                "description": "Browse one of the largest flower markets in Asia and pick a bunch of fresh blossoms.",
            },
        ],
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
        "intro": (
            "China's tropical island, Hainan turns long warm days and a blue "
            "coast into a long, easy summer."
        ),
        "best_time": "June to August",
        "activities": [
            {
                "title": "Coral Coast Snorkelling",
                "description": "Float over the coral reef, look for colourful fish, and let the warm sea carry you along.",
            },
            {
                "title": "Sunset Ride on the Coastal Road",
                "description": "Cycle beside the ocean as the sun drops and the sky turns orange and pink.",
            },
            {
                "title": "Fresh Coconut by the Shore",
                "description": "Find a palm-tree stand, drink the water straight from a coconut, and rest in the shade.",
            },
            {
                "title": "Surfing at Riyue Bay",
                "description": "Learn to catch gentle waves on a wide, sandy bay with a rented board.",
            },
            {
                "title": "Rainforest Walk in Wuzhishan",
                "description": "Trek through the green tropical forest and listen for birds among the tall trees.",
            },
            {
                "title": "Beach Volleyball at Sunset",
                "description": "Join a game on the sand and play until the sky turns orange over the water.",
            },
        ],
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
        "intro": (
            "In October the valleys around Jiuzhaigou turn gold and red, and "
            "the still lakes reflect the forest like a mirror."
        ),
        "best_time": "September to November",
        "activities": [
            {
                "title": "Boardwalk Walk Between the Lakes",
                "description": "Follow the wooden paths past turquoise water while red and gold leaves drift down from the trees.",
            },
            {
                "title": "Photograph the Golden Reflections",
                "description": "Frame the coloured forest mirrored in the still lakes, especially in the soft morning light.",
            },
            {
                "title": "Waterfall Listening",
                "description": "Stand close to the falling water, hear the valley echo, and feel the cool spray in the autumn air.",
            },
            {
                "title": "View Nuorilang Waterfall",
                "description": "Watch the wide curtain of water that spreads across the valley in one of Jiuzhaigou's best-known views.",
            },
            {
                "title": "Walk to Long Lake",
                "description": "Climb slowly to the highest lake, where the clear water lies surrounded by quiet peaks.",
            },
            {
                "title": "Taste Local Tibetan Food",
                "description": "Warm up after the trails with butter tea, yak milk yogurt, and fresh flatbread.",
            },
        ],
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
        "intro": (
            "High in Tibet, winter brings clear air, bright sun and cold "
            "mornings that turn the mountains golden."
        ),
        "best_time": "December to February",
        "activities": [
            {
                "title": "Golden Sunrise over the Mountains",
                "description": "Wake early and watch the first light turn the snow-covered peaks a deep golden orange.",
            },
            {
                "title": "Pilgrimage Walk in the Old Quarter",
                "description": "Walk slowly through the historic streets, follow the local rhythm, and see the prayer flags in the wind.",
            },
            {
                "title": "Butter Tea on a Rooftop",
                "description": "Warm your hands around a cup of butter tea and look out over the winter rooftops toward the mountains.",
            },
            {
                "title": "Visit the Potala Palace",
                "description": "Climb the white and red palace on the hill and see its halls in the clear winter light.",
            },
            {
                "title": "Browse the Local Market",
                "description": "Look for warm yak-wool scarves and hand-made souvenirs among the market stalls.",
            },
            {
                "title": "Evening Prayer at Jokhang Temple",
                "description": "Watch the butter lamps glow and see pilgrims walk around the temple as evening falls.",
            },
        ],
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
    links.append('<a class="mini-nav-compare" href="/compare">Compare</a>')
    links.append('<a class="mini-nav-compare" href="/memories">Memories</a>')
    return "\n".join(links)


def image_variants(image: str) -> tuple[str, str]:
    stem = image.rsplit(".", 1)[0]
    return f"{stem}.webp", f"{stem}-small.webp"


def picture_markup(
    image: str,
    alt: str,
    sizes: str,
    loading: str = "",
    fetchpriority: str = "",
) -> str:
    webp, webp_small = image_variants(image)
    source = (
        f'<source type="image/webp" '
        f'srcset="/static/{escape(webp)} 1800w, /static/{escape(webp_small)} 900w" '
        f'sizes="{sizes}">'
    )
    image_tag = (
        f'<img src="/static/{escape(image)}" alt="{escape(alt)}" '
        f'{loading}{fetchpriority}>'
    )
    return f"<picture>{source}{image_tag}</picture>"


def activities_markup(activities: list[dict[str, str]], slug: str) -> str:
    items = []
    for index, activity in enumerate(activities, start=1):
        items.append(
            f'<li><label class="activity-item">'
            f'<input class="activity-checkbox" type="checkbox" data-activity>'
            f'<span class="activity-marker" aria-hidden="true"></span>'
            f'<span class="activity-content">'
            f'<strong class="activity-title">{escape(activity["title"])}</strong>'
            f'<span class="activity-text">{escape(activity["description"])}</span>'
            f'</span></label></li>'
        )
    return (
        f'<div class="season-activities" data-activity-list data-slug="{slug}" data-reveal>'
        '<div class="activities-heading">'
        '<h2 class="activities-title">Things to do here</h2>'
        '<span class="activity-progress"><span data-activity-count>0</span> / '
        f'{len(activities)}</span>'
        "</div>"
        '<ul class="season-activities-list">' + "".join(items) + "</ul></div>"
    )


def season_cards() -> str:
    cards = []
    for slug in SEASON_ORDER:
        season = SEASONS[slug]
        loading = "eager" if season["number"] in ("01", "02") else "lazy"
        loading_attr = f'loading="{loading}"' if loading else ""
        cards.append(
            f"""
            <a class="season-card"
               href="/season/{season['slug']}"
               style="--accent: {season['accent']}; --wash: {season['wash']};"
               data-season-card
               data-season="{season['slug']}"
               data-name="{escape(season['name'])}"
               data-location="{escape(season['location'])}"
               data-page-transition
               aria-label="Explore {escape(season['name'])} in {escape(season['location'])}">
              <span class="card-image-wrap">
                {picture_markup(
                    season["image"],
                    season["image_alt"],
                    "(max-width: 760px) 100vw, 25vw",
                    loading=loading_attr,
                )}
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
            "ACTIVITIES": activities_markup(selected["activities"], selected["slug"]),
            "NUMBER": escape(selected["number"]),
            "ACCENT": escape(selected["accent"]),
            "WASH": escape(selected["wash"]),
            "INTRO": escape(selected["intro"]),
            "BEST_TIME": escape(selected["best_time"]),
            "PICTURE": picture_markup(
                selected["image"],
                selected["image_alt"],
                "(max-width: 760px) 100vw, 55vw",
                fetchpriority='fetchpriority="high"',
            ),
            "PREVIOUS_SLUG": previous["slug"],
            "PREVIOUS_NAME": escape(previous["name"]),
            "NEXT_SLUG": following["slug"],
            "NEXT_NAME": escape(following["name"]),
        },
    )


def not_found_page() -> str:
    return render_template("404.html", {})


def compare_page() -> str:
    return render_template(
        "compare.html",
        {
            "MINI_NAV": mini_navigation(),
            "COMPARE_TABLE": compare_table_markup(),
        },
    )


def memories_page() -> str:
    return render_template("memories.html", {"MINI_NAV": mini_navigation()})


def compare_table_markup() -> str:
    rows = []
    for slug in SEASON_ORDER:
        season = SEASONS[slug]
        activity_titles = " · ".join(
            activity["title"] for activity in season["activities"]
        )
        rows.append(
            "<tr>"
            f'<th scope="row">{escape(season["name"])}</th>'
            f'<td>{escape(season["location"])}</td>'
            f'<td>{escape(season["best_time"])}</td>'
            f'<td>{escape(season["intro"])}</td>'
            f'<td>{escape(activity_titles)}</td>'
            "</tr>"
        )
    body = "".join(rows)
    return (
        '<div class="compare-scroll"><table class="compare-table">'
        "<thead><tr>"
        "<th>Season</th><th>Location</th><th>Best time</th>"
        "<th>What to expect</th><th>Things to do</th>"
        "</tr></thead><tbody>"
        f"{body}</tbody></table></div>"
    )


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
        elif path == "/compare":
            self.send_page(compare_page(), send_body)
        elif path == "/memories":
            self.send_page(memories_page(), send_body)
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
