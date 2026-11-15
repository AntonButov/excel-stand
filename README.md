# excel-stand

QA stand for spreadsheet files: **validate → open in LibreOffice → PNG screenshot**.

Open source. Used as an internal quality gate for PDF→Excel work.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# requires LibreOffice (`soffice`) on PATH
excel-stand check tests/corpus/pass/01_simple.xlsx --out-dir out
```

HTTP service:

```bash
docker compose up --build
curl -F "file=@tests/corpus/pass/01_simple.xlsx" http://localhost:8080/check
```

## Corpus gate

`tests/corpus/pass/` holds **20** known-good files (xlsx / xltx / xlsm / xls / ods).  
CI runs the full pipeline on every push/PR — all must return `ok: true`.

```bash
pytest -q
```

## API

`POST /check` — multipart file upload → JSON:

```json
{
  "ok": true,
  "format": "xlsx",
  "sheets": ["Sheet1"],
  "errors": [],
  "engine": {"libreoffice_version": "...", "soffice_path": "..."},
  "screenshot_path": "...",
  "screenshot_base64": "..."
}
```

## License

MIT
