# Bias and Subgroup Evaluation Plan

## Goal

Evaluate whether model performance and calibration differ across clinically, demographically, geographically, or acquisition-relevant groups when metadata is available.

## Candidate Subgroups

- patient or record identifier;
- age group;
- sex or gender where ethically collected;
- device or acquisition source;
- language or dialect for speech/audio extensions;
- region or collection site;
- noise level or recording quality.

## Metrics by Subgroup

- accuracy;
- recall and specificity;
- Brier score;
- Expected Calibration Error;
- calibration slope;
- false negative and false positive counts;
- confidence margin and prediction entropy.

## Reporting Requirement

Subgroup results should be reported with sample sizes and uncertainty intervals. Small or sensitive subgroups should be handled carefully to avoid misleading claims or privacy risks.