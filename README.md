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

- **2026-09-05**（今日）— 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/sphere-volume.html`（#7 · 數學 · Free，阿基米德「球為外接圓柱三分之二」的推導、
  直徑 πd³/6 與周長 C³/(6π²) 兩條換算、由體積反解半徑 ∛(3V/4π)，含半球 (2/3)πr³、
  球殼 (4/3)π(R³−r³)、把直徑當半徑的 8 倍錯誤與漏掉 4/3 的 25% 短缺）。
  Formula 卡片由 placeholder 轉為連結（66 → 65），Tier 與名稱／表達式皆與文章一致，分類計數不變。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 19/19）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-09-05.

- **2026-09-02**（今日）— 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/circle-area.html`（#1 · 數學 · Free，πr² 的扇形拼合推導、直徑／周長／反解半徑三條換算路徑，
  含環形 π(R²−r²)、把直徑當半徑的 4 倍錯誤、π 取 3 的 4.51% 短缺，以及 12 吋 vs 兩個 9 吋披薩對照）。
  Formula 卡片由 placeholder 轉為連結（67 → 66），Tier 與名稱／表達式皆與文章一致，分類計數不變。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 16/16）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-09-02.

- **2026-09-01**（今日）— 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/daily-water-intake.html`（#98 · 健康 · Free，體重 × 30 mL 的每日水分需求公式，
  含 30/35 係數之爭、EFSA 總水分定義、Holliday–Segar 4-2-1 分段法對照與 ACSM 運動補水加成）。
  Formula 卡片由 placeholder 轉為連結（68 → 67），Tier 與名稱／表達式皆與文章一致，分類計數不變。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 21/21）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-09-01.

- **2026-08-31**（同日第二次）— 刪除 `scripts/regen-sitemap-writing.py`（2026-06-08 建立，
  2026-08-05 起已是轉呼叫的相容層）。查核後全站無任何可執行呼叫者：launchd 排程、技能檔、
  settings.json 皆未提及，只有兩處文件字串。**刪除的真正理由不是「沒人用」而是它會說謊**——
  它硬寫 `--section writing`，所以同日 guides 併入後，任何走舊入口的呼叫都會**安靜地少重生一區**，
  而它印的棄用提醒還停在「可一併重生 formulas 區」。連帶更新 `regen_sitemap.py` 的溯源註記
  （標明該檔已刪，讓日後 grep 到的人不會以為 repo 壞了）與 `/boboweb` 技能檔第 5 步的描述。
  檔案內容由 git 保存（`54abce4`、`20ef628`），需要時可還原。
  Removed the regen-sitemap-writing.py compatibility shim. It had no executable callers, but the
  real reason is that it hardcoded --section writing: after guides was folded in the same day, any
  call through the old entrypoint would have silently regenerated one section too few.

- **2026-08-31** — sitemap 產生器納入 guides 區（非發文，改的是工具）：
  ①**動機**：guides 那行原本手動維護（08-30 的紀錄還明寫「`regen_sitemap.py` 重跑不動該區」），
  等於保留了 08-29 才修掉的那個坑——改了文章但忘記手改 sitemap，**完全沒有症狀**。
  ②**併入時多出兩個既有兩區沒有的需求，兩個都不做就等於沒併**：
  (a) **lastmod 精確到秒**。該篇的改動發生在 2026-08-30 23:53:48，寫成日期型 `2026-08-30`
  依 sitemap 規範等同當日 00:00，**比 sitemap 當時的值還舊**——重生一次就把剛解掉的凍結裝回去。
  改用 `%cI`（W3C datetime 含時區），同日內的改動仍是嚴格較新的值。
  (b) **保留 `changefreq`**。guides 那行本來就有 `monthly`，而 `build_block` 只吐 loc/lastmod/priority，
  直接併入會靜默掉一個既有欄位。兩者都做成 per-section 選填，**writing / formulas 的輸出逐字不變**。
  ③**驗證**：TDD 先紅後綠，測試從 30 增至 38 項（新增 guides 精度、changefreq 只出現在該區、
  欄位順序、`<!-- Guides -->` 註解不被吃、別區不被動、冪等、重生後仍是合法 XML）；
  對真實 sitemap 跑出 **byte-for-byte 無差異**，再故意把值改成 `2026-01-01` 重跑，確認它
  **真的會糾正**而不是掃描範圍空掉的假通過。`test_verify_formula_math` 46/46 同步不受影響。
  ④連帶更新 `/bobo-autopublish` 技能檔 Phase 3-C 的描述（它呼叫的是不帶 `--section` 的
  `regen_sitemap.py`＝`all`，所以 guides 自 2026-08-31 起已納入每日自動化）。
  Folded the hand-maintained guides entry into regen_sitemap.py so it can no longer silently freeze.
  Required two new per-section options — second-precision lastmod and changefreq preservation —
  without changing a byte of the writing/formulas output. Tests 30 -> 38, TDD red first.

- **2026-08-30**（同日第五次，人工）— `guides/mac-mini-vs-mac-studio-2026.html` 新增「多機叢集」整節，補上前一版漏掉的 Thunderbolt 4／5 使用情境分野：
  ①**核心缺口**：前一版把 Thunderbolt 定位成「接周邊與螢幕，不是擴充算力」，這句話在 TB5 世代是錯的。macOS 26.2 起支援 RDMA over Thunderbolt，可把多台 Mac 的統一記憶體串成一個池跑單機裝不下的模型——**而這件事硬性要求 TB5，Mac mini M6（TB4）做不到**。官方依據：Apple 台灣 Mac mini 頁「還能讓你將多部 Mac mini 串連成裝置叢集，以執行更大型的本地 AI 模型」（僅 M5 Pro 段落）、Mac Studio 頁「支援叢集運算，分散式 AI 推論速度提升，最快可達 3 倍」。
  ②**節點上限是埠數推出來的**：全網狀要求每兩台之間一條實體 TB5 線，故上限 = 埠數 + 1（mini M5 Pro 4 台／M5 Max 5 台／M5 Ultra 7 台），N 節點需 N(N−1)/2 條線；市面上無 TB5 switch。Apple 自己示範與標示的都是 4 節點，5／7 台標為理論值。mini 組完 4 節點後 **TB 埠一個不剩**，螢幕只能走 HDMI。
  ③**釐清「官方 3 倍」與「實測 1.6 倍」不衝突**：Apple 註腳 22 寫明測的是 72B **稠密**模型配 32K 提示詞（算力瓶頸，平行化有效）；第三方實測（Geerling 2025-12，4 × M3 Ultra／1.5TB）測的是巨大 MoE，exo + RDMA 在 Qwen3 235B 上是 19.5 → 31.9 tok/s（1.64 倍），而 llama.cpp 走 TCP 反而 20.4 → 15.2（**越串越慢**）。結論：串連買到的主要是容量，速度是附帶的。
  ④**回答「TB5 只有 10 GB/s 怎麼串得動」**：跨機器傳的是活化值（每詞元數 MB）不是權重，瓶頸是往返延遲而非頻寬（TCP 約 300 µs → RDMA 50 µs 以下）；並區分張量平行（會變快、吃延遲）與管線平行（只解決裝不裝得下）。
  ⑤**成本結論（用本頁既有官網實價算的）**：湊 256GB 記憶體池，1 台 M5 Ultra NT$339,900／2 台 M5 Max NT$351,800／4 台 M5 Pro NT$379,600——**單機在售價、頻寬、功率、佈線四項全勝**，因為記憶體單價固定 875 元／GB，串連不會讓那個常數變便宜。串連唯一無可取代的是單機買不到的容量（上限 512GB，10 月底推出）。附七項動手門檻（版本號須完全一致、Recovery 執行 `rdma_ctl enable`、線材須支援 TB5、四台 Studio 峰值 1,920W 超過台灣 110V／15A 迴路的 1,650W 上限等）。
  ⑥連帶更新 title／meta／og／JSON-LD／導覽列／Markdown 匯出／「數字怎麼來的」段（新增第三方數字類別並註明是前一代硬體、只能看趨勢），並在 TB4／TB5 對照表加一列 RDMA。1232px 與 375px 皆 0 溢出、0 擠壓，未引入任何寫死顏色。
  Added a full section on multi-Mac RDMA clustering over Thunderbolt 5, correcting the previous claim that Thunderbolt is only for peripherals. Cluster size is capped by port count (full mesh); Apple's 3x claim and the measured 1.6x are both real but measure different things; and at equal capacity a single machine beats a cluster on price, bandwidth, power and cabling.

- **2026-08-30**（同日第四次，人工）— `guides/mac-mini-vs-mac-studio-2026.html` **全文重寫**，加入記憶體頻寬與 Thunderbolt 兩條新軸線：
  ①**四個售價經官網設定工具逐項核實，全部正確**——因此移除前一版「售價為推估值」的標註。該標註本身是錯的（50,900／94,900／175,900／339,900 皆為官網實算金額）。
  ②**新發現：記憶體加購邊際單價全線一律 NT$875／GB**。七個級距（M6 16→24／16→32、M5 Pro 24→48／24→64、M5 Max 48→64／48→128、M5 Ultra 96→256）換算後完全相同。這使舊版兩張互相矛盾的「售價÷記憶體」表失效——該指標把機殼、散熱、SSD、10GbE 都攤進記憶體，故同批機器換個配置就得出相反結論。改以大數字＋七列驗算表呈現，並附 SSD 邊際單價 17.09 元／GB（記憶體是它的 51.2 倍）。
  ③**新增記憶體頻寬節**：M6 的頻寬綁在容量上（16GB 153GB/s，加購 24／32GB 才是 170GB/s）；Mac Studio 的 128GB 只有 40 核 GPU 版可選，因此 128GB 必然拿到 614GB/s，36GB 版只有 460GB/s。對數軸點圖把四台的統一記憶體頻寬與 TB5／TB4／10GbE／2.5GbE 放在同一條軸上（M5 Ultra 是 TB5 對稱頻寬的 120 倍）。
  ④**新增 Thunderbolt 節**：釐清官網標示的 120Gb/s 是頻寬提升模式（120 下行／40 上行）而非對稱頻寬（80Gb/s）；補上各機埠數、正面埠速度、USB4 上限（Studio 120Gb/s vs mini 40Gb/s）、DP 1.4 與 2.1、單一埠可帶螢幕數（2／3／4／4）。
  ⑤**本地 LLM 段改為可驗算的 roofline**：`tok/s ≈ 記憶體頻寬 ÷ 權重位元組 × 0.70`，取代舊版無來源的體感數字，並明確區分官方數字／推導值／經驗係數三類。
  ⑥**更正舊版兩處事實**：M5 Ultra 記憶體上限是 512GB（36 核／80 核版，官網註明 10 月底推出）而非 256GB；補上媒體引擎階梯（1/1/1 → 1/1/1 → 1/2/2 → 2/4/4）。
  ⑦**修六個既有前端缺陷**：白字壓在 `--accent-gradient` 上三個色停僅 2.14／2.98／2.64:1（漸層是 background-image，掃描器讀不到底色故長期潛伏）；亮色主題未覆寫 `--accent-blue`／`--accent-purple`／`--accent-amber`（2.14／3.96／1.67:1）；兩張重點卡把深色底 `rgba(22,27,39,.8)` 寫死在漸層裡，亮色主題下變成深底配深字；整份樣式表沒有任何 `:focus-visible` 規則；88 個圖示只有 24 個標了 `aria-hidden`；`localStorage.getItem` 未加 try/catch，瀏覽器封鎖網站資料時會讓整包互動初始化中止。另移除假造即時狀態的無限脈動點與漸層標題字，補上 `prefers-reduced-motion`。兩主題各掃 560 個文字元素、皆 0 違規；375px 無溢出。
  Full rewrite adding memory-bandwidth and Thunderbolt axes. Key finding: Apple charges a flat NT$875/GB for unified memory across all seven upgrade tiers and all four chips, which invalidates the old price-per-GB metric. Also fixed six pre-existing frontend defects, including white text on a gradient that no contrast scanner could see.

- **2026-08-30**（同日第三次，人工）— `guides/mac-mini-vs-mac-studio-2026.html` 兩輪內容更正，全部依 Apple 台灣官網實查：
  ①**M6 的 NPU 是「雙 16 核心神經網路引擎」**，原文寫 16 核心；卡片、參數表、Markdown 匯出三處同步更正（M5 Pro 16 核／M5 Max 16 核／M5 Ultra 32 核核對無誤）。
  ②**更正前一版標註**——前一版斷言這些晶片「非 Apple 官方已發表資料、依市場傳聞推估」，實查後這是錯的，四款規格官網都查得到；真正的落差是本頁四台機器的記憶體皆為加購後的客製配置、售價為推估值。標註改寫並附官方起價對照，連帶更正 meta / og / 表格欄名 / 頁尾共 6 處。
  ③**新增「官方標配起售價 × 標配記憶體」對照表**（Mac mini M6 NT$29,900／16GB，M5 Pro NT$59,900／24GB，Mac Studio M5 Max NT$84,900／36GB，M5 Ultra NT$199,900／96GB），四個起售價於購買頁獨立複查、每 GB 欄位由腳本驗算。此表結論與上方相反：用官方標配算，最便宜的是入門 M6（NT$1,869/GB）、M5 Pro 反而最貴（NT$2,496/GB），並寫明此指標把 SSD 成本攤進了記憶體（四台標配 SSD 差距達四倍）故不能直接橫向比。加導覽錨點並同步進「複製 MD」匯出。
  ④**修兩個色彩缺陷**：`html.light` 未覆寫 `--accent-green` / `--accent-rose`，亮色底僅 1.91:1 與 3.64:1（兩 token 全站只作文字色，badge/chip 底色另外寫死，故可安全覆寫為 #047857 / #be123c）；新區塊註腳誤用 writing 版型的 `.article-foot`（本頁無此類別）且 `--text-subtle` 僅 3.85:1，改為 `.baseline-source` 搭 `--text-muted`。修正後兩主題全數過 AA，並連帶修好既有 NPU 列與 LLM 速查器在亮色模式的失效。
  Two rounds of fact-checking against Apple Taiwan: corrected the M6 NPU to dual 16-core, replaced an inaccurate disclaimer of my own making, added an official base-price table whose conclusion contradicts the article's, and fixed two light-mode contrast failures.


- **2026-08-30**（今日，人工發布）— 新增 `guides/` 區與第一篇選購指南：
  `guides/mac-mini-vs-mac-studio-2026.html`（Mac mini vs Mac Studio 一頁式全參數對比）。
  來源是外部草稿的單檔 `standalone.html`（自帶深色玻璃擬態設計、互動篩選、參數交叉表、每 GB 記憶體成本圖表、本地 LLM 適配速查、複製 Markdown），
  進站時保留原設計，只做進站整理：加 canonical / OG / Cloudflare Web Analytics beacon、品牌由 MoneyAI Labs 統一為 Bobo Labs、header 品牌改為回首頁連結。
  **內容誠信處理**：文中 Apple M6 / M5 Pro / M5 Max / M5 Ultra 的規格與新台幣定價並非 Apple 官方已發表資料，
  原稿只有頁尾一行小字免責、正文卻以「官方參考售價」的既成事實語氣書寫；
  改為 hero 下方常駐推測性標註（說明數字為推估、算式可驗但輸入值會變、適合當比較框架而非下單依據），
  表格與 Markdown 匯出的「官方參考售價」一併改為「推估售價（非官方）」。
  另修兩個顯示缺陷：`fa-microchip-ai` 是 FontAwesome Pro 專屬圖示（免費版載不到、實測 62 個圖示中唯一破圖）改用 `fa-microchip`；窄螢幕品牌名換行擠壓 header，加 640px 斷點讓品牌名不換行並隱藏 Hardware Lab 標籤。
  驗證：HTML 巢狀無誤、明暗兩主題對比皆過 AA（暗 6.8:1／亮 7.0:1）、375px 無水平溢出、情境篩選與主題切換實測可用、sitemap 加 Guides 區（125 → 127 網址）且 `regen_sitemap.py` 重跑不動該區。
  Added `guides/` section with a Mac buying guide; kept the source design, added a prominent speculative-data notice since the specs and prices are not official Apple figures.

- **2026-08-30**（今日）— 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/target-heart-rate.html`（#93 · 健康 · Free，(220−年齡)×強度% 的五個強度區間實算，並比較 Karvonen 心率儲備法與 Tanaka 修正式）。
  Formula 卡片由 placeholder 轉為連結（69 → 68 張），Tier 與文章一致故分類計數與註腳未動；sitemap formulas 區重生為 29 篇。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 21 cases 全過）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-30.

