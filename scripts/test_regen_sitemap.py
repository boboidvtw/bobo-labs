#!/usr/bin/env python3
"""
test_regen_sitemap.py — regen_sitemap 的 lastmod 規格（2026-08-29 建立）

站台沒有測試框架，沿用 test_verify_formula_math.py 的慣例：純 assert 的可執行規格檔。
    python3 scripts/test_regen_sitemap.py

起因：2026-08-29 比對發現 27/28 篇公式頁的 sitemap lastmod 是錯的。舊的 derive_lastmod
對無日期檔名「保留 sitemap 既有值」，等於首次進 sitemap 後就永遠凍結——2026-06-18 的
長尾標題改動因此從未反映到 sitemap，Google 讀到「5/28 之後沒變過」就沒有回來重爬的理由。

所以這支的重點不是「產得出 sitemap」，而是**每一種「內容變了但 lastmod 沒變」都會被抓到**。
第一條測試就是那個 bug：它在修好之前必須是紅的（只證明 happy path 等於沒有守門）。
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from regen_sitemap import SECTIONS, build_block, derive_lastmod, regen_section  # noqa: E402

PASSED = 0
FAILED: list[str] = []
TODAY = date.today().isoformat()


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASSED
    if condition:
        PASSED += 1
    else:
        FAILED.append(f"{name}{f' — {detail}' if detail else ''}")


def git(repo: Path, *args: str, when: str | None = None) -> None:
    """在 repo 跑 git；when 可指定 commit 日期（YYYY-MM-DD）以模擬歷史。"""
    env = dict(os.environ)
    if when:
        stamp = f"{when}T12:00:00+0800"
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = stamp
    subprocess.run(["git", *args], cwd=repo, env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def make_repo(root: Path, dirname: str = "formulas") -> Path:
    """建一個帶指定內容目錄的 git repo。"""
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "spec@example.com")
    git(root, "config", "user.name", "spec")
    (root / dirname).mkdir()
    return root / dirname


def write(directory: Path, name: str, body: str) -> Path:
    path = directory / name
    path.write_text(body, encoding="utf-8")
    return path


def run(tmp: Path) -> None:
    # ---- 這條就是 2026-08-29 抓到的 bug：改過的頁，lastmod 必須跟著動 ----
    formulas = make_repo(tmp / "edited")
    write(formulas, "compound-interest.html", "<h1>v1</h1>")
    git(formulas.parent, "add", "-A")
    git(formulas.parent, "commit", "-m", "add", when="2026-05-28")
    write(formulas, "compound-interest.html", "<h1>v2 長尾標題</h1>")
    git(formulas.parent, "add", "-A")
    git(formulas.parent, "commit", "-m", "retitle", when="2026-06-18")

    got = derive_lastmod("compound-interest.html", formulas, by_date=False)
    check("改過的公式頁 → lastmod 取 git 最後改動日", got == "2026-06-18", f"得到 {got}")
    check("不得停在首次進 sitemap 的日期", got != "2026-05-28", f"得到 {got}")

    # ---- 未提交的改動＝現在正在改，算今天 ----
    write(formulas, "compound-interest.html", "<h1>v3 尚未提交</h1>")
    got = derive_lastmod("compound-interest.html", formulas, by_date=False)
    check("有未提交改動 → 算今天", got == TODAY, f"得到 {got}")

    # ---- 全新檔（autopublish promote 當下還沒 commit）----
    write(formulas, "brand-new.html", "<h1>新公式</h1>")
    got = derive_lastmod("brand-new.html", formulas, by_date=False)
    check("未追蹤的新檔 → 算今天", got == TODAY, f"得到 {got}")

    # ---- writing 區不受影響：檔名日期＝發布日，維持原行為 ----
    #      （全站注入 analytics 的機械式 commit 不該讓 93 篇都宣稱「已修改」）
    posts = make_repo(tmp / "writing_repo")
    write(posts, "2026-05-14-nomad-recon-sprint-d.html", "<h1>post</h1>")
    git(posts.parent, "add", "-A")
    git(posts.parent, "commit", "-m", "analytics", when="2026-06-04")
    got = derive_lastmod("2026-05-14-nomad-recon-sprint-d.html", posts, by_date=True)
    check("writing 日期檔 → 仍取檔名日期", got == "2026-05-14", f"得到 {got}")

    # ---- writing 的無日期前綴舊檔：取首次收錄日（發布日），不是 analytics 那次 ----
    write(posts, "antigravity-stack.html", "<h1>legacy</h1>")
    git(posts.parent, "add", "-A")
    git(posts.parent, "commit", "-m", "real Writing pages", when="2026-05-18")
    path = posts / "antigravity-stack.html"
    path.write_text("<h1>legacy</h1><script src='beacon'></script>", encoding="utf-8")
    git(posts.parent, "add", "-A")
    git(posts.parent, "commit", "-m", "analytics beacon", when="2026-06-04")
    got = derive_lastmod("antigravity-stack.html", posts, by_date=True)
    check("writing 無前綴檔 → 取 git 首次收錄日", got == "2026-05-18", f"得到 {got}")
    check("不得因注入 analytics 就宣稱已更新", got != "2026-06-04", f"得到 {got}")

    # ---- 不在 git 底下也不能炸，退回 mtime ----
    loose = tmp / "no_git" / "formulas"
    loose.mkdir(parents=True)
    path = write(loose, "orphan.html", "<h1>x</h1>")
    os.utime(path, (1_780_000_000, 1_780_000_000))  # 2026-06-08 前後
    expected = date.fromtimestamp(path.stat().st_mtime).isoformat()
    got = derive_lastmod("orphan.html", loose, by_date=False)
    check("無 git → 退回檔案 mtime 不中止", got == expected, f"得到 {got}")

    # ---- 冪等：連跑兩次同一答案 ----
    clean = make_repo(tmp / "idem")
    write(clean, "rule-of-72.html", "<h1>72</h1>")
    git(clean.parent, "add", "-A")
    git(clean.parent, "commit", "-m", "add", when="2026-06-07")
    first = derive_lastmod("rule-of-72.html", clean, by_date=False)
    second = derive_lastmod("rule-of-72.html", clean, by_date=False)
    check("同一檔連算兩次結果相同", first == second, f"{first} vs {second}")
    check("乾淨且已提交的檔 → 取 commit 日", first == "2026-06-07", f"得到 {first}")


def run_guides(tmp: Path) -> None:
    """guides 區規格（2026-08-31 併入）。

    與 formulas 的差別只有兩點，但兩點都是「不修就等於沒併」：
      1. lastmod 必須是精確到秒的 W3C datetime。日期粒度會讓 2026-08-30 23:53 的改動
         被寫成 `2026-08-30`＝當日 00:00，比 sitemap 現值還舊，等於把剛解掉的凍結裝回去。
      2. 必須保留 `<changefreq>`。guides 那行本來就有，靜默掉它是拿併入換掉一個既有欄位。
    """
    check("SECTIONS 收錄 guides", "guides" in SECTIONS)

    guides = make_repo(tmp / "guides_repo", "guides")
    write(guides, "mac-mini-vs-mac-studio-2026.html", "<h1>v1</h1>")
    git(guides.parent, "add", "-A")
    git(guides.parent, "commit", "-m", "add", when="2026-08-30")

    got = derive_lastmod("mac-mini-vs-mac-studio-2026.html", guides,
                         by_date=False, precise=True)
    check("guides lastmod 精確到秒（含 T）", "T" in got, f"得到 {got}")
    check("guides lastmod 帶時區", got[-6] in "+-" or got.endswith("Z"), f"得到 {got}")
    check("日期部分＝該檔的 commit 日", got.startswith("2026-08-30T"), f"得到 {got}")
    check("嚴格晚於同日的日期型值（否則等於沒 bump）",
          got > "2026-08-30", f"得到 {got}")

    # 未提交的改動＝現在，也要是精確時間戳
    write(guides, "mac-mini-vs-mac-studio-2026.html", "<h1>v2 尚未提交</h1>")
    got = derive_lastmod("mac-mini-vs-mac-studio-2026.html", guides,
                         by_date=False, precise=True)
    check("未提交改動 → 精確的今天時間戳",
          got.startswith(TODAY) and "T" in got, f"得到 {got}")

    # 無 git 也不能炸
    loose = tmp / "no_git_guides" / "guides"
    loose.mkdir(parents=True)
    path = write(loose, "orphan.html", "<h1>x</h1>")
    os.utime(path, (1_780_000_000, 1_780_000_000))
    got = derive_lastmod("orphan.html", loose, by_date=False, precise=True)
    check("無 git → 退回 mtime 的精確時間戳不中止", "T" in got, f"得到 {got}")

    # precise 是選項，不得污染既有兩區
    plain = derive_lastmod("mac-mini-vs-mac-studio-2026.html", guides, by_date=False)
    check("不帶 precise 時維持日期粒度（formulas 不受影響）",
          "T" not in plain, f"得到 {plain}")


def run_changefreq(tmp: Path) -> None:
    """changefreq 只出現在有設定的區，且只出現在該區。"""
    import regen_sitemap

    root = tmp / "cf_site"
    guides = make_repo(root, "guides")
    (root / "formulas").mkdir()
    write(guides, "mac-mini-vs-mac-studio-2026.html", "<h1>v1</h1>")
    write(root / "formulas", "rule-of-72.html", "<h1>72</h1>")
    git(root, "add", "-A")
    git(root, "commit", "-m", "add", when="2026-08-30")

    original_root = regen_sitemap.site_root
    regen_sitemap.site_root = lambda: root  # type: ignore[assignment]
    try:
        guide_lines = build_block(root, "guides")
        formula_lines = build_block(root, "formulas")
    finally:
        regen_sitemap.site_root = original_root  # type: ignore[assignment]

    check("guides 行保留 changefreq",
          all("<changefreq>monthly</changefreq>" in ln for ln in guide_lines),
          guide_lines)
    check("guides 行的 priority 是 0.9",
          all("<priority>0.9</priority>" in ln for ln in guide_lines), guide_lines)
    check("欄位順序為 loc→lastmod→changefreq→priority",
          all(ln.index("<lastmod>") < ln.index("<changefreq>") < ln.index("<priority>")
              for ln in guide_lines), guide_lines)
    check("formulas 行不得長出 changefreq（既有輸出不能被改）",
          all("changefreq" not in ln for ln in formula_lines), formula_lines)


GUIDES_SKELETON = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://labs.moneyai168.com/</loc><lastmod>2026-05-01</lastmod><priority>1.0</priority></url>
  <!-- Guides -->
  <url><loc>https://labs.moneyai168.com/guides/mac-mini-vs-mac-studio-2026.html</loc><lastmod>2026-08-30</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <!-- Formula Library -->
  <url><loc>https://labs.moneyai168.com/formulas/rule-of-72.html</loc><lastmod>2026-05-28</lastmod><priority>0.8</priority></url>
</urlset>
"""


