"""Distribution shift simulation utilities."""
from __future__ import annotations
import numpy as np

def amplitude_shift(signal: np.ndarray, scale: float = 1.0, offset: float = 0.0) -> np.ndarray:
    return np.asarray(signal, dtype=float) * scale + offset

def class_prior_subset(x: np.ndarray, y: np.ndarray, positive_fraction: float, seed: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    if not 0 <= positive_fraction <= 1:
        raise ValueError("positive_fraction must be between 0 and 1")
    x = np.asarray(x); y = np.asarray(y); rng = np.random.default_rng(seed)
    pos = np.where(y == 1)[0]; neg = np.where(y == 0)[0]
    total = min(len(y), 2 * min(len(pos), len(neg)))
    n_pos = min(len(pos), int(round(total * positive_fraction))); n_neg = min(len(neg), total - n_pos)
    selected = np.concatenate([rng.choice(pos, n_pos, replace=False), rng.choice(neg, n_neg, replace=False)])
    rng.shuffle(selected)
    return x[selected], y[selected]
