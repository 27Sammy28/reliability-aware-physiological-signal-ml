"""Create a corrupted synthetic signal example."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from src.corruption import PerturbationConfig, perturb_signal
from src.data import synthetic_ecg_dataset

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--noise-level', type=float, default=0.2); parser.add_argument('--output', default='results/corruption/noisy_signal_example.json'); args=parser.parse_args()
    x,_=synthetic_ecg_dataset(n_samples=2); corrupted=perturb_signal(x[0], PerturbationConfig(noise_level=args.noise_level, missing_rate=0.05, segment_fraction=0.1)); out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps({'clean_first_10': x[0][:10].tolist(), 'corrupted_first_10': corrupted[:10].tolist()}, indent=2)+'\n'); print(f'Wrote corrupted signal example to {out}')
if __name__ == '__main__': main()
