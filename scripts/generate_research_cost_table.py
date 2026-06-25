#!/usr/bin/env python3
"""Generate Research/Energy cost validation tables.

The script reuses the APK-derived cost formulas from optimize_farm_upgrades.py.
It is intended for quick UI validation before trusting optimizer outputs.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OPTIMIZER_PATH = SCRIPT_DIR / "optimize_farm_upgrades.py"
DEFAULT_OUTPUT_DIR = (
    PROJECT_ROOT
    / "IdleHeroTD-apk"
    / "apk_analysis"
    / "dados-consolidados"
    / "upgrades"
    / "tabelas-validacao"
)

ENERGY_UPGRADES = [
    ("Damage", "researchDmg1"),
    ("Damage", "researchDmg2"),
    ("Damage", "researchDmg3"),
    ("Damage", "researchDmg4"),
    ("Damage", "researchDmg5"),
    ("Damage", "researchDmg6"),
    ("Gold", "researchKillGold1"),
    ("Gold", "researchKillGold2"),
    ("Gold", "researchKillGold3"),
    ("Gold", "researchKillGold4"),
    ("Gold", "researchKillGold5"),
    ("Gold", "researchKillGold6"),
    ("Prestige", "researchPrestigePower1"),
    ("Prestige", "researchPrestigePower2"),
    ("Prestige", "researchPrestigePower3"),
    ("Prestige", "researchPrestigePower4"),
    ("Prestige", "researchPrestigePower5"),
]

DEFAULT_COUNTS = [1, 10, 100, 1000, 10000]


def load_optimizer_module():
    spec = importlib.util.spec_from_file_location("optimize_farm_upgrades", OPTIMIZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load optimizer module from {OPTIMIZER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def count_label(count: int) -> str:
    if count >= 1000 and count % 1000 == 0:
        return f"+{count // 1000}k"
    return f"+{count}"


def format_exact(value: Decimal | None) -> str:
    if value is None:
        return "-"
    if value == 0:
        return "0"
    if value == value.to_integral_value() and abs(value) < Decimal("1e15"):
        return f"{int(value):,}".replace(",", ".")
    return f"{value:.12E}"


def format_game(value: Decimal | None) -> str:
    if value is None:
        return "-"
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    value = -value if value < 0 else value
    for suffix, scale in (
        ("T", Decimal("1e12")),
        ("B", Decimal("1e9")),
        ("M", Decimal("1e6")),
        ("K", Decimal("1e3")),
    ):
        if value >= scale:
            return sign + f"{value / scale:.2f}".replace(".", ",") + suffix
    if value == value.to_integral_value():
        return sign + f"{int(value):,}".replace(",", ".")
    return sign + str(value).replace(".", ",")


def total_cost(optimizer, upgrades, key: str, level: int, count: int) -> tuple[int, Decimal]:
    total = Decimal(0)
    bought = 0
    for offset in range(count):
        cost = optimizer.next_level_cost(upgrades[key], level + offset)
        if cost is None:
            break
        total += cost
        bought += 1
    return bought, total


def max_affordable(
    optimizer,
    upgrades,
    key: str,
    level: int,
    budget: Decimal,
) -> tuple[int, Decimal, Decimal]:
    total = Decimal(0)
    bought = 0
    while True:
        cost = optimizer.next_level_cost(upgrades[key], level + bought)
        if cost is None or cost <= 0 or total + cost > budget:
            break
        total += cost
        bought += 1
    return bought, total, budget - total


def build_rows(
    optimizer,
    state: dict[str, Any],
    energy: Decimal,
    counts: list[int],
    include_locked: bool,
) -> list[dict[str, Any]]:
    upgrades = optimizer.load_upgrades()
    levels = {key: int(value) for key, value in state.get("levels", {}).items()}
    locked = set(state.get("locked_upgrades", []))
    rows: list[dict[str, Any]] = []

    for group, key in ENERGY_UPGRADES:
        if key in locked and not include_locked:
            continue
        level = levels.get(key, 0)
        status = "locked" if key in locked else "available"
        row: dict[str, Any] = {
            "group": group,
            "upgrade_key": key,
            "level": level,
            "status": status,
        }

        for count in counts:
            bought, cost = total_cost(optimizer, upgrades, key, level, count)
            label = count_label(count)
            row[label] = "maxed" if bought < count else format_exact(cost)
            row[f"{label}_game"] = "maxed" if bought < count else format_game(cost)

        bought, cost, remaining = max_affordable(optimizer, upgrades, key, level, energy)
        row.update(
            {
                "max_levels": bought,
                "max_to_level": level + bought,
                "max_cost": format_exact(cost),
                "max_cost_game": format_game(cost),
                "max_remaining": format_exact(remaining),
                "max_remaining_game": format_game(remaining),
            }
        )
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], counts: list[int]) -> None:
    headers = ["group", "upgrade_key", "level", "status"]
    headers.extend(count_label(count) for count in counts)
    headers.extend(
        [
            "max_levels",
            "max_to_level",
            "max_cost",
            "max_cost_game",
            "max_remaining",
            "max_remaining_game",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def write_md(path: Path, rows: list[dict[str, Any]], counts: list[int], energy: Decimal) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    count_headers = [count_label(count) for count in counts]
    with path.open("w", encoding="utf-8") as handle:
        handle.write("# Tabela de custo Research - Damage, Gold e Prestige Power\n\n")
        handle.write(
            f"Energy disponivel para MAX: `{format_game(energy)}` (`{format_exact(energy)}`).\n\n"
        )
        handle.write(
            "Formula: `roundToEven(baseCost * targetLevel ^ multCost)`, somada nivel a nivel.\n\n"
        )
        handle.write(
            "`MAX` simula gastar toda a Energy apenas naquele upgrade. "
            "Status `locked` significa bloqueado por wave no estado atual; os custos fixos sao teoricos.\n\n"
        )
        handle.write("| Grupo | Upgrade | Lv | Status | ")
        handle.write(" | ".join(count_headers))
        handle.write(" | MAX com Energy | Sobra |\n")
        handle.write("| --- | --- | ---: | --- | ")
        handle.write(" | ".join("---:" for _ in count_headers))
        handle.write(" | --- | ---: |\n")

        for row in rows:
            max_text = (
                f"+{row['max_levels']} lv -> {row['max_to_level']} "
                f"/ custo {row['max_cost']}"
            )
            handle.write(
                f"| {row['group']} | `{row['upgrade_key']}` | {row['level']} | {row['status']} | "
            )
            handle.write(" | ".join(str(row[label]) for label in count_headers))
            handle.write(f" | {max_text} | {row['max_remaining']} |\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path, help="Consolidated optimizer state JSON")
    parser.add_argument("--energy", required=True, help="Energy budget for MAX, e.g. 2,57M")
    parser.add_argument(
        "--counts",
        default=",".join(str(value) for value in DEFAULT_COUNTS),
        help="Comma-separated fixed counts, default: 1,10,100,1000,10000",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_OUTPUT_DIR / "research_dmg_gold_prestige_costs.md",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=DEFAULT_OUTPUT_DIR / "research_dmg_gold_prestige_costs.csv",
    )
    parser.add_argument(
        "--hide-locked",
        action="store_true",
        help="Do not include upgrades currently listed in locked_upgrades",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    optimizer = load_optimizer_module()
    state = load_json(args.state)
    energy = optimizer.parse_game_number(args.energy)
    counts = [int(item.strip()) for item in args.counts.split(",") if item.strip()]
    rows = build_rows(
        optimizer=optimizer,
        state=state,
        energy=energy,
        counts=counts,
        include_locked=not args.hide_locked,
    )
    write_md(args.output_md, rows, counts, energy)
    write_csv(args.output_csv, rows, counts)
    print(args.output_md)
    print(args.output_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
