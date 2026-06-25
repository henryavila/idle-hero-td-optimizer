#!/usr/bin/env python3
"""Regression checks for APK-derived upgrade cost formulas."""

from __future__ import annotations

import importlib.util
import sys
from decimal import Decimal
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
OPTIMIZER_PATH = SCRIPT_DIR / "optimize_farm_upgrades.py"


def load_optimizer_module():
    spec = importlib.util.spec_from_file_location("optimize_farm_upgrades", OPTIMIZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load optimizer module from {OPTIMIZER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def total_cost(module, upgrades, key: str, level: int, count: int) -> Decimal:
    total = Decimal(0)
    for offset in range(count):
        cost = module.next_level_cost(upgrades[key], level + offset)
        if cost is None:
            break
        total += cost
    return total


def assert_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")


def main() -> int:
    module = load_optimizer_module()
    upgrades = module.load_upgrades()

    # Fixtures from the 2026-06-25 screenshots. These catch the exact bug where
    # Research cost was treated as constant / wrong-axis exponential.
    research_next_costs = {
        ("researchDmg1", 446): Decimal("2235"),
        ("researchDmg2", 112): Decimal("8475"),
        ("researchDmg3", 31): Decimal("32000"),
        ("researchDmg4", 10): Decimal("110000"),
        ("researchDmg5", 10): Decimal("1100000"),
        ("researchPrestigePower1", 765): Decimal("7660"),
        ("researchKillGold5", 3): Decimal("400000"),
    }
    for (key, level), expected in research_next_costs.items():
        assert_equal(module.next_level_cost(upgrades[key], level), expected, f"{key} +1")

    research_batch_costs = {
        ("researchDmg1", 446, 10): Decimal("22575"),
        ("researchDmg2", 112, 10): Decimal("88125"),
        ("researchDmg5", 10, 10): Decimal("15500000"),
        ("researchPrestigePower1", 765, 100): Decimal("815500"),
    }
    for (key, level, count), expected in research_batch_costs.items():
        assert_equal(total_cost(module, upgrades, key, level, count), expected, f"{key} +{count}")

    # Prestige costs are BigDouble-style fractional powers. The UI rounds them,
    # so the regression uses the same scientific formatting used in generated artifacts.
    prestige_next_costs = {
        ("prestigeDmg2", 332689): "1.411858498205E+14",
        ("prestigeDmg3", 10936): "4.251015530343E+15",
        ("prestigeDmg4", 638): "6.938252494388E+16",
        ("prestigeKillGold4", 638): "6.938252494388E+16",
    }
    for (key, level), expected in prestige_next_costs.items():
        formatted = module.format_decimal(module.next_level_cost(upgrades[key], level))
        assert_equal(formatted, expected, f"{key} +1 formatted")

    print("upgrade cost formula regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
