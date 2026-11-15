from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from excel_stand.pipeline import check_file

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests" / "corpus" / "manifest.json"
PASS_DIR = ROOT / "tests" / "corpus" / "pass"
SHOTS = ROOT / "out" / "corpus-screenshots"


def _entries() -> list[dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return data["pass"]


@pytest.fixture(scope="session")
def require_soffice():
    if not shutil.which("soffice") and not Path(
        "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    ).exists():
        pytest.skip("LibreOffice soffice not available")


@pytest.mark.libreoffice
@pytest.mark.parametrize("entry", _entries(), ids=lambda e: e["id"])
def test_corpus_pass(entry: dict, require_soffice, tmp_path: Path):
    path = PASS_DIR / entry["file"]
    assert path.exists(), f"missing fixture {path}"
    out = tmp_path / entry["id"]
    result = check_file(path, out_dir=out, include_base64=False, timeout_s=120)
    assert result.ok, f"{entry['file']} failed: {[e.to_dict() for e in result.errors]}"
    assert result.screenshot_path
    png = Path(result.screenshot_path)
    assert png.exists() and png.stat().st_size > 0

    SHOTS.mkdir(parents=True, exist_ok=True)
    dest = SHOTS / f"{entry['id']}_{path.stem}.png"
    dest.write_bytes(png.read_bytes())


def test_manifest_has_20():
    assert len(_entries()) == 20
