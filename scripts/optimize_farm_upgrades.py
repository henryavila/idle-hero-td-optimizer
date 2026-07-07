#!/usr/bin/env python3
"""Optimize Idle Hero TD permanent upgrades for selected target metrics.

The script uses the consolidated APK-derived CSVs, not rounded UI numbers.
For FARM, Kill Gold is excluded by default because it only matters when extra
gold becomes useful hero levels during the run.
"""

from __future__ import annotations

import argparse
import csv
import heapq
import json
import math
import re
import sys
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP, getcontext
from functools import lru_cache
from pathlib import Path
from typing import Any


getcontext().prec = 80

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FORMULAS_DIR = (
    PROJECT_ROOT
    / "IdleHeroTD-apk"
    / "apk_analysis"
    / "dados-consolidados"
    / "formulas"
)
CSV_DIR = FORMULAS_DIR / "csv"
FACTORS_CSV = CSV_DIR / "core_upgrade_formula_factors.csv"
COSTS_CSV = CSV_DIR / "core_upgrade_cost_formula_classes.csv"

METRIC_LABELS = {
    "damage": "Damage",
    "kill_gold": "Kill Gold",
    "prestige_power": "Prestige Power",
}
METRIC_TARGET_ALIASES = {
    "dmg": "damage",
    "damage": "damage",
    "gold": "kill_gold",
    "kill_gold": "kill_gold",
    "killgold": "kill_gold",
    "prestige": "prestige_power",
    "prestige_power": "prestige_power",
    "prestigepower": "prestige_power",
}
DEFAULT_TARGETS_BY_OBJECTIVE = {
    "FARM": ["damage", "prestige_power"],
    "GOLD_PREP": ["kill_gold"],
    "PUSH_GOLD": ["kill_gold"],
    "KILL_GOLD": ["kill_gold"],
}
RESOURCE_ALIASES = {
    "energy": "energy",
    "research_energy": "energy",
    "prestige": "prestige_points",
    "prestige_points": "prestige_points",
    "prestigePoints": "prestige_points",
    "powerups": "prestige_points",
}
DEFAULT_FARM_WEIGHTS = {
    "damage": 1.0,
    "kill_gold": 0.0,
    "prestige_power": 1.0,
}
SCALE_SUFFIXES = {
    "k": Decimal("1e3"),
    "m": Decimal("1e6"),
    "b": Decimal("1e9"),
    "t": Decimal("1e12"),
}
POWERUPS_HIGH_THRESHOLD_PCT = Decimal("0.800000011920929")
POWERUPS_ENDGAME_SLOPE = Decimal("0.0010000000474974513")
MAX_EXACT_POW_LOG10 = 2500.0
LN_10 = math.log(10.0)


@dataclass(frozen=True)
class Upgrade:
    key: str
    resource: str
    metric: str
    percent_per_level: Decimal
    base_cost: Decimal
    mult_cost: Decimal
    max_level: int
    override_formula_endgame: bool
    formula_class: str
    formula_factor: str


@dataclass
class Purchase:
    upgrade_key: str
    resource: str
    metric: str
    from_level: int
    to_level: int
    levels_bought: int
    spent: Decimal
    log_gain: float


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_number_text(text: str, suffix_context: bool = False) -> str:
    compact = text.strip().replace("_", "").replace(" ", "")
    if "," not in compact:
        return compact
    if "." in compact:
        return compact.replace(",", "")
    if suffix_context:
        return compact.replace(",", ".")

    parts = compact.split(",")
    if len(parts) > 2:
        return "".join(parts)
    left, right = parts
    if left.lstrip("+-").isdigit() and right.isdigit() and len(right) == 3:
        return left + right
    return left + "." + right


