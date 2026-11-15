from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from excel_stand.pipeline import check_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="excel-stand", description="Validate Excel file and capture LibreOffice screenshot")
    sub = parser.add_subparsers(dest="command", required=True)

    check_p = sub.add_parser("check", help="Check a spreadsheet file")
    check_p.add_argument("file", type=Path, help="Path to .xlsx/.xlsm/.xltx/.xls/.ods")
    check_p.add_argument("--out-dir", type=Path, default=Path("out"), help="Directory for PDF/PNG/JSON")
    check_p.add_argument("--timeout", type=int, default=60, help="LibreOffice timeout seconds")
    check_p.add_argument("--base64", action="store_true", help="Include screenshot_base64 in JSON")

    args = parser.parse_args(argv)
    if args.command == "check":
        args.out_dir.mkdir(parents=True, exist_ok=True)
        result = check_file(
            args.file,
            out_dir=args.out_dir,
            include_base64=args.base64,
            timeout_s=args.timeout,
        )
        report = args.out_dir / f"{args.file.stem}.json"
        payload = result.to_dict()
        if not args.base64:
            payload.pop("screenshot_base64", None)
        report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if result.ok else 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