- **2026-08-29** — 修正 sitemap `lastmod` 失真（非發文，改的是產生器）：
  `scripts/regen_sitemap.py` 原本對 formulas 區「保留 sitemap 既有值」，等於首次收錄後永遠凍結——實測 **27/28 篇公式頁的 lastmod 是錯的**，2026-06-18 的長尾標題改動（`cce8df3`）從未反映到 sitemap，Google 讀到「5/28 之後沒變過」就沒有回來重爬的理由。
  改以 git 為唯一來源：formulas 取內容最後改動日、未提交的改動算今天、無 git 才退回 mtime（mtime 在全新 clone 會整批變成 clone 當天，不能當常態來源）。writing 維持發布日語意——日期前綴檔取檔名日期，3 篇無前綴舊檔改取 git 首次收錄日，避免 2026-06-04 全站注入 analytics 的單行 commit 讓文章謊稱更新。
  新增 `scripts/test_regen_sitemap.py`（17 項純 assert 規格，含整合層與冪等驗證）；修正前對同一組測試跑出 4/8 紅，另做兩次變異測試確認測試抓得到退化。
  sitemap 重生：formulas 27 行、writing 3 行更正，網址總數 125 不變、其餘區塊零變動。
  Fixed sitemap lastmod drift: formulas now derive from git instead of freezing at first inclusion (27/28 pages were stale, hiding the 2026-06-18 title change from Google). Adds test_regen_sitemap.py.

