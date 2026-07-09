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


def rows_by_key(rows: pd.DataFrame) -> dict[str, pd.Series]:
    return {str(row["upgrade_key"]): row for _, row in rows.iterrows()}


class NullContext:
    def __enter__(self) -> "NullContext":
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> bool:
        return False


class FakeColumnConfig:
    def CheckboxColumn(self, *args: object, **kwargs: object) -> tuple[str, tuple[object, ...], dict[str, object]]:
        return ("CheckboxColumn", args, kwargs)

    def NumberColumn(self, *args: object, **kwargs: object) -> tuple[str, tuple[object, ...], dict[str, object]]:
        return ("NumberColumn", args, kwargs)

    def SelectboxColumn(self, *args: object, **kwargs: object) -> tuple[str, tuple[object, ...], dict[str, object]]:
        return ("SelectboxColumn", args, kwargs)

    def TextColumn(self, *args: object, **kwargs: object) -> tuple[str, tuple[object, ...], dict[str, object]]:
        return ("TextColumn", args, kwargs)


def minimal_research_ocr_payload() -> list[dict[str, object]]:
    return [
        {
            "screen": "research-core",
            "records": [
                {"upgrade_key": "researchDmg1", "level": 1217, "text": "DAMAGE I (Lv. 1217)"},
                {"upgrade_key": "researchKillGold1", "level": 447, "text": "KILL GOLD I (Lv. 447)"},
                {"upgrade_key": "researchPrestigePower1", "level": 768, "text": "PRESTIGE POWER I (Lv. 768)"},
            ],
        }
    ]


def test_advanced_editor_is_visible_before_ocr() -> None:
    original_session_state = app.st.session_state
    original_render_advanced_editor = app.render_advanced_editor
    original_load_saved_advanced_overrides = app.load_saved_advanced_overrides
    captured: dict[str, object] = {}

    def fake_render_advanced_editor(merged: pd.DataFrame, base_rows: pd.DataFrame) -> None:
        captured["called"] = True
        captured["row_count"] = len(merged)
        captured["base_row_count"] = len(base_rows)
        captured["researchDmg1_status"] = rows_by_key(merged)["researchDmg1"]["status"]
        captured["base_researchDmg1_status"] = rows_by_key(base_rows)["researchDmg1"]["status"]

    app.st.session_state = {}
    app.render_advanced_editor = fake_render_advanced_editor
    app.load_saved_advanced_overrides = lambda: {"researchDmg1": {"status": "maxed", "level": 1217}}
    try:
        result = app.show_editor()
    finally:
        app.st.session_state = original_session_state
        app.render_advanced_editor = original_render_advanced_editor
        app.load_saved_advanced_overrides = original_load_saved_advanced_overrides

    assert_equal(result, None, "pre-OCR editor must not expose rows for macro generation")
    assert_equal(captured.get("called"), True, "advanced editor before OCR")
    assert_equal(captured.get("row_count"), len(app.CORE_KEYS), "pre-OCR advanced editor row count")
    assert_equal(captured.get("base_row_count"), len(app.CORE_KEYS), "pre-OCR advanced editor base row count")
    assert_equal(captured.get("researchDmg1_status"), "maxed", "pre-OCR saved advanced override is visible")
    assert_equal(captured.get("base_researchDmg1_status"), "ignore", "pre-OCR base remains unprocessed")