def parse_game_number(value: Any, default: Decimal = Decimal(0)) -> Decimal:
    if value is None or value == "":
        return default
    if isinstance(value, Decimal):
        return value

    text = str(value).strip()
    if not text:
        return default

    compact = text.replace("_", "").replace(" ", "")
    if re.fullmatch(r"[eE][+-]?\d+", compact):
        compact = "1" + compact

    normalized = normalize_number_text(compact)
    try:
        return Decimal(normalized)
    except Exception:
        pass

    match = re.fullmatch(r"([+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+))([kKmMbBtT])", compact)
    if match:
        mantissa = Decimal(normalize_number_text(match.group(1), suffix_context=True))
        return mantissa * SCALE_SUFFIXES[match.group(2).lower()]

    examples = "100K, 1.5M, 2B, 3.25T, 1e15, 2.4e16"
    raise ValueError(f"invalid game number {value!r}; accepted examples: {examples}")


def dec(value: Any, default: Decimal = Decimal(0)) -> Decimal:
    return parse_game_number(value, default)


def load_upgrades() -> dict[str, Upgrade]:
    factor_rows = {row["upgrade_key"]: row for row in read_rows(FACTORS_CSV)}
    cost_rows = {row["upgrade_key"]: row for row in read_rows(COSTS_CSV)}
    upgrades: dict[str, Upgrade] = {}

    for key, factor in factor_rows.items():
        cost = cost_rows.get(key)
        if not cost:
            continue
        upgrades[key] = Upgrade(
            key=key,
            resource=normalize_resource(cost["resource"]),
            metric=factor["metric"],
            percent_per_level=dec(factor["percent_per_level"]),
            base_cost=dec(cost["base_cost"]),
            mult_cost=dec(cost["mult_cost"]),
            max_level=int(dec(cost["max_level"])),
            override_formula_endgame=bool(int(cost["override_formula_endgame"] or 0)),
            formula_class=cost["formula_class"],
            formula_factor=factor["formula_factor"],
        )

    return upgrades


def normalize_resource(resource: str) -> str:
    key = resource.strip()
    try:
        return RESOURCE_ALIASES[key]
    except KeyError as exc:
        raise ValueError(f"unknown resource name: {resource}") from exc


def round_to_even(value: Decimal) -> Decimal:
    return value.to_integral_value(rounding=ROUND_HALF_EVEN)


def round_half_up_int(value: Decimal) -> int:
    return int(value.to_integral_value(rounding=ROUND_HALF_UP))


def decimal_log10(value: Decimal) -> float:
    if value <= 0:
        return float("-inf")
    adjusted = value.adjusted()
    mantissa = float(value.scaleb(-adjusted))
    return math.log10(mantissa) + adjusted


def decimal_ln(value: Decimal) -> float:
    return decimal_log10(value) * LN_10


def decimal_from_log10(log10_value: float) -> Decimal:
    if log10_value == float("-inf"):
        return Decimal(0)
    exponent = math.floor(log10_value)
    mantissa = 10 ** (log10_value - exponent)
    return Decimal(str(mantissa)).scaleb(exponent)


def pow_decimal(base: Decimal, exponent: Decimal) -> Decimal:
    if base == 0:
        return Decimal(0)

    log10_value = decimal_log10(base) * float(exponent)
    if exponent == exponent.to_integral_value():
        integer_exponent = int(exponent)
        if 0 <= integer_exponent <= 20 and log10_value <= MAX_EXACT_POW_LOG10:
            return base ** integer_exponent
    return decimal_from_log10(log10_value)


def powerups_extra_multiplier(target_level: int, max_level: int) -> Decimal:
    threshold_a = round_half_up_int(Decimal(max_level) * Decimal("0.5"))
    threshold_b = round_half_up_int(Decimal(max_level) * POWERUPS_HIGH_THRESHOLD_PCT)

    extra = Decimal(1)
    if target_level >= threshold_a:
        extra *= Decimal(3)
    if target_level >= threshold_b:
        extra *= Decimal(8)
    if target_level >= 2 and max_level >= 1000:
        extra *= Decimal(1) + Decimal(target_level) * POWERUPS_ENDGAME_SLOPE
    return extra


