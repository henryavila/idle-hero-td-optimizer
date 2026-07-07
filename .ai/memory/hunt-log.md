# Hunt Log

## 2026-06-26 - `ui.app.build_state_rows`

- Added adversarial coverage in `scripts/test_ui_state_conversion.py` for locked/maxed/review state conversion.
- Covered visible `Lv. 0` Wave locks, positive-level rows contaminated by adjacent Wave text, missing tiers after visible locks, missing tiers beyond visible limits, non-contiguous visible runs, ambiguous gaps, and manual locked overrides.
- No deferred bugs remain from this hunt.

## 2026-07-07 - `optimize_farm_upgrades.build_weights` and `optimize`

- Added adversarial coverage in `scripts/test_optimizer_target_metrics.py` for metric-based optimizer target selection.
- Covered compatibility presets, explicit targets overriding legacy farm fields, target weight overrides, unknown target rejection, exclusion of unselected metrics even with better ROI, weighted greedy choice, separate resource budgets, CLI rejection for no active target, and large single-target batching.
- Use small synthetic upgrades for ROI/efficiency tests so expected purchases come from the domain rule rather than from APK fixture magnitudes.
- No deferred bugs remain from this hunt.
