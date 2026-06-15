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

- **2026-06-15** — 由 /boboweb 核可發布 5 篇文章：
  `2026-06-14-three-layer-cache-debug.html`（一個 I/l typo 致第三方 SDK 靜默失效 11 天、SW/HTTP/CDN 三層快取與 ground truth 除錯方法論）、
  `2026-06-14-projects-board-workflow.html`（用會自動載入的 memory 檔在終端 AI 助理建立跨對話專案看板）、
  `2026-06-11-headroom-learning-m0-m6.html`（一天 TDD 重建 headroom M0–M6、跨語言 byte-for-byte parity gate）、
  `2026-06-09-bobo-labs-qa-context-aware.html`（autopublish QA gate 高危專名硬擋＋通用敏感詞語境感知兩層）、
  `2026-05-31-nomad-hub-registry-loop.html`（emoji 炸 JSON 序列化、nomad-hub scan→import 讀寫邊界）。
  Index Writing 區依時間倒序插入、sitemap 重生、清空 _pending/ 待審草稿。
  Promoted 5 drafts from _pending/ via /boboweb on 2026-06-15.

- **2026-06-15** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-14-headroom-m8-lazy-registration.html`（register_ccr_tool lazy 掛工具修復跨 process 快取歸零、parity gate 436→436）、
  `2026-06-12-headroom-cache-wrap-debug.html`（錄音重放法 stage bisect 找出 cache_read 63695→0 根因）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-15.

- **2026-06-14** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-12-headroom-live-traffic.html`（curl 三組實測 · cache 全命中 · input_tokens 省 81.6% · SSE 照穿）、
  `2026-06-02-nomad-hub-analysis-tab.html`（tree-sitter 離線確定性分析 · LLM 語意降級 · 213→256 tests）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-14.

- **2026-06-13** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-12-headroom-m7-axum-proxy.html`（axum HTTP proxy · SSE 重切不變量 · byte-faithful 七個整合測試全綠）、
  `2026-05-31-understand-anything-plugin.html`（1200 個 .py 知識圖 · 7 phase pipeline · import 依賴顯式化）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-13.

- **2026-06-12** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-04-nomad-hub-portowner-fix.html`（後端 304 tests 全綠但前端 ReferenceError，Node vm sandbox 跨語言守衛，RED 先讓測試 fail，cache bust 同 commit）、
  `2026-06-02-nomad-hub-semantic-layer.html`（tree-sitter 知識圖加 LLM 語意層，可插拔 claude/gemma，降級 heuristic 保底，背景 job 避免同步等 77 秒）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-12.

- **2026-06-11** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-06-10-bobo-labs-gsc-first-index.html`（技術 SEO 就緒兩個月 GSC 索引仍 0，首次手動叩關 5 篇理財公式集群，topical cluster 策略 + 配額管理）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-06-11.

- **2026-06-10** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-03-stock-grid-bot-ops-recovery.html`（launchd 排程不補跑 + session_state 跨 restart 消失 + 靜默失效比崩潰危險，三層補強讓交易機器人重新可信）、
  `2026-06-03-canonical-fix-autopublish.html`（grep 命中 ≠ 結構正確，canonical 放錯位置不是缺少，QA gate 只擋不修，log 括號說明是真診斷）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-10.

- **2026-06-09** — 由 /boboweb 核可發布 1 篇文章：
  `2026-06-07-qa-pipeline-false-positives.html`（關鍵字誤判讓草稿永遠卡死的 meta 故事）。
  此前因 autopublish QA #1 純關鍵字硬擋 `secret`/`token` 把安全討論誤判紅線而卡死；連帶治本 QA #1 改為「高危專名硬擋 + 通用詞語境感知」分層判定，安全討論放行、真密鑰仍擋。
  Promoted 1 draft from _pending/ via /boboweb on 2026-06-09; also fixed QA #1 keyword false-positives.

