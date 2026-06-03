# Responsible AI and Non-Clinical-Use Statement

This repository is a research and educational software project. It is not a medical device, clinical diagnostic system, triage tool, monitoring device, or substitute for professional medical judgment.

## Intended Use

- Research benchmarking for reliability-aware ECG and health-signal machine learning.
- Studying calibration, robustness, uncertainty, and signal corruption effects.
- Demonstrating reproducible ML engineering workflows for noisy observational signals.

## Not Intended For

- Clinical diagnosis or treatment decisions.
- Patient monitoring or emergency triage.
- Deployment in hospital, wearable, or public-health systems without clinical validation.
- Claims of medical performance based only on benchmark or synthetic experiments.

## Key Risks

- Dataset bias and limited representativeness.
- Train/test leakage through duplicate or patient-overlapping signals.
- Poor calibration under distribution shift.
- Overconfident predictions under noisy or missing signals.
- Device, acquisition, demographic, and clinical workflow mismatch.

## Required Before Any Clinical Translation

- Independent clinical validation.
- External dataset evaluation.
- Subgroup and bias analysis.
- Prospective evaluation under real acquisition conditions.
- Regulatory, ethical, and institutional review.