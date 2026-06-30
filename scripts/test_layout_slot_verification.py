#!/usr/bin/env python3
"""Regression checks for layout-slot / auto-detect tier confidence.

These capture the root cause of three consensus errors reported on sample/4
(prestige screen):

* prestigeDmg4   conflicting 0 vs 1975   -> layout slot read the wrong row
  ("AD + ULTRA CRIT CHANCE", no tier) and emitted it via slot_fallback.
* prestigeKillGold3 untrusted 36 vs 71153 -> layout slot read "KILL GOLD (Lv.36)"
  (which is tier V) and emitted it as tier 3 via slot_fallback.
* prestigeDmg1   untrusted 619726         -> auto-detect labeled the DAMAGE II row
  (Lv 619726) as tier 1 because total-effect tier (1) overrode the label tier (2).

The fix: a slot may only emit a key when the tier is confirmable from the text
(never a positional slot_fallback), and auto-detect must prefer the label tier
over the back-computed total-effect tier.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import extract_upgrade_levels_from_image as ocr  # noqa: E402


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def slot(family: str, tier: int) -> ocr.LayoutSlot:
    return ocr.LayoutSlot(family, [0.0, 0.0, 1.0, 1.0], tier)


def test_slot_rejects_wrong_family_fallback() -> None:
    """prestigeDmg4 root cause: slot reads 'ULTRA CRIT CHANCE' (wrong family, no tier)."""
    key, source = ocr.slot_key_info(
        slot("prestigeDmg", 4),
        "AD + ULTRA CRIT CHANCE (Lv: 0) WAVE IOK +0%",
    )
    assert_equal(key, None, "prestigeDmg4 slot must not emit a wrong-family fallback")
    assert_equal(source, None, "prestigeDmg4 slot source must be None for wrong family")

    # A damage slot must likewise refuse a kill-gold row that landed in it.
    key, source = ocr.slot_key_info(
        slot("prestigeDmg", 3),
        "KILL GOLD (Lv.36) 1.16E+22 +2.700% (+8.400%) (x112)",
    )
    assert_equal(key, None, "prestigeDmg slot must not emit a kill-gold fallback")
    assert_equal(source, None, "prestigeDmg slot source must be None for kill-gold row")


def test_slot_keeps_same_family_fallback() -> None:
    """Regression guard: a same-family row with a garbled tier keeps its fallback.

    The wrong-tier 'KILL GOLD (Lv.36)' read by a prestigeKillGold slot is still a
    kill-gold row, so the fallback is emitted (the consensus then rejects the
    unvalidated level). This preserves aligned screenshots whose Roman numeral
    was OCR-garbled (samples 1/3 relied on this)."""
    assert_equal(
        ocr.slot_key_info(
            slot("prestigeKillGold", 3),
            "KILL GOLD (Lv.36) 1.16E+22 +2.700% (+8.400%) (x112)",
        ),
        ("prestigeKillGold3", "slot_fallback"),
        "prestigeKillGold fallback must stay for a same-family row",
    )


def test_slot_with_confirmable_tier_still_emits() -> None:
    """Regression guard: a row whose tier IS readable must still map to its key."""
    assert_equal(
        ocr.slot_key_info(slot("prestigeKillGold", 5), "KILL Gozd V (Lv 36) 116E+22"),
        ("prestigeKillGold5", "label"),
        "prestigeKillGold5 label-tier reading must still emit",
    )
    assert_equal(
        ocr.slot_key_info(slot("prestigeKillGold", 6), "KILL GOLD VI (Lv 0) WAVE 8000"),
        ("prestigeKillGold6", "label"),
        "prestigeKillGold6 label-tier reading must still emit",
    )


def test_damage_total_effect_tolerates_ocr_letter_o() -> None:
    """prestigeDmg1 root cause: OCR garbled '6,20M%' to '6,2OM%' (0->O).

    The total-effect tier back-computes the tier from effect/level. With the O
    unread, the effect regex skipped '+6,2OM%' and matched '+3,80M%' instead,
    computing tier 1 and labeling the DAMAGE II row (Lv 619726) as prestigeDmg1.
    parse_level_int already maps O->0; the effect parser must too."""
    ppl = ocr.load_percent_per_level()
    label_text = "DAMAGE I1 (Lv. 619.726)"
    context_text = "DAMAGE I1 (Lv. 619.726) 6.48E+21 +6,2OM% (+3,80M%380273}"
    assert_equal(ocr.parse_display_number("6,2OM"), 6_200_000.0, "OCR O must read as 0 in effect numbers")
    assert_equal(
        ocr.tier_from_total_effect("prestigeDmg", context_text, ppl, 619726),
        2,
        "DAMAGE II total-effect tier must be 2 (effect 6.2M / 10% per level)",
    )
    key = ocr.key_for_detected_context("prestige-core", label_text, context_text, ppl)
    assert_equal(key, "prestigeDmg2", "DAMAGE II row must map to prestigeDmg2, not prestigeDmg1")


def test_killgold_label_tolerates_ocr_garbling() -> None:
    """prestigeKillGold3 root cause: 'KELL GOLD' (I->E) was dropped by classify_metric.

    The correct level 11153 is math-recoverable (effect 278,83K% / 25% per level),
    but only if the row is classified kill_gold so auto-detect emits it. The
    special 'ULTRA GOLD AMOUNT/CHANCE' rows must still be excluded (no k-word)."""
    assert_equal(
        ocr.classify_metric("KELL GOLD TIT (Lv. 11.153) 1.17E+22 +278,83K%"),
        "kill_gold",
        "OCR-garbled KELL GOLD must classify as kill_gold",
    )
    assert_equal(
        ocr.classify_metric("KTLL GOLD TT (Lv. 342.153)"),
        "kill_gold",
        "OCR-garbled KTLL GOLD must classify as kill_gold",
    )
    assert_equal(
        ocr.classify_metric("AD + ULTRA GOLD AMOUNT (Lv. O)"),
        None,
        "ULTRA GOLD AMOUNT special must not classify as kill_gold",
    )
    assert_equal(
        ocr.classify_metric("AD + ULTRA GOLD CHANCE (Lv. O)"),
        None,
        "ULTRA GOLD CHANCE special must not classify as kill_gold",
    )


def test_prestige_killgold3_resolves_via_math_validation() -> None:
    """End-to-end: prestigeKillGold3 -> 11153 (math-validated) beats paddle's 71153."""
    ppl = ocr.load_percent_per_level()
    text = "KELL GOLD TIT (Lv. 11.153) 1.17E+22 +278,83K% (+1,86M%)"
    key = ocr.key_for_detected_context("prestige-core", text, text, ppl)
    assert_equal(key, "prestigeKillGold3", "KELL GOLD III row must map to prestigeKillGold3")
    candidates = [
        {"upgrade_key": "prestigeKillGold3", "engine": "vision", "strategy": "auto-lines",
         "source": "level_text", "level": 11153, "text": text, "key_source": "auto_label"},
        {"upgrade_key": "prestigeKillGold3", "engine": "paddle", "strategy": "auto-lines",
         "source": "level_text", "level": 71153, "text": "KILL GOLD III (Lv.71.153)", "key_source": "auto_label"},
        {"upgrade_key": "prestigeKillGold3", "engine": "vision", "strategy": "layout-slots",
         "source": "layout_level_text", "level": 36, "text": "KILL GOLD (Lv.36)", "key_source": "slot_fallback"},
    ]
    merged, warnings = ocr.merge_ensemble_records(candidates, ["prestigeKillGold3"])
    assert_equal(merged[0].get("level"), 11153, "prestigeKillGold3 must resolve to 11153")
    assert_equal(warnings, [], "prestigeKillGold3 must produce no consensus warning")


