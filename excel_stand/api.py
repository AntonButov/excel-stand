from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from excel_stand.detect import ALLOWLIST
from excel_stand.pipeline import check_file

app = FastAPI(title="excel-stand", version="0.1.0")

MAX_BYTES = 25 * 1024 * 1024


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/check")
async def check(file: UploadFile = File(...)) -> dict:
    name = file.filename or "upload.bin"
    ext = Path(name).suffix.lower()
    if ext not in ALLOWLIST:
        raise HTTPException(status_code=400, detail=f"unsupported extension: {ext}")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="empty file")
    if len(raw) > MAX_BYTES:
        raise HTTPException(status_code=400, detail=f"file too large (max {MAX_BYTES} bytes)")

    with tempfile.TemporaryDirectory(prefix="excel-stand-api-") as tmp:
        tmp_path = Path(tmp)
        src = tmp_path / name
        src.write_bytes(raw)
        result = check_file(src, out_dir=tmp_path / "out", include_base64=True)
        return result.to_dict()
