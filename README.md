# 🏯 温泉休憩室 空き部屋・予約状況リアルタイム管理システム

温泉休憩室の客室状態・顧客フロー・認証付きリアルタイム管理Webアプリです。フロントスタッフが客室の空き状況・清掃状態・受付状況を一画面で把握できます。

🖥️ **[デモを見る](https://dogoakiheyasysytem-tama3.tatagen.workers.dev)**

---

## ✨ 主な機能

- **客室状態管理** — 空室・清掃中・使用中・使用停止を一覧で管理
- **顧客フロー管理** — チェックイン・チェックアウト・部屋割り当てのフローを管理
- **受付・待合管理** — 待機中ゲストの受付番号発券と呼び出し管理
- **認証機能** — スタッフログイン・セッション管理
- **リアルタイム同期** — Cloudflare KV によるリアルタイム状態共有

## 🛠️ 技術スタック

| 分類 | 技術 |
|------|------|
| バックエンド | Python / FastAPI (Starlette) |
| データ | Cloudflare KV（リアルタイム状態管理） |
| デプロイ | Cloudflare Workers（Python Workers） |

## 🚀 ローカル実行

**前提:** Python 3.11+ / Node.js

```bash
git clone https://github.com/tatagen/dogoakiheyasysytem_tama3.git
cd dogoakiheyasysytem_tama3
pip install -r requirements.txt
npx wrangler dev
```

## 🚀 デプロイ（Cloudflare Workers）

```bash
npx wrangler login
npx wrangler deploy
```
