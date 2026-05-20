# Bobo Labs

> 邊學邊做，做完就分享。 — Learn by doing, share when done.

Personal corner / 個人角落：<https://labs.moneyai168.com>

Hand-written Swiss-style static site. No framework, no build step, zero dependencies.
手寫 Swiss 風格靜態站，無框架、無建置、零依賴。

## Structure / 結構

```
index.html          Single-page home (Work / Writing / Contact)
styles.css          Design tokens + layout
writing/
  article.css       Article-layer styles (reuses index tokens)
  *.html            Long-form notes linked from the Writing section
CNAME               Custom domain (labs.moneyai168.com)
```

## Changelog / 變更紀錄

- **2026-05-20** — 新增 Writing 文章 `2026-05-20-supercalc-day.html`（∑ Calc 一日深審日誌：
  v3.5.3→v3.5.6 三版連推、手機 Bug C 浮動列、揪出兩個 latent engine bug、Pro 全 8 賣點端對端驗證）。
  Index Writing 區置頂新條目，採時間倒序。
  Added daily-log article and pinned it to top of Writing section (reverse chronological).
- **2026-05-18** — Writing & Docs 區改為真實連結；新增 3 篇文章頁面
  （∑ Calc Pro 架構演進、Antigravity-Stack 工程設計、Skills Governance 三維治理）。
  Writing entries are now real links; added 3 article pages.
- **2026-05-18** — 初始站台上線（CNAME + 真實專案內容）。Initial site live.

## Local preview / 本地預覽

```bash
python3 -m http.server 4321 --directory .
```
