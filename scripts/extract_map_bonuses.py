#!/usr/bin/env python3
"""Extract Idle Hero TD map perks and placement bonuses from Unity data."""

from __future__ import annotations

import csv
import re
import struct
from pathlib import Path
from typing import Any

import UnityPy


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = PROJECT_ROOT / "IdleHeroTD-apk" / "apk_analysis"
ASSETS_DIR = ANALYSIS_DIR / "dados-brutos" / "extracted" / "base" / "assets"
MAPS_DIR = ANALYSIS_DIR / "dados-consolidados" / "mapas"
MAPS_CSV_DIR = MAPS_DIR / "csv"
TECH_CSV_DIR = ANALYSIS_DIR / "dados-consolidados" / "tecnico" / "csv"
UPGRADES_CSV_DIR = ANALYSIS_DIR / "dados-consolidados" / "upgrades" / "csv"
SCRIPT_DIR = ANALYSIS_DIR / "scripts-extraidos" / "il2cpp" / "Cpp2IL-diffable-cs" / "DiffableCs" / "Assembly-CSharp"

MAP_NAMES = {
    1: "Island Hideout",
    2: "Snow Fort",
    3: "Barren Desert",
    4: "Haunted Cemetery",
    5: "Lava Dungeon",
    6: "Sunny Farm",
    7: "Astral Battleground",
}


class Reader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.offset = 0

    def align4(self) -> None:
        self.offset = (self.offset + 3) & ~3

    def i32(self) -> int:
        value = struct.unpack_from("<i", self.data, self.offset)[0]
        self.offset += 4
        return value

    def i64(self) -> int:
        value = struct.unpack_from("<q", self.data, self.offset)[0]
        self.offset += 8
        return value

    def pptr_base(self) -> tuple[int, int]:
        file_id = self.i32()
        path_id = self.i64()
        return file_id, path_id

    def string(self) -> str:
        length = self.i32()
        value = self.data[self.offset : self.offset + length].decode("utf-8", errors="replace")
        self.offset += length
        self.align4()
        return value


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


def parse_enum(path: Path) -> dict[int, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    enum: dict[int, str] = {}
    for name, value in re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\d+),", text, re.MULTILINE):
        enum[int(value)] = name
    return enum


