"""Harbor Books Definition of Done — same ```dod``` contract as Penti GOAL.md.

One slice per loop. After Print, the first unchecked row is verified against
the command + output (+ leftover.csv for write-left). Pass → checked.
"""

from __future__ import annotations

import copy
import csv
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

# Seven pipe-separated fields — same layout next-slice.sh / verify-dod.sh parse.
# id | status | verify | spec | cwd | files | title
BUDGET_DOD_ROWS: List[Dict[str, str]] = [
    {
        "id": "DOD-01",
        "status": "unchecked",
        "verify": "cmd",
        "spec": "see-budget",
        "cwd": "books",
        "files": "books/budget.csv",
        "title": "The register",
    },
    {
        "id": "DOD-02",
        "status": "unchecked",
        "verify": "cmd",
        "spec": "see-spent",
        "cwd": "books",
        "files": "books/receipt.txt",
        "title": "The cash",
    },
    {
        "id": "DOD-03",
        "status": "unchecked",
        "verify": "cmd",
        "spec": "write-left",
        "cwd": "books",
        "files": "books/leftover.csv",
        "title": "The books match",
    },
]


def books_dir(override: Optional[Path] = None) -> Path:
    if override is not None:
        return Path(override)
    env = (os.getenv("ACCRUAL_BOOKS_DIR") or "").strip()
    if env:
        return Path(env)
    return Path(__file__).resolve().parent / "books"


def fresh_rows() -> List[Dict[str, Any]]:
    return copy.deepcopy(BUDGET_DOD_ROWS)


def format_registry(rows: List[Dict[str, Any]]) -> str:
    lines = ["```dod"]
    for row in rows:
        lines.append(
            " | ".join(
                [
                    row["id"],
                    row.get("status") or "unchecked",
                    row.get("verify") or "cmd",
                    row.get("spec") or "",
                    row.get("cwd") or "books",
                    row.get("files") or "",
                    row.get("title") or "",
                ]
            )
        )
    lines.append("```")
    return "\n".join(lines)


