from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REL = "nofollow sponsored noopener"


def load_json(path_str: str) -> dict:
    path = Path(path_str)
    if not path.is_absolute():
        path = ROOT / path
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_catalog(catalog_data: dict) -> dict[str, dict]:
    links = catalog_data.get("links", [])
    mapping: dict[str, dict] = {}
    for item in links:
        item_id = item.get("id")
        if item_id:
          mapping[item_id] = item
    return mapping


def build_cards(selection_data: dict, catalog: dict[str, dict]) -> list[dict]:
    cards = selection_data.get("affiliateSelection", {}).get("cards", [])
    rendered: list[dict] = []
    missing: list[str] = []
    for card in cards:
        link_id = card.get("linkId")
        link = catalog.get(link_id)
        if not link:
            missing.append(link_id or "(empty)")
            continue
        rendered.append(
            {
                "title": card["title"],
                "body": card["body"],
                "cta": card["cta"],
                "url": link["url"],
                "rel": card.get("rel", DEFAULT_REL),
                "secondary": bool(card.get("secondary", False)),
            }
        )
    if missing:
        raise SystemExit(f"台帳にない linkId があります: {', '.join(missing)}")
    return rendered


def render_js_object(cards: list[dict]) -> str:
    lines = ["["]
    for card in cards:
        lines.append("  {")
        lines.append(f'    "title": {json.dumps(card["title"], ensure_ascii=False)},')
        lines.append(f'    "body": {json.dumps(card["body"], ensure_ascii=False)},')
        lines.append(f'    "cta": {json.dumps(card["cta"], ensure_ascii=False)},')
        lines.append(f'    "url": {json.dumps(card["url"], ensure_ascii=False)},')
        lines.append(f'    "rel": {json.dumps(card["rel"], ensure_ascii=False)},')
        if card.get("secondary"):
            lines.append('    "secondary": "1"')
        else:
            lines[-1] = lines[-1].rstrip(",")
        lines.append("  },")
    if len(lines) > 1:
        lines[-1] = lines[-1].rstrip(",")
    lines.append("]")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="affiliateSelection から affiliate_cards を生成")
    parser.add_argument("selection", help="記事ごとの affiliateSelection JSON")
    parser.add_argument(
        "--catalog",
        default="data/affiliate-links.sample.json",
        help="楽天リンク台帳 JSON",
    )
    args = parser.parse_args()

    selection_data = load_json(args.selection)
    catalog_data = load_json(args.catalog)
    catalog = resolve_catalog(catalog_data)
    cards = build_cards(selection_data, catalog)
    print(render_js_object(cards))


if __name__ == "__main__":
    main()
