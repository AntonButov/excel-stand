from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def pdf_to_png(pdf: Path, png_path: Path) -> str | None:
    """Render first PDF page to PNG. Prefer pdftoppm; fallback to PyMuPDF."""
    png_path.parent.mkdir(parents=True, exist_ok=True)

    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm:
        prefix = png_path.with_suffix("")
        try:
            proc = subprocess.run(
                [pdftoppm, "-png", "-f", "1", "-l", "1", "-singlefile", str(pdf), str(prefix)],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return "screenshot_fail:pdftoppm timeout"
        if proc.returncode != 0 or not png_path.exists() or png_path.stat().st_size == 0:
            return "screenshot_fail:pdftoppm"
        return None

    try:
        import pymupdf
    except ImportError:
        return "screenshot_fail:no_pdftoppm_or_pymupdf"

    try:
        doc = pymupdf.open(pdf)
        try:
            if doc.page_count < 1:
                return "screenshot_fail:empty_pdf"
            page = doc[0]
            pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
            pix.save(png_path)
        finally:
            doc.close()
    except Exception as exc:  # noqa: BLE001
        return f"screenshot_fail:{exc}"

    if not png_path.exists() or png_path.stat().st_size == 0:
        return "screenshot_fail:empty_png"
    return None