def test_show_editor_after_ocr_rebuilds_base_and_applies_saved_overrides() -> None:
    original_session_state = app.st.session_state
    original_expander = app.st.expander
    original_render_state_summary = app.render_state_summary
    original_render_inference_summary = app.render_inference_summary
    original_render_advanced_editor = app.render_advanced_editor
    original_render_debug_rows = app.render_debug_rows
    original_load_saved_advanced_overrides = app.load_saved_advanced_overrides
    captured: dict[str, object] = {}

    def fake_render_advanced_editor(merged: pd.DataFrame, base_rows: pd.DataFrame) -> None:
        merged_by_key = rows_by_key(merged)
        base_by_key = rows_by_key(base_rows)
        captured["called"] = True
        captured["merged_researchDmg1_status"] = merged_by_key["researchDmg1"]["status"]
        captured["base_researchDmg1_status"] = base_by_key["researchDmg1"]["status"]
        captured["base_researchDmg1_level"] = base_by_key["researchDmg1"]["level"]

    app.st.session_state = {
        "state_rows": app.build_state_rows([]),
        "ocr_results": minimal_research_ocr_payload(),
    }
    app.st.expander = lambda *args, **kwargs: NullContext()
    app.render_state_summary = lambda rows: None
    app.render_inference_summary = lambda rows: None
    app.render_advanced_editor = fake_render_advanced_editor
    app.render_debug_rows = lambda rows: None
    app.load_saved_advanced_overrides = lambda: {"researchDmg1": {"status": "maxed", "level": None}}
    try:
        result = app.show_editor()
    finally:
        app.st.session_state = original_session_state
        app.st.expander = original_expander
        app.render_state_summary = original_render_state_summary
        app.render_inference_summary = original_render_inference_summary
        app.render_advanced_editor = original_render_advanced_editor
        app.render_debug_rows = original_render_debug_rows
        app.load_saved_advanced_overrides = original_load_saved_advanced_overrides

    if result is None:
        raise AssertionError("post-OCR editor should return rows for macro generation")
    result_by_key = rows_by_key(result)
    assert_equal(captured.get("called"), True, "advanced editor after OCR")
    assert_equal(captured.get("base_researchDmg1_status"), "available", "post-OCR base status comes from OCR")
    assert_equal(captured.get("base_researchDmg1_level"), 1217, "post-OCR base level comes from OCR")
    assert_equal(captured.get("merged_researchDmg1_status"), "maxed", "post-OCR saved override is visible")
    assert_equal(result_by_key["researchDmg1"]["status"], "maxed", "post-OCR result keeps saved override")
    assert_equal(result_by_key["researchDmg2"]["status"], "locked", "post-OCR inferred rows remain present")
    assert_equal(len(result), len(app.CORE_KEYS), "post-OCR editor returns complete optimizer row set")


def test_render_advanced_editor_saves_user_edits_and_invalidates_macro() -> None:
    original_session_state = app.st.session_state
    original_expander = app.st.expander
    original_tabs = app.st.tabs
    original_data_editor = app.st.data_editor
    original_column_config = app.st.column_config
    original_caption = app.st.caption
    original_load_saved_advanced_overrides = app.load_saved_advanced_overrides
    original_save_advanced_overrides = app.save_advanced_overrides
    saved: dict[str, object] = {}

    def fake_data_editor(frame: pd.DataFrame, **kwargs: object) -> pd.DataFrame:
        edited = frame.copy()
        if "researchDmg1" in set(edited["upgrade_key"].astype(str)):
            edited.loc[edited["upgrade_key"] == "researchDmg1", "status"] = "maxed"
            edited.loc[edited["upgrade_key"] == "researchDmg1", "level"] = None
        if "prestigeDmg5" in set(edited["upgrade_key"].astype(str)):
            edited.loc[edited["upgrade_key"] == "prestigeDmg5", "status"] = "locked"
            edited.loc[edited["upgrade_key"] == "prestigeDmg5", "level"] = None
        return edited

    base_rows = app.build_state_rows([])
    merged = base_rows.copy()
    fake_state = {"state_version": "test", "last_macro_text": "old macro", "last_result": {"ok": True}}
    app.st.session_state = fake_state
    app.st.expander = lambda *args, **kwargs: NullContext()
    app.st.tabs = lambda labels: [NullContext() for _ in labels]
    app.st.data_editor = fake_data_editor
    app.st.column_config = FakeColumnConfig()
    app.st.caption = lambda *args, **kwargs: None
    app.load_saved_advanced_overrides = lambda: {}
    app.save_advanced_overrides = lambda overrides: saved.update({"overrides": overrides})
    try:
        app.render_advanced_editor(merged, base_rows)
    finally:
        app.st.session_state = original_session_state
        app.st.expander = original_expander
        app.st.tabs = original_tabs
        app.st.data_editor = original_data_editor
        app.st.column_config = original_column_config
        app.st.caption = original_caption
        app.load_saved_advanced_overrides = original_load_saved_advanced_overrides
        app.save_advanced_overrides = original_save_advanced_overrides

    assert_equal(
        saved.get("overrides"),
        {
            "researchDmg1": {"status": "maxed", "level": None},
            "prestigeDmg5": {"status": "locked", "level": 0},
        },
        "advanced editor saves edited overrides from both tabs",
    )
    assert_equal(fake_state.get("last_macro_text"), None, "advanced edit invalidates macro text")
    assert_equal(fake_state.get("last_result"), None, "advanced edit invalidates optimizer result")
    edited_by_key = rows_by_key(merged)
    assert_equal(edited_by_key["researchDmg1"]["status"], "maxed", "advanced editor mutates merged status")
    assert_equal(edited_by_key["prestigeDmg5"]["status"], "locked", "advanced editor mutates prestige status")


