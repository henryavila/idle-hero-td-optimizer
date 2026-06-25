#!/usr/bin/env python3
"""Streamlit UI for Idle Hero TD optimizer macro output."""

from __future__ import annotations

from decimal import Decimal
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


APP_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = APP_ROOT / "scripts"
DATA_DIR = APP_ROOT / "IdleHeroTD-apk" / "apk_analysis" / "dados-consolidados"
COSTS_CSV = DATA_DIR / "formulas" / "csv" / "core_upgrade_cost_formula_classes.csv"
RUNS_DIR = APP_ROOT / "runs"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from optimize_farm_upgrades import parse_game_number  # noqa: E402

RESEARCH_KEYS = [
    *(f"researchDmg{i}" for i in range(1, 7)),
    *(f"researchKillGold{i}" for i in range(1, 7)),
    *(f"researchPrestigePower{i}" for i in range(1, 6)),
]
PRESTIGE_KEYS = [
    *(f"prestigeDmg{i}" for i in range(1, 8)),
    *(f"prestigeKillGold{i}" for i in range(1, 8)),
]
CORE_KEYS = [*RESEARCH_KEYS, *PRESTIGE_KEYS]
STATUS_OPTIONS = ["available", "locked", "maxed", "ignore", "review"]
PREVIEW_WIDTH = 420
SCREEN_ORDER = ["Research/Energy", "Prestige/PowerUps"]
SCREEN_TITLES = {
    "Research/Energy": "Research / Energy",
    "Prestige/PowerUps": "Prestige / PowerUps",
}
SCREEN_ACCENTS = {
    "Research/Energy": "#39d98a",
    "Prestige/PowerUps": "#bb86fc",
}
ROMAN_BY_TIER = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
}
SUMMARY_GROUPS = [
    ("damage", "Damage", "#ff4b4b"),
    ("kill_gold", "Kill Gold", "#f2d33d"),
    ("prestige_power", "Prestige Power", "#bb4dff"),
]


def page_setup() -> None:
    st.set_page_config(
        page_title="Idle Hero TD Optimizer",
        page_icon=None,
        layout="wide",
    )
    st.title("Idle Hero TD Optimizer")
    st.caption("Arraste os prints, confirme o estado e copie a saida para sua macro.")


def ensure_run_dir() -> Path:
    if "run_dir" not in st.session_state:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state["run_dir"] = str(RUNS_DIR / stamp)
    path = Path(st.session_state["run_dir"])
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_max_levels() -> dict[str, int]:
    if not COSTS_CSV.exists():
        return {}
    frame = pd.read_csv(COSTS_CSV)
    return {
        str(row["upgrade_key"]): int(float(row["max_level"]))
        for _, row in frame.iterrows()
        if str(row.get("upgrade_key", "")) in CORE_KEYS
    }


def label_for_key(key: str) -> str:
    replacements = [
        ("researchPrestigePower", "Research prest"),
        ("researchKillGold", "Research gold"),
        ("researchDmg", "Research dmg"),
        ("prestigeKillGold", "Prestige gold"),
        ("prestigeDmg", "Prestige dmg"),
    ]
    for prefix, label in replacements:
        if key.startswith(prefix):
            return f"{label}{key.removeprefix(prefix)}"
    return key


def screen_for_key(key: str) -> str:
    return "Research/Energy" if key.startswith("research") else "Prestige/PowerUps"


def screen_id_for_key(key: str) -> str:
    return "research-core" if key.startswith("research") else "prestige-core"


def family_and_tier(key: str) -> tuple[str, int]:
    match = re.match(r"^(researchDmg|researchKillGold|researchPrestigePower|prestigeDmg|prestigeKillGold)(\d+)$", key)
    if not match:
        return key, 0
    return match.group(1), int(match.group(2))


def summary_group_for_key(key: str) -> tuple[str, str, str]:
    if "KillGold" in key:
        return "kill_gold", "Kill Gold", "#f2d33d"
    if "PrestigePower" in key:
        return "prestige_power", "Prestige Power", "#bb4dff"
    return "damage", "Damage", "#ff4b4b"


def upgrade_display_name(key: str) -> str:
    _, tier = family_and_tier(key)
    _, label, _ = summary_group_for_key(key)
    return f"{label} {ROMAN_BY_TIER.get(tier, str(tier))}"


