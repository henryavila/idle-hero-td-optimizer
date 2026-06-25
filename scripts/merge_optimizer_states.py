#!/usr/bin/env python3
"""Merge OCR/state JSON files into one optimizer input state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from optimize_farm_upgrades import format_decimal, load_upgrades, parse_game_number


def load_json(path: str) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected JSON object")
    return data


def read_levels(path: str) -> dict[str, int]:
    data = load_json(path)
    raw_levels = data.get("levels")
    if not isinstance(raw_levels, dict):
        raise SystemExit(f"{path}: missing object field 'levels'")

    levels: dict[str, int] = {}
    for key, value in raw_levels.items():
        if value is None:
            continue
        levels[str(key)] = int(parse_game_number(value))
    return levels


def parse_set_level(raw: str) -> tuple[str, int]:
    if "=" not in raw:
        raise SystemExit(f"--set expects upgrade_key=level, got {raw!r}")
    key, value = raw.split("=", 1)
    key = key.strip()
    if not key:
        raise SystemExit(f"--set expects upgrade_key=level, got {raw!r}")
    return key, int(parse_game_number(value))


def parse_key_args(values: list[str]) -> list[str]:
    keys: list[str] = []
    for value in values:
        keys.extend(key.strip() for key in str(value).split(",") if key.strip())
    return keys


def merge_levels(paths: list[str], conflict: str) -> tuple[dict[str, int], list[str]]:
    merged: dict[str, int] = {}
    warnings: list[str] = []
    for path in paths:
        for key, value in read_levels(path).items():
            if key in merged and merged[key] != value:
                message = f"conflict for {key}: {merged[key]} vs {value} from {path}"
                if conflict == "error":
                    raise SystemExit(message)
                warnings.append(message + " (kept last)")
            merged[key] = value
    return merged, warnings


def state_document(
    objective: str,
    energy: str,
    prestige_points: str,
    levels: dict[str, int],
    warnings: list[str],
    locked_upgrades: list[str],
) -> dict[str, Any]:
    payload = {
        "objective": objective,
        "resources": {
            "energy": format_decimal(parse_game_number(energy)),
            "prestige_points": format_decimal(parse_game_number(prestige_points)),
        },
        "levels": {key: levels[key] for key in sorted(levels)},
        "warnings": warnings,
    }
    if locked_upgrades:
        payload["locked_upgrades"] = sorted(set(locked_upgrades))
    return payload


def write_json(path: str | None, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if path:
        Path(path).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge Idle Hero TD optimizer state JSON files.")
    parser.add_argument("--state", action="append", default=[], help="State/report JSON with a top-level levels object.")
    parser.add_argument("--output", help="Output merged optimizer state JSON.")
    parser.add_argument("--objective", default="FARM", help="FARM, GOLD_PREP, PUSH_GOLD, etc.")
    parser.add_argument("--energy", default="0", help="Energy amount, accepts K/M/B/T/e notation.")
    parser.add_argument("--prestige-points", default="0", help="Prestige Points amount, accepts K/M/B/T/e notation.")
    parser.add_argument("--set", action="append", default=[], help="Manual level override: upgrade_key=level.")
    parser.add_argument("--maxed", action="append", default=[], help="Mark upgrade as max level from APK tables. Repeat or comma-separate.")
    parser.add_argument("--locked", action="append", default=[], help="Mark upgrade as locked/unavailable; optimizer will not buy it. Repeat or comma-separate.")
    parser.add_argument("--conflict", choices=["last", "error"], default="last")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.state and not args.set and not args.maxed:
        raise SystemExit("provide at least one --state, --set, or --maxed")

    levels, warnings = merge_levels(args.state, args.conflict)
    upgrades = load_upgrades()

    for key in parse_key_args(args.maxed):
        upgrade = upgrades.get(key)
        if upgrade is None:
            raise SystemExit(f"--maxed unknown upgrade key: {key}")
        if key in levels and levels[key] != upgrade.max_level:
            warnings.append(f"maxed override for {key}: {levels[key]} -> {upgrade.max_level}")
        levels[key] = upgrade.max_level

    for raw in args.set:
        key, value = parse_set_level(raw)
        if key in levels and levels[key] != value:
            warnings.append(f"manual override for {key}: {levels[key]} -> {value}")
        levels[key] = value

    payload = state_document(
        objective=str(args.objective).upper(),
        energy=args.energy,
        prestige_points=args.prestige_points,
        levels=levels,
        warnings=warnings,
        locked_upgrades=parse_key_args(args.locked),
    )
    write_json(args.output, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