@lru_cache(maxsize=None)
def next_level_cost(upgrade: Upgrade, current_level: int) -> Decimal | None:
    if current_level >= upgrade.max_level:
        return None

    target_level = current_level + 1
    if upgrade.formula_class.startswith("research_"):
        raw = upgrade.base_cost * pow_decimal(Decimal(target_level), upgrade.mult_cost)
        return round_to_even(raw)

    if upgrade.override_formula_endgame:
        raw = upgrade.base_cost * pow_decimal(upgrade.mult_cost, Decimal(target_level - 1))
    else:
        raw = upgrade.base_cost * pow_decimal(Decimal(target_level), upgrade.mult_cost)
    raw *= powerups_extra_multiplier(target_level, upgrade.max_level)
    return round_to_even(raw)


def is_constant_cost_research(upgrade: Upgrade) -> bool:
    return False


def factor_at(level: int, percent_per_level: Decimal) -> Decimal:
    return Decimal(1) + Decimal(level) * percent_per_level


def log_gain(upgrade: Upgrade, current_level: int, levels_bought: int, weight: float) -> float:
    if levels_bought <= 0 or weight <= 0:
        return 0.0
    before = float(factor_at(current_level, upgrade.percent_per_level))
    after = float(factor_at(current_level + levels_bought, upgrade.percent_per_level))
    return weight * math.log(after / before)


def score_for_next(
    upgrade: Upgrade,
    current_level: int,
    weights: dict[str, float],
    remaining: dict[str, Decimal],
) -> tuple[float, Decimal] | None:
    weight = weights.get(upgrade.metric, 0.0)
    if weight <= 0:
        return None

    cost = next_level_cost(upgrade, current_level)
    if cost is None or cost <= 0:
        return None
    if remaining.get(upgrade.resource, Decimal(0)) < cost:
        return None

    gain = log_gain(upgrade, current_level, 1, weight)
    if gain <= 0:
        return None

    score = math.log(gain) - decimal_ln(cost)
    return score, cost


def score_at_level(upgrade: Upgrade, current_level: int, weight: float, unit_cost: Decimal) -> float:
    gain = log_gain(upgrade, current_level, 1, weight)
    if gain <= 0 or unit_cost <= 0:
        return float("-inf")
    return math.log(gain) - decimal_ln(unit_cost)


def score_for_level(upgrade: Upgrade, current_level: int, weight: float) -> float:
    cost = next_level_cost(upgrade, current_level)
    if cost is None or cost <= 0:
        return float("-inf")
    return score_at_level(upgrade, current_level, weight, cost)


def constant_cost_batch_size(
    upgrade: Upgrade,
    current_level: int,
    unit_cost: Decimal,
    remaining: Decimal,
    runner_score: float,
    weight: float,
) -> int:
    max_by_level = upgrade.max_level - current_level
    max_by_budget_decimal = remaining // unit_cost
    if max_by_budget_decimal >= max_by_level:
        max_by_budget = max_by_level
    else:
        max_by_budget = int(max_by_budget_decimal)
    high = min(max_by_level, max_by_budget)
    if high <= 1:
        return max(0, high)
    if runner_score == float("-inf"):
        return high

    low = 1
    best = 1
    while low <= high:
        mid = (low + high) // 2
        last_level_before_purchase = current_level + mid - 1
        score = score_at_level(upgrade, last_level_before_purchase, weight, unit_cost)
        if score >= runner_score:
            best = mid
            low = mid + 1
        else:
            high = mid - 1
    return best


def monotonic_batch_size_by_score(
    upgrade: Upgrade,
    current_level: int,
    runner_score: float,
    weight: float,
) -> int:
    high = upgrade.max_level - current_level
    if high <= 1:
        return max(0, high)
    if runner_score == float("-inf"):
        return high

    low = 1
    best = 1
    while low <= high:
        mid = (low + high) // 2
        last_level_before_purchase = current_level + mid - 1
        score = score_for_level(upgrade, last_level_before_purchase, weight)
        if score >= runner_score:
            best = mid
            low = mid + 1
        else:
            high = mid - 1
    return best


