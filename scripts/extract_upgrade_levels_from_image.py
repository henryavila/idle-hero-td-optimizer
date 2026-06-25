#!/usr/bin/env python3
"""Extract Idle Hero TD upgrade levels from screenshots without LLMs.

The script is deterministic: it uses Tesseract OCR TSV output, then parses
levels with fixed regexes and optional fixed regions of interest.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FORMULA_FACTORS_CSV = (
    PROJECT_ROOT
    / "IdleHeroTD-apk"
    / "apk_analysis"
    / "dados-consolidados"
    / "formulas"
    / "csv"
    / "core_upgrade_formula_factors.csv"
)
VISION_OCR_SOURCE = SCRIPT_DIR / "macos_vision_ocr.swift"
VISION_OCR_BINARY = Path("/tmp/idle_hero_macos_vision_ocr")

RESEARCH_CORE_KEYS = [
    "researchDmg1",
    "researchDmg2",
    "researchDmg3",
    "researchDmg4",
    "researchDmg5",
    "researchDmg6",
    "researchKillGold1",
    "researchKillGold2",
    "researchKillGold3",
    "researchKillGold4",
    "researchKillGold5",
    "researchKillGold6",
    "researchPrestigePower1",
    "researchPrestigePower2",
    "researchPrestigePower3",
    "researchPrestigePower4",
    "researchPrestigePower5",
]
PRESTIGE_CORE_KEYS = [
    "prestigeDmg1",
    "prestigeDmg2",
    "prestigeDmg3",
    "prestigeDmg4",
    "prestigeDmg5",
    "prestigeDmg6",
    "prestigeDmg7",
    "prestigeKillGold1",
    "prestigeKillGold2",
    "prestigeKillGold3",
    "prestigeKillGold4",
    "prestigeKillGold5",
    "prestigeKillGold6",
    "prestigeKillGold7",
]
PRESETS = {
    "research-core": RESEARCH_CORE_KEYS,
    "prestige-core": PRESTIGE_CORE_KEYS,
    "all-core": RESEARCH_CORE_KEYS + PRESTIGE_CORE_KEYS,
}
METRIC_TO_KEY_PREFIX = {
    "research-core": {
        "damage": "researchDmg",
        "kill_gold": "researchKillGold",
        "prestige_power": "researchPrestigePower",
    },
    "prestige-core": {
        "damage": "prestigeDmg",
        "kill_gold": "prestigeKillGold",
    },
}
ROMAN_VALUES = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
}
LEVEL_PATTERNS = [
    re.compile(r"\b(?:lv|lvl|level|l)\.?\s*[.:a#-]?\s*([0-9A-Za-z][0-9A-Za-z,\.]*)\b", re.IGNORECASE),
    re.compile(r"\b([0-9][0-9,\.]*)\s*/\s*(?:999999|999|[0-9]{2,})\b", re.IGNORECASE),
    re.compile(r"\b(?:current|curr)\s*[:#-]?\s*([0-9][0-9,\.]*)\b", re.IGNORECASE),
]


@dataclass
class OcrWord:
    text: str
    conf: float
    left: int
    top: int
    width: int
    height: int
    page_num: str
    block_num: str
    par_num: str
    line_num: str

    @property
    def center(self) -> tuple[float, float]:
        return self.left + self.width / 2, self.top + self.height / 2

    @property
    def line_key(self) -> tuple[str, str, str, str]:
        return self.page_num, self.block_num, self.par_num, self.line_num


@dataclass
class OcrLine:
    text: str
    words: list[OcrWord]
    top: int
    left: int


def run_ocr(
    image_path: Path,
    engine: str,
    tesseract_bin: str,
    lang: str,
    psm: int,
) -> tuple[str, str]:
    if engine == "auto":
        if easyocr_available():
            engine = "easyocr"
        elif shutil.which(tesseract_bin):
            engine = "tesseract"
        elif shutil.which("swiftc") and VISION_OCR_SOURCE.exists():
            engine = "vision"
        else:
            raise SystemExit(
                "no OCR engine found. Install Tesseract with 'brew install tesseract' "
                "or use macOS with swiftc/Vision available."
            )

    if engine == "tesseract":
        return run_tesseract(image_path, tesseract_bin, lang, psm), "tesseract"
    if engine == "easyocr":
        return run_easyocr(image_path), "easyocr"
    if engine == "vision":
        return run_vision_ocr(image_path), "vision"
    raise SystemExit(f"unknown OCR engine: {engine}")


def easyocr_available() -> bool:
    try:
        import easyocr  # noqa: F401
    except Exception:
        return False
    return True


def run_easyocr(image_path: Path) -> str:
    try:
        import easyocr
    except Exception as exc:
        raise SystemExit(f"easyocr is not installed: {exc}") from exc

    reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    result = reader.readtext(str(image_path), detail=1, paragraph=False)

    width, height = image_size(image_path)
    lines = [
        "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext",
        f"1\t1\t0\t0\t0\t0\t0\t0\t{width}\t{height}\t-1\t",
    ]
    for index, (box, text, conf) in enumerate(result, start=1):
        xs = [int(point[0]) for point in box]
        ys = [int(point[1]) for point in box]
        left = min(xs)
        top = min(ys)
        box_width = max(xs) - left
        box_height = max(ys) - top
        clean_text = str(text).replace("\t", " ").replace("\n", " ").strip()
        lines.append(
            f"5\t1\t1\t1\t{index}\t1\t{left}\t{top}\t{box_width}\t{box_height}\t{float(conf) * 100:.1f}\t{clean_text}"
        )
    return "\n".join(lines) + "\n"


def image_size(image_path: Path) -> tuple[int, int]:
    try:
        from PIL import Image
    except Exception as exc:
        raise SystemExit(f"Pillow is required for image size detection: {exc}") from exc
    with Image.open(image_path) as image:
        return image.size


def run_tesseract(image_path: Path, tesseract_bin: str, lang: str, psm: int) -> str:
    executable = shutil.which(tesseract_bin)
    if executable is None:
        raise SystemExit(
            "tesseract not found. Install it first, for example: brew install tesseract"
        )

    command = [
        executable,
        str(image_path),
        "stdout",
        "-l",
        lang,
        "--psm",
        str(psm),
        "tsv",
    ]
    result = subprocess.run(command, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "tesseract failed")
    return result.stdout


def run_vision_ocr(image_path: Path) -> str:
    if not VISION_OCR_SOURCE.exists():
        raise SystemExit(f"missing Vision OCR helper: {VISION_OCR_SOURCE}")
    if shutil.which("swiftc") is None:
        raise SystemExit("swiftc not found; install Tesseract or run on macOS with Xcode command line tools")

    source_mtime = VISION_OCR_SOURCE.stat().st_mtime
    needs_compile = not VISION_OCR_BINARY.exists() or VISION_OCR_BINARY.stat().st_mtime < source_mtime
    if needs_compile:
        compile_result = subprocess.run(
            ["swiftc", str(VISION_OCR_SOURCE), "-o", str(VISION_OCR_BINARY)],
            check=False,
            text=True,
            capture_output=True,
        )
        if compile_result.returncode != 0:
            raise SystemExit(compile_result.stderr.strip() or "failed to compile Vision OCR helper")

    result = subprocess.run(
        [str(VISION_OCR_BINARY), str(image_path)],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "Vision OCR helper failed")
    return result.stdout


def parse_tsv(tsv_text: str, min_conf: float) -> tuple[list[OcrWord], tuple[int, int]]:
    reader = csv.DictReader(io.StringIO(tsv_text), delimiter="\t")
    words: list[OcrWord] = []
    page_size = (0, 0)

    for row in reader:
        try:
            level = int(row.get("level", "0") or 0)
            left = int(row.get("left", "0") or 0)
            top = int(row.get("top", "0") or 0)
            width = int(row.get("width", "0") or 0)
            height = int(row.get("height", "0") or 0)
        except ValueError:
            continue

        if level == 1 and width > 0 and height > 0:
            page_size = (width, height)

        text = (row.get("text") or "").strip()
        if not text:
            continue

        try:
            conf = float(row.get("conf", "-1") or -1)
        except ValueError:
            conf = -1
        if conf < min_conf:
            continue

        words.append(
            OcrWord(
                text=text,
                conf=conf,
                left=left,
                top=top,
                width=width,
                height=height,
                page_num=row.get("page_num", "0"),
                block_num=row.get("block_num", "0"),
                par_num=row.get("par_num", "0"),
                line_num=row.get("line_num", "0"),
            )
        )

    if page_size == (0, 0) and words:
        page_size = (
            max(word.left + word.width for word in words),
            max(word.top + word.height for word in words),
        )
    return words, page_size


def group_lines(words: list[OcrWord]) -> list[OcrLine]:
    grouped: dict[tuple[str, str, str, str], list[OcrWord]] = {}
    for word in words:
        grouped.setdefault(word.line_key, []).append(word)

    lines: list[OcrLine] = []
    for line_words in grouped.values():
        ordered = sorted(line_words, key=lambda word: word.left)
        lines.append(
            OcrLine(
                text=" ".join(word.text for word in ordered),
                words=ordered,
                top=min(word.top for word in ordered),
                left=min(word.left for word in ordered),
            )
        )
    return sorted(lines, key=lambda line: (line.top, line.left))


def parse_level(text: str) -> int | None:
    for pattern in LEVEL_PATTERNS:
        match = pattern.search(text)
        if match:
            return parse_level_int(match.group(1))
    return None


def parse_level_int(raw: str) -> int | None:
    normalized = raw.upper().strip()
    compact = re.sub(r"[^A-Z0-9]", "", normalized)
    if compact in {"1Z", "IZ", "LZ"}:
        return 112

    normalized = (
        normalized
        .replace("O", "0")
        .replace("Q", "0")
        .replace("I", "1")
        .replace("L", "1")
        .replace("|", "1")
        .replace("W", "1")
        .replace("Z", "2")
        .replace("S", "5")
        .replace("J", "3")
    )
    digits = re.sub(r"\D", "", normalized)
    if not digits:
        return None
    return int(digits)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.lower())).strip()


def roman_to_int(raw: str) -> int | None:
    normalized = re.sub(r"[^A-Z0-9]", "", raw.upper())
    normalized = (
        normalized.replace("1", "I")
        .replace("L", "I")
        .replace("|", "I")
        .replace("T", "I")
        .replace("!", "I")
    )
    if normalized in ROMAN_VALUES:
        return ROMAN_VALUES[normalized]
    return None


def classify_metric(text: str) -> str | None:
    norm = normalize_text(text)
    compact = norm.replace(" ", "")
    if "crit" in compact or "rankexp" in compact:
        return None
    if any(token in compact for token in ("damage", "damace", "darnage")):
        return "damage"
    if "prest" in compact and ("power" in compact or "p0wer" in compact):
        return "prestige_power"
    if ("kill" in compact or "kil" in compact or compact.startswith("ki")) and any(
        token in compact for token in ("gold", "g0ld", "god", "cod", "cold", "c0ld", "golp", "goup")
    ):
        return "kill_gold"
    return None


def tier_from_label(text: str) -> int | None:
    before_level = re.split(r"\b(?:lv|lvl|level)\b", text, flags=re.IGNORECASE)[0]
    cleaned = normalize_text(before_level).upper()
    for noise in [
        "DAMAGE",
        "KILL",
        "GOLD",
        "GOD",
        "COLD",
        "C0LD",
        "GOLP",
        "GOUP",
        "PRESTIGE",
        "PRESTTGE",
        "POWER",
        "POwER".upper(),
        "P0WER",
        "RANK",
        "EXP",
    ]:
        cleaned = cleaned.replace(noise, " ")
    tokens = re.findall(r"[A-Z0-9]+", cleaned)
    for token in reversed(tokens):
        tier = roman_to_int(token)
        if tier is not None:
            return tier
    return None


def key_for_detected_label(screen: str, text: str) -> str | None:
    metric = classify_metric(text)
    if metric is None:
        return None
    prefix = METRIC_TO_KEY_PREFIX.get(screen, {}).get(metric)
    if prefix is None:
        return None
    tier = tier_from_label(text)
    if tier is None:
        return None
    return f"{prefix}{tier}"


def tier_from_effect_increment(prefix: str, context_text: str, percent_per_level: dict[str, float]) -> int | None:
    matches = re.findall(r"\(\s*\+\s*([0-9][0-9.,]*)\s*%\s*\)", context_text, flags=re.IGNORECASE)
    if not matches:
        return None
    value = parse_display_number(matches[-1])
    if value is None:
        return None
    candidates = []
    for key, percent in percent_per_level.items():
        if not key.startswith(prefix):
            continue
        if abs(percent - value) < 0.01:
            match = re.search(r"(\d+)$", key)
            if match:
                candidates.append(int(match.group(1)))
    if len(candidates) == 1:
        return candidates[0]
    return None


def tier_from_total_effect(
    prefix: str,
    context_text: str,
    percent_per_level: dict[str, float],
    level: int | None,
) -> int | None:
    if level is None or level <= 0:
        return None

    match = re.search(r"\+\s*([0-9][0-9.,]*\s*[KMBT]?)\s*%", context_text, flags=re.IGNORECASE)
    if not match:
        return None
    displayed_total = parse_display_number(match.group(1))
    if displayed_total is None:
        return None

    candidates: list[tuple[float, int]] = []
    for key, percent in percent_per_level.items():
        if not key.startswith(prefix):
            continue
        tier_match = re.search(r"(\d+)$", key)
        if not tier_match:
            continue
        expected_total = percent * level
        if expected_total <= 0:
            continue
        relative_error = abs(displayed_total - expected_total) / max(abs(displayed_total), abs(expected_total), 1.0)
        candidates.append((relative_error, int(tier_match.group(1))))

    if not candidates:
        return None
    candidates.sort()
    best_error, best_tier = candidates[0]
    return best_tier if best_error <= 0.5 else None


def key_for_detected_context(
    screen: str,
    label_text: str,
    context_text: str,
    percent_per_level: dict[str, float],
) -> str | None:
    metric = classify_metric(label_text)
    if metric is None:
        return None
    prefix = METRIC_TO_KEY_PREFIX.get(screen, {}).get(metric)
    if prefix is None:
        return None

    level = parse_level(context_text)
    tier = tier_from_total_effect(prefix, context_text, percent_per_level, level)
    if tier is None:
        tier = tier_from_effect_increment(prefix, context_text, percent_per_level)
    if tier is None:
        tier = tier_from_label(label_text)
    if tier is None:
        return None
    return f"{prefix}{tier}"


def rect_to_pixels(rect: list[float], page_size: tuple[int, int]) -> tuple[float, float, float, float]:
    if len(rect) != 4:
        raise ValueError(f"rect must have 4 values, got {rect!r}")
    width, height = page_size
    if max(abs(value) for value in rect) <= 1:
        left, top, right, bottom = rect
        return left * width, top * height, right * width, bottom * height
    return tuple(rect)  # type: ignore[return-value]


def words_in_rect(
    words: list[OcrWord],
    rect: list[float],
    page_size: tuple[int, int],
) -> list[OcrWord]:
    left, top, right, bottom = rect_to_pixels(rect, page_size)
    selected = []
    for word in words:
        cx, cy = word.center
        if left <= cx <= right and top <= cy <= bottom:
            selected.append(word)
    return sorted(selected, key=lambda word: (word.top, word.left))


def text_from_words(words: list[OcrWord]) -> str:
    lines = group_lines(words)
    return " ".join(line.text for line in lines)


def confidence(words: list[OcrWord]) -> float | None:
    if not words:
        return None
    return sum(word.conf for word in words) / len(words)


def extract_with_rois(
    words: list[OcrWord],
    page_size: tuple[int, int],
    rois: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    records = []
    warnings = []
    for roi in rois:
        key = roi["upgrade_key"]
        rect = roi["rect"]
        selected = words_in_rect(words, rect, page_size)
        text = text_from_words(selected)
        level = parse_level(text)
        if level is None:
            warnings.append(f"level not found for {key}")
        records.append(
            {
                "upgrade_key": key,
                "level": level,
                "confidence": confidence(selected),
                "text": text,
                "rect": rect,
            }
        )
    return records, warnings


def extract_auto_lines(lines: list[OcrLine], upgrade_keys: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    records = []
    warnings = []
    normalized_lines = [normalize_text(line.text) for line in lines]

    for key in upgrade_keys:
        aliases = key_aliases(key)
        found_index = None
        for index, line_text in enumerate(normalized_lines):
            if any(alias in line_text for alias in aliases):
                found_index = index
                break

        if found_index is None:
            records.append({"upgrade_key": key, "level": None, "confidence": None, "text": "", "rect": None})
            warnings.append(f"label not found for {key}")
            continue

        candidate_lines = lines[found_index : found_index + 3]
        text = " ".join(line.text for line in candidate_lines)
        level = parse_level(text)
        if level is None:
            warnings.append(f"level not found near label for {key}")
        line_words = [word for line in candidate_lines for word in line.words]
        records.append(
            {
                "upgrade_key": key,
                "level": level,
                "confidence": confidence(line_words),
                "text": text,
                "rect": None,
            }
        )

    return records, warnings


def load_percent_per_level() -> dict[str, float]:
    if not FORMULA_FACTORS_CSV.exists():
        return {}
    rows = {}
    with FORMULA_FACTORS_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                rows[row["upgrade_key"]] = float(row["stat_amt_percent"])
            except Exception:
                continue
    return rows


def line_bounds(lines: list[OcrLine]) -> tuple[int, int, int, int] | None:
    words = [word for line in lines for word in line.words]
    if not words:
        return None
    return (
        min(word.left for word in words),
        min(word.top for word in words),
        max(word.left + word.width for word in words),
        max(word.top + word.height for word in words),
    )


def nearest_following_lines(lines: list[OcrLine], index: int, max_count: int = 3) -> list[OcrLine]:
    label = lines[index]
    label_words = label.words
    if not label_words:
        return [label]
    left = min(word.left for word in label_words)
    right = max(word.left + word.width for word in label_words)
    min_left = left - 45
    max_right = right + 180
    selected = [label]
    for candidate in lines:
        if candidate is label:
            continue
        if candidate.top < label.top - 4:
            continue
        if candidate.top - label.top > 78:
            continue
        bounds = line_bounds([candidate])
        if bounds is None:
            continue
        candidate_left, _, candidate_right, _ = bounds
        candidate_center = (candidate_left + candidate_right) / 2
        overlaps_column = min(max_right, candidate_right) >= max(min_left, candidate_left)
        starts_near_label = abs(candidate_left - left) < 70
        center_near_label = min_left <= candidate_center <= max_right
        if overlaps_column or starts_near_label or center_near_label:
            selected.append(candidate)
        if len(selected) >= max_count:
            break
    selected_keys = {id(line) for line in selected}
    for candidate in lines:
        if id(candidate) in selected_keys:
            continue
        if abs(candidate.top - label.top) <= 24 and re.search(r"\bwave\b|lock", candidate.text, re.IGNORECASE):
            selected.append(candidate)
    return selected


def parse_display_number(raw: str) -> float | None:
    value = raw.strip().upper().replace(" ", "")
    if not value:
        return None
    suffix = 1.0
    if value.endswith("K"):
        suffix = 1_000.0
        value = value[:-1]
    elif value.endswith("M"):
        suffix = 1_000_000.0
        value = value[:-1]
    elif value.endswith("B"):
        suffix = 1_000_000_000.0
        value = value[:-1]
    elif value.endswith("T"):
        suffix = 1_000_000_000_000.0
        value = value[:-1]

    if "," in value and "." in value:
        value = value.replace(".", "").replace(",", ".")
    elif "," in value:
        value = value.replace(",", ".")
    elif "." in value:
        right = value.rsplit(".", 1)[1]
        if len(right) == 3 and suffix == 1.0:
            value = value.replace(".", "")
    try:
        return float(value) * suffix
    except ValueError:
        return None


def level_from_effect_text(text: str, upgrade_key: str, percent_per_level: dict[str, float]) -> int | None:
    percent = percent_per_level.get(upgrade_key)
    if not percent:
        return None
    match = re.search(r"\+\s*([0-9][0-9.,]*\s*[KMBT]?)\s*%", text, flags=re.IGNORECASE)
    if not match:
        return None
    value = parse_display_number(match.group(1))
    if value is None:
        return None
    return int(round(value / percent))


def level_looks_suspicious(level: int | None, raw_text: str) -> bool:
    if level is None:
        return True
    match = re.search(r"\b(?:lv|lvl|level|l)\.?\s*[.:a#-]?\s*([0-9A-Za-z][0-9A-Za-z,\.]*)", raw_text, re.IGNORECASE)
    if not match:
        return True
    raw = match.group(1)
    compact = re.sub(r"[^A-Za-z0-9]", "", raw.upper())
    if compact in {"1Z", "IZ", "LZ"}:
        return False
    return bool(re.search(r"[A-Za-z]", raw)) or len(re.sub(r"\D", "", raw)) < len(raw.replace(",", "").replace(".", ""))


def extract_auto_detect(
    lines: list[OcrLine],
    screen: str,
    requested_keys: list[str] | None,
) -> tuple[list[dict[str, Any]], list[str]]:
    percent_per_level = load_percent_per_level()
    detected: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []

    for index, line in enumerate(lines):
        context_lines = nearest_following_lines(lines, index)
        context_text = " ".join(item.text for item in context_lines)
        key = key_for_detected_context(screen, line.text, context_text, percent_per_level)
        if key is None:
            continue
        if requested_keys is not None and key not in requested_keys:
            continue

        level = parse_level(context_text)
        source = "level_text"
        effect_level = level_from_effect_text(context_text, key, percent_per_level)
        if effect_level is not None and level_looks_suspicious(level, context_text):
            level = effect_level
            source = "effect_text"
        bounds = line_bounds(context_lines)
        record = {
            "upgrade_key": key,
            "level": level,
            "confidence": confidence([word for item in context_lines for word in item.words]),
            "text": context_text,
            "rect": list(bounds) if bounds else None,
            "source": source,
        }

        previous = detected.get(key)
        if previous is None or (record["confidence"] or 0) > (previous.get("confidence") or 0):
            detected[key] = record

    if requested_keys is None:
        records = sorted(detected.values(), key=lambda record: (record["rect"] or [0, 0])[1:2] + [(record["rect"] or [0, 0])[0]])
    else:
        records = []
        for key in requested_keys:
            record = detected.get(key)
            if record is None:
                warnings.append(f"label not found for {key}")
                record = {"upgrade_key": key, "level": None, "confidence": None, "text": "", "rect": None, "source": None}
            records.append(record)

    for record in records:
        if record.get("level") is None:
            warnings.append(f"level not found for {record['upgrade_key']}")
    return records, warnings


def build_grid_rois(
    grid: str,
    cols: int,
    rows: int,
    keys: list[str],
) -> list[dict[str, Any]]:
    rect = [float(part.strip()) for part in grid.split(",")]
    if len(rect) != 4:
        raise SystemExit("--grid must be left,top,right,bottom")
    left, top, right, bottom = rect
    cell_width = (right - left) / cols
    cell_height = (bottom - top) / rows
    rois = []

    for index, key in enumerate(keys[: cols * rows]):
        row = index // cols
        col = index % cols
        rois.append(
            {
                "upgrade_key": key,
                "rect": [
                    left + col * cell_width,
                    top + row * cell_height,
                    left + (col + 1) * cell_width,
                    top + (row + 1) * cell_height,
                ],
            }
        )
    return rois


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def preset_keys(screen: str) -> list[str]:
    try:
        return PRESETS[screen]
    except KeyError as exc:
        raise SystemExit(f"unknown screen preset {screen!r}; choices: {', '.join(PRESETS)}") from exc


def visible_keys(args: argparse.Namespace) -> list[str]:
    if args.visible_keys:
        return [key.strip() for key in args.visible_keys.split(",") if key.strip()]
    return preset_keys(args.screen)


def config_template(screen: str) -> dict[str, Any]:
    return {
        "description": "Edit rect values after one screenshot calibration. Rects are normalized: left, top, right, bottom.",
        "engine": {
            "name": "easyocr",
            "lang": "eng",
            "psm": 11,
            "min_conf": 0,
        },
        "screen": screen,
        "rois": [
            {
                "upgrade_key": key,
                "label": key,
                "rect": [0.0, 0.0, 1.0, 1.0],
            }
            for key in preset_keys(screen)
        ],
    }


def result_document(
    image_path: Path,
    mode: str,
    engine: str,
    page_size: tuple[int, int],
    records: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "image": str(image_path),
        "mode": mode,
        "engine": engine,
        "page_size": {
            "width": page_size[0],
            "height": page_size[1],
        },
        "levels": {record["upgrade_key"]: record["level"] for record in records},
        "records": records,
        "warnings": warnings,
    }


def write_json(path: str | None, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if path:
        Path(path).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def write_csv(path: str | None, records: list[dict[str, Any]]) -> None:
    fieldnames = ["upgrade_key", "level", "confidence", "source", "text", "rect"]
    if path:
        with Path(path).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow({name: record.get(name, "") for name in fieldnames})
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({name: record.get(name, "") for name in fieldnames})


def state_document(records: list[dict[str, Any]], objective: str) -> dict[str, Any]:
    return {
        "objective": objective,
        "resources": {
            "energy": "0",
            "prestige_points": "0",
        },
        "levels": {
            record["upgrade_key"]: record["level"]
            for record in records
            if record.get("level") is not None
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract Idle Hero TD upgrade levels from screenshots with deterministic OCR parsing."
    )
    parser.add_argument("--image", help="Screenshot path.")
    parser.add_argument("--output", help="Output JSON/CSV path.")
    parser.add_argument("--format", choices=["json", "csv", "state"], default="json")
    parser.add_argument("--objective", default="FARM", help="Objective used only with --format state.")
    parser.add_argument("--screen", choices=sorted(PRESETS), default="research-core")
    parser.add_argument("--config", help="JSON config with per-upgrade ROI rectangles.")
    parser.add_argument("--grid", help="Generate fixed ROIs from left,top,right,bottom. Normalized values recommended.")
    parser.add_argument("--cols", type=int, help="Grid columns used with --grid.")
    parser.add_argument("--rows", type=int, help="Grid rows used with --grid.")
    parser.add_argument("--visible-keys", help="Comma-separated upgrade keys visible in row-major order.")
    parser.add_argument("--print-config-template", action="store_true", help="Print an ROI config template and exit.")
    parser.add_argument("--tesseract-bin", default="tesseract")
    parser.add_argument("--engine", choices=["auto", "easyocr", "tesseract", "vision"], default="auto")
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--psm", type=int, default=11, help="Tesseract page segmentation mode.")
    parser.add_argument("--min-conf", type=float, default=0.0)
    parser.add_argument("--dump-tsv", help="Write raw Tesseract TSV for debugging.")
    parser.add_argument("--dump-ocr-text", help="Write grouped OCR lines for debugging.")
    parser.add_argument("--require-all", action="store_true", help="Exit non-zero if any requested level is missing.")
    parser.add_argument("--self-test", action="store_true", help="Run parser self-test without an image.")
    return parser.parse_args()


def self_test() -> int:
    sample = """level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext
