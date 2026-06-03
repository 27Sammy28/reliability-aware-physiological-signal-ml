# Project Architecture

```text
                    Kaggle MIT-BIH / Future Health Signals
                                  │
                                  ▼
                         data loading + validation
                    src/data.py        src/schema.py
                                  │
                                  ▼
                         leakage-aware preprocessing
                                  │
                                  ▼
                           baseline model training
                              src/models.py
                                  │
                                  ▼
                         perturbation stress testing
                           src/perturbations.py
                                  │
                                  ▼
                 metrics + calibration + robustness analysis
              src/metrics.py   src/calibration.py   src/results.py
                                  │
                                  ▼
                      reports, figures, and GitHub assets
             src/figures.py   scripts/generate_report.py   docs/assets/
```

## Design Principles

- Keep data out of git.
- Make every result reproducible from scripts.
- Evaluate reliability, not only accuracy.
- Treat ECG as the first testbed for broader health-signal ML.
- Maintain responsible-AI boundaries for non-clinical research use.