def test_render_advanced_editor_can_clear_saved_override() -> None:
    original_session_state = app.st.session_state
    original_expander = app.st.expander
    original_tabs = app.st.tabs
    original_data_editor = app.st.data_editor
    original_column_config = app.st.column_config
    original_caption = app.st.caption
    original_load_saved_advanced_overrides = app.load_saved_advanced_overrides
    original_save_advanced_overrides = app.save_advanced_overrides
    saved: dict[str, object] = {}

    base_rows = app.build_state_rows(minimal_research_ocr_payload())
    merged = app.apply_advanced_overrides(
        base_rows,
        {"researchDmg1": {"status": "maxed", "level": None}},
    )

    def fake_data_editor(frame: pd.DataFrame, **kwargs: object) -> pd.DataFrame:
        edited = frame.copy()
        if "researchDmg1" in set(edited["upgrade_key"].astype(str)):
            edited.loc[edited["upgrade_key"] == "researchDmg1", "status"] = "available"
            edited.loc[edited["upgrade_key"] == "researchDmg1", "level"] = 1217
        return edited

    fake_state = {"state_version": "test", "last_macro_text": "old macro", "last_result": {"ok": True}}
    app.st.session_state = fake_state
    app.st.expander = lambda *args, **kwargs: NullContext()
    app.st.tabs = lambda labels: [NullContext() for _ in labels]
    app.st.data_editor = fake_data_editor
    app.st.column_config = FakeColumnConfig()
    app.st.caption = lambda *args, **kwargs: None
    app.load_saved_advanced_overrides = lambda: {"researchDmg1": {"status": "maxed", "level": None}}
    app.save_advanced_overrides = lambda overrides: saved.update({"overrides": overrides})
    try:
        app.render_advanced_editor(merged, base_rows)
    finally:
        app.st.session_state = original_session_state
        app.st.expander = original_expander
        app.st.tabs = original_tabs
        app.st.data_editor = original_data_editor
        app.st.column_config = original_column_config
        app.st.caption = original_caption
        app.load_saved_advanced_overrides = original_load_saved_advanced_overrides
        app.save_advanced_overrides = original_save_advanced_overrides

    assert_equal(saved.get("overrides"), {}, "advanced editor saves empty overrides when user returns to base")
    assert_equal(fake_state.get("last_macro_text"), None, "clearing override invalidates macro text")
    assert_equal(fake_state.get("last_result"), None, "clearing override invalidates optimizer result")


