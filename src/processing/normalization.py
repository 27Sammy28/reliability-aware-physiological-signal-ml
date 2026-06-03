"""Normalization helpers for leakage-safe preprocessing."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class TrainOnlyStandardizer:
    mean_: np.ndarray | None = None
    std_: np.ndarray | None = None
    def fit(self, x_train: np.ndarray) -> "TrainOnlyStandardizer":
        x_train = np.asarray(x_train, dtype=float)
        self.mean_ = np.mean(x_train, axis=0)
        std = np.std(x_train, axis=0)
        self.std_ = np.where(std == 0, 1.0, std)
        return self
    def transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise RuntimeError("TrainOnlyStandardizer must be fit before transform")
        return (np.asarray(x, dtype=float) - self.mean_) / self.std_
    def fit_transform(self, x_train: np.ndarray) -> np.ndarray:
        return self.fit(x_train).transform(x_train)

def minmax_normalize(signal: np.ndarray) -> np.ndarray:
    signal = np.asarray(signal, dtype=float)
    minimum = np.min(signal); maximum = np.max(signal)
    if maximum == minimum:
        return np.zeros_like(signal)
    return (signal - minimum) / (maximum - minimum)
