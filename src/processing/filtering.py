"""Filtering utilities: bandpass placeholders, denoising, artifact reduction."""
from __future__ import annotations
import numpy as np

def moving_average(signal: np.ndarray, window_size: int = 5) -> np.ndarray:
    if window_size <= 1:
        return np.asarray(signal, dtype=float).copy()
    signal = np.asarray(signal, dtype=float)
    kernel = np.ones(window_size) / window_size
    return np.apply_along_axis(lambda row: np.convolve(row, kernel, mode="same"), -1, signal)

def bandpass_filter(signal: np.ndarray, low_hz: float = 0.5, high_hz: float = 40.0, sampling_rate: float = 125.0) -> np.ndarray:
    _ = (low_hz, high_hz, sampling_rate)
    return np.asarray(signal, dtype=float).copy()

def denoise_signal(signal: np.ndarray, window_size: int = 5) -> np.ndarray:
    return moving_average(signal, window_size=window_size)

def reduce_artifacts(signal: np.ndarray, clip_std: float = 5.0) -> np.ndarray:
    signal = np.asarray(signal, dtype=float)
    mean = float(np.mean(signal)); std = float(np.std(signal)) or 1.0
    return np.clip(signal, mean - clip_std * std, mean + clip_std * std)
