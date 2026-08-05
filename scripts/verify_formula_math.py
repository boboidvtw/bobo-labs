#!/usr/bin/env python3
"""
verify_formula_math.py — formula 文章的確定性數值守門（2026-08-05 建立）

用途：在 /bobo-autopublish 全自主發布 formula 文章前，獨立驗算文章宣稱的數字。
      技術日誌寫錯只是丟臉，公式文章算錯會長期掛在網上並拿去導流，
      LLM 自評（QA #5）擋不住算術錯誤，所以需要這道不靠 LLM 的關卡。

守門原理（三段扣合，缺一不可）：
  1. 文章內嵌 <script type="application/json" id="formula-check"> 宣告公式與測試案例。
  2. 本腳本以 AST 白名單安全求值該公式，比對 case 的 expect。
  3. expect 換算後必須「等於」case 的 text，且 text 必須literally 出現在文章正文。
     → 光是「檢查區塊自己算得對」不算守門，正文寫別的數字一樣要被擋下。

用法：
    python3 scripts/verify_formula_math.py formulas/compound-interest.html
    python3 scripts/verify_formula_math.py --optional writing/2026-01-01-foo.html
    python3 scripts/verify_formula_math.py --json formulas/*.html

退出碼：0 = 全數通過；1 = 有案例失敗或結構不合法。
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import operator
import re
import sys
from pathlib import Path

CHECK_BLOCK = re.compile(
    r'<script\b[^>]*\bid=["\']formula-check["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
SCRIPT_OR_STYLE = re.compile(r"<(script|style)\b.*?</\1>", re.DOTALL | re.IGNORECASE)
TAG = re.compile(r"<[^>]+>")
ENTITY = re.compile(r"&(nbsp|#160|amp|lt|gt|quot|#39);")
ENTITY_MAP = {"nbsp": " ", "#160": " ", "amp": "&", "lt": "<", "gt": ">", "quot": '"', "#39": "'"}

# 白名單求值：預設拒絕。只允許純算術與下列具名函式/常數。
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
FUNCS = {
    "sqrt": math.sqrt, "log": math.log, "ln": math.log, "log10": math.log10,
    "log2": math.log2, "exp": math.exp, "abs": abs, "round": round,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "radians": math.radians, "degrees": math.degrees,
    "min": min, "max": max,
}
CONSTS = {"pi": math.pi, "e": math.e}

MAX_ABS = 1e300      # 中間值上限，擋溢位與 DoS
MAX_EXPONENT = 1000  # 指數上限，擋 9**9**9 這種爆炸


class CheckError(Exception):
    """結構不合法或求值失敗——一律視為守門不通過。"""


# --------------------------------------------------------------------------- 求值

def _eval_node(node: ast.AST, names: dict[str, float]) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise CheckError(f"只允許數值常數，收到 {node.value!r}")
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id in names:
            return float(names[node.id])
        if node.id in CONSTS:
            return CONSTS[node.id]
        raise CheckError(f"未定義的變數 `{node.id}`（需在 case.input 或常數表內）")
    if isinstance(node, ast.BinOp):
        op = BIN_OPS.get(type(node.op))
        if op is None:
            raise CheckError(f"不允許的運算子 {type(node.op).__name__}")
        left, right = _eval_node(node.left, names), _eval_node(node.right, names)
        if isinstance(node.op, ast.Pow) and abs(right) > MAX_EXPONENT:
            raise CheckError(f"指數過大（{right}），超過上限 {MAX_EXPONENT}")
        try:
            return _guard(op(left, right))
        except ArithmeticError as exc:
            raise CheckError(f"運算失敗：{exc}") from exc
    if isinstance(node, ast.UnaryOp):
        op = UNARY_OPS.get(type(node.op))
        if op is None:
            raise CheckError(f"不允許的一元運算子 {type(node.op).__name__}")
        return _guard(op(_eval_node(node.operand, names)))
    if isinstance(node, ast.Call):
        return _eval_call(node, names)
    raise CheckError(f"不允許的語法節點 {type(node).__name__}（白名單外一律拒絕）")


def _eval_call(node: ast.Call, names: dict[str, float]) -> float:
    if not isinstance(node.func, ast.Name):
        raise CheckError("只允許直接呼叫具名函式，不允許屬性存取或間接取得參照")
    if node.keywords:
        raise CheckError("不允許關鍵字引數")
    fn = FUNCS.get(node.func.id)
    if fn is None:
        raise CheckError(f"不允許的函式 `{node.func.id}`（白名單：{', '.join(sorted(FUNCS))}）")
    args = [_eval_node(a, names) for a in node.args]
    try:
        return _guard(float(fn(*args)))
    except CheckError:
        raise
    except Exception as exc:  # 定義域錯誤等
        raise CheckError(f"呼叫 {node.func.id} 失敗：{exc}") from exc


def _guard(value: float) -> float:
    value = float(value)
    if math.isnan(value) or math.isinf(value) or abs(value) > MAX_ABS:
        raise CheckError(f"中間值非有限或過大（{value}）")
    return value


def safe_eval(expr: str, names: dict[str, float]) -> float:
    """以白名單 AST 求值純算術式。任何白名單外的語法一律拒絕。"""
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise CheckError(f"公式語法錯誤：{exc}") from exc
    return _eval_node(tree.body, names)


# --------------------------------------------------------------------------- 解析

def extract_check(html: str) -> dict:
    match = CHECK_BLOCK.search(html)
    if not match:
        raise CheckError('找不到 <script type="application/json" id="formula-check"> 檢查區塊')
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise CheckError(f"formula-check 區塊不是合法 JSON：{exc}") from exc
    if not isinstance(data, dict):
        raise CheckError("formula-check 頂層必須是物件")
    return data


def visible_text(html: str) -> str:
    """取文章可見正文：先整段移除 script/style（含檢查區塊本身），再去標籤。"""
    body = SCRIPT_OR_STYLE.sub(" ", html)
    body = TAG.sub(" ", body)
    body = ENTITY.sub(lambda m: ENTITY_MAP[m.group(1)], body)
    return re.sub(r"\s+", " ", body)


NUMBER_TOKEN = re.compile(r"\d[\d,]*(?:\.\d+)?")
NEAR_MISS_BAND = 1e-3  # 相對誤差在此以內、但不等於目標 → 視為打錯字的重複提及


def find_near_misses(body: str, text: str, target: float, tol: float) -> list[str]:
    """找出「和目標很接近但不相等」的數字。

    同一個計算結果在文中往往被提及兩次以上，只驗「有出現過」會讓打錯的那一處溜掉
    （2026-08-05 實測：1.6289 被改成 1.6290 後仍通過）。這裡限定「小數位數相同、
    相對誤差 < 0.1%」才算近似，避免把文中本來就不同的鄰近數字（如 613,913 與
    607,161，差 1.1%）誤判成錯字。
    """
    want_decimals = _decimals(text)
    misses = []
    for token in NUMBER_TOKEN.findall(body):
        if token == text or _decimals(token) != want_decimals:
            continue
        try:
            value = parse_display_number(token)
        except CheckError:
            continue
        if value == 0 or target == 0:
            continue
        if abs(value - target) <= tol:
            continue
        if abs(value - target) / abs(target) < NEAR_MISS_BAND:
            misses.append(token)
    return sorted(set(misses))


def _decimals(text: str) -> int:
    """text 顯示到小數第幾位——決定它承諾了多少精度。"""
    cleaned = text.replace(",", "").replace(" ", "").strip()
    return len(cleaned.split(".", 1)[1]) if "." in cleaned else 0


def parse_display_number(text: str) -> float:
    """把正文顯示字串（可含千分位逗號）轉成數值。單位與 % 不放進 text。"""
    cleaned = text.replace(",", "").replace(" ", "").strip()
    if not re.fullmatch(r"[+-]?\d+(\.\d+)?", cleaned):
        raise CheckError(f'case.text 必須是純數字字串（可含千分位逗號），收到 "{text}"')
    return float(cleaned)


# --------------------------------------------------------------------------- 驗證

def _tolerance(case: dict, expect: float) -> float:
    if "tol" in case:
        tol = case["tol"]
        if not isinstance(tol, (int, float)) or isinstance(tol, bool) or tol < 0:
            raise CheckError("case.tol 必須是非負數")
        return float(tol)
    return max(abs(expect) * 1e-9, 1e-9)


def verify_case(index: int, case: dict, default_expr: str, body: str) -> str:
    if not isinstance(case, dict):
        raise CheckError(f"case[{index}] 必須是物件")
    # 文章常拿兩個情境相減（「差 55,518」），那個數字不是主公式算得出來的。
    # 允許單一 case 自帶 expr，讓比較型數字一樣被驗，而不是被放過。
    expr = case.get("expr", default_expr)
    if not isinstance(expr, str) or not expr.strip():
        raise CheckError(f"case[{index}].expr 必須是非空字串")
    for key in ("input", "expect", "text"):
        if key not in case:
            raise CheckError(f"case[{index}] 缺少必要欄位 `{key}`")
    inputs = case["input"]
    if not isinstance(inputs, dict) or not inputs:
        raise CheckError(f"case[{index}].input 必須是非空物件")
    for name, value in inputs.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise CheckError(f"case[{index}].input.{name} 必須是數值")

    expect = case["expect"]
    if isinstance(expect, bool) or not isinstance(expect, (int, float)):
        raise CheckError(f"case[{index}].expect 必須是數值")
    expect = float(expect)

    computed = safe_eval(expr, {k: float(v) for k, v in inputs.items()})
    tol = _tolerance(case, expect)
    if abs(computed - expect) > tol:
        raise CheckError(
            f"case[{index}] 算不出宣稱值：公式得 {computed:.10g}，"
            f"expect 寫 {expect:.10g}（容差 {tol:.10g}）"
        )

    scale = case.get("scale", 1)
    if isinstance(scale, bool) or not isinstance(scale, (int, float)) or scale == 0:
        raise CheckError(f"case[{index}].scale 必須是非零數值")
    text = case["text"]
    if not isinstance(text, str) or not text.strip():
        raise CheckError(f"case[{index}].text 必須是非空字串")

    shown = parse_display_number(text)
    target = expect * float(scale)
    # 顯示值的容差由 text 自己的精度決定（末位的半個單位），而非拍腦袋的相對值：
    # 正文寫 "5.12" 只承諾到小數第 2 位，就只用 ±0.005 檢查；寫整數則是 ±0.5。
    text_tol = max(0.5 * 10 ** -_decimals(text), tol * abs(float(scale)))
    if abs(shown - target) > text_tol:
        raise CheckError(
            f"case[{index}] 正文數字與計算結果不符："
            f'text 寫 "{text}"，但 expect×scale = {target:.10g}'
        )
    if text not in body:
        raise CheckError(f'case[{index}] 正文找不到宣稱的數字 "{text}"（檢查區塊與內文脫鉤）')

    misses = find_near_misses(body, text, target, text_tol)
    if misses:
        raise CheckError(
            f'case[{index}] 正文出現與 "{text}" 極接近但不相等的數字：'
            f"{', '.join(misses)}（同一個結果被提及多次、其中一處打錯？）"
        )
    return f'case[{index}] ✓ {expr} = {computed:.10g} → 正文 "{text}"'


def verify_file(path: Path, optional: bool = False) -> dict:
    html = path.read_text(encoding="utf-8")
    result: dict = {"file": str(path), "ok": True, "cases": [], "errors": []}
    try:
        data = extract_check(html)
    except CheckError as exc:
        if optional and "找不到" in str(exc):
            result["skipped"] = "無檢查區塊（--optional）"
            return result
        result["ok"] = False
        result["errors"].append(str(exc))
        return result

    expr = data.get("expr")
    if not isinstance(expr, str) or not expr.strip():
        result["ok"] = False
        result["errors"].append("formula-check.expr 必須是非空字串")
        return result
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        result["ok"] = False
        result["errors"].append("formula-check.cases 必須是至少 1 個案例的陣列")
        return result

    body = visible_text(html)
    for index, case in enumerate(cases):
        try:
            result["cases"].append(verify_case(index, case, expr, body))
        except CheckError as exc:
            result["ok"] = False
            result["errors"].append(str(exc))
    return result


# --------------------------------------------------------------------------- CLI

def main() -> int:
    parser = argparse.ArgumentParser(description="formula 文章數值守門")
    parser.add_argument("files", nargs="+", help="要驗算的 HTML 檔")
    parser.add_argument("--optional", action="store_true",
                        help="沒有檢查區塊時視為跳過而非失敗（給非 formula 文章用）")
    parser.add_argument("--json", action="store_true", help="輸出 JSON 供程式解析")
    args = parser.parse_args()

    results = []
    for name in args.files:
        path = Path(name)
        if not path.is_file():
            results.append({"file": name, "ok": False, "cases": [], "errors": ["檔案不存在"]})
            continue
        results.append(verify_file(path, optional=args.optional))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for res in results:
            label = res["file"]
            if res.get("skipped"):
                print(f"[skip] {label} — {res['skipped']}")
                continue
            print(f"[{'pass' if res['ok'] else 'FAIL'}] {label}")
            for line in res["cases"]:
                print(f"    {line}")
            for err in res["errors"]:
                print(f"    ✗ {err}")

    failed = [r for r in results if not r["ok"]]
    if not args.json:
        print(f"\n[verify-formula-math] {len(results) - len(failed)}/{len(results)} 檔通過")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