def test_screenshot_locked_inference_regression() -> None:
    ocr_payload = [
        {
            "screen": "research-core",
            "records": [
                {"upgrade_key": "researchDmg1", "level": 1217, "text": "DAMAGE I (Lv. 1217)"},
                {"upgrade_key": "researchDmg2", "level": 176, "text": "DAMAGE II (Lv. 176)"},
                {"upgrade_key": "researchDmg3", "level": 48, "text": "DAMAGE III (Lv. 48)"},
                {"upgrade_key": "researchDmg4", "level": 14, "text": "DAMAGE IV (Lv. 14)"},
                {"upgrade_key": "researchDmg5", "level": 10, "text": "DAMAGE V (Lv. 10)"},
                {"upgrade_key": "researchKillGold1", "level": 447, "text": "KILL GOLD I (Lv. 447)"},
                {"upgrade_key": "researchKillGold2", "level": 112, "text": "KILL GOLD II (Lv. 112)"},
                {"upgrade_key": "researchKillGold3", "level": 30, "text": "KILL GOLD III (Lv. 30)"},
                {"upgrade_key": "researchKillGold4", "level": 9, "text": "KILL GOLD IV (Lv. 9)"},
                {"upgrade_key": "researchKillGold5", "level": 3, "text": "KILL GOLD V (Lv. 3)"},
                {"upgrade_key": "researchPrestigePower1", "level": 768, "text": "PRESTIGE POWER I (Lv. 768)"},
                {"upgrade_key": "researchPrestigePower2", "level": 195, "text": "PRESTIGE POWER II (Lv. 195)"},
                {"upgrade_key": "researchPrestigePower3", "level": 38, "text": "PRESTIGE POWER III (Lv. 38)"},
                {"upgrade_key": "researchPrestigePower4", "level": 12, "text": "PRESTIGE POWER IV (Lv. 12)"},
            ],
        },
        {
            "screen": "prestige-core",
            "records": [
                {"upgrade_key": "prestigeDmg2", "level": 499028, "text": "DAMAGE II (Lv. 499.028)"},
                {"upgrade_key": "prestigeDmg3", "level": 16356, "text": "DAMAGE III (Lv. 16.356)"},
                {"upgrade_key": "prestigeDmg4", "level": 1037, "text": "DAMAGE IV (Lv. 1037)"},
                {"upgrade_key": "prestigeDmg5", "level": 0, "text": "DAMAGE V (Lv. 0) WAVE 5000 +0%"},
                {"upgrade_key": "prestigeKillGold2", "level": 338755, "text": "KILL GOLD II (Lv. 338.755)"},
                {"upgrade_key": "prestigeKillGold3", "level": 10941, "text": "KILL GOLD III (Lv. 10.941)"},
                {"upgrade_key": "prestigeKillGold4", "level": 641, "text": "KILL GOLD IV (Lv. 641)"},
                {"upgrade_key": "prestigeKillGold5", "level": 0, "text": "KILL GOLD V (Lv. 0) WAVE 5000 +0%"},
                {"upgrade_key": "prestigeKillGold6", "level": 0, "text": "KILL GOLD VI (Lv. O) WAVE 8000 +0%"},
            ],
        },
    ]
    rows = app.build_state_rows(ocr_payload)
    locked_keys = set(rows.loc[rows["status"] == "locked", "upgrade_key"].astype(str))
    expected_locked = {
        "researchDmg6",
        "researchKillGold6",
        "researchPrestigePower5",
        "prestigeDmg5",
        "prestigeDmg6",
        "prestigeDmg7",
        "prestigeKillGold5",
        "prestigeKillGold6",
        "prestigeKillGold7",
    }
    assert_equal(locked_keys, expected_locked, "reported screenshot locked keys")
    assert_equal(
        rows.loc[rows["status"] == "review", "upgrade_key"].astype(str).tolist(),
        [],
        "reported screenshot pending reviews",
    )


def test_locked_inference_boundaries() -> None:
    ocr_payload = [
        {
            "screen": "prestige-core",
            "records": [
                {"upgrade_key": "prestigeDmg2", "level": 499028, "text": "DAMAGE II (Lv. 499.028)"},
                {"upgrade_key": "prestigeDmg3", "level": 16356, "text": "DAMAGE III (Lv. 16.356)"},
                {
                    "upgrade_key": "prestigeDmg4",
                    "level": 1028,
                    "text": "DAMAGE IV (Lv. 1028) +51400% (+50%) WAVE 5000",
                },
                {"upgrade_key": "prestigeDmg5", "level": 0, "text": "DAMAGE V (Lv. 0) WAVE 5000 +0%"},
            ],
        }
    ]
    rows = app.build_state_rows(ocr_payload)
    by_key = rows_by_key(rows)

    assert_equal(by_key["prestigeDmg1"]["status"], "maxed", "missing before contiguous visible tiers")
    assert_equal(
        by_key["prestigeDmg1"]["inference"],
        "missing=maxed:before-contiguous-visible-run",
        "missing before visible tiers inference",
    )
    assert_equal(by_key["prestigeDmg4"]["status"], "available", "positive level with adjacent Wave text")
    assert_equal(by_key["prestigeDmg5"]["status"], "locked", "visible zero-level Wave lock")
    assert_equal(by_key["prestigeDmg5"]["inference"], "ocr", "visible zero-level Wave lock inference")
    assert_equal(by_key["prestigeDmg6"]["status"], "locked", "missing after visible locked tier")
    assert_equal(
        by_key["prestigeDmg6"]["inference"],
        "missing=locked:after-visible-lock",
        "missing after visible locked tier inference",
    )
    assert_equal(by_key["prestigeDmg7"]["status"], "locked", "second missing after visible locked tier")


