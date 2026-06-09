# 記事運用メモ

## いまの前提

- 記事一覧とトップページの表示制御は `assets/article-registry.js` でまとめて管理する。
- `index.html` と `articles/index.html` に記事データを直書きしない。
- 沖縄記事生成スクリプト `scripts/generate_okinawa_articles.py` は、記事ページ生成と sitemap 更新だけを担当する。
- sitemap は `scripts/build_sitemap.py` で再生成する。

## レジストリで持つ項目

- `status`
  - `published`: 公開中
  - `scheduled`: 公開予約。`publishAt` の日時を過ぎたら表示対象
  - `review`: 下書き・確認中。公開面には出さない
  - `hidden`: 非表示。URL を知っていれば見せる想定の記事を置くときに使う
- `publishAt`
  - `scheduled` のときに使う
- `publishedAt`
  - 初回公開日
- `updatedAt`
  - リライト日
- `imageStatus`
  - `none` / `temp` / `done`
- `rewriteStatus`
  - `review` / `reviewed` / `fixed`
- `factCheckStatus`
  - `pending` / `done`
- `qualityChecked`
  - 一覧上で自分用の確認済み印を出すための真偽値
- `topFeature`
  - トップの「自分に合った旅を見つける」に出すかどうか
- `noteFeature`
  - トップの「旅のひとりごと」に出すかどうか

## 予約投稿の扱い

1. 記事 HTML を先に作る
2. `assets/article-registry.js` に記事を追加する
3. `status: "scheduled"` を入れる
4. `publishAt` に公開日時を入れる
5. 時刻を過ぎたらトップと一覧に自動で出る

### 注意

- いまの仕組みは、トップと記事一覧の表示制御を自動化するもの。
- `sitemap.xml` は静的ファイルなので、予約日時を過ぎても自動では更新されない。
- 検索向けの公開日も揃えたいときは、公開日に合わせて再デプロイする。
- 記事 HTML 自体は静的に置かれるため、URL を知っていれば公開前でも直接開ける。完全な公開制御が必要なら、将来的にはビルド時の出し分けか CMS / backend を入れる。

## 非表示記事の扱い

- 重複記事、比較用の旧記事、URL は残したいが一覧には出したくない記事は `status: "hidden"` にする。
- 例: SEO が弱い旧記事を残しつつ、一覧やトップからは下げるとき。

## 自分用の確認表示

- `articles/index.html?admin=1`
- または `articles/index.html#admin`

このときだけ、記事一覧に以下の内部メモが出る。

- 公開状態
- 画像の準備状況
- リライト状況
- 事実確認状況

通常の閲覧者には出ない。

## 更新時の基本手順

1. 記事本文を直す
2. 必要なら `updatedAt` を更新
3. 仮画像なら `imageStatus: "temp"`、差し替え完了なら `imageStatus: "done"` にする
4. リライト完了なら `rewriteStatus: "fixed"` にする
5. 事実確認が終わったら `factCheckStatus: "done"` にする
6. 仕上がったら `qualityChecked: true`
7. 最後に `scripts/build_sitemap.py` を実行する

## 新規記事を追加するときの補助

- 公開記事のサンプル: `knowledge/article-entry-template.published.json`
- 予約投稿のサンプル: `knowledge/article-entry-template.scheduled.json`
- レジストリ追加用の整形: `scripts/render_registry_entry.py`
- 楽天リンクの差し込み設計: `knowledge/rakuten-affiliate-operations.md`
- 記事ごとの楽天導線サンプル: `knowledge/article-affiliate-template.json`
- 楽天導線の整形: `scripts/render_affiliate_cards.py`

実行例:

```powershell
& "C:\Users\ayuay\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\render_registry_entry.py knowledge\article-entry-template.scheduled.json
```

出力されたオブジェクトを `assets/article-registry.js` に貼り付ける。

楽天導線カードの生成例:

```powershell
& "C:\Users\ayuay\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts\render_affiliate_cards.py knowledge\article-affiliate-template.json
```

出力された配列を、記事生成スクリプトの `affiliate_cards` や、記事HTML内の予約導線に使う。

## 今後の拡張候補

- 画像差し込み予定の空欄をレジストリ連動にする
- `publishedAt` / `updatedAt` から sitemap の `lastmod` を自動生成する
- Markdown または JSON からレジストリを自動生成する