def save_upload(upload: Any, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(upload.getbuffer())
    return path


def run_command(args: list[str], cwd: Path = APP_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def run_ocr(
    python_bin: str,
    image_path: Path,
    output_path: Path,
    screen: str,
    engine: str,
) -> dict[str, Any]:
    cmd = [
        python_bin,
        str(SCRIPTS_DIR / "extract_upgrade_levels_from_image.py"),
        "--engine",
        engine,
        "--image",
        str(image_path),
        "--screen",
        screen,
        "--format",
        "json",
        "--output",
        str(output_path),
    ]
    result = run_command(cmd)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "OCR failed")
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    payload["screen"] = screen
    return payload


def records_by_key(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for result in results:
        for record in result.get("records", []):
            records[str(record["upgrade_key"])] = record
    return records


def looks_locked_text(text: str) -> bool:
    normalized = text.lower()
    return "wave" in normalized or "locked" in normalized or "unlock" in normalized


def detected_status(
    level: int | None,
    max_level: int | None,
    text: str,
) -> str:
    if looks_locked_text(text):
        return "locked"
    if level is None:
        return "review"
    if max_level is not None and level >= max_level:
        return "maxed"
    return "available"


def infer_missing_status(
    tier: int,
    family_detected_tiers: list[int],
    family_locked_tiers: list[int],
) -> tuple[str, str]:
    if not family_detected_tiers:
        return "review", "missing=review:no-family-anchor"

    detected = sorted(set(family_detected_tiers))
    lowest_detected = detected[0]
    highest_detected = detected[-1]

    if any(locked_tier <= tier for locked_tier in family_locked_tiers):
        return "locked", "missing=locked:after-visible-lock"
    if tier > highest_detected:
        return "locked", "missing=locked:beyond-visible-tiers"
    if tier < lowest_detected:
        contiguous_anchor = detected == list(range(lowest_detected, highest_detected + 1))
        if contiguous_anchor:
            return "maxed", "missing=maxed:before-contiguous-visible-run"
        return "review", "missing=review:non-contiguous-visible-run"
    return "review", "missing=review:ambiguous"


def build_state_rows(ocr_results: list[dict[str, Any]]) -> pd.DataFrame:
    max_levels = load_max_levels()
    records = records_by_key(ocr_results)
    loaded_screens = {str(result.get("screen")) for result in ocr_results if result.get("screen")}
    raw_rows: list[dict[str, Any]] = []
    for key in CORE_KEYS:
        detected = key in records
        screen_id = screen_id_for_key(key)
        screen_loaded = screen_id in loaded_screens
        family, tier = family_and_tier(key)
        record = records.get(key, {})
        raw_level = record.get("level")
        level = int(raw_level) if raw_level is not None else None
        max_level = max_levels.get(key)
        text = str(record.get("text", ""))
        status = detected_status(level=level, max_level=max_level, text=text) if detected else None
        raw_rows.append(
            {
                "screen": screen_for_key(key),
                "screen_id": screen_id,
                "family": family,
                "tier": tier,
                "upgrade_key": key,
                "label": label_for_key(key),
                "level": level,
                "status": status,
                "max_level": max_level,
                "detected": detected,
                "screen_loaded": screen_loaded,
                "inference": "ocr" if detected else None,
                "confidence": record.get("confidence"),
                "ocr_text": text,
            }
        )
    family_detected: dict[str, list[int]] = {}
    family_locked: dict[str, list[int]] = {}
    for row in raw_rows:
        if not row["screen_loaded"] or not row["detected"]:
            continue
        family_detected.setdefault(row["family"], []).append(row["tier"])
        if row["status"] == "locked":
            family_locked.setdefault(row["family"], []).append(row["tier"])

    rows: list[dict[str, Any]] = []
    for row in raw_rows:
        if row["detected"]:
            rows.append(row)
            continue
        if not row["screen_loaded"]:
            row["status"] = "ignore"
            row["inference"] = "not-loaded"
        else:
            status, inference = infer_missing_status(
                tier=row["tier"],
                family_detected_tiers=family_detected.get(row["family"], []),
                family_locked_tiers=family_locked.get(row["family"], []),
            )
            row["status"] = status
            row["inference"] = inference
        rows.append(row)
    return pd.DataFrame(rows)


def coerce_int(value: Any) -> int | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    return int(float(text.replace(".", "").replace(",", ".")))


def validate_resource_inputs(energy: str, prestige_points: str) -> list[str]:
    errors: list[str] = []
    parsed: dict[str, Decimal] = {}
    labels = {
        "energy": "Energy",
        "prestige_points": "Prestige Points",
    }

    for key, raw_value in (("energy", energy), ("prestige_points", prestige_points)):
        try:
            value = parse_game_number(raw_value)
        except ValueError as exc:
            errors.append(f"{labels[key]} invalido: {exc}")
            continue
        if value < 0:
            errors.append(f"{labels[key]} nao pode ser negativo.")
        parsed[key] = value

    if errors:
        return errors
    if parsed.get("energy", Decimal(0)) <= 0 and parsed.get("prestige_points", Decimal(0)) <= 0:
        errors.append("Informe Energy ou Prestige Points antes de gerar a macro. Um deles pode ficar 0, mas nao os dois.")
    return errors


def build_optimizer_state(
    rows: pd.DataFrame,
    objective: str,
    energy: str,
    prestige_points: str,
) -> tuple[dict[str, Any], list[str]]:
    levels: dict[str, int] = {}
    locked: list[str] = []
    errors: list[str] = []
    max_levels = load_max_levels()

    for _, row in rows.iterrows():
        key = str(row["upgrade_key"])
        status = str(row["status"])
        if status == "ignore":
            continue
        if status == "review":
            errors.append(f"{key}: resolva esta pendencia antes de gerar.")
            continue
        if status == "maxed":
            max_level = max_levels.get(key)
            if max_level is None:
                errors.append(f"{key}: max level desconhecido.")
                continue
            levels[key] = max_level
            continue
        level = coerce_int(row.get("level"))
        if level is None:
            if status == "locked":
                level = 0
            else:
                errors.append(f"{key}: level vazio.")
                continue
        levels[key] = level
        if status == "locked":
            locked.append(key)

    state = {
        "objective": objective,
        "resources": {
            "energy": energy,
            "prestige_points": prestige_points,
        },
        "levels": {key: levels[key] for key in sorted(levels)},
        "locked_upgrades": sorted(set(locked)),
        "warnings": [],
    }
    return state, errors


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_optimizer(
    python_bin: str,
    state_path: Path,
    result_path: Path,
    objective: str,
) -> dict[str, Any]:
    script = "optimize_gold_push_prep.py" if objective == "GOLD_PREP" else "optimize_farm_upgrades.py"
    cmd = [
        python_bin,
        str(SCRIPTS_DIR / script),
        "--state",
        str(state_path),
        "--output",
        str(result_path),
    ]
    result = run_command(cmd)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "optimizer failed")
    return json.loads(result_path.read_text(encoding="utf-8"))


def run_macro_formatter(python_bin: str, result_path: Path, output_path: Path) -> str:
    cmd = [
        python_bin,
        str(SCRIPTS_DIR / "format_optimizer_clicks.py"),
        "--result",
        str(result_path),
        "--output",
        str(output_path),
    ]
    result = run_command(cmd)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "macro formatter failed")
    return output_path.read_text(encoding="utf-8")


