#!/usr/bin/env python3
"""Regression checks for selected optimizer target metrics."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OPTIMIZER_PATH = SCRIPT_DIR / "optimize_farm_upgrades.py"


def load_optimizer_module():
    spec = importlib.util.spec_from_file_location("optimize_farm_upgrades", OPTIMIZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load optimizer module from {OPTIMIZER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def default_args() -> SimpleNamespace:
    return SimpleNamespace(
        include_gold=False,
        damage_weight=None,
        prestige_weight=None,
        gold_weight=None,
    )


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def assert_true(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def make_upgrade(
    module: Any,
    key: str,
    metric: str,
    percent_per_level: str,
    *,
    base_cost: str = "100",
    resource: str = "energy",
    max_level: int = 1,
) -> Any:
    return module.Upgrade(
        key=key,
        resource=resource,
        metric=metric,
        percent_per_level=Decimal(percent_per_level),
        base_cost=Decimal(base_cost),
        mult_cost=Decimal("0"),
        max_level=max_level,
        override_formula_endgame=False,
        formula_class="research_test",
        formula_factor="test",
    )


def optimize_once(module: Any, upgrades: dict[str, Any], weights: dict[str, float], resources: dict[str, Decimal]):
    return module.optimize(
        upgrades=upgrades,
        levels={key: 0 for key in upgrades},
        resources=resources,
        weights=weights,
        max_steps=100,
        locked_upgrades=set(),
    )


def purchase_keys(purchases: list[Any]) -> list[str]:
    return sorted(item.upgrade_key for item in purchases)


def purchase_metrics(purchases: list[Any]) -> list[str]:
    return sorted(item.metric for item in purchases)


def test_default_objectives_build_expected_weights(module: Any) -> None:
    args = default_args()

    farm = module.build_weights({"objective": "FARM"}, args)
    assert_equal(farm, {"damage": 1.0, "kill_gold": 0.0, "prestige_power": 1.0}, "FARM weights")

    gold_prep = module.build_weights({"objective": "GOLD_PREP"}, args)
    assert_equal(gold_prep, {"damage": 0.0, "kill_gold": 1.0, "prestige_power": 0.0}, "GOLD_PREP weights")

    custom = module.build_weights(
        {"objective": "OPT_GOLD_PRESTIGE", "target_metrics": ["prestige", "gold"]},
        args,
    )
    assert_equal(custom, {"damage": 0.0, "kill_gold": 1.0, "prestige_power": 1.0}, "custom target weights")


def test_explicit_targets_ignore_legacy_farm_fields(module: Any) -> None:
    weights = module.build_weights(
        {
            "objective": "FARM",
            "target_metrics": ["gold"],
            "farm": {
                "include_gold": False,
                "damage_effective": True,
                "prestige_power_effective": True,
                "weights": {
                    "damage": 1.0,
                    "kill_gold": 0.0,
                    "prestige_power": 1.0,
                },
            },
        },
        default_args(),
    )
    assert_equal(weights, {"damage": 0.0, "kill_gold": 1.0, "prestige_power": 0.0}, "explicit target weights")


def test_target_weights_override_selected_target_strength(module: Any) -> None:
    weights = module.build_weights(
        {
            "objective": "OPT_DMG_GOLD",
            "target_metrics": ["damage", "gold"],
            "target_weights": {
                "damage": 2.0,
                "gold": 3.5,
                "prestige": 99.0,
            },
        },
        default_args(),
    )
    assert_equal(weights, {"damage": 2.0, "kill_gold": 3.5, "prestige_power": 0.0}, "target weight override")


def test_unknown_targets_warn_and_do_not_create_active_weight(module: Any) -> None:
    warnings: list[str] = []
    weights = module.build_weights(
        {"objective": "OPT_UNKNOWN", "target_metrics": ["unknown"]},
        default_args(),
        warnings,
    )
    assert_equal(weights, {"damage": 0.0, "kill_gold": 0.0, "prestige_power": 0.0}, "unknown target weights")
    assert_equal(warnings, ["ignored unknown target metric: unknown"], "unknown target warning")
    assert_equal(module.active_target_metrics(weights), [], "no active targets")


def test_single_target_ignores_better_roi_from_unselected_metric(module: Any) -> None:
    upgrades = {
        "dmg": make_upgrade(module, "dmg", "damage", "0.10"),
        "gold": make_upgrade(module, "gold", "kill_gold", "10.0"),
    }
    final_levels, remaining, purchases, diagnostics = optimize_once(
        module,
        upgrades,
        {"damage": 1.0, "kill_gold": 0.0, "prestige_power": 0.0},
        {"energy": Decimal("100"), "prestige_points": Decimal("0")},
    )

    assert_equal(purchase_keys(purchases), ["dmg"], "single target purchase key")
    assert_equal(final_levels["dmg"], 1, "selected metric final level")
    assert_equal(final_levels["gold"], 0, "unselected metric final level")
    assert_equal(remaining["energy"], Decimal("0"), "single target remaining energy")
    assert_equal(diagnostics["target_metrics"], ["damage"], "single target diagnostics")


def test_multi_target_excludes_unselected_metric_even_when_it_is_best(module: Any) -> None:
    upgrades = {
        "dmg": make_upgrade(module, "dmg", "damage", "100.0", base_cost="1"),
        "gold": make_upgrade(module, "gold", "kill_gold", "0.50"),
        "prestige": make_upgrade(module, "prestige", "prestige_power", "0.50"),
    }
    final_levels, remaining, purchases, diagnostics = optimize_once(
        module,
        upgrades,
        {"damage": 0.0, "kill_gold": 1.0, "prestige_power": 1.0},
        {"energy": Decimal("200"), "prestige_points": Decimal("0")},
    )

    assert_equal(purchase_metrics(purchases), ["kill_gold", "prestige_power"], "multi target purchase metrics")
    assert_equal(final_levels["dmg"], 0, "unselected high ROI metric stays unchanged")
    assert_equal(final_levels["gold"], 1, "selected gold level")
    assert_equal(final_levels["prestige"], 1, "selected prestige level")
    assert_equal(remaining["energy"], Decimal("0"), "multi target remaining energy")
    assert_equal(diagnostics["excluded_metrics"], ["damage"], "excluded metric diagnostics")


def test_greedy_prefers_larger_log_gain_per_cost_when_budget_fits_one(module: Any) -> None:
    upgrades = {
        "dmg": make_upgrade(module, "dmg", "damage", "1.0"),
        "gold": make_upgrade(module, "gold", "kill_gold", "0.10"),
    }
    final_levels, _remaining, purchases, _diagnostics = optimize_once(
        module,
        upgrades,
        {"damage": 1.0, "kill_gold": 1.0, "prestige_power": 0.0},
        {"energy": Decimal("100"), "prestige_points": Decimal("0")},
    )

    assert_equal(purchase_keys(purchases), ["dmg"], "higher log ROI purchase")
    assert_equal(final_levels["dmg"], 1, "higher log ROI level")
    assert_equal(final_levels["gold"], 0, "lower log ROI level")


def test_target_weight_can_change_the_greedy_choice(module: Any) -> None:
    upgrades = {
        "dmg": make_upgrade(module, "dmg", "damage", "1.0"),
        "gold": make_upgrade(module, "gold", "kill_gold", "0.10"),
    }
    weights = module.build_weights(
        {
            "objective": "OPT_DMG_GOLD",
            "target_metrics": ["damage", "gold"],
            "target_weights": {"gold": 10.0},
        },
        default_args(),
    )
    final_levels, _remaining, purchases, _diagnostics = optimize_once(
        module,
        upgrades,
        weights,
        {"energy": Decimal("100"), "prestige_points": Decimal("0")},
    )

    assert_equal(purchase_keys(purchases), ["gold"], "weighted target purchase")
    assert_equal(final_levels["dmg"], 0, "lower weighted target level")
    assert_equal(final_levels["gold"], 1, "higher weighted target level")


def test_resource_budgets_are_separate_for_selected_targets(module: Any) -> None:
    upgrades = {
        "gold_energy": make_upgrade(module, "gold_energy", "kill_gold", "1.0", resource="energy"),
        "gold_prestige": make_upgrade(module, "gold_prestige", "kill_gold", "1.0", resource="prestige_points"),
    }
    final_levels, remaining, purchases, _diagnostics = optimize_once(
        module,
        upgrades,
        {"damage": 0.0, "kill_gold": 1.0, "prestige_power": 0.0},
        {"energy": Decimal("100"), "prestige_points": Decimal("0")},
    )

    assert_equal(purchase_keys(purchases), ["gold_energy"], "separate resource purchase")
    assert_equal(final_levels["gold_energy"], 1, "energy-backed target level")
    assert_equal(final_levels["gold_prestige"], 0, "prestige-backed target level")
    assert_equal(remaining["energy"], Decimal("0"), "remaining energy")
    assert_equal(remaining["prestige_points"], Decimal("0"), "remaining prestige points")


def test_single_target_large_purchase_is_batched_efficiently(module: Any) -> None:
    upgrades = {
        "dmg": make_upgrade(module, "dmg", "damage", "0.01", base_cost="1", max_level=1000),
    }
    final_levels, remaining, purchases, diagnostics = module.optimize(
        upgrades=upgrades,
        levels={"dmg": 0},
        resources={"energy": Decimal("1000"), "prestige_points": Decimal("0")},
        weights={"damage": 1.0, "kill_gold": 0.0, "prestige_power": 0.0},
        max_steps=1,
        locked_upgrades=set(),
    )

    assert_equal(final_levels["dmg"], 1000, "batched final level")
    assert_equal(remaining["energy"], Decimal("0"), "batched remaining energy")
    assert_equal(len(purchases), 1, "batched purchase row count")
    assert_equal(purchases[0].levels_bought, 1000, "batched levels bought")
    assert_equal(diagnostics["iterations"], 1, "batched optimizer iterations")
    assert_equal(diagnostics["hit_step_limit"], False, "batched optimizer step limit")


def test_cli_rejects_state_without_active_target_metric() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        state_path = Path(tmp) / "state.json"
        output_path = Path(tmp) / "result.json"
        state_path.write_text(
            json.dumps(
                {
                    "objective": "OPT_UNKNOWN",
                    "target_metrics": ["unknown"],
                    "resources": {"energy": "100", "prestige_points": "0"},
                    "levels": {},
                }
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(OPTIMIZER_PATH),
                "--state",
                str(state_path),
                "--output",
                str(output_path),
            ],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    assert_equal(result.returncode, 1, "CLI invalid target exit code")
    assert_true("select at least one target metric" in result.stderr, "CLI invalid target error")


def main() -> int:
    module = load_optimizer_module()

    test_default_objectives_build_expected_weights(module)
    test_explicit_targets_ignore_legacy_farm_fields(module)
    test_target_weights_override_selected_target_strength(module)
    test_unknown_targets_warn_and_do_not_create_active_weight(module)
    test_single_target_ignores_better_roi_from_unselected_metric(module)
    test_multi_target_excludes_unselected_metric_even_when_it_is_best(module)
    test_greedy_prefers_larger_log_gain_per_cost_when_budget_fits_one(module)
    test_target_weight_can_change_the_greedy_choice(module)
    test_resource_budgets_are_separate_for_selected_targets(module)
    test_single_target_large_purchase_is_batched_efficiently(module)
    test_cli_rejects_state_without_active_target_metric()

    print("optimizer target metric regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
