"""Reliability-aware health ML protocol checklist."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class ReliabilityProtocol:
    leakage_safe_split: bool = True
    train_only_preprocessing: bool = True
    perturbation_sweep: bool = True
    calibration_metrics: bool = True
    distribution_shift_test: bool = True
    uncertainty_reporting: bool = True
    def checklist(self) -> list[str]:
        items = []
        if self.leakage_safe_split:
            items.append("Use leakage-safe record-level or patient-level splits when identifiers exist.")
        if self.train_only_preprocessing:
            items.append("Fit preprocessing only on training data.")
        if self.perturbation_sweep:
            items.append("Evaluate noise, missingness, and contiguous segment corruption.")
        if self.calibration_metrics:
            items.append("Report Brier score, ECE, calibration slope, and reliability diagrams.")
        if self.distribution_shift_test:
            items.append("Stress test distribution shift across records, devices, or subsets.")
        if self.uncertainty_reporting:
            items.append("Report uncertainty using bootstrap confidence intervals where possible.")
        return items
