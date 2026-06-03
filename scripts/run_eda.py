"""Run ECG exploratory data analysis."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.data import load_mitbih_csv, synthetic_ecg_dataset
from src.eda import representative_signal, signal_summary, write_eda_report

def main() -> None:
    parser = argparse.ArgumentParser(description="Run EDA for ECG data.")
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--output", default="results/eda_summary.json")
    args = parser.parse_args()
    if args.synthetic:
        x, y = synthetic_ecg_dataset()
    else:
        x_train, y_train, _, _ = load_mitbih_csv(args.raw_dir)
        x, y = x_train, y_train
    summary = signal_summary(x, y)
    summary["representative_signal_first_10"] = representative_signal(x, y)[:10]
    write_eda_report(summary, args.output)
    print(f"Wrote EDA summary to {args.output}")
if __name__ == "__main__":
    main()
