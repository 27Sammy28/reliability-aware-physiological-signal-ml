from __future__ import annotations
import numpy as np
from src.metrics import binary_probabilities

def calibration_curve(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> dict[str, np.ndarray]:
    y_true = np.asarray(y_true, dtype=float); y_prob = binary_probabilities(y_prob); edges = np.linspace(0, 1, n_bins + 1)
    confidence, empirical, counts = [], [], []
    for idx in range(n_bins):
        lower, upper = edges[idx], edges[idx + 1]
        in_bin = (y_prob >= lower) & (y_prob <= upper if idx == n_bins - 1 else y_prob < upper)
        if np.any(in_bin):
            confidence.append(float(np.mean(y_prob[in_bin]))); empirical.append(float(np.mean(y_true[in_bin]))); counts.append(int(np.sum(in_bin)))
    return {"confidence": np.asarray(confidence), "empirical": np.asarray(empirical), "counts": np.asarray(counts)}
