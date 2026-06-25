#!/usr/bin/env python3
"""Generate clean map-bonus and hero-synergy reference docs."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import UnityPy

from synergy_values import SynergyValueCalculator, format_bonus_value


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = PROJECT_ROOT / "IdleHeroTD-apk" / "apk_analysis"
ASSETS_DIR = ANALYSIS_DIR / "dados-brutos" / "extracted" / "base" / "assets"
MAPS_DIR = ANALYSIS_DIR / "dados-consolidados" / "mapas"
MAPS_CSV_DIR = MAPS_DIR / "csv"
HEROES_DIR = ANALYSIS_DIR / "dados-consolidados" / "herois"
HEROES_CSV_DIR = HEROES_DIR / "csv"

MAP_NAMES = {
    1: "Island Hideout",
    2: "Snow Fort",
    3: "Barren Desert",
    4: "Haunted Cemetery",
    5: "Lava Dungeon",
    6: "Sunny Farm",
    7: "Astral Battleground",
}

ASTRAL_BATTLEGROUND_SKILL_PERKS = [
    ("+5% Skill Power", "+5%", "Skill Power", "green"),
    ("-25% Skill Cooldown", "-25%", "Skill Cooldown", "green"),
    ("-10% Spell Cooldown", "-10%", "Spell Cooldown", "green"),
    ("+5% Instant Skill Chance", "+5%", "Instant Skill Chance", "green"),
    ("+3% Instant Spell Chance", "+3%", "Instant Spell Chance", "green"),
    ("-75% Battlepass Exp", "-75%", "Battlepass Exp", "red"),
]

EFFECT_LABELS = {
    "damage": "Damage",
    "attSpeed": "Attack Speed",
    "range": "Range",
    "critChance": "Crit Chance",
    "critDmg": "Crit Damage",
    "skillPower": "Skill Power",
    "skillDuration": "Skill Duration",
    "skillCd": "Skill Cooldown",
    "killGold": "Kill Gold",
    "killExp": "Kill Exp",
    "superCritChance": "Super Crit Chance",
    "superCritDmg": "Super Crit Damage",
    "ultraCritChance": "Ultra Crit Chance",
    "ultraCritDmg": "Ultra Crit Damage",
    "goldSuperChance": "Gold Super Chance",
    "goldSuperAmount": "Gold Super Amount",
    "goldUltraChance": "Gold Ultra Chance",
    "goldUltraAmount": "Gold Ultra Amount",
    "expSuperChance": "Exp Super Chance",
    "expSuperAmount": "Exp Super Amount",
    "expUltraChance": "Exp Ultra Chance",
    "expUltraAmount": "Exp Ultra Amount",
    "energySuperChance": "Energy Super Chance",
    "energySuperAmount": "Energy Super Amount",
    "energyUltraChance": "Energy Ultra Chance",
    "energyUltraAmount": "Energy Ultra Amount",
    "energyIncome": "Energy Income",
    "bossGold": "Boss Gold",
    "bossExp": "Boss Exp",
    "powerMageEnergy": "Power Mage Energy",
    "shadowRunes": "Shadow Runes",
    "alienTech": "Alien Tech",
    "ultraBossDmg": "Ultra Boss Damage",
    "battlepassExp": "Battlepass Exp",
    "wavePerkBonus": "Wave Perk Bonus",
    "bossDmg": "Boss Damage",
    "instantSkillChance": "Instant Skill Chance",
    "goblinHoarderGold": "Goblin Hoarder Gold",
    "instantSpell_gold": "Instant Spell Gold",
    "instantspell_exp": "Instant Spell Exp",
    "instantSpell_blizzard": "Instant Spell Blizzard",
    "instantSpell_agility": "Instant Spell Agility",
    "instantSpell_accelerate": "Instant Spell Accelerate",
    "instantSpell_powerPlant": "Instant Spell Power Plant",
    "instantSpell_timeWarp": "Instant Spell Time Warp",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def load_unity_env() -> Any:
    paths = [ASSETS_DIR / "bin" / "Data" / "data.unity3d"]
    paths.extend(
        p
        for p in ASSETS_DIR.iterdir()
        if p.is_file() and p.name != "UnityServicesProjectConfiguration.json"
    )
    return UnityPy.load(*map(str, paths))


def strip_rich_text(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value)
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def split_effect_key(effect_key: str) -> tuple[str, str]:
    if effect_key.endswith("_global"):
        return effect_key.removesuffix("_global"), "global"
    if effect_key.endswith("_personal"):
        return effect_key.removesuffix("_personal"), "personal"
    return effect_key, "special"


def effect_label(effect_key: str) -> tuple[str, str]:
    base_key, scope = split_effect_key(effect_key)
    return EFFECT_LABELS.get(base_key, base_key), scope


def find_map_panel_texts() -> dict[str, dict[str, Any]]:
    env = load_unity_env()
    found: dict[str, dict[str, Any]] = {}
    for obj in env.objects:
        try:
            text = obj.get_raw_data().decode("utf-8", errors="ignore")
        except Exception:
            continue
        if "<color=#00FFFF>" not in text:
            continue
        for map_name in MAP_NAMES.values():
            marker = f"<color=#00FFFF>{map_name}</color>"
            marker_pos = text.find(marker)
            if marker_pos == -1:
                continue
            start = text.rfind("<size=32>", 0, marker_pos)
            end = text.find("\x00", marker_pos)
            if start == -1:
                start = marker_pos
            if end == -1:
                end = min(len(text), marker_pos + 800)
            found[map_name] = {
                "source_behaviour_path_id": obj.path_id,
                "rich_text": text[start:end].strip(),
            }
    return found


def parse_map_bonus_line(line: str) -> dict[str, str]:
    match = re.match(r"<color=(?P<color>[^>]+)>(?P<value>[^<]+)</color>\s*(?P<stat>.*)", line)
    clean = strip_rich_text(line)
    if not match:
        return {
            "bonus_text": clean,
            "bonus_value": "",
            "bonus_stat": clean,
            "ui_color": "",
        }
    return {
        "bonus_text": clean,
        "bonus_value": match.group("value").strip(),
        "bonus_stat": strip_rich_text(match.group("stat")),
        "ui_color": match.group("color").strip(),
    }


def build_map_bonus_rows() -> list[dict[str, Any]]:
    panel_texts = find_map_panel_texts()
    rows: list[dict[str, Any]] = []

    for map_num in range(1, 7):
        map_name = MAP_NAMES[map_num]
        panel = panel_texts.get(map_name, {})
        lines = [line.strip() for line in panel.get("rich_text", "").splitlines() if line.strip()]
        bonus_lines = lines[1:] if len(lines) > 1 else ["Default Stats"]
        for order, rich_line in enumerate(bonus_lines, start=1):
            parsed = parse_map_bonus_line(rich_line)
            rows.append(
                {
                    "map_num": map_num,
                    "map_id": f"map{map_num}",
                    "map_name": map_name,
                    "bonus_order": order,
                    **parsed,
                    "source": "map_panel_text",
                    "source_behaviour_path_id": panel.get("source_behaviour_path_id", ""),
                }
            )

    for order, (text, value, stat, color) in enumerate(ASTRAL_BATTLEGROUND_SKILL_PERKS, start=1):
        rows.append(
            {
                "map_num": 7,
                "map_id": "map7",
                "map_name": MAP_NAMES[7],
                "bonus_order": order,
                "bonus_text": text,
                "bonus_value": value,
                "bonus_stat": stat,
                "ui_color": color,
                "source": "user_screenshot_astral_skill_perks_2026-06-25",
                "source_behaviour_path_id": "",
            }
        )

    return rows


def write_map_bonus_doc(rows: list[dict[str, Any]]) -> None:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["map_num"])].append(row)

    lines = [
        "# Bonus fixos de mapas",
        "",
        "Este arquivo lista somente os bonus/penalidades especificos de cada mapa.",
        "Nao mistura bonus de slot/posicionamento nem a lista completa de perks compraveis.",
        "",
    ]

    for map_num in range(1, 8):
        lines.extend([f"## map{map_num} - {MAP_NAMES[map_num]}", ""])
        for row in sorted(grouped.get(map_num, []), key=lambda item: int(item["bonus_order"])):
            suffix = ""
            if row.get("ui_color"):
                suffix = f" (UI color: {row['ui_color']})"
            if row.get("source") == "user_screenshot_astral_skill_perks_2026-06-25":
                suffix += " (Astral Skill Perks)"
            lines.append(f"- {row['bonus_text']}{suffix}")
        lines.append("")

    (MAPS_DIR / "bonus_fixos.md").write_text("\n".join(lines), encoding="utf-8")


def build_hero_synergy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    calculator = SynergyValueCalculator()
    for row in read_csv(HEROES_CSV_DIR / "sinergias_mapa.csv"):
        label, scope = effect_label(row["synergy_upgrade_name"])
        required_names = row["required_hero_names"].replace("|", " + ")
        if row.get("base_bonus_value"):
            base_bonus_value = int(float(row["base_bonus_value"]))
            base_bonus_raw = row.get("base_bonus_raw", "")
            base_bonus_text = row.get("base_bonus_text") or format_bonus_value(
                base_bonus_value, row["synergy_upgrade_name"]
            )
        else:
            base_bonus_value = calculator.base_value(int(row["synergy_upgrade_id"]), int(row["synergy_num"]))
            base_bonus_raw = calculator.base_value_raw(int(row["synergy_upgrade_id"]), int(row["synergy_num"]))
            base_bonus_text = format_bonus_value(base_bonus_value, row["synergy_upgrade_name"])
        rows.append(
            {
                "hero_id": row["hero_id"],
                "hero_name": row["hero_name"],
                "hero_class": row["hero_class"],
                "hero_rarity": row["hero_rarity"],
                "synergy_num": row["synergy_num"],
                "tier": row["tier"],
                "rank_required": row["rank_required"],
                "requirements": required_names,
                "active_heroes_needed_including_self": row["active_heroes_needed_including_self"],
                "base_bonus_value": base_bonus_value,
                "base_bonus_raw": base_bonus_raw,
                "base_bonus_text": base_bonus_text,
                "effect_stat": label,
                "effect_with_value": f"{base_bonus_text} {label}",
                "effect_scope": scope,
                "effect_key": row["synergy_upgrade_name"],
                "synergy_upgrade_id": row["synergy_upgrade_id"],
                "required_hero_ids": row["required_hero_ids"],
                "source": "Hero MonoBehaviour synergy fields",
            }
        )
    return rows


def write_hero_synergy_doc(rows: list[dict[str, Any]]) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    hero_meta: dict[str, dict[str, Any]] = {}
    for row in rows:
        grouped[row["hero_name"]].append(row)
        hero_meta[row["hero_name"]] = row

    lines = [
        "# Sinergias de herois",
        "",
        "Mapa limpo das sinergias extraidas dos MonoBehaviours `Hero`.",
        "",
        "- `Tier`: duas sinergias por tier.",
        "- `Rank min`: rank minimo exigido para todos os herois da sinergia.",
        "- `Requer`: herois que precisam ficar proximos do heroi principal.",
        "- `Bonus base`: valor estatico calculado de `GlobalMethods.GetSynergyValue` antes de modificadores dinamicos de save/mapa/slot.",
        "- `Scope`: `personal` afeta o heroi principal; `global` afeta todos os herois.",
        "- `Effect key`: enum raw `HeroUpgrade` extraida do jogo.",
        "",
        "Nota: a UI do seu save pode mostrar um valor maior que o base se houver multiplicadores dinamicos. Ex.: base `+10% Attack Speed` pode aparecer como `+11%` com bonus global ativo.",
        "",
    ]

    for hero_name in sorted(grouped, key=lambda name: int(hero_meta[name]["hero_id"])):
        meta = hero_meta[hero_name]
        lines.extend(
            [
                f"## {hero_name}",
                "",
                f"- Hero ID: {meta['hero_id']}",
                f"- Class: {meta['hero_class']}",
                f"- Rarity: {meta['hero_rarity']}",
                "",
                "| # | Tier | Rank min | Requer | Bonus base | Scope | Effect key |",
                "|---:|---:|---:|---|---|---|---|",
            ]
        )
        for row in sorted(grouped[hero_name], key=lambda item: int(item["synergy_num"])):
            lines.append(
                "| {synergy_num} | {tier} | {rank_required}+ | {requirements} | {effect_with_value} | {effect_scope} | `{effect_key}` |".format(
                    **row
                )
            )
        lines.append("")

    (HEROES_DIR / "sinergias_por_heroi.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    map_rows = build_map_bonus_rows()
    write_csv(
        MAPS_CSV_DIR / "bonus_fixos.csv",
        map_rows,
        [
            "map_num",
            "map_id",
            "map_name",
            "bonus_order",
            "bonus_text",
            "bonus_value",
            "bonus_stat",
            "ui_color",
            "source",
            "source_behaviour_path_id",
        ],
    )
    write_map_bonus_doc(map_rows)

    synergy_rows = build_hero_synergy_rows()
    write_csv(
        HEROES_CSV_DIR / "sinergias_por_heroi.csv",
        synergy_rows,
        [
            "hero_id",
            "hero_name",
            "hero_class",
            "hero_rarity",
            "synergy_num",
            "tier",
            "rank_required",
            "requirements",
            "active_heroes_needed_including_self",
            "base_bonus_value",
            "base_bonus_raw",
            "base_bonus_text",
            "effect_stat",
            "effect_with_value",
            "effect_scope",
            "effect_key",
            "synergy_upgrade_id",
            "required_hero_ids",
            "source",
        ],
    )
    write_hero_synergy_doc(synergy_rows)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
