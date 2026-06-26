#!/usr/bin/env python3
"""Streamlit UI for Idle Hero TD optimizer macro output."""

from __future__ import annotations

import base64
from decimal import Decimal
import hashlib
import html as html_lib
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
USER_STATE_DIR = APP_ROOT / "user_state"
LOCKED_UPGRADES_PATH = USER_STATE_DIR / "locked_upgrades.json"

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
THUMBNAIL_WIDTH = 220
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
PYTHON_CANDIDATES = (
    ".venv/bin/python",
    ".venv/bin/python3",
    ".venv/Scripts/python.exe",
    "bin/python",
    "bin/python3",
    "Scripts/python.exe",
    "python",
    "python3",
    "python.exe",
)


def page_setup() -> None:
    st.set_page_config(
        page_title="Idle Hero TD Optimizer",
        page_icon=None,
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1760px;
        }
        .block-container h1 {
            font-size: 2.35rem;
            line-height: 1.08;
            margin-bottom: 0.35rem;
        }
        [data-testid="stFileUploaderDropzone"] {
            min-height: 4.5rem;
            padding: 0.55rem 0.75rem;
        }
        [data-testid="stFileUploaderDropzone"] > div {
            padding: 0;
        }
        [data-testid="stTextArea"] textarea {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
            font-size: 0.88rem;
            line-height: 1.35;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("Idle Hero TD Optimizer")
    st.caption("Arraste os prints, informe os recursos e copie a macro gerada no topo.")


def ensure_run_dir() -> Path:
    if "run_dir" not in st.session_state:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state["run_dir"] = str(RUNS_DIR / stamp)
    path = Path(st.session_state["run_dir"])
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_python_folder() -> str:
    python_path = Path(os.environ.get("IDLE_HERO_PYTHON", sys.executable)).expanduser()
    if python_path.exists() and python_path.is_dir():
        return str(python_path)
    return str(python_path.parent if python_path.name else APP_ROOT)


def choose_folder_dialog(initial_dir: str) -> str | None:
    if sys.platform == "darwin":
        script = """
        on run argv
            set initialPath to item 1 of argv
            try
                set chosenFolder to choose folder with prompt "Selecione a pasta do Python" default location POSIX file initialPath
                return POSIX path of chosenFolder
            on error number -128
                return ""
            on error
                try
                    set chosenFolder to choose folder with prompt "Selecione a pasta do Python"
                    return POSIX path of chosenFolder
                on error number -128
                    return ""
                end try
            end try
        end run
        """
        result = subprocess.run(
            ["osascript", "-e", script, initial_dir],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            path = result.stdout.strip()
            return path or None
        raise RuntimeError(result.stderr.strip() or "Nao foi possivel abrir o seletor de pasta.")

    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception as exc:
        raise RuntimeError("Seletor de pasta indisponivel neste ambiente.") from exc

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        path = filedialog.askdirectory(initialdir=initial_dir, title="Selecione a pasta do Python")
        return path or None
    finally:
        root.destroy()


def resolve_python_from_folder(folder: str) -> tuple[str, str | None]:
    folder_path = Path(folder).expanduser()
    if folder_path.is_file():
        return str(folder_path), None

    if not folder_path.exists():
        return sys.executable, f"Pasta nao encontrada: {folder}"

    for candidate in PYTHON_CANDIDATES:
        candidate_path = folder_path / candidate
        if candidate_path.exists() and candidate_path.is_file():
            return str(candidate_path), None

    return sys.executable, "Python nao encontrado nesta pasta. Usando o Python atual do app."


def render_python_folder_selector() -> str:
    if "python_folder" not in st.session_state:
        st.session_state["python_folder"] = default_python_folder()

    selected_folder = str(st.session_state["python_folder"])
    select_col, reset_col = st.columns([2, 1])
    with select_col:
        if st.button("Selecionar pasta do Python", width="stretch"):
            try:
                chosen_folder = choose_folder_dialog(selected_folder)
                if chosen_folder:
                    st.session_state["python_folder"] = chosen_folder
                    selected_folder = chosen_folder
            except Exception as exc:
                st.warning(str(exc))
    with reset_col:
        if st.button("Atual", width="stretch"):
            selected_folder = default_python_folder()
            st.session_state["python_folder"] = selected_folder

    python_bin, warning = resolve_python_from_folder(selected_folder)
    st.caption("Pasta selecionada")
    st.code(selected_folder, language=None)
    st.caption("Python detectado")
    st.code(python_bin, language=None)
    if warning:
        st.warning(warning)
    return python_bin


def load_max_levels() -> dict[str, int]:
    if not COSTS_CSV.exists():
        return {}
    frame = pd.read_csv(COSTS_CSV)
    return {
        str(row["upgrade_key"]): int(float(row["max_level"]))
        for _, row in frame.iterrows()
        if str(row.get("upgrade_key", "")) in CORE_KEYS
    }


def normalize_manual_locked(keys: Any) -> list[str]:
    if isinstance(keys, dict):
        keys = keys.get("locked_upgrades", [])
    if not isinstance(keys, (list, set, tuple)):
        return []
    return sorted({str(key) for key in keys if str(key) in CORE_KEYS})


def load_manual_locked(path: Path = LOCKED_UPGRADES_PATH) -> set[str]:
    if not path.exists():
        return set()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return set(normalize_manual_locked(payload))


def save_manual_locked(keys: set[str], path: Path = LOCKED_UPGRADES_PATH) -> None:
    locked = normalize_manual_locked(keys)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "locked_upgrades": locked,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
    if engine == "paddle":
        cmd.extend(["--strategy", "auto-lines"])
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
    if level is None:
        return "review"
    if level == 0 and looks_locked_text(text):
        return "review"
    if max_level is not None and level >= max_level:
        return "maxed"
    return "available"


def infer_missing_status(
    tier: int,
    family_detected_tiers: list[int],
) -> tuple[str, str]:
    if not family_detected_tiers:
        return "review", "missing=review:no-family-anchor"

    detected = sorted(set(family_detected_tiers))
    lowest_detected = detected[0]
    highest_detected = detected[-1]

    if tier > highest_detected:
        return "review", "missing=review:beyond-visible-tiers"
    if tier < lowest_detected:
        contiguous_anchor = detected == list(range(lowest_detected, highest_detected + 1))
        if contiguous_anchor:
            return "maxed", "missing=maxed:before-contiguous-visible-run"
        return "review", "missing=review:non-contiguous-visible-run"
    return "review", "missing=review:ambiguous"


def apply_manual_locked(rows: pd.DataFrame, manual_locked: set[str]) -> pd.DataFrame:
    if rows.empty:
        return rows
    result = rows.copy()
    if "ocr_level" not in result.columns:
        result["ocr_level"] = result["level"]
    if "ocr_status" not in result.columns:
        result["ocr_status"] = result["status"]
    result["manual_locked"] = result["upgrade_key"].astype(str).isin(manual_locked)
    locked_mask = result["manual_locked"]
    result.loc[locked_mask, "status"] = "locked"
    result.loc[locked_mask, "level"] = 0
    result.loc[locked_mask, "inference"] = "manual=locked"
    return result


def build_state_rows(
    ocr_results: list[dict[str, Any]],
    manual_locked: set[str] | None = None,
) -> pd.DataFrame:
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
                "ocr_level": level,
                "ocr_status": status,
                "max_level": max_level,
                "detected": detected,
                "screen_loaded": screen_loaded,
                "inference": "ocr" if detected else None,
                "manual_locked": False,
                "confidence": record.get("confidence"),
                "ocr_text": text,
            }
        )
    family_detected: dict[str, list[int]] = {}
    for row in raw_rows:
        if not row["screen_loaded"] or not row["detected"]:
            continue
        family_detected.setdefault(row["family"], []).append(row["tier"])

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
            )
            row["status"] = status
            row["ocr_status"] = status
            row["inference"] = inference
        rows.append(row)
    return apply_manual_locked(pd.DataFrame(rows), manual_locked or set())


