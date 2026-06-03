"""Exploratory data analysis helpers for ECG signals."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

def signal_summary(x: np.ndarray, y: np.ndarray) -> dict[str, object]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)
    labels, counts = np.unique(y, return_counts=True)
    return {"n_samples": int(x.shape[0]), "n_features": int(x.shape[1]) if x.ndim > 1 else 1, "signal_mean": float(np.mean(x)), "signal_std": float(np.std(x)), "signal_min": float(np.min(x)), "signal_max": float(np.max(x)), "class_counts": {str(label): int(count) for label, count in zip(labels, counts)}}

def representative_signal(x: np.ndarray, y: np.ndarray, label: int | None = None) -> list[float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)
    if label is not None and np.any(y == label):
        return np.mean(x[y == label], axis=0).round(6).tolist()
    return np.mean(x, axis=0).round(6).tolist()

def write_eda_report(summary: dict[str, object], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n")
