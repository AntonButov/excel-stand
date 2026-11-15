from __future__ import annotations

from pathlib import Path

OOXML_EXTS = {".xlsx", ".xlsm", ".xltx"}
ALLOWLIST = OOXML_EXTS | {".xls", ".ods"}

# Magic bytes
ZIP_MAGIC = b"PK\x03\x04"
OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def detect_format(path: Path) -> tuple[str | None, str | None]:
    """Return (format_ext_without_dot, error_code_or_None)."""
    ext = path.suffix.lower()
    if ext not in ALLOWLIST:
        return None, "unsupported_format"

    head = path.read_bytes()[:8]
    if ext in OOXML_EXTS or ext == ".ods":
        if not head.startswith(ZIP_MAGIC):
            return None, "not_zip"
        return ext.lstrip("."), None
    if ext == ".xls":
        if not head.startswith(OLE_MAGIC) and not head.startswith(ZIP_MAGIC):
            # Some .xls are mislabeled; still try LO later if OLE-ish fails hard
            return None, "bad_xls_magic"
        return "xls", None
    return None, "unsupported_format"


def is_ooxml(fmt: str) -> bool:
    return f".{fmt}" in OOXML_EXTS
