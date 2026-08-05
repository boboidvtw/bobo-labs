#!/usr/bin/env python3
"""
regen-sitemap-writing.py — 已由 regen_sitemap.py 取代（2026-08-05）

原本只重生 writing 區、明文不碰 formulas 區。自動化火力轉向 formulas 後這個限制
變成落差來源，邏輯已泛化到 scripts/regen_sitemap.py（可指定 --section）。

本檔保留為轉呼叫的相容層：舊呼叫（人工手打、舊文件）仍會得到正確的 writing 區重生。
新的呼叫請直接用：python3 scripts/regen_sitemap.py
"""
import runpy
import sys

if __name__ == "__main__":
    print("[regen-sitemap] 提醒：本腳本已由 regen_sitemap.py 取代，"
          "改跑 `python3 scripts/regen_sitemap.py`（可一併重生 formulas 區）",
          file=sys.stderr)
    sys.argv = [sys.argv[0], "--section", "writing"]
    runpy.run_path(str(__import__("pathlib").Path(__file__).parent / "regen_sitemap.py"),
                   run_name="__main__")
