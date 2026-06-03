# Reliability-Aware ECG and Health Signal Machine Learning

Advanced GitHub research scaffold for reliability-aware machine learning on noisy health signals. The project starts with ECG classification using the Kaggle MIT-BIH dataset and is designed to extend toward voice, speech, and language biomarkers for health assessment.

## Research Direction

This repository is aligned with health-signal research at the intersection of signal processing, speech science, and machine learning, including the broader direction associated with Visar Berisha at Arizona State University. In the proposed academic pathway, Berisha is framed as a prospective supervisor whose expertise could provide training for reliable inference from noisy health signals.

The current ECG implementation is a first testbed for calibration, robustness, and reliability. The long-term direction extends toward voice, cough, respiratory audio, speech, and language signals for Africa-focused public-health surveillance, including future Africa CDC-style applications for tuberculosis, respiratory infections, and emerging outbreak detection.

## Long-Term Africa CDC Pathway

The guiding research statement is:

> My long-term research goal is to develop reliable machine learning methods for extracting actionable health information from noisy observational signals, with applications ranging from physiological monitoring to public-health surveillance systems in Africa.

See `docs/africa_cdc_research_pathway.md` for the full pathway from ECG reliability experiments to voice/audio-based disease surveillance.

## Common Commands

```bash
make test          # run unit tests
make smoke         # run a small synthetic experiment
make figures       # generate synthetic figures
make report        # generate metrics, figures, and reliability report
make validate-data # validate downloaded Kaggle files
make clean         # remove generated local artifacts
```

## Quick Start

Run without Kaggle data using synthetic ECG-like signals:

```bash
python scripts/run_experiment.py --synthetic
```

Download Kaggle data after configuring credentials:

```bash
export KAGGLE_USERNAME="Sammy2278"
export KAGGLE_KEY="KGAT_cfa65405ad11560c1b799a782495a0ad"
python scripts/download_data.py
python scripts/validate_data.py
```

Run EDA:

```bash
python scripts/run_eda.py --synthetic
```

Run tests:

```bash
python -m pytest -q
```

## Project Structure

```text
configs/        experiment settings
data/           ignored raw and processed data folders
docs/           dataset card, model card, research framing
notebooks/      EDA guide and future notebooks
results/        ignored generated outputs
scripts/        command-line runners
src/            reusable ML and reliability modules
tests/          unit and smoke tests
```


## Figures and Results

Generate synthetic demo figures and result tables:

```bash
python scripts/generate_figures.py
```

Generate real MIT-BIH figures after downloading the dataset:

```bash
python scripts/generate_real_data_report.py
```

Generate a complete synthetic metrics/results report:

```bash
python scripts/generate_report.py
```

This creates local outputs under `results/`, including class distribution, representative ECG waveforms, corruption examples, reliability diagrams, and robustness curves. The generated files are ignored by git by default so the repository stays lightweight.

Recommended README figures after generation:

- `results/figures/class_distribution.png`
- `results/figures/representative_waveforms.png`
- `results/figures/corruption_example.png`
- `results/figures/reliability_diagram.png`
- `results/figures/robustness_ece_curve.png`
- `results/figures/robustness_accuracy_curve.png`


## Figure Gallery

The following synthetic demonstration figures are curated in `docs/assets/` for GitHub display. They illustrate the intended result style before running the workflow on downloaded MIT-BIH data.

### 1. Class Distribution

![Class distribution](docs/assets/class_distribution.png)

Shows the label balance in the synthetic ECG demonstration dataset. For real MIT-BIH experiments, this helps identify class imbalance before model training.

### 2. Representative ECG Waveforms by Class

![Representative ECG waveforms](docs/assets/representative_waveforms.png)

Shows mean ECG waveform morphology by class. This gives a quick visual check of whether classes differ in signal shape.

### 3. Clean vs Corrupted Signal Example

![Clean vs corrupted ECG signal](docs/assets/corruption_example.png)

Shows how the robustness pipeline degrades a clean signal using noise, missingness, and temporal masking.

### 4. Reliability Diagram

![Reliability diagram](docs/assets/reliability_diagram.png)

Compares predicted probability confidence against empirical outcome frequency. This is central to calibration-aware evaluation.

### 5. Robustness Curve for ECE

![Robustness ECE curve](docs/assets/robustness_ece_curve.png)

Shows how calibration error changes as signal corruption increases. Rising ECE indicates worsening probability reliability.

### 6. Robustness Curve for Accuracy

![Robustness accuracy curve](docs/assets/robustness_accuracy_curve.png)

Shows how predictive performance changes under progressively noisier signal conditions.

## Core Metrics

- Accuracy, precision, recall, F1-score
- Brier score
- Expected Calibration Error
- Calibration slope
- Degradation rate under perturbation
- Signal summary statistics for EDA
- Confusion matrix counts: TP, TN, FP, FN
- Balanced accuracy, specificity, and negative predictive value
- Prediction entropy and confidence margin
- Delta metrics from clean baseline

## Data Policy

Do not commit raw Kaggle files, processed datasets, credentials, generated plots, or large result artifacts. The repository tracks code, configs, docs, and tests.
## Responsible AI and Non-Clinical Use

This repository is for research and education only. It is not a clinical diagnostic system, medical device, triage tool, or substitute for medical judgment. See `docs/responsible_ai_statement.md` for the full statement.

## Citation and License

- Citation metadata: `CITATION.cff`
- License: `LICENSE`
