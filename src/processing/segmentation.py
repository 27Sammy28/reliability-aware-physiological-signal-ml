"""Heartbeat extraction, windowing, and sequence generation."""
from __future__ import annotations
import numpy as np

def sliding_windows(signal: np.ndarray, window_size: int, step: int) -> np.ndarray:
    signal = np.asarray(signal, dtype=float)
    if window_size <= 0 or step <= 0:
        raise ValueError("window_size and step must be positive")
    if signal.ndim != 1:
        raise ValueError("sliding_windows expects a one-dimensional signal")
    if len(signal) < window_size:
        return np.empty((0, window_size))
    return np.asarray([signal[start:start + window_size] for start in range(0, len(signal) - window_size + 1, step)])

def heartbeat_extraction(signal: np.ndarray, peaks: np.ndarray, radius: int = 50) -> np.ndarray:
    signal = np.asarray(signal, dtype=float); windows = []
    for peak in np.asarray(peaks, dtype=int):
        start = peak - radius; end = peak + radius + 1
        if start >= 0 and end <= len(signal):
            windows.append(signal[start:end])
    return np.asarray(windows)

def sequence_generation(signal: np.ndarray, window_size: int, step: int) -> np.ndarray:
    return sliding_windows(signal, window_size=window_size, step=step)
