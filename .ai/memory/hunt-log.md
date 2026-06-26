# Hunt Log

## 2026-06-26 - `ui.app.build_state_rows`

- Added adversarial coverage in `scripts/test_ui_state_conversion.py` for locked/maxed/review state conversion.
- Covered visible `Lv. 0` Wave locks, positive-level rows contaminated by adjacent Wave text, missing tiers after visible locks, missing tiers beyond visible limits, non-contiguous visible runs, ambiguous gaps, and manual locked overrides.
- No deferred bugs remain from this hunt.