def next_slice(rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for row in rows:
        if row.get("status") != "checked":
            return row
    return None


def _blob(command: str, stdout: str, finding: str) -> str:
    return "\n".join([command or "", stdout or "", finding or ""])


def _verify_see_budget(command: str, stdout: str, stderr: str, finding: str) -> Dict[str, Any]:
    cmd = (command or "").strip()
    if cmd.upper() == "EXIT":
        return {"ok": False, "reason": "DOD-01 needs the budget, not EXIT."}
    text = stdout or ""
    if re.search(r"0\s*,\s*10000\b", text):
        return {"ok": True, "evidence": "Budget still shows spent $0, leftover $10,000"}
    if "command not found" in (stderr or "").lower():
        return {"ok": False, "reason": "Command not found."}
    return {"ok": False, "reason": "Output did not show leftover still $10,000 (spent $0, leftover $10,000)."}


def _verify_see_spent(command: str, stdout: str, stderr: str, finding: str) -> Dict[str, Any]:
    cmd = (command or "").strip()
    if cmd.upper() == "EXIT":
        return {"ok": False, "reason": "DOD-02 needs the receipt named before EXIT."}
    text = _blob(command, stdout, finding)
    has_amount = bool(re.search(r"10[, ]?000", text))
    has_paid = bool(re.search(r"\b(paid|rent|spent|receipt)\b", text, flags=re.I))
    if has_amount and has_paid:
        return {"ok": True, "evidence": "Receipt shows $10,000 spent"}
    return {"ok": False, "reason": "Name the $10,000 payment (paid / rent / spent)."}


_FIELD_ALIASES = {
    "item": "item",
    "budget": "budget",
    "spent": "spent",
    "left": "left",
    "leftover": "left",
    "remaining": "left",
}
_DEFAULT_FIELDS = ("item", "budget", "spent", "left")


def _cells(line: str) -> List[str]:
    cleaned = re.sub(r"\$(\d{1,3}(?:,\d{3})+|\d+)", lambda m: m.group(1).replace(",", ""), line)
    return [cell.strip() for cell in next(csv.reader([cleaned]))]


def _norm_key(name: str) -> str:
    return _FIELD_ALIASES.get(re.sub(r"[^a-z]", "", (name or "").lower()), "")


def _is_header(cells: List[str]) -> bool:
    return any(_norm_key(cell) in {"item", "budget", "spent", "left"} for cell in cells)


def _row_from_cells(cells: List[str], fields: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for index, raw in enumerate(fields):
        key = _norm_key(raw) or raw.lower()
        if index < len(cells):
            out[key] = cells[index]
    return out


def _parse_entry(path: Path) -> List[Dict[str, str]]:
    if not path.is_file():
        return []
    rows: List[Dict[str, str]] = []
    fields = list(_DEFAULT_FIELDS)
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        cells = _cells(line)
        if _is_header(cells):
            fields = cells
            continue
        rows.append(_row_from_cells(cells, fields))
    return rows


def _amount(value: str) -> int:
    digits = re.sub(r"[^\d]", "", value or "")
    return int(digits) if digits else 0


def _left_raw(row: Dict[str, str]) -> str:
    return row.get("left") or row.get("leftover") or ""


def _row_matches_cash(row: Dict[str, str]) -> bool:
    left_digits = re.sub(r"[^\d]", "", _left_raw(row))
    return _amount(row.get("spent") or "") == 10000 and left_digits == "0"


def _verify_write_left(
    command: str,
    stdout: str,
    stderr: str,
    finding: str,
    *,
    books: Path,
) -> Dict[str, Any]:
    path = books / "leftover.csv"
    rows = _parse_entry(path)
    if any(_row_matches_cash(row) for row in rows):
        return {"ok": True, "evidence": "Spent $10,000, leftover $0"}
    if (command or "").strip().upper() != "EXIT" and not path.is_file():
        return {"ok": False, "reason": "Write books/leftover.csv, then EXIT."}
    if not path.is_file():
        return {"ok": False, "reason": "books/leftover.csv is missing."}
    return {"ok": False, "reason": "leftover.csv must show spent $10,000 and leftover $0."}


_VERIFIERS = {
    "see-budget": _verify_see_budget,
    "see-spent": _verify_see_spent,
}


def verify_row(
    row: Dict[str, Any],
    command: str,
    stdout: str,
    stderr: str = "",
    finding: str = "",
    books: Optional[Path] = None,
) -> Dict[str, Any]:
    spec = str(row.get("spec") or "")
    if spec == "write-left":
        result = _verify_write_left(command, stdout, stderr, finding, books=books_dir(books))
    else:
        fn = _VERIFIERS.get(spec)
        if not fn:
            return {"ok": False, "reason": f"Unknown DoD spec: {row.get('spec')}"}
        result = fn(command, stdout, stderr, finding)
    result["id"] = row["id"]
    result["title"] = row.get("title")
    return result


def _finding_from_turn(turn: Dict[str, Any]) -> str:
    parsed = turn.get("parsed") if isinstance(turn.get("parsed"), dict) else {}
    return str(turn.get("finding") or parsed.get("finding") or "")


def apply_history(history: List[Dict[str, Any]], books: Optional[Path] = None) -> List[Dict[str, Any]]:
    rows = fresh_rows()
    for turn in history or []:
        current = next_slice(rows)
        if not current:
            break
        result = verify_row(
            current,
            str(turn.get("command") or ""),
            str(turn.get("stdout") or ""),
            str(turn.get("stderr") or ""),
            _finding_from_turn(turn),
            books=books,
        )
        if result.get("ok"):
            current["status"] = "checked"
            current["evidence"] = result.get("evidence") or ""
            current.pop("last_attempt", None)
        else:
            current["last_attempt"] = result.get("reason") or "Did not pass."
    return rows


def _serialize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    nxt = next_slice(rows)
    return {
        "rows": rows,
        "next": nxt,
        "complete": nxt is None,
        "markdown": format_registry(rows),
    }


def snapshot_from_history(history: List[Dict[str, Any]], books: Optional[Path] = None) -> Dict[str, Any]:
    return _serialize(apply_history(history, books=books))


def evaluate_print(
    history: List[Dict[str, Any]],
    command: str,
    stdout: str,
    stderr: str = "",
    finding: str = "",
    books: Optional[Path] = None,
) -> Dict[str, Any]:
    rows = apply_history(history, books=books)
    current = next_slice(rows)
    verification: Optional[Dict[str, Any]] = None
    if current:
        verification = verify_row(current, command, stdout, stderr, finding, books=books)
        if verification.get("ok"):
            current["status"] = "checked"
            current["evidence"] = verification.get("evidence") or ""
            current.pop("last_attempt", None)
        else:
            current["last_attempt"] = verification.get("reason") or "Did not pass."
    snap = _serialize(rows)
    snap["current"] = current
    snap["verification"] = verification
    return snap


def dod_prompt_block(history: List[Dict[str, Any]], books: Optional[Path] = None) -> str:
    snap = snapshot_from_history(history, books=books)
    nxt = snap.get("next")
    lines = [
        "DEFINITION OF DONE (machine-checkable — attack ONLY the next unchecked slice):",
        snap["markdown"],
    ]
    if nxt:
        lines.append(f"NEXT SLICE: {nxt['id']} — {nxt['title']}")
        lines.append(f"This loop must satisfy {nxt['id']}. Do not skip ahead.")
    else:
        lines.append("All DoD slices are checked. COMMAND: EXIT with FINDING if not already.")
    return "\n".join(lines)
