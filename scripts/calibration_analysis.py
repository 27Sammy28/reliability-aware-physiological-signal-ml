"""Run calibration-focused analysis."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from src.experiment import ExperimentConfig, run_experiment
from src.reporting import write_csv

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--synthetic', action='store_true'); parser.add_argument('--output', default='results/calibration/calibration_metrics.csv'); args=parser.parse_args(); rows=run_experiment(ExperimentConfig(use_synthetic=args.synthetic, noise_levels=(0,0.05,0.1,0.2,0.4))); keep=['noise_level','missing_rate','segment_fraction','brier','ece','calibration_slope','prediction_entropy']; write_csv([{k:r[k] for k in keep if k in r} for r in rows], args.output); print(f'Wrote calibration analysis to {args.output}')
if __name__ == '__main__': main()
