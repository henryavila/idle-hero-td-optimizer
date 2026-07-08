# Optimizer Input Normalization

- Streamlit/Pandas can return manually reviewed upgrade levels as integer-valued floats such as `499028.0`. Treat those as exact integers before any string separator logic.
- Do not blindly strip `.` from all level inputs. That turns editor floats like `499028.0` into `4990280` and sends inflated levels to the optimizer.
- OCR can emit game-formatted thousands such as `499.028`; manual entry may also use `499,028`. UI level coercion should accept both as thousands only when the separator groups are exactly three digits.
- Resource inputs use game-number parsing. Keep both decimal suffix formats valid: `20,258k` and `20.258k` should parse to the same value.
- Objective selection is now metric-based: `DMG` maps to `damage`, `Gold` maps to `kill_gold`, and `Prestige` maps to `prestige_power`. `FARM` is the compatibility preset for `damage + prestige_power`; `GOLD_PREP` is the compatibility preset for `kill_gold`.
- When `target_metrics` is explicit, legacy `farm.weights` must not override selected targets. Use `target_weights` for intentional per-target strength overrides.
- Persist the UI's last optimizer target selection in `user_state/target_metrics.json` after a successful macro generation, and use it as the next Streamlit multiselect default. Keep that file local runtime state, not source.
