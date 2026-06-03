"""Schema validation and manifest utilities for MIT-BIH style CSV data."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from src.data import TEST_CANDIDATES, TRAIN_CANDIDATES, find_first_existing


EXPECTED_FEATURES = 187
EXPECTED_LABELS = {0, 1, 2, 3, 4}


def file_sha256(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA-256 hash for a file."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def file_manifest(root: str | Path) -> list[dict[str, object]]:
    """Create a manifest with relative paths, byte sizes, and hashes."""
    root_path = Path(root)
    rows = []
    for path in sorted(p for p in root_path.rglob("*") if p.is_file()):
        rows.append(
            {
                "path": str(path.relative_to(root_path)),
                "size_bytes": path.stat().st_size,
                "sha256": file_sha256(path),
            }
        )
    return rows


def validate_csv_array(array: np.ndarray, name: str, expected_features: int = EXPECTED_FEATURES) -> dict[str, object]:
    """Validate a loaded MIT-BIH CSV array."""
    if array.ndim != 2:
        raise ValueError(f"{name} must be a 2D array")
    if array.shape[1] != expected_features + 1:
        raise ValueError(f"{name} expected {expected_features + 1} columns, found {array.shape[1]}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} contains non-finite values")
    labels = array[:, -1].astype(int)
    unique_labels = set(int(label) for label in np.unique(labels))
    unexpected = unique_labels - EXPECTED_LABELS
    if unexpected:
        raise ValueError(f"{name} contains unexpected labels: {sorted(unexpected)}")
    values, counts = np.unique(labels, return_counts=True)
    return {
        "name": name,
        "n_samples": int(array.shape[0]),
        "n_features": int(array.shape[1] - 1),
        "labels": {str(int(label)): int(count) for label, count in zip(values, counts)},
    }


def validate_mitbih_directory(raw_dir: str | Path = "data/raw", expected_features: int = EXPECTED_FEATURES) -> dict[str, object]:
    """Validate downloaded Kaggle MIT-BIH train/test CSV files."""
    raw_path = Path(raw_dir)
    train_path = find_first_existing(raw_path, TRAIN_CANDIDATES)
    test_path = find_first_existing(raw_path, TEST_CANDIDATES)
    if train_path is None or test_path is None:
        raise FileNotFoundError("Could not find mitbih_train.csv and mitbih_test.csv under data/raw.")
    train = np.loadtxt(train_path, delimiter=",")
    test = np.loadtxt(test_path, delimiter=",")
    return {
        "raw_dir": str(raw_path),
        "train_file": str(train_path),
        "test_file": str(test_path),
        "train_schema": validate_csv_array(train, "train", expected_features),
        "test_schema": validate_csv_array(test, "test", expected_features),
        "manifest": file_manifest(raw_path),
    }
