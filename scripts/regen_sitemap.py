#!/usr/bin/env python3
"""
regen_sitemap.py — 冪等重生 sitemap.xml 的 writing 與 formulas 兩區（2026-08-05 建立）

由 regen-sitemap-writing.py（2026-06-08）泛化而來：原版明文「只動 writing 區、不碰
Formula 區」，導致自動化火力轉向 formulas 後，新公式文章不會進 sitemap。

原則不變：
  - 只重寫指定區塊的 <url> 行，其餘（Home / Projects / Formula Index / 註解）完全不動。
  - 區塊必須是連續行，否則中止（避免誤刪夾雜的條目）。
  - 重複執行結果不變（idempotent）。

排序 / lastmod：
  - writing：日期檔（YYYY-MM-DD 前綴）依日期升序、同日依檔名；lastmod 取檔名日期。
  - formulas：依檔名升序；lastmod 保留 sitemap 既有值，新檔取檔案 mtime。

用法：
    python3 scripts/regen_sitemap.py              # 兩區都重生
    python3 scripts/regen_sitemap.py --section formulas
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

BASE = "https://labs.moneyai168.com"
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
LASTMOD = re.compile(r"<lastmod>([^<]+)</lastmod>")

# 每區的設定。loc 正則只吃 *.html，所以 `/formulas/` 索引頁那行不會被視為區塊成員。
# exclude：目錄索引頁不進文章區（`/formulas/` 已由 sitemap 的 Formula Library Index
# 區塊單獨收錄，再收 `/formulas/index.html` 會變成同一頁的重複 URL）。
SECTIONS: dict[str, dict] = {
    "writing": {"dir": "writing", "priority": "0.5", "by_date": True, "exclude": {"index.html"}},
    "formulas": {"dir": "formulas", "priority": "0.8", "by_date": False, "exclude": {"index.html"}},
}


def site_root() -> Path:
    """腳本位於 <repo>/scripts/，repo 根為其上層。"""
    return Path(__file__).resolve().parent.parent


def loc_pattern(dirname: str) -> re.Pattern[str]:
    return re.compile(rf"/{re.escape(dirname)}/([^<\"]+\.html)")


def existing_lastmods(sitemap_text: str, pattern: re.Pattern[str]) -> dict[str, str]:
    """抽出該區每檔既有的 lastmod，供無日期檔名保留原值。"""
    result: dict[str, str] = {}
    for line in sitemap_text.splitlines():
        loc, mod = pattern.search(line), LASTMOD.search(line)
        if loc and mod:
            result[loc.group(1)] = mod.group(1)
    return result


def derive_lastmod(basename: str, prior: dict[str, str], directory: Path, by_date: bool) -> str:
    """日期檔→檔名日期；否則→既有值，無則檔案 mtime。"""
    match = DATE_PREFIX.match(basename)
    if by_date and match:
        return match.group(1)
    if basename in prior:
        return prior[basename]
    mtime = (directory / basename).stat().st_mtime
    return datetime.fromtimestamp(mtime).date().isoformat()


def sort_key(basename: str, by_date: bool) -> tuple[int, str, str]:
    """日期檔(0)依(日期,檔名)；非日期檔(1)依檔名。"""
    match = DATE_PREFIX.match(basename) if by_date else None
    return (0, match.group(1), basename) if match else (1, "", basename)


def build_block(root: Path, section: str, prior: dict[str, str]) -> list[str]:
    config = SECTIONS[section]
    directory = root / config["dir"]
    names = sorted(
        (p.name for p in directory.glob("*.html") if p.name not in config["exclude"]),
        key=lambda n: sort_key(n, config["by_date"]),
    )
    return [
        f"  <url><loc>{BASE}/{config['dir']}/{name}</loc>"
        f"<lastmod>{derive_lastmod(name, prior, directory, config['by_date'])}</lastmod>"
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

    new_block = build_block(site_root(), section, existing_lastmods(text, pattern))
    new_text = "\n".join(lines[:first] + new_block + lines[last + 1:]) + "\n"
    if new_text == text:
        return False, len(new_block)
    sitemap_path.write_text(new_text, encoding="utf-8")
    return True, len(new_block)


def main() -> int:
    parser = argparse.ArgumentParser(description="冪等重生 sitemap 的 writing / formulas 區")
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
