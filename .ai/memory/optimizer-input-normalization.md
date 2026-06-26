# Optimizer Input Normalization

- Streamlit/Pandas can return manually reviewed upgrade levels as integer-valued floats such as `499028.0`. Treat those as exact integers before any string separator logic.
- Do not blindly strip `.` from all level inputs. That turns editor floats like `499028.0` into `4990280` and sends inflated levels to the optimizer.
- OCR can emit game-formatted thousands such as `499.028`; manual entry may also use `499,028`. UI level coercion should accept both as thousands only when the separator groups are exactly three digits.
- Resource inputs use game-number parsing. Keep both decimal suffix formats valid: `20,258k` and `20.258k` should parse to the same value.
