#!/usr/bin/env python3
"""
regen_sitemap.py — 冪等重生 sitemap.xml 的 writing / formulas / guides 三區（2026-08-05 建立）

由 regen-sitemap-writing.py（2026-06-08，已於 2026-08-31 刪除）泛化而來：原版明文「只動 writing 區、不碰
Formula 區」，導致自動化火力轉向 formulas 後，新公式文章不會進 sitemap。

原則不變：
  - 只重寫指定區塊的 <url> 行，其餘（Home / Projects / Formula Index / 註解）完全不動。
  - 區塊必須是連續行，否則中止（避免誤刪夾雜的條目）。
  - 重複執行結果不變（idempotent）。

排序 / lastmod：
  - writing：日期檔（YYYY-MM-DD 前綴）依日期升序、同日依檔名；lastmod 取檔名日期＝發布日。
  - formulas：依檔名升序；lastmod 取內容最後改動日（git），未提交的改動算今天。
  - guides：同 formulas，但 lastmod 精確到秒（W3C datetime）並保留 changefreq。

2026-08-29 修正：formulas 原本「保留 sitemap 既有值」，等於首次進 sitemap 後永遠凍結，
27/28 篇的 lastmod 因此是錯的——2026-06-18 的長尾標題改動從未反映到 sitemap，Google
讀到「5/28 之後沒變過」就沒有回來重爬的理由。改以 git 為唯一來源，既有值不再參與計算。
writing 維持檔名日期：那批的 git 日期幾乎全是全站注入 analytics 的機械式 commit，
拿它當 lastmod 會讓 93 篇同時謊稱已修改，而 Google 對不可信的 lastmod 是整欄不再採信。

2026-08-31 併入 guides：原本是手動維護的一行，會重演 formulas 那次的凍結——改了文章
卻忘記手改 sitemap，完全沒有症狀。併入時多了兩個既有兩區沒有的需求，兩個都不做就等於沒併：
  - **精確到秒**。該篇 2026-08-30 23:53 的改動若寫成日期型 `2026-08-30`，依 sitemap 規範
    等同當日 00:00，比 sitemap 當時的值還舊——重生一次就把剛解掉的凍結裝回去。
  - **保留 changefreq**。guides 那行本來就有 `monthly`，靜默掉它是拿併入換掉一個既有欄位。
兩者都做成 per-section 選項，writing / formulas 的輸出逐字不變。

用法：
    python3 scripts/regen_sitemap.py              # 三區都重生
    python3 scripts/regen_sitemap.py --section guides
"""
from __future__ import annotations

import argparse
import re
import sys
import subprocess
from datetime import date, datetime
from pathlib import Path

BASE = "https://labs.moneyai168.com"
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
GIT_TIMEOUT = 10  # 秒；單檔查詢，逾時即視為取不到而退回 mtime

# 每區的設定。loc 正則只吃 *.html，所以 `/formulas/` 索引頁那行不會被視為區塊成員。
# exclude：目錄索引頁不進文章區（`/formulas/` 已由 sitemap 的 Formula Library Index
# 區塊單獨收錄，再收 `/formulas/index.html` 會變成同一頁的重複 URL）。
# changefreq / precise 為選填：未設定即維持 writing / formulas 原本的輸出形狀。
SECTIONS: dict[str, dict] = {
    "writing": {"dir": "writing", "priority": "0.5", "by_date": True, "exclude": {"index.html"}},
    "formulas": {"dir": "formulas", "priority": "0.8", "by_date": False, "exclude": {"index.html"}},
    "guides": {"dir": "guides", "priority": "0.9", "by_date": False, "exclude": {"index.html"},
               "changefreq": "monthly", "precise": True},
}


def site_root() -> Path:
    """腳本位於 <repo>/scripts/，repo 根為其上層。"""
    return Path(__file__).resolve().parent.parent


def loc_pattern(dirname: str) -> re.Pattern[str]:
    return re.compile(rf"/{re.escape(dirname)}/([^<\"]+\.html)")


def git_output(directory: Path, *args: str) -> str:
    """在 directory 下跑 git，任何失敗都回空字串（未安裝 git／不是 repo 都走這條）。"""
    try:
        done = subprocess.run(["git", *args], cwd=directory, check=True,
                              capture_output=True, text=True, timeout=GIT_TIMEOUT)
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout.strip()


def stamp_now(precise: bool) -> str:
    """「現在」：precise 時輸出到秒的本地時區 W3C datetime，否則只有日期。"""
    if precise:
        return datetime.now().astimezone().replace(microsecond=0).isoformat()
    return date.today().isoformat()


def stamp_mtime(path: Path, precise: bool) -> str:
    """檔案 mtime，粒度同 stamp_now。"""
    if precise:
        return (datetime.fromtimestamp(path.stat().st_mtime)
                .astimezone().replace(microsecond=0).isoformat())
    return date.fromtimestamp(path.stat().st_mtime).isoformat()