- **2026-06-09** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-07-skills-dedup-finale.html`（Skills 程式庫去重收尾，198 → 179，三段安全刪除法 + grep 假陽性教訓）、
  `2026-06-05-stock-grid-bot-cooldown.html`（防呆寫在執行點才擋所有 caller，start_bot.sh 兜底 + 46 tests pass）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-09.

- **2026-06-08** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-07-formula-seo-breadcrumb.html`（15 篇公式頁補齊 BreadcrumbList + 內部連結，冪等 Python 腳本一次搞定 4 個孤兒頁）、
  `2026-06-05-stock-grid-bot-race-fix.html`（stop_flag cool-down 從 menubar 移到 start_bot.sh 兜底，46/46 tests PASS）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-08.

- **2026-06-07** — 由 /boboweb 人工核可解套 3 篇 QA 卡關草稿並補齊 sitemap：
  `2026-05-20-supercalc-pro-verify.html`（∑ Calc Pro 7 個賣點端到端驗收）、
  `2026-05-20-supercalc-v355-v356.html`（科學記號 e 與 toFixed underflow 兩個 latent engine bug）、
  `2026-06-03-nomad-hub-phase5-six-deliverables.html`（Phase 5 六項交付收尾）。
  三篇皆遭 autopublish QA gate 誤判卡死（token/secret 關鍵字命中、一處錯字），確認無紅線後人工修用詞發布。順帶補齊 sitemap 落差 46→53 URL（autopublish 發文流程未同步 sitemap，含 6/4 漏的 4 篇），writing 36 篇全涵蓋。
  Unblocked 3 QA-stuck drafts via /boboweb (keyword false-positives + a typo; fixed wording after confirming no red-line content) and backfilled sitemap 46→53 URLs covering all 36 writing posts on 2026-06-07.

- **2026-06-06** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-04-nomad-hub-gemma-multiturn.html`（Gemma 多輪持久對話 UI + v0.2.0 切版：雙模式設計、首則自動命名 session、__version__ 單一來源）、
  `2026-06-04-nomad-hub-frontend-test-vm.html`（Node vm sandbox 為純 Python 專案加前端守衛測試：portOwnerLabel 四態覆蓋、pytest 整合、先紅後綠驗證）。
  Index Writing 區依時間倒序插入頂部（同日既有文章之前）。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM 自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-06.

- **2026-06-05** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-04-bobo-labs-stage0-metrics.html`（GSC 0 頁索引紀實：sitemap 16→46、CF Web Analytics 全站注入、UTM 基準線建立）、
  `2026-06-04-skills-dedup-shared-engine.html`（Skills 去重第三輪 183→179：description 相似不等於功能重複，共用引擎模式辨認）。
  Index Writing 區依時間倒序插入頂部。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM 自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-05.

- **2026-06-04** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-05-20-supercalc-v353-audit.html`（v3.5.3 深審：SEO 教學區從未渲染、Stored XSS、y= 前綴誤判三個 latent bug）、
  `2026-05-20-supercalc-bug-c.html`（純 CSS 修復手機閉合括號消失，bottom-fixed 浮動列零 DOM 改動）。
  Index Writing 區依時間倒序插入同日條目前。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM 自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-04.
- **2026-06-04** — 變現策略階段 0「裝儀表」（三項）：
  ① sitemap.xml 全面補齊 16 → 46 URL（formulas 全 15 篇、writing 全 29 篇，補回先前漏掉的 2 篇 05-20 文章），修正 lastmod，為 Google Search Console 提交鋪路。
  ② 全站 46 頁注入 Cloudflare Web Analytics（零 cookie，符合隱私導向），開始量測頁面流量與來源。
  ③ 15 篇 formula 文章的 CTA 連結埋 UTM（utm_source=bobolabs），為「formulas → ∑ Calc」跨站轉換歸因鋪路。
  Stage 0 "instrumentation" for monetization: rebuilt sitemap to true full coverage (16 → 46 URLs), added cookieless Cloudflare Web Analytics to all 46 pages, and UTM-tagged the 15 formula CTA links for cross-site conversion attribution.
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