def run_guides_integration(tmp: Path) -> None:
    """整合層：日期粒度的既有值必須被精確時間戳取代，且不得動到別區。"""
    import regen_sitemap

    root = tmp / "guides_site"
    guides = make_repo(root, "guides")
    (root / "formulas").mkdir()
    write(guides, "mac-mini-vs-mac-studio-2026.html", "<h1>v1</h1>")
    write(root / "formulas", "rule-of-72.html", "<h1>72</h1>")
    git(root, "add", "-A")
    git(root, "commit", "-m", "add", when="2026-08-30")

    sitemap = root / "sitemap.xml"
    sitemap.write_text(GUIDES_SKELETON, encoding="utf-8")

    original_root = regen_sitemap.site_root
    regen_sitemap.site_root = lambda: root  # type: ignore[assignment]
    try:
        changed, count = regen_section(sitemap, "guides")
        after = sitemap.read_text(encoding="utf-8")
        changed_again, _ = regen_section(sitemap, "guides")
        stable = sitemap.read_text(encoding="utf-8")
    finally:
        regen_sitemap.site_root = original_root  # type: ignore[assignment]

    line = next(ln for ln in after.splitlines() if "mac-mini" in ln)
    check("guides 收錄 1 篇", count == 1, f"得到 {count}")
    check("日期粒度值被換成精確時間戳",
          "<lastmod>2026-08-30T" in line, line)
    check("changefreq 沒有在重生中消失",
          "<changefreq>monthly</changefreq>" in line, line)
    check("<!-- Guides --> 註解沒被吃掉", "<!-- Guides -->" in after)
    check("Home 那行沒被動到",
          "<loc>https://labs.moneyai168.com/</loc><lastmod>2026-05-01" in after)
    check("formulas 那行沒被動到",
          "rule-of-72.html</loc><lastmod>2026-05-28</lastmod><priority>0.8</priority>" in after,
          [ln for ln in after.splitlines() if "rule-of-72" in ln])
    check("guides 第二次重生無變動（冪等）", not changed_again)
    check("guides 兩次重生內容一致", after == stable)
    check("重生後仍是合法 XML", _xml_ok(stable), stable[:200])


