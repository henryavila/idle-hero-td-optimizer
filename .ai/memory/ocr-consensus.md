# OCR Consensus

- The OCR consensus should accept a level when independent layers agree or when the displayed total effect validates the visible `Lv.` value. A single unvalidated OCR layer should remain review-worthy.
- Displayed effects with suffixes such as `K` and `M` are rounded. They may validate a visible level within display precision, but should not always infer an exact level by themselves.
- PaddleOCR/PP-OCRv5 is useful as an optional extra layer, but not as the primary engine. In fixture comparisons it produced helpful agreement on some hard cases and false positives on others.
- When PaddleOCR is available, use `PP-OCRv5_server_det` plus `PP-OCRv5_server_rec` and include only its `auto-lines` records in consensus. Do not include Paddle `layout-slots` unless future fixtures prove it is reliable.
