#!/usr/bin/env python3
"""Regression checks for Streamlit UI state coercion."""

from __future__ import annotations

import sys
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

    print("ui state conversion regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