def _xml_ok(text: str) -> bool:
    import xml.dom.minidom
    try:
        xml.dom.minidom.parseString(text)
        return True
    except Exception:
        return False


SITEMAP_SKELETON = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://labs.moneyai168.com/</loc><lastmod>2026-05-01</lastmod><priority>1.0</priority></url>
  <!-- Formula Library -->
  <url><loc>https://labs.moneyai168.com/formulas/compound-interest.html</loc><lastmod>2026-05-28</lastmod><priority>0.8</priority></url>
  <url><loc>https://labs.moneyai168.com/formulas/rule-of-72.html</loc><lastmod>2026-05-28</lastmod><priority>0.8</priority></url>
</urlset>
"""


def run_integration(tmp: Path) -> None:
    """整合層：既有 sitemap 帶著過期值時，重生後必須被糾正而不是被沿用。"""
    import regen_sitemap

    root = tmp / "site"
    formulas = make_repo(root)
    write(formulas, "compound-interest.html", "<h1>v1</h1>")
    write(formulas, "rule-of-72.html", "<h1>72</h1>")
    git(root, "add", "-A")
    git(root, "commit", "-m", "add", when="2026-05-28")
    write(formulas, "compound-interest.html", "<h1>v2 長尾標題</h1>")
    git(root, "add", "-A")
    git(root, "commit", "-m", "retitle", when="2026-06-18")

    sitemap = root / "sitemap.xml"
    sitemap.write_text(SITEMAP_SKELETON, encoding="utf-8")

    original_root = regen_sitemap.site_root
    regen_sitemap.site_root = lambda: root  # type: ignore[assignment]
    try:
        changed, count = regen_section(sitemap, "formulas")
        after = sitemap.read_text(encoding="utf-8")
        # 冪等：第二次不應再有變動
        changed_again, _ = regen_section(sitemap, "formulas")
        stable = sitemap.read_text(encoding="utf-8")
    finally:
        regen_sitemap.site_root = original_root  # type: ignore[assignment]

    check("重生後回報有變動", changed)
    check("兩篇都收錄", count == 2, f"得到 {count}")
    check("改過那篇的過期值被糾正",
          "compound-interest.html</loc><lastmod>2026-06-18" in after,
          [ln for ln in after.splitlines() if "compound-interest" in ln])
    check("沒改過那篇維持原日期",
          "rule-of-72.html</loc><lastmod>2026-05-28" in after,
          [ln for ln in after.splitlines() if "rule-of-72" in ln])
    check("非本區的 Home 那行沒被動到",
          "<loc>https://labs.moneyai168.com/</loc><lastmod>2026-05-01" in after)
    check("第二次重生無變動（冪等）", not changed_again)
    check("兩次重生內容一致", after == stable)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        run(Path(td))
        run_integration(Path(td))
        run_guides(Path(td))
        run_changefreq(Path(td))
        run_guides_integration(Path(td))
    total = PASSED + len(FAILED)
    for line in FAILED:
        print(f"  ✗ {line}")
    print(f"\n[test_regen_sitemap] {PASSED}/{total} 通過")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
