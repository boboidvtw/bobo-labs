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

- **2026-06-03** — sitemap.xml 全面補齊（SEO 基建，變現第一步「裝儀表」）：URL 從 16 → 44（formulas 10→15 全收錄、writing 4→27 全收錄），修正 daily log 的 lastmod。為提交 Google Search Console 鋪路，讓 Google 看得到全部內容。
  Rebuilt sitemap.xml for full coverage: 16 → 44 URLs (all 15 formula articles + all 27 writing posts), with correct lastmod dates. Prep for Google Search Console submission so Google can index everything.
- **2026-06-03** — 由 /boboweb 補發 5 篇積壓 daily log（修 canonical 治本後）：
  `2026-06-01-nomad-hub-discover-complete.html`、`2026-05-31-nomad-hub-discover-registry.html`、`2026-05-30-nomad-hub-phase5-week1.html`、`2026-05-29-bobo-autopublish-v2.html`、`2026-05-29-boboweb-decision-rules.html`。
  根因：/bobo-draft-pending 模板未生成 `<link rel="canonical">`，autopublish QA gate 的 structure 檢查連續擋下 → 草稿堆積。已修模板加 canonical 規則，並回補 5 篇 head 的 canonical（另修 2026-06-01 一篇缺漏的 viewport meta）。Index Writing 區依時間倒序插入。
  Backfilled 5 stuck daily-log drafts via /boboweb after fixing the canonical root cause (draft template now emits canonical; QA gate no longer blocks). Also restored a missing viewport meta on the 2026-06-01 article.
- **2026-06-03** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-06-02-nomad-hub-treesitter-analysis.html`（先 spike 再選路 — nomad-hub Analysis tab 從失效 CLI 到 tree-sitter 知識圖；沒有 CLI ≠ 不能用，spike 驗 cwd 獨立性，TDD 五步，測試 198→213）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-06-03.
- **2026-05-29** — 由 /boboweb 第二輪核可 5 篇 /formulas/ 子站文章：
  `formulas/arithmetic-mean.html`（#13 數學 Free · 平均值為何說謊、中位數什麼時候誠實）、
  `formulas/distance-formula.html`（#25 數學 Free · 勾股定理的座標版本）、
  `formulas/mortgage-payment.html`（#40 金融 Free · 等額本息背後的 30 年數學）、
  `formulas/newtons-second-law.html`（#70 物理 Free · F=ma 為何力會改變運動）、
  `formulas/universal-gravitation.html`（#79 物理 Free · 為何月球不會掉下來）。
  formulas/index.html：3 個 placeholder 替換為 active card、2 張新卡片（#13、#40）插入 active 區末端、#79 萬有引力 Tier 從 Pro→Free（採文章 eyebrow 為準）；物理分類計數 12F/9P→13F/8P、數學註腳 26→25 條、金融註腳 8→7 條。同輪清掉 `writing/_pending/_patch_articles.py` 一次性補丁腳本。
  Promoted 5 /formulas/ articles via /boboweb second round on 2026-05-29 (math/finance/physics, all Free)
  and cleaned up one-shot _patch_articles.py from _pending/.
- **2026-05-29** — 由 /boboweb 核可 1 篇文章：
  `2026-05-27-supercalc-monetization-phase1.html`（三件事一次做完 — ∑ Calc 贊助按鈕、公式分層 markdown、/formulas/ 子站初版十篇；AskUserQuestion 一輪收四個阻塞決策後六小時無中斷推進）。
  Index Writing 區依時間倒序插入。
  Promoted 1 draft from `_pending/` via /boboweb on 2026-05-29 (∑ Calc monetization Phase 1-3:
  sponsor button, formula tiering, and /formulas/ subsite launch).
- **2026-05-26** — 由 /boboweb 核可 3 篇文章：
  `2026-05-25-grid-bot-tick-verified.html`（grid bot tick 修復盤中驗證 — BUY 0%→100% PENDING，模擬 SELL 賣空限制，4/29 以來靜默失敗解謎）、
  `2026-05-24-auto-publish-pipeline.html`（日誌堆著不上站 — 三個零件把 journal→文章流程自動化，自動化拆 A/B/C，gitignored 隔本地與對外效果）、
  `2026-05-20-bobo-labs-publish-flow.html`（「上站」這兩個字到底許可了哪些動作 — 授權粒度拆四級，AskUserQuestion 問範圍不問是否，until-loop 比 sleep 誠實）。
  Index Writing 區依時間倒序插入；5/24、5/20 兩篇昨日 LLM 紅線跳過，今日重新評估通過。
  Promoted 3 drafts from `_pending/` via /boboweb on 2026-05-26 (grid bot tick verification,
  auto-publish pipeline design, and authorization granularity for publish flow).
- **2026-05-25** — 由 /boboweb 核可 3 篇文章：
  `2026-05-24-stock-grid-tick-fix.html`（台股升降單位沒對齊的 CRITICAL — 423 筆 CANCELLED 自 4/29 起靜默失敗，snap_to_tick 修法 + 14 條回歸）、
  `2026-05-18-skills-40-eval.html`（40 個 Skills 評估 — 32 已有等效，Superpowers 12/14 覆蓋不值整包，外科式單抽方法論）、
  `2026-05-15-skills-governance-v1.html`（215 個 Skills 治理問題 — 版本控制／稽核／測試三系統一天建完，hook 三鐵律）。
  Index Writing 區依時間倒序插入。
  Promoted 3 drafts from `_pending/` via /boboweb on 2026-05-25 (tick alignment CRITICAL fix,
  40-skills evaluation methodology, and skills governance v1.0 architecture).
- **2026-05-24** — 補上最後一篇老 journal：`2026-05-14-nomad-recon-sprint-d.html`
  （subagent-driven 切片開發 + graceful degradation 寫進型別 + 187/187 tests passing）。
  lookback 14 天範圍內落差歸零。
  Backfilled the last older journal — nomad-recon Sprint D log on subagent-driven slicing
  and graceful-degradation contracts; gap-reminder backlog now clear within 14-day lookback.
- **2026-05-24** — 再補貼 3 篇先前工作的 Writing 文章（5/15–5/18 的舊落差）：
  `2026-05-18-pages-cert-stuck.html`（GitHub Pages 憑證 pipeline 卡死的檔案層級重置解法）、
  `2026-05-17-bobo-labs-origin.html`（站台「為何存在」的四輪需求釐清歷程）、
  `2026-05-15-test-the-tests.html`（測試框架自己也得被測——3 失敗中 1 真實 bug + 2 規則偽陽性）。
  Index Writing 區依時間倒序插入。
  Backfilled 3 more daily-log articles for older 5/15–5/18 work (GitHub Pages cert
  troubleshooting, site-origin Q&amp;A, and a meta-lesson on testing the test framework).
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