def test_absent_tier_in_detected_family_is_silent() -> None:
    """A tier absent from the screen (family otherwise visible) resolves to None
    without a 'consensus level not found' warning -- prestigeDmg1/7 when II-VI show."""
    candidates = [
        {"upgrade_key": "prestigeDmg2", "engine": "easyocr", "strategy": "auto-lines",
         "source": "level_text", "level": 619726, "text": "DAMAGE II (Lv.619726)", "key_source": "auto_label"},
    ]
    merged, warnings = ocr.merge_ensemble_records(candidates, ["prestigeDmg1", "prestigeDmg2"])
    levels = {m["upgrade_key"]: m.get("level") for m in merged}
    assert_equal(levels.get("prestigeDmg1"), None, "absent prestigeDmg1 must resolve to None")
    assert not any("prestigeDmg1" in w for w in warnings), \
        f"absent tier in a detected family must not warn: {warnings}"


def test_wholly_missed_family_still_warns() -> None:
    """A family nothing detected is a real OCR miss, not an absent tier -- keep the warning."""
    merged, warnings = ocr.merge_ensemble_records([], ["prestigeDmg1"])
    assert_equal(merged[0].get("level"), None, "missed prestigeDmg1 resolves to None")
    assert_equal(
        warnings,
        ["consensus level not found for prestigeDmg1"],
        "a wholly-missed family must still warn",
    )


def main() -> int:
    test_slot_rejects_wrong_family_fallback()
    test_slot_keeps_same_family_fallback()
    test_slot_with_confirmable_tier_still_emits()
    test_damage_total_effect_tolerates_ocr_letter_o()
    test_killgold_label_tolerates_ocr_garbling()
    test_prestige_killgold3_resolves_via_math_validation()
    test_absent_tier_in_detected_family_is_silent()
    test_wholly_missed_family_still_warns()
    print("layout slot / tier confidence regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
