"""Signal quality checks."""
from __future__ import annotations
import numpy as np

def missing_fraction(signal: np.ndarray) -> float:
    return float(np.mean(~np.isfinite(np.asarray(signal))))

def flatline_fraction(signal: np.ndarray) -> float:
    signal = np.asarray(signal, dtype=float)
    if signal.shape[-1] < 2:
        return 0.0
    return float(np.mean(np.diff(signal, axis=-1) == 0))

def quality_summary(signal: np.ndarray) -> dict[str, float]:
    signal = np.asarray(signal, dtype=float)
    return {"missing_fraction": missing_fraction(signal), "flatline_fraction": flatline_fraction(signal), "mean": float(np.mean(signal)), "std": float(np.std(signal))}
