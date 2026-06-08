from __future__ import annotations

import html
import json
import re
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "articles"
INDEX_PATH = ROOT / "index.html"
SITEMAP_PATH = ROOT / "sitemap.xml"


def write_text_utf8_bom(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8-sig")


ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | tabinote</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="author" content="tabinote編集部">
  <meta name="theme-color" content="#1f5f8f">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="tabinote">
  <meta property="og:title" content="{title} | tabinote">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{image}">
  <meta property="og:locale" content="ja_JP">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | tabinote">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&family=Shippori+Mincho:wght@500;600;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">
    {json_ld}
  </script>
  <style>
    :root {{
      color-scheme: light;
      --ink: #111827;
      --sub: #4b5563;
      --muted: #7b8794;
      --line: #e5e7eb;
      --paper: #fbfaf7;
      --white: #fff;
      --teal: #1f5f8f;
      --teal-2: #eef6fb;
      --deep: #14191c;
      --r: 18px;
      --shadow: 0 18px 44px rgba(15, 23, 42, .08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Noto Sans JP", sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.85;
    }}
    a {{ color: inherit; text-decoration: none; }}
    .site-header {{
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
      padding: 0 clamp(18px, 4vw, 52px);
      background: rgba(255, 255, 255, .92);
      border-bottom: 1px solid rgba(17, 17, 17, .08);
      backdrop-filter: blur(14px);
    }}
    .brand-name {{
      font-family: "Shippori Mincho", serif;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: .04em;
    }}
    .brand-name span {{ color: var(--teal); }}
    .nav-links {{
      display: flex;
      gap: 22px;
      color: var(--sub);
      font-size: 13px;
      font-weight: 700;
    }}
    .article-hero {{
      min-height: 420px;
      display: grid;
      align-items: end;
      background:
        linear-gradient(180deg, rgba(17, 24, 39, .08), rgba(17, 24, 39, .62)),
        url("{image}") center/cover;
      color: var(--white);
    }}
    .hero-inner {{
      width: min(1040px, 100%);
      margin: 0 auto;
      padding: clamp(72px, 12vw, 120px) clamp(18px, 4vw, 32px) clamp(40px, 6vw, 72px);
    }}
    .article-label {{
      display: inline-flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }}
    .article-label span {{
      border-radius: 999px;
      padding: 6px 10px;
      background: rgba(255, 255, 255, .88);
      color: var(--teal);
      font-size: 12px;
      font-weight: 800;
    }}
    h1, h2, h3 {{
      font-family: "Shippori Mincho", serif;
      line-height: 1.35;
      letter-spacing: .02em;
    }}
    h1 {{
      max-width: 880px;
      margin: 0;
      font-size: clamp(34px, 5.5vw, 58px);
    }}
    .lead {{
      max-width: 760px;
      margin: 20px 0 0;
      color: rgba(255, 255, 255, .9);
      font-size: 15px;
    }}
    .article-wrap {{
      width: min(1040px, 100%);
      margin: 0 auto;
      padding: clamp(36px, 6vw, 72px) clamp(18px, 4vw, 32px);
      display: grid;
      grid-template-columns: minmax(0, 1fr) 280px;
      gap: clamp(28px, 5vw, 52px);
      align-items: start;
    }}
    .article-main {{
      display: grid;
      gap: 30px;
    }}
    .content-box,
    .side-box {{
      border: 1px solid var(--line);
      border-radius: var(--r);
      background: var(--white);
      box-shadow: var(--shadow);
    }}
    .content-box {{
      padding: clamp(24px, 4vw, 42px);
    }}
    .content-box h2 {{
      margin: 0 0 14px;
      font-size: clamp(24px, 3vw, 34px);
    }}
    .content-box h3 {{
      margin: 26px 0 10px;
      font-size: 22px;
    }}
    .content-box p {{
      margin: 0 0 16px;
      color: var(--sub);
    }}
    .content-box ul,
    .content-box ol {{
      margin: 0;
      padding-left: 1.3em;
      color: var(--sub);
    }}
    .content-box li + li {{ margin-top: 8px; }}
    .summary-list {{
      display: grid;
      gap: 10px;
      margin: 0;
      padding: 0;
      list-style: none;
    }}
    .summary-list li {{
      border-left: 3px solid var(--teal);
      padding: 8px 0 8px 14px;
      background: #f8fbfd;
    }}
    .info-card {{
      display: grid;
      gap: 10px;
      margin-top: 16px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: #fbfdff;
    }}
    .info-card h3 {{
      margin: 0;
      font-size: 21px;
    }}
    .ranking-grid {{
      display: grid;
      gap: 16px;
      margin-top: 18px;
    }}
    .ranking-card {{
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 18px;
      background: #fff;
    }}
    .ranking-card .rank {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 32px;
      height: 32px;
      margin-bottom: 10px;
      border-radius: 999px;
      background: var(--teal);
      color: var(--white);
      font-size: 13px;
      font-weight: 800;
    }}
    .ranking-card p:last-child {{ margin-bottom: 0; }}
    .hotel-contact {{
      display: grid;
      gap: 6px;
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--line);
      color: var(--sub);
      font-size: 13px;
      line-height: 1.7;
    }}
    .hotel-contact p {{
      margin: 0;
    }}
    .hotel-contact b {{
      color: var(--ink);
      font-weight: 700;
    }}
    .hotel-contact a {{
      color: var(--teal);
      text-decoration: underline;
      text-underline-offset: 3px;
    }}
    .affiliate-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 18px;
    }}
    .affiliate-card {{
      display: grid;
      gap: 8px;
      min-height: 180px;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 18px;
      background: var(--white);
    }}
    .affiliate-card b {{
      font-size: 16px;
    }}
    .affiliate-card p {{
      margin: 0;
      font-size: 13px;
    }}
    .button {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: fit-content;
      border-radius: 999px;
      padding: 10px 16px;
      background: var(--deep);
      color: var(--white);
      font-size: 13px;
      font-weight: 800;
    }}
    .button.secondary {{
      border: 1px solid var(--line);
      background: var(--white);
      color: var(--teal);
    }}
    .side-box {{
      position: sticky;
      top: 84px;
      padding: 18px;
    }}
    .side-box h2 {{
      margin: 0 0 12px;
      font-size: 18px;
    }}
    .side-box a {{
      display: block;
      padding: 9px 0;
      border-bottom: 1px solid var(--line);
      color: var(--sub);
      font-size: 13px;
    }}
    .article-dates {{
      display: grid;
      gap: 6px;
      margin-top: 16px;
      padding-top: 14px;
      border-top: 1px solid var(--line);
      color: var(--muted);
      font-size: 12px;
    }}
    .article-dates span {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
    }}
    .article-dates b {{
      color: var(--sub);
      font-weight: 700;
    }}
    .source-list a {{
      color: var(--teal);
      text-decoration: underline;
      text-underline-offset: 3px;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      gap: 24px;
      padding: 28px clamp(18px, 4vw, 52px);
      border-top: 1px solid var(--line);
      color: var(--muted);
      font-size: 12px;
      background: #f8f9f9;
    }}
    .footer-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
    }}
    @media (max-width: 860px) {{
      .article-wrap {{ grid-template-columns: 1fr; }}
      .affiliate-grid {{ grid-template-columns: 1fr; }}
      .side-box {{ position: static; }}
      .nav-links {{ display: none; }}
    }}
  </style>
</head>
<body>
  <header class="site-header">
    <a href="/" class="brand" aria-label="tabinote トップ">
      <span class="brand-name">tabi<span>note</span></span>
    </a>
    <nav class="nav-links" aria-label="メインメニュー">
      <a href="/#articles">記事を探す</a>
      <a href="/finder.html">旅先レコメンド</a>
    </nav>
  </header>

  <main>
    <section class="article-hero">
      <div class="hero-inner">
        <div class="article-label">
          {hero_labels}
        </div>
        <h1>{title}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>

    <div class="article-wrap">
      <article class="article-main">
        {article_sections}
      </article>

      <aside class="side-box" aria-label="記事目次">
        <h2>この記事の内容</h2>
        {toc_links}
        <div class="article-dates">
          <span><b>公開日</b>{published}</span>
          <span><b>更新日</b>{updated}</span>
        </div>
      </aside>
    </div>
  </main>

  <footer class="footer">
    <div>© 2026 tabinote. 当サイトはPR・アフィリエイト広告を利用する場合があります。</div>
    <div class="footer-links">
      <a href="/about.html">運営者情報</a>
      <a href="/contact.html">お問い合わせ</a>
      <a href="/privacy.html">プライバシーポリシー</a>
      <a href="/ads.html">広告掲載について</a>
    </div>
    <a href="/">トップへ戻る</a>
  </footer>
