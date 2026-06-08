#!/usr/bin/env python3
"""
regen-sitemap-writing.py — 冪等重生 sitemap.xml 的 writing 區
用途：掃 writing/*.html，重建 sitemap.xml 內所有 /writing/ 的 <url> 條目，
      使 autopublish/boboweb 自動發文後 sitemap 永不落差。
原則：只動 writing 區，不碰 Home / Formula 區；重複執行結果不變（idempotent）。
建立：2026-06-08（治本：autopublish/boboweb promote 不更新 sitemap 的歷史落差）

排序：日期檔（YYYY-MM-DD 前綴）依日期升序、同日依檔名；非日期檔置後依檔名。
lastmod：日期檔取檔名日期（確定性）；非日期檔保留 sitemap 既有值，無則取檔案 mtime。
"""

import re
import sys
from datetime import date, datetime
from pathlib import Path

BASE = "https://labs.moneyai168.com"
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
WRITING_LOC = re.compile(r"/writing/([^<\"]+\.html)")
LASTMOD = re.compile(r"<lastmod>([^<]+)</lastmod>")


def site_root() -> Path:
    """腳本位於 <repo>/scripts/，repo 根為其上層。"""
    return Path(__file__).resolve().parent.parent


def existing_lastmods(sitemap_text: str) -> dict[str, str]:
    """從現有 sitemap 抽出 writing 每檔的 lastmod，供非日期檔保留。"""
    result: dict[str, str] = {}
    for line in sitemap_text.splitlines():
        loc = WRITING_LOC.search(line)
        mod = LASTMOD.search(line)
        if loc and mod:
            result[loc.group(1)] = mod.group(1)
    return result


def derive_lastmod(basename: str, prior: dict[str, str], root: Path) -> str:
    """日期檔→檔名日期；非日期檔→既有值，無則檔案 mtime。"""
    m = DATE_PREFIX.match(basename)
    if m:
        return m.group(1)
    if basename in prior:
        return prior[basename]
    mtime = (root / "writing" / basename).stat().st_mtime
    return datetime.fromtimestamp(mtime).date().isoformat()


def sort_key(basename: str) -> tuple[int, str, str]:
    """日期檔(0)優先依(日期,檔名)；非日期檔(1)依檔名。"""
    m = DATE_PREFIX.match(basename)
    if m:
        return (0, m.group(1), basename)
    return (1, "", basename)


def build_writing_block(root: Path, prior: dict[str, str]) -> list[str]:
    files = sorted(
        (p.name for p in (root / "writing").glob("*.html")),
        key=sort_key,
    )
    lines = []
    for name in files:
        mod = derive_lastmod(name, prior, root)
        lines.append(
            f"  <url><loc>{BASE}/writing/{name}</loc>"
            f"<lastmod>{mod}</lastmod><priority>0.5</priority></url>"
        )
    return lines


def regen(sitemap_path: Path) -> bool:
    """重生 writing 區，回傳是否有變動。"""
    text = sitemap_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    prior = existing_lastmods(text)

    writing_idx = [i for i, ln in enumerate(lines) if WRITING_LOC.search(ln)]
    if not writing_idx:
        raise SystemExit("[regen-sitemap] 找不到任何 /writing/ 條目，sitemap 結構異常，中止")

    first, last = writing_idx[0], writing_idx[-1]
    # 確認 writing 條目連續（中間無夾雜其他 url），避免誤刪
    if writing_idx != list(range(first, last + 1)):
        raise SystemExit("[regen-sitemap] writing 條目非連續區塊，需人工檢查，中止")

    new_block = build_writing_block(site_root(), prior)
    new_lines = lines[:first] + new_block + lines[last + 1:]
    new_text = "\n".join(new_lines) + "\n"

    if new_text == text:
        return False
    sitemap_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    root = site_root()
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        print(f"[regen-sitemap] 找不到 {sitemap}", file=sys.stderr)
        return 1
    changed = regen(sitemap)
    total = len(list((root / "writing").glob("*.html")))
    if changed:
        print(f"[regen-sitemap] writing 區已重生，共 {total} 篇")
    else:
        print(f"[regen-sitemap] 無變動，writing 區已是最新（{total} 篇）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
