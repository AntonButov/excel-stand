from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class CheckError:
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class EngineInfo:
    libreoffice_version: str | None = None
    soffice_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CheckResult:
    ok: bool
    format: str
    sheets: list[str] = field(default_factory=list)
    errors: list[CheckError] = field(default_factory=list)
    engine: EngineInfo = field(default_factory=EngineInfo)
    screenshot_path: str | None = None
    screenshot_base64: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "format": self.format,
            "sheets": self.sheets,
            "errors": [e.to_dict() for e in self.errors],
            "engine": self.engine.to_dict(),
            "screenshot_path": self.screenshot_path,
            "screenshot_base64": self.screenshot_base64,
        }