- **2026-08-28**（今日）— 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/dividend-yield.html`（#110 · 金融 · Pro，股息殖利率 D/P：股價 42.5 元、年配 2.55 元 → 6%；買 10 張成本 425,000 元、年領 25,500 元，扣二代健保補充保費 2.11%（538.05 元）後實質殖利率 5.87%；除息參考價 39.95 元、填息所需漲幅 6.38% 與殖利率虛胖 0.38 個百分點的常見誤用；追高 55 元剩 4.64% vs 低接 34 元 7.50%、yield on cost 8.50%；總報酬對照 A 股 0.12% 輸 B 股 11.00%，配息率 75% vs 133.33% 兩道體檢）。
  Formula 卡片由 placeholder 轉為連結（1 張替換，Tier 一致計數不動）；金融分類 13 條至此全數完成，區塊註腳同步更正；sitemap 重生（formulas 28 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 19 case 全過）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-28.
- **2026-08-27**（今日）— 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/gross-profit-margin.html`（#109 · 金融 · Pro，毛利率 (R−C)/R：年營收 1.2 億、銷貨成本 7,350 萬 → 毛利 46,500,000 元／毛利率 38.75%；再扣營業費用 3,120 萬與 20% 稅得營業利益率 12.75%、淨利率 9.33%，三層落差 26 個百分點實算；降成本 5%（41.81%）與漲價 5%（41.67%）反直覺對照，通路商 8.92% vs 軟體 82% 說明跨產業不可比）。
  Formula 卡片由 placeholder 轉為連結（1 張替換，Tier 一致計數不動）；卡片 expr 依文章更正為「銷貨成本」；sitemap 重生（formulas 27 篇）。
  同批補提交 2026-08-26 因 launchd 中斷而未 commit 的 `formulas/break-even-point.html`（已複驗 QA 通過）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 18 case 全過）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-27.

