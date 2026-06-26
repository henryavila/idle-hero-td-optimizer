# Manual Locked Upgrades

- Infer `locked` when OCR reads a visible `Lv. 0` upgrade with `Wave`/lock text.
- Infer missing tiers beyond the visible family limit as `locked`, and infer missing tiers after a visible locked tier as `locked`.
- Keep positive-level rows `available` even if adjacent OCR text includes `Wave`, because neighboring locked buttons can contaminate OCR context.
- Persist manual locked selections in `user_state/locked_upgrades.json` and reapply them to future OCR state rows as corrections or explicit overrides.
- Keep `user_state/` out of git. It is local runtime state, not project source.
