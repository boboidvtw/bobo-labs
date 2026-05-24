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

- **2026-05-24** — 補貼 4 篇先前工作的 Writing 文章（5/21–5/22 的日誌落差）：
  `2026-05-22-supercalc-a11y.html`（∑ Calc v3.6.0 WCAG 強化 + 5 個耦合陷阱）、
  `2026-05-22-supercalc-v359.html`（nCr 大數溢位 + 三角浮點殘渣 + 公式破百）、
  `2026-05-22-skills-governance-audit-and-llm.html`（v1.2 audit 區塊 + v1.3 LLM 規則 + dead-weight 訊號）、
  `2026-05-21-supercalc-click-test.html`（90 案例點擊測試揪 2 真實 bug + 物理常數 SI 2019 升級）。
  Index Writing 區依時間倒序置頂。
  Backfilled 4 daily-log articles for prior 5/21–5/22 work that had not yet been posted;
  pinned to top of Writing in reverse chronological order.
- **2026-05-22** — 新增 Writing 文章 `2026-05-22-skills-governance-phase4.html`（Skills Governance
  Phase 4 日誌：觀測儀表板、六訊號演化引擎、為「資料不足」設計的空狀態、為治理框架自己補 20 個單元測試）。
  Index Writing 區置頂新條目。
  Added daily-log article on Skills Governance Phase 4 (observability dashboard, evolution engine, unit tests); pinned to top of Writing.
- **2026-05-21** — 新增 Writing 文章 `2026-05-21-formula-audit.html`（∑ Calc v3.5.7 公式庫
  一致性深審日誌：揪出一條掛錯名的「目標心率」公式與三份和實機脫節的文件）。
  Index Writing 區置頂新條目。
  Added daily-log article on a formula-library consistency audit; pinned to top of Writing.
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