- **2026-08-26** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/break-even-point.html`（#49 · 金融 · Pro，損益平衡點 BEP=FC/(P−VC)：月固定成本 190,000 元、售價 60 元、變動成本 22 元的手搖店打平 5,000 杯／日 166.67 杯／營收 300,000 元；漲價 10% 打平點降 681.8 杯（13.64%），原物料漲 6 元（5,937.5 杯）比多請一名店員（5,789.5 杯）更傷，目標利潤與安全邊際率 28.57% 實算）。
  Formula 卡片由 placeholder 轉為連結（1 張替換，Tier 一致計數不動）；sitemap 重生（formulas 26 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 15 case 全過）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-26.

- **2026-08-23** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/present-value-annuity.html`（#44 · 金融 · Pro，年金現值 PVA=PMT×(1−(1+r)⁻ⁿ)/r：月領 1 萬 6% 20 年現值 1,395,808 元，利率差 1% 造成 40 萬差距（3%→180 萬 vs 6%→139 萬），年限 20→30 年現值僅多 27 萬，貸款公式正反面關係說明）。
  Formula 卡片由 placeholder 轉為連結（1 張替換，Tier 一致計數不動）；sitemap 重生（formulas 25 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 6 cases）自動上線。
  Auto-published 1 formula draft from _pending/ via /bobo-autopublish on 2026-08-23.