def coerce_int(value: Any) -> int | None:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (int, float, Decimal)) and not isinstance(value, bool):
        numeric = Decimal(str(value))
        if numeric == numeric.to_integral_value():
            return int(numeric)
        return None

    text = str(value).strip()
    if not text:
        return None
    compact = text.replace("_", "").replace(" ", "")
    if re.fullmatch(r"[+-]?\d+", compact):
        return int(compact)
    if re.fullmatch(r"[+-]?\d+[.,]0+", compact):
        return int(Decimal(compact.replace(",", ".")))
    if re.fullmatch(r"[+-]?\d+(?:[.,]\d{3})+", compact):
        return int(compact.replace(".", "").replace(",", ""))
    return None


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


def rows_state_fingerprint(rows: pd.DataFrame) -> str:
    payload = []
    for _, row in rows.sort_values("upgrade_key").iterrows():
        payload.append(
            {
                "upgrade_key": str(row["upgrade_key"]),
                "status": str(row["status"]),
                "level": coerce_int(row.get("level")),
            }
        )
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


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
        "rows": rows_state_fingerprint(rows),
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
        "missing=review:beyond-visible-tiers": "ausente alem dos tiers visiveis",
        "missing=review:ambiguous": "ausencia ambigua",
        "missing=maxed:before-contiguous-visible-run": "maxed inferido antes da sequencia visivel",
        "missing=locked:after-visible-lock": "locked inferido depois de tier travado",
        "missing=locked:beyond-visible-tiers": "locked inferido alem do limite visivel",
        "manual=locked": "bloqueio manual salvo",
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


