"""Figure generation utilities for ECG reliability experiments."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from src.calibration import calibration_curve


def _prepare_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    return plt


def ensure_output_dir(output_dir: str | Path) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def plot_class_distribution(y: np.ndarray, output_path: str | Path) -> Path:
    """Plot class counts."""
    plt = _prepare_matplotlib()
    labels, counts = np.unique(y, return_counts=True)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([str(label) for label in labels], counts, color="#4C72B0")
    ax.set_title("Class Distribution")
    ax.set_xlabel("Class Label")
    ax.set_ylabel("Count")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def plot_representative_waveforms(x: np.ndarray, y: np.ndarray, output_path: str | Path, max_classes: int = 5) -> Path:
    """Plot mean ECG waveform per class."""
    plt = _prepare_matplotlib()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    labels = np.unique(y)[:max_classes]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for label in labels:
        class_waveform = np.mean(x[y == label], axis=0)
        ax.plot(class_waveform, label=f"Class {label}", linewidth=1.6)
    ax.set_title("Representative ECG Waveforms by Class")
    ax.set_xlabel("Time Index")
    ax.set_ylabel("Amplitude")
    ax.legend(loc="best")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def plot_corruption_example(clean: np.ndarray, corrupted: np.ndarray, output_path: str | Path) -> Path:
    """Plot clean vs corrupted ECG signal."""
    plt = _prepare_matplotlib()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(clean, label="Clean", linewidth=1.8)
    ax.plot(corrupted, label="Corrupted", linewidth=1.2, alpha=0.8)
    ax.set_title("Signal Corruption Example")
    ax.set_xlabel("Time Index")
    ax.set_ylabel("Amplitude")
    ax.legend(loc="best")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def plot_reliability_diagram(y_true: np.ndarray, y_prob: np.ndarray, output_path: str | Path, n_bins: int = 10) -> Path:
    """Plot a reliability diagram from labels and predicted probabilities."""
    plt = _prepare_matplotlib()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    curve = calibration_curve(y_true, y_prob, n_bins=n_bins)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot([0, 1], [0, 1], linestyle="--", color="black", label="Perfect calibration")
    ax.plot(curve["confidence"], curve["empirical"], marker="o", color="#55A868", label="Model")
    ax.set_title("Reliability Diagram")
    ax.set_xlabel("Mean Predicted Probability")
    ax.set_ylabel("Empirical Positive Rate")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc="best")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def plot_robustness_curve(rows: list[dict[str, object]], metric: str, output_path: str | Path) -> Path:
    """Plot metric value across noise levels from experiment rows."""
    plt = _prepare_matplotlib()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    grouped: dict[float, list[float]] = {}
    for row in rows:
        if float(row.get("missing_rate", 0.0)) != 0.0 or float(row.get("segment_fraction", 0.0)) != 0.0:
            continue
        noise_level = float(row["noise_level"])
        grouped.setdefault(noise_level, []).append(float(row[metric]))

    noise_levels = sorted(grouped)
    values = [float(np.mean(grouped[level])) for level in noise_levels]

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(noise_levels, values, marker="o", color="#C44E52")
    ax.set_title(f"Robustness Curve: {metric}")
    ax.set_xlabel("Noise Level")
    ax.set_ylabel(metric)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output
