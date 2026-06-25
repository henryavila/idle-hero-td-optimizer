#!/usr/bin/env python3
"""Streamlit UI for Idle Hero TD optimizer macro output."""

from __future__ import annotations

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


APP_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = APP_ROOT / "scripts"
DATA_DIR = APP_ROOT / "IdleHeroTD-apk" / "apk_analysis" / "dados-consolidados"
COSTS_CSV = DATA_DIR / "formulas" / "csv" / "core_upgrade_cost_formula_classes.csv"
RUNS_DIR = APP_ROOT / "runs"

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


def show_editor() -> pd.DataFrame | None:
    rows = st.session_state.get("state_rows")
    if rows is None:
        st.info("Arraste as imagens e clique em 'Ler imagens' para montar o estado.")
        return None

    st.subheader("Resolver pendencias")
    counts = rows["status"].value_counts().to_dict()
    st.caption(
        f"{counts.get('available', 0)} prontos | "
        f"{counts.get('locked', 0)} locked | "
        f"{counts.get('maxed', 0)} maxed | "
        f"{counts.get('review', 0)} pendencias"
    )

    merged = rows.copy()
    pending = merged[merged["status"] == "review"].copy()

    if pending.empty:
        st.success("Nada pendente. O estado ja esta pronto para gerar a macro.")
    else:
        st.info(f"Resolva somente estes {len(pending)} item(ns). O restante ja foi inferido pelo app.")
        columns = st.columns(2)
        state_version = st.session_state.get("state_version", "v0")
        decision_options = ["review", "available", "locked", "maxed", "ignore"]
        for position, (_, row) in enumerate(pending.iterrows()):
            key = str(row["upgrade_key"])
            with columns[position % 2]:
                with st.container(border=True):
                    st.markdown(f"**{row['label']}**")
                    st.caption(f"{row['screen']} - {inference_label(row.get('inference'))}")
                    if row.get("ocr_text"):
                        st.caption(str(row["ocr_text"])[:140])
                    decision = st.selectbox(
                        "Decisao",
                        decision_options,
                        index=0,
                        format_func=status_label,
                        key=f"pending_status_{state_version}_{key}",
                    )
                    level = row.get("level")
                    if decision == "available":
                        level = st.number_input(
                            "Level",
                            min_value=0,
                            step=1,
                            value=review_level_default(row.get("level")),
                            key=f"pending_level_{state_version}_{key}",
                        )
                    elif decision == "locked":
                        level = 0 if pd.isna(level) else level
                    update_row(merged, key, decision, level)

    inferred_maxed = int(((rows["status"] == "maxed") & (~rows["detected"])).sum())
    inferred_locked = int(((rows["status"] == "locked") & (~rows["detected"])).sum())
    visible_locked = int(((rows["status"] == "locked") & (rows["detected"])).sum())

    with st.expander("Resumo das inferencias", expanded=False):
        st.write(
            f"- {inferred_maxed} maxed inferidos antes de sequencias visiveis\n"
            f"- {inferred_locked} locked inferidos alem dos tiers visiveis\n"
            f"- {visible_locked} locked detectados por botao Wave/lock"
        )

    with st.expander("Ajustes avancados", expanded=False):
        editor_columns = ["label", "level", "status", "confidence", "screen", "upgrade_key"]
        edited = st.data_editor(
            merged[editor_columns],
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            column_config={
                "label": st.column_config.TextColumn("Upgrade", disabled=True, width="medium"),
                "level": st.column_config.NumberColumn("Level", min_value=0, step=1, width="small"),
                "status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTIONS, required=True, width="small"),
                "confidence": st.column_config.NumberColumn("OCR", disabled=True, format="%.1f", width="small"),
                "screen": st.column_config.TextColumn("Tela", disabled=True),
                "upgrade_key": st.column_config.TextColumn("Key", disabled=True),
            },
            disabled=["screen", "upgrade_key", "label", "confidence"],
            key="advanced_state_editor",
        )
        for _, edited_row in edited.iterrows():
            update_row(merged, str(edited_row["upgrade_key"]), str(edited_row["status"]), edited_row["level"])

    with st.expander("Debug OCR", expanded=False):
        detail_columns = ["label", "status", "inference", "detected", "confidence", "ocr_text", "upgrade_key"]
        st.dataframe(merged[detail_columns], use_container_width=True, hide_index=True)

    st.session_state["state_rows"] = merged

    return merged


