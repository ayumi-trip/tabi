from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

DEFAULTS = {
    "dateLabel": "2026.06",
    "status": "review",
    "publishAt": "",
    "publishedAt": "",
    "updatedAt": "",
    "imageStatus": "none",
    "rewriteStatus": "review",
    "factCheckStatus": "pending",
    "qualityChecked": False,
    "topFeature": False,
    "noteFeature": False,
}

REQUIRED_KEYS = [
    "slug",
    "title",
    "description",
    "url",
    "area",
    "region",
    "tags",
    "cardLabels",
    "image",
]


def quote(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def load_entry(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    entry = {**DEFAULTS, **data}
    missing = [key for key in REQUIRED_KEYS if not entry.get(key)]
    if missing:
        raise SystemExit(f"必須項目が不足しています: {', '.join(missing)}")
    if not isinstance(entry["tags"], list) or not isinstance(entry["cardLabels"], list):
        raise SystemExit("tags と cardLabels は配列で指定してください。")
    return entry


def render_entry(entry: dict) -> str:
    key_order = [
        "slug",
        "title",
        "description",
        "url",
        "area",
        "region",
        "tags",
        "cardLabels",
        "image",
        "dateLabel",
        "status",
        "publishAt",
        "publishedAt",
        "updatedAt",
        "imageStatus",
        "rewriteStatus",
        "factCheckStatus",
        "qualityChecked",
        "topFeature",
        "noteFeature",
    ]
    lines = ["{"]
    for key in key_order:
        if key not in entry:
            continue
        lines.append(f"  {key}: {quote(entry[key])},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="article-registry.js に追加するオブジェクトを生成")
    parser.add_argument("input", help="JSON テンプレファイル")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    entry = load_entry(input_path)
    print(render_entry(entry))


if __name__ == "__main__":
    main()