1\t1\t0\t0\t0\t0\t0\t0\t1000\t1000\t-1\t
5\t1\t1\t1\t1\t1\t10\t10\t100\t20\t90\tDamage
5\t1\t1\t1\t1\t2\t120\t10\t20\t20\t92\t1
5\t1\t1\t1\t2\t1\t10\t40\t20\t20\t91\tLv
5\t1\t1\t1\t2\t2\t35\t40\t40\t20\t93\t123
"""
    words, page_size = parse_tsv(sample, min_conf=35)
    rois = [{"upgrade_key": "researchDmg1", "rect": [0, 0, 0.5, 0.2]}]
    records, warnings = extract_with_rois(words, page_size, rois)
    assert records[0]["level"] == 123, records
    assert not warnings, warnings

    percent_per_level = {
        "researchKillGold1": 5.0,
        "researchKillGold2": 10.0,
        "researchKillGold3": 25.0,
        "researchKillGold5": 75.0,
        "researchPrestigePower1": 10.0,
        "researchPrestigePower2": 25.0,
        "prestigeDmg2": 10.0,
        "prestigeDmg3": 25.0,
        "researchDmg3": 25.0,
    }
    assert key_for_detected_context(
        "research-core",
        "KILL Goup I (Lv: 446)",
        "KILL Goup I (Lv: 446) +2.230% (+5%)",
        percent_per_level,
    ) == "researchKillGold1"
    assert key_for_detected_context(
        "research-core",
        "KIl GOlD I (Lv: 1Z)",
        "KIl GOlD I (Lv: 1Z) +1720% (+830%)",
        percent_per_level,
    ) == "researchKillGold2"
    assert key_for_detected_context(
        "research-core",
        "Kill COD III (Lv 30)",
        "Kill COD III (Lv 30) +750% (+575%)",
        percent_per_level,
    ) == "researchKillGold3"
    assert key_for_detected_context(
        "research-core",
        "PRESTIGE POwER L (Lv: 195}",
        "PRESTIGE POwER L (Lv: 195} +4.875% (+750%)",
        percent_per_level,
    ) == "researchPrestigePower2"
    assert key_for_detected_context(
        "research-core",
        "SUPER CRIT DAMAGE (Lv: 2)",
        "SUPER CRIT DAMAGE (Lv: 2) +10% (+25%)",
        percent_per_level,
    ) is None
    assert key_for_detected_context(
        "prestige-core",
        "DAMACE IT (Lv: 499.023)",
        "DAMACE IT (Lv: 499.023) +4,99M% (+10%)",
        percent_per_level,
    ) == "prestigeDmg2"
    assert key_for_detected_context(
        "research-core",
        "Ki COlD V (Lv 3)",
        "Ki COlD V (Lv 3) +225% (+75%)",
        percent_per_level,
    ) == "researchKillGold5"

    print("self-test ok")
    return 0


def main() -> int:
    args = parse_args()

    if args.self_test:
        return self_test()

    if args.print_config_template:
        write_json(args.output, config_template(args.screen))
        return 0

    if not args.image:
        raise SystemExit("--image is required unless --print-config-template or --self-test is used")
    image_path = Path(args.image)
    if not image_path.exists():
        raise SystemExit(f"image not found: {image_path}")

    tsv_text, engine_used = run_ocr(image_path, args.engine, args.tesseract_bin, args.lang, args.psm)
    if args.dump_tsv:
        Path(args.dump_tsv).write_text(tsv_text, encoding="utf-8")

    words, page_size = parse_tsv(tsv_text, min_conf=args.min_conf)
    lines = group_lines(words)
    if args.dump_ocr_text:
        Path(args.dump_ocr_text).write_text("\n".join(line.text for line in lines) + "\n", encoding="utf-8")

    mode = "auto-lines"
    config = load_config(Path(args.config)) if args.config else {}
    if config.get("engine"):
        engine = config["engine"]
        if "min_conf" in engine and float(engine["min_conf"]) != args.min_conf:
            words, page_size = parse_tsv(tsv_text, min_conf=float(engine["min_conf"]))
            lines = group_lines(words)

    if config.get("rois"):
        records, warnings = extract_with_rois(words, page_size, config["rois"])
        mode = "config-rois"
    elif args.grid:
        if not args.cols or not args.rows:
            raise SystemExit("--grid requires --cols and --rows")
        rois = build_grid_rois(args.grid, args.cols, args.rows, visible_keys(args))
        records, warnings = extract_with_rois(words, page_size, rois)
        mode = "grid-rois"
    else:
        requested = [key.strip() for key in args.visible_keys.split(",") if key.strip()] if args.visible_keys else None
        if args.screen == "all-core" and requested is None:
            raise SystemExit("--screen all-core requires --visible-keys, --grid, or --config")
        records, warnings = extract_auto_detect(lines, args.screen, requested)

    result = result_document(image_path, mode, engine_used, page_size, records, warnings)
    if args.format == "json":
        write_json(args.output, result)
    elif args.format == "csv":
        write_csv(args.output, records)
    else:
        write_json(args.output, state_document(records, args.objective))

    if args.require_all and any(record["level"] is None for record in records):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
