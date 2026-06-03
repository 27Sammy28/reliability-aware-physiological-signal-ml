"""Generate metrics, figures, and report from downloaded MIT-BIH data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data import load_mitbih_csv
from src.experiment import ExperimentConfig, run_experiment
from src.figures import ensure_output_dir, plot_class_distribution, plot_representative_waveforms, plot_robustness_curve
from src.reporting import write_csv, write_markdown_summary
from src.results import write_reliability_report
from src.schema import validate_mitbih_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate real-data MIT-BIH reliability outputs after Kaggle download.")
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--positive-class", type=int, default=1)
    args = parser.parse_args()

    validate_mitbih_directory(args.raw_dir)
    x_train, y_train_raw, _, _ = load_mitbih_csv(args.raw_dir)
    results_dir = Path(args.results_dir)
    figures_dir = ensure_output_dir(results_dir / "figures")
    rows = run_experiment(
        ExperimentConfig(
            raw_dir=args.raw_dir,
            use_synthetic=False,
            positive_class=args.positive_class,
            noise_levels=(0.0, 0.05, 0.1, 0.2, 0.4),
            missing_rates=(0.0, 0.1),
            segment_fractions=(0.0,),
        )
    )
    figure_paths = [
        plot_class_distribution(y_train_raw, figures_dir / "real_class_distribution.png"),
        plot_representative_waveforms(x_train, y_train_raw, figures_dir / "real_representative_waveforms.png"),
        plot_robustness_curve(rows, "accuracy", figures_dir / "real_robustness_accuracy_curve.png"),
        plot_robustness_curve(rows, "ece", figures_dir / "real_robustness_ece_curve.png"),
    ]
    write_csv(rows, results_dir / "real_metrics.csv")
    write_markdown_summary(rows, results_dir / "real_summary.md")
    report_path = write_reliability_report(rows, results_dir / "real_reliability_report.md", figure_paths=figure_paths, title="MIT-BIH Reliability Report")
    print(f"Wrote real-data report: {report_path}")


if __name__ == "__main__":
    main()
