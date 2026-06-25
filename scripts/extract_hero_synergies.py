#!/usr/bin/env python3
"""Extract Idle Hero TD hero synergy requirements from Unity MonoBehaviour data."""

from __future__ import annotations

import csv
import re
import struct
from pathlib import Path
from typing import Any

import UnityPy

from synergy_values import SynergyValueCalculator, format_bonus_value


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = PROJECT_ROOT / "IdleHeroTD-apk" / "apk_analysis"
ASSETS_DIR = ANALYSIS_DIR / "dados-brutos" / "extracted" / "base" / "assets"
HEROES_DIR = ANALYSIS_DIR / "dados-consolidados" / "herois"
HEROES_CSV_DIR = HEROES_DIR / "csv"
SCRIPT_DIR = ANALYSIS_DIR / "scripts-extraidos" / "il2cpp" / "Cpp2IL-diffable-cs" / "DiffableCs" / "Assembly-CSharp"

HERO_SCRIPT_PATH_ID = 1967

SYNERGY_GROUPS = {
    1: ["synergyHero1"],
    2: ["synergyHero2_1", "synergyHero2_2"],
    3: ["synergyHero3"],
    4: ["synergyHero4_1", "synergyHero4_2"],
    5: ["synergyHero5"],
    6: ["synergyHero6_1", "synergyHero6_2"],
    7: ["synergyHero7"],
    8: ["synergyHero8_1", "synergyHero8_2"],
    9: ["synergyHero9"],
    10: ["synergyHero10_1", "synergyHero10_2"],
    11: ["synergyHero11"],
    12: ["synergyHero12_1", "synergyHero12_2"],
    13: ["synergyHero13"],
    14: ["synergyHero14_1", "synergyHero14_2"],
    15: ["synergyHero15_1", "synergyHero15_2", "synergyHero15_3"],
    16: ["synergyHero16_1", "synergyHero16_2", "synergyHero16_3"],
}

SYNERGY_REF_FIELDS = [field for fields in SYNERGY_GROUPS.values() for field in fields]
SYNERGY_REQUIRED_RANKS = [0, 15, 50, 100, 150, 250, 500, 1000, 1500]


def synergy_tier(synergy_num: int) -> int:
    return (synergy_num + 1) // 2


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

    def f32(self) -> float:
        value = struct.unpack_from("<f", self.data, self.offset)[0]
        self.offset += 4
        return value

    def pptr_base(self) -> tuple[int, int]:
        file_id = self.i32()
        path_id = self.i64()
        return file_id, path_id

    def pptr_hero_synergy(self) -> tuple[int, int]:
        # In this Hero block the Unity object reference is stored as:
        # path_id int64, then file_id int32. The earlier base references use
        # the usual file_id + path_id order, so keep this separate.
        path_id = self.i64()
        file_id = self.i32()
        return file_id, path_id

    def pptr_hero_synergy_final(self) -> tuple[int, int]:
        # The final synergyHero16_3 reference is stored as just path_id int64.
        # Reading a trailing file_id would shift every synergyUpgrade by 4 bytes.
        return 0, self.i64()

    def string(self) -> str:
        length = self.i32()
        value = self.data[self.offset : self.offset + length].decode("utf-8", errors="replace")
        self.offset += length
        self.align4()
        return value

    def skip_obscured_int(self) -> None:
        # Serialized ACTk ObscuredInt layout in this build is 5 int32 fields.
        self.offset += 20

    def skip_obscured_float(self) -> None:
        # Serialized ACTk ObscuredFloat layout in this build is 36 bytes.
        self.offset += 36


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


def parse_hero(raw: bytes) -> dict[str, Any]:
    r = Reader(raw)
    hero: dict[str, Any] = {}

    hero["m_GameObject"] = r.pptr_base()
    hero["m_Enabled"] = r.i32()
    hero["m_Script"] = r.pptr_base()
    hero["m_Name"] = r.string()

    hero["isPrefab"] = r.i32()
    hero["prefabHero"] = r.pptr_base()
    hero["heroId"] = r.i32()
    hero["heroClass"] = r.i32()
    hero["heroIconHead"] = r.pptr_base()
    hero["heroIconFull"] = r.pptr_base()
    hero["heroName"] = r.string()
    hero["heroRarity"] = r.i32()
    hero["pronoun"] = r.string()
    hero["backstory"] = r.string()

    r.skip_obscured_int()
    r.skip_obscured_float()
    r.skip_obscured_float()
    r.skip_obscured_float()
    r.skip_obscured_int()
    hero["skillTitle"] = r.string()
    r.skip_obscured_float()
    r.skip_obscured_float()
    hero["skillPowerBonusEffect"] = r.string()
    hero["skillDurationTimeEffect"] = r.f32()
    hero["skillMasteryBaseReqVal"] = r.i32()

    milestone_count = r.i32()
    hero["milestoneUpgrades"] = [r.i32() for _ in range(milestone_count)]
    hero["milestoneCount"] = r.i32()

    synergy_refs: dict[str, tuple[int, int]] = {}
    for index, field in enumerate(SYNERGY_REF_FIELDS):
        # In this build all synergy references except the last one use the
        # unusual path_id + file_id layout. The final synergyHero16_3 field
        # stores only path_id int64.
        if index == len(SYNERGY_REF_FIELDS) - 1:
            synergy_refs[field] = r.pptr_hero_synergy_final()
        else:
            synergy_refs[field] = r.pptr_hero_synergy()
    hero["synergyRefs"] = synergy_refs
    hero["synergyUpgrades"] = [r.i32() for _ in range(16)]
    return hero