</body>
</html>
"""


def p(text: str) -> str:
    return f"<p>{html.escape(text)}</p>"


def ul(items: list[str], klass: str | None = None) -> str:
    class_attr = f' class="{klass}"' if klass else ""
    inner = "\n".join(f"  <li>{html.escape(item)}</li>" for item in items)
    return f"<ul{class_attr}>\n{inner}\n</ul>"


def ol(items: list[str]) -> str:
    inner = "\n".join(f"  <li>{html.escape(item)}</li>" for item in items)
    return f"<ol>\n{inner}\n</ol>"


def section(section_id: str, title: str, body_html: str) -> str:
    return dedent(
        f"""\
        <section class="content-box" id="{section_id}">
          <h2>{html.escape(title)}</h2>
          {body_html}
        </section>
        """
    ).strip()


def info_card(title: str, paragraphs: list[str], bullets: list[str] | None = None) -> str:
    parts = [f"<h3>{html.escape(title)}</h3>"]
    parts.extend(p(text) for text in paragraphs)
    if bullets:
        parts.append(ul(bullets))
    return '<div class="info-card">\n' + "\n".join(parts) + "\n</div>"


def ranking_cards(cards: list[dict[str, object]]) -> str:
    blocks: list[str] = []
    for i, card in enumerate(cards, start=1):
        body = [f'<div class="rank">{i}</div>', f"<h3>{html.escape(str(card['name']))}</h3>"]
        for para in card["paragraphs"]:  # type: ignore[index]
            body.append(p(str(para)))
        body.append(ul([str(item) for item in card["bullets"]]))  # type: ignore[index]
        meta: list[str] = []
        if card.get("address"):
            meta.append(f'<p><b>住所：</b>{html.escape(str(card["address"]))}</p>')
        if card.get("phone"):
            meta.append(f'<p><b>電話番号：</b>{html.escape(str(card["phone"]))}</p>')
            meta.append(
                f'<p><b>公式サイト：</b><a href="{html.escape(str(card["url"]))}" target="_blank" rel="noopener">{html.escape(str(card["url"]))}</a></p>'
            )
        body.append('<div class="hotel-contact">\n' + "\n".join(meta) + "\n</div>")
        blocks.append('<article class="ranking-card">\n' + "\n".join(body) + "\n</article>")
    return '<div class="ranking-grid">\n' + "\n".join(blocks) + "\n</div>"


def affiliate_grid(cards: list[dict[str, str]]) -> str:
    items: list[str] = []
    for card in cards:
        klass = "button secondary" if card.get("secondary") else "button"
        items.append(
            dedent(
                f"""\
                <div class="affiliate-card">
                  <b>{html.escape(card["title"])}</b>
                  <p>{html.escape(card["body"])}</p>
                  <a class="{klass}" href="#">{html.escape(card["cta"])}</a>
                </div>
                """
            ).strip()
        )
    return '<div class="affiliate-grid">\n' + "\n".join(items) + "\n</div>"


def render_sources(sources: list[tuple[str, str]]) -> str:
    links = "\n".join(
        f'  <li><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(label)}</a></li>'
        for label, url in sources
    )
    return f"<ul class=\"source-list\">\n{links}\n</ul>"


def article_json_ld(article: dict[str, object], canonical: str) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["description"],
        "datePublished": article["published_iso"],
        "dateModified": article["updated_iso"],
        "author": {"@type": "Organization", "name": "tabinote編集部"},
        "publisher": {"@type": "Organization", "name": "tabinote"},
        "mainEntityOfPage": canonical,
    }
    return json.dumps(payload, ensure_ascii=False, indent=4)


def build_sections(article: dict[str, object]) -> list[tuple[str, str, str]]:
    sections: list[tuple[str, str, str]] = []
    sections.append(("summary", "ひとことでいうと", ul(article["summary"], "summary-list")))  # type: ignore[arg-type]

    fit_parts = [p(text) for text in article["fit_paragraphs"]]  # type: ignore[index]
    fit_parts.append(ul(article["fit_list"]))  # type: ignore[arg-type]
    sections.append(("fit", str(article["fit_heading"]), "\n".join(fit_parts)))

    main_parts = [p(text) for text in article["main_paragraphs"]]  # type: ignore[index]
    for card in article.get("main_cards", []):  # type: ignore[union-attr]
        main_parts.append(info_card(card["title"], card["paragraphs"], card.get("bullets")))  # type: ignore[index]
    if article.get("main_list"):
        main_parts.append(ul(article["main_list"]))  # type: ignore[arg-type]
    sections.append(("main", str(article["main_heading"]), "\n".join(main_parts)))

    hotel_intro = [p(text) for text in article["hotel_intro"]]  # type: ignore[index]
    hotel_intro.append(ranking_cards(article["hotels"]))  # type: ignore[arg-type]
    sections.append(("hotels", str(article["hotel_heading"]), "\n".join(hotel_intro)))

    booking_parts = [p(text) for text in article["booking_intro"]]  # type: ignore[index]
    for card in article.get("booking_cards", []):  # type: ignore[union-attr]
        booking_parts.append(info_card(card["title"], card["paragraphs"], card.get("bullets")))  # type: ignore[index]
    if article.get("booking_list"):
        booking_parts.append(ul(article["booking_list"]))  # type: ignore[arg-type]
    booking_parts.append(affiliate_grid(article["affiliate_cards"]))  # type: ignore[arg-type]
    sections.append(("booking", "予約前に確認したいこと", "\n".join(booking_parts)))  # type: ignore[arg-type]
    return sections


ARTICLES: list[dict[str, object]] = [
    {
        "slug": "ishigaki-solo-hotels-3",
        "title": "石垣島でひとり旅をするのにおすすめしたいホテル3選",
        "description": "石垣島でひとり旅をするなら、離島ターミナルや飲食店への動きやすさが重要です。実体験メモと公式情報をもとに、石垣島で選びやすいホテルを3つに絞って整理します。",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "石垣島", "ひとり旅", "ホテル3選"],
        "lead": "石垣島のひとり旅は、海より先に宿の立地を見ておくと組みやすい旅になります。離島ターミナル、夜ごはん、空港からの動線を軸に、ひとりでも使いやすいホテルを3つに絞りました。",
        "summary": [
            "石垣島のひとり旅は、市街地か離島ターミナル周辺を拠点にすると動きやすい。",
            "夜ごはんを外で食べるなら、港周辺のホテルが失敗しにくい。",
            "ホテル内で完結したいなら、港近くより少し予算を上げたほうが満足しやすい。",
        ],
        "fit_heading": "この選び方が向く人",
        "fit_paragraphs": [
            "石垣島のひとり旅で迷いやすいのは、ホテルの雰囲気よりも動きやすさです。特に初めて行く場合は、空港からホテル、ホテルから夜ごはん、翌日の離島観光までを一本でつなげられるかが大事です。",
        ],
        "fit_list": [
            "レンタカーなしで石垣島を回したい",
            "離島ターミナルを使って竹富島や西表島方面にも行きたい",
            "夜は歩いてごはんに行けるほうが安心",
            "宿選びで大きく失敗したくない",
        ],
        "main_heading": "石垣島でひとり旅のホテルを選ぶポイント",
        "main_paragraphs": [
            "ひとり旅では、海が見えるかよりも、夜にひとりで戻りやすいか、朝に荷物を持って移動しやすいかを優先したほうが旅程が安定します。",
        ],
        "main_cards": [
            {
                "title": "最初に見るべきは立地",
                "paragraphs": [
                    "石垣港離島ターミナルの近くに泊まると、竹富島への日帰りや、西表島ツアーに出る朝も動きが軽くなります。",
                    "市街地の飲食店も集まりやすいため、ひとりで夜ごはんを取りやすいのも利点です。",
                ],
                "bullets": ["港・飲食店・コンビニの距離", "空港バスからの乗り継ぎやすさ"],
            },
            {
                "title": "ひとり旅なら大浴場や朝食の使い勝手も大事",
                "paragraphs": [
                    "夜を外で過ごすか、宿で締めるかで満足度が変わります。大浴場があるホテルは、街歩きのあとに部屋以外で休めるのが強いです。",
                ],
                "bullets": ["大浴場の有無", "朝食の評判より、朝の出発時間に合うか"],
            },
        ],
        "hotel_heading": "おすすめホテル3選",
        "hotel_intro": [
            "石垣島でひとり旅をするなら、離島ターミナルへの動きやすさと夜の過ごしやすさが大きな判断軸です。市街地で動きやすいホテルを中心に、選びやすい3軒をまとめました。",
        ],
        "hotels": [
            {
                "name": "ホテルグランビュー石垣 The First",
                "paragraphs": [
                    "730交差点前で、離島ターミナルに出やすい立地です。新しめで大浴場があり、ひとり旅で“部屋に戻るだけ”になりにくいのが強みです。",
                    "港周辺に飲食店が集まるため、夜ごはんを歩いて済ませたい人にも向きます。",
                ],
                "bullets": ["港周辺の利便性", "大浴場あり", "新しめで選びやすい"],
                "url": "https://granview.co.jp/ishigaki/",
            },
            {
                "name": "アパホテル〈石垣島〉",
                "paragraphs": [
                    "離島ターミナルから徒歩圏で、ホテルはシンプルに使いたい人向けです。2024年2月にリニューアルオープンしていて、ブランドの安心感もあります。",
                    "とにかく寝る場所と立地を優先したいひとり旅なら、候補に入れやすい一軒です。",
                ],
                "bullets": ["港徒歩圏", "ブランドの安心感", "コスパ重視向き"],
                "url": "https://www.apahotel.com/hotel/kyushu-okinawa/okinawa/ishigakijima/",
            },
            {
                "name": "THIRD石垣島",
                "paragraphs": [
                    "離島ターミナル至近で、港前に泊まりたい人向けです。オールインクルーシブの要素があり、街中でも少し旅感を出したいときに向きます。",
                    "ビーチリゾートではなく、港前のライフスタイルホテルとして考えると使い方が見えやすいです。",
                ],
                "bullets": ["離島ターミナル至近", "街中でもホテル時間を楽しみやすい", "若めの大人旅にも合う"],
                "url": "https://hotelthird.com/",
            },
        ],
        "booking_intro": [
            "石垣島は、同じ“港近く”でも雰囲気がかなり違います。離島観光を主軸にするのか、夜ごはんやバーも楽しみたいのかで選ぶとずれにくくなります。",
        ],
        "booking_cards": [
            {
                "title": "港近くか、海沿いリゾートか",
                "paragraphs": [
                    "ひとり旅デビューなら、まずは港近くが無難です。海沿いリゾートは気分が上がる一方で、夜ごはんや移動の自由度は落ちやすいです。",
                ],
                "bullets": ["初めてなら港近く", "2回目以降なら海沿いも候補"],
            },
            {
                "title": "朝の動きまで想像しておく",
                "paragraphs": [
                    "離島ツアーの集合や空港バスの時間が早いと、朝食があっても使い切れないことがあります。出発時間に合うかまで見ておくと選びやすいです。",
                ],
            },
        ],
        "booking_list": [
            "離島ターミナルまでの距離",
            "夜に歩いて戻れる範囲に飲食店があるか",
            "大浴場や朝食など、宿内で完結できる要素があるか",
        ],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "石垣島のホテルを比較しながら予約する。", "cta": "石垣島の宿を探す"},
            {"title": "航空券", "body": "羽田・関空などからの直行便を比較する。", "cta": "石垣島行きの航空券を探す", "secondary": "1"},
            {"title": "離島ツアー", "body": "竹富島や西表島の日帰りツアーを比較する。", "cta": "離島ツアーを探す", "secondary": "1"},
        ],
        "sources": [
            ("グランビュー石垣 The First 公式", "https://granview.co.jp/ishigaki/"),
            ("アパホテル〈石垣島〉公式", "https://www.apahotel.com/hotel/kyushu-okinawa/okinawa/ishigakijima/"),
            ("THIRD石垣島 公式", "https://hotelthird.com/"),
        ],
        "published": "2026.06.07",
        "updated": "2026.06.07",
        "published_iso": "2026-06-07",
        "updated_iso": "2026-06-07",
        "tags": ["solo", "okinawa"],
        "area": "沖縄・石垣島",
        "card_labels": ["石垣島", "ひとり旅"],
    },
    {
        "slug": "ishigaki-terminal-hotels-3",
        "title": "石垣島で離島ターミナル近くに泊まりたい人向けホテル3選",
        "description": "石垣島で竹富島や西表島へ行くなら、離島ターミナル近くのホテルが便利です。港周辺で比較しやすいホテルを3つに絞って整理します。",
        "image": "https://images.unsplash.com/photo-1493558103817-58b2924bce98?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "石垣島", "港近く", "ホテル3選"],
        "lead": "石垣島で離島めぐりを優先するなら、まずホテルの立地を港基準で考えたほうが楽です。竹富島や西表島に出る朝の軽さを重視して、港周辺で選びやすいホテルを3つに絞りました。",
        "summary": [
            "離島観光を軸にするなら、港周辺のホテルが最も組みやすい。",
            "同じ港近くでも、老舗・新しめ・オールインクルーシブ系で使い方が分かれる。",
            "海沿いリゾート感より、朝の移動と夜ごはんのしやすさを優先したい記事。",
        ],
        "fit_heading": "この選び方が向く人",
        "fit_paragraphs": [
            "石垣島で竹富島や西表島に出る場合、朝の集合時間が早いことが多く、荷物の預け直しやバス移動の回数が少ないだけでかなり楽になります。",
        ],
        "fit_list": [
            "石垣島滞在中に離島へ行く予定がある",
            "最終日も港周辺で買い物や食事をしたい",
            "宿にリゾート感より利便性を求める",
        ],
        "main_heading": "港近ホテルの選び方",
        "main_paragraphs": [
            "港近くのホテルを選ぶときは、離島ターミナルまでの徒歩分数よりも、実際に夜歩いて戻りやすいか、朝の食事や荷物預けに無理がないかを見たほうが実用的です。",
        ],
        "main_cards": [
            {
                "title": "ホテルの個性はかなり違う",
                "paragraphs": [
                    "同じ港周辺でも、老舗のシティホテル、新しめの大浴場付きホテル、ライフスタイルホテルで体験は分かれます。港近という共通点だけで決めないほうがずれにくいです。",
                ],
            }
        ],
        "hotel_heading": "港近くで選びたい3軒",
        "hotel_intro": [
            "離島ターミナル近くに泊まると、竹富島などへの日帰り観光や空港バスへの移動が組みやすくなります。港周辺で選びやすい3軒をまとめました。",
        ],
        "hotels": [
            {
                "name": "南の美ら花ホテルミヤヒラ",
                "paragraphs": [
                    "離島ターミナル徒歩1分で、港に最も寄せたい旅向きです。老舗感はありますが、石垣島で離島観光を優先するなら分かりやすい候補です。",
                ],
                "bullets": ["離島ターミナル徒歩1分", "港基準の旅程を組みやすい", "食事施設あり"],
                "url": "https://www.miyahira.co.jp/",
            },
            {
                "name": "ホテルイーストチャイナシー",
                "paragraphs": [
                    "港ビューと市街地アクセスのバランスが強みです。離島ターミナルに近く、客室から海や船の景色を楽しみたい人に向きます。",
                ],
                "bullets": ["港の景色", "徒歩でごはんに行きやすい", "離島観光の拠点向き"],
                "url": "https://www.courthotels.co.jp/eastchinasea/",
            },
            {
                "name": "THIRD石垣島",
                "paragraphs": [
                    "港前に泊まりつつ、ホテル時間も楽しみたい人向けです。若めの大人旅や、ホテルに少し雰囲気を求めたいときに選びやすいです。",
                ],
                "bullets": ["港至近", "ライフスタイルホテル", "街中でも非日常感を出しやすい"],
                "url": "https://hotelthird.com/",
            },
        ],
        "booking_intro": [
            "港近ホテルは便利ですが、部屋の広さや大浴場の有無はかなり差があります。何を削って何を残すかを先に決めておくと選びやすいです。",
        ],
        "booking_cards": [
            {
                "title": "夜ごはんまで含めて考える",
                "paragraphs": [
                    "港周辺は居酒屋や市場が近い一方で、ホテル館内のリゾート感は薄くなりがちです。夜を街で楽しむ前提なら相性がよく、ホテルでこもりたい人には向きません。",
                ],
            }
        ],
        "booking_list": [
            "離島ターミナルまでの徒歩分数",
            "荷物を預けやすいか",
            "朝食時間が早めの出発に合うか",
        ],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "港周辺ホテルを立地で比較する。", "cta": "港近くの宿を探す"},
            {"title": "フェリー・ツアー", "body": "竹富島や西表島のツアーを比較する。", "cta": "離島ツアーを探す", "secondary": "1"},
            {"title": "航空券", "body": "直行便と乗継便を比較する。", "cta": "石垣島行きの航空券を探す", "secondary": "1"},
        ],
        "sources": [
            ("南の美ら花ホテルミヤヒラ 公式", "https://www.miyahira.co.jp/"),
            ("ホテルイーストチャイナシー 公式", "https://www.courthotels.co.jp/eastchinasea/"),
            ("THIRD石垣島 公式", "https://hotelthird.com/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["okinawa"], "area": "沖縄・石垣島", "card_labels": ["石垣島", "港近く"],
    },
    {
        "slug": "yaeyama-anniversary-hotels-3",
        "title": "八重山で記念日旅に向くホテル3選",
        "description": "石垣島・竹富島・小浜島を含む八重山エリアで、記念日旅に向くホテルを3軒に絞りました。静けさ、海の見え方、宿で過ごす時間を軸に整理します。",
        "image": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "八重山", "記念日", "ホテル3選"],
        "lead": "八重山で記念日旅を考えるなら、石垣島だけでなく、竹富島や小浜島まで視野に入れると選択肢が広がります。海の見え方、夜の静けさ、宿にこもる価値で3軒に絞りました。",
        "summary": [
            "外で動くより、宿で過ごす時間が主役になる旅向けの記事。",
            "石垣島の上質リゾート、竹富島で泊まる非日常、小浜島の静けさで方向が分かれる。",
            "どこに泊まるかで、記念日の雰囲気はかなり変わる。",
        ],
        "fit_heading": "この選び方が向く人",
        "fit_paragraphs": ["記念日旅では、観光の数よりも“そのホテルでどんな時間を過ごしたいか”を先に決めたほうが失敗しにくいです。"],
        "fit_list": ["ホテル時間を主役にしたい", "海の景色や夜の静けさを重視したい", "価格より体験価値を優先したい"],
        "main_heading": "八重山の記念日ホテルは何で分かれるか",
        "main_paragraphs": ["石垣島はアクセスと設備、小浜島は静けさ、竹富島は島に泊まる非日常が強みです。同じ沖縄でも、旅のテンションがかなり変わります。"],
        "hotel_heading": "記念日旅に向く3軒",
        "hotel_intro": ["八重山で記念日旅をするなら、島にこもるのか、石垣島を拠点に動くのかでホテルの選び方が変わります。雰囲気の異なる3軒をまとめました。"],
        "hotels": [
            {
                "name": "ANAインターコンチネンタル石垣リゾート",
                "paragraphs": [
                    "石垣島でワンランク上の滞在をしたいなら第一候補です。クラブカテゴリーを含めて、王道のラグジュアリーリゾートとして選びやすい一軒です。",
                ],
                "bullets": ["大人二人旅", "記念日・ハネムーン", "石垣島で上質感を優先"],
                "url": "https://www.anaintercontinental-ishigaki.jp/",
            },
            {
                "name": "星のや竹富島",
                "paragraphs": [
                    "石垣島から日帰りで終えず、竹富島に泊まる価値を作りやすい宿です。島時間に浸る感覚が強く、観光というより滞在そのものが目的になります。",
                ],
                "bullets": ["竹富島に泊まる非日常", "静かな大人旅", "景色より空気感を重視"],
                "url": "https://hoshinoresorts.com/ja/hotels/hoshinoyataketomijima/",
            },
            {
                "name": "はいむるぶし",
                "paragraphs": [
                    "小浜島で昼は海、夜は暗さと静けさを楽しみたいなら強い候補です。実体験メモでも、月の道や夜の落ち着きが印象に残るホテルとして残っています。",
                ],
                "bullets": ["小浜島らしい静けさ", "夜空や月の道", "島でゆっくり過ごす贅沢"],
                "url": "https://www.haimurubushi.co.jp/",
            },
        ],
        "booking_intro": ["八重山の記念日旅は、宿の前後にどれだけ動くかで相性が変わります。石垣島拠点か、島に泊まるかは先に決めたほうが整理しやすいです。"],
        "booking_cards": [
            {
                "title": "石垣島拠点か、島泊まりか",
                "paragraphs": [
                    "石垣島はアクセスが楽で、食事や移動の自由度があります。竹富島や小浜島は移動の自由度を少し落としてでも、泊まる意味を作りやすい選択です。",
                ],
            }
        ],
        "booking_list": ["空港や港からの移動方法", "レストラン予約の要否", "島泊まりの場合の船時刻"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "八重山の記念日向けホテルを比較する。", "cta": "記念日向けの宿を探す"},
            {"title": "航空券", "body": "石垣島行きの便を比較する。", "cta": "石垣島行きの航空券を探す", "secondary": "1"},
            {"title": "離島フェリー", "body": "竹富島・小浜島へ渡る手段を確認する。", "cta": "フェリー情報を見る", "secondary": "1"},
        ],
        "sources": [
            ("ANAインターコンチネンタル石垣リゾート 公式", "https://www.anaintercontinental-ishigaki.jp/"),
            ("星のや竹富島 公式", "https://hoshinoresorts.com/ja/hotels/hoshinoyataketomijima/"),
            ("はいむるぶし 公式", "https://www.haimurubushi.co.jp/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["anniversary", "couple", "okinawa"], "area": "沖縄・八重山", "card_labels": ["八重山", "記念日"],
    },
    {
        "slug": "kohama-hotels-2",
        "title": "小浜島で静かな島時間を楽しみたい人におすすめのホテル2選",
        "description": "小浜島に泊まるなら、昼の海と夜の静けさをどう楽しみたいかで選び方が変わります。小浜島で比較しやすいホテルを2軒に絞って整理します。",
        "image": "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "小浜島", "島時間", "ホテル2選"],
        "lead": "小浜島に泊まる意味は、海の近さよりも、夜の静けさや暗さまで含めた島時間にあります。小浜島で選択肢になりやすい2軒を、雰囲気の違いが分かる形で整理しました。",
        "summary": [
            "小浜島は“どこへ行くか”より“そこでどう過ごすか”が主役になりやすい。",
            "はいむるぶしは島の静けさを活かすホテル、リゾナーレ小浜島は星野らしい華やかさがある。",
            "どちらも夜は静かだが、ホテルに求める空気感が違う。",
        ],
        "fit_heading": "この選び方が向く人",
        "fit_paragraphs": ["小浜島は、離島観光を詰め込むより、海・風・夜の暗さまで含めて宿で過ごしたい人に向きます。"],
        "fit_list": ["石垣島から一歩離れて静かに過ごしたい", "昼は海、夜は星や月を楽しみたい", "ホテル時間を旅の主役にしたい"],
        "main_heading": "小浜島のホテル選びで見るポイント",
        "main_paragraphs": ["同じ島内でも、リゾートの見せ方はかなり違います。派手さより島らしさを優先するか、ブランド感や映えも欲しいかで分かれます。"],
        "hotel_heading": "小浜島で比較しやすい2軒",
        "hotel_intro": ["どちらも定番ですが、夜の過ごし方や空気感の好みで選ぶと判断しやすいです。"],
        "hotels": [
            {
                "name": "はいむるぶし",
                "paragraphs": [
                    "実体験メモでは、夜に明かりを絞った雰囲気や、月の道の美しさが印象に残るホテルとして整理されています。小浜島らしい静けさを活かしたいなら強い候補です。",
                ],
                "bullets": ["静かな夜", "月や星を楽しむ", "島らしさを活かした滞在"],
                "url": "https://www.haimurubushi.co.jp/",
            },
            {
                "name": "リゾナーレ小浜島",
                "paragraphs": [
                    "広い敷地や景色の見せ方など、星野らしい分かりやすい華やかさがあります。島の静けさもありつつ、ホテルの演出を楽しみたい人向けです。",
                ],
                "bullets": ["ブランド感", "広い敷地", "映える体験も欲しい人向け"],
                "url": "https://hoshinoresorts.com/ja/hotels/risonarekohamajima/",
            },
        ],
        "booking_intro": ["小浜島は島内での選択肢が限られるため、食事や送迎の時間まで含めて先に決めたほうが安心です。"],
        "booking_cards": [],
        "booking_list": ["港からの送迎", "夕食の予約要否", "夜に何をして過ごしたいか"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "小浜島で泊まれるホテルを比較する。", "cta": "小浜島の宿を探す"},
            {"title": "石垣島行き航空券", "body": "小浜島へ渡る前提で石垣島行きの便を比較する。", "cta": "石垣島行きの航空券を探す", "secondary": "1"},
            {"title": "フェリー情報", "body": "小浜港への船時刻を確認する。", "cta": "フェリー情報を見る", "secondary": "1"},
        ],
        "sources": [
            ("はいむるぶし 公式", "https://www.haimurubushi.co.jp/"),
            ("リゾナーレ小浜島 公式", "https://hoshinoresorts.com/ja/hotels/risonarekohamajima/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["couple", "anniversary", "okinawa"], "area": "沖縄・小浜島", "card_labels": ["小浜島", "ホテル比較"],
    },
    {
        "slug": "miyakojima-hotels-3",
        "title": "宮古島で目的別に選びたいホテル3選",
        "description": "宮古島のホテルは、前浜ビーチを軸にするか、シギラエリアで完結するか、市街地と海のバランスを取るかで選び方が変わります。目的別に3軒に絞って整理します。",
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "宮古島", "ホテル3選", "目的別"],
        "lead": "宮古島のホテルは、海の近さだけで選ぶとずれやすいです。前浜ビーチを主役にしたいのか、シギラ内で完結したいのか、初めての宮古島で安心感を取りたいのかで3軒に絞りました。",
        "summary": [
            "王道なら宮古島東急、コスパとシギラ内完結ならサンタモニカ、新しめ大型リゾートならヒルトン。",
            "宮古島はホテルの立地で旅の動き方がかなり変わる。",
            "何を見たいかより、どこで過ごす時間を長くしたいかで選ぶと分かりやすい。",
        ],
        "fit_heading": "この選び方が向く人",
        "fit_paragraphs": ["宮古島は、石垣島よりもホテル時間の比重が高くなりやすい島です。どのエリアに泊まるかで、海の見え方も夜ごはんの選び方も変わります。"],
        "fit_list": ["初めての宮古島で大きく外したくない", "ホテルで過ごす時間も重視したい", "ビーチ・ブランド感・コスパのどれを優先するか迷っている"],
        "main_heading": "宮古島ホテル選びの軸",
        "main_paragraphs": ["前浜ビーチの王道感、シギラのリゾートシティ感、新しめ大型ブランドの安心感。この3つで比べると宮古島は選びやすくなります。"],
        "hotel_heading": "目的別に選ぶ3軒",
        "hotel_intro": ["宮古島は、ビーチを主役にしたいのか、市街地の便利さを優先したいのかで宿選びが変わります。目的別に選びやすい3軒をまとめました。"],
        "hotels": [
            {
                "name": "宮古島東急ホテル＆リゾーツ",
                "paragraphs": [
                    "前浜ビーチを主役にしたいなら王道です。初めての宮古島でもイメージしやすく、海の見え方で選びたい人に向きます。",
                ],
                "bullets": ["前浜ビーチ", "王道リゾート", "初めての宮古島向き"],
                "url": "https://www.tokyuhotels.co.jp/miyakojima-h/index.html",
            },
            {
                "name": "ホットクロスポイント サンタモニカ",
                "paragraphs": [
                    "シギラエリアでコスパよく泊まりたいときの候補です。宿泊費を抑えつつ、シギラ内の施設を使いたい旅と相性がいいです。",
                ],
                "bullets": ["シギラ内で完結しやすい", "コスパ型", "女子旅・ひとり旅にも使いやすい"],
                "url": "https://shigira.com/hotel/santamonica",
            },
            {
                "name": "ヒルトン沖縄宮古島リゾート",
                "paragraphs": [
                    "新しめの大型ブランドリゾートで、伊良部大橋ビューやサンセットを重視したい人向きです。子連れでも大人旅でも使いやすいバランスがあります。",
                ],
                "bullets": ["新しめ大型リゾート", "伊良部大橋ビュー", "ファミリー・カップル両対応"],
                "url": "https://miyakojima.hiltonjapan.co.jp/",
            },
        ],
        "booking_intro": ["宮古島は工事情報や休館が出るホテルもあるため、候補を絞ったあとに最新のお知らせを一度確認したほうが安心です。"],
        "booking_cards": [
            {
                "title": "空港とビーチの位置関係を見る",
                "paragraphs": [
                    "宮古空港、下地島空港、前浜ビーチ、シギラ、伊良部方面はそれぞれ距離感が違います。ホテル単体ではなく、旅程全体で見ると判断しやすいです。",
                ],
            }
        ],
        "booking_list": ["工事・休館情報", "空港からの所要時間", "レンタカー前提度"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "宮古島のホテルを目的別に比較する。", "cta": "宮古島の宿を探す"},
            {"title": "航空券", "body": "宮古空港・下地島空港着の便を比較する。", "cta": "宮古島行きの航空券を探す", "secondary": "1"},
            {"title": "レンタカー", "body": "宮古島での移動手段を比較する。", "cta": "レンタカーを探す", "secondary": "1"},
        ],
        "sources": [
            ("宮古島東急ホテル＆リゾーツ 公式", "https://www.tokyuhotels.co.jp/miyakojima-h/index.html"),
            ("ホットクロスポイント サンタモニカ 公式", "https://shigira.com/hotel/santamonica"),
            ("ヒルトン沖縄宮古島リゾート 公式", "https://miyakojima.hiltonjapan.co.jp/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["couple", "solo", "okinawa"], "area": "沖縄・宮古島", "card_labels": ["宮古島", "ホテル3選"],
    },
    {
        "slug": "naha-hotels-3",
        "title": "那覇で立地重視で選びたいホテル3選",
        "description": "那覇でホテルを選ぶなら、国際通り・おもろまち・首里寄りなど、何をしたいかで選び方が変わります。立地重視で使いやすいホテルを3軒に絞って整理します。",
        "image": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "那覇", "ホテル3選", "立地重視"],
        "lead": "那覇のホテル選びは、海の見え方より、どこを歩きたいかで決めたほうが早いです。国際通り、おもろまち、首里方面まで見て、立地で選びやすい3軒に絞りました。",
        "summary": [
            "国際通りを軸にするならダイワロイネット、おもろまちならアルモント、リゾート感を少し足すならノボテル。",
            "那覇は同じ市内でも、歩きやすい範囲がかなり違う。",
            "初沖縄なら、移動のしやすさと朝食・大浴場などの使い勝手で見ると選びやすい。",
        ],
        "fit_heading": "この選び方が向く人",
        "fit_paragraphs": ["那覇は空港から近い一方で、どこを拠点にするかで街歩きの快適さが変わります。ホテルを観光の延長として考えると選びやすいです。"],
        "fit_list": ["国際通りやモノレールを使いたい", "那覇1泊を効率よく使いたい", "リゾート感より街歩きとの相性を重視したい"],
        "main_heading": "那覇ホテルを立地で選ぶ基準",
        "main_paragraphs": ["空港からの近さだけでは決めにくいため、国際通り、おもろまち、首里寄りのどこに寄せるかで見たほうが分かりやすいです。"],
        "hotel_heading": "立地重視で選びたい3軒",
        "hotel_intro": ["いずれも実際に記事素材として残っているホテルですが、旅の目的によって向き不向きが分かれます。"],
        "hotels": [
            {
                "name": "ダイワロイネットホテル那覇国際通り",
                "paragraphs": [
                    "牧志駅直結で、国際通りを歩く旅に向きます。観光・買い物・朝食の取りやすさまで含めて、最初に見やすいホテルです。",
                ],
                "bullets": ["牧志駅直結", "国際通り徒歩圏", "朝食も強め"],
                "url": "https://www.daiwaroynet.jp/naha-kokusaidori/",
            },
            {
                "name": "アルモントホテル那覇おもろまち",
                "paragraphs": [
                    "おもろまち駅徒歩圏で、大浴場があるのが強みです。街歩きのあとに大浴場へ戻れる動線は、那覇では分かりやすい価値があります。",
                ],
                "bullets": ["おもろまち駅近く", "大浴場あり", "ビジネス寄りでも快適"],
                "url": "https://www.almont.jp/naha-omoromachi/",
            },
            {
                "name": "ノボテル沖縄那覇",
                "paragraphs": [
                    "那覇市内でも少しリゾート感を足したい人向けです。首里寄りで駅近ではないぶん、プールやホテル時間の満足度を足しやすい一軒です。",
                ],
                "bullets": ["那覇で少しリゾート感", "インフィニティプール", "早割で価格差が縮むこともある"],
                "url": "https://www.novotelokinawanaha.jp/",
            },
        ],
        "booking_intro": ["那覇はレンタカーなしでも動ける一方で、駅近かどうか、夜ごはんを歩いて取りに行けるかで満足度が変わります。"],
        "booking_cards": [],
        "booking_list": ["モノレール駅との距離", "国際通り・飲食店までの徒歩圏", "大浴場や朝食の必要性"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "那覇のホテルを立地で比較する。", "cta": "那覇の宿を探す"},
            {"title": "航空券", "body": "那覇空港着の便を比較する。", "cta": "那覇行きの航空券を探す", "secondary": "1"},
            {"title": "レンタカー", "body": "本島へそのまま出る日の移動手段を比較する。", "cta": "レンタカーを探す", "secondary": "1"},
        ],
        "sources": [
            ("ダイワロイネットホテル那覇国際通り 公式", "https://www.daiwaroynet.jp/naha-kokusaidori/"),
            ("アルモントホテル那覇おもろまち 公式", "https://www.almont.jp/naha-omoromachi/"),
            ("ノボテル沖縄那覇 公式", "https://www.novotelokinawanaha.jp/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["solo", "couple", "okinawa"], "area": "沖縄・那覇", "card_labels": ["那覇", "ホテル3選"],
    },
    {
        "slug": "miyakojima-anniversary-hotels-3",
        "title": "宮古島で記念日旅に向くホテル3選",
        "description": "宮古島で記念日旅をするなら、伊良部島のラグジュアリー、東海岸の隠れ家、前浜ビーチの王道感で選び方が変わります。記念日向けのホテル3軒を整理します。",
        "image": "https://images.unsplash.com/photo-1493558103817-58b2924bce98?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "宮古島", "記念日", "ホテル3選"],
        "lead": "宮古島の記念日旅は、ホテルの価格帯よりも、どんな景色と時間を残したいかで選んだほうがぶれません。王道、隠れ家、伊良部島のラグジュアリーで3軒に絞りました。",
        "summary": [
            "前浜ビーチの王道感なら宮古島東急、静けさならthe rescape、伊良部島のラグジュアリーならイラフSUI。",
            "宮古島はホテルの立地で旅のテンションが大きく変わる。",
            "観光を詰め込むより、宿で過ごす時間が長い人向けの記事。",
        ],
        "fit_heading": "この選び方が向く人",
        "fit_paragraphs": ["宮古島の記念日旅では、部屋にいる時間、朝夕の景色、ホテルから動く量まで含めて選ぶと失敗しにくいです。"],
        "fit_list": ["海の景色を主役にしたい", "大人二人でゆっくり過ごしたい", "価格より体験を優先したい"],
        "main_heading": "宮古島で記念日ホテルを選ぶ軸",
        "main_paragraphs": ["王道ビーチ、隠れ家、伊良部島ラグジュアリー。この3つでかなり性格が分かれます。レンタカー前提度もあわせて見たほうが現実的です。"],
        "hotel_heading": "記念日旅で候補にしたい3軒",
        "hotel_intro": ["宮古島で記念日旅をするなら、海の見え方、過ごす時間帯、ホテルで味わいたい空気感で候補が変わります。記念日向きの3軒をまとめました。"],
        "hotels": [
            {
                "name": "イラフ SUI ラグジュアリーコレクションホテル 沖縄宮古",
                "paragraphs": [
                    "伊良部ブルーの海を前に、サンセットや大人っぽい空気感を楽しみたい人向けです。送迎やスパも含めて、分かりやすく非日常に入りやすい一軒です。",
                ],
                "bullets": ["伊良部島", "サンセット", "マリオット系ラグジュアリー"],
                "url": "https://www.suihotels.com/iraphsui-miyako_okinawa/",
            },
            {
                "name": "the rescape",
                "paragraphs": [
                    "東海岸の静けさを重視したいときの候補です。観光の拠点というより、ホテルにこもる時間を大事にしたい記念日旅向きです。",
                ],
                "bullets": ["東海岸の隠れ家", "プライベート感", "静かな大人旅"],
                "url": "https://www.uds-hotels.com/the-rescape/",
            },
            {
                "name": "宮古島東急ホテル＆リゾーツ",
                "paragraphs": [
                    "前浜ビーチの王道感で選びたいならやはり強い候補です。初めての宮古島の記念日旅でも、景色の分かりやすさがあります。",
                ],
                "bullets": ["前浜ビーチ", "王道の宮古島感", "初訪問でも選びやすい"],
                "url": "https://www.tokyuhotels.co.jp/miyakojima-h/index.html",
            },
        ],
        "booking_intro": ["宮古島はエリアが分かれるため、記念日ディナーをどこで取るか、レンタカーをどこまで使うかを先に考えておくと選びやすいです。"],
        "booking_cards": [],
        "booking_list": ["レストラン予約", "レンタカー前提度", "空港からの距離"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "宮古島の記念日向けホテルを比較する。", "cta": "記念日向けの宿を探す"},
            {"title": "航空券", "body": "宮古島行きの便を比較する。", "cta": "宮古島行きの航空券を探す", "secondary": "1"},
            {"title": "レンタカー", "body": "宮古島での移動手段を比較する。", "cta": "レンタカーを探す", "secondary": "1"},
        ],
        "sources": [
            ("イラフ SUI ラグジュアリーコレクションホテル 沖縄宮古 公式", "https://www.suihotels.com/iraphsui-miyako_okinawa/"),
            ("the rescape 公式", "https://www.uds-hotels.com/the-rescape/"),
            ("宮古島東急ホテル＆リゾーツ 公式", "https://www.tokyuhotels.co.jp/miyakojima-h/index.html"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["anniversary", "couple", "okinawa"], "area": "沖縄・宮古島", "card_labels": ["宮古島", "記念日"],
    },
    {
        "slug": "ishigaki-2days-model-course",
        "title": "石垣島1泊2日モデルコース｜弾丸でも離島まで楽しむ動き方",
        "description": "石垣島を1泊2日で楽しむなら、基本は石垣島に絞りつつ、竹富島を1つ足す組み方が現実的です。弾丸でも動きやすいモデルコースを整理します。",
        "image": "https://images.unsplash.com/photo-1493558103817-58b2924bce98?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "石垣島", "1泊2日", "モデルコース"],
        "lead": "石垣島の1泊2日は、詰め込みすぎるとすぐ崩れます。基本は石垣島に軸を置き、足すなら竹富島までに絞る前提で、弾丸でも回しやすい流れを組みました。",
        "summary": [
            "石垣島1泊2日は、島を増やしすぎず石垣＋竹富島までが現実的。",
            "空港から港、市街地、ホテルの動線を軽くすると弾丸でも満足しやすい。",
            "夜ごはんを市街地で取りやすい宿を選ぶと崩れにくい。",
        ],
        "fit_heading": "このモデルコースが向く人",
        "fit_paragraphs": ["忙しい週末でも離島っぽさを感じたい人向けの組み方です。西表島や由布島まで足すのではなく、竹富島で非日常感を出す前提で考えます。"],
        "fit_list": ["石垣島へ直行便で入れる", "1泊2日で無理なく離島感を味わいたい", "レンタカーなしで動きたい"],
        "main_heading": "1泊2日の組み方",
        "main_paragraphs": ["初日は石垣空港から港へ出て竹富島を足し、夜は石垣市街地へ戻る流れが分かりやすいです。2日目は石垣島内を軽く回すか、半日ツアーを入れる程度がちょうどいいです。"],
        "main_cards": [
            {
                "title": "1日目",
                "paragraphs": [
                    "午前から昼に石垣空港着。空港で軽く食べて、路線バスで石垣港離島ターミナルへ移動。荷物を預けて竹富島へ日帰りで渡る。",
                    "夕方に石垣へ戻り、市街地のホテルへチェックイン。夜は美崎町周辺でごはんを取る。",
                ],
                "bullets": ["空港→港→竹富島→石垣市街地", "宿は港徒歩圏が楽"],
            },
            {
                "title": "2日目",
                "paragraphs": [
                    "石垣島内で海沿いドライブを少し入れるか、午前発の離島ツアーを入れてもよいです。ただし、午後の飛行機に間に合うよう空港バスの時間は余裕を見ます。",
                ],
                "bullets": ["詰め込みすぎない", "港周辺でおみやげ時間を残す"],
            },
        ],
        "hotel_heading": "このモデルコースで相性がいい宿",
        "hotel_intro": ["1泊2日で弾丸なら、港徒歩圏か市街地近くのホテルが相性良好です。"],
        "hotels": [
            {
                "name": "アパホテル〈石垣島〉",
                "paragraphs": ["シンプルに泊まって動く弾丸旅向きです。"],
                "bullets": ["港徒歩圏", "コスパ重視"],
                "url": "https://www.apahotel.com/hotel/kyushu-okinawa/okinawa/ishigakijima/",
            },
            {
                "name": "ホテルグランビュー石垣 The First",
                "paragraphs": ["大浴場も欲しい弾丸旅なら候補に入れやすいです。"],
                "bullets": ["港周辺", "大浴場あり"],
                "url": "https://granview.co.jp/ishigaki/",
            },
            {
                "name": "南の美ら花ホテルミヤヒラ",
                "paragraphs": ["離島ターミナル最優先で考えるなら分かりやすい立地です。"],
                "bullets": ["港最優先", "老舗感"],
                "url": "https://www.miyahira.co.jp/",
            },
        ],
        "booking_intro": ["便の時間とフェリーの時間で旅程が決まるため、まず飛行機を押さえてからホテルと離島行きを組むとずれにくいです。"],
        "booking_cards": [
            {
                "title": "石垣島1泊2日は基本ひとつの島に絞る",
                "paragraphs": [
                    "石垣島から複数の離島を詰め込むと、港の往復ばかりになりがちです。足すなら竹富島までにして、あとは石垣島側で余白を持たせたほうが満足しやすいです。",
                ],
            }
        ],
        "booking_list": ["空港到着時間", "竹富島へ渡るフェリー時刻", "空港バスの所要時間"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "石垣島で1泊2日に向く宿を比較する。", "cta": "石垣島の宿を探す"},
            {"title": "航空券", "body": "石垣島直行便と乗継便を比較する。", "cta": "石垣島行きの航空券を探す", "secondary": "1"},
            {"title": "竹富島ツアー", "body": "竹富島の水牛車や日帰りツアーを比較する。", "cta": "竹富島ツアーを探す", "secondary": "1"},
        ],
        "sources": [
            ("沖縄観光情報WEBサイト おきなわ物語", "https://www.okinawastory.jp/"),
            ("八重山観光フェリー", "https://book.yaeyama.co.jp/"),
            ("アパホテル〈石垣島〉公式", "https://www.apahotel.com/hotel/kyushu-okinawa/okinawa/ishigakijima/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["solo", "okinawa"], "area": "沖縄・石垣島", "card_labels": ["石垣島", "1泊2日"],
    },
    {
        "slug": "ishigaki-vs-miyakojima-solo",
        "title": "石垣島と宮古島、ひとり旅ならどっち？",
        "description": "石垣島と宮古島はどちらも人気ですが、ひとり旅のしやすさはかなり違います。移動、夜ごはん、宿の選びやすさを軸に比較します。",
        "image": "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "比較", "ひとり旅", "石垣島と宮古島"],
        "lead": "石垣島と宮古島はどちらも海がきれいですが、ひとり旅のしやすさは同じではありません。行動しやすさなら石垣島、こもる旅なら宮古島、という前提で比較します。",
        "summary": [
            "初めてのひとり旅なら石垣島のほうが動きやすい。",
            "宮古島はホテル時間を長く取る前提なら合う。",
            "夜ごはんとレンタカー前提度で差が出やすい。",
        ],
        "fit_heading": "この比較が向く人",
        "fit_paragraphs": ["どちらも良さはありますが、今の自分が“動きたい”のか“こもりたい”のかで向く島が変わります。"],
        "fit_list": ["沖縄の離島にひとり旅してみたい", "レンタカーを借りるか迷っている", "夜ごはんや宿の空気感も気になる"],
        "main_heading": "ひとり旅目線での違い",
        "main_paragraphs": ["石垣島は市街地と離島ターミナルが近く、飲食店も多いため、ひとり旅での不安を減らしやすいです。宮古島は海のきれいさが強い一方で、ホテルやレンタカー前提度が旅の満足度を左右しやすいです。"],
        "main_cards": [
            {
                "title": "石垣島が向くケース",
                "paragraphs": [
                    "ひとりでごはんに入りやすい店が多く、離島観光もレンタカーなしで組みやすいです。初めての沖縄離島ひとり旅なら安心感があります。",
                ],
                "bullets": ["市街地が使いやすい", "離島観光しやすい", "バス移動も組みやすい"],
            },
            {
                "title": "宮古島が向くケース",
                "paragraphs": [
                    "海を見て静かに過ごしたい、ホテルでこもる時間も楽しみたいなら宮古島向きです。観光より滞在そのものが旅の中心になります。",
                ],
                "bullets": ["静かな時間", "海の眺め", "ホテル滞在を重視"],
            },
        ],
        "hotel_heading": "ひとり旅で見ておきたい宿の例",
        "hotel_intro": ["比較の目安になるよう、それぞれひとり旅と相性のいい宿を1〜2軒ずつ挙げます。"],
        "hotels": [
            {
                "name": "ホテルグランビュー石垣 The First（石垣島）",
                "paragraphs": ["港周辺・大浴場ありで、石垣島らしい動きやすさを取りやすい宿です。"],
                "bullets": ["港近く", "ひとり旅向き"],
                "url": "https://granview.co.jp/ishigaki/",
            },
            {
                "name": "たびのホテルlit宮古島（宮古島）",
                "paragraphs": ["西里通り沿いで、宮古島の中では街に寄せて動きやすい宿です。大浴場があるのもひとり旅向きです。"],
                "bullets": ["街中", "大浴場", "長期滞在にも向く"],
                "url": "https://miyakojima.tabino-hotel.jp/",
            },
            {
                "name": "ホットクロスポイント サンタモニカ（宮古島）",
                "paragraphs": ["ひとりでこもる前提なら、シギラ内でコスパよく泊まる候補として見やすいです。"],
                "bullets": ["シギラ内", "ホテル時間重視"],
                "url": "https://shigira.com/hotel/santamonica",
            },
        ],
        "booking_intro": ["ひとり旅では、映えよりも不安を減らせるかが大事です。夜ごはん、移動、宿の立地を先に決めておくと迷いにくくなります。"],
        "booking_cards": [],
        "booking_list": ["夜ごはんを歩いて取りに行けるか", "レンタカーなしで動けるか", "宿にこもる時間を楽しめるか"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "石垣島・宮古島の宿を比較する。", "cta": "沖縄離島の宿を探す"},
            {"title": "航空券", "body": "石垣島・宮古島行きの便を比較する。", "cta": "沖縄離島の航空券を探す", "secondary": "1"},
            {"title": "レンタカー", "body": "宮古島側で必要かどうかを比較する。", "cta": "レンタカーを探す", "secondary": "1"},
        ],
        "sources": [
            ("ホテルグランビュー石垣 The First 公式", "https://granview.co.jp/ishigaki/"),
            ("たびのホテルlit宮古島 公式", "https://miyakojima.tabino-hotel.jp/"),
            ("ホットクロスポイント サンタモニカ 公式", "https://shigira.com/hotel/santamonica"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["solo", "okinawa"], "area": "沖縄・比較", "card_labels": ["比較", "ひとり旅"],
    },
    {
        "slug": "winter-okinawa-sea-guide",
        "title": "冬の沖縄で海遊びはできる？海遊びと観光の組み立て方",
        "description": "冬の沖縄でも海遊びは可能ですが、服装や風の強さ、海から上がったあとの寒さまで見ておく必要があります。シュノーケルと観光をどう組み合わせるか整理します。",
        "image": "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "冬旅", "海遊び", "ガイド"],
        "lead": "冬の沖縄は、真夏のように海へ飛び込む旅とは少し違います。ただ、旅費が下がりやすく、混雑も落ち着く時期だからこそ、海遊びと観光をうまく組み合わせる価値があります。",
        "summary": [
            "冬でもシュノーケルなど主要な海遊びは可能。",
            "水中より、海から上がったあとの寒さと風対策が大事。",
            "海だけで終わらず、ホエールウォッチングや桜など冬の見どころも組み合わせやすい。",
        ],
        "fit_heading": "この組み方が向く人",
        "fit_paragraphs": ["冬に沖縄へ行くなら、真夏ほど海に全振りしない前提で考えると満足しやすいです。天気や風を見ながら、海と観光を半々で組むのが現実的です。"],
        "fit_list": ["冬でも少し海に入りたい", "旅費を抑えて沖縄へ行きたい", "ホエールウォッチングや桜も気になる"],
        "main_heading": "冬の沖縄旅で押さえたいこと",
        "main_paragraphs": ["平均気温は本土よりかなり暖かい一方、風が強い日は体感温度が下がります。服装は薄着だけで決めず、海辺や朝晩の羽織りを前提に考えたほうが安全です。"],
        "main_cards": [
            {
                "title": "海遊びはできる",
                "paragraphs": [
                    "シュノーケルなどの主要なアクティビティは冬でも開催されます。ウェットスーツ前提なら海の中は意外と平気でも、上がったあとがかなり寒く感じやすいです。",
                ],
                "bullets": ["ウェットスーツ前提", "海から上がったあとが寒い", "風が強い日は無理をしない"],
            },
            {
                "title": "冬ならではの見どころも足す",
                "paragraphs": [
                    "ホエールウォッチングや1月の桜など、冬の沖縄だからこそ入れやすい見どころがあります。海遊びと観光を分けて考えると旅程が組みやすいです。",
                ],
                "bullets": ["ホエールウォッチング", "今帰仁の桜", "街やホテルの冬イベント"],
            },
        ],
        "hotel_heading": "冬旅で合わせやすい宿の考え方",
        "hotel_intro": ["冬はホテルで温まる時間の価値も上がるため、大浴場や朝食、観光拠点としての使いやすさを見たほうが満足しやすいです。"],
        "hotels": [
            {
                "name": "那覇・本島拠点のホテル",
                "paragraphs": ["海遊びに全振りしないなら、那覇や本島中部を拠点にして、海・街・冬の観光を組み合わせるほうが動きやすいです。"],
                "bullets": ["街と海を分けて考えやすい", "悪天候でも組み替えしやすい"],
                "url": "https://www.okinawastory.jp/",
            },
            {
                "name": "離島で海遊び重視の宿",
                "paragraphs": ["離島に行く場合は、海に出られない時間も楽しめるホテルを選んだほうが冬はぶれにくいです。"],
                "bullets": ["ホテル時間も大事", "海況次第で代替が効くかを見る"],
                "url": "https://www.okinawastory.jp/",
            },
            {
                "name": "ホエールウォッチングを組みたい人の宿",
                "paragraphs": ["本島側で泊まると、冬の海遊びとホエールウォッチングを1つの旅にまとめやすいです。"],
                "bullets": ["本島拠点向き", "海と観光を組みやすい"],
                "url": "https://www.okinawastory.jp/",
            },
        ],
        "booking_intro": ["冬旅は天候の振れ幅があるため、海だけに寄せすぎないことが重要です。特に船に乗る日は体調管理も旅程の一部として考えたほうが安全です。"],
        "booking_cards": [
            {
                "title": "服装は薄着＋羽織り",
                "paragraphs": [
                    "日中は暖かくても、海辺や朝晩は寒く感じる日があります。薄手ダウンやパーカーのように、脱ぎ着しやすいものがあると安心です。",
                ],
            },
            {
                "title": "ホエールウォッチングは船酔い対策まで入れる",
                "paragraphs": [
                    "冬の定番ですが、揺れが強い日もあります。寝不足・二日酔い・朝ごはん抜きは避けたほうが無難です。",
                ],
            },
        ],
        "booking_list": ["羽織りものの用意", "海から上がったあとに着替えやすい服装", "船酔い対策"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "冬の沖縄旅に向く宿を比較する。", "cta": "冬の沖縄の宿を探す"},
            {"title": "航空券", "body": "オフシーズンの便を比較する。", "cta": "沖縄行きの航空券を探す", "secondary": "1"},
            {"title": "アクティビティ", "body": "シュノーケルやホエールウォッチングを比較する。", "cta": "冬のアクティビティを探す", "secondary": "1"},
        ],
        "sources": [
            ("おきなわ物語 公式", "https://www.okinawastory.jp/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["okinawa"], "area": "沖縄・冬旅", "card_labels": ["沖縄", "冬旅"],
    },
    {
        "slug": "first-okinawa-qa",
        "title": "初めての沖縄旅行Q&A｜日数・レンタカー・ホテルの選び方",
        "description": "初めての沖縄旅行で迷いやすい、どこへ行くか、何泊必要か、レンタカーが必要かを整理します。那覇・恩納村・北谷など、最初に見ておきたい考え方をまとめました。",
        "image": "https://images.unsplash.com/photo-1512100356356-de1b84283e18?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "初心者向け", "Q&A", "本島旅"],
        "lead": "初めての沖縄旅行は、情報が多すぎて決めきれないことがよくあります。最初に迷いやすい日数、エリア、レンタカー、ホテルの選び方だけを絞って整理しました。",
        "summary": [
            "初めてなら沖縄本島が選びやすい。",
            "観光するならレンタカー前提で考えたほうが楽。",
            "2泊3日より、できれば3泊4日あると余裕を作りやすい。",
        ],
        "fit_heading": "このQ&Aが向く人",
        "fit_paragraphs": ["初沖縄で、島選びからホテル選びまで一度に決めようとしている人向けです。まずは本島を前提にすると整理しやすくなります。"],
        "fit_list": ["沖縄に初めて行く", "本島と離島で迷っている", "ホテルの場所までまだ決まっていない"],
        "main_heading": "最初に整理したい3つのこと",
        "main_paragraphs": ["沖縄旅行の最初の分岐は、本島か離島か、何泊するか、レンタカーを借りるかです。この3つが決まると、ホテル選びもかなり楽になります。"],
        "main_cards": [
            {
                "title": "どこへ行く？",
                "paragraphs": [
                    "初めてなら沖縄本島が無難です。観光地、ホテル、食事の選択肢が多く、LCCも含めてアクセスも強いです。",
                ],
            },
            {
                "title": "何泊いる？",
                "paragraphs": [
                    "2泊3日でも行けますが、移動時間を考えると3泊4日のほうが余白を作りやすいです。特に本島は観光地が広く点在します。",
                ],
            },
            {
                "title": "レンタカーは必要？",
                "paragraphs": [
                    "本島観光なら基本は必要です。那覇市内だけならなくても過ごせますが、恩納村や北部へ出るなら前提で考えたほうが楽です。",
                ],
            },
        ],
        "hotel_heading": "最初に見やすいエリアとホテルの考え方",
        "hotel_intro": ["華やかなリゾート感なら北谷、王道の沖縄リゾートなら恩納村、と分けると考えやすいです。"],
        "hotels": [
            {
                "name": "北谷エリア",
                "paragraphs": ["海外っぽい雰囲気や街歩きも楽しみたい人向け。カフェやレストランがまとまりやすいです。"],
                "bullets": ["街と海のバランス", "レンタカーがなくても一部歩ける"],
                "url": "https://www.okinawastory.jp/",
            },
            {
                "name": "恩納村エリア",
                "paragraphs": ["沖縄らしい海沿いリゾートを楽しみたい人向け。ホテル選びの幅も広いです。"],
                "bullets": ["王道リゾート", "本島観光の拠点にもなる"],
                "url": "https://www.okinawastory.jp/",
            },
            {
                "name": "那覇市内",
                "paragraphs": ["初日や最終日だけ泊まるなら便利です。モノレールや空港アクセスを重視する場合に向きます。"],
                "bullets": ["空港アクセス", "街歩き", "前後泊向き"],
                "url": "https://www.okinawastory.jp/",
            },
        ],
        "booking_intro": ["最初の沖縄旅行では、全てを一度にやろうとすると詰まりがちです。最初の1回は“行く場所を絞る”ことを優先したほうが満足しやすいです。"],
        "booking_cards": [],
        "booking_list": ["本島か離島か", "何泊するか", "レンタカーをどこで借りるか"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "沖縄本島の宿をエリア別に比較する。", "cta": "沖縄本島の宿を探す"},
            {"title": "航空券", "body": "那覇行きの便を比較する。", "cta": "那覇行きの航空券を探す", "secondary": "1"},
            {"title": "レンタカー", "body": "本島観光に向く移動手段を比較する。", "cta": "レンタカーを探す", "secondary": "1"},
        ],
        "sources": [
            ("おきなわ物語 公式", "https://www.okinawastory.jp/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["okinawa"], "area": "沖縄・本島", "card_labels": ["沖縄", "初心者向け"],
    },
    {
        "slug": "okinawa-anniversary-hotels-3",
        "title": "沖縄本島で記念日旅に向くホテル3選",
        "description": "沖縄本島で記念日旅をするなら、北谷の大人っぽさ、読谷の記憶に残るホスピタリティ、名護の王道高級リゾートで選び方が分かれます。おすすめの3軒を整理します。",
        "image": "https://images.unsplash.com/photo-1473116763249-2faaef81ccda?auto=format&fit=crop&w=1400&q=82",
        "labels": ["沖縄", "本島", "記念日", "ホテル3選"],
        "lead": "沖縄本島の記念日旅は、海が見えるだけでは足りません。食事の取り方、ホテルの雰囲気、帰り道まで含めて“記憶に残るか”で選ぶと、候補はかなり絞れます。",
        "summary": [
            "北谷で歩いて食事に行きたいならMBギャラリー。",
            "ホスピタリティや記憶に残る滞在ならホテル日航アリビラ。",
            "王道の大人リゾートならザ・ブセナテラス。",
        ],
        "fit_heading": "この選び方が向く人",
        "fit_paragraphs": ["記念日旅では、客室そのものよりも、夕方から夜の流れが心地いいかどうかが大事です。本島はエリアごとに空気感がはっきり違います。"],
        "fit_list": ["大人二人でゆっくり過ごしたい", "食事まで含めて失敗したくない", "本島でホテル選びに迷っている"],
        "main_heading": "本島の記念日ホテルで分かれるポイント",
        "main_paragraphs": ["歩いて街へ出られる北谷、ホスピタリティの読谷、王道高級リゾートの名護。この3つでかなり性格が分かれます。"],
        "hotel_heading": "記念日旅で候補にしたい3軒",
        "hotel_intro": ["Yahoo記事で実際に使っていた軸に沿って、沖縄本島の記念日候補を3軒に絞りました。"],
        "hotels": [
            {
                "name": "MBギャラリーチャタン by ザ・テラスホテルズ",
                "paragraphs": [
                    "北谷で大人っぽい雰囲気を取りたい人向けです。車を置いて歩いて食事に行けるのが、本島の記念日旅ではかなり強いです。",
                ],
                "bullets": ["北谷の街歩き", "ラウンジ利用", "大人向けの空気感"],
                "url": "https://mb-gallery.jp/",
            },
            {
                "name": "ホテル日航アリビラ",
                "paragraphs": [
                    "記念日に“印象が残る”ホテルを探すなら候補です。香りや建物、朝食など、旅の記憶に残りやすい要素が揃っています。",
                ],
                "bullets": ["ホスピタリティ", "読谷の空気感", "記憶に残りやすい"],
                "url": "https://www.alivila.co.jp/",
            },
            {
                "name": "ザ・ブセナテラス",
                "paragraphs": [
                    "王道の高級リゾートを探すなら外しにくい一軒です。自然音が主役の落ち着いた雰囲気で、大人の記念日旅に向きます。",
                ],
                "bullets": ["名護の王道高級リゾート", "大人向け", "特別なディナーも組みやすい"],
                "url": "https://www.terrace.co.jp/busena/",
            },
        ],
        "booking_intro": ["沖縄本島の記念日旅は、ホテルの中だけで完結するか、外に食事へ出るかを先に決めると選びやすいです。"],
        "booking_cards": [],
        "booking_list": ["食事を外で取るか", "車を置いて歩けるか", "客室より空気感を優先するか"],
        "affiliate_cards": [
            {"title": "宿泊予約", "body": "沖縄本島の記念日向けホテルを比較する。", "cta": "記念日向けの宿を探す"},
            {"title": "航空券", "body": "那覇行きの便を比較する。", "cta": "那覇行きの航空券を探す", "secondary": "1"},
            {"title": "レンタカー", "body": "本島リゾート滞在の移動手段を比較する。", "cta": "レンタカーを探す", "secondary": "1"},
        ],
        "sources": [
            ("MBギャラリーチャタン by ザ・テラスホテルズ 公式", "https://mb-gallery.jp/"),
            ("ホテル日航アリビラ 公式", "https://www.alivila.co.jp/"),
            ("ザ・ブセナテラス 公式", "https://www.terrace.co.jp/busena/"),
        ],
        "published": "2026.06.07", "updated": "2026.06.07", "published_iso": "2026-06-07", "updated_iso": "2026-06-07",
        "tags": ["anniversary", "couple", "okinawa"], "area": "沖縄・本島", "card_labels": ["本島", "記念日"],
    },
]


BASE_ARTICLES = [
    {
        "title": "指宿ひとり旅｜砂むし温泉と海沿い宿で過ごす1泊2日",
        "area": "鹿児島・指宿",
        "date": "2026.06",
        "tags": ["solo", "onsen", "carfree"],
        "label": ["ひとり旅", "温泉"],
        "image": "https://images.unsplash.com/photo-1542640244-7e672d6cef4e?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/ibusuki-solo-trip/",
    },
    {
        "title": "沖縄離島は1泊2日で行ける？短い休みで選びたい島を整理する",
        "area": "沖縄",
        "date": "2026.06",
        "tags": ["solo", "couple", "okinawa"],
        "label": ["沖縄離島", "週末旅行"],
        "image": "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/okinawa-islands-2days/",
    },
    {
        "title": "男鹿半島は2泊3日でゆっくり行きたい。なまはげと秋田市内の文化旅",
        "area": "秋田・男鹿",
        "date": "2026.06",
        "tags": ["couple", "solo"],
        "label": ["文化旅", "2泊3日"],
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/oga-solo-trip/",
    },
    {
        "title": "奈良カップル旅｜記念日に使いやすいホテルと街歩きで回る1泊2日",
        "area": "奈良",
        "date": "2026.06",
        "tags": ["couple", "anniversary", "carfree"],
        "label": ["カップル", "記念日"],
        "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/nara-couple-trip/",
    },
    {
        "title": "金沢は車なし旅に向いている？ひとりでもカップルでも楽しむ1泊2日",
        "area": "石川・金沢",
        "date": "2026.06",
        "tags": ["solo", "couple"],
        "label": ["街歩き", "グルメ"],
        "image": "https://images.unsplash.com/photo-1528164344705-47542687000d?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/kanazawa-city-walk/",
    },
    {
        "title": "箱根は記念日旅行に向いている？温泉宿とフリーパスで回る1泊2日",
        "area": "神奈川・箱根",
        "date": "2026.06",
        "tags": ["anniversary", "couple", "onsen"],
        "label": ["箱根", "記念日"],
        "image": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/hakone-anniversary-trip/",
    },
    {
        "title": "由布院は週末温泉旅に向いている？街歩きと宿時間で組む1泊2日",
        "area": "大分・由布院",
        "date": "2026.06",
        "tags": ["onsen", "couple", "solo"],
        "label": ["由布院", "週末旅行"],
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/yufuin-onsen-weekend/",
    },
]


LOCATION_ARTICLES = [
    {
        "title": "指宿",
        "area": "鹿児島",
        "date": "温泉と車なし旅",
        "label": ["ひとり旅", "砂むし温泉"],
        "image": "https://images.unsplash.com/photo-1542640244-7e672d6cef4e?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/ibusuki-solo-trip/",
    },
    {
        "title": "沖縄離島",
        "area": "沖縄",
        "date": "弾丸でも行きやすい島",
        "label": ["海", "週末旅行"],
        "image": "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/okinawa-islands-2days/",
    },
    {
        "title": "男鹿半島",
        "area": "秋田",
        "date": "文化旅と温泉",
        "label": ["なまはげ", "ドライブ"],
        "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/oga-solo-trip/",
    },
    {
        "title": "奈良",
        "area": "奈良",
        "date": "街歩きと記念日",
        "label": ["歴史", "カップル"],
        "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/nara-couple-trip/",
    },
    {
        "title": "箱根",
        "area": "神奈川",
        "date": "温泉と記念日",
        "label": ["フリーパス", "カップル"],
        "image": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/hakone-anniversary-trip/",
    },
    {
        "title": "由布院",
        "area": "大分",
        "date": "温泉と週末旅行",
        "label": ["街歩き", "のんびり"],
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/yufuin-onsen-weekend/",
    },
    {
        "title": "石垣島",
        "area": "沖縄",
        "date": "ひとり旅と港拠点",
        "label": ["石垣島", "ホテル選び"],
        "image": "https://images.unsplash.com/photo-1493558103817-58b2924bce98?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/ishigaki-solo-hotels-3/",
    },
    {
        "title": "宮古島",
        "area": "沖縄",
        "date": "海とホテル時間",
        "label": ["宮古島", "リゾート"],
        "image": "https://images.unsplash.com/photo-1493558103817-58b2924bce98?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/miyakojima-hotels-3/",
    },
    {
        "title": "那覇",
        "area": "沖縄",
        "date": "立地重視のホテル選び",
        "label": ["那覇", "街歩き"],
        "image": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=900&q=80",
        "url": "/articles/naha-hotels-3/",
    },
]


def write_articles() -> None:
    for article in ARTICLES:
        canonical = f"https://tabi.ayumi-biz.com/articles/{article['slug']}/"
        sections = build_sections(article)
        article_sections = "\n\n".join(section(section_id, title, body) for section_id, title, body in sections)
        toc = "\n".join(
            f'<a href="#{section_id}">{html.escape(title)}</a>' for section_id, title, _ in sections
        )
        page = ARTICLE_TEMPLATE.format(
            title=html.escape(str(article["title"])),
            description=html.escape(str(article["description"])),
            canonical=canonical,
            image=html.escape(str(article["image"])),
            json_ld=article_json_ld(article, canonical),
            hero_labels="\n".join(f"<span>{html.escape(label)}</span>" for label in article["labels"]),  # type: ignore[index]
            lead=html.escape(str(article["lead"])),
            article_sections=article_sections,
            toc_links=toc,
            published=html.escape(str(article["published"])),
            updated=html.escape(str(article["updated"])),
        )
        target = OUTPUT_DIR / str(article["slug"]) / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        write_text_utf8_bom(target, page)


def update_index() -> None:
    all_articles = BASE_ARTICLES + [
        {
            "title": article["title"],
            "area": article["area"],
            "date": "2026.06",
            "tags": article["tags"],
            "label": article["card_labels"],
            "image": article["image"],
            "url": f"/articles/{article['slug']}/",
        }
        for article in ARTICLES
    ]
    content = INDEX_PATH.read_text(encoding="utf-8")
    articles_js = json.dumps(all_articles, ensure_ascii=False, indent=6)
    locations_js = json.dumps(LOCATION_ARTICLES, ensure_ascii=False, indent=6)
    content = re.sub(r"const articles = \[.*?\n    \];", f"const articles = {articles_js};", content, count=1, flags=re.S)
    content = re.sub(r"const locationArticles = \[.*?\n    \];", f"const locationArticles = {locations_js};", content, count=1, flags=re.S)
    write_text_utf8_bom(INDEX_PATH, content)


def update_sitemap() -> None:
    static_urls = [
        ("https://tabi.ayumi-biz.com/", "1.0", "weekly"),
        ("https://tabi.ayumi-biz.com/about.html", "0.4", "monthly"),
        ("https://tabi.ayumi-biz.com/contact.html", "0.4", "monthly"),
        ("https://tabi.ayumi-biz.com/privacy.html", "0.4", "monthly"),
        ("https://tabi.ayumi-biz.com/ads.html", "0.4", "monthly"),
        ("https://tabi.ayumi-biz.com/finder.html", "0.9", "weekly"),
    ]
    article_urls = [
        "https://tabi.ayumi-biz.com/articles/ibusuki-solo-trip/",
        "https://tabi.ayumi-biz.com/articles/ibusuki-carfree/",
        "https://tabi.ayumi-biz.com/articles/anniversary-onsen-ryokan/",
        "https://tabi.ayumi-biz.com/articles/carfree-onsen-destinations/",
        "https://tabi.ayumi-biz.com/articles/okinawa-islands-2days/",
        "https://tabi.ayumi-biz.com/articles/oga-solo-trip/",
        "https://tabi.ayumi-biz.com/articles/nara-couple-trip/",
        "https://tabi.ayumi-biz.com/articles/kanazawa-city-walk/",
        "https://tabi.ayumi-biz.com/articles/hakone-anniversary-trip/",
        "https://tabi.ayumi-biz.com/articles/yufuin-onsen-weekend/",
    ] + [f"https://tabi.ayumi-biz.com/articles/{article['slug']}/" for article in ARTICLES]
    items: list[str] = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, priority, freq in static_urls:
        items.append(
            dedent(
                f"""\
                <url>
                  <loc>{loc}</loc>
                  <lastmod>2026-06-07</lastmod>
                  <changefreq>{freq}</changefreq>
                  <priority>{priority}</priority>
                </url>
                """
            ).strip()
        )
    for loc in article_urls:
        items.append(
            dedent(
                f"""\
                <url>
                  <loc>{loc}</loc>
                  <lastmod>2026-06-07</lastmod>
                  <changefreq>monthly</changefreq>
                  <priority>0.8</priority>
                </url>
                """
            ).strip()
        )
    items.append("</urlset>")
    SITEMAP_PATH.write_text("\n".join(items) + "\n", encoding="utf-8")


def main() -> None:
    write_articles()
    update_index()
    update_sitemap()
    print(f"generated {len(ARTICLES)} okinawa articles")


if __name__ == "__main__":
    main()