def test_missing_tier_review_boundaries() -> None:
    ocr_payload = [
        {
            "screen": "research-core",
            "records": [
                {"upgrade_key": "researchDmg2", "level": 176, "text": "DAMAGE II (Lv. 176)"},
                {"upgrade_key": "researchDmg4", "level": 14, "text": "DAMAGE IV (Lv. 14)"},
            ],
        }
    ]
    rows = app.build_state_rows(ocr_payload)
    by_key = rows_by_key(rows)

    assert_equal(by_key["researchDmg1"]["status"], "review", "missing before non-contiguous visible tiers")
    assert_equal(
        by_key["researchDmg1"]["inference"],
        "missing=review:non-contiguous-visible-run",
        "missing before non-contiguous visible tiers inference",
    )
    assert_equal(by_key["researchDmg3"]["status"], "review", "gap between visible tiers")
    assert_equal(by_key["researchDmg3"]["inference"], "missing=review:ambiguous", "gap inference")
    assert_equal(by_key["researchDmg5"]["status"], "locked", "missing beyond highest visible tier")
    assert_equal(
        by_key["researchDmg5"]["inference"],
        "missing=locked:beyond-visible-tiers",
        "missing beyond highest visible tier inference",
    )
    assert_equal(by_key["researchDmg6"]["status"], "locked", "second missing beyond highest visible tier")


def test_empty_consensus_placeholder_uses_missing_inference() -> None:
    ocr_payload = [
        {
            "screen": "prestige-core",
            "records": [
                {"upgrade_key": "prestigeDmg1", "level": None, "confidence": None, "text": "", "rect": None, "source": None},
                {"upgrade_key": "prestigeDmg2", "level": 619726, "text": "DAMAGE II (Lv. 619,726)"},
                {"upgrade_key": "prestigeDmg3", "level": 28429, "text": "DAMAGE III (Lv. 28,429)"},
                {"upgrade_key": "prestigeDmg4", "level": 1975, "text": "DAMAGE IV (Lv. 1,975)"},
                {"upgrade_key": "prestigeDmg5", "level": 0, "text": "DAMAGE V (Lv. 0) +0% (+14,400%)"},
                {"upgrade_key": "prestigeKillGold2", "level": 342153, "text": "KILL GOLD II (Lv. 342,153)"},
                {"upgrade_key": "prestigeKillGold3", "level": 11141, "text": "KILL GOLD III (Lv. 11,141)"},
                {"upgrade_key": "prestigeKillGold4", "level": 701, "text": "KILL GOLD IV (Lv. 701)"},
                {"upgrade_key": "prestigeKillGold5", "level": 0, "text": "KILL GOLD V (Lv. 0) +0% (+14,400%)"},
            ],
        }
    ]
    rows = app.build_state_rows(ocr_payload)
    by_key = rows_by_key(rows)

    assert_equal(by_key["prestigeDmg1"]["detected"], False, "empty OCR placeholder is not a detected row")
    assert_equal(by_key["prestigeDmg1"]["status"], "maxed", "empty placeholder before visible run")
    assert_equal(
        by_key["prestigeDmg1"]["inference"],
        "missing=maxed:before-contiguous-visible-run",
        "empty placeholder before visible run inference",
    )
    assert_equal(by_key["prestigeDmg2"]["status"], "available", "visible anchor remains available")


def test_empty_consensus_placeholder_without_anchor_stays_review() -> None:
    ocr_payload = [
        {
            "screen": "prestige-core",
            "records": [
                {"upgrade_key": "prestigeDmg1", "level": None, "confidence": None, "text": "", "rect": None, "source": None},
            ],
        }
    ]
    rows = app.build_state_rows(ocr_payload)
    by_key = rows_by_key(rows)

    assert_equal(by_key["prestigeDmg1"]["detected"], False, "empty OCR placeholder without anchor is missing")
    assert_equal(by_key["prestigeDmg1"]["status"], "review", "missing placeholder without family anchor")
    assert_equal(
        by_key["prestigeDmg1"]["inference"],
        "missing=review:no-family-anchor",
        "missing placeholder without family anchor inference",
    )


def test_visible_ocr_record_without_level_stays_review() -> None:
    ocr_payload = [
        {
            "screen": "prestige-core",
            "records": [
                {
                    "upgrade_key": "prestigeDmg1",
                    "level": None,
                    "confidence": 88.0,
                    "text": "DAMAGE I (Lv. ?) +0%",
                    "rect": [10, 20, 300, 50],
                    "source": "level_text",
                },
            ],
        }
    ]
    rows = app.build_state_rows(ocr_payload)
    by_key = rows_by_key(rows)

    assert_equal(by_key["prestigeDmg1"]["detected"], True, "real OCR text without level remains detected")
    assert_equal(by_key["prestigeDmg1"]["status"], "review", "visible OCR text without level")
    assert_equal(by_key["prestigeDmg1"]["inference"], "ocr", "visible OCR text without level inference")


