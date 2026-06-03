"""Signal corruption functions for robustness experiments."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
@dataclass(frozen=True)
class PerturbationConfig:
    noise_level: float = 0.0
    missing_rate: float = 0.0
    segment_fraction: float = 0.0
    seed: int = 42

def add_gaussian_noise(signal: np.ndarray, noise_level: float, seed: int | None = None) -> np.ndarray:
    if noise_level < 0:
        raise ValueError("noise_level must be non-negative")
    signal = np.asarray(signal, dtype=float)
    rng = np.random.default_rng(seed)
    return signal + rng.normal(0.0, noise_level * float(np.std(signal)), size=signal.shape)

def apply_random_missingness(signal: np.ndarray, missing_rate: float, seed: int | None = None) -> np.ndarray:
    if not 0 <= missing_rate <= 1:
        raise ValueError("missing_rate must be between 0 and 1")
    signal = np.asarray(signal, dtype=float)
    rng = np.random.default_rng(seed)
    return signal * (rng.random(signal.shape) >= missing_rate)

def mask_contiguous_segment(signal: np.ndarray, segment_fraction: float, seed: int | None = None) -> np.ndarray:
    if not 0 <= segment_fraction <= 1:
        raise ValueError("segment_fraction must be between 0 and 1")
    signal = np.asarray(signal, dtype=float)
    if signal.shape[-1] == 0 or segment_fraction == 0:
        return signal.copy()
    rng = np.random.default_rng(seed)
    output = signal.copy()
    length = signal.shape[-1]
    segment_length = max(1, int(round(length * segment_fraction)))
    start = int(rng.integers(0, length - segment_length + 1))
    output[..., start : start + segment_length] = 0.0
    return output

def perturb_signal(signal: np.ndarray, config: PerturbationConfig) -> np.ndarray:
    output = np.asarray(signal, dtype=float).copy()
    if config.noise_level:
        output = add_gaussian_noise(output, config.noise_level, config.seed)
    if config.missing_rate:
        output = apply_random_missingness(output, config.missing_rate, config.seed + 1)
    if config.segment_fraction:
        output = mask_contiguous_segment(output, config.segment_fraction, config.seed + 2)
    return output
