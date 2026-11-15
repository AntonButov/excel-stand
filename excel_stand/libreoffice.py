from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def find_soffice() -> str | None:
    env = os.environ.get("SOFFICE_PATH")
    if env and Path(env).exists():
        return env
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    mac = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
    if mac.exists():
        return str(mac)
    return None


def libreoffice_version(soffice: str | None = None) -> str | None:
    binary = soffice or find_soffice()
    if not binary:
        return None
    try:
        proc = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        line = (proc.stdout or proc.stderr or "").strip().splitlines()
        return line[0] if line else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def convert_to_pdf(
    source: Path,
    out_dir: Path,
    *,
    timeout_s: int = 60,
    soffice: str | None = None,
) -> tuple[Path | None, str | None]:
    """Convert spreadsheet to PDF. Returns (pdf_path, error_code)."""
    binary = soffice or find_soffice()
    if not binary:
        return None, "libreoffice_missing"

    out_dir.mkdir(parents=True, exist_ok=True)
    profile = Path(tempfile.mkdtemp(prefix="excel-stand-lo-"))
    try:
        env_user = f"file://{profile}"
        cmd = [
            binary,
            f"-env:UserInstallation={env_user}",
            "--headless",
            "--norestore",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_dir),
            str(source.resolve()),
        ]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_s,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return None, "timeout"

        pdf = out_dir / f"{source.stem}.pdf"
        if proc.returncode != 0 or not pdf.exists() or pdf.stat().st_size == 0:
            detail = (proc.stderr or proc.stdout or "").strip()[:500]
            return None, f"libreoffice_fail:{detail}" if detail else "libreoffice_fail"
        return pdf, None
    finally:
        shutil.rmtree(profile, ignore_errors=True)