def clean_text(value: str) -> str:
    value = value or ""
    value = value.replace("<value>", "VALUE").replace("<formula>", "FORMULA")
    value = re.sub(r"<br\s*/?>", " ", value)
    value = re.sub(r"</?(i|b|u)>", "", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("\r", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", value).strip()


def infer_categories(*values: str) -> str:
    text = " ".join(v or "" for v in values).lower()
    categories: list[str] = []
    checks = [
        ("dano", ("damage", "dmg", "crit", "splash", "double shot", "att speed", "attspeed")),
        ("ouro", ("gold",)),
        ("exp", ("exp", "rank", "mastery", "battlepass")),
        ("energia", ("energy", "powermage", "power mage")),
        ("boss", ("boss", "mimic", "hoarder", "shadow", "alien")),
        ("skill_spell", ("skill", "spell", "cooldown", "instant")),
        ("alcance", ("range",)),
        ("sinergia", ("synergy",)),
        ("milestone", ("milestone",)),
        ("prestige", ("prestige",)),
        ("ritmo_mapa", ("enemy spawn", "wave perk", "waves", "trainer", "ad bonus")),
        ("controle_enemy", ("enemy move", "enemy hp", "enemy speed")),
    ]
    for category, needles in checks:
        if any(needle in text for needle in needles):
            categories.append(category)
    return "|".join(dict.fromkeys(categories)) or "geral"


def read_mono_base(raw: bytes) -> Reader:
    reader = Reader(raw)
    reader.pptr_base()
    reader.i32()
    reader.pptr_base()
    reader.string()
    return reader


def parse_map_perk_cell(raw: bytes) -> dict[str, Any]:
    reader = read_mono_base(raw)
    perk_id = reader.i32()
    upgrade_file_id, upgrade_path_id = reader.pptr_base()
    return {
        "perk_id": perk_id,
        "upgrade_file_id": upgrade_file_id,
        "upgrade_object_path_id": upgrade_path_id,
        "is_default_perk": reader.i32(),
        "is_astral_group": reader.i32(),
        "base_cost": reader.i32(),
        "max_level": reader.i32(),
        "base_amt": reader.i32(),
        "stat_amt": reader.i32(),
        "wave_req": reader.i32(),
    }


def parse_map_placement_cell(raw: bytes) -> dict[str, Any]:
    reader = read_mono_base(raw)
    upgrade_file_id, upgrade_path_id = reader.pptr_base()
    return {
        "upgrade_file_id": upgrade_file_id,
        "upgrade_object_path_id": upgrade_path_id,
        "bonus_id": reader.i32(),
        "base_cost": reader.i32(),
        "max_level": reader.i32(),
        "stat_amt": reader.i32(),
        "wave_req": reader.i32(),
    }


def upgrade_fields(row: dict[str, str] | None) -> dict[str, str]:
    if not row:
        return {
            "upgrade_field_name": "",
            "upgrade_title": "",
            "upgrade_short_desc": "",
            "upgrade_long_desc": "",
        }
    return {
        "upgrade_field_name": row.get("field_name", ""),
        "upgrade_title": row.get("title", ""),
        "upgrade_short_desc": clean_text(row.get("short_desc", "")),
        "upgrade_long_desc": clean_text(row.get("long_desc", "")),
    }


def main() -> int:
    mono_rows = read_csv(TECH_CSV_DIR / "mono_behaviours_amostra.csv")
    upgrade_rows = read_csv(UPGRADES_CSV_DIR / "catalogo_upgrades.csv")
    upgrade_by_path = {int(row["upgrade_object_path_id"]): row for row in upgrade_rows}

    map_perk_names = parse_enum(SCRIPT_DIR / "MapPerk.cs")
    placement_bonus_names = parse_enum(SCRIPT_DIR / "MapPlacementBonus.cs")

    env = load_unity_env()
    objects_by_path = {obj.path_id: obj for obj in env.objects}

    perk_rows: list[dict[str, Any]] = []
    placement_rows: list[dict[str, Any]] = []

    for mono in mono_rows:
        script_name = mono["script_name"]
        if script_name not in {"MapPerkUpgradeCell", "MapPlacementUpgradeCell"}:
            continue

        obj_path_id = int(mono["path_id"])
        raw = objects_by_path[obj_path_id].get_raw_data()

        if script_name == "MapPerkUpgradeCell":
            parsed = parse_map_perk_cell(raw)
            perk_name = map_perk_names.get(parsed["perk_id"], "")
            match = re.match(r"map(\d+)_(.+)", perk_name)
            map_num = int(match.group(1)) if match else 0
            perk_key = match.group(2) if match else perk_name
            upgrade = upgrade_by_path.get(parsed["upgrade_object_path_id"])
            fields = upgrade_fields(upgrade)
            perk_rows.append(
                {
                    "map_num": map_num,
                    "map_id": f"map{map_num}" if map_num else "",
                    "map_name": MAP_NAMES.get(map_num, ""),
                    "perk_id": parsed["perk_id"],
                    "perk_name": perk_name,
                    "perk_key": perk_key,
                    "is_default_perk": parsed["is_default_perk"],
                    "is_astral_group": parsed["is_astral_group"],
                    "upgrade_object_path_id": parsed["upgrade_object_path_id"],
                    **fields,
                    "base_cost": parsed["base_cost"],
                    "max_level": parsed["max_level"],
                    "base_amt": parsed["base_amt"],
                    "stat_amt": parsed["stat_amt"],
                    "wave_req": parsed["wave_req"],
                    "purpose_categories": infer_categories(perk_name, *fields.values()),
                    "source_behaviour_path_id": obj_path_id,
                    "gameobject_path_id": mono["gameobject_path_id"],
                }
            )
        else:
            parsed = parse_map_placement_cell(raw)
            bonus_name = placement_bonus_names.get(parsed["bonus_id"], "")
            upgrade = upgrade_by_path.get(parsed["upgrade_object_path_id"])
            fields = upgrade_fields(upgrade)
            if bonus_name == "empty":
                continue
            placement_rows.append(
                {
                    "bonus_id": parsed["bonus_id"],
                    "bonus_name": bonus_name,
                    "available_on_maps": "|".join(f"map{i}" for i in MAP_NAMES),
                    "upgrade_object_path_id": parsed["upgrade_object_path_id"],
                    **fields,
                    "base_cost": parsed["base_cost"],
                    "max_level": parsed["max_level"],
                    "stat_amt": parsed["stat_amt"],
                    "wave_req": parsed["wave_req"],
                    "purpose_categories": infer_categories(bonus_name, *fields.values()),
                    "source_behaviour_path_id": obj_path_id,
                    "gameobject_path_id": mono["gameobject_path_id"],
                }
            )

    perk_rows.sort(key=lambda row: (int(row["map_num"]), int(row["perk_id"])))
    placement_rows.sort(key=lambda row: int(row["bonus_id"]))

    write_csv(
        MAPS_CSV_DIR / "perks.csv",
        perk_rows,
        [
            "map_num",
            "map_id",
            "map_name",
            "perk_id",
            "perk_name",
            "perk_key",
            "is_default_perk",
            "is_astral_group",
            "upgrade_object_path_id",
            "upgrade_field_name",
            "upgrade_title",
            "upgrade_short_desc",
            "upgrade_long_desc",
            "base_cost",
            "max_level",
            "base_amt",
            "stat_amt",
            "wave_req",
            "purpose_categories",
            "source_behaviour_path_id",
            "gameobject_path_id",
        ],
    )
    write_csv(
        MAPS_CSV_DIR / "bonus_slots_posicionamento.csv",
        placement_rows,
        [
            "bonus_id",
            "bonus_name",
            "available_on_maps",
            "upgrade_object_path_id",
            "upgrade_field_name",
            "upgrade_title",
            "upgrade_short_desc",
            "upgrade_long_desc",
            "base_cost",
            "max_level",
            "stat_amt",
            "wave_req",
            "purpose_categories",
            "source_behaviour_path_id",
            "gameobject_path_id",
        ],
    )

    summary = [
        "# Map perks and placement bonuses",
        "",
        "Dados extraidos dos MonoBehaviours `MapPerkUpgradeCell` e `MapPlacementUpgradeCell`.",
        "",
        "Arquivos gerados:",
        "",
        "- `csv/perks.csv`: perks por mapa (`map1` a `map7`).",
        "- `csv/bonus_slots_posicionamento.csv`: upgrades de bonus de slot/posicionamento.",
        "",
        "Leitura:",
        "",
        "- `stat_amt` e o incremento principal por nivel do upgrade.",
        "- `base_amt` aparece em perks de mapa e representa valor base quando aplicavel.",
        "- `wave_req` e a wave exigida para desbloqueio quando o jogo define uma trava.",
        "- `map_name` usa os nomes exibidos nos textos da UI dos mapas.",
        "- Este arquivo inclui perks/upgrades extraidos de `MapPerkUpgradeCell`; os bonus fixos exibidos no painel do mapa ficam em `bonus_fixos.md`.",
        "",
        f"Total de perks de mapa: {len(perk_rows)}",
        f"Total de bonus de slot: {len(placement_rows)}",
    ]
    (MAPS_DIR / "bonus_resumo.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
