"""Validate downloaded Kaggle MIT-BIH files and write a manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.schema import validate_mitbih_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate MIT-BIH CSV schema and file manifest.")
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--output", default="results/data_validation.json")
    args = parser.parse_args()
    report = validate_mitbih_directory(args.raw_dir)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Wrote validation report to {output}")


if __name__ == "__main__":
    main()
