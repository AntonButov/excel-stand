from __future__ import annotations

import base64
import tempfile
from pathlib import Path

from excel_stand.detect import detect_format
from excel_stand.libreoffice import convert_to_pdf, find_soffice, libreoffice_version
from excel_stand.models import CheckError, CheckResult, EngineInfo
from excel_stand.schema import check_schema
from excel_stand.screenshot import pdf_to_png
from excel_stand.structure import check_structure


def check_file(
    path: Path | str,
    *,
    out_dir: Path | str | None = None,
    include_base64: bool = False,
    timeout_s: int = 60,
) -> CheckResult:
    source = Path(path)
    work = Path(out_dir) if out_dir else Path(tempfile.mkdtemp(prefix="excel-stand-out-"))
    work.mkdir(parents=True, exist_ok=True)

    soffice = find_soffice()
    engine = EngineInfo(
        libreoffice_version=libreoffice_version(soffice),
        soffice_path=soffice,
    )

    if not source.exists():
        return CheckResult(
            ok=False,
            format="unknown",
            errors=[CheckError("not_found", f"file not found: {source}")],
            engine=engine,
        )

    fmt, detect_err = detect_format(source)
    if detect_err or not fmt:
        return CheckResult(
            ok=False,
            format=source.suffix.lstrip(".") or "unknown",
            errors=[CheckError(detect_err or "unsupported_format", f"cannot detect format for {source.name}")],
            engine=engine,
        )

    errors: list[CheckError] = []
    sheets, struct_errors = check_structure(source, fmt)
    errors.extend(struct_errors)
    errors.extend(check_schema(source, fmt))

    if errors:
        return CheckResult(ok=False, format=fmt, sheets=sheets, errors=errors, engine=engine)

    pdf, lo_err = convert_to_pdf(source, work / "pdf", timeout_s=timeout_s, soffice=soffice)
    if lo_err or pdf is None:
        code = "timeout" if lo_err == "timeout" else "libreoffice_fail"
        if lo_err == "libreoffice_missing":
            code = "libreoffice_missing"
        msg = lo_err or "libreoffice_fail"
        if msg.startswith("libreoffice_fail:"):
            msg = msg.split(":", 1)[1] or "libreoffice_fail"
        errors.append(CheckError(code, msg))
        return CheckResult(ok=False, format=fmt, sheets=sheets, errors=errors, engine=engine)

    png_path = work / f"{source.stem}.png"
    shot_err = pdf_to_png(pdf, png_path)
    if shot_err:
        errors.append(CheckError("screenshot_fail", shot_err))
        return CheckResult(ok=False, format=fmt, sheets=sheets, errors=errors, engine=engine)

    b64: str | None = None
    if include_base64:
        b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")

    return CheckResult(
        ok=True,
        format=fmt,
        sheets=sheets,
        errors=[],
        engine=engine,
        screenshot_path=str(png_path),
        screenshot_base64=b64,
    )