- **2026-08-20** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/price-earnings-ratio.html`（#47 · 金融 · Free，本益比 P/E：P÷E，750÷25=30 倍 vs 400÷40=10 倍實例，反推合理股價 20×25=500 元，Trailing vs Forward P/E 選擇說明）。
  Formula 卡片由 placeholder 轉為連結（1 張替換，Tier 一致計數不動）；sitemap 重生（formulas 24 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 3 cases）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-20.

- **2026-08-18** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/return-on-investment.html`（#45 · 金融 · Free，投資報酬率 ROI：(V₂−V₁)/V₁×100%，5 萬買進 8 萬賣出得 60%，負報酬 -15% 實例，持有 3 年 30% 年化換算 9.14%，三大誤用：分母搞錯 vs 37.5%、忽略手續費、不年化直接跨期比）。
  Formula 卡片由 placeholder 轉為連結（1 張替換，Tier 一致計數不動）；sitemap 重生（formulas 23 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 5 cases）自動上線。
  Auto-published 1 formula draft from _pending/ via /bobo-autopublish on 2026-08-18.

- **2026-08-16** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/simple-interest.html`（#41 · 金融 · Free，單利公式 P(1+rt)：100 萬 5% 三年終值 1,150,000，單利 vs 複利 3/10/30 年差距對照（7,625→128,895→1,821,942），四種公式變形與適用場景）。
  Formula 卡片由 placeholder 轉為連結（1 張替換 Tier 一致計數不動）；sitemap 重生（formulas 22 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 12 cases）自動上線。
  Auto-published 1 formula draft from _pending/ via /bobo-autopublish on 2026-08-16.

- **2026-08-14** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/body-fat-deurenberg.html`（#96 · 健康 · Pro，體脂率 Deurenberg：BF% = 1.20×BMI + 0.23×age − 10.8×sex − 5.4，BMI 24 的 30 歲男性估 19.5%、同齡女性 30.3%，差 10.8 個百分點；40 歲年齡效應 2.3% 實例；亞洲族裔與重訓者誤差討論）。
  Formula 卡片由 placeholder 轉為連結（1 張替換 Tier 一致計數不動）；sitemap 重生（formulas 21 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 5 cases）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-14.

