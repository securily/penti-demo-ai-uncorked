"""Canned Print-output tests for Harbor Books budget DoD verifiers."""

from __future__ import annotations

from pathlib import Path

from dod import evaluate_print, fresh_rows, snapshot_from_history, verify_row

BUDGET_STDOUT = """item,budget,spent,left
Rent,10000,0,10000
"""

RECEIPT_STDOUT = """Paid rent $10,000.
"""

LEFTOVER_CSV = """item,budget,spent,left
Rent,10000,10000,0
"""


def _row(spec: str):
    return next(r for r in fresh_rows() if r["spec"] == spec)


def test_see_budget_passes_on_spent_zero_left_10000():
    result = verify_row(_row("see-budget"), "cat books/budget.csv", BUDGET_STDOUT)
    assert result["ok"] is True
    assert "$10,000" in result["evidence"]
    assert "$0" in result["evidence"]


def test_see_budget_rejects_exit():
    result = verify_row(_row("see-budget"), "EXIT", "", finding="leftover is 10000")
    assert result["ok"] is False


def test_see_budget_rejects_empty():
    result = verify_row(_row("see-budget"), "cat books/budget.csv", "")
    assert result["ok"] is False


def test_see_spent_passes_paid_amount():
    result = verify_row(
        _row("see-spent"),
        "cat books/receipt.txt",
        RECEIPT_STDOUT,
        finding="Paid rent $10,000",
    )
    assert result["ok"] is True


def test_see_spent_passes_spent_word():
    result = verify_row(_row("see-spent"), "cat books/receipt.txt", "Spent 10000 on rent.")
    assert result["ok"] is True


def test_see_spent_rejects_exit():
    result = verify_row(_row("see-spent"), "EXIT", "", finding="Paid rent 10000")
    assert result["ok"] is False


def test_see_spent_rejects_without_amount():
    result = verify_row(_row("see-spent"), "echo hi", "Paid rent")
    assert result["ok"] is False


def test_write_left_passes_on_exit_and_file(tmp_path: Path):
    (tmp_path / "leftover.csv").write_text(LEFTOVER_CSV, encoding="utf-8")
    result = verify_row(
        _row("write-left"),
        "EXIT",
        "",
        finding="Spent 10000, leftover 0",
        books=tmp_path,
    )
    assert result["ok"] is True


def test_write_left_passes_on_write_when_file_exists(tmp_path: Path):
    (tmp_path / "leftover.csv").write_text(LEFTOVER_CSV, encoding="utf-8")
    result = verify_row(_row("write-left"), "cat books/leftover.csv", LEFTOVER_CSV, books=tmp_path)
    assert result["ok"] is True


def test_write_left_rejects_missing_file(tmp_path: Path):
    result = verify_row(_row("write-left"), "EXIT", "", books=tmp_path)
    assert result["ok"] is False


def test_write_left_passes_headerless_rent_line(tmp_path: Path):
    (tmp_path / "leftover.csv").write_text("Rent,10000,10000,0\n", encoding="utf-8")
    result = verify_row(_row("write-left"), "EXIT", "", books=tmp_path)
    assert result["ok"] is True
    assert "$10,000" in result["evidence"]
    assert "$0" in result["evidence"]


def test_write_left_passes_leftover_column_name(tmp_path: Path):
    (tmp_path / "leftover.csv").write_text(
        "item,budget,spent,leftover\nRent,10000,10000,0\n",
        encoding="utf-8",
    )
    result = verify_row(_row("write-left"), "EXIT", "", books=tmp_path)
    assert result["ok"] is True


def test_write_left_passes_dollar_formatted_amounts(tmp_path: Path):
    (tmp_path / "leftover.csv").write_text(
        "item,budget,spent,left\nRent,$10,000,$10,000,$0\n",
        encoding="utf-8",
    )
    result = verify_row(_row("write-left"), "EXIT", "", books=tmp_path)
    assert result["ok"] is True


def test_write_left_rejects_wrong_amounts(tmp_path: Path):
    (tmp_path / "leftover.csv").write_text(
        "item,budget,spent,left\nRent,10000,1,9999\n",
        encoding="utf-8",
    )
    result = verify_row(_row("write-left"), "EXIT", "", books=tmp_path)
    assert result["ok"] is False


def test_evaluate_print_advances_slices(tmp_path: Path):
    (tmp_path / "leftover.csv").write_text(LEFTOVER_CSV, encoding="utf-8")
    first = evaluate_print([], "cat books/budget.csv", BUDGET_STDOUT, books=tmp_path)
    assert first["verification"]["ok"] is True
    assert first["rows"][0]["status"] == "checked"
    assert first["next"]["id"] == "DOD-02"

    history = [{"command": "cat books/budget.csv", "stdout": BUDGET_STDOUT}]
    second = evaluate_print(history, "cat books/receipt.txt", RECEIPT_STDOUT, books=tmp_path)
    assert second["verification"]["ok"] is True
    assert second["next"]["id"] == "DOD-03"

    history.append({"command": "cat books/receipt.txt", "stdout": RECEIPT_STDOUT})
    third = evaluate_print(
        history,
        "EXIT",
        "",
        finding="Leftover is $0",
        books=tmp_path,
    )
    assert third["verification"]["ok"] is True
    assert third["complete"] is True


def test_snapshot_starts_at_see_budget():
    snap = snapshot_from_history([])
    assert snap["next"]["spec"] == "see-budget"
    assert snap["complete"] is False