def test_manual_locked_does_not_override_maxed_row() -> None:
    ocr_payload = [
        {
            "screen": "prestige-core",
            "records": [
                {"upgrade_key": "prestigeDmg2", "level": 619726, "text": "DAMAGE II (Lv. 619,726)"},
                {"upgrade_key": "prestigeDmg3", "level": 28429, "text": "DAMAGE III (Lv. 28,429)"},
                {"upgrade_key": "prestigeDmg4", "level": 1975, "text": "DAMAGE IV (Lv. 1,975)"},
                {"upgrade_key": "prestigeDmg5", "level": 0, "text": "DAMAGE V (Lv. 0) +0% (+14,400%)"},
                {"upgrade_key": "prestigeKillGold2", "level": 342153, "text": "KILL GOLD II (Lv. 342,153)"},
                {"upgrade_key": "prestigeKillGold3", "level": 11141, "text": "KILL GOLD III (Lv. 11,141)"},
                {"upgrade_key": "prestigeKillGold4", "level": 701, "text": "KILL GOLD IV (Lv. 701)"},
                {"upgrade_key": "prestigeKillGold5", "level": 0, "text": "KILL GOLD V (Lv. 0) +0% (+14,400%)"},
            ],
        }
    ]
    rows = app.build_state_rows(ocr_payload, manual_locked={"prestigeDmg1"})
    by_key = rows_by_key(rows)

    assert_equal(by_key["prestigeDmg1"]["status"], "maxed", "manual lock does not override maxed status")
    assert_equal(bool(by_key["prestigeDmg1"]["manual_locked"]), False, "manual lock is not applied to maxed row")
    state, errors = app.build_optimizer_state(rows, objective="FARM", energy="20,258k", prestige_points="20.258k")
    assert_equal(errors, [], "optimizer state errors for stale manual lock on maxed row")
    assert_equal(state["levels"]["prestigeDmg1"], app.load_max_levels()["prestigeDmg1"], "maxed level survives stale lock")
    assert_equal("prestigeDmg1" in state["locked_upgrades"], False, "maxed row is not emitted as locked")


def test_manual_locked_overrides_available_row() -> None:
    ocr_payload = [
        {
            "screen": "research-core",
            "records": [
                {"upgrade_key": "researchKillGold1", "level": 447, "text": "KILL GOLD I (Lv. 447)"},
            ],
        }
    ]
    rows = app.build_state_rows(ocr_payload, manual_locked={"researchKillGold1"})
    by_key = rows_by_key(rows)

    assert_equal(by_key["researchKillGold1"]["ocr_level"], 447, "manual lock preserves original OCR level")
    assert_equal(by_key["researchKillGold1"]["ocr_status"], "available", "manual lock preserves original OCR status")
    assert_equal(by_key["researchKillGold1"]["status"], "locked", "manual lock overrides available status")
    assert_equal(by_key["researchKillGold1"]["level"], 0, "manual lock emits locked level")
    assert_equal(by_key["researchKillGold1"]["inference"], "manual=locked", "manual lock inference")


def test_optimizer_target_selection_state() -> None:
    assert_equal(
        app.objective_for_target_metrics(["damage", "prestige_power"]),
        "FARM",
        "farm target preset objective",
    )
    assert_equal(app.objective_for_target_metrics(["kill_gold"]), "GOLD_PREP", "gold target preset objective")
    assert_equal(
        app.objective_for_target_metrics(["prestige_power"]),
        "OPT_PRESTIGE",
        "prestige-only objective",
    )
    assert_equal(
        app.objective_for_target_metrics(["damage", "kill_gold", "prestige_power"]),
        "OPT_DMG_GOLD_PRESTIGE",
        "all-target objective",
    )
    assert_equal(app.validate_target_metrics([]), ["Selecione pelo menos um upgrade alvo: DMG, Gold ou Prestige."], "empty targets")

    rows = pd.DataFrame(
        [
            {"upgrade_key": "researchDmg1", "status": "available", "level": 10},
            {"upgrade_key": "researchKillGold1", "status": "available", "level": 20},
            {"upgrade_key": "researchPrestigePower1", "status": "available", "level": 30},
        ]
    )
    state, errors = app.build_optimizer_state(
        rows=rows,
        objective="OPT_GOLD_PRESTIGE",
        target_metrics=["kill_gold", "prestige_power"],
        energy="1M",
        prestige_points="0",
    )
    assert_equal(errors, [], "target optimizer state errors")
    assert_equal(state["target_metrics"], ["kill_gold", "prestige_power"], "state target metrics")
    assert_equal(state["objective"], "OPT_GOLD_PRESTIGE", "state target objective")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "target_metrics.json"
        assert_equal(
            app.load_saved_target_metrics(path),
            app.DEFAULT_TARGET_METRICS,
            "missing target metric state falls back to defaults",
        )
        app.save_target_metrics(["prestige_power", "unknown", "damage"], path)
        assert_equal(
            app.load_saved_target_metrics(path),
            ["damage", "prestige_power"],
            "persisted target metrics are normalized",
        )
        path.write_text('{"target_metrics": []}\n', encoding="utf-8")
        assert_equal(
            app.load_saved_target_metrics(path),
            app.DEFAULT_TARGET_METRICS,
            "empty target metric state falls back to defaults",
        )


