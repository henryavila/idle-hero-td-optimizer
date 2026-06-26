#!/usr/bin/env python3
"""Regression checks for Streamlit UI state coercion."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui import app  # noqa: E402


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def assert_no_resource_errors(energy: str, prestige_points: str) -> None:
    errors = app.validate_resource_inputs(energy, prestige_points)
    if errors:
        raise AssertionError(f"resource inputs {energy!r}/{prestige_points!r} should be valid: {errors}")


def test_manual_locked_editor_is_available_before_ocr() -> None:
    original_session_state = app.st.session_state
    original_render_manual_locked_editor = app.render_manual_locked_editor
    captured: dict[str, object] = {}

    def fake_render_manual_locked_editor(rows: pd.DataFrame, **kwargs: object) -> pd.DataFrame:
        captured["called"] = True
        captured["row_count"] = len(rows)
        captured["show_state"] = kwargs.get("show_state")
        return rows

    app.st.session_state = {}
    app.render_manual_locked_editor = fake_render_manual_locked_editor
    try:
        result = app.show_editor()
    finally:
        app.st.session_state = original_session_state
        app.render_manual_locked_editor = original_render_manual_locked_editor

    assert_equal(result, None, "pre-OCR editor must not expose rows for macro generation")
    assert_equal(captured.get("called"), True, "manual locked editor before OCR")
    assert_equal(captured.get("row_count"), len(app.CORE_KEYS), "pre-OCR manual locked row count")
    assert_equal(captured.get("show_state"), False, "pre-OCR manual locked editor state columns")


def main() -> int:
    assert_equal(app.coerce_int(499028.0), 499028, "integer-valued editor float")
    assert_equal(app.coerce_int(1028.0), 1028, "small integer-valued editor float")
    assert_equal(app.coerce_int(999999.0), 999999, "max boundary editor float")
    assert_equal(app.coerce_int(0.0), 0, "zero editor float")
    assert_equal(app.coerce_int("499.028"), 499028, "dotted thousands level")
    assert_equal(app.coerce_int("499,028"), 499028, "comma thousands level")
    assert_equal(app.coerce_int(None), None, "none level")
    assert_equal(app.coerce_int(""), None, "blank level")
    assert_equal(app.coerce_int(float("nan")), None, "nan level")

    assert_no_resource_errors("20,258k", "0")
    assert_no_resource_errors("20.258k", "0")
    assert_no_resource_errors("0", "20,258k")
    assert_no_resource_errors("0", "20.258k")
    assert_equal(app.parse_game_number("20,258k"), app.parse_game_number("20.258k"), "decimal suffix separators")
    assert_equal(app.parse_game_number("20,258k"), app.parse_game_number("20258"), "decimal suffix value")

    rows = pd.DataFrame(
        [
            {"upgrade_key": "prestigeDmg2", "status": "available", "level": 499028.0},
            {"upgrade_key": "prestigeDmg3", "status": "available", "level": 16356.0},
            {"upgrade_key": "prestigeDmg4", "status": "available", "level": 1028.0},
            {"upgrade_key": "prestigeDmg5", "status": "locked", "level": 0.0},
        ]
    )
    state, errors = app.build_optimizer_state(
        rows=rows,
        objective="FARM",
        energy="20,258k",
        prestige_points="20.258k",
    )
    assert_equal(errors, [], "optimizer state errors")
    assert_equal(state["levels"]["prestigeDmg2"], 499028, "state prestigeDmg2 level")
    assert_equal(state["levels"]["prestigeDmg3"], 16356, "state prestigeDmg3 level")
    assert_equal(state["levels"]["prestigeDmg4"], 1028, "state prestigeDmg4 level")
    assert_equal(state["levels"]["prestigeDmg5"], 0, "state locked level")
    assert_equal(state["locked_upgrades"], ["prestigeDmg5"], "state locked upgrades")

    ocr_payload = [
        {
            "screen": "prestige-core",
            "records": [
                {
                    "upgrade_key": "prestigeDmg4",
                    "level": 1028,
                    "confidence": 100.0,
                    "text": "DAMACEIV(Lv.1028) 1.675+17 +51400% (+50%) WAVE 5000",
                },
                {
                    "upgrade_key": "prestigeDmg5",
                    "level": 0,
                    "confidence": 100.0,
                    "text": "DAMAGE V (Lv. O) WAVE 5000 +0%",
                },
            ],
        }
    ]
    rows = app.build_state_rows(ocr_payload)
    status_by_key = dict(zip(rows["upgrade_key"], rows["status"]))
    assert_equal(status_by_key["prestigeDmg4"], "available", "positive-level prestigeDmg4 contaminated by adjacent wave")
    assert_equal(status_by_key["prestigeDmg5"], "review", "zero-level wave should not become inferred locked")

    rows = app.build_state_rows(ocr_payload, manual_locked={"prestigeDmg5"})
    row_by_key = {str(row["upgrade_key"]): row for _, row in rows.iterrows()}
    assert_equal(row_by_key["prestigeDmg5"]["status"], "locked", "manual locked status")
    assert_equal(row_by_key["prestigeDmg5"]["level"], 0, "manual locked level")
    assert_equal(row_by_key["prestigeDmg5"]["inference"], "manual=locked", "manual locked inference")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "locked_upgrades.json"
        app.save_manual_locked({"prestigeDmg5", "unknownKey", "prestigeDmg4"}, path)
        assert_equal(
            app.load_manual_locked(path),
            {"prestigeDmg4", "prestigeDmg5"},
            "persisted manual locked keys",
        )

    test_manual_locked_editor_is_available_before_ocr()

    print("ui state conversion regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
