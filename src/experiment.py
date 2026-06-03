"""End-to-end reliability experiment pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from src.data import load_mitbih_csv, make_binary_task, standardize_train_test, synthetic_ecg_dataset
from src.metrics import add_baseline_deltas, classification_metrics, reliability_metrics
from src.models import LogisticRegressionGD
from src.perturbations import PerturbationConfig, perturb_signal


@dataclass(frozen=True)
class ExperimentConfig:
    raw_dir: str = "data/raw"
    use_synthetic: bool = False
    positive_class: int = 1
    noise_levels: tuple[float, ...] = (0.0, 0.05, 0.1, 0.2, 0.4)
    missing_rates: tuple[float, ...] = (0.0,)
    segment_fractions: tuple[float, ...] = (0.0,)
    n_bins: int = 10
    seed: int = 42
    max_train_samples: int | None = 5000
    max_test_samples: int | None = 2000


def load_experiment_data(config: ExperimentConfig):
    """Load either synthetic demo data or Kaggle MIT-BIH data."""
    if config.use_synthetic:
        x, y = synthetic_ecg_dataset(seed=config.seed)
        split = int(0.8 * len(y))
        return x[:split], y[:split], x[split:], y[split:]

    x_train, y_train_raw, x_test, y_test_raw = load_mitbih_csv(config.raw_dir)
    y_train = make_binary_task(y_train_raw, config.positive_class)
    y_test = make_binary_task(y_test_raw, config.positive_class)
    if config.max_train_samples:
        x_train = x_train[: config.max_train_samples]
        y_train = y_train[: config.max_train_samples]
    if config.max_test_samples:
        x_test = x_test[: config.max_test_samples]
        y_test = y_test[: config.max_test_samples]
    return x_train, y_train, x_test, y_test


def run_experiment(config: ExperimentConfig) -> list[dict[str, object]]:
    """Train a baseline model and evaluate metrics across perturbation levels."""
    x_train, y_train, x_test, y_test = load_experiment_data(config)
    x_train, x_test = standardize_train_test(x_train, x_test)
    model = LogisticRegressionGD().fit(x_train, y_train)

    rows: list[dict[str, object]] = []
    for noise_level in config.noise_levels:
        for missing_rate in config.missing_rates:
            for segment_fraction in config.segment_fractions:
                perturbation = PerturbationConfig(noise_level, missing_rate, segment_fraction, config.seed)
                probabilities = model.predict_proba(perturb_signal(x_test, perturbation))[:, 1]
                row = {
                    "model": "logistic_regression_gd",
                    "noise_level": noise_level,
                    "missing_rate": missing_rate,
                    "segment_fraction": segment_fraction,
                    **classification_metrics(y_test, probabilities),
                    **reliability_metrics(y_test, probabilities, config.n_bins),
                }
                rows.append(row)

    rows = add_baseline_deltas(rows)
    return [
        {key: round(value, 6) if isinstance(value, float) else value for key, value in row.items()}
        for row in rows
    ]
