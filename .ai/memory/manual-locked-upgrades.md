# Advanced Upgrade Overrides

- Infer `locked` when OCR reads a visible `Lv. 0` upgrade with `Wave`/lock text.
- Infer missing tiers beyond the visible family limit as `locked`, and infer missing tiers after a visible locked tier as `locked`.
- Keep positive-level rows `available` even if adjacent OCR text includes `Wave`, because neighboring locked buttons can contaminate OCR context.
- `Ajustes avancados` is the single persistent manual control for core upgrade `status` and `level`. It should be visible before OCR so users can prepare exceptions, but pre-OCR rows must not enable macro generation.
- Persist advanced overrides in `user_state/advanced_overrides.json` and reapply them every time the UI rebuilds state. Rebuild base rows from the current OCR results first, then apply saved overrides on top.
- Clearing an override means returning that row to the same `status` and `level` as the current rebuilt base. Saving should then remove that row from `advanced_overrides.json`.
- Optimizer conversion rules for advanced overrides: `maxed` uses known `max_level`, `locked` without a level becomes `0` and enters `locked_upgrades`, and `ignore` is omitted from optimizer state.
- If `advanced_overrides.json` is missing, import legacy `user_state/locked_upgrades.json` as `locked` overrides. Once the advanced file exists, it is the source of truth.
- Keep `user_state/` out of git. It is local runtime state, not project source.
