"""Generate synthetic metrics, figures, and a reliability report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data import synthetic_ecg_dataset
from src.experiment import ExperimentConfig, run_experiment
from src.figures import ensure_output_dir, plot_class_distribution, plot_representative_waveforms, plot_robustness_curve
from src.reporting import write_csv, write_markdown_summary
from src.results import write_reliability_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic results and reliability report.")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    figures_dir = ensure_output_dir(results_dir / "figures")
    x, y = synthetic_ecg_dataset(seed=args.seed)
    rows = run_experiment(
        ExperimentConfig(
            use_synthetic=True,
            seed=args.seed,
            noise_levels=(0.0, 0.05, 0.1, 0.2, 0.4),
            missing_rates=(0.0, 0.1),
            segment_fractions=(0.0,),
        )
    )
    figure_paths = [
        plot_class_distribution(y, figures_dir / "class_distribution.png"),
        plot_representative_waveforms(x, y, figures_dir / "representative_waveforms.png"),
        plot_robustness_curve(rows, "accuracy", figures_dir / "robustness_accuracy_curve.png"),
        plot_robustness_curve(rows, "ece", figures_dir / "robustness_ece_curve.png"),
        plot_robustness_curve(rows, "prediction_entropy", figures_dir / "robustness_entropy_curve.png"),
    ]
    write_csv(rows, results_dir / "metrics.csv")
    write_markdown_summary(rows, results_dir / "summary.md")
    report_path = write_reliability_report(rows, results_dir / "reliability_report.md", figure_paths=figure_paths)
    print(f"Wrote metrics: {results_dir / 'metrics.csv'}")
    print(f"Wrote summary: {results_dir / 'summary.md'}")
    print(f"Wrote report: {report_path}")


if __name__ == "__main__":
    main()
