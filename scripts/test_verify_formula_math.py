#!/usr/bin/env python3
"""
test_verify_formula_math.py — verify_formula_math 的規格（2026-08-05 建立）

站台沒有測試框架，所以這支用純 assert 寫成可直接執行的規格檔：
    python3 scripts/test_verify_formula_math.py

重點不是「守門會放行正確的文章」，而是「守門會擋下每一種錯法」——
只證明 happy path 等於沒有守門（2026-08-04 YouTube 擴充功能的教訓）。
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from verify_formula_math import (  # noqa: E402
    CheckError, parse_display_number, safe_eval, verify_file, visible_text,
)

PASSED = 0
FAILED: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASSED
    if condition:
        PASSED += 1
    else:
        FAILED.append(f"{name}{(' — ' + detail) if detail else ''}")


def expect_raises(name: str, fn, needle: str = "") -> None:
    try:
        fn()
    except CheckError as exc:
        check(name, needle in str(exc), f"訊息未含 '{needle}'：{exc}")
    except Exception as exc:  # noqa: BLE001
        FAILED.append(f"{name} — 拋出非 CheckError：{type(exc).__name__}: {exc}")
    else:
        FAILED.append(f"{name} — 應該要擋卻放行了")


ARTICLE = """<!DOCTYPE html><html><head><title>t</title>
<script type="application/json" id="formula-check">
{{"expr": "P * (1 + r/n) ** (n*t)",
  "cases": [{{"input": {{"P": 1000000, "r": 0.05, "n": 1, "t": 30}},
             "expect": 4321942.375, "tol": 1, "text": "{shown}"}}]}}
