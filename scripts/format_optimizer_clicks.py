#!/usr/bin/env python3
"""Convert optimizer purchases into game multiplier click commands."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


MULTIPLY = "\u00d7"
MULTIPLIERS = (
    (10000, "10k"),
    (1000, "1k"),
    (100, "100"),
    (10, "10"),
    (1, "1"),
)

KEY_PATTERNS = (
    (re.compile(r"^researchDmg(\d+)$"), "Research/Energy", "dmg"),
    (re.compile(r"^researchKillGold(\d+)$"), "Research/Energy", "gold"),
    (re.compile(r"^researchPrestigePower(\d+)$"), "Research/Energy", "prest"),
    (re.compile(r"^prestigeDmg(\d+)$"), "Prestige/PowerUps", "dmg"),
    (re.compile(r"^prestigeKillGold(\d+)$"), "Prestige/PowerUps", "gold"),
)

SECTION_ORDER = {
    "Research/Energy": 0,
    "Prestige/PowerUps": 1,
}

LABEL_ORDER = {
    "dmg": 0,
    "gold": 1,
    "prest": 2,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def classify_upgrade(key: str) -> tuple[str, str, int]:
    for pattern, section, label_prefix in KEY_PATTERNS:
        match = pattern.match(key)
        if match:
            return section, label_prefix, int(match.group(1))
    return "Other", key, 0


def decompose_clicks(levels: int) -> list[tuple[int, str]]:
    remaining = int(levels)
    parts: list[tuple[int, str]] = []
    for value, label in MULTIPLIERS:
        clicks, remaining = divmod(remaining, value)
        if clicks:
            parts.append((clicks, label))
    return parts


def format_clicks(levels: int) -> str:
    parts = decompose_clicks(levels)
    if not parts:
        return f"0{MULTIPLY}1"
    return " + ".join(f"{clicks}{MULTIPLY}{label}" for clicks, label in parts)


def build_lines(result: dict[str, Any], include_zero: bool = False) -> dict[str, list[str]]:
    sections: dict[str, list[tuple[int, int, str]]] = {}
    for purchase in result.get("purchases", []):
        levels = int(purchase.get("levels_bought", 0))
        if levels == 0 and not include_zero:
            continue
        key = str(purchase["upgrade_key"])
        section, label_prefix, number = classify_upgrade(key)
        label = f"{label_prefix}{number}" if number else label_prefix
        sort_key = LABEL_ORDER.get(label_prefix, 99), number
        line = f"{label}: {format_clicks(levels)}"
        sections.setdefault(section, []).append((sort_key[0], sort_key[1], line))

    ordered: dict[str, list[str]] = {}
    for section, entries in sorted(
        sections.items(),
        key=lambda item: SECTION_ORDER.get(item[0], 99),
    ):
        ordered[section] = [line for _label_order, _number, line in sorted(entries)]
    return ordered


def render_sections(sections: dict[str, list[str]], no_headers: bool = False) -> str:
    chunks: list[str] = []
    for section, lines in sections.items():
        if not lines:
            continue
        if no_headers:
            chunks.extend(lines)
        else:
            chunks.append(f"{section}:")
            chunks.extend(lines)
        chunks.append("")
    return "\n".join(chunks).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", required=True, type=Path, help="Optimizer result JSON")
    parser.add_argument("--output", type=Path, help="Output text file")
    parser.add_argument("--include-zero", action="store_true", help="Include zero-level purchases")
    parser.add_argument(
        "--no-headers",
        action="store_true",
        help="Emit only command lines, without section headers",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = load_json(args.result)
    text = render_sections(
        build_lines(result, include_zero=args.include_zero),
        no_headers=args.no_headers,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
