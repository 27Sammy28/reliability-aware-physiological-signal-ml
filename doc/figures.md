# Figure Workflow

Generated figures are written to `results/figures/` and ignored by git by default.

## Synthetic Demo Figures

```bash
make figures
```

or

```bash
python scripts/generate_figures.py
```

## Complete Synthetic Report

```bash
make report
```

or

```bash
python scripts/generate_report.py
```

## Real MIT-BIH Figures After Download

After configuring Kaggle credentials and downloading data:

```bash
python scripts/download_data.py
make validate-data
python scripts/generate_real_data_report.py
```

## Curated README Figures

For GitHub display, do not commit the full `results/` folder. Instead, copy only selected final images into `docs/assets/` and reference those from `README.md`.

Suggested curated assets:

- `docs/assets/class_distribution.png`
- `docs/assets/representative_waveforms.png`
- `docs/assets/reliability_diagram.png`
- `docs/assets/robustness_ece_curve.png`