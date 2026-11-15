# Excel Stand design

> Date: 2026-11-14 · Status: approved

## Goal

Open-source QA stand: upload a spreadsheet, validate it, open it in LibreOffice, return JSON + PNG screenshot of the first page.

## Scope (v1)

- Formats: `.xlsx`, `.xlsm`, `.xltx`, `.xls`, `.ods`
- Steps: detect → structure (OOXML via openpyxl) → schema (`openxml-audit` for OOXML only) → LibreOffice PDF → PNG
- Interfaces: CLI `excel-stand check`, HTTP `POST /check`, GitHub Actions corpus gate
- Corpus: 20 pass fixtures must succeed on every commit

## Out of scope

- Microsoft Excel / Windows COM
- Production VPS deploy
- PDF→Excel conversion
- External SaaS validators
