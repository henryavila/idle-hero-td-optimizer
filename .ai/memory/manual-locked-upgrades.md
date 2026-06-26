# Manual Locked Upgrades

- Do not infer `locked` from OCR text or missing tiers. Treat `Wave`/lock text as review unless the user explicitly marks the upgrade locked.
- Persist manual locked selections in `user_state/locked_upgrades.json` and reapply them to future OCR state rows.
- Keep `user_state/` out of git. It is local runtime state, not project source.
