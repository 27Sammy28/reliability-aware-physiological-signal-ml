# External Validation Plan

## Purpose

External validation is required before any health-signal ML system can be considered reliable beyond a benchmark dataset.

## Validation Stages

1. Internal synthetic smoke testing.
2. Benchmark ECG testing on downloaded MIT-BIH data.
3. Cross-record or patient-level validation where identifiers are available.
4. External ECG dataset evaluation.
5. Extension to voice/cough/respiratory audio datasets.
6. Prospective or field validation in the target public-health context.

## Required Checks

- Dataset schema validation.
- Duplicate and near-duplicate detection.
- Class balance and subgroup analysis.
- Device and acquisition condition analysis.
- Calibration and robustness under noise.
- Confidence interval reporting.
- Error analysis for overconfident incorrect predictions.

## Africa-Focused Validation Questions

- Does performance hold across languages and regions?
- Does device mismatch reduce reliability?
- Are rural and remote collection conditions represented?
- Are privacy, consent, and governance mechanisms appropriate?