def manual_locked_conflicts(rows: pd.DataFrame, manual_locked: set[str]) -> list[str]:
    conflicts = []
    for _, row in rows.iterrows():
        key = str(row["upgrade_key"])
        if key not in manual_locked:
            continue
        ocr_level = coerce_int(row.get("ocr_level"))
        if ocr_level is not None and ocr_level > 0:
            conflicts.append(f"{label_for_key(key)}: OCR leu Lv {level_display(ocr_level)}")
    return conflicts


def manual_locked_editor_frame(
    rows: pd.DataFrame,
    manual_locked: set[str],
    *,
    show_state: bool = True,
) -> pd.DataFrame:
    ordered = rows.sort_values(["family", "tier"]).copy()
    data = {
        "locked": [str(key) in manual_locked for key in ordered["upgrade_key"]],
        "label": [upgrade_display_name(str(key)) for key in ordered["upgrade_key"]],
    }
    if show_state:
        data["status"] = [status_label(str(status)) for status in ordered["status"]]
        data["level"] = [level_display(value) or "" for value in ordered["level"]]
    data["upgrade_key"] = [str(key) for key in ordered["upgrade_key"]]
    return pd.DataFrame(data)


def render_manual_locked_editor(merged: pd.DataFrame, *, show_state: bool = True) -> pd.DataFrame:
    manual_locked = load_manual_locked()
    if merged.empty:
        return merged

    edited_locked = set(manual_locked)
    state_version = st.session_state.get("state_version", "v0")
    with st.expander(f"Bloqueios manuais ({len(manual_locked)})", expanded=bool(manual_locked)):
        tabs = st.tabs([SCREEN_TITLES.get(screen, screen) for screen in SCREEN_ORDER])
        for screen, tab in zip(SCREEN_ORDER, tabs):
            with tab:
                subset = merged[merged["screen"] == screen]
                if subset.empty:
                    st.caption("Sem itens nesta tela.")
                    continue
                frame = manual_locked_editor_frame(subset, edited_locked, show_state=show_state)
                disabled_columns = ["label", "upgrade_key"]
                column_config = {
                    "locked": st.column_config.CheckboxColumn("Locked", width="small"),
                    "label": st.column_config.TextColumn("Upgrade", width="medium"),
                    "upgrade_key": st.column_config.TextColumn("Key", width="medium"),
                }
                if show_state:
                    disabled_columns.extend(["status", "level"])
                    column_config.update(
                        {
                            "status": st.column_config.TextColumn("Status", width="small"),
                            "level": st.column_config.TextColumn("Level", width="small"),
                        }
                    )
                edited = st.data_editor(
                    frame,
                    width="stretch",
                    hide_index=True,
                    num_rows="fixed",
                    disabled=disabled_columns,
                    column_config=column_config,
                    key=f"manual_locked_editor_{state_version}_{screen_slug(screen)}",
                )
                screen_keys = set(frame["upgrade_key"])
                edited_locked.difference_update(screen_keys)
                edited_locked.update(
                    str(row["upgrade_key"])
                    for _, row in edited.iterrows()
                    if bool(row.get("locked"))
                )

        edited_locked = set(normalize_manual_locked(edited_locked))
        if edited_locked != manual_locked:
            save_manual_locked(edited_locked)
            st.session_state["last_macro_text"] = None
            st.session_state["last_result"] = None

        conflicts = manual_locked_conflicts(merged, edited_locked)
        if conflicts:
            st.warning("Bloqueio manual conflita com OCR: " + "; ".join(conflicts[:6]))
        st.caption(f"Arquivo: {LOCKED_UPGRADES_PATH.relative_to(APP_ROOT)}")

    return apply_manual_locked(merged, edited_locked)


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
            manual_locked = int(subset.get("manual_locked", pd.Series(dtype=bool)).fillna(False).sum())
            review_missing = int(((subset["status"] == "review") & (~subset["detected"])).sum())
            st.markdown(f"**{SCREEN_TITLES.get(screen, screen)}**")
            st.write(
                f"- {inferred_maxed} maxed inferidos antes de sequencias visiveis\n"
                f"- {manual_locked} locked manuais salvos\n"
                f"- {review_missing} ausencias para revisar"
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
                    width="stretch",
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
                st.dataframe(subset[detail_columns], width="stretch", hide_index=True)


def show_editor() -> pd.DataFrame | None:
    rows = st.session_state.get("state_rows")
    if rows is None:
        pre_ocr_rows = build_state_rows([], manual_locked=load_manual_locked())
        render_manual_locked_editor(pre_ocr_rows, show_state=False)
        return None

    merged = rows.copy()
    merged = render_manual_locked_editor(merged)
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

    with st.expander("Resumo dos levels lidos", expanded=not pending.empty):
        render_state_summary(merged)
    render_inference_summary(merged)
    render_advanced_editor(merged)
    merged = apply_manual_locked(merged, load_manual_locked())
    render_debug_rows(merged)

    st.session_state["state_rows"] = merged

    return merged


def show_validation_errors(errors: list[str]) -> None:
    if not errors:
        return
    st.warning(f"{len(errors)} ajuste(s) precisam ser resolvidos antes de gerar a macro.")
    with st.expander("Ver ajustes pendentes", expanded=False):
        st.write("\n".join(f"- {error}" for error in errors))


def build_open_image_html(image_bytes: bytes, mime_type: str, caption: str) -> str:
    safe_mime_type = html_lib.escape(mime_type or "image/png", quote=True)
    safe_caption = html_lib.escape(caption)
    encoded_image = base64.b64encode(image_bytes).decode("ascii")
    data_url = f"data:{safe_mime_type};base64,{encoded_image}"
    preview_page = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{safe_caption}</title>
<style>
html, body {{
    margin: 0;
    min-height: 100%;
    background: #111827;
}}
body {{
    display: grid;
    place-items: start center;
    padding: 16px;
}}
img {{
    max-width: 100%;
    height: auto;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.35);
}}
</style>
</head>
<body>
<img src="{data_url}" alt="{safe_caption}">
</body>
</html>"""
    return f"""
    <button
        id="open-image-preview"
        type="button"
        style="
            display: inline-block;
            width: 100%;
            box-sizing: border-box;
            text-align: center;
            border: 1px solid rgba(250, 250, 250, 0.25);
            border-radius: 0.45rem;
            background: #2563eb;
            color: white;
            font: 700 14px -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            padding: 0.42rem 0.72rem;
            cursor: pointer;
        "
        title="{safe_caption}"
    >Abrir print em nova aba</button>
    <script>
    const button = document.getElementById("open-image-preview");
    const previewHtml = {json.dumps(preview_page)};

    button.addEventListener("click", () => {{
        const blob = new Blob([previewHtml], {{ type: "text/html" }});
        const openUrl = URL.createObjectURL(blob);
        const opened = window.open(openUrl, "_blank", "noopener,noreferrer");
        if (!opened) {{
            window.location.href = openUrl;
        }}
        window.setTimeout(() => URL.revokeObjectURL(openUrl), 60000);
    }});
    </script>
    """


def show_upload_preview(upload: Any, caption: str) -> None:
    if upload is None:
        st.caption("Nenhum print anexado.")
        return
    st.image(upload, caption=caption, width=THUMBNAIL_WIDTH)
    image_bytes = bytes(upload.getbuffer())
    mime_type = str(getattr(upload, "type", "image/png") or "image/png")
    components.html(
        build_open_image_html(image_bytes, mime_type, caption),
        height=42,
    )


def show_upload_block(
    title: str,
    subtitle: str,
    accent: str,
    uploader_key: str,
    preview_caption: str,
) -> Any:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="border-left: 7px solid {accent}; padding: 0.05rem 0 0.1rem 0.7rem; margin-bottom: 0.55rem;">
                <div style="font-size: 1.1rem; font-weight: 850; line-height: 1.15;">{title}</div>
                <div style="font-size: 0.82rem; opacity: 0.72; margin-top: 0.18rem;">{subtitle}</div>
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
        show_upload_preview(upload, preview_caption)
        return upload


def render_macro_output_panel(
    result: dict[str, Any] | None,
    macro_text: str | None,
    run_dir: Path,
    *,
    has_pending: bool = False,
    resource_errors: list[str] | None = None,
    macro_stale: bool = False,
    key_prefix: str = "top",
    show_details: bool = False,
) -> None:
    resource_errors = resource_errors or []
    st.markdown("### Macro")

    if has_pending:
        st.info("Resolva as pendencias de OCR abaixo para liberar a macro.")
    elif resource_errors:
        st.warning(resource_errors[0])
    elif not macro_text:
        st.info("A macro aparece aqui assim que as imagens forem lidas.")
    elif macro_stale:
        st.warning("Recursos ou objetivo mudaram. Recalcule para atualizar esta macro.")

    sections = split_macro_sections(macro_text or "")
    research_text = sections.get("Research/Energy", "")
    prestige_text = sections.get("Prestige/PowerUps", "")
    macro_digest = hashlib.sha1((macro_text or "").encode("utf-8")).hexdigest()[:10]

    st.text_area(
        "ENERGY / RESEARCH",
        research_text,
        height=90,
        placeholder="Sem macro de Energy ainda.",
        key=f"{key_prefix}_energy_macro_text_{macro_digest}",
    )
    render_copy_button(research_text, f"{key_prefix}_energy_macro", "Copiar Energy")

    st.text_area(
        "PRESTIGE / POWERUPS",
        prestige_text,
        height=90,
        placeholder="Sem macro de Prestige ainda.",
        key=f"{key_prefix}_prestige_macro_text_{macro_digest}",
    )
    render_copy_button(prestige_text, f"{key_prefix}_prestige_macro", "Copiar Prestige")

    if macro_text:
        with st.expander("Macro completa", expanded=False):
            st.text_area(
                "Macro combinada",
                macro_text,
                height=180,
                label_visibility="collapsed",
                key=f"{key_prefix}_combined_macro_text_{macro_digest}",
            )
            render_copy_button(macro_text, f"{key_prefix}_combined_macro", "Copiar tudo")
            st.download_button(
                "Baixar macro .txt",
                data=macro_text,
                file_name="macro_clicks.txt",
                mime="text/plain",
                key=f"{key_prefix}_download_macro",
            )

    if show_details and result is not None:
        with st.expander("Detalhes da otimizacao", expanded=False):
            detail_col_a, detail_col_b = st.columns(2)
            with detail_col_a:
                st.markdown("**Recursos**")
                st.json(result.get("resources", {}), expanded=False)
            with detail_col_b:
                st.markdown("**Multiplicadores**")
                st.json(result.get("factors", {}), expanded=False)

            purchases = result.get("purchases", [])
            if purchases:
                st.markdown("**Compras recomendadas**")
                st.dataframe(pd.DataFrame(purchases), width="stretch", hide_index=True)
            st.caption(f"Artefatos salvos em: {run_dir}")


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
            padding: 0.36rem 0.72rem;
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
        height=40,
    )


def render_result(result: dict[str, Any], macro_text: str, run_dir: Path) -> None:
    render_macro_output_panel(
        result,
        macro_text,
        run_dir,
        key_prefix="result",
        show_details=True,
    )


def main() -> None:
    page_setup()
    run_dir = ensure_run_dir()

    with st.sidebar:
        st.header("Configuracao tecnica")
        python_bin = render_python_folder_selector()
        engine = st.selectbox("OCR engine", ["consensus", "auto", "vision", "easyocr", "paddle", "tesseract"], index=0)
        st.caption("Ajuste aqui apenas se precisar trocar engine ou a pasta do Python.")

    control_slot = st.empty()
    macro_status_slot = st.empty()

    col_left, col_middle, col_right = st.columns([1, 1, 1.35], gap="large")
    with col_left:
        research_upload = show_upload_block(
            title="ENERGIA / RESEARCH",
            subtitle="Print da aba Research.",
            accent=SCREEN_ACCENTS["Research/Energy"],
            uploader_key="research_upload",
            preview_caption="Energia / Research",
        )
    with col_middle:
        prestige_upload = show_upload_block(
            title="PRESTIGE / POWERUPS",
            subtitle="Print da aba Prestige.",
            accent=SCREEN_ACCENTS["Prestige/PowerUps"],
            uploader_key="prestige_upload",
            preview_caption="Prestige / PowerUps",
        )
    with col_right:
        macro_output_slot = st.empty()

    with control_slot.container():
        control_col_a, control_col_b, control_col_c, control_col_d = st.columns([1.2, 1, 1, 1.35], gap="medium")
        with control_col_a:
            objective = st.radio("Objetivo", ["FARM", "GOLD_PREP"], horizontal=True)
        with control_col_b:
            energy = st.text_input("Energy", "0")
        with control_col_c:
            prestige_points = st.text_input("Prestige Points", "0")
        resource_errors_for_button = validate_resource_inputs(energy, prestige_points)
        with control_col_d:
            st.caption("Escala do jogo: 2,59M, 1,21e20, 850K. Um recurso pode ficar 0.")
            process_button_slot = st.empty()
            process_button_disabled = (
                research_upload is None and prestige_upload is None
            ) or bool(resource_errors_for_button)
            process_button_label = (
                "Reler imagens e gerar macro"
                if st.session_state.get("state_rows") is not None
                else "Ler imagens e gerar macro"
            )
            process_images = process_button_slot.button(
                process_button_label,
                type="primary",
                disabled=process_button_disabled,
                width="stretch",
                key="process_images_button",
            )
            macro_action_slot = st.empty()

    ocr_notice = st.session_state.pop("ocr_notice", None)
    if ocr_notice:
        with macro_status_slot.container():
            st.caption(str(ocr_notice))
    ocr_error = st.session_state.pop("ocr_error", None)
    if ocr_error:
        with macro_status_slot.container():
            st.error(str(ocr_error))

    if process_images:
        process_button_slot.button(
            "Processando imagens...",
            type="primary",
            disabled=True,
            width="stretch",
            key="process_images_busy_button",
        )
        ocr_results: list[dict[str, Any]] = []
        with macro_status_slot.status("Processando imagens...", expanded=True) as status:
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
                    st.session_state["state_rows"] = build_state_rows(
                        ocr_results,
                        manual_locked=load_manual_locked(),
                    )
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

    panel_has_pending = False
    panel_resource_errors = resource_errors_for_button
    panel_macro_stale = False

    if edited_rows is not None:
        has_pending = bool((edited_rows["status"] == "review").any())
        panel_has_pending = has_pending
        should_auto_generate = bool(st.session_state.pop("auto_generate_macro", False))
        current_generation_inputs = {
            "objective": objective,
            "energy": energy,
            "prestige_points": prestige_points,
            "rows": rows_state_fingerprint(edited_rows),
        }
        resource_errors = validate_resource_inputs(energy, prestige_points)
        panel_resource_errors = resource_errors
        macro_stale = (
            bool(st.session_state.get("last_macro_text"))
            and st.session_state.get("last_generation_inputs") != current_generation_inputs
        )
        panel_macro_stale = macro_stale

        if should_auto_generate and not has_pending and not resource_errors:
            with macro_status_slot.status("Gerando macros automaticamente...", expanded=True) as status:
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
            with macro_status_slot.container():
                st.info("A macro nao foi gerada automaticamente porque ainda existem pendencias de OCR.")
        elif should_auto_generate and resource_errors:
            with macro_status_slot.container():
                st.info("A macro nao foi gerada automaticamente porque os recursos ainda nao foram informados.")

        if st.session_state.get("last_macro_text"):
            macro_button_label = "Recalcular macro" if macro_stale else "Atualizar macro"
        else:
            macro_button_label = "Gerar macro"
        with macro_action_slot.container():
            run_macro = st.button(
                macro_button_label,
                disabled=has_pending or bool(resource_errors),
                type="secondary",
                width="stretch",
                key="generate_macro_button",
            )
        if run_macro:
            with macro_action_slot.container():
                st.button(
                    "Gerando macro...",
                    disabled=True,
                    type="secondary",
                    width="stretch",
                    key="generate_macro_busy_button",
                )
            with macro_status_slot.status("Gerando macro...", expanded=True) as status:
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
    with macro_output_slot.container():
        render_macro_output_panel(
            stored_result,
            stored_macro_text,
            run_dir,
            has_pending=panel_has_pending,
            resource_errors=panel_resource_errors,
            macro_stale=panel_macro_stale,
            key_prefix="top",
            show_details=True,
        )

    with st.expander("Passada residual", expanded=False):
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
