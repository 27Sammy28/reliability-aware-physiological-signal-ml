"""Dataset loading and synthetic ECG generation utilities."""
from __future__ import annotations
from pathlib import Path
import numpy as np
TRAIN_CANDIDATES = ("mitbih_train.csv", "mitbih_train.csv.zip", "MITBIH_train.csv")
TEST_CANDIDATES = ("mitbih_test.csv", "mitbih_test.csv.zip", "MITBIH_test.csv")

def find_first_existing(root: str | Path, candidates: tuple[str, ...]) -> Path | None:
    root_path = Path(root)
    for name in candidates:
        direct = root_path / name
        if direct.exists():
            return direct
    for name in candidates:
        matches = sorted(root_path.rglob(name))
        if matches:
            return matches[0]
    return None

def load_mitbih_csv(raw_dir: str | Path = "data/raw") -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    raw_path = Path(raw_dir)
    train_path = find_first_existing(raw_path, TRAIN_CANDIDATES)
    test_path = find_first_existing(raw_path, TEST_CANDIDATES)
    if train_path is None or test_path is None:
        raise FileNotFoundError("MIT-BIH CSV files not found. Run scripts/download_data.py first.")
    train = np.loadtxt(train_path, delimiter=",")
    test = np.loadtxt(test_path, delimiter=",")
    return train[:, :-1], train[:, -1].astype(int), test[:, :-1], test[:, -1].astype(int)

def make_binary_task(labels: np.ndarray, positive_class: int = 1) -> np.ndarray:
    return (np.asarray(labels) == positive_class).astype(int)

def standardize_train_test(x_train: np.ndarray, x_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(x_train, axis=0)
    std = np.std(x_train, axis=0)
    std = np.where(std == 0, 1.0, std)
    return (x_train - mean) / std, (x_test - mean) / std

def synthetic_ecg_dataset(n_samples: int = 600, n_features: int = 187, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    time = np.linspace(0, 1, n_features)
    labels = rng.integers(0, 2, size=n_samples)
    signals = []
    for label in labels:
        rhythm = np.sin(2 * np.pi * (4 + label) * time)
        qrs = np.exp(-((time - (0.45 + 0.05 * label)) ** 2) / 0.0015)
        t_wave = 0.35 * np.exp(-((time - 0.72) ** 2) / 0.01)
        drift = 0.12 * np.sin(2 * np.pi * time)
        noise = rng.normal(0, 0.07, size=n_features)
        signals.append(rhythm + (1.1 + 0.5 * label) * qrs + t_wave + drift + noise)
    return np.asarray(signals), labels.astype(int)