</script></head>
<body><article><p class="article-lede">{lede}</p>
<div class="article-body"><p>本金 100 萬、年利率 5%、每年複利一次，30 年後是 {shown} 元。</p></div>
</article></body></html>"""


def write(tmp: Path, name: str, content: str) -> Path:
    path = tmp / name
    path.write_text(content, encoding="utf-8")
    return path


def run(tmp: Path) -> None:
    # --- 安全求值：白名單內 ---
    check("四則運算", abs(safe_eval("1 + 2 * 3", {}) - 7) < 1e-12)
    check("次方", abs(safe_eval("2 ** 10", {}) - 1024) < 1e-12)
    check("變數代入", abs(safe_eval("P * r", {"P": 100, "r": 0.05}) - 5) < 1e-12)
    check("白名單函式", abs(safe_eval("sqrt(16)", {}) - 4) < 1e-12)
    check("常數 pi", abs(safe_eval("pi", {}) - 3.14159265) < 1e-6)
    check("複利公式", abs(safe_eval("P*(1+r/n)**(n*t)",
                                {"P": 1e6, "r": 0.05, "n": 1, "t": 30}) - 4321942.375) < 1.0)

    # --- 安全求值：白名單外一律拒絕（擋「取得參照」而非列舉呼叫寫法）---
    expect_raises("擋屬性存取", lambda: safe_eval("(1).__class__", {}), "不允許")
    expect_raises("擋間接取參照", lambda: safe_eval("().__class__.__base__", {}), "不允許")
    expect_raises("擋 import", lambda: safe_eval("__import__('os')", {}), "不允許的函式")
    expect_raises("擋 open", lambda: safe_eval("open('/etc/passwd')", {}), "不允許的函式")
    expect_raises("擋 subscript", lambda: safe_eval("[1,2][0]", {}), "不允許")
    expect_raises("擋 lambda", lambda: safe_eval("(lambda: 1)()", {}), "不允許")
    expect_raises("擋比較運算", lambda: safe_eval("1 < 2", {}), "不允許")
    expect_raises("擋字串常數", lambda: safe_eval("'abc'", {}), "只允許數值常數")
    expect_raises("擋未定義變數", lambda: safe_eval("Q * 2", {}), "未定義的變數")
    expect_raises("擋關鍵字引數", lambda: safe_eval("round(1.5, ndigits=0)", {}), "關鍵字引數")
    expect_raises("擋指數爆炸", lambda: safe_eval("9 ** 9 ** 9", {}), "指數過大")
    expect_raises("擋除以零", lambda: safe_eval("1/0", {}), "")
    expect_raises("擋定義域錯誤", lambda: safe_eval("sqrt(-1)", {}), "失敗")

    # --- 顯示字串解析 ---
    check("千分位", abs(parse_display_number("4,321,942") - 4321942) < 1e-9)
    check("小數", abs(parse_display_number("1.36") - 1.36) < 1e-12)
    expect_raises("擋帶單位的 text", lambda: parse_display_number("4321942 元"), "純數字")
    expect_raises("擋帶百分號的 text", lambda: parse_display_number("1.36%"), "純數字")

    # --- 可見正文抽取 ---
    body = visible_text(ARTICLE.format(shown="4,321,942", lede="lede"))
    check("正文含內文數字", "4,321,942" in body)
    check("正文排除檢查區塊", "formula-check" not in body and '"expect"' not in body)

    # --- 端到端：正確的文章要過 ---
    good = write(tmp, "good.html", ARTICLE.format(shown="4,321,942", lede="lede"))
    res = verify_file(good)
    check("正確文章通過", res["ok"], str(res["errors"]))

    # --- 端到端：每一種錯法都要被擋 ---
    # 1. 正文數字與計算結果不符（最關鍵的一種：檢查區塊對、內文寫錯）
    bad_text = ARTICLE.replace('"text": "{shown}"', '"text": "5,000,000"')
    bad = write(tmp, "bad_text.html", bad_text.format(shown="5,000,000", lede="lede"))
    res = verify_file(bad)
    check("擋正文數字算不出來", not res["ok"], "應擋下 text 與 expect 不符")
    check("擋錯數字有講原因", any("不符" in e for e in res["errors"]), str(res["errors"]))

    # 2. expect 與公式算出來的不符
    bad_expect = ARTICLE.replace('"expect": 4321942.375', '"expect": 9999999')
    bad = write(tmp, "bad_expect.html", bad_expect.format(shown="9,999,999", lede="lede"))
    res = verify_file(bad)
    check("擋 expect 與公式不符", not res["ok"])
    check("擋 expect 有講原因", any("算不出宣稱值" in e for e in res["errors"]), str(res["errors"]))

    # 3. 檢查區塊算得對，但正文根本沒出現這個數字（脫鉤）
    detached = ARTICLE.format(shown="4,321,942", lede="lede").replace(
        "30 年後是 4,321,942 元", "30 年後會長很多"
    )
    bad = write(tmp, "detached.html", detached)
    res = verify_file(bad)
    check("擋檢查區塊與內文脫鉤", not res["ok"])
    check("脫鉤有講原因", any("找不到宣稱的數字" in e for e in res["errors"]), str(res["errors"]))

    # 4. 完全沒有檢查區塊
    bare = write(tmp, "bare.html", "<html><body><p>沒有檢查區塊</p></body></html>")
    check("擋缺檢查區塊", not verify_file(bare)["ok"])
    check("--optional 才放行缺區塊", verify_file(bare, optional=True)["ok"])

    # 5. 結構不合法
    broken = write(tmp, "broken.html",
                   '<script type="application/json" id="formula-check">{not json}</script>')
    check("擋壞掉的 JSON", not verify_file(broken)["ok"])

    no_cases = write(tmp, "nocases.html",
                     '<script type="application/json" id="formula-check">'
                     '{"expr": "1+1", "cases": []}</script>')
    check("擋零案例", not verify_file(no_cases)["ok"])

    # 6. 公式裡藏程式碼
    evil = write(tmp, "evil.html",
                 '<script type="application/json" id="formula-check">'
                 '{"expr": "__import__(\'os\').system(\'echo pwned\')",'
                 ' "cases": [{"input": {"x": 1}, "expect": 0, "text": "0"}]}</script><p>0</p>')
    res = verify_file(evil)
    check("擋公式內程式碼", not res["ok"], str(res["errors"]))

    # 7. scale：百分比案例
    pct = ('<script type="application/json" id="formula-check">'
           '{"expr": "(1 + r/n) ** n - 1",'
           ' "cases": [{"input": {"r": 0.05, "n": 12}, "expect": 0.05116189788,'
           ' "tol": 1e-8, "scale": 100, "text": "5.12"}]}</script>'
           '<p>實質年利率是 5.12%。</p>')
    check("scale 百分比通過", verify_file(write(tmp, "pct.html", pct))["ok"])

    pct_bad = pct.replace('"text": "5.12"', '"text": "5.99"').replace("5.12%", "5.99%")
    check("擋 scale 百分比寫錯", not verify_file(write(tmp, "pct_bad.html", pct_bad))["ok"])

    # 8. per-case expr：比較型數字（兩情境相減）也要能被驗
    diff = ('<script type="application/json" id="formula-check">'
            '{"expr": "F / (1+r) ** t",'
            ' "cases": [{"input": {"F": 1000000, "r": 0.05, "t": 10},'
            '            "expect": 613913.2535, "tol": 1, "text": "613,913"},'
            '           {"expr": "F/(1+a)**t - F/(1+b)**t",'
            '            "input": {"F": 1000000, "a": 0.05, "b": 0.06, "t": 10},'
            '            "expect": 55518.4766, "tol": 1, "text": "55,518"}]}'
            '</script><p>算出 613,913 元，和另一情境相差 55,518 元。</p>')
    res = verify_file(write(tmp, "diff.html", diff))
    check("per-case expr 通過", res["ok"], str(res["errors"]))

    diff_bad = diff.replace('"text": "55,518"', '"text": "99,999"').replace("55,518 元", "99,999 元")
    check("擋 per-case expr 算錯", not verify_file(write(tmp, "diff_bad.html", diff_bad))["ok"])

    empty_expr = diff.replace('"expr": "F/(1+a)**t - F/(1+b)**t"', '"expr": ""')
    check("擋 case.expr 空字串", not verify_file(write(tmp, "empty_expr.html", empty_expr))["ok"])

    # 9. 近似錯字：同一結果提及兩次、其中一處打錯，光靠「有出現過」會漏掉
    twice = ('<script type="application/json" id="formula-check">'
             '{"expr": "(1+r) ** t",'
             ' "cases": [{"input": {"r": 0.05, "t": 10}, "expect": 1.628894626777,'
             '            "tol": 1e-9, "text": "1.6289"}]}</script>'
             '<p>折現因子是 1.6289，也就是說 1.6289 倍。</p>')
    check("同一數字提兩次都對 → 通過", verify_file(write(tmp, "twice.html", twice))["ok"])

    typo = twice.replace("也就是說 1.6289 倍", "也就是說 1.6290 倍")
    res = verify_file(write(tmp, "typo.html", typo))
    check("擋重複提及其中一處打錯", not res["ok"], str(res["errors"]))
    check("近似錯字有講原因", any("極接近但不相等" in e for e in res["errors"]), str(res["errors"]))

    # 近似偵測不可誤傷「本來就不同」的鄰近數字（613,913 與 607,161 差 1.1%）
    neighbours = ('<script type="application/json" id="formula-check">'
                  '{"expr": "F / (1 + r/n) ** (n*t)",'
                  ' "cases": [{"input": {"F": 1000000, "r": 0.05, "n": 1, "t": 10},'
                  '            "expect": 613913.2535, "tol": 1, "text": "613,913"}]}</script>'
                  '<p>年複利 613,913 元，月複利則是 607,161 元。</p>')
    res = verify_file(write(tmp, "neighbours.html", neighbours))
    check("不誤傷差 1% 的鄰近數字", res["ok"], str(res["errors"]))


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        run(Path(td))
    total = PASSED + len(FAILED)
    for line in FAILED:
        print(f"  ✗ {line}")
    print(f"\n[test_verify_formula_math] {PASSED}/{total} 通過")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
