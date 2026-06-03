"""Run robustness analysis."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from src.experiment import ExperimentConfig, run_experiment
from src.reporting import write_csv
from src.robustness import robustness_table

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--synthetic', action='store_true'); parser.add_argument('--output', default='results/robustness/robustness_metrics.csv'); args=parser.parse_args(); rows=run_experiment(ExperimentConfig(use_synthetic=args.synthetic, noise_levels=(0,0.05,0.1,0.2,0.4))); write_csv(robustness_table(rows,'accuracy'), args.output); print(f'Wrote robustness analysis to {args.output}')
if __name__ == '__main__': main()
