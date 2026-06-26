#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m venv .venv

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

if [[ "${1:-}" == "--with-easyocr" || "${1:-}" == "--with-ocr" ]]; then
  .venv/bin/python -m pip install -r requirements-ocr-optional.txt
fi

echo
echo "Install complete."
echo "Run with: ./run.sh"
echo
echo "OCR notes:"
echo "- Default app OCR engine is consensus."
echo "- On macOS, auto can use Vision if swiftc is available."
echo "- For EasyOCR and PaddleOCR, run: ./install.sh --with-ocr"
