"""Generate synthetic demonstration figures for the repository."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data import synthetic_ecg_dataset
from src.experiment import ExperimentConfig, run_experiment
from src.figures import (
    ensure_output_dir,
    plot_class_distribution,
    plot_corruption_example,
    plot_reliability_diagram,
    plot_representative_waveforms,
    plot_robustness_curve,
)
from src.models import LogisticRegressionGD
from src.perturbations import PerturbationConfig, perturb_signal
from src.reporting import write_csv, write_markdown_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic ECG figures and example results.")
    parser.add_argument("--output-dir", default="results/figures", help="Directory for figure PNG files.")
    parser.add_argument("--results-dir", default="results", help="Directory for example result tables.")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    figure_dir = ensure_output_dir(args.output_dir)
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    x, y = synthetic_ecg_dataset(seed=args.seed)
    rows = run_experiment(
        ExperimentConfig(
            use_synthetic=True,
            seed=args.seed,
            noise_levels=(0.0, 0.05, 0.1, 0.2, 0.4),
            missing_rates=(0.0,),
            segment_fractions=(0.0,),
        )
    )

    split = int(0.8 * len(y))
    model = LogisticRegressionGD().fit(x[:split], y[:split])
    probabilities = model.predict_proba(x[split:])[:, 1]
    corrupted = perturb_signal(x[0], PerturbationConfig(noise_level=0.25, missing_rate=0.05, segment_fraction=0.12, seed=args.seed))

    generated = [
        plot_class_distribution(y, figure_dir / "class_distribution.png"),
        plot_representative_waveforms(x, y, figure_dir / "representative_waveforms.png"),
        plot_corruption_example(x[0], corrupted, figure_dir / "corruption_example.png"),
        plot_reliability_diagram(y[split:], probabilities, figure_dir / "reliability_diagram.png"),
        plot_robustness_curve(rows, "ece", figure_dir / "robustness_ece_curve.png"),
        plot_robustness_curve(rows, "accuracy", figure_dir / "robustness_accuracy_curve.png"),
    ]

    write_csv(rows, results_dir / "synthetic_metrics.csv")
    write_markdown_summary(rows, results_dir / "synthetic_summary.md")

    print("Generated figures:")
    for path in generated:
        print(f"- {path}")
    print(f"Generated results table: {results_dir / 'synthetic_metrics.csv'}")
    print(f"Generated results summary: {results_dir / 'synthetic_summary.md'}")


if __name__ == "__main__":
    main()
