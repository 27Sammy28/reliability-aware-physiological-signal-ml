"""Remove generated local artifacts while preserving source files and placeholders."""

from __future__ import annotations

from pathlib import Path
import shutil

PATHS = [
    ".pytest_cache",
    "scripts/__pycache__",
    "src/__pycache__",
    "tests/__pycache__",
    "results/figures",
    "results/metrics.csv",
    "results/summary.md",
    "results/reliability_report.md",
    "results/synthetic_metrics.csv",
    "results/synthetic_summary.md",
    "results/eda_summary.json",
    "results/smoke_metrics.csv",
    "results/smoke_summary.md",
    "main.aux",
    "main.fdb_latexmk",
    "main.fls",
    "main.log",
    "main.out",
    "main.pdf",
    "main.synctex",
]


def main() -> None:
    for item in PATHS:
        path = Path(item)
        if not path.exists():
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    print("Cleaned generated artifacts.")


if __name__ == "__main__":
    main()