- **2026-08-12** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/tdee.html`（#94 · 健康 · Pro，TDEE = BMR × 活動係數，拆解 5 種活動等級係數 1.2–1.9，男性 70kg 久坐 1,979 到高強度 3,133 kcal 實例，女性 60kg 同步對照）。
  Formula 卡片由 placeholder 轉為連結（1 張替換 Tier 一致計數不動）；sitemap 重生（formulas 20 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算 12 cases）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-12.

- **2026-08-10** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/bmr.html`（#91 · 健康 · Free，BMR 基礎代謝率 = 10w + 6.25h − 5a + s，拆解 Mifflin-St Jeor 公式四係數，附男女差 360 kcal、30 vs 40 歲年齡效應 50 kcal 實例）。
  Formula 卡片由 placeholder 轉為連結（1 張替換 Tier 一致計數不動）；sitemap 重生（formulas 19 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-10.

- **2026-08-09** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `formulas/effective-annual-rate.html`（#48 · 金融 · Pro，實質年利率 EAR = (1+r/n)ⁿ−1，拆解名目利率 vs EAR、月複利 6%→6.17%、信用卡循環 18%→EAR 19.56%）、
  `writing/2026-08-07-auto-resizer-v301-portrait-fix.html`（Auto Resizer v3.0.1：74→98 單元全綠但兩條測試是 tautology、直式影片面積比不裝擴充功能小 14.8%、聚合命中次數掩蓋兩個獨立欄位）。
  Writing 區依時間倒序插入；Formula 卡片由 placeholder 轉為連結（1 張替換 Tier 一致計數不動）；sitemap 重生（writing 93 篇、formulas 18 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-08-09.

- **2026-08-07** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `formulas/future-value-annuity.html`（#43 · 金融 · Pro，年金終值 FV = PMT×((1+r)^n−1)/r，逐步拆解等比數列推導、利率敏感度、早晚 10 年差距 542 萬）。
  Formula 卡片由 placeholder 轉為連結（1 張替換，Tier 一致計數不動）；sitemap 重生（formulas 17 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評/數值驗算）自動上線。
  Auto-published 1 formula draft from _pending/ via /bobo-autopublish on 2026-08-07.

- **2026-08-06** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `writing/2026-08-05-gemma4-e4b-false-pass-and-e-axis.html`（四層生產路徑同日全失全復原・比對腳本空集合靜默通過加 assert 才是真守門・GPU 高峰值不能重疊・E 軸 9/9 否決自己的修法）。
  Writing 區依時間倒序插入 index.html；sitemap 同步重生（writing 92 篇）。
  通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-06.

- **2026-08-05** — 自動化火力轉向公式庫：新增 `formulas/present-value.html`（#42 · 金融 · Pro，
  現值計算公式，含折現率敏感度與 n 的影響實例）。Formula 卡片由 placeholder 轉為連結。
  同時上線 formula 文章的數值守門 `scripts/verify_formula_math.py`（獨立驗算文章宣稱的每個數字，
  並要求該數字逐字出現在正文），以及泛化的 `scripts/regen_sitemap.py`（writing + formulas 兩區）。
  Shifted the publishing pipeline from dev-journal posts to the formula library, and added a
  deterministic math verifier that gates every number a formula article claims.

- **2026-08-01** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-07-30-github-fork-cleanup.html`（334 fork 掃出 317 個純鏡像，連續四次用代理指標拿到自信錯誤答案；ahead_by 來自可秒建產出物不算原創，commit 標題說新增不等於現在存在）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-08-01.

- **2026-07-29** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-07-25-gemma4-zhtw-adapter.html`（v7、v8 混訓兩度 REJECTED，診出語言假設互斥根因；base 對照組才知微調在繁中是雙向的；四個守門機制是被自己犯的錯逼出來的）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-07-29.

- **2026-07-26** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-07-25-gemma4-longctx-two-diseases.html`（同一個「0/3」背後兩種不同的病：06/07 是檢索失明、08 是抽取失敗，修法不能混用）、`2026-07-25-nomad-dashboard-path-bug.html`（路徑 bug 讓任何專案都讀到空白，POST 默默建孤兒檔，services/handoff.py 加 mtime 樂觀鎖三層同修）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-07-26.

- **2026-07-25** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-07-24-longctx-eval-mapreduce.html`（L0/L1/L2 三層可歸因評測 Map-Reduce 長上下文管線：query-aware 5/5 vs stuffing 1/5、128K 名目 8K 甜蜜點、四個真實缺陷、窄修補套全套必倒賠第五次）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-07-25.

