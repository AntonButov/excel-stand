from __future__ import annotations

from pathlib import Path

from excel_stand.detect import is_ooxml
from excel_stand.models import CheckError


def check_schema(path: Path, fmt: str) -> list[CheckError]:
    """OOXML schema validation via openxml-audit. Skipped for xls/ods."""
    if not is_ooxml(fmt):
        return []

    try:
        from openxml_audit import OpenXmlValidator
    except ImportError as exc:
        return [CheckError("schema_unavailable", f"openxml-audit not installed: {exc}")]

    try:
        validator = OpenXmlValidator()
        result = validator.validate(str(path))
    except Exception as exc:  # noqa: BLE001
        return [CheckError("schema_error", f"openxml-audit raised: {exc}")]

    errors: list[CheckError] = []
    for item in getattr(result, "errors", []) or []:
        severity = getattr(item, "severity", None)
        sev = str(getattr(severity, "value", severity) or "").upper()
        if "WARN" in sev or "INFO" in sev:
            continue
        if sev and "ERROR" not in sev:
            continue
        desc = getattr(item, "description", None) or str(item)
        errors.append(CheckError("schema_error", desc))

    # Fallback: is_valid false but severities not tagged as ERROR
    if not errors and not getattr(result, "is_valid", True):
        if int(getattr(result, "error_count", 0) or 0) > 0:
            errors.append(
                CheckError(
                    "schema_error",
                    f"openxml-audit reported {result.error_count} errors",
                )
            )
    return errors