def content_lastmod(path: Path, precise: bool = False) -> str:
    """內容最後改動時間：未提交的改動算現在，否則取 git 最後 commit，無 git 才退回 mtime。

    mtime 只當退路而非常態來源——全新 clone 會把整批檔案的 mtime 設成 clone 當天，
    拿它產 sitemap 會讓每一頁都謊稱剛改過。

    precise=True 時全程用 %cI（含時區、精確到秒）而非 %cs（只有日期）。同一天內的
    改動因此仍是嚴格較新的值，不會被日期粒度抹平成當日 00:00。
    """
    directory = path.parent
    if git_output(directory, "status", "--porcelain", "--", path.name):
        return stamp_now(precise)
    fmt = "--format=%cI" if precise else "--format=%cs"
    committed = git_output(directory, "log", "-1", fmt, "--", path.name)
    return committed or stamp_mtime(path, precise)


def publish_lastmod(path: Path) -> str:
    """發布日：git 首次收錄該檔的 commit 日；取不到才退回內容最後改動日。

    給 writing 的無日期前綴舊檔用。它們最後一次改動是 2026-06-04 全站注入 analytics
    的單行 commit——拿那個當 lastmod 等於為一支追蹤腳本宣稱文章更新過。
    """
    created = git_output(path.parent, "log", "--diff-filter=A", "--format=%cs",
                         "--", path.name)
    return created.splitlines()[-1] if created else content_lastmod(path)


def derive_lastmod(basename: str, directory: Path, by_date: bool,
                   precise: bool = False) -> str:
    """writing→發布日（檔名日期，無前綴則取 git 首次收錄日）；formulas/guides→內容最後改動時間。"""
    if by_date:
        match = DATE_PREFIX.match(basename)
        return match.group(1) if match else publish_lastmod(directory / basename)
    return content_lastmod(directory / basename, precise)


def sort_key(basename: str, by_date: bool) -> tuple[int, str, str]:
    """日期檔(0)依(日期,檔名)；非日期檔(1)依檔名。"""
    match = DATE_PREFIX.match(basename) if by_date else None
    return (0, match.group(1), basename) if match else (1, "", basename)


def build_block(root: Path, section: str) -> list[str]:
    config = SECTIONS[section]
    directory = root / config["dir"]
    names = sorted(
        (p.name for p in directory.glob("*.html") if p.name not in config["exclude"]),
        key=lambda n: sort_key(n, config["by_date"]),
    )
    changefreq = config.get("changefreq")
    freq_tag = f"<changefreq>{changefreq}</changefreq>" if changefreq else ""
    precise = config.get("precise", False)
    return [
        f"  <url><loc>{BASE}/{config['dir']}/{name}</loc>"
        f"<lastmod>{derive_lastmod(name, directory, config['by_date'], precise)}</lastmod>"
        f"{freq_tag}"
        f"<priority>{config['priority']}</priority></url>"
        for name in names
    ]


def regen_section(sitemap_path: Path, section: str) -> tuple[bool, int]:
    """重生單一區塊，回傳 (是否有變動, 檔數)。"""
    config = SECTIONS[section]
    pattern = loc_pattern(config["dir"])
    text = sitemap_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    idx = [i for i, ln in enumerate(lines) if pattern.search(ln)]
    if not idx:
        raise SystemExit(f"[regen-sitemap] 找不到任何 /{config['dir']}/*.html 條目，"
                         "sitemap 結構異常，中止")
    first, last = idx[0], idx[-1]
    if idx != list(range(first, last + 1)):
        raise SystemExit(f"[regen-sitemap] {section} 條目非連續區塊，需人工檢查，中止")

    new_block = build_block(site_root(), section)
    new_text = "\n".join(lines[:first] + new_block + lines[last + 1:]) + "\n"
    if new_text == text:
        return False, len(new_block)
    sitemap_path.write_text(new_text, encoding="utf-8")
    return True, len(new_block)


def main() -> int:
    parser = argparse.ArgumentParser(description="冪等重生 sitemap 的 writing / formulas / guides 區")
    parser.add_argument("--section", choices=[*SECTIONS, "all"], default="all")
    args = parser.parse_args()

    sitemap = site_root() / "sitemap.xml"
    if not sitemap.exists():
        print(f"[regen-sitemap] 找不到 {sitemap}", file=sys.stderr)
        return 1

    targets = list(SECTIONS) if args.section == "all" else [args.section]
    for section in targets:
        changed, total = regen_section(sitemap, section)
        state = "已重生" if changed else "無變動（已是最新）"
        print(f"[regen-sitemap] {section} 區{state}，共 {total} 篇")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
