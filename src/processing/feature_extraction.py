"""Feature extraction helpers for classical ML baselines."""
from __future__ import annotations
import numpy as np

def statistical_features(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[None, :]
    return np.column_stack([np.mean(x, axis=1), np.std(x, axis=1), np.min(x, axis=1), np.max(x, axis=1), np.median(x, axis=1), np.percentile(x, 25, axis=1), np.percentile(x, 75, axis=1)])

def waveform_features(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return x.reshape(1, -1) if x.ndim == 1 else x