- **2026-07-22** — 由 /boboweb 核可 1 篇文章：
  `2026-07-18-supercalc-v384-quality-audit.html`（Lighthouse mobile A11y 94→100、雙主題 contrast ratio 手算、og:image 從無到有、FAQPage JSON-LD 5 題、Carbon Ads 被拒後文案誠實化）。
  Index Writing 區依時間倒序插入。
  Promoted 1 draft from _pending/ via /boboweb on 2026-07-22.

- **2026-07-22** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-07-19-graphify-loop-routing.html`（第一炮打在沒開的 8081 · stage 路由從可選變前置 · 4 跨 repo episode 記憶全回寫）、`2026-07-19-graphify-vs-ua-dashboard.html`（AST 3.2s $0 vs LLM 費時 stale · 跨邊界邊兩工具都 0 條 · 重跑成本決定圖壽命）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-07-22.

- **2026-07-19** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-07-17-gemma4-adapter-clobber-recovery.html`（RLCF demo 少帶 --adapter-path 靜默覆寫生產 adapter、「舊 holdout 突然過了」是警訊、0000300 checkpoint 救援、輸出目錄隔離防再犯）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-07-19.

- **2026-07-17** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-07-16-gemma4-e4b-coding-v2.html`（四類任務形狀補齊、50 筆 SFT、max_tokens 截斷是根因、all-pass 5→15/16 不需重訓）、
  `2026-07-16-gemma4-e4b-deployment.html`（GGUF Q4_K_M 4.9GB、llama-server + Ollama 各 3/3、launchd 常駐、雙模型路由 verify 2/2）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-07-17.

- **2026-07-16** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-07-11-gemma4-isolated-adapter-lessons.html`（v6 混合訓練域衝突、獨立 adapter 驗兩假設、12 筆量不足 val loss 降仍零遷移）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-07-16.

- **2026-07-12** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-07-10-gemma4-v6-domain-collision.html`（v6 域混合讓 coding + tool-calling 同時退步、獨立 adapter 解衝突但 12 筆資料量不足、兩次 REJECTED 兩個不同根因）、
  `2026-07-01-gemma4-training-pipeline-v2.html`（Hermes 1893→1100 清洗、三個資料 bug、LoRA val loss 0.292、300 筆負樣本讓 Gemma4 2.3B 學會誠實婉拒）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-07-12.

- **2026-07-10** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-07-09-gemma4-md-eval-diagnosis.html`（診斷 gemma4 E2B v3 7 道必掛題：病因分類、monkeypatch 修好 09 但讓 01/02 崩掉、2.3B prompt 餘裕教訓）、
  `2026-07-02-local-coding-agent-pivot.html`（pivot 從訓模型到地端 coding agent：90% 價值在 harness、LM Studio + Aider + qwen2.5-coder-7b MA 落地）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-07-10.

- **2026-07-09** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-07-02-gemma4-v5-refusal-grounding.html`（五輪 contrastive 訓練教 2.3B 先讀工具清單，v5c minimal pairs 修 grounding，refusal 類推 1→3→4/5，v5d 為基準）、
  `2026-07-02-gemma4-v3-serving-casual.html`（固化 mlx_lm.server tool-calling 守門腳本，補 82 筆 curated casual 訓 v3，v4 矯枉過正廢棄）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-07-09.

- **2026-07-09（人工 /boboweb）** — 排除 QA#1a 誤判後人工發布 1 篇文章：
  `2026-06-25-stock-grid-bot-smoke-test-restore.html`（先驗再復原：金融 bot 盤前煙測與安全自啟的 6 條原則，git log 先於直覺、byte-by-byte 比對 DB、secure-by-default 比 denylist 穩健）。
  原本 QA#1a 命中「broker」硬擋（1a 高危專名清單不分語境），核對後確認內文只是引用 gate 狀態訊息「尚未登入 broker」非真憑證，改用詞為「尚未完成下單系統登入」後人工 mv + 編 index.html + push。
  Manually published 1 draft (previously QA#1a-blocked false positive) via /boboweb on 2026-07-09.

- **2026-07-09** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-07-03-translate-rubric-falsification.html`（花四版 SFT 打設計壞掉的靶：dangling referent 讓 eval 失敗四版、base 並排照出 thought channel 被壓垮、20 分鐘 prompt 實驗揭穿比訓練便宜）、`2026-07-03-coding-agent-eval-suite.html`（16 道真實 coding 任務成績單：max_tokens confound 修正讓 gemma 3/8→5/8、examples_as_sys_msg 一行治好 edit-format、3B + 好 harness ≈ 7B）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。1 篇因 QA#1a blocked（broker）留 _pending/，4 篇 deferred 留待下次。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-07-09.

