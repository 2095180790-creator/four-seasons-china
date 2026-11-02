"""Export the Python-rendered site as static files for GitHub Pages."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from app import SEASON_ORDER, STATIC_DIR, home_page, not_found_page, season_page


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "docs"


def replace_static_paths(markup: str, prefix: str) -> str:
    markup = markup.replace('href="/static/', f'href="{prefix}static/')
    markup = markup.replace('src="/static/', f'src="{prefix}static/')
    return markup


def build_home() -> str:
    markup = home_page()
    markup = re.sub(
        r'href="/season/([a-z]+)"',
        lambda match: f'href="{match.group(1)}/"',
        markup,
    )
    markup = markup.replace('href="/"', 'href="./"')
    return replace_static_paths(markup, "")


def build_season(slug: str) -> str:
    page = season_page(slug)
    if page is None:
        raise ValueError(f"Unknown season: {slug}")

    position = SEASON_ORDER.index(slug)
    previous_slug = SEASON_ORDER[(position - 1) % len(SEASON_ORDER)]
    next_slug = SEASON_ORDER[(position + 1) % len(SEASON_ORDER)]

    page = page.replace('data-home-url="/"', 'data-home-url="../"')
    page = page.replace(
        f'data-previous-url="/season/{previous_slug}"',
        f'data-previous-url="../{previous_slug}/"',
    )
    page = page.replace(
        f'data-next-url="/season/{next_slug}"',
        f'data-next-url="../{next_slug}/"',
    )
    page = re.sub(
        r'href="/season/([a-z]+)"',
        lambda match: f'href="../{match.group(1)}/"',
        page,
    )
    page = page.replace('href="/"', 'href="../"')
    return replace_static_paths(page, "../")


def build_not_found() -> str:
    markup = not_found_page()
    markup = markup.replace('href="/"', 'href="./"')
    return replace_static_paths(markup, "")


def export_static(output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    output_dir = output_dir.resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    shutil.copytree(STATIC_DIR, output_dir / "static")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / "index.html").write_text(build_home(), encoding="utf-8")
    (output_dir / "404.html").write_text(build_not_found(), encoding="utf-8")

    for slug in SEASON_ORDER:
        season_dir = output_dir / slug
        season_dir.mkdir()
        (season_dir / "index.html").write_text(
            build_season(slug),
            encoding="utf-8",
        )

    shutil.copy2(PROJECT_DIR / "Project_Report.pdf", output_dir / "Project_Report.pdf")


if __name__ == "__main__":
    export_static()
    print(DEFAULT_OUTPUT_DIR.resolve())