def test_advanced_overrides_persist_and_reapply_maxed_status() -> None:
    ocr_payload = [
        {
            "screen": "research-core",
            "records": [
                {"upgrade_key": "researchDmg1", "level": 1217, "text": "DAMAGE I (Lv. 1217)"},
            ],
        }
    ]
    base_rows = app.build_state_rows(ocr_payload)
    edited_rows = base_rows.copy()
    edited_rows.loc[edited_rows["upgrade_key"] == "researchDmg1", "status"] = "maxed"

    overrides = app.collect_advanced_overrides(base_rows, edited_rows)
    assert_equal(
        overrides,
        {"researchDmg1": {"status": "maxed", "level": 1217}},
        "advanced maxed override payload",
    )

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "advanced_overrides.json"
        app.save_advanced_overrides(overrides, path)
        loaded = app.load_advanced_overrides(path)

    reloaded_rows = app.apply_advanced_overrides(app.build_state_rows(ocr_payload), loaded)
    reloaded_by_key = rows_by_key(reloaded_rows)
    assert_equal(reloaded_by_key["researchDmg1"]["status"], "maxed", "persisted advanced maxed status")
    assert_equal(bool(reloaded_by_key["researchDmg1"]["advanced_override"]), True, "advanced override marker")

    maxed_row = reloaded_rows[reloaded_rows["upgrade_key"] == "researchDmg1"]
    state, errors = app.build_optimizer_state(
        maxed_row,
        objective="FARM",
        energy="1M",
        prestige_points="0",
    )
    assert_equal(errors, [], "optimizer state errors with persisted advanced maxed override")
    assert_equal(
        state["levels"]["researchDmg1"],
        app.load_max_levels()["researchDmg1"],
        "persisted advanced maxed emits max level",
    )


def test_advanced_overrides_drive_optimizer_state_for_all_statuses() -> None:
    ocr_payload = [
        {
            "screen": "research-core",
            "records": [
                {"upgrade_key": "researchDmg1", "level": 1217, "text": "DAMAGE I (Lv. 1217)"},
                {"upgrade_key": "researchDmg2", "level": 176, "text": "DAMAGE II (Lv. 176)"},
                {"upgrade_key": "researchDmg3", "level": 48, "text": "DAMAGE III (Lv. 48)"},
                {"upgrade_key": "researchDmg4", "level": 14, "text": "DAMAGE IV (Lv. 14)"},
            ],
        }
    ]
    rows = app.apply_advanced_overrides(
        app.build_state_rows(ocr_payload),
        {
            "researchDmg1": {"status": "maxed", "level": None},
            "researchDmg2": {"status": "locked", "level": None},
            "researchDmg3": {"status": "ignore", "level": 48},
            "researchDmg4": {"status": "available", "level": "14"},
        },
    )
    selected_rows = rows[rows["upgrade_key"].isin(["researchDmg1", "researchDmg2", "researchDmg3", "researchDmg4"])]
    state, errors = app.build_optimizer_state(
        selected_rows,
        objective="FARM",
        energy="1M",
        prestige_points="0",
    )

    assert_equal(errors, [], "optimizer state errors with mixed advanced overrides")
    assert_equal(state["levels"]["researchDmg1"], app.load_max_levels()["researchDmg1"], "advanced maxed emits max level")
    assert_equal(state["levels"]["researchDmg2"], 0, "advanced locked emits zero level")
    assert_equal(state["locked_upgrades"], ["researchDmg2"], "advanced locked is emitted as locked")
    assert_equal("researchDmg3" in state["levels"], False, "advanced ignore is omitted from optimizer levels")
    assert_equal(state["levels"]["researchDmg4"], 14, "advanced available emits edited level")


