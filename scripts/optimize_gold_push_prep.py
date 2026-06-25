#!/usr/bin/env python3
"""Optimize Kill Gold-only permanent upgrades for PUSH preparation.

This script spends Energy and Prestige Points only on Kill Gold upgrades. It is
useful when the next strategic step is preparing a push where extra run gold is
expected to become useful hero levels.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Any

from optimize_farm_upgrades import (
    METRIC_LABELS,
    format_decimal,
    load_state,
    load_upgrades,
    metric_factor,
    metric_factor_delta,
    optimize,
    parse_levels,
    parse_locked_upgrades,
    parse_resources,
    write_result,
)


GOLD_ONLY_WEIGHTS = {
    "damage": 0.0,
    "prestige_power": 0.0,
    "kill_gold": 1.0,
}
SUPPORTED_OBJECTIVES = {"GOLD_PREP", "PUSH_GOLD", "KILL_GOLD"}


def template(upgrades: dict[str, Any]) -> dict[str, Any]:
    return {
        "objective": "GOLD_PREP",
        "resources": {
            "energy": "0",
            "prestige_points": "0",
        },
        "levels": {key: 0 for key in sorted(upgrades)},
        "gold_prep": {
            "reason": "Prepare for a PUSH where extra Kill Gold becomes useful hero levels during the run.",
            "weights": {
                "damage": 0.0,
                "prestige_power": 0.0,
                "kill_gold": 1.0,
            },
        },
    }


def gold_only_result_document(
    upgrades: dict[str, Any],
    state: dict[str, Any],
    initial_levels: dict[str, int],
    final_levels: dict[str, int],
    resources: dict[str, Any],
    remaining: dict[str, Any],
    purchases: list[Any],
    weights: dict[str, float],
    warnings: list[str],
    diagnostics: dict[str, Any],
) -> dict[str, Any]:
    objective = str(state.get("objective", "GOLD_PREP")).upper()
    factors = {}
    for metric in METRIC_LABELS:
        factors[metric] = {
            "label": METRIC_LABELS[metric],
            "initial_factor": format_decimal(metric_factor(upgrades, initial_levels, metric)),
            "final_factor": format_decimal(metric_factor(upgrades, final_levels, metric)),
            "delta_multiplier": format_decimal(metric_factor_delta(upgrades, initial_levels, final_levels, metric)),
            "weight": weights.get(metric, 0.0),
        }

    resource_summary = {}
    for resource, start_value in resources.items():
        resource_summary[resource] = {
            "initial": format_decimal(start_value),
            "spent": format_decimal(start_value - remaining.get(resource, 0)),
            "remaining": format_decimal(remaining.get(resource, 0)),
        }

    return {
        "objective": objective,
        "method": "gold_only_marginal_log_roi_greedy_with_variable_cost_batching",
        "assumptions": [
            "Uses APK-derived factor and cost CSVs, not rounded UI values.",
            "Energy and Prestige Points are separate budgets.",
            "Only Kill Gold upgrades are candidates: Research Kill Gold and Prestige Kill Gold.",
            "Upgrades listed in locked_upgrades/unavailable_upgrades are excluded from candidate purchases.",
            "Damage and Prestige Power have weight 0 in this optimization.",
            "Use this for PUSH preparation only when extra gold is expected to become useful hero levels during the run.",
        ],
        "warnings": warnings,
        "diagnostics": diagnostics,
        "weights": weights,
        "resources": resource_summary,
        "factors": factors,
        "purchases": [
            {
                "upgrade_key": item.upgrade_key,
                "resource": item.resource,
                "metric": item.metric,
                "metric_label": METRIC_LABELS.get(item.metric, item.metric),
                "from_level": item.from_level,
                "to_level": item.to_level,
                "levels_bought": item.levels_bought,
                "spent": format_decimal(item.spent),
                "log_gain": item.log_gain,
                "delta_multiplier": math.exp(item.log_gain) if item.log_gain < 700 else "overflow",
            }
            for item in purchases
        ],
        "final_levels": {key: final_levels[key] for key in sorted(final_levels)},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Optimize Idle Hero TD permanent upgrades for Kill Gold-only PUSH preparation."
    )
    parser.add_argument("--state", help="Input JSON state file. Use '-' to read stdin.")
    parser.add_argument("--output", help="Optional JSON output path.")
    parser.add_argument("--print-template", action="store_true", help="Print a complete input template.")
    parser.add_argument("--gold-weight", type=float, default=1.0, help="Weight for Kill Gold. Must be positive.")
    parser.add_argument("--max-steps", type=int, default=200000, help="Safety cap for non-batched optimizer iterations.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.gold_weight <= 0:
        raise SystemExit("--gold-weight must be positive for the gold-only optimizer")

    upgrades = load_upgrades()
    if args.print_template:
        print(json.dumps(template(upgrades), indent=2, ensure_ascii=False))
        return 0

    state = load_state(args.state)
    objective = str(state.get("objective", "GOLD_PREP")).upper()
    if objective not in SUPPORTED_OBJECTIVES:
        supported = ", ".join(sorted(SUPPORTED_OBJECTIVES))
        raise SystemExit(f"unsupported objective {objective!r}; supported: {supported}")

    resources = parse_resources(state)
    levels, warnings = parse_levels(state, upgrades)
    locked_upgrades, locked_warnings = parse_locked_upgrades(state, upgrades)
    warnings.extend(locked_warnings)
    weights = dict(GOLD_ONLY_WEIGHTS)
    weights["kill_gold"] = float(args.gold_weight)

    final_levels, remaining, purchases, diagnostics = optimize(
        upgrades=upgrades,
        levels=levels,
        resources=resources,
        weights=weights,
        max_steps=args.max_steps,
        locked_upgrades=locked_upgrades,
    )
    result = gold_only_result_document(
        upgrades=upgrades,
        state=state,
        initial_levels=levels,
        final_levels=final_levels,
        resources=resources,
        remaining=remaining,
        purchases=purchases,
        weights=weights,
        warnings=warnings,
        diagnostics=diagnostics,
    )
    write_result(args.output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
