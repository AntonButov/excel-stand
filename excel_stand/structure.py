from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook

from excel_stand.detect import is_ooxml
from excel_stand.models import CheckError


def check_structure(path: Path, fmt: str) -> tuple[list[str], list[CheckError]]:
    """Return (sheet_names, errors). Non-OOXML: skip deep parse, sheets unknown until LO."""
    if not is_ooxml(fmt):
        return [], []

    try:
        wb = load_workbook(path, read_only=True, data_only=False)
    except Exception as exc:  # noqa: BLE001 — surface as structured error
        return [], [CheckError("bad_ooxml", f"openpyxl failed to open: {exc}")]

    try:
        names = list(wb.sheetnames)
        if not names:
            return [], [CheckError("no_sheets", "workbook has no sheets")]

        has_value = False
        for name in names:
            ws = wb[name]
            for row in ws.iter_rows(max_row=200, max_col=50, values_only=True):
                if any(cell is not None and str(cell).strip() != "" for cell in row):
                    has_value = True
                    break
            if has_value:
                break

        if not has_value:
            return names, [CheckError("empty_workbook", "no non-empty cells found")]
        return names, []
    finally:
        wb.close()
