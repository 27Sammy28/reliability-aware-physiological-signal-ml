"""Run ECG reliability experiments."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.experiment import ExperimentConfig, run_experiment
from src.reporting import write_csv, write_markdown_summary

def parse_float_list(value: str) -> tuple[float, ...]:
    return tuple(float(item.strip()) for item in value.split(",") if item.strip())
def main() -> None:
    parser = argparse.ArgumentParser(description="Run reliability-aware ECG ML experiments.")
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--positive-class", type=int, default=1)
    parser.add_argument("--noise-levels", default="0,0.05,0.1,0.2,0.4")
    parser.add_argument("--missing-rates", default="0")
    parser.add_argument("--segment-fractions", default="0")
    parser.add_argument("--output-csv", default="results/metrics.csv")
    parser.add_argument("--output-md", default="results/summary.md")
    args = parser.parse_args()
    config = ExperimentConfig(raw_dir=args.raw_dir, use_synthetic=args.synthetic, positive_class=args.positive_class, noise_levels=parse_float_list(args.noise_levels), missing_rates=parse_float_list(args.missing_rates), segment_fractions=parse_float_list(args.segment_fractions))
    rows = run_experiment(config)
    write_csv(rows, args.output_csv)
    write_markdown_summary(rows, args.output_md)
    print(f"Wrote {len(rows)} experiment rows to {args.output_csv} and {args.output_md}")
if __name__ == "__main__":
    main()
