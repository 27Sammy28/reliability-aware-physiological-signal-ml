"""Classification, calibration, uncertainty, and robustness metrics."""

from __future__ import annotations

import math

import numpy as np


def binary_probabilities(scores: np.ndarray) -> np.ndarray:
    """Normalize model output into positive-class probabilities."""
    scores = np.asarray(scores, dtype=float)
    if scores.ndim == 2:
        return scores[:, 1] if scores.shape[1] > 1 else scores[:, 0]
    return scores


def predicted_labels(y_prob: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """Convert probabilities to binary labels."""
    return (binary_probabilities(y_prob) >= threshold).astype(int)


def confusion_counts(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5) -> dict[str, int]:
    """Return binary confusion matrix counts."""
    y_true = np.asarray(y_true, dtype=int)
    y_pred = predicted_labels(y_prob, threshold=threshold)
    return {
        "tp": int(np.sum((y_true == 1) & (y_pred == 1))),
        "tn": int(np.sum((y_true == 0) & (y_pred == 0))),
        "fp": int(np.sum((y_true == 0) & (y_pred == 1))),
        "fn": int(np.sum((y_true == 1) & (y_pred == 0))),
    }


def brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Compute binary Brier score."""
    y_true = np.asarray(y_true, dtype=float)
    y_prob = binary_probabilities(y_prob)
    if y_true.shape != y_prob.shape:
        raise ValueError("y_true and y_prob must have same shape")
    return float(np.mean((y_prob - y_true) ** 2))


def expected_calibration_error(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """Compute Expected Calibration Error using equal-width bins."""
    if n_bins <= 0:
        raise ValueError("n_bins must be positive")
    y_true = np.asarray(y_true, dtype=float)
    y_prob = binary_probabilities(y_prob)
    edges = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for idx in range(n_bins):
        lower, upper = edges[idx], edges[idx + 1]
        in_bin = (y_prob >= lower) & (y_prob <= upper if idx == n_bins - 1 else y_prob < upper)
        if np.any(in_bin):
            ece += float(np.mean(in_bin)) * abs(float(np.mean(y_true[in_bin])) - float(np.mean(y_prob[in_bin])))
    return float(ece)


def calibration_slope(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Estimate calibration slope from logit probabilities."""
    y_true = np.asarray(y_true, dtype=float)
    y_prob = np.clip(binary_probabilities(y_prob), 1e-6, 1 - 1e-6)
    if len(np.unique(y_true)) < 2:
        return math.nan
    logits = np.log(y_prob / (1 - y_prob))
    denominator = float(np.sum((logits - np.mean(logits)) ** 2))
    if denominator == 0:
        return math.nan
    return float(np.sum((logits - np.mean(logits)) * (y_true - np.mean(y_true))) / denominator)


def prediction_entropy(y_prob: np.ndarray) -> float:
    """Mean binary predictive entropy."""
    prob = np.clip(binary_probabilities(y_prob), 1e-12, 1 - 1e-12)
    entropy = -(prob * np.log2(prob) + (1 - prob) * np.log2(1 - prob))
    return float(np.mean(entropy))


def confidence_margin(y_prob: np.ndarray) -> float:
    """Mean distance from the decision boundary."""
    prob = binary_probabilities(y_prob)
    return float(np.mean(np.abs(prob - 0.5)))


def classification_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5) -> dict[str, float | int]:
    """Compute binary classification metrics with confusion counts."""
    y_true = np.asarray(y_true, dtype=int)
    counts = confusion_counts(y_true, y_prob, threshold=threshold)
    tp, tn, fp, fn = counts["tp"], counts["tn"], counts["fp"], counts["fn"]
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    specificity = tn / max(tn + fp, 1)
    negative_predictive_value = tn / max(tn + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-12)
    return {
        **counts,
        "accuracy": float((tp + tn) / max(len(y_true), 1)),
        "balanced_accuracy": float((recall + specificity) / 2),
        "precision": float(precision),
        "recall": float(recall),
        "specificity": float(specificity),
        "negative_predictive_value": float(negative_predictive_value),
        "f1": float(f1),
    }


def reliability_metrics(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> dict[str, float]:
    """Compute probability reliability and uncertainty metrics."""
    return {
        "brier": brier_score(y_true, y_prob),
        "ece": expected_calibration_error(y_true, y_prob, n_bins),
        "calibration_slope": calibration_slope(y_true, y_prob),
        "prediction_entropy": prediction_entropy(y_prob),
        "confidence_margin": confidence_margin(y_prob),
        "mean_predicted_probability": float(np.mean(binary_probabilities(y_prob))),
    }


def degradation_rate(baseline: float, perturbed: float, lower_is_better: bool = False) -> float:
    """Compute relative degradation from baseline to perturbed value."""
    if baseline == 0:
        raise ValueError("baseline must be non-zero")
    return float((perturbed - baseline) / baseline if lower_is_better else (baseline - perturbed) / baseline)


def add_baseline_deltas(rows: list[dict[str, object]], metrics: tuple[str, ...] = ("accuracy", "f1", "brier", "ece")) -> list[dict[str, object]]:
    """Add absolute deltas from the clean baseline row."""
    if not rows:
        return []
    baseline = next(
        (
            row
            for row in rows
            if float(row.get("noise_level", 0.0)) == 0.0
            and float(row.get("missing_rate", 0.0)) == 0.0
            and float(row.get("segment_fraction", 0.0)) == 0.0
        ),
        rows[0],
    )
    output = []
    for row in rows:
        updated = dict(row)
        for metric in metrics:
            if metric in row and metric in baseline:
                updated[f"delta_{metric}"] = float(row[metric]) - float(baseline[metric])
        output.append(updated)
    return output
