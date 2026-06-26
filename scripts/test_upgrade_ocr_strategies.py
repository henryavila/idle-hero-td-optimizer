#!/usr/bin/env python3
"""Compare OCR strategies against checked sample screenshots."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import extract_upgrade_levels_from_image as ocr


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "sample" / "upgrade_ocr_gold.json"

OCR_CACHE: dict[tuple[str, Path], tuple[list[ocr.OcrWord], tuple[int, int], list[ocr.OcrLine]]] = {}


def available_engines() -> list[str]:
    engines = []
    if ocr.easyocr_available():
        engines.append("easyocr")
    if ocr.shutil.which("swiftc") and ocr.VISION_OCR_SOURCE.exists():
        engines.append("vision")
    if ocr.shutil.which("tesseract"):
        engines.append("tesseract")
    if ocr.paddleocr_available():
        engines.append("paddle")
    return engines


def records_to_levels(records: list[dict[str, object]]) -> dict[str, int | None]:
    return {str(record["upgrade_key"]): record.get("level") for record in records}


def load_samples() -> list[dict[str, object]]:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    samples = []
    for sample in payload["samples"]:
        sample = dict(sample)
        sample["image"] = PROJECT_ROOT / str(sample["image"])
        samples.append(sample)
    return samples


def score(levels: dict[str, int | None], expected: dict[str, int]) -> tuple[int, int, int, list[str]]:
    ok = 0
    missing = 0
    wrong = 0
    details = []
    for key, expected_level in expected.items():
        actual = levels.get(key)
        if actual is None:
            missing += 1
            details.append(f"{key}: missing expected {expected_level}")
        elif actual == expected_level:
            ok += 1
        else:
            wrong += 1
            details.append(f"{key}: got {actual}, expected {expected_level}")
    for key, actual in sorted(levels.items()):
        if key not in expected and actual is not None:
            wrong += 1
            details.append(f"{key}: unexpected non-null level {actual}")
    return ok, missing, wrong, details


def ocr_payload(
    engine: str,
    image: Path,
) -> tuple[list[ocr.OcrWord], tuple[int, int], list[ocr.OcrLine]]:
    cache_key = (engine, image)
    if cache_key in OCR_CACHE:
        return OCR_CACHE[cache_key]
    tsv_text, _engine_used = ocr.run_ocr(image, engine, "tesseract", "eng", 11)
    words, page_size = ocr.parse_tsv(tsv_text, min_conf=0)
    lines = ocr.group_lines(words)
    OCR_CACHE[cache_key] = (words, page_size, lines)
    return words, page_size, lines


def run_strategy(
    strategy: str,
    engine: str,
    image: Path,
    screen: str,
    expected_keys: list[str],
) -> tuple[dict[str, int | None], list[str]]:
    words, page_size, lines = ocr_payload(engine, image)

    if strategy == "auto-lines":
        records, warnings = ocr.extract_auto_detect(lines, screen, expected_keys)
    elif strategy == "layout-slots":
        records, warnings = ocr.extract_layout_slots(words, page_size, screen, expected_keys)
    else:
        raise AssertionError(f"unknown strategy: {strategy}")
    return records_to_levels(records), warnings


def run_consensus(
    image: Path,
    screen: str,
    expected_keys: list[str],
) -> tuple[dict[str, int | None], list[str]]:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "extract_upgrade_levels_from_image.py"),
            "--image",
            str(image),
            "--screen",
            screen,
            "--engine",
            "consensus",
            "--visible-keys",
            ",".join(expected_keys),
            "--format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr.strip() or result.stdout.strip())
    payload = json.loads(result.stdout)
    return payload["levels"], payload.get("warnings", [])


def assert_parser_regressions() -> list[str]:
    failures = []
    percent_per_level = ocr.load_percent_per_level()

    text = "DAMACE LI (Lv. 499.028) 344.15T +4,99M% (+10%)"
    level = ocr.parse_level(text)
    if level != 499028:
        failures.append(f"parse_level dotted level: got {level}, expected 499028")
    if ocr.level_looks_suspicious(level, text):
        failures.append("level_looks_suspicious marked a precise dotted Lv after tier LI as suspicious")
    if not ocr.effect_level_matches(text, "prestigeDmg2", 499028, percent_per_level):
        failures.append("effect_level_matches did not validate rounded M suffix against visible Lv")
    if ocr.effect_level_for_validation(text, "prestigeDmg2", percent_per_level) is not None:
        failures.append("effect_level_for_validation inferred exact level from coarse M suffix")

    plain_text = "DAMAGE IV (Lv.1028) 1.67E+17 +51400% (+50%)"
    plain_effect_level = ocr.effect_level_for_validation(plain_text, "prestigeDmg4", percent_per_level)
    if plain_effect_level != 1028:
        failures.append(f"effect_level_for_validation plain percent: got {plain_effect_level}, expected 1028")

    k_text = "KILL GOLD L1T (Lv. 10.941) 4.26E+15 +273,53K% (+25%)"
    effect_level = ocr.effect_level_for_validation(k_text, "prestigeKillGold3", percent_per_level)
    if effect_level != 10941:
        failures.append(f"effect_level_for_validation K suffix: got {effect_level}, expected 10941")

    records, warnings = ocr.merge_ensemble_records(
        [
            {
                "upgrade_key": "prestigeKillGold3",
                "level": 10941,
                "confidence": 100.0,
                "text": k_text,
                "source": "level_text",
                "key_source": "auto_label",
                "engine": "vision",
                "strategy": "auto-lines",
            }
        ],
        ["prestigeKillGold3"],
    )
    merged_level = records[0]["level"] if records else None
    if merged_level != 10941 or warnings:
        failures.append(f"single mathematically validated K suffix candidate not accepted: level={merged_level}, warnings={warnings}")

    mismatch_text = "KILL GOLD III (Lv. 10.940) 4.26E+15 +273,53K% (+25%)"
    records, warnings = ocr.merge_ensemble_records(
        [
            {
                "upgrade_key": "prestigeKillGold3",
                "level": 10940,
                "confidence": 100.0,
                "text": mismatch_text,
                "source": "level_text",
                "key_source": "auto_label",
                "engine": "vision",
                "strategy": "auto-lines",
            }
        ],
        ["prestigeKillGold3"],
    )
    merged_level = records[0]["level"] if records else None
    if merged_level is not None or not warnings:
        failures.append(f"mismatched K suffix candidate accepted: level={merged_level}, warnings={warnings}")

    return failures


def main() -> int:
    engines = available_engines()
    if not engines:
        raise SystemExit("no OCR engine available for sample comparison")

    samples = load_samples()
    strategies = ["auto-lines", "layout-slots"]
    failures = assert_parser_regressions()
    print("OCR strategy comparison")
    print("=======================")
    for sample in samples:
        print(f"\n{sample['name']} ({sample['image'].name})")
        expected = sample["expected"]
        expected_keys = list(expected)
        for engine in engines:
            for strategy in strategies:
                levels, warnings = run_strategy(
                    strategy=strategy,
                    engine=engine,
                    image=sample["image"],
                    screen=sample["screen"],
                    expected_keys=expected_keys,
                )
                ok, missing, wrong, details = score(levels, expected)
                print(f"- {engine}/{strategy}: ok={ok} missing={missing} wrong={wrong}")
                if warnings:
                    print(f"  warnings={len(warnings)}")
                for detail in details[:6]:
                    print(f"  {detail}")
        levels, warnings = run_consensus(image=sample["image"], screen=sample["screen"], expected_keys=expected_keys)
        ok, missing, wrong, details = score(levels, expected)
        print(f"- consensus: ok={ok} missing={missing} wrong={wrong}")
        if warnings:
            print(f"  warnings={len(warnings)}")
        for detail in details[:8]:
            print(f"  {detail}")
        if missing or wrong:
            failures.append(f"{sample['name']} consensus failed")

    if failures:
        print("\nFAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nPASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