def split_macro_sections(macro_text: str) -> dict[str, str]:
    sections = {
        "Research/Energy": "",
        "Prestige/PowerUps": "",
    }
    current_section: str | None = None
    buffers: dict[str, list[str]] = {key: [] for key in sections}

    for raw_line in macro_text.splitlines():
        line = raw_line.strip()
        if line in {"Research/Energy:", "Prestige/PowerUps:"}:
            current_section = line.removesuffix(":")
            continue
        if current_section in buffers and line:
            buffers[current_section].append(line)

    return {
        section: "\n".join(lines) + ("\n" if lines else "")
        for section, lines in buffers.items()
    }


def generate_macro_result(
    rows: pd.DataFrame,
    objective: str,
    energy: str,
    prestige_points: str,
    python_bin: str,
    run_dir: Path,
) -> tuple[dict[str, Any] | None, str | None, list[str]]:
    resource_errors = validate_resource_inputs(energy, prestige_points)
    if resource_errors:
        return None, None, resource_errors

    state, errors = build_optimizer_state(
        rows=rows,
        objective=objective,
        energy=energy,
        prestige_points=prestige_points,
    )
    if errors:
        return None, None, errors

    state_path = run_dir / f"estado_{objective.lower()}.json"
    result_path = run_dir / f"resultado_{objective.lower()}.json"
    macro_path = run_dir / f"macro_clicks_{objective.lower()}.txt"
    write_json(state_path, state)
    result = run_optimizer(python_bin, state_path, result_path, objective)
    macro_text = run_macro_formatter(python_bin, result_path, macro_path)
    st.session_state["last_result"] = result
    st.session_state["last_objective"] = objective
    st.session_state["last_locked"] = state.get("locked_upgrades", [])
    st.session_state["last_generation_inputs"] = {
        "objective": objective,
        "energy": energy,
        "prestige_points": prestige_points,
    }
    return result, macro_text, []


def show_warnings(ocr_results: list[dict[str, Any]]) -> None:
    warnings = []
    for result in ocr_results:
        warnings.extend(result.get("warnings", []))
    if warnings:
        with st.expander("Avisos do OCR", expanded=True):
            for warning in warnings:
                st.warning(warning)


def status_label(status: str) -> str:
    return {
        "review": "Decidir",
        "available": "Disponivel",
        "locked": "Locked",
        "maxed": "Maxed",
        "ignore": "Ignorar",
    }.get(status, status)


def inference_label(inference: Any) -> str:
    text = str(inference or "")
    labels = {
        "missing=review:no-family-anchor": "sem referencia suficiente nesta familia",
        "missing=review:non-contiguous-visible-run": "buraco em sequencia visivel; pode ser OCR falho",
        "missing=review:ambiguous": "ausencia ambigua",
        "missing=maxed:before-contiguous-visible-run": "maxed inferido antes da sequencia visivel",
        "missing=locked:after-visible-lock": "locked inferido depois de tier travado",
        "missing=locked:beyond-visible-tiers": "locked inferido alem do limite visivel",
        "ocr": "lido pelo OCR",
        "not-loaded": "tela nao anexada",
    }
    return labels.get(text, text or "sem inferencia")