def main() -> int:
    heroes_csv = HEROES_CSV_DIR / "detalhes_herois.csv"
    hero_rows = read_csv(heroes_csv)
    hero_by_path = {int(row["hero_behaviour_path_id"]): row for row in hero_rows}

    hero_upgrade_names = parse_enum(SCRIPT_DIR / "HeroUpgrade.cs")
    synergy_value_calculator = SynergyValueCalculator()
    env = load_unity_env()
    objects_by_path = {obj.path_id: obj for obj in env.objects}

    parsed_heroes: list[dict[str, Any]] = []
    for row in hero_rows:
        path_id = int(row["hero_behaviour_path_id"])
        obj = objects_by_path[path_id]
        parsed = parse_hero(obj.get_raw_data())

        expected_milestones = row["milestone_upgrades"]
        actual_milestones = "|".join(str(x) for x in parsed["milestoneUpgrades"])
        if actual_milestones != expected_milestones:
            raise RuntimeError(f"Parser validation failed for {row['hero_name']} milestones")
        if str(parsed["heroId"]) != row["hero_id"] or parsed["heroName"] != row["hero_name"]:
            raise RuntimeError(f"Parser validation failed for {row['hero_name']} identity")

        parsed_heroes.append({**parsed, "sourceRow": row, "heroBehaviourPathId": path_id})

    synergy_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    matrix_rows: list[dict[str, Any]] = []

    for hero in sorted(parsed_heroes, key=lambda h: h["heroId"]):
        source_row = hero["sourceRow"]
        upgrades = hero["synergyUpgrades"]
        matrix_row: dict[str, Any] = {
            "hero_id": source_row["hero_id"],
            "hero_name": source_row["hero_name"],
            "hero_class": source_row["hero_class"],
            "hero_rarity": source_row["hero_rarity"],
        }
        for synergy_num, fields in SYNERGY_GROUPS.items():
            tier = synergy_tier(synergy_num)
            rank_required = SYNERGY_REQUIRED_RANKS[tier - 1]
            required_rows = []
            required_path_ids = []
            missing_refs = []
            for field in fields:
                file_id, path_id = hero["synergyRefs"][field]
                required_path_ids.append(path_id)
                target = hero_by_path.get(path_id)
                if not target:
                    missing_refs.append(f"{field}:{file_id}:{path_id}")
                    continue
                required_rows.append(target)
                edge_rows.append(
                    {
                        "hero_id": source_row["hero_id"],
                        "hero_name": source_row["hero_name"],
                        "hero_class": source_row["hero_class"],
                        "hero_rarity": source_row["hero_rarity"],
                        "synergy_num": synergy_num,
                        "tier": tier,
                        "rank_required": rank_required,
                        "required_slot": field,
                        "required_hero_id": target["hero_id"],
                        "required_hero_name": target["hero_name"],
                        "required_hero_class": target["hero_class"],
                        "required_hero_rarity": target["hero_rarity"],
                        "required_hero_path_id": path_id,
                    }
                )

            upgrade_id = upgrades[synergy_num - 1]
            upgrade_name = hero_upgrade_names.get(upgrade_id, "")
            base_bonus_value = synergy_value_calculator.base_value(upgrade_id, synergy_num)
            base_bonus_raw = synergy_value_calculator.base_value_raw(upgrade_id, synergy_num)
            base_bonus_text = format_bonus_value(base_bonus_value, upgrade_name)
            synergy_rows.append(
                {
                    "hero_id": source_row["hero_id"],
                    "hero_name": source_row["hero_name"],
                    "hero_class": source_row["hero_class"],
                    "hero_rarity": source_row["hero_rarity"],
                    "synergy_num": synergy_num,
                    "tier": tier,
                    "rank_required": rank_required,
                    "required_count_excluding_self": len(required_rows),
                    "active_heroes_needed_including_self": len(required_rows) + 1,
                    "required_hero_ids": "|".join(row["hero_id"] for row in required_rows),
                    "required_hero_names": "|".join(row["hero_name"] for row in required_rows),
                    "required_hero_classes": "|".join(row["hero_class"] for row in required_rows),
                    "required_hero_rarities": "|".join(row["hero_rarity"] for row in required_rows),
                    "required_hero_path_ids": "|".join(str(pid) for pid in required_path_ids),
                    "synergy_upgrade_id": upgrade_id,
                    "synergy_upgrade_name": upgrade_name,
                    "base_bonus_value": base_bonus_value,
                    "base_bonus_raw": base_bonus_raw,
                    "base_bonus_text": base_bonus_text,
                    "missing_refs": "|".join(missing_refs),
                }
            )
            matrix_row[f"synergy_{synergy_num:02d}_required_heroes"] = "|".join(
                row["hero_name"] for row in required_rows
            )
            matrix_row[f"synergy_{synergy_num:02d}_required_hero_ids"] = "|".join(
                row["hero_id"] for row in required_rows
            )
            matrix_row[f"synergy_{synergy_num:02d}_tier"] = tier
            matrix_row[f"synergy_{synergy_num:02d}_rank_required"] = rank_required
            matrix_row[f"synergy_{synergy_num:02d}_upgrade"] = upgrade_name
            matrix_row[f"synergy_{synergy_num:02d}_base_bonus"] = base_bonus_text
        matrix_rows.append(matrix_row)

    write_csv(
        HEROES_CSV_DIR / "sinergias_mapa.csv",
        synergy_rows,
        [
            "hero_id",
            "hero_name",
            "hero_class",
            "hero_rarity",
            "synergy_num",
            "tier",
            "rank_required",
            "required_count_excluding_self",
            "active_heroes_needed_including_self",
            "required_hero_ids",
            "required_hero_names",
            "required_hero_classes",
            "required_hero_rarities",
            "required_hero_path_ids",
            "synergy_upgrade_id",
            "synergy_upgrade_name",
            "base_bonus_value",
            "base_bonus_raw",
            "base_bonus_text",
            "missing_refs",
        ],
    )
    write_csv(
        HEROES_CSV_DIR / "sinergias_arestas.csv",
        edge_rows,
        [
            "hero_id",
            "hero_name",
            "hero_class",
            "hero_rarity",
            "synergy_num",
            "tier",
            "rank_required",
            "required_slot",
            "required_hero_id",
            "required_hero_name",
            "required_hero_class",
            "required_hero_rarity",
            "required_hero_path_id",
        ],
    )
    matrix_fields = ["hero_id", "hero_name", "hero_class", "hero_rarity"]
    for synergy_num in SYNERGY_GROUPS:
        matrix_fields.extend(
            [
                f"synergy_{synergy_num:02d}_required_heroes",
                f"synergy_{synergy_num:02d}_required_hero_ids",
                f"synergy_{synergy_num:02d}_tier",
                f"synergy_{synergy_num:02d}_rank_required",
                f"synergy_{synergy_num:02d}_upgrade",
                f"synergy_{synergy_num:02d}_base_bonus",
            ]
        )
    write_csv(
        HEROES_CSV_DIR / "sinergias_matriz.csv",
        matrix_rows,
        matrix_fields,
    )

    summary = [
        "# Hero synergy map",
        "",
        "Mapa completo de sinergias extraido dos MonoBehaviours `Hero` do Unity.",
        "",
        "Arquivos gerados:",
        "",
        "- `csv/sinergias_mapa.csv`: uma linha por heroi e numero de sinergia.",
        "- `csv/sinergias_arestas.csv`: uma linha por relacao heroi -> parceiro exigido.",
        "- `csv/sinergias_matriz.csv`: uma linha por heroi, com as 16 sinergias em colunas.",
        "",
        "Leitura:",
        "",
        "- `required_hero_names` lista os parceiros exigidos alem do proprio heroi.",
        "- `active_heroes_needed_including_self` inclui o proprio heroi na contagem.",
        "- `tier` agrupa duas sinergias por tier; `rank_required` e o rank minimo de todos os herois exigidos.",
        "- `synergy_upgrade_name` e o efeito aplicado quando a sinergia esta ativa.",
        "- `base_bonus_text` e o valor base estatico calculado do APK antes de modificadores dinamicos de save/mapa/slot.",
        "",
        f"Total de herois: {len(parsed_heroes)}",
        f"Total de sinergias: {len(synergy_rows)}",
        f"Total de arestas/parceiros exigidos: {len(edge_rows)}",
        f"Total de linhas na matriz: {len(matrix_rows)}",
    ]
    (HEROES_DIR / "sinergias_resumo.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