def affordable_variable_batch(
    upgrade: Upgrade,
    current_level: int,
    max_levels: int,
    remaining: Decimal,
) -> tuple[int, Decimal]:
    bought = 0
    total_cost = Decimal(0)
    for offset in range(max_levels):
        cost = next_level_cost(upgrade, current_level + offset)
        if cost is None or cost <= 0:
            break
        if total_cost + cost > remaining:
            break
        total_cost += cost
        bought += 1
    return bought, total_cost


def best_runner_score_for_resource(
    heap: list[tuple[float, int, str]],
    upgrades: dict[str, Upgrade],
    resource: str,
    final_levels: dict[str, int],
    weights: dict[str, float],
    remaining: dict[str, Decimal],
) -> float:
    best = float("-inf")
    for _negative_score, _serial, key in heap:
        upgrade = upgrades[key]
        if upgrade.resource != resource:
            continue
        candidate = score_for_next(upgrade, final_levels[key], weights, remaining)
        if candidate is not None:
            best = max(best, candidate[0])
    return best


def merge_purchase(purchases: dict[str, Purchase], purchase: Purchase) -> None:
    existing = purchases.get(purchase.upgrade_key)
    if existing is None:
        purchases[purchase.upgrade_key] = purchase
        return

    existing.to_level = purchase.to_level
    existing.levels_bought += purchase.levels_bought
    existing.spent += purchase.spent
    existing.log_gain += purchase.log_gain


def optimize(
    upgrades: dict[str, Upgrade],
    levels: dict[str, int],
    resources: dict[str, Decimal],
    weights: dict[str, float],
    max_steps: int,
    locked_upgrades: set[str] | None = None,
) -> tuple[dict[str, int], dict[str, Decimal], list[Purchase], dict[str, Any]]:
    remaining = dict(resources)
    final_levels = {key: int(levels.get(key, 0)) for key in upgrades}
    locked_upgrades = locked_upgrades or set()
    purchases: dict[str, Purchase] = {}
    heap: list[tuple[float, int, str]] = []
    serial = 0
    diagnostics: dict[str, Any] = {
        "iterations": 0,
        "hit_step_limit": False,
        "target_metrics": sorted(metric for metric, weight in weights.items() if weight > 0),
        "excluded_metrics": sorted(metric for metric, weight in weights.items() if weight <= 0),
        "locked_upgrades": sorted(locked_upgrades),
    }

    for key, upgrade in upgrades.items():
        if key in locked_upgrades:
            continue
        candidate = score_for_next(upgrade, final_levels[key], weights, remaining)
        if candidate is None:
            continue
        score, _cost = candidate
        heapq.heappush(heap, (-score, serial, key))
        serial += 1

    while heap and diagnostics["iterations"] < max_steps:
        diagnostics["iterations"] += 1
        _negative_score, _serial, key = heapq.heappop(heap)
        if key in locked_upgrades:
            continue
        upgrade = upgrades[key]
        current_level = final_levels[key]
        candidate = score_for_next(upgrade, current_level, weights, remaining)
        if candidate is None:
            continue
        score, cost = candidate
        runner_score = best_runner_score_for_resource(
            heap=heap,
            upgrades=upgrades,
            resource=upgrade.resource,
            final_levels=final_levels,
            weights=weights,
            remaining=remaining,
        )
        weight = weights[upgrade.metric]

        levels_to_buy = 1
        total_cost = cost
        total_log_gain = log_gain(upgrade, current_level, 1, weight)

        if is_constant_cost_research(upgrade):
            levels_to_buy = constant_cost_batch_size(
                upgrade=upgrade,
                current_level=current_level,
                unit_cost=cost,
                remaining=remaining[upgrade.resource],
                runner_score=runner_score,
                weight=weight,
            )
            if levels_to_buy <= 0:
                continue
            total_cost = cost * Decimal(levels_to_buy)
            total_log_gain = log_gain(upgrade, current_level, levels_to_buy, weight)
        else:
            candidate_batch_size = monotonic_batch_size_by_score(
                upgrade=upgrade,
                current_level=current_level,
                runner_score=runner_score,
                weight=weight,
            )
            levels_to_buy, total_cost = affordable_variable_batch(
                upgrade=upgrade,
                current_level=current_level,
                max_levels=candidate_batch_size,
                remaining=remaining[upgrade.resource],
            )
            if levels_to_buy <= 0:
                continue
            total_log_gain = log_gain(upgrade, current_level, levels_to_buy, weight)

        if remaining[upgrade.resource] < total_cost:
            continue

        final_levels[key] += levels_to_buy
        remaining[upgrade.resource] -= total_cost
        merge_purchase(
            purchases,
            Purchase(
                upgrade_key=key,
                resource=upgrade.resource,
                metric=upgrade.metric,
                from_level=current_level,
                to_level=final_levels[key],
                levels_bought=levels_to_buy,
                spent=total_cost,
                log_gain=total_log_gain,
            ),
        )

        next_candidate = score_for_next(upgrade, final_levels[key], weights, remaining)
        if next_candidate is not None:
            next_score, _next_cost = next_candidate
            heapq.heappush(heap, (-next_score, serial, key))
            serial += 1

    if heap and diagnostics["iterations"] >= max_steps:
        diagnostics["hit_step_limit"] = True

    ordered = sorted(
        purchases.values(),
        key=lambda item: (item.resource, item.metric, item.upgrade_key),
    )
    return final_levels, remaining, ordered, diagnostics


