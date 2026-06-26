#!/usr/bin/env python3
"""Regression checks for uploaded image preview actions."""

from __future__ import annotations

import base64
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui import app  # noqa: E402


class DummyUpload:
    type = "image/png"

    def __init__(self, payload: bytes) -> None:
        self._payload = payload

    def getbuffer(self) -> memoryview:
        return memoryview(self._payload)


def capture_preview_html(payload: bytes = b"fake-png", caption: str = "Research <Print>") -> str:
    captured: dict[str, Any] = {}
    original_image = app.st.image
    original_html = app.components.html

    def fake_image(*args: Any, **kwargs: Any) -> None:
        captured["image_args"] = args
        captured["image_kwargs"] = kwargs

    def fake_html(html: str, *args: Any, **kwargs: Any) -> None:
        captured["html"] = html
        captured["html_args"] = args
        captured["html_kwargs"] = kwargs

    app.st.image = fake_image
    app.components.html = fake_html
    try:
        app.show_upload_preview(DummyUpload(payload), caption)
    finally:
        app.st.image = original_image
        app.components.html = original_html

    if "html" not in captured:
        raise AssertionError("preview did not render an HTML open action")
    if captured.get("image_kwargs", {}).get("width") != app.THUMBNAIL_WIDTH:
        raise AssertionError("preview thumbnail width changed")
    return str(captured["html"])


def test_preview_opens_blob_page_instead_of_top_level_data_url() -> None:
    html = capture_preview_html()
    if 'href="data:' in html or "href='data:" in html:
        raise AssertionError("preview must not navigate the new tab directly to a data: URL")
    if "URL.createObjectURL" not in html:
        raise AssertionError("preview must open a browser object URL")
    if "window.open" not in html:
        raise AssertionError("preview must still open the image in a new tab")


def test_preview_keeps_original_mime_and_bytes_in_embedded_image() -> None:
    payload = b"\x89PNG\r\npreview"
    html = capture_preview_html(payload=payload)
    expected_data_url = "data:image/png;base64," + base64.b64encode(payload).decode("ascii")
    if expected_data_url not in html:
        raise AssertionError("preview did not embed the original image bytes and MIME type")


def test_preview_escapes_caption_inside_generated_page() -> None:
    html = capture_preview_html(caption='Research "main" <script>')
    if "&lt;script&gt;" not in html:
        raise AssertionError("caption must be HTML-escaped inside the generated preview page")
    if 'Research "main" <script>' in html or 'Research \\"main\\" <script>' in html:
        raise AssertionError("raw caption HTML leaked into the generated preview page")


def test_streamlit_container_width_deprecation_is_not_used() -> None:
    source = (PROJECT_ROOT / "ui" / "app.py").read_text(encoding="utf-8")
    if "use_container_width" in source:
        raise AssertionError("replace deprecated use_container_width with width='stretch'")


def main() -> int:
    test_preview_opens_blob_page_instead_of_top_level_data_url()
    test_preview_keeps_original_mime_and_bytes_in_embedded_image()
    test_preview_escapes_caption_inside_generated_page()
    test_streamlit_container_width_deprecation_is_not_used()
    print("ui upload preview regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
