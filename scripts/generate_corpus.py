#!/usr/bin/env python3
"""Regenerate tests/corpus/pass fixtures and manifest.json."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Border, Font, PatternFill, Side

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "corpus" / "pass"
MANIFEST = ROOT / "tests" / "corpus" / "manifest.json"


def save(wb: Workbook, name: str) -> None:
    path = OUT / name
    wb.save(path)
    print("wrote", path.relative_to(ROOT))


def soffice_convert(src: Path, fmt: str, dest_name: str) -> None:
    soffice = "soffice"
    subprocess.run(
        [soffice, "--headless", "--convert-to", fmt, "--outdir", str(OUT), str(src)],
        check=True,
        capture_output=True,
        text=True,
    )
    produced = OUT / f"{src.stem}.{fmt}"
    target = OUT / dest_name
    if produced != target:
        produced.replace(target)
    print("wrote", target.relative_to(ROOT))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["Name", "Qty", "Price"])
    for row in [
        ["Apple", 3, 1.5],
        ["Banana", 5, 0.8],
        ["Cherry", 2, 3.2],
        ["Date", 10, 2.1],
        ["Elderberry", 1, 4.0],
    ]:
        ws.append(row)
    save(wb, "01_simple.xlsx")

    wb = Workbook()
    wb.active.title = "Sales"
    wb.active.append(["A", "B"])
    wb.active.append([1, 2])
    inv = wb.create_sheet("Inventory")
    inv.append(["SKU", "Stock"])
    inv.append(["X1", 100])
    notes = wb.create_sheet("Notes")
    notes.append(["Note"])
    notes.append(["ok"])
    save(wb, "02_multisheet.xlsx")

    wb = Workbook()
    ws = wb.active
    ws["A1"] = 10
    ws["A2"] = 20
    ws["A3"] = "=A1+A2"
    ws["B1"] = "=SUM(A1:A2)"
    save(wb, "03_formulas.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.merge_cells("A1:C1")
    ws["A1"] = "Merged header"
    ws["A2"] = "a"
    ws["B2"] = "b"
    ws["C2"] = "c"
    save(wb, "04_merged.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append(["Number", "Date", "Percent", "Currency"])
    ws.append([1234.56, date(2026, 11, 14), 0.15, 99.99])
    ws["B2"].number_format = "YYYY-MM-DD"
    ws["C2"].number_format = "0%"
    ws["D2"].number_format = '"$"#,##0.00'
    save(wb, "05_types.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append(["Товар", "Количество", "Цена"])
    ws.append(["Яблоки", 10, 120.5])
    ws.append(["Молоко", 2, 89.0])
    save(wb, "06_russian.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append([f"Col{i}" for i in range(1, 31)])
    ws.append(list(range(1, 31)))
    save(wb, "07_wide.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append(["id", "value"])
    for i in range(1, 1001):
        ws.append([i, i * 1.5])
    save(wb, "08_tall.xlsx")

    wb = Workbook()
    ws = wb.active
    header_font = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="2E7D32")
    thin = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )
    ws.append(["Product", "Score"])
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = fill
        cell.border = thin
    ws.append(["Alpha", 9])
    ws.append(["Beta", 7])
    for row in ws.iter_rows(min_row=2, max_row=3, max_col=2):
        for cell in row:
            cell.border = thin
    save(wb, "09_styled.xlsx")

    wb = Workbook()
    wb.active.title = "Data"
    wb.active.append(["x"])
    wb.active.append([1])
    wb.create_sheet("Empty")
    save(wb, "10_empty_second_sheet.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append(["Template field", "Value"])
    ws.append(["Name", ""])
    save(wb, "11_template.xltx")

    wb = Workbook()
    ws = wb.active
    ws.append(["Item", "Flag"])
    ws.append(["demo", 1])
    src12 = OUT / "_12_macro_src.xlsx"
    wb.save(src12)

    wb = Workbook()
    ws = wb.active
    ws.append(["line"])
    for i in range(1, 6):
        ws.append([f"row-{i}"])
    save(wb, "15_csv_origin.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append(["City", "Pop", "Region"])
    for row in [["Moscow", 12, "C"], ["SPb", 5, "NW"], ["Kazan", 1, "V"]]:
        ws.append(row)
    ws.auto_filter.ref = "A1:C4"
    ws.freeze_panes = "A2"
    save(wb, "16_freeze_filter.xlsx")

    wb = Workbook()
    ws = wb.active
    ws["A1"] = "Link"
    ws["A2"] = "https://example.com"
    ws["A2"].hyperlink = "https://example.com"
    ws["A2"].style = "Hyperlink"
    save(wb, "17_hyperlinks.xlsx")

    wb = Workbook()
    ws = wb.active
    ws["A1"] = "Value"
    ws["A2"] = 42
    ws["A2"].comment = Comment("проверка комментария", "tester")
    save(wb, "18_comments.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append(["A", "B"])
    ws.append([1, 2])
    ws.append([3, 4])
    ws.print_area = "A1:B3"
    ws.page_setup.orientation = "landscape"
    save(wb, "19_print_area.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.append(["Label", "Amount", "Note"])
    ws.append(["total", 1000, "ok"])
    ws["B2"].number_format = "#,##0.00"
    ws["A2"].font = Font(bold=True)
    ws.append(["rate", 0.255, "quarter"])
    ws["B3"].number_format = "0.00%"
    save(wb, "20_mixed_formats.xlsx")

    try:
        soffice_convert(OUT / "01_simple.xlsx", "xls", "13_legacy.xls")
        soffice_convert(OUT / "01_simple.xlsx", "ods", "14_ods.ods")
        soffice_convert(src12, "xlsm", "12_macro.xlsm")
        # Round-trip OOXML through LibreOffice so openxml-audit accepts packages
        # (openpyxl often emits inlineStr / theme quirks).
        for path in sorted(OUT.glob("*")):
            if path.suffix.lower() not in {".xlsx", ".xlsm", ".xltx"}:
                continue
            if path.name.startswith("_"):
                continue
            soffice_convert(path, path.suffix.lstrip("."), path.name)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print("LibreOffice conversion failed:", exc, file=sys.stderr)
        return 1
    finally:
        if src12.exists():
            src12.unlink()

    entries = [
        {"id": "01", "file": "01_simple.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "02", "file": "02_multisheet.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "03", "file": "03_formulas.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "04", "file": "04_merged.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "05", "file": "05_types.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "06", "file": "06_russian.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "07", "file": "07_wide.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "08", "file": "08_tall.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "09", "file": "09_styled.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "10", "file": "10_empty_second_sheet.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "11", "file": "11_template.xltx", "format": "xltx", "expect": "pass"},
        {"id": "12", "file": "12_macro.xlsm", "format": "xlsm", "expect": "pass"},
        {"id": "13", "file": "13_legacy.xls", "format": "xls", "expect": "pass"},
        {"id": "14", "file": "14_ods.ods", "format": "ods", "expect": "pass"},
        {"id": "15", "file": "15_csv_origin.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "16", "file": "16_freeze_filter.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "17", "file": "17_hyperlinks.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "18", "file": "18_comments.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "19", "file": "19_print_area.xlsx", "format": "xlsx", "expect": "pass"},
        {"id": "20", "file": "20_mixed_formats.xlsx", "format": "xlsx", "expect": "pass"},
    ]
    MANIFEST.write_text(json.dumps({"pass": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", MANIFEST.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