def metric_factor(upgrades: dict[str, Upgrade], levels: dict[str, int], metric: str) -> Decimal:
    result = Decimal(1)
    for upgrade in upgrades.values():
        if upgrade.metric == metric:
            result *= factor_at(levels.get(upgrade.key, 0), upgrade.percent_per_level)
    return result


def metric_factor_delta(
    upgrades: dict[str, Upgrade],
    initial_levels: dict[str, int],
    final_levels: dict[str, int],
    metric: str,
) -> Decimal:
    before = metric_factor(upgrades, initial_levels, metric)
    after = metric_factor(upgrades, final_levels, metric)
    if before == 0:
        return Decimal(0)
    return after / before


def format_decimal(value: Decimal) -> str:
    if value == 0:
        return "0"
    adjusted = value.adjusted()
    if adjusted >= 12 or adjusted <= -6:
        return f"{value:.12E}"
    text = format(value.normalize(), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def normalize_target_metric(value: Any) -> str | None:
    key = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    return METRIC_TARGET_ALIASES.get(key)


def parse_target_metrics(raw_value: Any) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    selected: list[str] = []
    for raw_metric in _string_list(raw_value):
        metric = normalize_target_metric(raw_metric)
        if metric is None:
            warnings.append(f"ignored unknown target metric: {raw_metric}")
            continue
        if metric not in selected:
            selected.append(metric)
    ordered = [metric for metric in METRIC_LABELS if metric in selected]
    return ordered, warnings


def target_metrics_from_state(state: dict[str, Any], objective: str) -> tuple[list[str], list[str], bool]:
    for key in ("target_metrics", "targets", "upgrade_targets"):
        if key in state:
            metrics, warnings = parse_target_metrics(state.get(key))
            return metrics, warnings, True
    return list(DEFAULT_TARGETS_BY_OBJECTIVE.get(objective, [])), [], False


def build_weights(
    state: dict[str, Any],
    args: argparse.Namespace,
    warnings: list[str] | None = None,
) -> dict[str, float]:
    objective = str(state.get("objective", "FARM")).upper()
    target_metrics, target_warnings, explicit_targets = target_metrics_from_state(state, objective)
    if warnings is not None:
        warnings.extend(target_warnings)

    farm = state.get("farm", {})
    if explicit_targets or objective != "FARM":
        weights = {metric: 0.0 for metric in METRIC_LABELS}
        for metric in target_metrics:
            weights[metric] = 1.0
        raw_weight_overrides = state.get("target_weights", state.get("weights", {}))
        for raw_metric, raw_weight in raw_weight_overrides.items():
            metric = normalize_target_metric(raw_metric)
            if metric in target_metrics:
                weights[metric] = float(raw_weight)
    else:
        weights = dict(DEFAULT_FARM_WEIGHTS)
        weights.update({key: float(value) for key, value in farm.get("weights", {}).items()})

        if farm.get("damage_effective") is False:
            weights["damage"] = 0.0
        if farm.get("prestige_power_effective") is False:
            weights["prestige_power"] = 0.0

        include_gold = bool(args.include_gold or farm.get("include_gold"))
        if include_gold and weights.get("kill_gold", 0.0) == 0.0:
            weights["kill_gold"] = 1.0
        elif not include_gold and "kill_gold" not in farm.get("weights", {}):
            weights["kill_gold"] = 0.0

    if args.damage_weight is not None:
        weights["damage"] = args.damage_weight
    if args.prestige_weight is not None:
        weights["prestige_power"] = args.prestige_weight
    if args.gold_weight is not None:
        weights["kill_gold"] = args.gold_weight

    return {key: float(weights.get(key, 0.0)) for key in METRIC_LABELS}


def active_target_metrics(weights: dict[str, float]) -> list[str]:
    return [metric for metric in METRIC_LABELS if weights.get(metric, 0.0) > 0]


def load_state(path: str | None) -> dict[str, Any]:
    if path == "-":
        return json.load(sys.stdin)
    if path:
        with Path(path).open(encoding="utf-8") as handle:
            return json.load(handle)
    raise SystemExit("--state is required unless --print-template is used")


def parse_resources(state: dict[str, Any]) -> dict[str, Decimal]:
    resources = {"energy": Decimal(0), "prestige_points": Decimal(0)}
    for raw_key, raw_value in state.get("resources", {}).items():
        resources[normalize_resource(raw_key)] = dec(raw_value)
    return resources


def parse_levels(state: dict[str, Any], upgrades: dict[str, Upgrade]) -> tuple[dict[str, int], list[str]]:
    warnings: list[str] = []
    raw_levels = state.get("levels", {})
    levels: dict[str, int] = {}

    for key, upgrade in upgrades.items():
        raw = raw_levels.get(key, 0)
        level = int(dec(raw))
        if level < 0:
            warnings.append(f"{key}: negative level {level} changed to 0")
            level = 0
        if level > upgrade.max_level:
            warnings.append(f"{key}: level {level} capped at max_level {upgrade.max_level}")
            level = upgrade.max_level
        levels[key] = level

    unknown = sorted(set(raw_levels) - set(upgrades))
    for key in unknown:
        warnings.append(f"ignored unknown upgrade level: {key}")
    return levels, warnings


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(_string_list(item))
        return result
    text = str(value).strip()
    return [text] if text else []


def parse_locked_upgrades(state: dict[str, Any], upgrades: dict[str, Upgrade]) -> tuple[set[str], list[str]]:
    warnings: list[str] = []
    locked = set(_string_list(state.get("locked_upgrades")))
    locked.update(_string_list(state.get("unavailable_upgrades")))

    unknown = sorted(locked - set(upgrades))
    for key in unknown:
        warnings.append(f"ignored unknown locked upgrade: {key}")
    return locked & set(upgrades), warnings


def template(upgrades: dict[str, Upgrade]) -> dict[str, Any]:
    return {
        "objective": "FARM",
        "target_metrics": ["damage", "prestige_power"],
        "resources": {
            "energy": "0",
            "prestige_points": "0",
        },
        "levels": {key: 0 for key in sorted(upgrades)},
        "locked_upgrades": [],
        "farm": {
            "damage_effective": True,
            "prestige_power_effective": True,
            "include_gold": False,
            "weights": {
                "damage": 1.0,
                "prestige_power": 1.0,
                "kill_gold": 0.0,
            },
        },
    }


def result_document(
    upgrades: dict[str, Upgrade],
    state: dict[str, Any],
    initial_levels: dict[str, int],
    final_levels: dict[str, int],
    resources: dict[str, Decimal],
    remaining: dict[str, Decimal],
    purchases: list[Purchase],
    weights: dict[str, float],
    warnings: list[str],
    diagnostics: dict[str, Any],
) -> dict[str, Any]:
    objective = str(state.get("objective", "FARM")).upper()
    target_metrics = active_target_metrics(weights)
    target_labels = ", ".join(METRIC_LABELS[metric] for metric in target_metrics)
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
            "spent": format_decimal(start_value - remaining.get(resource, Decimal(0))),
            "remaining": format_decimal(remaining.get(resource, Decimal(0))),
        }

    return {
        "objective": objective,
        "target_metrics": target_metrics,
        "method": "marginal_log_roi_greedy_with_research_and_powerups_batching",
        "assumptions": [
            "Uses APK-derived factor and cost CSVs, not rounded UI values.",
            "Energy and Prestige Points are separate budgets.",
            f"Selected optimization targets: {target_labels}.",
            "Upgrades listed in locked_upgrades/unavailable_upgrades are excluded from candidate purchases.",
            "Score maximized is the weighted log multiplier across the selected target metrics.",
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


def write_result(path: str | None, result: dict[str, Any]) -> None:
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if path:
        Path(path).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Optimize Idle Hero TD permanent upgrades from a JSON state."
    )
    parser.add_argument("--state", help="Input JSON state file. Use '-' to read stdin.")
    parser.add_argument("--output", help="Optional JSON output path.")
    parser.add_argument("--print-template", action="store_true", help="Print a complete input template.")
    parser.add_argument("--include-gold", action="store_true", help="Include Kill Gold with weight 1 unless overridden.")
    parser.add_argument("--damage-weight", type=float, help="Override FARM weight for Damage.")
    parser.add_argument("--prestige-weight", type=float, help="Override FARM weight for Prestige Power.")
    parser.add_argument("--gold-weight", type=float, help="Override FARM weight for Kill Gold.")
    parser.add_argument("--max-steps", type=int, default=200000, help="Safety cap for non-batched optimizer iterations.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    upgrades = load_upgrades()

    if args.print_template:
        print(json.dumps(template(upgrades), indent=2, ensure_ascii=False))
        return 0

    state = load_state(args.state)
    objective = str(state.get("objective", "FARM")).upper()
    has_explicit_targets = any(key in state for key in ("target_metrics", "targets", "upgrade_targets"))
    if objective not in DEFAULT_TARGETS_BY_OBJECTIVE and not has_explicit_targets:
        supported = ", ".join(sorted(DEFAULT_TARGETS_BY_OBJECTIVE))
        raise SystemExit(
            f"unsupported objective {objective!r}; supported: {supported}; "
            "or provide target_metrics"
        )

    resources = parse_resources(state)
    levels, warnings = parse_levels(state, upgrades)
    locked_upgrades, locked_warnings = parse_locked_upgrades(state, upgrades)
    warnings.extend(locked_warnings)
    weights = build_weights(state, args, warnings)
    if not active_target_metrics(weights):
        raise SystemExit("select at least one target metric: damage, kill_gold, prestige_power")
    final_levels, remaining, purchases, diagnostics = optimize(
        upgrades=upgrades,
        levels=levels,
        resources=resources,
        weights=weights,
        max_steps=args.max_steps,
        locked_upgrades=locked_upgrades,
    )
    result = result_document(
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
