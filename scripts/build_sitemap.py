from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "assets" / "article-registry.js"
SITEMAP_PATH = ROOT / "sitemap.xml"
SITE_ORIGIN = "https://tabi.ayumi-biz.com"
JST = "+09:00"

STATIC_URLS = [
    (f"{SITE_ORIGIN}/", "1.0", "weekly", "2026-06-09"),
    (f"{SITE_ORIGIN}/about.html", "0.4", "monthly", "2026-06-09"),
    (f"{SITE_ORIGIN}/contact.html", "0.4", "monthly", "2026-06-09"),
    (f"{SITE_ORIGIN}/privacy.html", "0.4", "monthly", "2026-06-09"),
    (f"{SITE_ORIGIN}/ads.html", "0.4", "monthly", "2026-06-09"),
    (f"{SITE_ORIGIN}/finder.html", "0.9", "weekly", "2026-06-09"),
    (f"{SITE_ORIGIN}/articles/", "0.9", "weekly", "2026-06-09"),
]


def run_node(code: str) -> str:
    result = subprocess.run(
        ["node", "-e", code],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def load_registry_articles() -> list[dict]:
    node_code = dedent(
        f"""
        const path = {json.dumps(str(REGISTRY_PATH))};
        require(path);
        process.stdout.write(JSON.stringify(global.window.TABINOTE_ARTICLES));
        """
    ).strip()
    payload = run_node(
        "global.window = {};\n"
        + node_code
    )
    return json.loads(payload)


def is_published(article: dict, now: datetime) -> bool:
    status = article.get("status")
    if status == "published":
        return True
    if status == "scheduled":
        publish_at = article.get("publishAt")
        if not publish_at:
            return False
        publish_dt = datetime.fromisoformat(publish_at)
        return publish_dt <= now
    return False


def build_url_entry(loc: str, lastmod: str, changefreq: str, priority: str) -> str:
    return dedent(
        f"""\
        <url>
          <loc>{loc}</loc>
          <lastmod>{lastmod}</lastmod>
          <changefreq>{changefreq}</changefreq>
          <priority>{priority}</priority>
        </url>
        """
    ).strip()


def build_sitemap_xml() -> str:
    now = datetime.fromisoformat(f"{datetime.now().date()}T23:59:59{JST}")
    articles = load_registry_articles()
    visible_articles = [
        article
        for article in articles
        if is_published(article, now) and article.get("status") != "hidden"
    ]

    items = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    for loc, priority, freq, lastmod in STATIC_URLS:
        items.append(build_url_entry(loc, lastmod, freq, priority))

    for article in visible_articles:
        loc = f"{SITE_ORIGIN}{article['url']}"
        lastmod = article.get("updatedAt") or article.get("publishedAt") or "2026-06-09"
        items.append(build_url_entry(loc, lastmod, "monthly", "0.8"))

    items.append("</urlset>")
    return "\n".join(items) + "\n"


def main() -> None:
    SITEMAP_PATH.write_text(build_sitemap_xml(), encoding="utf-8")
    print(f"updated sitemap: {SITEMAP_PATH}")


if __name__ == "__main__":
    main()
