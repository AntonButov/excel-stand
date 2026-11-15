from pathlib import Path

from excel_stand.detect import detect_format
from excel_stand.structure import check_structure

CORPUS = Path(__file__).parent / "corpus" / "pass"


def test_detect_simple_xlsx():
    fmt, err = detect_format(CORPUS / "01_simple.xlsx")
    assert err is None
    assert fmt == "xlsx"


def test_structure_simple_xlsx():
    sheets, errors = check_structure(CORPUS / "01_simple.xlsx", "xlsx")
    assert errors == []
    assert "Sheet1" in sheets


def test_detect_ods():
    fmt, err = detect_format(CORPUS / "14_ods.ods")
    assert err is None
    assert fmt == "ods"
