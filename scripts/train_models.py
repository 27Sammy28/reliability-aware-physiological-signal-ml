"""Train/evaluate classical ECG baselines."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from src.experiment import ExperimentConfig, run_experiment
from src.reporting import write_csv, write_markdown_summary

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--synthetic', action='store_true'); parser.add_argument('--raw-dir', default='data/raw'); parser.add_argument('--output-csv', default='results/metrics/train_models_metrics.csv'); parser.add_argument('--output-md', default='results/metrics/train_models_summary.md'); args=parser.parse_args()
    rows=run_experiment(ExperimentConfig(use_synthetic=args.synthetic, raw_dir=args.raw_dir, noise_levels=(0.0,)))
    write_csv(rows,args.output_csv); write_markdown_summary(rows,args.output_md); print(f'Wrote model metrics to {args.output_csv}')
if __name__ == '__main__': main()