def update_row(merged: pd.DataFrame, key: str, status: str, level: Any) -> None:
    index = merged.index[merged["upgrade_key"] == key]
    if len(index) != 1:
        return
    merged.loc[index[0], "status"] = status
    merged.loc[index[0], "level"] = level


def review_level_default(value: Any) -> int:
    if value is None or pd.isna(value):
        return 0
    return int(value)


def level_display(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    try:
        number = int(float(value))
    except (TypeError, ValueError):
        return str(value)
    return f"{number:,}".replace(",", ".")


def status_summary(row: pd.Series) -> str:
    status = str(row["status"])
    level = level_display(row.get("level"))
    if status == "available":
        return f"Lv {level}" if level is not None else "Lv ?"
    if status == "maxed":
        return "Maxed"
    if status == "locked":
        return "Locked"
    if status == "review":
        return "Revisar"
    return status_label(status)


def screen_slug(screen: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", screen.lower()).strip("_")


def screen_counts_text(rows: pd.DataFrame) -> str:
    if rows.empty:
        return "sem itens"
    if not bool(rows["screen_loaded"].any()):
        return "print nao anexado | itens ignorados"
    counts = rows["status"].value_counts().to_dict()
    return (
        f"{counts.get('available', 0)} disponiveis | "
        f"{counts.get('locked', 0)} locked | "
        f"{counts.get('maxed', 0)} maxed | "
        f"{counts.get('review', 0)} pendencias"
    )


def screen_section_header(screen: str, rows: pd.DataFrame) -> None:
    title = SCREEN_TITLES.get(screen, screen)
    color = SCREEN_ACCENTS.get(screen, "#4ea1ff")
    st.markdown(
        f"""
        <div style="border-left: 6px solid {color}; padding: 0.35rem 0 0.35rem 0.8rem; margin: 1.2rem 0 0.7rem 0;">
            <div style="font-size: 1.25rem; font-weight: 750;">{title}</div>
            <div style="opacity: 0.72; font-size: 0.92rem;">{screen_counts_text(rows)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pending_cards(
    merged: pd.DataFrame,
    pending: pd.DataFrame,
    screen: str,
    state_version: str,
) -> None:
    title = SCREEN_TITLES.get(screen, screen)
    screen_pending = pending[pending["screen"] == screen].copy()
    screen_rows = merged[merged["screen"] == screen]

    if not bool(screen_rows["screen_loaded"].any()):
        st.caption("Print nao anexado. Os upgrades desta tela ficam como ignore.")
        return
    if screen_pending.empty:
        return

    st.info(f"{title}: resolva somente estes {len(screen_pending)} item(ns).")
    columns = st.columns(2)
    decision_options = ["review", "available", "locked", "maxed", "ignore"]
    slug = screen_slug(screen)

    for position, (_, row) in enumerate(screen_pending.iterrows()):
        key = str(row["upgrade_key"])
        with columns[position % 2]:
            with st.container(border=True):
                st.markdown(f"**{row['label']}**")
                st.caption(inference_label(row.get("inference")))
                if row.get("ocr_text"):
                    st.caption(str(row["ocr_text"])[:140])
                decision = st.selectbox(
                    "Status",
                    decision_options,
                    index=0,
                    format_func=status_label,
                    key=f"pending_status_{state_version}_{slug}_{key}",
                )
                level = row.get("level")
                if decision == "available":
                    level = st.number_input(
                        "Level",
                        min_value=0,
                        step=1,
                        value=review_level_default(row.get("level")),
                        key=f"pending_level_{state_version}_{slug}_{key}",
                    )
                elif decision == "locked":
                    level = 0 if pd.isna(level) else level
                update_row(merged, key, decision, level)


def render_state_summary(rows: pd.DataFrame) -> None:
    st.subheader("Resumo lido")
    screen_labels = {
        "Research/Energy": "ENERGIA / RESEARCH",
        "Prestige/PowerUps": "PRESTIGE / POWERUPS",
    }

    for screen in SCREEN_ORDER:
        subset = rows[(rows["screen"] == screen) & (rows["status"] != "ignore")].copy()
        subset = subset.sort_values(["family", "tier"])
        color = SCREEN_ACCENTS.get(screen, "#4ea1ff")
        st.markdown(
            f"""
            <div style="border-left: 7px solid {color}; padding: 0.25rem 0 0.25rem 0.75rem; margin: 1rem 0 0.35rem 0;">
                <div style="font-size: 1.18rem; font-weight: 850;">{screen_labels.get(screen, screen)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if subset.empty or not bool(subset["screen_loaded"].any()):
            st.caption("Print nao anexado.")
            continue

        visible_groups = []
        for group_id, group_label, color in SUMMARY_GROUPS:
            group_rows = [
                row
                for _, row in subset.iterrows()
                if summary_group_for_key(str(row["upgrade_key"]))[0] == group_id
            ]
            if group_rows:
                visible_groups.append((group_label, color, group_rows))

        group_columns = st.columns(max(len(visible_groups), 1), gap="large")
        for column, (group_label, color, group_rows) in zip(group_columns, visible_groups):
            with column:
                st.markdown(
                    f"""
                    <div style="margin: 0.15rem 0 0.25rem 0; border-left: 5px solid {color}; padding-left: 0.55rem; font-weight: 750;">
                        {group_label}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for row in sorted(group_rows, key=lambda item: int(item["tier"])):
                    name = upgrade_display_name(str(row["upgrade_key"]))
                    st.markdown(f"{name}: **{status_summary(row)}**")


def render_inference_summary(rows: pd.DataFrame) -> None:
    with st.expander("Resumo das inferencias", expanded=False):
        for screen in SCREEN_ORDER:
            subset = rows[rows["screen"] == screen]
            if subset.empty:
                continue
            inferred_maxed = int(((subset["status"] == "maxed") & (~subset["detected"])).sum())
            inferred_locked = int(((subset["status"] == "locked") & (~subset["detected"])).sum())
            visible_locked = int(((subset["status"] == "locked") & (subset["detected"])).sum())
            st.markdown(f"**{SCREEN_TITLES.get(screen, screen)}**")
            st.write(
                f"- {inferred_maxed} maxed inferidos antes de sequencias visiveis\n"
                f"- {inferred_locked} locked inferidos alem dos tiers visiveis\n"
                f"- {visible_locked} locked detectados por botao Wave/lock"
            )


def render_advanced_editor(merged: pd.DataFrame) -> None:
    with st.expander("Ajustes avancados", expanded=False):
        editor_columns = ["label", "level", "status", "confidence", "upgrade_key"]
        tabs = st.tabs([SCREEN_TITLES.get(screen, screen) for screen in SCREEN_ORDER])
        for screen, tab in zip(SCREEN_ORDER, tabs):
            with tab:
                subset = merged[merged["screen"] == screen]
                if subset.empty:
                    st.caption("Sem itens nesta tela.")
                    continue
                edited = st.data_editor(
                    subset[editor_columns],
                    use_container_width=True,
                    hide_index=True,
                    num_rows="fixed",
                    column_config={
                        "label": st.column_config.TextColumn("Upgrade", disabled=True, width="medium"),
                        "level": st.column_config.NumberColumn("Level", min_value=0, step=1, width="small"),
                        "status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTIONS, required=True, width="small"),
                        "confidence": st.column_config.NumberColumn("OCR", disabled=True, format="%.1f", width="small"),
                        "upgrade_key": st.column_config.TextColumn("Key", disabled=True),
                    },
                    disabled=["upgrade_key", "label", "confidence"],
                    key=f"advanced_state_editor_{screen_slug(screen)}",
                )
                for _, edited_row in edited.iterrows():
                    update_row(merged, str(edited_row["upgrade_key"]), str(edited_row["status"]), edited_row["level"])


def render_debug_rows(merged: pd.DataFrame) -> None:
    with st.expander("Debug OCR", expanded=False):
        detail_columns = ["label", "status", "inference", "detected", "confidence", "ocr_text", "upgrade_key"]
        tabs = st.tabs([SCREEN_TITLES.get(screen, screen) for screen in SCREEN_ORDER])
        for screen, tab in zip(SCREEN_ORDER, tabs):
            with tab:
                subset = merged[merged["screen"] == screen]
                st.dataframe(subset[detail_columns], use_container_width=True, hide_index=True)


def show_editor() -> pd.DataFrame | None:
    rows = st.session_state.get("state_rows")
    if rows is None:
        st.info("Arraste as imagens e clique em 'Ler imagens' para montar o estado.")
        return None

    merged = rows.copy()
    pending = merged[merged["status"] == "review"].copy()

    if not pending.empty:
        st.subheader("Resolver pendencias")
        st.info(f"Resolva somente os {len(pending)} item(ns) abaixo. O restante ja foi inferido pelo app.")
        state_version = st.session_state.get("state_version", "v0")
        for screen in SCREEN_ORDER:
            screen_pending = pending[pending["screen"] == screen]
            if screen_pending.empty:
                continue
            subset = merged[merged["screen"] == screen]
            screen_section_header(screen, subset)
            render_pending_cards(merged, pending, screen, state_version)

    render_state_summary(merged)
    render_inference_summary(merged)
    render_advanced_editor(merged)
    render_debug_rows(merged)

    st.session_state["state_rows"] = merged

    return merged


def show_validation_errors(errors: list[str]) -> None:
    if not errors:
        return
    st.warning(f"{len(errors)} ajuste(s) precisam ser resolvidos antes de gerar a macro.")
    with st.expander("Ver ajustes pendentes", expanded=False):
        st.write("\n".join(f"- {error}" for error in errors))


def show_upload_preview(upload: Any, caption: str) -> None:
    if upload is None:
        st.caption("Nenhum print anexado.")
        return
    st.image(upload, caption=caption, width=PREVIEW_WIDTH)


def show_upload_block(
    column_name: str,
    title: str,
    subtitle: str,
    accent: str,
    uploader_key: str,
    preview_caption: str,
) -> Any:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="border-left: 8px solid {accent}; padding: 0.1rem 0 0.2rem 0.85rem; margin-bottom: 0.85rem;">
                <div style="font-size: 0.78rem; font-weight: 800; opacity: 0.72; text-transform: uppercase;">{column_name}</div>
                <div style="font-size: 1.55rem; font-weight: 850; line-height: 1.1;">{title}</div>
                <div style="font-size: 0.95rem; opacity: 0.75; margin-top: 0.25rem;">{subtitle}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        upload = st.file_uploader(
            f"Arquivo de {title}",
            type=["png", "jpg", "jpeg"],
            key=uploader_key,
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown(f"**Preview: {title}**")
        show_upload_preview(upload, preview_caption)
        return upload


def render_copy_button(text: str, key: str, label: str = "Copiar") -> None:
    disabled = not bool(text.strip())
    button_id = f"copy_{key}"
    message_id = f"copy_msg_{key}"
    payload = json.dumps(text)
    disabled_attr = "disabled" if disabled else ""
    components.html(
        f"""
        <button id="{button_id}" {disabled_attr} style="
            border: 1px solid rgba(250, 250, 250, 0.25);
            border-radius: 0.45rem;
            background: {'rgba(80, 80, 90, 0.35)' if disabled else '#2563eb'};
            color: white;
            font-weight: 700;
            padding: 0.48rem 0.8rem;
            cursor: {'not-allowed' if disabled else 'pointer'};
        ">{label}</button>
        <span id="{message_id}" style="margin-left: 0.6rem; font: 14px sans-serif; color: #39d98a;"></span>
        <script>
        const button = document.getElementById({json.dumps(button_id)});
        const message = document.getElementById({json.dumps(message_id)});
        if (button && !button.disabled) {{
            button.addEventListener("click", async () => {{
                try {{
                    await navigator.clipboard.writeText({payload});
                    message.textContent = "Copiado";
                    setTimeout(() => message.textContent = "", 1800);
                }} catch (error) {{
                    message.style.color = "#ff6b6b";
                    message.textContent = "Falha ao copiar";
                }}
            }});
        }}
        </script>
        """,
        height=48,
    )


def render_result(result: dict[str, Any], macro_text: str, run_dir: Path) -> None:
    st.subheader("Codigo para macro")
    sections = split_macro_sections(macro_text)
    macro_left, macro_right = st.columns(2, gap="large")
    with macro_left:
        st.markdown("#### ENERGIA / RESEARCH")
        research_text = sections.get("Research/Energy", "")
        st.text_area(
            "Copiar macro de Energy",
            research_text,
            height=180,
            placeholder="Nenhum upgrade de Energy recomendado.",
        )
        render_copy_button(research_text, "energy_macro", "Copiar Energy")
        st.download_button(
            "Baixar Energy .txt",
            data=research_text,
            file_name="macro_energy_research.txt",
            mime="text/plain",
            disabled=not bool(research_text.strip()),
        )
    with macro_right:
        st.markdown("#### PRESTIGE / POWERUPS")
        prestige_text = sections.get("Prestige/PowerUps", "")
        st.text_area(
            "Copiar macro de Prestige",
            prestige_text,
            height=180,
            placeholder="Nenhum upgrade de Prestige recomendado.",
        )
        render_copy_button(prestige_text, "prestige_macro", "Copiar Prestige")
        st.download_button(
            "Baixar Prestige .txt",
            data=prestige_text,
            file_name="macro_prestige_powerups.txt",
            mime="text/plain",
            disabled=not bool(prestige_text.strip()),
        )

    with st.expander("Macro combinada", expanded=False):
        st.text_area("Copiar tudo", macro_text, height=220)
        render_copy_button(macro_text, "combined_macro", "Copiar tudo")
        st.download_button(
            "Baixar macro completa .txt",
            data=macro_text,
            file_name="macro_clicks.txt",
            mime="text/plain",
        )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Recursos**")
        st.json(result.get("resources", {}), expanded=False)
    with col_b:
        st.markdown("**Multiplicadores**")
        st.json(result.get("factors", {}), expanded=False)

    purchases = result.get("purchases", [])
    if purchases:
        st.markdown("**Compras recomendadas**")
        st.dataframe(pd.DataFrame(purchases), use_container_width=True, hide_index=True)

    st.caption(f"Artefatos salvos em: {run_dir}")


def main() -> None:
    page_setup()
    run_dir = ensure_run_dir()

    with st.sidebar:
        st.header("Configuracao")
        python_bin = st.text_input("Python dos scripts", os.environ.get("IDLE_HERO_PYTHON", sys.executable))
        engine = st.selectbox("OCR engine", ["auto", "vision", "easyocr", "tesseract"], index=0)
        objective = st.radio("Objetivo", ["FARM", "GOLD_PREP"], horizontal=True)
        energy = st.text_input("Energy", "0")
        prestige_points = st.text_input("Prestige Points", "0")
        st.caption("Use escala do jogo: 2,59M, 1,21e20, 850K.")

    st.markdown("### Prints de entrada")
    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        research_upload = show_upload_block(
            column_name="Coluna esquerda",
            title="ENERGIA / RESEARCH",
            subtitle="Use o print da aba Upgrades > Research. Consome Energy.",
            accent=SCREEN_ACCENTS["Research/Energy"],
            uploader_key="research_upload",
            preview_caption="Energia / Research",
        )
    with col_right:
        prestige_upload = show_upload_block(
            column_name="Coluna direita",
            title="PRESTIGE / POWERUPS",
            subtitle="Use o print da aba Upgrades > Prestige. Consome Prestige Points.",
            accent=SCREEN_ACCENTS["Prestige/PowerUps"],
            uploader_key="prestige_upload",
            preview_caption="Prestige / PowerUps",
        )

    action_col, hint_col = st.columns([1, 3])
    with action_col:
        process_button_slot = st.empty()
        process_images = process_button_slot.button(
            "Ler imagens",
            type="primary",
            disabled=research_upload is None and prestige_upload is None,
            use_container_width=True,
            key="process_images_button",
        )
    with hint_col:
        st.caption("O app infere pela ordem dos tiers: ausente antes de uma sequencia visivel = maxed; ausente depois do limite visivel = locked.")

    ocr_notice = st.session_state.pop("ocr_notice", None)
    if ocr_notice:
        st.caption(str(ocr_notice))
    ocr_error = st.session_state.pop("ocr_error", None)
    if ocr_error:
        st.error(str(ocr_error))

    if process_images:
        process_button_slot.button(
            "Processando imagens...",
            type="primary",
            disabled=True,
            use_container_width=True,
            key="process_images_busy_button",
        )
        ocr_results: list[dict[str, Any]] = []
        with st.status("Processando imagens...", expanded=True) as status:
            try:
                if research_upload is not None:
                    st.write("Salvando e lendo Energia / Research...")
                    image_path = save_upload(research_upload, run_dir / "uploads" / research_upload.name)
                    ocr_results.append(
                        run_ocr(
                            python_bin=python_bin,
                            image_path=image_path,
                            output_path=run_dir / "research_ocr.json",
                            screen="research-core",
                            engine=engine,
                        )
                    )
                if prestige_upload is not None:
                    st.write("Salvando e lendo Prestige / PowerUps...")
                    image_path = save_upload(prestige_upload, run_dir / "uploads" / prestige_upload.name)
                    ocr_results.append(
                        run_ocr(
                            python_bin=python_bin,
                            image_path=image_path,
                            output_path=run_dir / "prestige_ocr.json",
                            screen="prestige-core",
                            engine=engine,
                        )
                    )
                if not ocr_results:
                    status.update(label="Nenhuma imagem anexada.", state="error", expanded=True)
                    st.session_state["ocr_error"] = "Anexe pelo menos uma imagem."
                else:
                    st.write("Montando estado dos upgrades...")
                    st.session_state["ocr_results"] = ocr_results
                    st.session_state["state_rows"] = build_state_rows(ocr_results)
                    st.session_state["state_version"] = datetime.now().strftime("%H%M%S%f")
                    st.session_state["last_macro_text"] = None
                    st.session_state["last_result"] = None
                    st.session_state["last_objective"] = None
                    st.session_state["last_locked"] = []
                    st.session_state["last_generation_inputs"] = None
                    st.session_state["auto_generate_macro"] = True
                    status.update(label="OCR concluido.", state="complete", expanded=False)
                    st.session_state["ocr_notice"] = "OCR concluido."
            except Exception as exc:
                status.update(label="Falha ao processar imagens.", state="error", expanded=True)
                st.session_state["ocr_error"] = str(exc)
        st.rerun()

    ocr_results = st.session_state.get("ocr_results", [])
    show_warnings(ocr_results)
    edited_rows = show_editor()

    if edited_rows is not None:
        has_pending = bool((edited_rows["status"] == "review").any())
        should_auto_generate = bool(st.session_state.pop("auto_generate_macro", False))
        current_generation_inputs = {
            "objective": objective,
            "energy": energy,
            "prestige_points": prestige_points,
        }
        resource_errors = validate_resource_inputs(energy, prestige_points)
        macro_stale = (
            bool(st.session_state.get("last_macro_text"))
            and st.session_state.get("last_generation_inputs") != current_generation_inputs
        )

        if resource_errors:
            show_validation_errors(resource_errors)

        if should_auto_generate and not has_pending and not resource_errors:
            with st.status("Gerando macros automaticamente...", expanded=True) as status:
                try:
                    st.write("Rodando otimizador...")
                    result, macro_text, errors = generate_macro_result(
                        rows=edited_rows,
                        objective=objective,
                        energy=energy,
                        prestige_points=prestige_points,
                        python_bin=python_bin,
                        run_dir=run_dir,
                    )
                    if errors:
                        status.update(label="Nao foi possivel gerar a macro.", state="error", expanded=True)
                        show_validation_errors(errors)
                    elif result is not None and macro_text is not None:
                        st.session_state["last_macro_text"] = macro_text
                        status.update(label="Macros geradas.", state="complete", expanded=False)
                except Exception as exc:
                    status.update(label="Falha ao gerar macros.", state="error", expanded=True)
                    st.error(str(exc))
        elif should_auto_generate and has_pending:
            st.info("A macro nao foi gerada automaticamente porque ainda existem pendencias de OCR.")
        elif should_auto_generate and resource_errors:
            st.info("A macro nao foi gerada automaticamente porque os recursos ainda nao foram informados.")

        if macro_stale:
            st.warning("Energy, Prestige Points ou objetivo mudaram. Clique em `Recalcular macro` para atualizar os codigos sem reprocessar as imagens.")

        if st.session_state.get("last_macro_text"):
            macro_button_label = "Recalcular macro" if macro_stale else "Atualizar macro"
        else:
            macro_button_label = "Gerar macro"
        macro_button_slot = st.empty()
        run_macro = macro_button_slot.button(
            macro_button_label,
            disabled=has_pending or bool(resource_errors),
            type="primary",
            key="generate_macro_button",
        )
        if run_macro:
            macro_button_slot.button(
                "Gerando macro...",
                disabled=True,
                type="primary",
                key="generate_macro_busy_button",
            )
            with st.status("Gerando macro...", expanded=True) as status:
                try:
                    st.write("Validando recursos e levels...")
                    st.write("Rodando otimizador...")
                    result, macro_text, errors = generate_macro_result(
                        rows=edited_rows,
                        objective=objective,
                        energy=energy,
                        prestige_points=prestige_points,
                        python_bin=python_bin,
                        run_dir=run_dir,
                    )
                    if errors:
                        status.update(label="Nao foi possivel gerar a macro.", state="error", expanded=True)
                        show_validation_errors(errors)
                    elif result is not None and macro_text is not None:
                        st.session_state["last_macro_text"] = macro_text
                        status.update(label="Macro gerada.", state="complete", expanded=False)
                except Exception as exc:
                    status.update(label="Falha ao gerar macro.", state="error", expanded=True)
                    st.error(str(exc))

        stored_result = st.session_state.get("last_result")
        stored_macro_text = st.session_state.get("last_macro_text")
        if stored_result is not None and stored_macro_text:
            render_result(stored_result, stored_macro_text, run_dir)

    st.divider()
    st.subheader("Passada residual")
    st.caption("Use depois de executar a macro principal e ver sobra real na UI do jogo.")
    residual_col_a, residual_col_b = st.columns(2)
    with residual_col_a:
        residual_energy = st.text_input("Energy residual", "0")
    with residual_col_b:
        residual_prestige = st.text_input("Prestige residual", "0")

    if st.button("Gerar macro residual"):
        last_result = st.session_state.get("last_result")
        if not last_result:
            st.error("Gere uma macro principal primeiro nesta sessao.")
        else:
            try:
                residual_objective = st.session_state.get("last_objective", "FARM")
                residual_state = {
                    "objective": residual_objective,
                    "resources": {
                        "energy": residual_energy,
                        "prestige_points": residual_prestige,
                    },
                    "levels": last_result["final_levels"],
                    "locked_upgrades": last_result.get("diagnostics", {}).get("locked_upgrades", []),
                    "warnings": ["post-macro residual pass from UI"],
                }
                state_path = run_dir / f"estado_residual_{residual_objective.lower()}.json"
                result_path = run_dir / f"resultado_residual_{residual_objective.lower()}.json"
                macro_path = run_dir / f"macro_clicks_residual_{residual_objective.lower()}.txt"
                write_json(state_path, residual_state)
                result = run_optimizer(python_bin, state_path, result_path, residual_objective)
                macro_text = run_macro_formatter(python_bin, result_path, macro_path)
                render_result(result, macro_text, run_dir)
            except Exception as exc:
                st.error(str(exc))


if __name__ == "__main__":
    main()
