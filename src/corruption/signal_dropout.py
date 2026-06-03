"""Signal dropout corruption."""
from __future__ import annotations
import numpy as np

def signal_dropout(signal: np.ndarray, dropout_rate: float, seed: int | None = None) -> np.ndarray:
    if not 0 <= dropout_rate <= 1:
        raise ValueError("dropout_rate must be between 0 and 1")
    signal = np.asarray(signal, dtype=float); rng = np.random.default_rng(seed)
    if signal.ndim == 1:
        return np.zeros_like(signal) if rng.random() < dropout_rate else signal.copy()
    keep = (rng.random(signal.shape[0]) >= dropout_rate).astype(float)[:, None]
    return signal * keep