- **2026-07-02** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-07-01-gemma4-chat-template-fix.html`（Gemini 寫的 Gemma 4 微調指南格式錯在哪：ChatML 混入 Gemma 4 原生 turn/model 格式、訓練與 serving template 必須同一、assert 防呆讓格式錯誤在訓練前報錯）、`2026-07-01-agent-context-cost-rules-dedup.html`（裝 299 個 Agent context window 怎麼算：name+description 常駐 11K tokens 非全文、rules 三重重複聯集再刪非直接刪）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。1 篇因 QA#1a blocked（broker）留 _pending/。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-07-02.

- **2026-07-01** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-06-30-headroom-closeout.html`（Headroom 學習重建完結篇：Python/Rust 154 tests 全綠、parity 14 fixtures byte-for-byte、邊際學習價值趨零、封存判定靠跑測試不靠感覺）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。1 篇草稿因 QA#1a blocked（broker）留 _pending/。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-07-01.

- **2026-06-30** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-06-29-headroom-m17-csv.html`（Headroom M17 CSV 內容感知壓縮：表頭釘第0行、首尾代表列保原文、中段同構列收斂marker、壓縮率69%零回歸、M11骨架第七度驗證）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。1 篇草稿因 QA#1a blocked（broker）留 _pending/。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-06-30.

- **2026-06-28** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-06-27-headroom-answer-key-m16.html`（工業版解答本 5 個架構差距 + M16 frame 感知 stack trace 策略：auth-mode gating / byte-range surgery 等學習版沒有的概念，研究到 commit 同日完成）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-06-28.

- **2026-06-26** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-06-25-supercalc-carbon-ads.html`（∑ Calc 廣告路線確認：移除殭屍 AdSense dead script、Ezoic 門檻 250K MAU 不符、選定 Carbon Ads 並確認 exclusive network 條款）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-06-26.

- **2026-06-23** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-22-headroom-m13-m14-m15.html`（JSON byte-level 照抄不重序列化：M13/M14/M15 三片壓縮策略，dispatcher 零改造五片連推）、
  `2026-06-22-understand-anything-nomad.html`（Understand Anything 分析 nomad-dashboard 結案：234 節點 364 邊 8 架構層，磁碟才是 ground truth）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-23.

- **2026-06-22** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-18-supercalc-v382-defer.html`（∑ Calc v3.8.2 效能深審：inline JS 177KB 是真大頭，5 個外部 script 加 defer，async 會亂序壞模組鏈）、
  `2026-06-15-stock-grid-bot-armed-gate.html`（armed gate：拆開「追蹤狀態」與「送出委託」的唯一防線）。
  Index Writing 區依時間倒序插入。通過 QA gate（紅線語境評估放行/結構/佔位/不覆蓋/LLM自評）自動上線。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-22.

- **2026-06-21** — 由 /bobo-autopublish 全自主發布 1 篇文章：
  `2026-06-20-headroom-m12-log-compression.html`（log 內容感知壓縮：逐行嗅探訊號/噪音，14473→1147 bytes，Python/Rust 逐字節一致）。
  Index Writing 區依時間倒序插入頂端。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  2 篇擋下（redline 1a: `broker` ×2 in armed-gate；`PayPal` in supercalc-v382-defer `window.PayPalIntegration`）。
  Auto-published 1 draft from _pending/ via /bobo-autopublish on 2026-06-21.

- **2026-06-19** — 由 /bobo-autopublish 全自主發布 2 篇文章：
  `2026-06-18-headroom-m9-m10-ccr-sse.html`（M9 server-side resolve loop 取回壓縮上下文、M10 觀察式 SSE probe 旁觀不攔截）、
  `2026-06-18-bobo-labs-gsc-zero-impressions.html`（formula 頁全數進索引後 GSC 曝光仍 0，解剖三層病灶：標題意圖錯位、知識散文對撞工具意圖、零權重域硬碰紅海 head term）。
  Index Writing 區依時間倒序插入頂端。通過 QA gate（紅線/結構/佔位/不覆蓋/LLM自評）自動上線。
  1 篇擋下（redline 1a: PayPal 出現於 `window.PayPalIntegration`）。
  Auto-published 2 drafts from _pending/ via /bobo-autopublish on 2026-06-19.

- **2026-06-18** — SEO 長尾標題實驗：`compound-interest.html` 與 `mortgage-payment.html` 的 `<title>` / meta description / og:title / JSON-LD headline / breadcrumb 由紅海 head term 改為長尾搜尋詞（複利→「複利計算公式｜複利終值怎麼算」、房貸→「房貸月繳怎麼算？等額本息公式拆解」），內文與切角保留。背景：5 篇理財 formula 已編入索引但搜尋曝光為 0，改打零權重新頁擠得進的長尾關鍵字空間。
  SEO long-tail title experiment on two formula pages (compound-interest, mortgage-payment): retargeted title/meta/og/JSON-LD from competitive head terms to long-tail queries, content unchanged. Indexed but zero-impression pages now aim at winnable long-tail keywords.

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