def test_advanced_override_normalization_rejects_unknown_keys_and_statuses() -> None:
    payload = {
        "overrides": {
            "researchDmg1": {"status": "maxed", "level": None},
            "researchDmg2": {"status": "locked", "level": None},
            "researchDmg3": {"status": "available", "level": "1.217"},
            "unknownKey": {"status": "maxed", "level": None},
            "researchDmg4": {"status": "unknown", "level": 14},
        }
    }
    assert_equal(
        app.normalize_advanced_overrides(payload),
        {
            "researchDmg1": {"status": "maxed", "level": None},
            "researchDmg2": {"status": "locked", "level": 0},
            "researchDmg3": {"status": "available", "level": 1217},
        },
        "advanced override normalization",
    )


def test_advanced_overrides_ignore_unchanged_rows() -> None:
    rows = pd.DataFrame(
        [
            {"upgrade_key": "prestigeDmg1", "status": "available", "level": 10},
            {"upgrade_key": "prestigeDmg2", "status": "locked", "level": 0},
        ]
    )
    assert_equal(app.collect_advanced_overrides(rows, rows.copy()), {}, "unchanged advanced rows are not persisted")


def test_advanced_overrides_fall_back_to_legacy_manual_locks_until_saved() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        advanced_path = Path(tmp) / "advanced_overrides.json"
        legacy_path = Path(tmp) / "locked_upgrades.json"
        app.save_manual_locked({"prestigeDmg5", "unknownKey"}, legacy_path)

        assert_equal(
            app.load_saved_advanced_overrides(advanced_path, legacy_path),
            {"prestigeDmg5": {"status": "locked", "level": 0}},
            "legacy manual locks become advanced overrides when advanced file is missing",
        )

        app.save_advanced_overrides({}, advanced_path)
        assert_equal(
            app.load_saved_advanced_overrides(advanced_path, legacy_path),
            {},
            "saved advanced file takes precedence over legacy manual locks",
        )


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
    assert_equal(status_by_key["prestigeDmg5"], "locked", "zero-level wave should become locked")

    rows = app.build_state_rows(ocr_payload, manual_locked={"prestigeDmg5"})
    row_by_key = {str(row["upgrade_key"]): row for _, row in rows.iterrows()}
    assert_equal(row_by_key["prestigeDmg5"]["status"], "locked", "manual locked status")
    assert_equal(row_by_key["prestigeDmg5"]["level"], 0, "manual locked level")
    assert_equal(row_by_key["prestigeDmg5"]["inference"], "manual=locked", "manual locked inference")
    assert_equal(row_by_key["prestigeDmg1"]["status"], "maxed", "missing before visible run remains maxed")
    assert_equal(row_by_key["prestigeDmg6"]["status"], "locked", "missing beyond visible lock")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "locked_upgrades.json"
        app.save_manual_locked({"prestigeDmg5", "unknownKey", "prestigeDmg4"}, path)
        assert_equal(
            app.load_manual_locked(path),
            {"prestigeDmg4", "prestigeDmg5"},
            "persisted manual locked keys",
        )

    test_advanced_editor_is_visible_before_ocr()
    test_screenshot_locked_inference_regression()
    test_locked_inference_boundaries()
    test_missing_tier_review_boundaries()
    test_empty_consensus_placeholder_uses_missing_inference()
    test_empty_consensus_placeholder_without_anchor_stays_review()
    test_visible_ocr_record_without_level_stays_review()
    test_manual_locked_does_not_override_maxed_row()
    test_manual_locked_overrides_available_row()
    test_optimizer_target_selection_state()
    test_advanced_overrides_persist_and_reapply_maxed_status()
    test_advanced_overrides_drive_optimizer_state_for_all_statuses()
    test_advanced_override_normalization_rejects_unknown_keys_and_statuses()
    test_advanced_overrides_ignore_unchanged_rows()
    test_advanced_overrides_fall_back_to_legacy_manual_locks_until_saved()
    test_show_editor_after_ocr_rebuilds_base_and_applies_saved_overrides()
    test_render_advanced_editor_saves_user_edits_and_invalidates_macro()
    test_render_advanced_editor_can_clear_saved_override()

    print("ui state conversion regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