def show_validation_errors(errors: list[str]) -> None:
    if not errors:
        return
    st.warning(f"{len(errors)} item(ns) precisam de ajuste antes de gerar a macro.")
    with st.expander("Ver itens pendentes", expanded=False):
        st.write("\n".join(f"- {error}" for error in errors))


def show_upload_preview(upload: Any, caption: str) -> None:
    if upload is None:
        st.caption("Nenhum print anexado.")
        return
    st.image(upload, caption=caption, width=PREVIEW_WIDTH)


def render_result(result: dict[str, Any], macro_text: str, run_dir: Path) -> None:
    st.subheader("Saida para macro")
    st.text_area("Copie este bloco", macro_text, height=240)
    st.download_button(
        "Baixar macro .txt",
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

    col_left, col_right = st.columns(2)
    with col_left:
        research_upload = st.file_uploader(
            "Arraste aqui o print de Research",
            type=["png", "jpg", "jpeg"],
            key="research_upload",
        )
    with col_right:
        prestige_upload = st.file_uploader(
            "Arraste aqui o print de Prestige",
            type=["png", "jpg", "jpeg"],
            key="prestige_upload",
        )

    action_col, hint_col = st.columns([1, 3])
    with action_col:
        process_images = st.button(
            "Ler imagens",
            type="primary",
            disabled=research_upload is None and prestige_upload is None,
            use_container_width=True,
        )
    with hint_col:
        st.caption("O app infere pela ordem dos tiers: ausente antes de uma sequencia visivel = maxed; ausente depois do limite visivel = locked.")

    if research_upload is not None or prestige_upload is not None:
        with st.expander("Previews dos prints", expanded=True):
            preview_left, preview_right = st.columns(2)
            with preview_left:
                show_upload_preview(research_upload, "Research")
            with preview_right:
                show_upload_preview(prestige_upload, "Prestige")

    if process_images:
        ocr_results: list[dict[str, Any]] = []
        try:
            if research_upload is not None:
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
                st.error("Anexe pelo menos uma imagem.")
            else:
                st.session_state["ocr_results"] = ocr_results
                st.session_state["state_rows"] = build_state_rows(ocr_results)
                st.session_state["state_version"] = datetime.now().strftime("%H%M%S%f")
                st.success("OCR concluido. Resolva as pendencias, se houver, e gere a macro.")
        except Exception as exc:
            st.error(str(exc))

    ocr_results = st.session_state.get("ocr_results", [])
    show_warnings(ocr_results)
    edited_rows = show_editor()

    if edited_rows is not None:
        if st.button("Gerar macro"):
            state, errors = build_optimizer_state(
                rows=edited_rows,
                objective=objective,
                energy=energy,
                prestige_points=prestige_points,
            )
            if errors:
                show_validation_errors(errors)
            else:
                try:
                    state_path = run_dir / f"estado_{objective.lower()}.json"
                    result_path = run_dir / f"resultado_{objective.lower()}.json"
                    macro_path = run_dir / f"macro_clicks_{objective.lower()}.txt"
                    write_json(state_path, state)
                    result = run_optimizer(python_bin, state_path, result_path, objective)
                    macro_text = run_macro_formatter(python_bin, result_path, macro_path)
                    st.session_state["last_result"] = result
                    st.session_state["last_objective"] = objective
                    st.session_state["last_locked"] = state.get("locked_upgrades", [])
                    render_result(result, macro_text, run_dir)
                except Exception as exc:
                    st.error(str(exc))

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
