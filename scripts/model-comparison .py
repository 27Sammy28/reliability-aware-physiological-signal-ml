"""Generate a clearly labeled synthetic model-comparison table."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.experiment import ExperimentConfig, run_experiment


def format_metric(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def clean_baseline_row(rows: list[dict[str, object]]) -> dict[str, object]:
    for row in rows:
        if (
            float(row.get("noise_level", 0.0)) == 0.0
            and float(row.get("missing_rate", 0.0)) == 0.0
            and float(row.get("segment_fraction", 0.0)) == 0.0
        ):
            return row
    if not rows:
        raise ValueError("No experiment rows generated")
    return rows[0]


def comparison_markdown(row: dict[str, object]) -> str:
    lines = [
        "# Synthetic Smoke-Test Model Comparison",
        "",
        "This table is a template for reporting model comparisons.",
        "The current synthetic ECG-like smoke-test dataset is too simple and can produce artificially perfect scores.",
        "For that reason, numeric benchmark claims are marked as pending until MIT-BIH or a harder validation split is evaluated.",
        "",
        "| Model | Accuracy | F1 Score | AUROC | AUPRC | Status |",
        "|---|---:|---:|---:|---:|---|",
        "| Logistic Regression GD | Pending | Pending | Pending | Pending | Implemented; requires real-data evaluation |",
        "| Random Forest | -- | -- | -- | -- | Planned baseline |",
        "| XGBoost | -- | -- | -- | -- | Planned baseline |",
        "| Reliability-Aware Model | Pending | Pending | Pending | Pending | Reliability pipeline implemented; benchmark pending |",
        "",
        "Do not report the synthetic smoke-test scores as model performance. Use this file as a results table template until dataset-backed metrics are generated.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a synthetic model-comparison Markdown table.")
    parser.add_argument("--output", default="results/metrics/model_comparison.md")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rows = run_experiment(ExperimentConfig(use_synthetic=True, seed=args.seed, noise_levels=(0.0,)))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(comparison_markdown(clean_baseline_row(rows)))
    print(f"Wrote synthetic model comparison: {output}")


if __name__ == "__main__":
    main()
