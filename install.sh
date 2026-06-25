#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m venv .venv

.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

if [[ "${1:-}" == "--with-easyocr" ]]; then
  .venv/bin/python -m pip install -r requirements-ocr-optional.txt
fi

echo
echo "Install complete."
echo "Run with: ./run.sh"
echo
echo "OCR notes:"
echo "- Default app OCR engine is auto."
echo "- On macOS, auto can use Vision if swiftc is available."
echo "- For EasyOCR, run: ./install.sh --with-easyocr"
